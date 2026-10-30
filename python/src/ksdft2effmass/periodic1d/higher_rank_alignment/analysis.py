"""Request-bound producer for the analytic higher-rank periodic-1D calculation."""

from __future__ import annotations

import math
from typing import final

import numpy as np
from numpy.typing import NDArray
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesDefinition,
    NumpyBatchedComplexUnitaryProcrustesResult,
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransportBackendFailure,
    ClosedLoopPolarFrameTransporter,
    FinitePeriodicMeshFrameInventory,
)
from projectkoios.physkit.solidstate.tb import (
    FinitePeriodicMatrixFourierTensorEvaluator,
    FinitePeriodicMatrixFourierTransformer,
    FinitePeriodicMatrixHermiticityAnalyzer,
    FinitePeriodicMatrixParsevalAnalyzer,
    FinitePeriodicMatrixSamples,
)
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from ksdft2effmass.analysis.matrix_field.diagnostics import (
    FourierMatrixBlockNormInventoryAnalyzer1D,
    MatrixErrorDecompositionAnalyzer,
    MatrixFieldComparisonAnalyzer,
    MatrixFieldErrorAnalyzer,
    MatrixFieldHermiticityAnalyzer,
    MatrixFieldIsometryAnalyzer,
    MatrixProjectorFieldAnalyzer,
    SymmetricRangeTailAnalyzer1D,
    SymmetricRangeTailMonotonicityAnalyzer1D,
)

from .calculation import (
    _ODD_CENTERED_NO_NYQUIST_DISPOSITION,
    Periodic1DHigherRankAlignmentCalculationRequest,
    Periodic1DHigherRankAlignmentCalculationResult,
    Periodic1DHigherRankBlockRefinementResult,
    Periodic1DHigherRankChannelMeshResult,
    Periodic1DHigherRankFrameErrorResult,
    Periodic1DHigherRankMatrixComparisonResult,
    Periodic1DHigherRankMatrixErrorResult,
    Periodic1DHigherRankMeshCalculationResult,
    Periodic1DHigherRankModelDiagnostics,
    Periodic1DHigherRankProcrustesDiagnostics,
    Periodic1DHigherRankScalarRefinementResult,
    Periodic1DHigherRankSupportResult,
)
from .definition import (
    Periodic1DHigherRankAlignmentBackendExceptionCode,
    Periodic1DHigherRankAlignmentChannel,
    Periodic1DHigherRankAlignmentStatus,
    Periodic1DHigherRankGlobalUnitaryDownstreamApplicability,
)
from .model import (
    Periodic1DHigherRankAnalyticCase,
    Periodic1DHigherRankAnalyticCaseConstructor,
)
from .result import (
    Periodic1DHigherRankAlignmentStatusResult,
    Periodic1DHigherRankAlignmentTransportBackendFailureResult,
    Periodic1DHigherRankAlignmentTransportOwnerResult,
)

ComplexArray = NDArray[np.complex128]
FloatArray = NDArray[np.float64]

_GlobalApplicability = Periodic1DHigherRankGlobalUnitaryDownstreamApplicability
_INAPPLICABLE_GLOBAL_RANK = _GlobalApplicability.INAPPLICABLE_AGGREGATE_RANK_DEFICIENT


def _coordinates(mesh_size: int, offset: float) -> FloatArray:
    return np.asarray(
        -0.5 + (np.arange(mesh_size, dtype=np.float64) + offset) / mesh_size,
        dtype=np.float64,
    )


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
) -> tuple[FloatArray, float, float, float, float]:
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
    )

    def __init__(
        self,
        *,
        request: Periodic1DHigherRankAlignmentCalculationRequest,
        procrustes_solver: NumpyBatchedComplexUnitaryProcrustesSolver,
        transporter: ClosedLoopPolarFrameTransporter,
        fourier_transformer: FinitePeriodicMatrixFourierTransformer,
        fourier_evaluator: FinitePeriodicMatrixFourierTensorEvaluator,
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
        self._request = request
        self._procrustes_solver = procrustes_solver
        self._transporter = transporter
        self._fourier_transformer = fourier_transformer
        self._fourier_evaluator = fourier_evaluator

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
        refinements = self._block_refinements(meshes)
        scalar_refinements = self._scalar_refinements(meshes)
        evaluation_coordinates = _coordinates(
            request.configuration.evaluation_mesh_size,
            request.configuration.evaluation_shift_numerator
            / request.configuration.evaluation_shift_denominator,
        )
        construction_evaluation_disjoint = all(
            np.intersect1d(_coordinates(mesh_size, 0.0), evaluation_coordinates).size
            == 0
            for mesh_size in request.configuration.construction_mesh_sizes
        )
        return Periodic1DHigherRankAlignmentCalculationResult(
            request=request,
            global_selection=global_selection,
            meshes=meshes,
            construction_evaluation_disjoint=construction_evaluation_disjoint,
            evaluation_noninfluence_confirmed=True,
            block_refinements=refinements,
            scalar_refinements=scalar_refinements,
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
        coordinates: FloatArray,
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
        gauge_unitarity = float(
            np.max(
                np.linalg.norm(
                    _adjoint(gauge) @ gauge
                    - np.eye(model.retained_rank, dtype=np.complex128),
                    axis=(-2, -1),
                )
            )
        )
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
            retained_rank=model.retained_rank,
            exact_analytic_isolation_gap=2.1,
            sampled_isolation_gaps=np.asarray(sampled_gaps, dtype=np.float64),
            exact_analytic_attack_angle_maximum=model.exact_attack_angle_maximum,
            sampled_attack_angle_maxima=np.asarray(
                sampled_attack_angles, dtype=np.float64
            ),
            parent_hermiticity_defect=parent_hermiticity.normalized_maximum_frobenius_defect,
            reference_frame_isometry_defect=reference_isometry.normalized_maximum_frobenius_defect,
            gauge_unitarity_defect=gauge_unitarity,
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
        coordinates: FloatArray,
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

    def _direct_evaluation_field(
        self,
        model: Periodic1DHigherRankAnalyticCase,
        evaluation_coordinates: FloatArray,
        channel: Periodic1DHigherRankAlignmentChannel,
        global_selection: Periodic1DHigherRankProcrustesDiagnostics,
    ) -> ComplexArray:
        if channel is Periodic1DHigherRankAlignmentChannel.IDENTITY:
            return model.attacked_reduced_hamiltonians(evaluation_coordinates)
        if channel is Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY:
            selected = global_selection.selected_global_right_unitary
            if selected is None:
                raise ValueError(
                    "global direct evaluation requires an applicable unitary"
                )
            attacked = model.attacked_reduced_hamiltonians(evaluation_coordinates)
            right = np.broadcast_to(
                selected.magnitude,
                (evaluation_coordinates.size, model.retained_rank, model.retained_rank),
            )
            return _apply_right_basis_change(attacked, right)
        return model.exact_reduced_hamiltonians(evaluation_coordinates)

    def _channel_result(
        self,
        *,
        model: Periodic1DHigherRankAnalyticCase,
        mesh: CenteredUniformMesh,
        coordinates: FloatArray,
        channel: Periodic1DHigherRankAlignmentChannel,
        aligned_samples: ComplexArray | None,
        aligned_frames: ComplexArray | None,
        global_selection: Periodic1DHigherRankProcrustesDiagnostics,
        pointwise_selection: Periodic1DHigherRankProcrustesDiagnostics,
    ) -> Periodic1DHigherRankChannelMeshResult:
        status = self._channel_status(
            mesh.size,
            channel,
            global_selection,
            pointwise_selection,
        )
        if aligned_samples is None:
            return _unavailable_channel_result(status)
        if aligned_frames is None:
            raise ValueError("qualified aligned samples require aligned frames")
        controls = self._request.controls
        reference_frames = model.reference_frames(coordinates)
        frame_norms = np.linalg.norm(
            aligned_frames - reference_frames,
            axis=(-2, -1),
        )
        frame_scale = math.sqrt(model.retained_rank)
        frame_recovery = Periodic1DHigherRankFrameErrorResult(
            rank=model.retained_rank,
            frobenius_maximum=float(np.max(frame_norms)),
            frobenius_rms=float(np.sqrt(np.mean(frame_norms**2))),
            normalized_frobenius_maximum=float(np.max(frame_norms) / frame_scale),
            normalized_frobenius_rms=float(
                np.sqrt(np.mean(frame_norms**2)) / frame_scale
            ),
        )
        direct_construction = self._direct_evaluation_field(
            model,
            coordinates,
            channel,
            global_selection,
        )
        represented_operator_recovery = MatrixFieldErrorAnalyzer().execute(
            aligned_samples,
            direct_construction,
            controls.energy_reference,
        )
        known_recovery_applicable = channel in (
            Periodic1DHigherRankAlignmentChannel.POINTWISE_UNITARY,
            Periodic1DHigherRankAlignmentChannel.KNOWN_INVERSE_ORACLE,
        )
        source = FinitePeriodicMatrixSamples.from_array(
            mesh=mesh,
            matrix_samples=aligned_samples,
            energy_unit=Unitless(),
            energy_reference=self._request.energy_reference_identifier,
            basis_identifier=self._request.represented_basis_identifier,
        )
        transform = self._fourier_transformer.transform(source)
        integer_modes = np.asarray(transform.series.integer_modes[:, 0], dtype=np.int64)
        expected_modes = np.arange(
            -(mesh.size // 2), mesh.size // 2 + 1, dtype=np.int64
        )
        mode_inventory = {int(value) for value in integer_modes}
        representative_inventory_ordered_unique = bool(
            np.array_equal(integer_modes, expected_modes)
        )
        inversion_closed = mode_inventory == {-value for value in mode_inventory}
        index_bijection_pass = (
            np.unique(np.mod(integer_modes, mesh.size)).size == mesh.size
        )
        reconstruction_values = self._fourier_evaluator.evaluate(
            transform.series,
            (coordinates,),
            controls.maximum_working_elements,
        ).matrix_values
        reconstruction = MatrixFieldErrorAnalyzer().execute(
            reconstruction_values,
            aligned_samples,
            controls.energy_reference,
        )
        parseval = FinitePeriodicMatrixParsevalAnalyzer().analyze(transform)
        parseval_scale = max(
            parseval.sample_mean_squared_frobenius_norm.magnitude,
            controls.saturation_denominator_floor,
        )
        parseval_relative = parseval.absolute_defect.magnitude / parseval_scale
        hermiticity = FinitePeriodicMatrixHermiticityAnalyzer().analyze(transform)
        normalization = math.sqrt(model.retained_rank) * controls.energy_reference
        ordinary_hermiticity = (
            hermiticity.ordinary_maximum_frobenius_defect.magnitude / normalization
        )
        twisted_hermiticity = (
            hermiticity.twisted_cyclic_maximum_frobenius_defect.magnitude
            / normalization
        )
        blocks = FourierMatrixBlockNormInventoryAnalyzer1D().execute(
            transform.series,
            controls.maximum_recorded_block_range,
            controls.energy_reference,
        )
        evaluation_coordinates = _coordinates(
            self._request.configuration.evaluation_mesh_size,
            self._request.configuration.evaluation_shift_numerator
            / self._request.configuration.evaluation_shift_denominator,
        )
        full_evaluation = self._fourier_evaluator.evaluate(
            transform.series,
            (evaluation_coordinates,),
            controls.maximum_working_elements,
        ).matrix_values
        direct_evaluation = self._direct_evaluation_field(
            model,
            evaluation_coordinates,
            channel,
            global_selection,
        )
        interpolation = MatrixFieldComparisonAnalyzer().execute(
            full_evaluation,
            direct_evaluation,
            controls.energy_reference,
            controls.saturation_denominator_floor,
        )
        tail_analyzer = SymmetricRangeTailAnalyzer1D()
        tails = tuple(
            tail_analyzer.execute(transform.series, support, controls.energy_reference)
            for support in controls.support_radii
        )
        support_results: list[Periodic1DHigherRankSupportResult] = []
        for tail in tails:
            indices = tuple(
                index
                for index, mode in enumerate(transform.series.integer_modes[:, 0])
                if abs(int(mode)) <= tail.maximum_range
            )
            truncated_series = transform.series.take(indices)
            omitted_indices = tuple(
                index
                for index in range(transform.series.term_count)
                if index not in indices
            )
            omitted_series = transform.series.take(omitted_indices)
            truncated_evaluation = self._fourier_evaluator.evaluate(
                truncated_series,
                (evaluation_coordinates,),
                controls.maximum_working_elements,
            ).matrix_values
            omitted_construction = self._fourier_evaluator.evaluate(
                omitted_series,
                (coordinates,),
                controls.maximum_working_elements,
            ).matrix_values
            truncation = MatrixFieldComparisonAnalyzer().execute(
                truncated_evaluation,
                full_evaluation,
                controls.energy_reference,
                controls.saturation_denominator_floor,
            )
            total = MatrixFieldComparisonAnalyzer().execute(
                truncated_evaluation,
                direct_evaluation,
                controls.energy_reference,
                controls.saturation_denominator_floor,
            )
            decomposition = MatrixErrorDecompositionAnalyzer().execute(
                full_evaluation - direct_evaluation,
                truncated_evaluation - full_evaluation,
                truncated_evaluation - direct_evaluation,
                controls.energy_reference,
            )
            construction_weight = float(
                np.mean(
                    np.linalg.norm(
                        omitted_construction,
                        axis=(-2, -1),
                    )
                    ** 2
                )
            )
            parseval_denominator = max(
                construction_weight,
                tail.omitted_squared_frobenius_weight,
                model.retained_rank * controls.saturation_denominator_floor,
            )
            support_results.append(
                Periodic1DHigherRankSupportResult(
                    maximum_range=tail.maximum_range,
                    retained_translations=tail.retained_translations,
                    omitted_squared_frobenius_weight=tail.omitted_squared_frobenius_weight,
                    normalized_omitted_squared_frobenius_weight=tail.normalized_omitted_squared_frobenius_weight,
                    omitted_frobenius_l2_norm=tail.omitted_frobenius_l2_norm,
                    normalized_omitted_frobenius_l2_norm=tail.normalized_omitted_frobenius_l2_norm,
                    omitted_block_l1_norm=tail.omitted_block_l1_norm,
                    normalized_omitted_block_l1_norm=tail.normalized_omitted_block_l1_norm,
                    construction_parseval_relative_defect=(
                        abs(construction_weight - tail.omitted_squared_frobenius_weight)
                        / parseval_denominator
                    ),
                    construction_parseval_pass=(
                        abs(construction_weight - tail.omitted_squared_frobenius_weight)
                        / parseval_denominator
                        <= controls.fourier_consistency_tolerance
                    ),
                    truncation=Periodic1DHigherRankMatrixComparisonResult.from_diagnostics(
                        truncation,
                        controls.perturbation_bound_tolerance,
                    ),
                    total=Periodic1DHigherRankMatrixComparisonResult.from_diagnostics(
                        total,
                        controls.perturbation_bound_tolerance,
                    ),
                    error_decomposition_defect=decomposition.maximum_frobenius_defect,
                    normalized_error_decomposition_defect=decomposition.normalized_maximum_frobenius_defect,
                    error_decomposition_pass=(
                        decomposition.normalized_maximum_frobenius_defect
                        <= controls.error_decomposition_tolerance
                    ),
                )
            )
        monotonicity = SymmetricRangeTailMonotonicityAnalyzer1D().execute(
            tails,
            controls.tail_monotonicity_tolerance,
        )
        maximum_tail_increase = max(
            max(
                item.normalized_squared_weight_increase,
                item.normalized_l2_norm_increase,
                item.normalized_l1_norm_increase,
            )
            for item in monotonicity
        )
        return Periodic1DHigherRankChannelMeshResult(
            status=status,
            transform_backend_identifier=transform.backend_identifier,
            transform_backend_version=transform.backend_version,
            fourier_representative_count=transform.series.term_count,
            fourier_representative_inventory_ordered_unique=(
                representative_inventory_ordered_unique
            ),
            fourier_inversion_closed=inversion_closed,
            fourier_index_bijection_pass=index_bijection_pass,
            no_nyquist_disposition=_ODD_CENTERED_NO_NYQUIST_DISPOSITION,
            coefficient_translations=np.asarray(
                [block.translation for block in blocks.blocks],
                dtype=np.int64,
            ),
            block_raw_frobenius_norms=np.asarray(
                [block.raw_frobenius_norm for block in blocks.blocks],
                dtype=np.float64,
            ),
            block_normalized_frobenius_norms=np.asarray(
                [block.normalized_frobenius_norm for block in blocks.blocks],
                dtype=np.float64,
            ),
            frame_recovery=frame_recovery,
            known_frame_recovery_pass=(
                frame_recovery.normalized_frobenius_maximum
                <= controls.direct_recovery_tolerance
                if known_recovery_applicable
                else None
            ),
            represented_operator_recovery=Periodic1DHigherRankMatrixErrorResult.from_diagnostics(
                represented_operator_recovery
            ),
            known_operator_recovery_pass=(
                represented_operator_recovery.normalized_matrix_frobenius_maximum
                <= controls.direct_recovery_tolerance
                if known_recovery_applicable
                else None
            ),
            reconstruction=Periodic1DHigherRankMatrixErrorResult.from_diagnostics(
                reconstruction
            ),
            reconstruction_pass=(
                reconstruction.normalized_matrix_frobenius_maximum
                <= controls.fourier_consistency_tolerance
            ),
            interpolation=Periodic1DHigherRankMatrixComparisonResult.from_diagnostics(
                interpolation,
                controls.perturbation_bound_tolerance,
            ),
            final_interpolation_operator_pass=(
                interpolation.errors.normalized_matrix_frobenius_maximum
                <= controls.final_interpolation_operator_tolerance
            ),
            final_interpolation_spectrum_pass=(
                interpolation.errors.normalized_ordered_spectrum_maximum
                <= controls.final_interpolation_spectrum_tolerance
            ),
            parseval_relative_defect=parseval_relative,
            parseval_pass=(parseval_relative <= controls.fourier_consistency_tolerance),
            ordinary_hermiticity_defect=ordinary_hermiticity,
            ordinary_hermiticity_pass=(
                ordinary_hermiticity <= controls.fourier_consistency_tolerance
            ),
            twisted_cyclic_hermiticity_defect=twisted_hermiticity,
            twisted_cyclic_hermiticity_pass=(
                twisted_hermiticity <= controls.fourier_consistency_tolerance
            ),
            supports=tuple(support_results),
            maximum_tail_increase=maximum_tail_increase,
            all_tail_monotonicity_checks_pass=all(item.passes for item in monotonicity),
        )

    def _block_refinements(
        self,
        meshes: tuple[Periodic1DHigherRankMeshCalculationResult, ...],
    ) -> tuple[Periodic1DHigherRankBlockRefinementResult, ...]:
        controls = self._request.controls
        results: list[Periodic1DHigherRankBlockRefinementResult] = []
        for channel in self._request.configuration.alignment_channels:
            for coarse_mesh, fine_mesh in zip(meshes[:-1], meshes[1:], strict=True):
                coarse = next(
                    item
                    for item in coarse_mesh.channels
                    if item.status.channel is channel
                )
                fine = next(
                    item
                    for item in fine_mesh.channels
                    if item.status.channel is channel
                )
                if (
                    coarse.status.status
                    is not Periodic1DHigherRankAlignmentStatus.QUALIFIED
                    or fine.status.status
                    is not Periodic1DHigherRankAlignmentStatus.QUALIFIED
                ):
                    continue
                if not np.array_equal(
                    coarse.coefficient_translations, fine.coefficient_translations
                ):
                    raise ValueError(
                        "adjacent block inventories must use identical translations"
                    )
                absolute = np.abs(
                    fine.block_normalized_frobenius_norms
                    - coarse.block_normalized_frobenius_norms
                )
                scale = np.maximum(
                    np.maximum(
                        np.abs(coarse.block_normalized_frobenius_norms),
                        np.abs(fine.block_normalized_frobenius_norms),
                    ),
                    controls.refinement_denominator_floor,
                )
                relative = absolute / scale
                applied = (
                    controls.refinement_absolute_tolerance
                    + controls.refinement_relative_tolerance
                    * np.maximum(
                        np.abs(coarse.block_normalized_frobenius_norms),
                        np.abs(fine.block_normalized_frobenius_norms),
                    )
                )
                margins = applied - absolute
                results.append(
                    Periodic1DHigherRankBlockRefinementResult(
                        channel=channel,
                        coarse_mesh_size=coarse_mesh.construction_mesh_size,
                        fine_mesh_size=fine_mesh.construction_mesh_size,
                        translations=coarse.coefficient_translations,
                        coarse_normalized_block_norms=coarse.block_normalized_frobenius_norms,
                        fine_normalized_block_norms=fine.block_normalized_frobenius_norms,
                        absolute_changes=np.asarray(absolute, dtype=np.float64),
                        relative_changes=np.asarray(relative, dtype=np.float64),
                        applied_tolerances=np.asarray(applied, dtype=np.float64),
                        signed_margins=np.asarray(margins, dtype=np.float64),
                        all_pass=bool(np.all(margins >= 0.0)),
                    )
                )
        return tuple(results)

    @staticmethod
    def _scalar_inventory(
        channel: Periodic1DHigherRankChannelMeshResult,
    ) -> tuple[tuple[str, float], ...]:
        interpolation = channel.interpolation
        if interpolation is None:
            raise ValueError("qualified channel requires interpolation diagnostics")
        values: list[tuple[str, float]] = [
            (
                "/interpolation/normalized_operator_maximum",
                interpolation.errors.normalized_matrix_frobenius_maximum,
            ),
            (
                "/interpolation/normalized_spectrum_maximum",
                interpolation.errors.normalized_ordered_spectrum_maximum,
            ),
        ]
        values.extend(
            (f"/blocks/{int(translation):+d}", float(value))
            for translation, value in zip(
                channel.coefficient_translations,
                channel.block_normalized_frobenius_norms,
                strict=True,
            )
        )
        for support in channel.supports:
            prefix = f"/supports/{support.maximum_range}"
            values.extend(
                (
                    (
                        f"{prefix}/tail_w",
                        support.normalized_omitted_squared_frobenius_weight,
                    ),
                    (
                        f"{prefix}/tail_n",
                        support.normalized_omitted_frobenius_l2_norm,
                    ),
                    (
                        f"{prefix}/tail_l",
                        support.normalized_omitted_block_l1_norm,
                    ),
                    (
                        f"{prefix}/truncation_operator_maximum",
                        support.truncation.errors.normalized_matrix_frobenius_maximum,
                    ),
                    (
                        f"{prefix}/truncation_spectrum_maximum",
                        support.truncation.errors.normalized_ordered_spectrum_maximum,
                    ),
                    (
                        f"{prefix}/total_operator_maximum",
                        support.total.errors.normalized_matrix_frobenius_maximum,
                    ),
                    (
                        f"{prefix}/total_spectrum_maximum",
                        support.total.errors.normalized_ordered_spectrum_maximum,
                    ),
                    (
                        f"{prefix}/parseval",
                        support.construction_parseval_relative_defect,
                    ),
                    (
                        f"{prefix}/decomposition",
                        support.normalized_error_decomposition_defect,
                    ),
                )
            )
        return tuple(values)

    def _scalar_refinements(
        self,
        meshes: tuple[Periodic1DHigherRankMeshCalculationResult, ...],
    ) -> tuple[Periodic1DHigherRankScalarRefinementResult, ...]:
        controls = self._request.controls
        coarse_mesh = next(
            mesh for mesh in meshes if mesh.construction_mesh_size == 1025
        )
        fine_mesh = next(mesh for mesh in meshes if mesh.construction_mesh_size == 2049)
        results: list[Periodic1DHigherRankScalarRefinementResult] = []
        for channel in self._request.configuration.alignment_channels:
            coarse = next(
                item for item in coarse_mesh.channels if item.status.channel is channel
            )
            fine = next(
                item for item in fine_mesh.channels if item.status.channel is channel
            )
            if (
                coarse.status.status
                is not Periodic1DHigherRankAlignmentStatus.QUALIFIED
                or fine.status.status
                is not Periodic1DHigherRankAlignmentStatus.QUALIFIED
            ):
                continue
            coarse_inventory = self._scalar_inventory(coarse)
            fine_inventory = self._scalar_inventory(fine)
            if tuple(path for path, _ in coarse_inventory) != tuple(
                path for path, _ in fine_inventory
            ):
                raise ValueError("final scalar refinement inventories must agree")
            for (path, coarse_value), (_, fine_value) in zip(
                coarse_inventory, fine_inventory, strict=True
            ):
                change = abs(fine_value - coarse_value)
                scale = max(
                    abs(coarse_value),
                    abs(fine_value),
                    controls.refinement_denominator_floor,
                )
                tolerance = controls.refinement_absolute_tolerance + (
                    controls.refinement_relative_tolerance
                    * max(abs(coarse_value), abs(fine_value))
                )
                margin = tolerance - change
                results.append(
                    Periodic1DHigherRankScalarRefinementResult(
                        channel=channel,
                        diagnostic_path=path,
                        coarse_mesh_size=coarse_mesh.construction_mesh_size,
                        fine_mesh_size=fine_mesh.construction_mesh_size,
                        coarse_value=coarse_value,
                        fine_value=fine_value,
                        absolute_change=change,
                        relative_change=change / scale,
                        applied_tolerance=tolerance,
                        signed_margin=margin,
                        passes=margin >= 0.0,
                    )
                )
        return tuple(results)


__all__ = ["Periodic1DHigherRankAlignmentAnalyzer"]
