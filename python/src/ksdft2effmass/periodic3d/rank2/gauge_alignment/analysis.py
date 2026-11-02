"""Periodic-3D rank-two restricted gauge-alignment action."""

from __future__ import annotations

from ksdft2effmass.band_equivalence_hopping_locality.alignment import (
    restricted_alignment_diagnostic,
)
from ksdft2effmass.periodic3d.gauge_alignment.base import (
    Periodic3DGaugeAlignmentAnalyzer,
)

from .request import Periodic3DRank2RestrictedGaugeAlignmentAnalysisRequest
from .result import Periodic3DRank2RestrictedGaugeAlignmentAnalysis


class Periodic3DRank2RestrictedGaugeAlignmentAnalyzer(
    Periodic3DGaugeAlignmentAnalyzer[
        Periodic3DRank2RestrictedGaugeAlignmentAnalysisRequest,
        Periodic3DRank2RestrictedGaugeAlignmentAnalysis,
    ]
):
    """Optimize one restricted global rotation through Project Koios."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic3DRank2RestrictedGaugeAlignmentAnalysisRequest,
    ) -> None:
        expected_type = Periodic3DRank2RestrictedGaugeAlignmentAnalysisRequest
        if type(request) is not expected_type:
            raise TypeError("request must be the exact periodic-3D alignment request")
        self._request = request

    @property
    def request(self) -> Periodic3DRank2RestrictedGaugeAlignmentAnalysisRequest:
        """Return the immutable request bound to this action."""
        return self._request

    def execute(self) -> Periodic3DRank2RestrictedGaugeAlignmentAnalysis:
        """Return the restricted global-rotation diagnostic."""
        diagnostic = restricted_alignment_diagnostic(
            self._request.reference,
            self._request.comparison,
        )
        return Periodic3DRank2RestrictedGaugeAlignmentAnalysis(
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


__all__ = ["Periodic3DRank2RestrictedGaugeAlignmentAnalyzer"]
