"""Canonical scalar-diagnostic inventory for higher-rank refinement."""

from __future__ import annotations

from typing import final

from ksdft2effmass.periodic1d.rankN.gauge_alignment.results import (
    Periodic1DRankNGaugeAlignmentMeshResult,
)

from .definition import Periodic1DRankNAlignmentStatus


@final
class Periodic1DRankNScalarDiagnosticInventoryExtractor:
    """Extract scalar diagnostics from one qualified gauge-alignment result."""

    __slots__ = ("_gauge_alignment_result",)

    def __init__(
        self, gauge_alignment: Periodic1DRankNGaugeAlignmentMeshResult
    ) -> None:
        if type(gauge_alignment) is not Periodic1DRankNGaugeAlignmentMeshResult:
            raise TypeError(
                "gauge_alignment must be the exact gauge-alignment result record"
            )
        if (
            gauge_alignment.status.status
            is not Periodic1DRankNAlignmentStatus.QUALIFIED
        ):
            raise ValueError("scalar inventory requires a qualified gauge alignment")
        self._gauge_alignment_result = gauge_alignment

    @property
    def gauge_alignment(self) -> Periodic1DRankNGaugeAlignmentMeshResult:
        """Return the exact gauge-alignment result bound to this action."""
        return self._gauge_alignment_result

    def execute(self) -> tuple[tuple[str, float], ...]:
        """Return the canonical path/value inventory for refinement."""
        gauge_alignment = self._gauge_alignment_result
        interpolation = gauge_alignment.interpolation
        if interpolation is None:
            raise ValueError("qualified alignment requires interpolation diagnostics")
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
                gauge_alignment.coefficient_translations,
                gauge_alignment.block_normalized_frobenius_norms,
                strict=True,
            )
        )
        for support in gauge_alignment.supports:
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


__all__ = ["Periodic1DRankNScalarDiagnosticInventoryExtractor"]
