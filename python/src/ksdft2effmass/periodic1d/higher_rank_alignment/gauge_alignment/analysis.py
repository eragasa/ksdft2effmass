"""Orchestrated analysis for one prescribed periodic-1D gauge alignment."""

from __future__ import annotations

from typing import final

from .assembly import (
    Periodic1DHigherRankGaugeAlignmentAssemblyRequest,
    Periodic1DHigherRankGaugeAlignmentResultAssembler,
)
from .fourier import (
    Periodic1DHigherRankFourierAnalysisRequest,
    Periodic1DHigherRankFourierAnalyzer,
)
from .interpolation import (
    Periodic1DHigherRankInterpolationAnalysisRequest,
    Periodic1DHigherRankInterpolationAnalyzer,
)
from .locality import (
    Periodic1DHigherRankLocalityAnalysisRequest,
    Periodic1DHigherRankLocalityAnalyzer,
)
from .recovery import (
    Periodic1DHigherRankRecoveryAnalysisRequest,
    Periodic1DHigherRankRecoveryAnalyzer,
)
from .request import Periodic1DHigherRankGaugeAlignmentAnalysisRequest
from .results import Periodic1DHigherRankGaugeAlignmentMeshResult


@final
class Periodic1DHigherRankGaugeAlignmentAnalyzer:
    """Run the typed recovery, Fourier, interpolation, and locality lifecycle."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic1DHigherRankGaugeAlignmentAnalysisRequest,
    ) -> None:
        """Bind one complete gauge-alignment analysis request."""
        if type(request) is not Periodic1DHigherRankGaugeAlignmentAnalysisRequest:
            raise TypeError(
                "request must be Periodic1DHigherRankGaugeAlignmentAnalysisRequest"
            )
        self._request = request

    @property
    def request(self) -> Periodic1DHigherRankGaugeAlignmentAnalysisRequest:
        """Return the exact immutable analysis request bound at construction."""
        return self._request

    def execute(self) -> Periodic1DHigherRankGaugeAlignmentMeshResult:
        """Execute and assemble the ordered gauge-alignment analysis lifecycle."""
        recovery = Periodic1DHigherRankRecoveryAnalyzer(
            Periodic1DHigherRankRecoveryAnalysisRequest(self._request)
        ).execute()
        fourier = Periodic1DHigherRankFourierAnalyzer(
            request=Periodic1DHigherRankFourierAnalysisRequest(self._request),
        ).execute()
        interpolation = Periodic1DHigherRankInterpolationAnalyzer(
            request=Periodic1DHigherRankInterpolationAnalysisRequest(
                analysis_request=self._request,
                fourier_analysis=fourier,
            ),
        ).execute()
        locality = Periodic1DHigherRankLocalityAnalyzer(
            request=Periodic1DHigherRankLocalityAnalysisRequest(
                analysis_request=self._request,
                fourier_analysis=fourier,
                interpolation_analysis=interpolation,
            ),
        ).execute()
        return Periodic1DHigherRankGaugeAlignmentResultAssembler(
            Periodic1DHigherRankGaugeAlignmentAssemblyRequest(
                analysis_request=self._request,
                recovery_analysis=recovery,
                fourier_analysis=fourier,
                interpolation_analysis=interpolation,
                locality_analysis=locality,
            )
        ).execute()


__all__ = [
    "Periodic1DHigherRankGaugeAlignmentAnalysisRequest",
    "Periodic1DHigherRankGaugeAlignmentAnalyzer",
]
