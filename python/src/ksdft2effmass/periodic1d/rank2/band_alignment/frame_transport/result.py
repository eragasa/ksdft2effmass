"""Result values for rank-two periodic frame transport."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.solidstate.band_frames import (
    PolarBandFrameTransportResult1D,
    ReciprocalBandFramePath1D,
)

from .request import Periodic1DRank2TransportAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRank2ResolvedTransportAnalysis:
    """Correlate one rank-two transport request with its owner result."""

    request: Periodic1DRank2TransportAnalysisRequest
    owner_result: PolarBandFrameTransportResult1D

    def __post_init__(self) -> None:
        if type(self.request) is not Periodic1DRank2TransportAnalysisRequest:
            raise TypeError("request must be the exact rank-two transport request")
        if type(self.owner_result) is not PolarBandFrameTransportResult1D:
            raise TypeError("owner_result must be PolarBandFrameTransportResult1D")
        if self.owner_result.source is not self.request.source:
            raise ValueError("owner result source must be the requested frame path")
        if (
            self.owner_result.overlap_singular_value_threshold
            != self.request.overlap_singular_value_threshold
        ):
            raise ValueError("owner result threshold must match the request")

    @property
    def transported(self) -> ReciprocalBandFramePath1D:
        """Return the transported closed frame path."""
        return self.owner_result.transported

    @property
    def minimum_overlap_singular_value(self) -> float:
        """Return the minimum admitted neighbor or closure singular value."""
        return self.owner_result.minimum_overlap_singular_value

    @property
    def closure_eigenphases(self) -> tuple[float, ...]:
        """Return the ordered closure-unitary eigenphases in radians."""
        return self.owner_result.closure_eigenphases


__all__ = ["Periodic1DRank2ResolvedTransportAnalysis"]
