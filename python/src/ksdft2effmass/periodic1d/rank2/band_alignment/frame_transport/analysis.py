"""Rank-two periodic frame-transport analysis."""

from __future__ import annotations

from typing import final

from ksdft2effmass.solidstate.band_frames import (
    PolarBandFrameTransporter1D,
    PolarBandFrameTransportRequest1D,
)

from .request import Periodic1DRank2TransportAnalysisRequest
from .result import Periodic1DRank2ResolvedTransportAnalysis


@final
class Periodic1DRank2TransportAnalyzer:
    """Transport one admitted rank-two raw frame path into a closed gauge."""

    __slots__ = ("_request",)

    def __init__(self, request: Periodic1DRank2TransportAnalysisRequest) -> None:
        if type(request) is not Periodic1DRank2TransportAnalysisRequest:
            raise TypeError("request must be the exact rank-two transport request")
        self._request = request

    @property
    def request(self) -> Periodic1DRank2TransportAnalysisRequest:
        """Return the complete immutable transport-analysis request."""
        return self._request

    def execute(self) -> Periodic1DRank2ResolvedTransportAnalysis:
        """Return the transported path and its overlap and closure diagnostics."""
        request = self.request
        owner_result = PolarBandFrameTransporter1D(
            PolarBandFrameTransportRequest1D(
                request.source,
                request.overlap_singular_value_threshold,
            )
        ).execute()
        return Periodic1DRank2ResolvedTransportAnalysis(
            request=request,
            owner_result=owner_result,
        )


__all__ = ["Periodic1DRank2TransportAnalyzer"]
