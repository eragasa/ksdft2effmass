"""Request-bound refinement analysis for higher-rank alignment results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

import numpy as np

from .calculation import (
    Periodic1DHigherRankAlignmentCalculationRequest,
    Periodic1DHigherRankBlockRefinementResult,
    Periodic1DHigherRankChannelMeshResult,
    Periodic1DHigherRankMeshCalculationResult,
    Periodic1DHigherRankScalarRefinementResult,
)
from .definition import Periodic1DHigherRankAlignmentStatus


@dataclass(frozen=True, slots=True)
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
        if tuple(mesh.construction_mesh_size for mesh in self.meshes) != (
            self.calculation_request.configuration.construction_mesh_sizes
        ):
            raise ValueError("refinement meshes must match the calculation request")


@dataclass(frozen=True, slots=True)
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

    __slots__ = ("_request",)

    def __init__(self, request: Periodic1DHigherRankRefinementAnalysisRequest) -> None:
        """Bind the complete immutable refinement-analysis request."""
        if type(request) is not Periodic1DHigherRankRefinementAnalysisRequest:
            raise TypeError(
                "request must be Periodic1DHigherRankRefinementAnalysisRequest"
            )
        self._request = request

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
        controls = calculation_request.controls
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
                applied = controls.refinement_absolute_tolerance + (
                    controls.refinement_relative_tolerance
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
    ) -> tuple[Periodic1DHigherRankScalarRefinementResult, ...]:
        calculation_request = self._request.calculation_request
        controls = calculation_request.controls
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
            coarse_inventory = self._scalar_inventory(coarse)
            fine_inventory = self._scalar_inventory(fine)
            if tuple(path for path, _ in coarse_inventory) != tuple(
                path for path, _ in fine_inventory
            ):
                raise ValueError("final scalar refinement inventories must agree")
            for (path, coarse_value), (_, fine_value) in zip(
                coarse_inventory,
                fine_inventory,
                strict=True,
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


__all__ = [
    "Periodic1DHigherRankRefinementAnalysis",
    "Periodic1DHigherRankRefinementAnalysisRequest",
    "Periodic1DHigherRankRefinementAnalyzer",
]
