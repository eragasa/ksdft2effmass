"""Canonical scalar-diagnostic inventory for higher-rank refinement."""

from __future__ import annotations

from typing import final

from .channel_results import Periodic1DHigherRankChannelMeshResult
from .definition import Periodic1DHigherRankAlignmentStatus


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

    @property
    def channel(self) -> Periodic1DHigherRankChannelMeshResult:
        """Return the exact channel result bound to this inventory action."""
        return self._channel

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


__all__ = ["Periodic1DHigherRankScalarDiagnosticInventoryExtractor"]
