"""Complete scientific request for one gauge-alignment analysis."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesResult,
)

from ..calculation import Periodic1DRankNAlignmentCalculationRequest
from ..definition import Periodic1DRankNAlignmentStatus
from ..diagnostics import Periodic1DRankNProcrustesDiagnostics
from ..model import Periodic1DRankNAnalyticCase
from ..result import Periodic1DRankNAlignmentStatusResult
from .definition import Periodic1DRankNGaugeAlignment
from .fields import (
    Periodic1DRankNGaugeAlignedFields,
    Periodic1DRankNGaugeAlignmentConstructionRequest,
    Periodic1DRankNGaugeAlignmentConstructor,
)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNGaugeAlignmentAnalysisRequest:
    """Bind one qualified gauge alignment and its immutable scientific inputs."""

    calculation_request: Periodic1DRankNAlignmentCalculationRequest
    model: Periodic1DRankNAnalyticCase
    mesh: CenteredUniformMesh
    status: Periodic1DRankNAlignmentStatusResult
    aligned_fields: Periodic1DRankNGaugeAlignedFields
    global_selection: Periodic1DRankNProcrustesDiagnostics
    pointwise_alignment: NumpyBatchedComplexUnitaryProcrustesResult | None = None

    def __post_init__(self) -> None:
        if (
            type(self.calculation_request)
            is not Periodic1DRankNAlignmentCalculationRequest
        ):
            raise TypeError("calculation_request must be the exact request record")
        if type(self.model) is not Periodic1DRankNAnalyticCase:
            raise TypeError("model must be Periodic1DRankNAnalyticCase")
        if type(self.mesh) is not CenteredUniformMesh:
            raise TypeError("mesh must be CenteredUniformMesh")
        if type(self.status) is not Periodic1DRankNAlignmentStatusResult:
            raise TypeError("status must be the exact alignment status record")
        if type(self.aligned_fields) is not Periodic1DRankNGaugeAlignedFields:
            raise TypeError(
                "aligned_fields must be the exact gauge-aligned field record"
            )
        if type(self.global_selection) is not Periodic1DRankNProcrustesDiagnostics:
            raise TypeError("global_selection must be the exact Procrustes record")
        calculation_request = self.calculation_request
        rank = self.model.retained_rank
        if (
            rank != calculation_request.retained_rank
            or self.model.circuit_depth != calculation_request.circuit_depth
        ):
            raise ValueError("model rank and depth must match the calculation request")
        if self.mesh.dimension != 1 or self.mesh.offsets != (0.0,):
            raise ValueError("analysis requires the unshifted periodic-1D mesh")
        coordinates = self.aligned_fields.coordinates
        expected_coordinates = np.asarray(
            -0.5 + np.arange(self.mesh.size, dtype=np.float64) / self.mesh.size,
            dtype=np.float64,
        )
        if not np.array_equal(coordinates, expected_coordinates):
            raise ValueError("coordinates must equal the declared construction mesh")
        if self.aligned_fields.represented_operators.shape != (
            self.mesh.size,
            rank,
            rank,
        ):
            raise ValueError("represented operators must have shape (M, r, r)")
        if self.aligned_fields.frames.shape != (
            self.mesh.size,
            self.model.ambient_dimension,
            rank,
        ):
            raise ValueError("aligned frames must have shape (M, 2r, r)")
        if (
            self.status.case_identity != calculation_request.case_identity
            or self.status.retained_rank != calculation_request.retained_rank
            or self.status.circuit_depth != calculation_request.circuit_depth
            or self.status.construction_mesh_size != self.mesh.size
        ):
            raise ValueError("status must match the calculation case and mesh")
        if self.status.status is not Periodic1DRankNAlignmentStatus.QUALIFIED:
            raise ValueError("analysis requires a qualified gauge alignment")
        if (
            self.status.gauge_alignment is not self.aligned_fields.gauge_alignment
            or self.aligned_fields.case_identity != calculation_request.case_identity
        ):
            raise ValueError(
                "aligned fields must match the status and calculation case"
            )
        if (
            self.status.gauge_alignment
            not in calculation_request.configuration.gauge_alignments
        ):
            raise ValueError("gauge alignment must belong to the calculation request")
        if (
            self.status.gauge_alignment
            is Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY
        ):
            if (
                type(self.pointwise_alignment)
                is not NumpyBatchedComplexUnitaryProcrustesResult
            ):
                raise TypeError("pointwise alignment requires the exact solver result")
        elif self.pointwise_alignment is not None:
            raise ValueError(
                "pointwise_alignment is reserved for pointwise-unitary alignment"
            )
        expected_fields = Periodic1DRankNGaugeAlignmentConstructor(
            Periodic1DRankNGaugeAlignmentConstructionRequest(
                calculation_request=calculation_request,
                model=self.model,
                gauge_alignment=self.status.gauge_alignment,
                coordinates=coordinates,
                global_selection=self.global_selection,
                pointwise_alignment=self.pointwise_alignment,
            )
        ).execute()
        if not np.array_equal(
            self.aligned_fields.represented_operators,
            expected_fields.represented_operators,
        ):
            raise ValueError(
                "represented operators do not match the declared gauge alignment"
            )
        if not np.array_equal(self.aligned_fields.frames, expected_fields.frames):
            raise ValueError("frames do not match the declared gauge alignment")
        selection_status = self.global_selection.status
        if (
            selection_status.case_identity != calculation_request.case_identity
            or selection_status.retained_rank != calculation_request.retained_rank
            or selection_status.circuit_depth != calculation_request.circuit_depth
            or selection_status.gauge_alignment
            is not Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY
            or selection_status.construction_mesh_size
            != calculation_request.configuration.global_unitary_selection_mesh_size
            or self.global_selection.selection_mesh_size
            != calculation_request.configuration.global_unitary_selection_mesh_size
        ):
            raise ValueError("global selection must match the calculation request")


__all__ = ["Periodic1DRankNGaugeAlignmentAnalysisRequest"]
