"""Typed periodic-3D rank-two band-equivalence/locality result ownership."""

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
from ksdft2effmass.serialization import SerializableValue

from .analysis import Periodic3DRank2BandEquivalenceHoppingLocalityAnalysis
from .base import (
    Periodic3DRank2BandEquivalenceHoppingLocalityAction,
    Periodic3DRank2BandEquivalenceHoppingLocalityValue,
)
from .request import Periodic3DRank2BandEquivalenceHoppingLocalityRequest


@dataclass(frozen=True, slots=True)
class Periodic3DRank2BandEquivalenceHoppingLocalityCalculationResult(
    BandEquivalenceHoppingLocalityCalculationResult,
    Periodic3DRank2BandEquivalenceHoppingLocalityValue,
):
    """Retain a periodic-3D rank-two calculation with its exact typed request."""

    request: Periodic3DRank2BandEquivalenceHoppingLocalityRequest

    def __post_init__(self) -> None:
        if (
            type(self.request)
            is not Periodic3DRank2BandEquivalenceHoppingLocalityRequest
        ):
            raise TypeError(
                "request must be Periodic3DRank2BandEquivalenceHoppingLocalityRequest"
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
            request=Periodic3DRank2BandEquivalenceHoppingLocalityRequest.from_dict(
                request
            ),
            diagnostics=BandEquivalenceHoppingLocalityDiagnostics.from_dict(
                diagnostics
            ),
        )


class Periodic3DRank2BandEquivalenceHoppingLocalityAnalysisRecorder(
    Periodic3DRank2BandEquivalenceHoppingLocalityAction
):
    """Project one rank-first analysis through the shared typed recorder."""

    __slots__ = ("_analysis", "_delegate")

    def __init__(
        self,
        analysis: Periodic3DRank2BandEquivalenceHoppingLocalityAnalysis,
    ) -> None:
        if type(analysis) is not Periodic3DRank2BandEquivalenceHoppingLocalityAnalysis:
            raise TypeError(
                "analysis must be Periodic3DRank2BandEquivalenceHoppingLocalityAnalysis"
            )
        self._analysis = analysis
        self._delegate = BandEquivalenceHoppingLocalityAnalysisRecorder(analysis)

    @property
    def analysis(self) -> Periodic3DRank2BandEquivalenceHoppingLocalityAnalysis:
        """Return the immutable scientific analysis bound to this recorder."""
        return self._analysis

    def result(self) -> Periodic3DRank2BandEquivalenceHoppingLocalityCalculationResult:
        """Return the dimension- and rank-qualified retained projection."""
        common = self._delegate.result()
        return Periodic3DRank2BandEquivalenceHoppingLocalityCalculationResult(
            request=self._analysis.request,
            diagnostics=common.diagnostics,
        )


__all__ = [
    "Periodic3DRank2BandEquivalenceHoppingLocalityAnalysisRecorder",
    "Periodic3DRank2BandEquivalenceHoppingLocalityCalculationResult",
]
