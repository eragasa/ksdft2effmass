"""Periodic-2D rank-two restricted gauge-alignment action."""

from __future__ import annotations

from ksdft2effmass.band_equivalence_hopping_locality.alignment import (
    restricted_alignment_diagnostic,
)
from ksdft2effmass.periodic2d.rank2.gauge_alignment.base import (
    Periodic2DRank2GaugeAlignmentAnalyzer,
)

from .request import Periodic2DRank2RestrictedGaugeAlignmentAnalysisRequest
from .result import Periodic2DRank2RestrictedGaugeAlignmentAnalysis


class Periodic2DRank2RestrictedGaugeAlignmentAnalyzer(
    Periodic2DRank2GaugeAlignmentAnalyzer[
        Periodic2DRank2RestrictedGaugeAlignmentAnalysisRequest,
        Periodic2DRank2RestrictedGaugeAlignmentAnalysis,
    ]
):
    """Optimize one restricted global rotation through Project Koios."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic2DRank2RestrictedGaugeAlignmentAnalysisRequest,
    ) -> None:
        expected_type = Periodic2DRank2RestrictedGaugeAlignmentAnalysisRequest
        if type(request) is not expected_type:
            raise TypeError("request must be the exact periodic-2D alignment request")
        self._request = request

    @property
    def request(self) -> Periodic2DRank2RestrictedGaugeAlignmentAnalysisRequest:
        """Return the immutable request bound to this action."""
        return self._request

    def execute(self) -> Periodic2DRank2RestrictedGaugeAlignmentAnalysis:
        """Return the restricted global-rotation diagnostic."""
        diagnostic = restricted_alignment_diagnostic(
            self._request.reference,
            self._request.comparison,
        )
        return Periodic2DRank2RestrictedGaugeAlignmentAnalysis(
            rotation_angle=diagnostic.rotation_angle,
            rotation_degenerate=diagnostic.rotation_degenerate,
            splitting_scale=diagnostic.splitting_scale,
            maximum_correlation=diagnostic.maximum_correlation,
            minimum_operator_threshold=diagnostic.minimum_operator_threshold,
            exact_spectrum_joint_operator_threshold=(
                diagnostic.exact_spectrum_joint_operator_threshold
            ),
            request=self._request,
        )


__all__ = ["Periodic2DRank2RestrictedGaugeAlignmentAnalyzer"]
