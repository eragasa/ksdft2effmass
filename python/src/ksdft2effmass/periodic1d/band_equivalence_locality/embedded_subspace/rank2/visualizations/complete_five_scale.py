"""Downstream rendering of authenticated complete-five-scale projection data."""

from __future__ import annotations

from ..retention.complete_five_scale_visualization_data import (
    Periodic1DRank2CompleteFiveScaleVisualizationData,
)


class Periodic1DRank2CompleteFiveScaleSummaryRenderer:
    """Render one admitted summary projection without scientific recomputation."""

    __slots__ = ("_data",)

    def __init__(
        self,
        data: Periodic1DRank2CompleteFiveScaleVisualizationData,
    ) -> None:
        if type(data) is not Periodic1DRank2CompleteFiveScaleVisualizationData:
            raise TypeError("data must be complete-five-scale visualization data")
        self._data = data

    def render(self) -> bytes:
        """Return a deterministic Markdown summary of stored projection values."""
        lines = [
            "# Complete five-scale finite-control summary",
            "",
            f"Authenticated calculation-record SHA-256: `{self._data.source_sha256}`",
            "",
            "| Parent scale | Momentum disposition | Principal points | "
            "Principal ranges |",
            "|---:|---|---:|---:|",
        ]
        lines.extend(
            f"| {scale:.17g} | {momentum} | {point_count} | {range_count} |"
            for scale, momentum, point_count, range_count in zip(
                self._data.parent_hopping_scales,
                self._data.momentum_dispositions,
                self._data.principal_truncation_point_counts,
                self._data.principal_truncation_range_counts,
                strict=True,
            )
        )
        lines.extend(
            (
                "",
                "Adaptive-amplitude disposition: "
                f"`{self._data.adaptive_amplitude_disposition}`",
                "",
                "| Construction mesh | Evaluation mesh | Changes from previous mesh |",
                "|---:|---:|---:|",
            )
        )
        for index, (construction_size, evaluation_size) in enumerate(
            zip(
                self._data.construction_mesh_sizes,
                self._data.evaluation_mesh_sizes,
                strict=True,
            )
        ):
            change_count = (
                "—"
                if index == 0
                else str(self._data.adjacent_decision_change_counts[index - 1])
            )
            lines.append(
                f"| {construction_size} | {evaluation_size} | {change_count} |"
            )
        lines.extend(
            (
                "",
                "This presentation reports stored finite-control values only. It does "
                "not establish continuum convergence or scientific validation.",
            )
        )
        return ("\n".join(lines) + "\n").encode("utf-8")


__all__ = ["Periodic1DRank2CompleteFiveScaleSummaryRenderer"]
