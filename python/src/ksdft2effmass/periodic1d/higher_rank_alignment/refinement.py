"""Request-bound refinement analysis for higher-rank alignment results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

import numpy as np

from ksdft2effmass.analysis.matrix_field.diagnostics import (
    ScalarRefinementAnalyzer,
    ScalarRefinementDiagnostics,
)

from .calculation import Periodic1DHigherRankAlignmentCalculationRequest
from .channel_results import (
    Periodic1DHigherRankChannelMeshResult,
    Periodic1DHigherRankMeshCalculationResult,
)
from .definition import Periodic1DHigherRankAlignmentStatus
from .refinement_results import (
    Periodic1DHigherRankBlockRefinementResult,
    Periodic1DHigherRankScalarRefinementResult,
)


@final
class Periodic1DHigherRankScalarDiagnosticInventoryExtractor:
    """Extract the scalar diagnostics owned by one qualified channel result."""

    __slots__ = ("_channel",)

    def __init__(self, channel: Periodic1DHigherRankChannelMeshResult) -> None:
        if type(channel) is not Periodic1DHigherRankChannelMeshResult:
            raise TypeError("channel must be the exact channel result record")
        if channel.status.status is not Periodic1DHigherRankAlignmentStatus.QUALIFIED:
            raise ValueError("scalar inventory requires a qualified channel")
        self._channel = channel

    def execute(self) -> tuple[tuple[str, float], ...]:
        """Return the canonical path/value inventory for refinement."""
        channel = self._channel
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


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DHigherRankRefinementAnalysisRequest:
    """Bind one calculation request and its complete construction-mesh results."""

    calculation_request: Periodic1DHigherRankAlignmentCalculationRequest
    meshes: tuple[Periodic1DHigherRankMeshCalculationResult, ...]

    def __post_init__(self) -> None:
        if (
            type(self.calculation_request)
            is not Periodic1DHigherRankAlignmentCalculationRequest
        ):
            raise TypeError("calculation_request must be the exact request record")
        if type(self.meshes) is not tuple or any(
            type(mesh) is not Periodic1DHigherRankMeshCalculationResult
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
                channel.status for channel in mesh.channels
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
class Periodic1DHigherRankRefinementAnalysis:
    """Retain block and scalar refinement records from one complete request."""

    blocks: tuple[Periodic1DHigherRankBlockRefinementResult, ...]
    scalars: tuple[Periodic1DHigherRankScalarRefinementResult, ...]

    def __post_init__(self) -> None:
        if type(self.blocks) is not tuple or any(
            type(item) is not Periodic1DHigherRankBlockRefinementResult
            for item in self.blocks
        ):
            raise TypeError("blocks must contain exact block refinement records")
        if type(self.scalars) is not tuple or any(
            type(item) is not Periodic1DHigherRankScalarRefinementResult
            for item in self.scalars
        ):
            raise TypeError("scalars must contain exact scalar refinement records")


@final
class Periodic1DHigherRankRefinementAnalyzer:
    """Calculate adjacent block and final-pair scalar refinement evidence."""

    __slots__ = ("_request", "_scalar_refinement_analyzer")

    def __init__(
        self,
        *,
        request: Periodic1DHigherRankRefinementAnalysisRequest,
        scalar_refinement_analyzer: ScalarRefinementAnalyzer,
    ) -> None:
        """Bind the complete request and canonical scalar-refinement owner."""
        if type(request) is not Periodic1DHigherRankRefinementAnalysisRequest:
            raise TypeError(
                "request must be Periodic1DHigherRankRefinementAnalysisRequest"
            )
        if type(scalar_refinement_analyzer) is not ScalarRefinementAnalyzer:
            raise TypeError(
                "scalar_refinement_analyzer must be ScalarRefinementAnalyzer"
            )
        self._request = request
        self._scalar_refinement_analyzer = scalar_refinement_analyzer

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

    def execute(self) -> Periodic1DHigherRankRefinementAnalysis:
        """Return complete block and scalar refinement inventories."""
        return Periodic1DHigherRankRefinementAnalysis(
            blocks=self._block_refinements(),
            scalars=self._scalar_refinements(),
        )

    def _block_refinements(
        self,
    ) -> tuple[Periodic1DHigherRankBlockRefinementResult, ...]:
        calculation_request = self._request.calculation_request
        meshes = self._request.meshes
        results: list[Periodic1DHigherRankBlockRefinementResult] = []
        for channel in calculation_request.configuration.alignment_channels:
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
                    Periodic1DHigherRankBlockRefinementResult(
                        channel=channel,
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
    ) -> tuple[Periodic1DHigherRankScalarRefinementResult, ...]:
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
        results: list[Periodic1DHigherRankScalarRefinementResult] = []
        for channel in calculation_request.configuration.alignment_channels:
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
            coarse_inventory = Periodic1DHigherRankScalarDiagnosticInventoryExtractor(
                coarse
            ).execute()
            fine_inventory = Periodic1DHigherRankScalarDiagnosticInventoryExtractor(
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
                    Periodic1DHigherRankScalarRefinementResult(
                        channel=channel,
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
    "Periodic1DHigherRankRefinementAnalysis",
    "Periodic1DHigherRankRefinementAnalysisRequest",
    "Periodic1DHigherRankRefinementAnalyzer",
]
