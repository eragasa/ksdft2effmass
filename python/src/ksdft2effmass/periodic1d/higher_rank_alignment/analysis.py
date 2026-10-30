"""Request-bound producer for the analytic higher-rank periodic-1D calculation."""

from __future__ import annotations

import math
from fractions import Fraction
from typing import final

import numpy as np
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.numerics.numpy.validation import (
    immutable_complex128_array,
    immutable_float64_array,
)
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesDefinition,
    NumpyBatchedComplexUnitaryProcrustesResult,
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray, RealArray
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransportBackendFailure,
    ClosedLoopPolarFrameTransporter,
    FinitePeriodicMeshFrameInventory,
)
from projectkoios.physkit.solidstate.tb import (
    FinitePeriodicMatrixFourierTensorEvaluator,
    FinitePeriodicMatrixFourierTransformer,
)
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from ksdft2effmass.analysis.matrix_field.diagnostics import (
    MatrixFieldErrorAnalyzer,
    MatrixFieldHermiticityAnalyzer,
    MatrixFieldIsometryAnalyzer,
    MatrixProjectorFieldAnalyzer,
    ScalarRefinementAnalyzer,
)

from .calculation import Periodic1DHigherRankAlignmentCalculationRequest
from .calculation_result import Periodic1DHigherRankAlignmentCalculationResult
from .channel_analysis import (
    Periodic1DHigherRankChannelAnalysisRequest,
    Periodic1DHigherRankChannelAnalyzer,
)
from .channel_results import (
    Periodic1DHigherRankChannelMeshResult,
    Periodic1DHigherRankMeshCalculationResult,
)
from .definition import (
    Periodic1DHigherRankAlignmentBackendExceptionCode,
    Periodic1DHigherRankAlignmentChannel,
    Periodic1DHigherRankAlignmentStatus,
    Periodic1DHigherRankGlobalUnitaryDownstreamApplicability,
)
from .diagnostics import (
    Periodic1DHigherRankModelDiagnostics,
    Periodic1DHigherRankProcrustesDiagnostics,
)
from .model import (
    Periodic1DHigherRankAnalyticCase,
    Periodic1DHigherRankAnalyticCaseConstructor,
)
from .provenance import Periodic1DHigherRankEvaluationIndependenceResult
from .refinement import (
    Periodic1DHigherRankRefinementAnalysisRequest,
    Periodic1DHigherRankRefinementAnalyzer,
)
from .result import (
    Periodic1DHigherRankAlignmentStatusResult,
    Periodic1DHigherRankAlignmentTransportBackendFailureResult,
    Periodic1DHigherRankAlignmentTransportOwnerResult,
)

_GlobalApplicability = Periodic1DHigherRankGlobalUnitaryDownstreamApplicability
_INAPPLICABLE_GLOBAL_RANK = _GlobalApplicability.INAPPLICABLE_AGGREGATE_RANK_DEFICIENT


def _coordinates(mesh_size: int, offset: float) -> RealArray:
    values = np.asarray(
        -0.5 + (np.arange(mesh_size, dtype=np.float64) + offset) / mesh_size,
        dtype=np.float64,
    )
    return immutable_float64_array(values, "coordinates")


def _adjoint(value: ComplexArray) -> ComplexArray:
    return np.swapaxes(value.conjugate(), -1, -2)


def _apply_right_basis_change(
    matrices: ComplexArray,
    right_unitaries: ComplexArray,
) -> ComplexArray:
    return np.asarray(
        _adjoint(right_unitaries) @ matrices @ right_unitaries,
        dtype=np.complex128,
    )


def _status(
    request: Periodic1DHigherRankAlignmentCalculationRequest,
    mesh_size: int,
    channel: Periodic1DHigherRankAlignmentChannel,
    status: Periodic1DHigherRankAlignmentStatus,
    backend_exception_code: (
        Periodic1DHigherRankAlignmentBackendExceptionCode | None
    ) = None,
) -> Periodic1DHigherRankAlignmentStatusResult:
    applicability = None
    if (
        channel is Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY
        and status is Periodic1DHigherRankAlignmentStatus.QUALIFIED
    ):
        applicability = (
            Periodic1DHigherRankGlobalUnitaryDownstreamApplicability.APPLICABLE
        )
    elif (
        channel is Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY
        and status is Periodic1DHigherRankAlignmentStatus.AGGREGATE_RANK_DEFICIENT
    ):
        applicability = _INAPPLICABLE_GLOBAL_RANK
    return Periodic1DHigherRankAlignmentStatusResult(
        case_identity=request.case_identity,
        retained_rank=request.retained_rank,
        circuit_depth=request.circuit_depth,
        construction_mesh_size=mesh_size,
        channel=channel,
        status=status,
        global_unitary_downstream_applicability=applicability,
        backend_exception_code=backend_exception_code,
    )


def _unavailable_channel_result(
    status: Periodic1DHigherRankAlignmentStatusResult,
) -> Periodic1DHigherRankChannelMeshResult:
    return Periodic1DHigherRankChannelMeshResult(
        status=status,
        transform_backend_identifier=None,
        transform_backend_version=None,
        fourier_representative_count=None,
        fourier_representative_inventory_ordered_unique=None,
        fourier_inversion_closed=None,
        fourier_index_bijection_pass=None,
        no_nyquist_disposition=None,
        coefficient_translations=np.empty(0, dtype=np.int64),
        block_raw_frobenius_norms=np.empty(0, dtype=np.float64),
        block_normalized_frobenius_norms=np.empty(0, dtype=np.float64),
        frame_recovery=None,
        known_frame_recovery_pass=None,
        represented_operator_recovery=None,
        known_operator_recovery_pass=None,
        reconstruction=None,
        reconstruction_pass=None,
        interpolation=None,
        final_interpolation_operator_pass=None,
        final_interpolation_spectrum_pass=None,
        parseval_relative_defect=None,
        parseval_pass=None,
        ordinary_hermiticity_defect=None,
        ordinary_hermiticity_pass=None,
        twisted_cyclic_hermiticity_defect=None,
        twisted_cyclic_hermiticity_pass=None,
        supports=(),
        maximum_tail_increase=None,
        all_tail_monotonicity_checks_pass=None,
    )


def _procrustes_integrity(
    source: ComplexArray,
    target: ComplexArray,
    result: NumpyBatchedComplexUnitaryProcrustesResult,
) -> tuple[RealArray, float, float, float, float]:
    rank = result.right_unitary_completions.shape[-1]
    right = result.right_unitary_completions
    residuals = np.asarray(
        result.optimal_residual_frobenius_norms / math.sqrt(rank),
        dtype=np.float64,
    )
    identity = np.eye(rank, dtype=np.complex128)
    unitary = float(
        np.max(np.linalg.norm(_adjoint(right) @ right - identity, axis=(-2, -1)))
    )
    cross = _adjoint(source) @ target
    stationary = _adjoint(right) @ cross
    stationarity = float(
        np.max(np.linalg.norm(stationary - _adjoint(stationary), axis=(-2, -1)))
        / math.sqrt(rank)
    )
    direct_objectives = (
        np.sum(
            np.abs(source @ right - target) ** 2,
            axis=(-2, -1),
            dtype=np.float64,
        )
        / rank
    )
    covariance_objectives = 2.0 - (2.0 / rank) * np.real(
        np.trace(_adjoint(cross) @ right, axis1=-2, axis2=-1)
    )
    objective_identity = float(
        np.max(np.abs(direct_objectives - covariance_objectives))
    )
    hermitian_part = 0.5 * (stationary + _adjoint(stationary))
    minimum_eigenvalues = np.linalg.eigvalsh(hermitian_part)[..., 0]
    psd_defect = float(max(0.0, -float(np.min(minimum_eigenvalues))))
    return residuals, unitary, stationarity, objective_identity, psd_defect


def _procrustes_backend_exception_code(
    exception: ArithmeticError | RuntimeError | ValueError,
) -> Periodic1DHigherRankAlignmentBackendExceptionCode:
    if isinstance(exception, FloatingPointError):
        return Periodic1DHigherRankAlignmentBackendExceptionCode.ARITHMETIC_NONFINITE
    if isinstance(exception, (np.linalg.LinAlgError, RuntimeError)):
        return Periodic1DHigherRankAlignmentBackendExceptionCode.NONCONVERGENCE
    return Periodic1DHigherRankAlignmentBackendExceptionCode.VALIDATION_FAILED


def _failed_procrustes_record(
    *,
    request: Periodic1DHigherRankAlignmentCalculationRequest,
    channel: Periodic1DHigherRankAlignmentChannel,
    selection_mesh_size: int,
    exception: ArithmeticError | RuntimeError | ValueError,
) -> Periodic1DHigherRankProcrustesDiagnostics:
    status = Periodic1DHigherRankAlignmentStatusResult(
        case_identity=request.case_identity,
        retained_rank=request.retained_rank,
        circuit_depth=request.circuit_depth,
        construction_mesh_size=selection_mesh_size,
        channel=channel,
        status=Periodic1DHigherRankAlignmentStatus.NUMERICALLY_UNRESOLVED,
        global_unitary_downstream_applicability=None,
        backend_exception_code=_procrustes_backend_exception_code(exception),
    )
    return Periodic1DHigherRankProcrustesDiagnostics(
        status=status,
        selection_mesh_size=selection_mesh_size,
        cross_singular_values=np.empty((0, request.retained_rank), dtype=np.float64),
        numerical_ranks=np.empty(0, dtype=np.int64),
        applied_rank_cutoffs=np.empty(0, dtype=np.float64),
        rank_margins=np.empty(0, dtype=np.float64),
        spectral_condition_numbers=(),
        deficient_point_indices=(),
        deficient_point_count=0,
        normalized_optimal_residuals=np.empty(0, dtype=np.float64),
        normalized_objective_maximum=None,
        normalized_objective_rms=None,
        minimum_rank_margin=None,
        maximum_unitarity_defect=None,
        maximum_stationarity_defect=None,
        maximum_objective_identity_defect=None,
        maximum_psd_defect=None,
        selected_global_right_unitary=None,
        backend_identifier=None,
        backend_version=None,
    )


def _procrustes_record(
    *,
    request: Periodic1DHigherRankAlignmentCalculationRequest,
    channel: Periodic1DHigherRankAlignmentChannel,
    selection_mesh_size: int,
    source: ComplexArray,
    target: ComplexArray,
    result: NumpyBatchedComplexUnitaryProcrustesResult,
) -> Periodic1DHigherRankProcrustesDiagnostics:
    full_rank = bool(np.all(result.full_rank))
    residuals, unitarity, stationarity, objective_identity, psd = _procrustes_integrity(
        source, target, result
    )
    integrity_passes = (
        max(
            unitarity,
            stationarity,
            objective_identity,
            psd,
        )
        <= request.controls.alignment_integrity_tolerance
    )
    if channel is Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY:
        outcome = (
            Periodic1DHigherRankAlignmentStatus.AGGREGATE_RANK_DEFICIENT
            if not full_rank
            else (
                Periodic1DHigherRankAlignmentStatus.QUALIFIED
                if integrity_passes
                else Periodic1DHigherRankAlignmentStatus.INTEGRITY_FAILED
            )
        )
    else:
        outcome = (
            Periodic1DHigherRankAlignmentStatus.POINTWISE_RANK_DEFICIENT
            if not full_rank
            else (
                Periodic1DHigherRankAlignmentStatus.QUALIFIED
                if integrity_passes
                else Periodic1DHigherRankAlignmentStatus.INTEGRITY_FAILED
            )
        )
    selected = None
    if (
        channel is Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY
        and outcome is Periodic1DHigherRankAlignmentStatus.QUALIFIED
    ):
        selected = ComplexMatrixQuantity(
            np.asarray(result.right_unitary_completions[0], dtype=np.complex128),
            Unitless(),
        )
    if result.backend_identifier is None or result.backend_version is None:
        raise ValueError("nonempty Procrustes selection requires backend evidence")
    return Periodic1DHigherRankProcrustesDiagnostics(
        status=_status(request, selection_mesh_size, channel, outcome),
        selection_mesh_size=selection_mesh_size,
        cross_singular_values=np.asarray(
            result.cross_singular_values, dtype=np.float64
        ),
        numerical_ranks=np.asarray(result.numerical_ranks, dtype=np.int64),
        applied_rank_cutoffs=np.asarray(result.applied_rank_cutoffs, dtype=np.float64),
        rank_margins=np.asarray(
            result.cross_singular_values[..., -1] - result.applied_rank_cutoffs,
            dtype=np.float64,
        ),
        spectral_condition_numbers=tuple(
            float(values[0] / values[-1])
            if rank == request.retained_rank and values[-1] > cutoff
            else None
            for values, rank, cutoff in zip(
                result.cross_singular_values,
                result.numerical_ranks,
                result.applied_rank_cutoffs,
                strict=True,
            )
        ),
        deficient_point_indices=(
            tuple(int(index) for index in np.flatnonzero(~result.full_rank))
            if channel is Periodic1DHigherRankAlignmentChannel.POINTWISE_UNITARY
            else ()
        ),
        deficient_point_count=(
            int(np.count_nonzero(~result.full_rank))
            if channel is Periodic1DHigherRankAlignmentChannel.POINTWISE_UNITARY
            else 0
        ),
        normalized_optimal_residuals=residuals,
        normalized_objective_maximum=float(np.max(residuals)),
        normalized_objective_rms=float(np.sqrt(np.mean(residuals**2))),
        minimum_rank_margin=float(
            np.min(result.cross_singular_values[..., -1] - result.applied_rank_cutoffs)
        ),
        maximum_unitarity_defect=unitarity,
        maximum_stationarity_defect=stationarity,
        maximum_objective_identity_defect=objective_identity,
        maximum_psd_defect=psd,
        selected_global_right_unitary=selected,
        backend_identifier=result.backend_identifier,
        backend_version=result.backend_version,
    )


@final
class Periodic1DHigherRankEvaluationIndependenceAnalyzer:
    """Derive exact mesh separation and selection-input provenance."""

    __slots__ = ("_request",)

    def __init__(
        self,
        request: Periodic1DHigherRankAlignmentCalculationRequest,
    ) -> None:
        """Bind one complete immutable higher-rank calculation request."""
        if type(request) is not Periodic1DHigherRankAlignmentCalculationRequest:
            raise TypeError(
                "request must be Periodic1DHigherRankAlignmentCalculationRequest"
            )
        self._request = request

    def execute(self) -> Periodic1DHigherRankEvaluationIndependenceResult:
        """Return exact rational mesh and selection provenance."""
        configuration = self._request.configuration
        denominator = configuration.evaluation_shift_denominator
        numerator = configuration.evaluation_shift_numerator
        evaluation_size = configuration.evaluation_mesh_size
        evaluation_coordinates = {
            Fraction(index * denominator + numerator, evaluation_size * denominator)
            for index in range(evaluation_size)
        }
        construction_evaluation_disjoint = all(
            evaluation_coordinates.isdisjoint(
                Fraction(index, mesh_size) for index in range(mesh_size)
            )
            for mesh_size in configuration.construction_mesh_sizes
        )
        evaluation_mesh_excluded_from_selection = (
            evaluation_size != configuration.global_unitary_selection_mesh_size
            and evaluation_size not in configuration.construction_mesh_sizes
        )
        return Periodic1DHigherRankEvaluationIndependenceResult(
            construction_mesh_sizes=configuration.construction_mesh_sizes,
            evaluation_mesh_size=evaluation_size,
            evaluation_shift_numerator=numerator,
            evaluation_shift_denominator=denominator,
            global_selection_mesh_size=(
                configuration.global_unitary_selection_mesh_size
            ),
            pointwise_selection_mesh_sizes=configuration.construction_mesh_sizes,
            construction_evaluation_disjoint=construction_evaluation_disjoint,
            evaluation_mesh_excluded_from_selection=(
                evaluation_mesh_excluded_from_selection
            ),
        )


@final
class Periodic1DHigherRankAlignmentAnalyzer:
    """Calculate one complete rank/depth case using explicit upstream owners.

    The action binds its immutable request and all numerical collaborators at
    construction. :meth:`execute` therefore has no arguments and performs no hidden
    configuration or collaborator discovery.
    """

    __slots__ = (
        "_request",
        "_procrustes_solver",
        "_transporter",
        "_fourier_transformer",
        "_fourier_evaluator",
        "_scalar_refinement_analyzer",
    )

    def __init__(
        self,
        *,
        request: Periodic1DHigherRankAlignmentCalculationRequest,
        procrustes_solver: NumpyBatchedComplexUnitaryProcrustesSolver,
        transporter: ClosedLoopPolarFrameTransporter,
        fourier_transformer: FinitePeriodicMatrixFourierTransformer,
        fourier_evaluator: FinitePeriodicMatrixFourierTensorEvaluator,
        scalar_refinement_analyzer: ScalarRefinementAnalyzer,
    ) -> None:
        """Bind the exact request and canonical numerical owners."""
        if type(request) is not Periodic1DHigherRankAlignmentCalculationRequest:
            raise TypeError(
                "request must be Periodic1DHigherRankAlignmentCalculationRequest"
            )
        if type(procrustes_solver) is not NumpyBatchedComplexUnitaryProcrustesSolver:
            raise TypeError(
                "procrustes_solver must be the canonical NumPy batched solver"
            )
        if type(transporter) is not ClosedLoopPolarFrameTransporter:
            raise TypeError("transporter must be ClosedLoopPolarFrameTransporter")
        if type(fourier_transformer) is not FinitePeriodicMatrixFourierTransformer:
            raise TypeError(
                "fourier_transformer must be the PhysKit finite-periodic owner"
            )
        if type(fourier_evaluator) is not FinitePeriodicMatrixFourierTensorEvaluator:
            raise TypeError(
                "fourier_evaluator must be the PhysKit finite-periodic evaluator"
            )
        if type(scalar_refinement_analyzer) is not ScalarRefinementAnalyzer:
            raise TypeError(
                "scalar_refinement_analyzer must be the KSD refinement owner"
            )
        self._request = request
        self._procrustes_solver = procrustes_solver
        self._transporter = transporter
        self._fourier_transformer = fourier_transformer
        self._fourier_evaluator = fourier_evaluator
        self._scalar_refinement_analyzer = scalar_refinement_analyzer

    def execute(self) -> Periodic1DHigherRankAlignmentCalculationResult:
        """Produce the complete typed calculation for the bound rank/depth case."""
        request = self._request
        model = Periodic1DHigherRankAnalyticCaseConstructor(
            retained_rank=request.retained_rank,
            circuit_depth=request.circuit_depth,
        ).execute()
        global_selection = self._global_selection(model)
        meshes = tuple(
            self._mesh_result(model, mesh_size, global_selection)
            for mesh_size in request.configuration.construction_mesh_sizes
        )
        refinement = Periodic1DHigherRankRefinementAnalyzer(
            request=Periodic1DHigherRankRefinementAnalysisRequest(
                calculation_request=request,
                meshes=meshes,
            ),
            scalar_refinement_analyzer=self._scalar_refinement_analyzer,
        ).execute()
        evaluation_independence = Periodic1DHigherRankEvaluationIndependenceAnalyzer(
            request
        ).execute()
        return Periodic1DHigherRankAlignmentCalculationResult(
            request=request,
            global_selection=global_selection,
            meshes=meshes,
            evaluation_independence=evaluation_independence,
            block_refinements=refinement.blocks,
            scalar_refinements=refinement.scalars,
        )

    def _solve(
        self,
        source: ComplexArray,
        target: ComplexArray,
    ) -> NumpyBatchedComplexUnitaryProcrustesResult:
        definition = NumpyBatchedComplexUnitaryProcrustesDefinition.from_arrays(
            source,
            target,
            self._request.configuration.owner_transport_tolerance(),
        )
        return self._procrustes_solver.solve(definition)

    def _global_selection(
        self,
        model: Periodic1DHigherRankAnalyticCase,
    ) -> Periodic1DHigherRankProcrustesDiagnostics:
        mesh_size = self._request.configuration.global_unitary_selection_mesh_size
        coordinates = _coordinates(mesh_size, 0.0)
        source_frames = model.attacked_frames(coordinates)
        target_frames = model.reference_frames(coordinates)
        scale = math.sqrt(mesh_size)
        source = np.asarray(
            source_frames.reshape(
                1, mesh_size * model.ambient_dimension, model.retained_rank
            )
            / scale,
            dtype=np.complex128,
        )
        target = np.asarray(
            target_frames.reshape(
                1, mesh_size * model.ambient_dimension, model.retained_rank
            )
            / scale,
            dtype=np.complex128,
        )
        try:
            result = self._solve(source, target)
        except (ArithmeticError, RuntimeError, ValueError) as exception:
            return _failed_procrustes_record(
                request=self._request,
                channel=Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY,
                selection_mesh_size=mesh_size,
                exception=exception,
            )
        return _procrustes_record(
            request=self._request,
            channel=Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY,
            selection_mesh_size=mesh_size,
            source=source,
            target=target,
            result=result,
        )

    def _mesh_result(
        self,
        model: Periodic1DHigherRankAnalyticCase,
        mesh_size: int,
        global_selection: Periodic1DHigherRankProcrustesDiagnostics,
    ) -> Periodic1DHigherRankMeshCalculationResult:
        coordinates = _coordinates(mesh_size, 0.0)
        mesh = CenteredUniformMesh(dimension=1, size=mesh_size, offsets=(0.0,))
        reference_frames = model.reference_frames(coordinates)
        attacked_frames = model.attacked_frames(coordinates)
        pointwise_result = None
        try:
            pointwise_result = self._solve(attacked_frames, reference_frames)
        except (ArithmeticError, RuntimeError, ValueError) as exception:
            pointwise_selection = _failed_procrustes_record(
                request=self._request,
                channel=Periodic1DHigherRankAlignmentChannel.POINTWISE_UNITARY,
                selection_mesh_size=mesh_size,
                exception=exception,
            )
        else:
            pointwise_selection = _procrustes_record(
                request=self._request,
                channel=Periodic1DHigherRankAlignmentChannel.POINTWISE_UNITARY,
                selection_mesh_size=mesh_size,
                source=attacked_frames,
                target=reference_frames,
                result=pointwise_result,
            )
        transport_source = FinitePeriodicMeshFrameInventory.from_arrays(
            mesh=mesh,
            frames=reference_frames,
            endpoint_sewing_map=model.endpoint_sewing_map,
            ambient_basis_identifier=self._request.ambient_basis_identifier,
            retained_frame_identifier=self._request.retained_frame_identifier,
            endpoint_sewing_identifier=self._request.endpoint_sewing_identifier,
            principal_phase_branch=self._request.configuration.principal_phase_branch,
            tolerance=self._request.configuration.owner_transport_tolerance(),
        )
        try:
            transport_outcome = self._transporter.transport(transport_source)
        except ClosedLoopPolarFrameTransportBackendFailure as failure:
            failure_result_type = (
                Periodic1DHigherRankAlignmentTransportBackendFailureResult
            )
            transport_failure = failure_result_type.from_owner_failure(
                case_identity=self._request.case_identity,
                retained_rank=self._request.retained_rank,
                circuit_depth=self._request.circuit_depth,
                construction_mesh_size=mesh_size,
                failure=failure,
            )
            model_diagnostics = self._model_diagnostics(
                model,
                coordinates,
                reference_frames,
                attacked_frames,
            )
            channels = tuple(
                _unavailable_channel_result(
                    _status(
                        self._request,
                        mesh_size,
                        channel,
                        Periodic1DHigherRankAlignmentStatus.NUMERICALLY_UNRESOLVED,
                        transport_failure.backend_exception_code,
                    )
                )
                for channel in self._request.configuration.alignment_channels
            )
            return Periodic1DHigherRankMeshCalculationResult(
                construction_mesh_size=mesh_size,
                model_diagnostics=model_diagnostics,
                transport=None,
                transport_backend_failure=transport_failure,
                endpoint_closure_defect=None,
                primitive_closure_defect=None,
                pointwise_selection=pointwise_selection,
                channels=channels,
            )
        transport = (
            Periodic1DHigherRankAlignmentTransportOwnerResult.from_owner_outcome(
                request=self._request.transport_request(mesh_size),
                outcome=transport_outcome,
            )
        )
        if (
            transport_outcome.transported_frames is None
            or transport_outcome.closure_alignment_right_action is None
        ):
            raise ValueError("analytic reference transport must remain full rank")
        transported = transport_outcome.transported_frames
        endpoint_defect = float(
            np.linalg.norm(transported[-1] - model.endpoint_sewing_map @ transported[0])
            / math.sqrt(model.retained_rank)
        )
        primitive_defect = float(
            np.linalg.norm(
                transported[-1] @ transport_outcome.closure_alignment_right_action
                - model.endpoint_sewing_map @ transported[0]
            )
            / math.sqrt(model.retained_rank)
        )
        model_diagnostics = self._model_diagnostics(
            model,
            coordinates,
            reference_frames,
            attacked_frames,
        )
        aligned = self._aligned_construction_fields(
            model,
            coordinates,
            pointwise_result,
            pointwise_selection,
            global_selection,
        )
        channels = tuple(
            self._channel_result(
                model=model,
                mesh=mesh,
                coordinates=coordinates,
                channel=channel,
                aligned_samples=aligned[0].get(channel),
                aligned_frames=aligned[1].get(channel),
                global_selection=global_selection,
                pointwise_result=pointwise_result,
                pointwise_selection=pointwise_selection,
            )
            for channel in self._request.configuration.alignment_channels
        )
        return Periodic1DHigherRankMeshCalculationResult(
            construction_mesh_size=mesh_size,
            model_diagnostics=model_diagnostics,
            transport=transport,
            transport_backend_failure=None,
            endpoint_closure_defect=endpoint_defect,
            primitive_closure_defect=primitive_defect,
            pointwise_selection=pointwise_selection,
            channels=channels,
        )

    def _model_diagnostics(
        self,
        model: Periodic1DHigherRankAnalyticCase,
        coordinates: RealArray,
        reference_frames: ComplexArray,
        attacked_frames: ComplexArray,
    ) -> Periodic1DHigherRankModelDiagnostics:
        energy = self._request.controls.energy_reference
        parent = model.parent_hamiltonians(coordinates)
        exact = model.exact_reduced_hamiltonians(coordinates)
        attacked = model.attacked_reduced_hamiltonians(coordinates)
        gauge = model.gauge_unitaries(coordinates)
        reference_recovered = _adjoint(reference_frames) @ parent @ reference_frames
        attacked_recovered = _adjoint(attacked_frames) @ parent @ attacked_frames
        oracle_frames = attacked_frames @ _adjoint(gauge)
        oracle_operator = _apply_right_basis_change(attacked, _adjoint(gauge))
        parent_hermiticity = MatrixFieldHermiticityAnalyzer().execute(parent, energy)
        reference_isometry = MatrixFieldIsometryAnalyzer().execute(reference_frames)
        attacked_isometry = MatrixFieldIsometryAnalyzer().execute(attacked_frames)
        gauge_isometry = MatrixFieldIsometryAnalyzer().execute(gauge)
        projectors = reference_frames @ _adjoint(reference_frames)
        attacked_projectors = attacked_frames @ _adjoint(attacked_frames)
        attacked_projector_equality = float(
            np.max(
                np.linalg.norm(
                    attacked_projectors - projectors,
                    axis=(-2, -1),
                )
            )
        )
        projector = MatrixProjectorFieldAnalyzer().execute(projectors)
        reference_error = MatrixFieldErrorAnalyzer().execute(
            reference_recovered, exact, energy
        )
        attacked_error = MatrixFieldErrorAnalyzer().execute(
            attacked_recovered, attacked, energy
        )
        attacked_spectrum = MatrixFieldErrorAnalyzer().execute(attacked, exact, energy)
        oracle_error = MatrixFieldErrorAnalyzer().execute(
            oracle_operator, exact, energy
        )
        oracle_frame = float(
            np.max(np.linalg.norm(oracle_frames - reference_frames, axis=(-2, -1)))
            / math.sqrt(model.retained_rank)
        )
        sampled_gaps = []
        sampled_attack_angles = []
        for mesh_size in self._request.configuration.construction_mesh_sizes:
            mesh_coordinates = _coordinates(mesh_size, 0.0)
            retained = model.retained_energies(mesh_coordinates)
            exterior = model.exterior_energies(mesh_coordinates)
            sampled_gaps.append(
                float(np.min(np.min(exterior, axis=1) - np.max(retained, axis=1)))
            )
            sampled_attack_angles.append(
                model.sampled_attack_angle_maximum(mesh_coordinates)
            )
        diagnostics = Periodic1DHigherRankModelDiagnostics(
            case_identity=self._request.case_identity,
            retained_rank=model.retained_rank,
            circuit_depth=model.circuit_depth,
            construction_mesh_size=coordinates.size,
            exact_analytic_isolation_gap=2.1,
            sampled_isolation_gaps=np.asarray(sampled_gaps, dtype=np.float64),
            exact_analytic_attack_angle_maximum=model.exact_attack_angle_maximum,
            sampled_attack_angle_maxima=np.asarray(
                sampled_attack_angles, dtype=np.float64
            ),
            parent_hermiticity_defect=parent_hermiticity.normalized_maximum_frobenius_defect,
            reference_frame_isometry_defect=reference_isometry.normalized_maximum_frobenius_defect,
            gauge_unitarity_defect=(gauge_isometry.normalized_maximum_frobenius_defect),
            attacked_frame_isometry_defect=attacked_isometry.normalized_maximum_frobenius_defect,
            attacked_projector_equality_defect=attacked_projector_equality,
            reference_projector_hermiticity_defect=projector.normalized_maximum_hermiticity_frobenius_defect,
            reference_projector_idempotency_defect=projector.normalized_maximum_idempotency_frobenius_defect,
            reference_operator_recovery_defect=reference_error.normalized_matrix_frobenius_maximum,
            reference_spectrum_recovery_defect=reference_error.normalized_ordered_spectrum_maximum,
            attacked_operator_recovery_defect=attacked_error.normalized_matrix_frobenius_maximum,
            attacked_spectrum_recovery_defect=attacked_spectrum.normalized_ordered_spectrum_maximum,
            oracle_frame_recovery_defect=oracle_frame,
            oracle_operator_recovery_defect=oracle_error.normalized_matrix_frobenius_maximum,
        )
        maximum_structure_defect = max(
            diagnostics.parent_hermiticity_defect,
            diagnostics.reference_frame_isometry_defect,
            diagnostics.gauge_unitarity_defect,
            diagnostics.attacked_frame_isometry_defect,
            diagnostics.attacked_projector_equality_defect,
            diagnostics.reference_projector_hermiticity_defect,
            diagnostics.reference_projector_idempotency_defect,
        )
        if maximum_structure_defect > self._request.controls.model_structure_tolerance:
            raise ValueError("analytic model structure exceeds the frozen tolerance")
        maximum_recovery_defect = max(
            diagnostics.reference_operator_recovery_defect,
            diagnostics.reference_spectrum_recovery_defect,
            diagnostics.attacked_operator_recovery_defect,
            diagnostics.attacked_spectrum_recovery_defect,
            diagnostics.oracle_frame_recovery_defect,
            diagnostics.oracle_operator_recovery_defect,
        )
        if maximum_recovery_defect > self._request.controls.direct_recovery_tolerance:
            raise ValueError("analytic model recovery exceeds the frozen tolerance")
        return diagnostics

    def _aligned_construction_fields(
        self,
        model: Periodic1DHigherRankAnalyticCase,
        coordinates: RealArray,
        pointwise_result: NumpyBatchedComplexUnitaryProcrustesResult | None,
        pointwise_selection: Periodic1DHigherRankProcrustesDiagnostics,
        global_selection: Periodic1DHigherRankProcrustesDiagnostics,
    ) -> tuple[
        dict[Periodic1DHigherRankAlignmentChannel, ComplexArray],
        dict[Periodic1DHigherRankAlignmentChannel, ComplexArray],
    ]:
        attacked = model.attacked_reduced_hamiltonians(coordinates)
        attacked_frames = model.attacked_frames(coordinates)
        matrix_result: dict[Periodic1DHigherRankAlignmentChannel, ComplexArray] = {
            Periodic1DHigherRankAlignmentChannel.IDENTITY: attacked,
        }
        frame_result: dict[Periodic1DHigherRankAlignmentChannel, ComplexArray] = {
            Periodic1DHigherRankAlignmentChannel.IDENTITY: attacked_frames,
        }
        selected = global_selection.selected_global_right_unitary
        if selected is not None:
            right = np.broadcast_to(
                selected.magnitude,
                (coordinates.size, model.retained_rank, model.retained_rank),
            )
            matrix_result[Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY] = (
                _apply_right_basis_change(attacked, right)
            )
            frame_result[Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY] = (
                np.asarray(attacked_frames @ right, dtype=np.complex128)
            )
        if (
            pointwise_selection.status.status
            is Periodic1DHigherRankAlignmentStatus.QUALIFIED
        ):
            if pointwise_result is None:
                raise ValueError("qualified pointwise selection requires a result")
            pointwise_right = pointwise_result.right_unitary_completions
            matrix_result[Periodic1DHigherRankAlignmentChannel.POINTWISE_UNITARY] = (
                _apply_right_basis_change(attacked, pointwise_right)
            )
            frame_result[Periodic1DHigherRankAlignmentChannel.POINTWISE_UNITARY] = (
                np.asarray(attacked_frames @ pointwise_right, dtype=np.complex128)
            )
        gauge_inverse = _adjoint(model.gauge_unitaries(coordinates))
        matrix_result[Periodic1DHigherRankAlignmentChannel.KNOWN_INVERSE_ORACLE] = (
            _apply_right_basis_change(attacked, gauge_inverse)
        )
        frame_result[Periodic1DHigherRankAlignmentChannel.KNOWN_INVERSE_ORACLE] = (
            np.asarray(attacked_frames @ gauge_inverse, dtype=np.complex128)
        )
        return matrix_result, frame_result

    def _channel_status(
        self,
        mesh_size: int,
        channel: Periodic1DHigherRankAlignmentChannel,
        global_selection: Periodic1DHigherRankProcrustesDiagnostics,
        pointwise_selection: Periodic1DHigherRankProcrustesDiagnostics,
    ) -> Periodic1DHigherRankAlignmentStatusResult:
        if channel is Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY:
            return _status(
                self._request,
                mesh_size,
                channel,
                global_selection.status.status,
                global_selection.status.backend_exception_code,
            )
        if channel is Periodic1DHigherRankAlignmentChannel.POINTWISE_UNITARY:
            return pointwise_selection.status
        return _status(
            self._request,
            mesh_size,
            channel,
            Periodic1DHigherRankAlignmentStatus.QUALIFIED,
        )

    def _channel_result(
        self,
        *,
        model: Periodic1DHigherRankAnalyticCase,
        mesh: CenteredUniformMesh,
        coordinates: RealArray,
        channel: Periodic1DHigherRankAlignmentChannel,
        aligned_samples: ComplexArray | None,
        aligned_frames: ComplexArray | None,
        global_selection: Periodic1DHigherRankProcrustesDiagnostics,
        pointwise_result: NumpyBatchedComplexUnitaryProcrustesResult | None,
        pointwise_selection: Periodic1DHigherRankProcrustesDiagnostics,
    ) -> Periodic1DHigherRankChannelMeshResult:
        status = self._channel_status(
            mesh.size,
            channel,
            global_selection,
            pointwise_selection,
        )
        if aligned_samples is None:
            if aligned_frames is not None:
                raise ValueError("unavailable channel fields must all be absent")
            return _unavailable_channel_result(status)
        if aligned_frames is None:
            raise ValueError("qualified aligned samples require aligned frames")
        return Periodic1DHigherRankChannelAnalyzer(
            request=Periodic1DHigherRankChannelAnalysisRequest(
                calculation_request=self._request,
                model=model,
                mesh=mesh,
                coordinates=coordinates,
                status=status,
                aligned_samples=immutable_complex128_array(
                    aligned_samples, "aligned_samples"
                ),
                aligned_frames=immutable_complex128_array(
                    aligned_frames, "aligned_frames"
                ),
                global_selection=global_selection,
                pointwise_alignment=(
                    pointwise_result
                    if channel is Periodic1DHigherRankAlignmentChannel.POINTWISE_UNITARY
                    else None
                ),
            ),
            fourier_transformer=self._fourier_transformer,
            fourier_evaluator=self._fourier_evaluator,
        ).execute()


__all__ = ["Periodic1DHigherRankAlignmentAnalyzer"]
