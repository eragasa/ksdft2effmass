"""Typed periodic-2D rank-two band-equivalence/locality result ownership."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.band_equivalence_hopping_locality.records import (
    BandEquivalenceHoppingLocalityDiagnostics,
)
from ksdft2effmass.band_equivalence_hopping_locality.result import (
    BandEquivalenceHoppingLocalityAnalysisRecorder,
    BandEquivalenceHoppingLocalityCalculationResult,
)
from ksdft2effmass.periodic2d.base import Periodic2DCapability
from ksdft2effmass.serialization import SerializableValue

from .analysis import Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis
from .request import Periodic2DRank2BandEquivalenceHoppingLocalityRequest


@dataclass(frozen=True, slots=True)
class Periodic2DRank2BandEquivalenceHoppingLocalityCalculationResult(
    BandEquivalenceHoppingLocalityCalculationResult,
    Periodic2DCapability,
):
    """Retain a periodic-2D rank-two calculation with its exact typed request."""

    request: Periodic2DRank2BandEquivalenceHoppingLocalityRequest

    def __post_init__(self) -> None:
        if (
            type(self.request)
            is not Periodic2DRank2BandEquivalenceHoppingLocalityRequest
        ):
            raise TypeError(
                "request must be Periodic2DRank2BandEquivalenceHoppingLocalityRequest"
            )
        super().__post_init__()

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {"request", "diagnostics"}:
            raise ValueError("band-equivalence calculation-result fields do not match")
        request = values["request"]
        diagnostics = values["diagnostics"]
        if not isinstance(request, Mapping) or not isinstance(diagnostics, Mapping):
            raise TypeError("calculation-result values must decode to mappings")
        return cls(
            request=Periodic2DRank2BandEquivalenceHoppingLocalityRequest.from_dict(
                request
            ),
            diagnostics=BandEquivalenceHoppingLocalityDiagnostics.from_dict(
                diagnostics
            ),
        )


class Periodic2DRank2BandEquivalenceHoppingLocalityAnalysisRecorder(
    Periodic2DCapability
):
    """Project one rank-first analysis through the shared typed recorder."""

    __slots__ = ("_analysis", "_delegate")

    def __init__(
        self,
        analysis: Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis,
    ) -> None:
        if type(analysis) is not Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis:
            raise TypeError(
                "analysis must be Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis"
            )
        self._analysis = analysis
        self._delegate = BandEquivalenceHoppingLocalityAnalysisRecorder(analysis)

    @property
    def analysis(self) -> Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis:
        """Return the immutable scientific analysis bound to this recorder."""
        return self._analysis

    def result(self) -> Periodic2DRank2BandEquivalenceHoppingLocalityCalculationResult:
        """Return the dimension- and rank-qualified retained projection."""
        common = self._delegate.result()
        return Periodic2DRank2BandEquivalenceHoppingLocalityCalculationResult(
            request=self._analysis.request,
            diagnostics=common.diagnostics,
        )


__all__ = [
    "Periodic2DRank2BandEquivalenceHoppingLocalityAnalysisRecorder",
    "Periodic2DRank2BandEquivalenceHoppingLocalityCalculationResult",
]
