"""Rank-N hopping-locality diagnostics for periodic one dimension."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

from ksdft2effmass.analysis.matrix_field.diagnostics import (
    SymmetricRangeTailAnalyzer1D,
    SymmetricRangeTailMonotonicityAnalyzer1D,
    SymmetricRangeTailMonotonicityDiagnostics1D,
)
from ksdft2effmass.periodic1d.hopping_locality import Periodic1DHoppingLocality
from ksdft2effmass.periodic1d.rankN.gauge_alignment.fourier import (  # noqa: E501
    Periodic1DRankNFourierAnalysis,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.request import (  # noqa: E501
    Periodic1DRankNGaugeAlignmentAnalysisRequest,
)

from .result import Periodic1DRankNHoppingTailResult


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNHoppingLocalityAnalysisRequest:
    """Bind an unchanged Fourier series for hopping-locality diagnostics."""

    analysis_request: Periodic1DRankNGaugeAlignmentAnalysisRequest
    fourier_analysis: Periodic1DRankNFourierAnalysis

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not Periodic1DRankNGaugeAlignmentAnalysisRequest
        ):
            raise TypeError(
                "analysis_request must be the exact gauge-alignment request"
            )
        if type(self.fourier_analysis) is not Periodic1DRankNFourierAnalysis:
            raise TypeError("fourier_analysis must be the exact Fourier analysis")
        if self.fourier_analysis.analysis_request is not self.analysis_request:
            raise ValueError("Fourier analysis must derive from the bound request")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNHoppingLocalityAnalysis(Periodic1DHoppingLocality):
    """Retain coefficient tails without removing real-space support."""

    analysis_request: Periodic1DRankNGaugeAlignmentAnalysisRequest
    tails: tuple[Periodic1DRankNHoppingTailResult, ...]
    monotonicity: tuple[SymmetricRangeTailMonotonicityDiagnostics1D, ...]
    maximum_tail_increase: float
    all_tail_monotonicity_checks_pass: bool

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not Periodic1DRankNGaugeAlignmentAnalysisRequest
        ):
            raise TypeError("analysis_request must be the exact analysis request")
        if type(self.tails) is not tuple or not all(
            type(item) is Periodic1DRankNHoppingTailResult for item in self.tails
        ):
            raise TypeError("tails must contain exact hopping-tail results")
        expected_ranges = (
            self.analysis_request.calculation_request.controls.support_radii
        )
        if tuple(item.maximum_range for item in self.tails) != expected_ranges:
            raise ValueError("tails must follow the frozen diagnostic-range inventory")
        if type(self.monotonicity) is not tuple or not all(
            type(item) is SymmetricRangeTailMonotonicityDiagnostics1D
            for item in self.monotonicity
        ):
            raise TypeError("monotonicity must contain exact generic diagnostics")
        expected_pairs = tuple(
            zip(expected_ranges[:-1], expected_ranges[1:], strict=True)
        )
        actual_pairs = tuple(
            (item.coarse_maximum_range, item.fine_maximum_range)
            for item in self.monotonicity
        )
        if actual_pairs != expected_pairs:
            raise ValueError("monotonicity must cover consecutive diagnostic ranges")
        if type(self.maximum_tail_increase) is not float:
            raise TypeError("maximum_tail_increase must be a built-in float")
        expected_maximum = max(
            max(
                item.normalized_squared_weight_increase,
                item.normalized_l2_norm_increase,
                item.normalized_l1_norm_increase,
            )
            for item in self.monotonicity
        )
        if self.maximum_tail_increase != expected_maximum:
            raise ValueError("maximum_tail_increase is inconsistent")
        if type(self.all_tail_monotonicity_checks_pass) is not bool:
            raise TypeError("all_tail_monotonicity_checks_pass must be a built-in bool")
        if self.all_tail_monotonicity_checks_pass is not all(
            item.passes for item in self.monotonicity
        ):
            raise ValueError("tail-monotonicity disposition is inconsistent")


@final
class Periodic1DRankNHoppingLocalityAnalyzer:
    """Measure coefficient tails without constructing truncated operators."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic1DRankNHoppingLocalityAnalysisRequest,
    ) -> None:
        if type(request) is not Periodic1DRankNHoppingLocalityAnalysisRequest:
            raise TypeError(
                "request must be Periodic1DRankNHoppingLocalityAnalysisRequest"
            )
        self._request = request

    @property
    def request(self) -> Periodic1DRankNHoppingLocalityAnalysisRequest:
        """Return the exact hopping-locality request bound to this action."""
        return self._request

    def execute(self) -> Periodic1DRankNHoppingLocalityAnalysis:
        """Return hopping tails and their nested-range monotonicity evidence."""
        analysis_request = self._request.analysis_request
        controls = analysis_request.calculation_request.controls
        series = self._request.fourier_analysis.transform.series
        generic_tails = tuple(
            SymmetricRangeTailAnalyzer1D().execute(
                series,
                maximum_range,
                controls.energy_reference,
            )
            for maximum_range in controls.support_radii
        )
        monotonicity = SymmetricRangeTailMonotonicityAnalyzer1D().execute(
            generic_tails,
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
        return Periodic1DRankNHoppingLocalityAnalysis(
            analysis_request=analysis_request,
            tails=tuple(
                Periodic1DRankNHoppingTailResult.from_diagnostics(item)
                for item in generic_tails
            ),
            monotonicity=monotonicity,
            maximum_tail_increase=maximum_tail_increase,
            all_tail_monotonicity_checks_pass=all(item.passes for item in monotonicity),
        )


__all__ = [
    "Periodic1DRankNHoppingLocalityAnalysis",
    "Periodic1DRankNHoppingLocalityAnalysisRequest",
    "Periodic1DRankNHoppingLocalityAnalyzer",
]
