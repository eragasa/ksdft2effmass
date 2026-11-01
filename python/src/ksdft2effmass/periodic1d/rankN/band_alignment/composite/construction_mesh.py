"""One complete construction-mesh analysis for rank-N band alignment."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

import numpy as np
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.numerics.typing.numpy.arrays import RealArray
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d.rankN.band_alignment.calculation import (
    Periodic1DRankNAlignmentCalculationRequest,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.frame_transport.analysis import (
    Periodic1DRankNFailedTransportAnalysis,
    Periodic1DRankNResolvedTransportAnalysis,
    Periodic1DRankNTransportAnalysisRequest,
    Periodic1DRankNTransportAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.mesh_sample import (
    Periodic1DRankNAnalyticMeshSample,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.model import (
    Periodic1DRankNAnalyticCase,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.model_diagnostics import (
    Periodic1DRankNModelDiagnostics,
    Periodic1DRankNModelDiagnosticsAnalyzer,
    Periodic1DRankNModelDiagnosticsRequest,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.definition import (
    Periodic1DRankNGaugeAlignment,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.fields import (
    Periodic1DRankNGaugeAlignedFields,
    Periodic1DRankNGaugeAlignmentConstructionRequest,
    Periodic1DRankNGaugeAlignmentConstructor,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.procrustes.result import (
    Periodic1DRankNProcrustesDiagnostics,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.procrustes.selection import (
    Periodic1DRankNProcrustesSelection,
    Periodic1DRankNProcrustesSelectionAnalyzer,
    Periodic1DRankNProcrustesSelectionRequest,
    Periodic1DRankNResolvedProcrustesSelection,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.request import (
    Periodic1DRankNGaugeAlignmentAnalysisRequest,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.status import (
    Periodic1DRankNAlignmentBackendExceptionCode,
    Periodic1DRankNAlignmentStatus,
    Periodic1DRankNAlignmentStatusResult,
)

from ..construction_mesh_result import Periodic1DRankNMeshCalculationResult
from ..gauge_case_result import Periodic1DRankNGaugeAlignmentMeshResult
from .gauge_case import Periodic1DRankNCompositeGaugeCaseAnalyzer


@dataclass(frozen=True, slots=True)
class Periodic1DRankNConstructionMeshAnalysisRequest:
    """Bind one mesh sample to case-wide global-selection evidence."""

    calculation_request: Periodic1DRankNAlignmentCalculationRequest
    sample: Periodic1DRankNAnalyticMeshSample
    global_selection: Periodic1DRankNProcrustesDiagnostics

    def __post_init__(self) -> None:
        if (
            type(self.calculation_request)
            is not Periodic1DRankNAlignmentCalculationRequest
        ):
            raise TypeError("calculation_request must be the exact rank-N request")
        if type(self.sample) is not Periodic1DRankNAnalyticMeshSample:
            raise TypeError("sample must be the exact analytic mesh sample")
        if type(self.global_selection) is not Periodic1DRankNProcrustesDiagnostics:
            raise TypeError("global_selection must be the exact Procrustes record")
        calculation_request = self.calculation_request
        model = self.sample.model
        if (
            model.retained_rank != calculation_request.retained_rank
            or model.circuit_depth != calculation_request.circuit_depth
            or self.sample.construction_mesh_size
            not in calculation_request.configuration.construction_mesh_sizes
        ):
            raise ValueError("sample must match the calculation request")
        status = self.global_selection.status
        if (
            status.case_identity != calculation_request.case_identity
            or status.retained_rank != calculation_request.retained_rank
            or status.circuit_depth != calculation_request.circuit_depth
            or status.gauge_alignment
            is not Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY
            or status.construction_mesh_size
            != calculation_request.configuration.global_unitary_selection_mesh_size
        ):
            raise ValueError("global selection must match the calculation request")


@final
class Periodic1DRankNConstructionMeshAnalyzer:
    """Compose selection, transport, diagnostics, and gauge cases for one mesh."""

    __slots__ = ("_request", "_procrustes_solver", "_transporter")

    def __init__(
        self,
        *,
        request: Periodic1DRankNConstructionMeshAnalysisRequest,
        procrustes_solver: NumpyBatchedComplexUnitaryProcrustesSolver,
        transporter: ClosedLoopPolarFrameTransporter,
    ) -> None:
        if type(request) is not Periodic1DRankNConstructionMeshAnalysisRequest:
            raise TypeError("request must be the exact construction-mesh request")
        if type(procrustes_solver) is not NumpyBatchedComplexUnitaryProcrustesSolver:
            raise TypeError("procrustes_solver must be the canonical NumPy solver")
        if type(transporter) is not ClosedLoopPolarFrameTransporter:
            raise TypeError("transporter must be the canonical frame transporter")
        self._request = request
        self._procrustes_solver = procrustes_solver
        self._transporter = transporter

    @property
    def request(self) -> Periodic1DRankNConstructionMeshAnalysisRequest:
        """Return the immutable construction-mesh analysis request."""
        return self._request

    def execute(self) -> Periodic1DRankNMeshCalculationResult:
        """Return the complete typed analysis for the bound construction mesh."""
        analysis_request = self._request
        calculation_request = analysis_request.calculation_request
        sample = analysis_request.sample
        model = sample.model
        mesh_size = sample.construction_mesh_size
        coordinates = sample.coordinates
        mesh = sample.mesh
        pointwise_outcome = self._pointwise_selection()
        pointwise_diagnostics = pointwise_outcome.diagnostics
        resolved_pointwise = (
            pointwise_outcome
            if type(pointwise_outcome) is Periodic1DRankNResolvedProcrustesSelection
            else None
        )
        transport_analysis = Periodic1DRankNTransportAnalyzer(
            Periodic1DRankNTransportAnalysisRequest(
                calculation_request=calculation_request,
                sample=sample,
            ),
            self._transporter,
        ).execute()
        if type(transport_analysis) is Periodic1DRankNFailedTransportAnalysis:
            transport_failure = transport_analysis.failure
            model_diagnostics = self._model_diagnostics()
            gauge_alignment_results = tuple(
                Periodic1DRankNGaugeAlignmentMeshResult.unavailable(
                    Periodic1DRankNAlignmentStatusResult.from_disposition(
                        case_identity=calculation_request.case_identity,
                        retained_rank=calculation_request.retained_rank,
                        circuit_depth=calculation_request.circuit_depth,
                        construction_mesh_size=mesh_size,
                        gauge_alignment=gauge_alignment,
                        status=Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED,
                        backend_exception_code=(
                            Periodic1DRankNAlignmentBackendExceptionCode(
                                transport_failure.backend_exception_code.value
                            )
                        ),
                    )
                )
                for gauge_alignment in (
                    calculation_request.configuration.gauge_alignments
                )
            )
            return Periodic1DRankNMeshCalculationResult(
                construction_mesh_size=mesh_size,
                model_diagnostics=model_diagnostics,
                transport=None,
                transport_backend_failure=transport_failure,
                endpoint_closure_defect=None,
                primitive_closure_defect=None,
                pointwise_selection=pointwise_diagnostics,
                gauge_alignment_results=gauge_alignment_results,
            )
        if type(transport_analysis) is not Periodic1DRankNResolvedTransportAnalysis:
            raise AssertionError("transport analysis returned an unsupported result")
        transport = transport_analysis.transport
        endpoint_defect = transport_analysis.endpoint_closure_defect
        primitive_defect = transport_analysis.primitive_closure_defect
        model_diagnostics = self._model_diagnostics()
        aligned = self._aligned_construction_fields(pointwise_outcome)
        gauge_alignment_results = tuple(
            self._gauge_alignment_result(
                model=model,
                mesh=mesh,
                coordinates=coordinates,
                gauge_alignment=gauge_alignment,
                aligned_fields=aligned.get(gauge_alignment),
                pointwise_selection=resolved_pointwise,
                pointwise_diagnostics=pointwise_diagnostics,
            )
            for gauge_alignment in calculation_request.configuration.gauge_alignments
        )
        return Periodic1DRankNMeshCalculationResult(
            construction_mesh_size=mesh_size,
            model_diagnostics=model_diagnostics,
            transport=transport,
            transport_backend_failure=None,
            endpoint_closure_defect=endpoint_defect,
            primitive_closure_defect=primitive_defect,
            pointwise_selection=pointwise_diagnostics,
            gauge_alignment_results=gauge_alignment_results,
        )

    def _pointwise_selection(self) -> Periodic1DRankNProcrustesSelection:
        calculation_request = self._request.calculation_request
        sample = self._request.sample
        return Periodic1DRankNProcrustesSelectionAnalyzer(
            request=Periodic1DRankNProcrustesSelectionRequest(
                case_identity=calculation_request.case_identity,
                retained_rank=calculation_request.retained_rank,
                circuit_depth=calculation_request.circuit_depth,
                gauge_alignment=Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY,
                selection_mesh_size=sample.construction_mesh_size,
                source=sample.attacked_frames,
                target=sample.reference_frames,
                tolerance=(
                    calculation_request.configuration.owner_transport_tolerance()
                ),
                alignment_integrity_tolerance=(
                    calculation_request.controls.alignment_integrity_tolerance
                ),
            ),
            solver=self._procrustes_solver,
        ).execute()

    def _model_diagnostics(self) -> Periodic1DRankNModelDiagnostics:
        return Periodic1DRankNModelDiagnosticsAnalyzer(
            Periodic1DRankNModelDiagnosticsRequest(
                calculation_request=self._request.calculation_request,
                sample=self._request.sample,
            )
        ).execute()

    def _aligned_construction_fields(
        self,
        pointwise_selection: Periodic1DRankNProcrustesSelection,
    ) -> dict[
        Periodic1DRankNGaugeAlignment,
        Periodic1DRankNGaugeAlignedFields,
    ]:
        analysis_request = self._request
        calculation_request = analysis_request.calculation_request
        sample = analysis_request.sample
        alignments: dict[
            Periodic1DRankNGaugeAlignment,
            Periodic1DRankNGaugeAlignedFields,
        ] = {}
        for gauge_alignment in calculation_request.configuration.gauge_alignments:
            if (
                gauge_alignment is Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY
                and analysis_request.global_selection.status.status
                is not Periodic1DRankNAlignmentStatus.QUALIFIED
            ) or (
                gauge_alignment is Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY
                and pointwise_selection.diagnostics.status.status
                is not Periodic1DRankNAlignmentStatus.QUALIFIED
            ):
                continue
            alignments[gauge_alignment] = Periodic1DRankNGaugeAlignmentConstructor(
                Periodic1DRankNGaugeAlignmentConstructionRequest(
                    calculation_request=calculation_request,
                    model=sample.model,
                    gauge_alignment=gauge_alignment,
                    coordinates=sample.coordinates,
                    global_selection=analysis_request.global_selection,
                    pointwise_selection=(
                        pointwise_selection
                        if gauge_alignment
                        is Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY
                        and type(pointwise_selection)
                        is Periodic1DRankNResolvedProcrustesSelection
                        else None
                    ),
                )
            ).execute()
        return alignments

    def _gauge_alignment_status(
        self,
        gauge_alignment: Periodic1DRankNGaugeAlignment,
        pointwise_diagnostics: Periodic1DRankNProcrustesDiagnostics,
    ) -> Periodic1DRankNAlignmentStatusResult:
        calculation_request = self._request.calculation_request
        global_selection = self._request.global_selection
        mesh_size = self._request.sample.construction_mesh_size
        if gauge_alignment is Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY:
            return Periodic1DRankNAlignmentStatusResult.from_disposition(
                case_identity=calculation_request.case_identity,
                retained_rank=calculation_request.retained_rank,
                circuit_depth=calculation_request.circuit_depth,
                construction_mesh_size=mesh_size,
                gauge_alignment=gauge_alignment,
                status=global_selection.status.status,
                backend_exception_code=(global_selection.status.backend_exception_code),
            )
        if gauge_alignment is Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY:
            return pointwise_diagnostics.status
        return Periodic1DRankNAlignmentStatusResult.from_disposition(
            case_identity=calculation_request.case_identity,
            retained_rank=calculation_request.retained_rank,
            circuit_depth=calculation_request.circuit_depth,
            construction_mesh_size=mesh_size,
            gauge_alignment=gauge_alignment,
            status=Periodic1DRankNAlignmentStatus.QUALIFIED,
        )

    def _gauge_alignment_result(
        self,
        *,
        model: Periodic1DRankNAnalyticCase,
        mesh: CenteredUniformMesh,
        coordinates: RealArray,
        gauge_alignment: Periodic1DRankNGaugeAlignment,
        aligned_fields: Periodic1DRankNGaugeAlignedFields | None,
        pointwise_selection: Periodic1DRankNResolvedProcrustesSelection | None,
        pointwise_diagnostics: Periodic1DRankNProcrustesDiagnostics,
    ) -> Periodic1DRankNGaugeAlignmentMeshResult:
        calculation_request = self._request.calculation_request
        status = self._gauge_alignment_status(
            gauge_alignment,
            pointwise_diagnostics,
        )
        if aligned_fields is None:
            return Periodic1DRankNGaugeAlignmentMeshResult.unavailable(status)
        if (
            aligned_fields.case_identity != calculation_request.case_identity
            or aligned_fields.gauge_alignment is not gauge_alignment
            or not np.array_equal(aligned_fields.coordinates, coordinates)
        ):
            raise ValueError("gauge-aligned fields must match the calculation request")
        return Periodic1DRankNCompositeGaugeCaseAnalyzer(
            request=Periodic1DRankNGaugeAlignmentAnalysisRequest(
                calculation_request=calculation_request,
                model=model,
                mesh=mesh,
                status=status,
                aligned_fields=aligned_fields,
                global_selection=self._request.global_selection,
                pointwise_selection=(
                    pointwise_selection
                    if gauge_alignment
                    is Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY
                    else None
                ),
            ),
        ).execute()


__all__ = [
    "Periodic1DRankNConstructionMeshAnalysisRequest",
    "Periodic1DRankNConstructionMeshAnalyzer",
]
