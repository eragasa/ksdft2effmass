"""Orchestrated analysis for one prescribed periodic-1D gauge alignment."""

from __future__ import annotations

from typing import final

from ksdft2effmass.gauge_alignment import GaugeAlignmentAnalyzer
from ksdft2effmass.periodic1d.rankN.gauge_alignment.fourier import (
    Periodic1DRankNFourierAnalysisRequest,
    Periodic1DRankNFourierAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.interpolation import (
    Periodic1DRankNInterpolationAnalysisRequest,
    Periodic1DRankNInterpolationAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.recovery import (
    Periodic1DRankNRecoveryAnalysisRequest,
    Periodic1DRankNRecoveryAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.request import (
    Periodic1DRankNGaugeAlignmentAnalysisRequest,
)
from ksdft2effmass.periodic1d.rankN.hopping_locality import (
    Periodic1DRankNHoppingLocalityAnalysisRequest,
    Periodic1DRankNHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.support_truncation import (
    Periodic1DRankNSupportTruncationAnalysisRequest,
    Periodic1DRankNSupportTruncationAnalyzer,
)

from ..assembly import (
    Periodic1DRankNGaugeAlignmentAssemblyRequest,
    Periodic1DRankNGaugeAlignmentResultAssembler,
)
from ..result.gauge_alignment import Periodic1DRankNGaugeAlignmentMeshResult


@final
class Periodic1DRankNGaugeAlignmentAnalyzer(
    GaugeAlignmentAnalyzer[
        Periodic1DRankNGaugeAlignmentAnalysisRequest,
        Periodic1DRankNGaugeAlignmentMeshResult,
    ]
):
    """Run the typed recovery, Fourier, interpolation, and locality lifecycle."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic1DRankNGaugeAlignmentAnalysisRequest,
    ) -> None:
        """Bind one complete gauge-alignment analysis request."""
        if type(request) is not Periodic1DRankNGaugeAlignmentAnalysisRequest:
            raise TypeError(
                "request must be Periodic1DRankNGaugeAlignmentAnalysisRequest"
            )
        self._request = request

    @property
    def request(self) -> Periodic1DRankNGaugeAlignmentAnalysisRequest:
        """Return the exact immutable analysis request bound at construction."""
        return self._request

    def execute(self) -> Periodic1DRankNGaugeAlignmentMeshResult:
        """Execute and assemble the ordered gauge-alignment analysis lifecycle."""
        recovery = Periodic1DRankNRecoveryAnalyzer(
            Periodic1DRankNRecoveryAnalysisRequest(self._request)
        ).execute()
        fourier = Periodic1DRankNFourierAnalyzer(
            request=Periodic1DRankNFourierAnalysisRequest(self._request),
        ).execute()
        interpolation = Periodic1DRankNInterpolationAnalyzer(
            request=Periodic1DRankNInterpolationAnalysisRequest(
                analysis_request=self._request,
                fourier_analysis=fourier,
            ),
        ).execute()
        hopping_locality = Periodic1DRankNHoppingLocalityAnalyzer(
            request=Periodic1DRankNHoppingLocalityAnalysisRequest(
                analysis_request=self._request,
                fourier_analysis=fourier,
            ),
        ).execute()
        support_truncation = Periodic1DRankNSupportTruncationAnalyzer(
            request=Periodic1DRankNSupportTruncationAnalysisRequest(
                analysis_request=self._request,
                fourier_analysis=fourier,
                interpolation_analysis=interpolation,
                hopping_locality_analysis=hopping_locality,
            ),
        ).execute()
        return Periodic1DRankNGaugeAlignmentResultAssembler(
            Periodic1DRankNGaugeAlignmentAssemblyRequest(
                analysis_request=self._request,
                recovery_analysis=recovery,
                fourier_analysis=fourier,
                interpolation_analysis=interpolation,
                hopping_locality_analysis=hopping_locality,
                support_truncation_analysis=support_truncation,
            )
        ).execute()


__all__ = [
    "Periodic1DRankNGaugeAlignmentAnalysisRequest",
    "Periodic1DRankNGaugeAlignmentAnalyzer",
]
