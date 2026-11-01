"""Request-bound refinement analysis for higher-rank alignment results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

import numpy as np

from ksdft2effmass.analysis.matrix_field.diagnostics import (
    ScalarRefinementAnalyzer,
    ScalarRefinementDiagnostics,
)
from ksdft2effmass.numerical_consistency import NumericalConsistency
from ksdft2effmass.periodic1d.rankN.gauge_alignment.results import (
    Periodic1DRankNMeshCalculationResult,
)

from .calculation import Periodic1DRankNAlignmentCalculationRequest
from .definition import Periodic1DRankNAlignmentStatus
from .refinement_results import (
    Periodic1DRankNBlockRefinementResult,
    Periodic1DRankNScalarRefinementResult,
)
from .scalar_diagnostics import (
    Periodic1DRankNScalarDiagnosticInventoryExtractor,
)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNRefinementAnalysisRequest:
    """Bind one calculation request and its complete construction-mesh results."""

    calculation_request: Periodic1DRankNAlignmentCalculationRequest
    meshes: tuple[Periodic1DRankNMeshCalculationResult, ...]

    def __post_init__(self) -> None:
        if (
            type(self.calculation_request)
            is not Periodic1DRankNAlignmentCalculationRequest
        ):
            raise TypeError("calculation_request must be the exact request record")
        if type(self.meshes) is not tuple or any(
            type(mesh) is not Periodic1DRankNMeshCalculationResult
            for mesh in self.meshes
        ):
            raise TypeError("meshes must contain exact mesh calculation results")
        request = self.calculation_request
        if tuple(mesh.construction_mesh_size for mesh in self.meshes) != (
            request.configuration.construction_mesh_sizes
        ):
            raise ValueError("refinement meshes must match the calculation request")
        expected_case = (
            request.case_identity,
            request.retained_rank,
            request.circuit_depth,
        )
        for mesh in self.meshes:
            if mesh.model_diagnostics.retained_rank != request.retained_rank:
                raise ValueError("mesh model diagnostics must match the request rank")
            statuses = (mesh.pointwise_selection.status,) + tuple(
                gauge_alignment.status
                for gauge_alignment in mesh.gauge_alignment_results
            )
            if any(
                (
                    status.case_identity,
                    status.retained_rank,
                    status.circuit_depth,
                )
                != expected_case
                or status.construction_mesh_size != mesh.construction_mesh_size
                for status in statuses
            ):
                raise ValueError(
                    "mesh statuses must match the calculation request and mesh"
                )
            if mesh.transport is not None:
                transport_case = (
                    mesh.transport.case_identity,
                    mesh.transport.retained_rank,
                    mesh.transport.circuit_depth,
                )
                if transport_case != expected_case:
                    raise ValueError(
                        "mesh transport must match the calculation request"
                    )
            if mesh.transport_backend_failure is not None:
                failure_case = (
                    mesh.transport_backend_failure.case_identity,
                    mesh.transport_backend_failure.retained_rank,
                    mesh.transport_backend_failure.circuit_depth,
                )
                if failure_case != expected_case:
                    raise ValueError(
                        "mesh transport failure must match the calculation request"
                    )


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNRefinementAnalysis(NumericalConsistency):
    """Retain block and scalar refinement records from one complete request."""

    blocks: tuple[Periodic1DRankNBlockRefinementResult, ...]
    scalars: tuple[Periodic1DRankNScalarRefinementResult, ...]

    def __post_init__(self) -> None:
        if type(self.blocks) is not tuple or any(
            type(item) is not Periodic1DRankNBlockRefinementResult
            for item in self.blocks
        ):
            raise TypeError("blocks must contain exact block refinement records")
        if type(self.scalars) is not tuple or any(
            type(item) is not Periodic1DRankNScalarRefinementResult
            for item in self.scalars
        ):
            raise TypeError("scalars must contain exact scalar refinement records")


@final
class Periodic1DRankNRefinementAnalyzer:
    """Calculate adjacent block and final-pair scalar refinement evidence."""

    __slots__ = ("_request", "_scalar_refinement_analyzer")

    def __init__(
        self,
        *,
        request: Periodic1DRankNRefinementAnalysisRequest,
        scalar_refinement_analyzer: ScalarRefinementAnalyzer,
    ) -> None:
        """Bind the complete request and canonical scalar-refinement owner."""
        if type(request) is not Periodic1DRankNRefinementAnalysisRequest:
            raise TypeError("request must be Periodic1DRankNRefinementAnalysisRequest")
        if type(scalar_refinement_analyzer) is not ScalarRefinementAnalyzer:
            raise TypeError(
                "scalar_refinement_analyzer must be ScalarRefinementAnalyzer"
            )
        self._request = request
        self._scalar_refinement_analyzer = scalar_refinement_analyzer

    @property
    def request(self) -> Periodic1DRankNRefinementAnalysisRequest:
        """Return the exact refinement request bound to this action."""
        return self._request

    def _diagnostic(
        self,
        *,
        coarse_mesh_size: int,
        fine_mesh_size: int,
        coarse_value: float,
        fine_value: float,
    ) -> ScalarRefinementDiagnostics:
        controls = self._request.calculation_request.controls
        return self._scalar_refinement_analyzer.execute(
            coarse_mesh_size=coarse_mesh_size,
            fine_mesh_size=fine_mesh_size,
            coarse_value=coarse_value,
            fine_value=fine_value,
            denominator_floor=controls.refinement_denominator_floor,
            absolute_tolerance=controls.refinement_absolute_tolerance,
            relative_tolerance=controls.refinement_relative_tolerance,
        )

    def execute(self) -> Periodic1DRankNRefinementAnalysis:
        """Return complete block and scalar refinement inventories."""
        return Periodic1DRankNRefinementAnalysis(
            blocks=self._block_refinements(),
            scalars=self._scalar_refinements(),
        )

    def _block_refinements(
        self,
    ) -> tuple[Periodic1DRankNBlockRefinementResult, ...]:
        calculation_request = self._request.calculation_request
        meshes = self._request.meshes
        results: list[Periodic1DRankNBlockRefinementResult] = []
        for gauge_alignment in calculation_request.configuration.gauge_alignments:
            for coarse_mesh, fine_mesh in zip(meshes[:-1], meshes[1:], strict=True):
                coarse = next(
                    item
                    for item in coarse_mesh.gauge_alignment_results
                    if item.status.gauge_alignment is gauge_alignment
                )
                fine = next(
                    item
                    for item in fine_mesh.gauge_alignment_results
                    if item.status.gauge_alignment is gauge_alignment
                )
                if (
                    coarse.status.status is not Periodic1DRankNAlignmentStatus.QUALIFIED
                    or fine.status.status
                    is not Periodic1DRankNAlignmentStatus.QUALIFIED
                ):
                    continue
                if not np.array_equal(
                    coarse.coefficient_translations,
                    fine.coefficient_translations,
                ):
                    raise ValueError(
                        "adjacent block inventories must use identical translations"
                    )
                diagnostics = tuple(
                    self._diagnostic(
                        coarse_mesh_size=coarse_mesh.construction_mesh_size,
                        fine_mesh_size=fine_mesh.construction_mesh_size,
                        coarse_value=float(coarse_value),
                        fine_value=float(fine_value),
                    )
                    for coarse_value, fine_value in zip(
                        coarse.block_normalized_frobenius_norms,
                        fine.block_normalized_frobenius_norms,
                        strict=True,
                    )
                )
                absolute = np.asarray(
                    tuple(item.absolute_change for item in diagnostics),
                    dtype=np.float64,
                )
                relative = np.asarray(
                    tuple(item.relative_change for item in diagnostics),
                    dtype=np.float64,
                )
                applied = np.asarray(
                    tuple(item.applied_tolerance for item in diagnostics),
                    dtype=np.float64,
                )
                margins = np.asarray(
                    tuple(item.signed_margin for item in diagnostics),
                    dtype=np.float64,
                )
                results.append(
                    Periodic1DRankNBlockRefinementResult(
                        gauge_alignment=gauge_alignment,
                        coarse_mesh_size=coarse_mesh.construction_mesh_size,
                        fine_mesh_size=fine_mesh.construction_mesh_size,
                        translations=coarse.coefficient_translations,
                        coarse_normalized_block_norms=(
                            coarse.block_normalized_frobenius_norms
                        ),
                        fine_normalized_block_norms=(
                            fine.block_normalized_frobenius_norms
                        ),
                        absolute_changes=np.asarray(absolute, dtype=np.float64),
                        relative_changes=np.asarray(relative, dtype=np.float64),
                        applied_tolerances=np.asarray(applied, dtype=np.float64),
                        signed_margins=np.asarray(margins, dtype=np.float64),
                        all_pass=all(item.passes for item in diagnostics),
                    )
                )
        return tuple(results)

    def _scalar_refinements(
        self,
    ) -> tuple[Periodic1DRankNScalarRefinementResult, ...]:
        calculation_request = self._request.calculation_request
        meshes = self._request.meshes
        construction_sizes = calculation_request.configuration.construction_mesh_sizes
        coarse_size, fine_size = construction_sizes[-2:]
        coarse_mesh = next(
            mesh for mesh in meshes if mesh.construction_mesh_size == coarse_size
        )
        fine_mesh = next(
            mesh for mesh in meshes if mesh.construction_mesh_size == fine_size
        )
        results: list[Periodic1DRankNScalarRefinementResult] = []
        for gauge_alignment in calculation_request.configuration.gauge_alignments:
            coarse = next(
                item
                for item in coarse_mesh.gauge_alignment_results
                if item.status.gauge_alignment is gauge_alignment
            )
            fine = next(
                item
                for item in fine_mesh.gauge_alignment_results
                if item.status.gauge_alignment is gauge_alignment
            )
            if (
                coarse.status.status is not Periodic1DRankNAlignmentStatus.QUALIFIED
                or fine.status.status is not Periodic1DRankNAlignmentStatus.QUALIFIED
            ):
                continue
            coarse_inventory = Periodic1DRankNScalarDiagnosticInventoryExtractor(
                coarse
            ).execute()
            fine_inventory = Periodic1DRankNScalarDiagnosticInventoryExtractor(
                fine
            ).execute()
            if tuple(path for path, _ in coarse_inventory) != tuple(
                path for path, _ in fine_inventory
            ):
                raise ValueError("final scalar refinement inventories must agree")
            for (path, coarse_value), (_, fine_value) in zip(
                coarse_inventory,
                fine_inventory,
                strict=True,
            ):
                diagnostic = self._diagnostic(
                    coarse_mesh_size=coarse_mesh.construction_mesh_size,
                    fine_mesh_size=fine_mesh.construction_mesh_size,
                    coarse_value=coarse_value,
                    fine_value=fine_value,
                )
                results.append(
                    Periodic1DRankNScalarRefinementResult(
                        gauge_alignment=gauge_alignment,
                        diagnostic_path=path,
                        coarse_mesh_size=coarse_mesh.construction_mesh_size,
                        fine_mesh_size=fine_mesh.construction_mesh_size,
                        coarse_value=coarse_value,
                        fine_value=fine_value,
                        absolute_change=diagnostic.absolute_change,
                        relative_change=diagnostic.relative_change,
                        applied_tolerance=diagnostic.applied_tolerance,
                        signed_margin=diagnostic.signed_margin,
                        passes=diagnostic.passes,
                    )
                )
        return tuple(results)


__all__ = [
    "Periodic1DRankNRefinementAnalysis",
    "Periodic1DRankNRefinementAnalysisRequest",
    "Periodic1DRankNRefinementAnalyzer",
]
