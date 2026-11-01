"""Request-bound producer for the analytic higher-rank periodic-1D calculation."""

from __future__ import annotations

import math
from typing import final

import numpy as np
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
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

from ksdft2effmass.analysis.matrix_field.diagnostics import (
    MatrixFieldErrorAnalyzer,
    MatrixFieldHermiticityAnalyzer,
    MatrixFieldIsometryAnalyzer,
    MatrixProjectorFieldAnalyzer,
    ScalarRefinementAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.analysis import (
    Periodic1DRankNGaugeAlignmentAnalysisRequest,
    Periodic1DRankNGaugeAlignmentAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.definition import (
    Periodic1DRankNGaugeAlignment,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.fields import (
    Periodic1DRankNGaugeAlignedFields,
    Periodic1DRankNGaugeAlignmentConstructionRequest,
    Periodic1DRankNGaugeAlignmentConstructor,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.results import (
    Periodic1DRankNGaugeAlignmentMeshResult,
    Periodic1DRankNMeshCalculationResult,
)

from ..calculation import Periodic1DRankNAlignmentCalculationRequest
from ..calculation_result import Periodic1DRankNAlignmentCalculationResult
from ..definition import Periodic1DRankNAlignmentStatus
from ..diagnostics import (
    Periodic1DRankNModelDiagnostics,
    Periodic1DRankNProcrustesDiagnostics,
)
from ..model import (
    Periodic1DRankNAnalyticCase,
    Periodic1DRankNAnalyticCaseConstructor,
)
from ..refinement import (
    Periodic1DRankNRefinementAnalysisRequest,
    Periodic1DRankNRefinementAnalyzer,
)
from ..result import (
    Periodic1DRankNAlignmentStatusResult,
    Periodic1DRankNAlignmentTransportBackendFailureResult,
    Periodic1DRankNAlignmentTransportOwnerResult,
)
from .evaluation import Periodic1DRankNEvaluationIndependenceAnalyzer
from .mesh import _coordinates, _status, _unavailable_gauge_alignment_result
from .procrustes import _failed_procrustes_record, _procrustes_record


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


@final
class Periodic1DRankNAlignmentAnalyzer:
    """Calculate one complete rank/depth case using explicit upstream owners.

    The action binds its immutable request and all numerical collaborators at
    construction. :meth:`execute` therefore has no arguments and performs no hidden
    configuration or collaborator discovery.
    """

    __slots__ = (
        "_request",
        "_procrustes_solver",
        "_transporter",
        "_scalar_refinement_analyzer",
    )

    def __init__(
        self,
        *,
        request: Periodic1DRankNAlignmentCalculationRequest,
        procrustes_solver: NumpyBatchedComplexUnitaryProcrustesSolver,
        transporter: ClosedLoopPolarFrameTransporter,
        scalar_refinement_analyzer: ScalarRefinementAnalyzer,
    ) -> None:
        """Bind the exact request and canonical numerical owners."""
        if type(request) is not Periodic1DRankNAlignmentCalculationRequest:
            raise TypeError(
                "request must be Periodic1DRankNAlignmentCalculationRequest"
            )
        if type(procrustes_solver) is not NumpyBatchedComplexUnitaryProcrustesSolver:
            raise TypeError(
                "procrustes_solver must be the canonical NumPy batched solver"
            )
        if type(transporter) is not ClosedLoopPolarFrameTransporter:
            raise TypeError("transporter must be ClosedLoopPolarFrameTransporter")
        if type(scalar_refinement_analyzer) is not ScalarRefinementAnalyzer:
            raise TypeError(
                "scalar_refinement_analyzer must be the KSD refinement owner"
            )
        self._request = request
        self._procrustes_solver = procrustes_solver
        self._transporter = transporter
        self._scalar_refinement_analyzer = scalar_refinement_analyzer

    @property
    def request(self) -> Periodic1DRankNAlignmentCalculationRequest:
        """Return the exact calculation request bound to this action."""
        return self._request

    def execute(self) -> Periodic1DRankNAlignmentCalculationResult:
        """Produce the complete typed calculation for the bound rank/depth case."""
        request = self._request
        model = Periodic1DRankNAnalyticCaseConstructor(
            retained_rank=request.retained_rank,
            circuit_depth=request.circuit_depth,
        ).execute()
        global_selection = self._global_selection(model)
        meshes = tuple(
            self._mesh_result(model, mesh_size, global_selection)
            for mesh_size in request.configuration.construction_mesh_sizes
        )
        refinement = Periodic1DRankNRefinementAnalyzer(
            request=Periodic1DRankNRefinementAnalysisRequest(
                calculation_request=request,
                meshes=meshes,
            ),
            scalar_refinement_analyzer=self._scalar_refinement_analyzer,
        ).execute()
        evaluation_independence = Periodic1DRankNEvaluationIndependenceAnalyzer(
            request
        ).execute()
        return Periodic1DRankNAlignmentCalculationResult(
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
        model: Periodic1DRankNAnalyticCase,
    ) -> Periodic1DRankNProcrustesDiagnostics:
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
                gauge_alignment=Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY,
                selection_mesh_size=mesh_size,
                exception=exception,
            )
        return _procrustes_record(
            request=self._request,
            gauge_alignment=Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY,
            selection_mesh_size=mesh_size,
            source=source,
            target=target,
            result=result,
        )

    def _mesh_result(
        self,
        model: Periodic1DRankNAnalyticCase,
        mesh_size: int,
        global_selection: Periodic1DRankNProcrustesDiagnostics,
    ) -> Periodic1DRankNMeshCalculationResult:
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
                gauge_alignment=Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY,
                selection_mesh_size=mesh_size,
                exception=exception,
            )
        else:
            pointwise_selection = _procrustes_record(
                request=self._request,
                gauge_alignment=Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY,
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
            failure_result_type = Periodic1DRankNAlignmentTransportBackendFailureResult
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
            gauge_alignment_results = tuple(
                _unavailable_gauge_alignment_result(
                    _status(
                        self._request,
                        mesh_size,
                        gauge_alignment,
                        Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED,
                        transport_failure.backend_exception_code,
                    )
                )
                for gauge_alignment in self._request.configuration.gauge_alignments
            )
            return Periodic1DRankNMeshCalculationResult(
                construction_mesh_size=mesh_size,
                model_diagnostics=model_diagnostics,
                transport=None,
                transport_backend_failure=transport_failure,
                endpoint_closure_defect=None,
                primitive_closure_defect=None,
                pointwise_selection=pointwise_selection,
                gauge_alignment_results=gauge_alignment_results,
            )
        transport = Periodic1DRankNAlignmentTransportOwnerResult.from_owner_outcome(
            request=self._request.transport_request(mesh_size),
            outcome=transport_outcome,
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
        gauge_alignment_results = tuple(
            self._gauge_alignment_result(
                model=model,
                mesh=mesh,
                coordinates=coordinates,
                gauge_alignment=gauge_alignment,
                aligned_fields=aligned.get(gauge_alignment),
                global_selection=global_selection,
                pointwise_result=pointwise_result,
                pointwise_selection=pointwise_selection,
            )
            for gauge_alignment in self._request.configuration.gauge_alignments
        )
        return Periodic1DRankNMeshCalculationResult(
            construction_mesh_size=mesh_size,
            model_diagnostics=model_diagnostics,
            transport=transport,
            transport_backend_failure=None,
            endpoint_closure_defect=endpoint_defect,
            primitive_closure_defect=primitive_defect,
            pointwise_selection=pointwise_selection,
            gauge_alignment_results=gauge_alignment_results,
        )

    def _model_diagnostics(
        self,
        model: Periodic1DRankNAnalyticCase,
        coordinates: RealArray,
        reference_frames: ComplexArray,
        attacked_frames: ComplexArray,
    ) -> Periodic1DRankNModelDiagnostics:
        energy = self._request.controls.energy_reference
        parent = model.parent_hamiltonians(coordinates)
        exact = model.exact_reduced_hamiltonians(coordinates)
        attacked = model.attacked_reduced_hamiltonians(coordinates)
        gauge = model.gauge_unitaries(coordinates)
        reference_recovered = _adjoint(reference_frames) @ parent @ reference_frames
        attacked_recovered = _adjoint(attacked_frames) @ parent @ attacked_frames
        oracle_frames = attacked_frames @ _adjoint(gauge)
        oracle_operator = _apply_right_basis_change(attacked, _adjoint(gauge))
        parent_hermiticity = MatrixFieldHermiticityAnalyzer(parent, energy).execute()
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
        reference_error = MatrixFieldErrorAnalyzer(
            approximation=reference_recovered,
            reference=exact,
            norm_energy_scale=energy,
        ).result()
        attacked_error = MatrixFieldErrorAnalyzer(
            approximation=attacked_recovered,
            reference=attacked,
            norm_energy_scale=energy,
        ).result()
        attacked_spectrum = MatrixFieldErrorAnalyzer(
            approximation=attacked,
            reference=exact,
            norm_energy_scale=energy,
        ).result()
        oracle_error = MatrixFieldErrorAnalyzer(
            approximation=oracle_operator,
            reference=exact,
            norm_energy_scale=energy,
        ).result()
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
        diagnostics = Periodic1DRankNModelDiagnostics(
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
        model: Periodic1DRankNAnalyticCase,
        coordinates: RealArray,
        pointwise_result: NumpyBatchedComplexUnitaryProcrustesResult | None,
        pointwise_selection: Periodic1DRankNProcrustesDiagnostics,
        global_selection: Periodic1DRankNProcrustesDiagnostics,
    ) -> dict[
        Periodic1DRankNGaugeAlignment,
        Periodic1DRankNGaugeAlignedFields,
    ]:
        alignments: dict[
            Periodic1DRankNGaugeAlignment,
            Periodic1DRankNGaugeAlignedFields,
        ] = {}
        for gauge_alignment in self._request.configuration.gauge_alignments:
            if (
                gauge_alignment is Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY
                and global_selection.status.status
                is not Periodic1DRankNAlignmentStatus.QUALIFIED
            ) or (
                gauge_alignment is Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY
                and pointwise_selection.status.status
                is not Periodic1DRankNAlignmentStatus.QUALIFIED
            ):
                continue
            alignments[gauge_alignment] = Periodic1DRankNGaugeAlignmentConstructor(
                Periodic1DRankNGaugeAlignmentConstructionRequest(
                    calculation_request=self._request,
                    model=model,
                    gauge_alignment=gauge_alignment,
                    coordinates=coordinates,
                    global_selection=global_selection,
                    pointwise_alignment=(
                        pointwise_result
                        if gauge_alignment
                        is Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY
                        else None
                    ),
                )
            ).execute()
        return alignments

    def _gauge_alignment_status(
        self,
        mesh_size: int,
        gauge_alignment: Periodic1DRankNGaugeAlignment,
        global_selection: Periodic1DRankNProcrustesDiagnostics,
        pointwise_selection: Periodic1DRankNProcrustesDiagnostics,
    ) -> Periodic1DRankNAlignmentStatusResult:
        if gauge_alignment is Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY:
            return _status(
                self._request,
                mesh_size,
                gauge_alignment,
                global_selection.status.status,
                global_selection.status.backend_exception_code,
            )
        if gauge_alignment is Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY:
            return pointwise_selection.status
        return _status(
            self._request,
            mesh_size,
            gauge_alignment,
            Periodic1DRankNAlignmentStatus.QUALIFIED,
        )

    def _gauge_alignment_result(
        self,
        *,
        model: Periodic1DRankNAnalyticCase,
        mesh: CenteredUniformMesh,
        coordinates: RealArray,
        gauge_alignment: Periodic1DRankNGaugeAlignment,
        aligned_fields: Periodic1DRankNGaugeAlignedFields | None,
        global_selection: Periodic1DRankNProcrustesDiagnostics,
        pointwise_result: NumpyBatchedComplexUnitaryProcrustesResult | None,
        pointwise_selection: Periodic1DRankNProcrustesDiagnostics,
    ) -> Periodic1DRankNGaugeAlignmentMeshResult:
        status = self._gauge_alignment_status(
            mesh.size,
            gauge_alignment,
            global_selection,
            pointwise_selection,
        )
        if aligned_fields is None:
            return _unavailable_gauge_alignment_result(status)
        if (
            aligned_fields.case_identity != self._request.case_identity
            or aligned_fields.gauge_alignment is not gauge_alignment
            or not np.array_equal(aligned_fields.coordinates, coordinates)
        ):
            raise ValueError("gauge-aligned fields must match the calculation request")
        return Periodic1DRankNGaugeAlignmentAnalyzer(
            request=Periodic1DRankNGaugeAlignmentAnalysisRequest(
                calculation_request=self._request,
                model=model,
                mesh=mesh,
                status=status,
                aligned_fields=aligned_fields,
                global_selection=global_selection,
                pointwise_alignment=(
                    pointwise_result
                    if gauge_alignment
                    is Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY
                    else None
                ),
            ),
        ).execute()


__all__ = ["Periodic1DRankNAlignmentAnalyzer"]
