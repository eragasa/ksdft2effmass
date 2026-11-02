"""Request-bound typed result for band-equivalence locality calculations."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .analysis import BandEquivalenceHoppingLocalityAnalysis
from .definitions import BandEquivalenceHoppingLocalityRequest
from .records import BandEquivalenceHoppingLocalityDiagnostics, CaseDiagnostic


@dataclass(frozen=True, slots=True)
class BandEquivalenceHoppingLocalityCalculationResult(BaseTypedRecord):
    """Retain one complete calculation with its exact scientific request."""

    request: BandEquivalenceHoppingLocalityRequest
    diagnostics: BandEquivalenceHoppingLocalityDiagnostics

    def __post_init__(self) -> None:
        if not isinstance(self.request, BandEquivalenceHoppingLocalityRequest):
            raise TypeError("request must be BandEquivalenceHoppingLocalityRequest")
        if type(self.diagnostics) is not BandEquivalenceHoppingLocalityDiagnostics:
            raise TypeError(
                "diagnostics must be BandEquivalenceHoppingLocalityDiagnostics"
            )
        if self.diagnostics.family is not self.request.family:
            raise ValueError("diagnostics family must match the request")
        if (
            self.diagnostics.construction_size != self.request.construction_size
            or self.diagnostics.evaluation_size != self.request.evaluation_size
        ):
            raise ValueError("diagnostic mesh sizes must match the request")
        if tuple(case.name for case in self.diagnostics.cases) != tuple(
            case.name for case in self.request.cases
        ):
            raise ValueError("diagnostic case inventory must match the request")
        expected_points = tuple(
            (parent_scale, amplitude)
            for parent_scale in self.request.parent_scales
            for amplitude in self.request.amplitudes
        )
        for case in self.diagnostics.cases:
            actual_points = tuple(
                (point.parent_scale, point.amplitude) for point in case.points
            )
            if actual_points != expected_points:
                raise ValueError("diagnostic point controls must match the request")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {"request": self.request, "diagnostics": self.diagnostics}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {"request", "diagnostics"}:
            raise ValueError("band-equivalence calculation-result fields do not match")
        request = values["request"]
        diagnostics = values["diagnostics"]
        if not isinstance(request, Mapping) or not isinstance(diagnostics, Mapping):
            raise TypeError("calculation-result values must decode to mappings")
        return cls(
            request=BandEquivalenceHoppingLocalityRequest.from_dict(request),
            diagnostics=BandEquivalenceHoppingLocalityDiagnostics.from_dict(
                diagnostics
            ),
        )


class BandEquivalenceHoppingLocalityAnalysisRecorder:
    """Project one bound scientific analysis into its retained record graph."""

    __slots__ = ("_analysis",)

    def __init__(self, analysis: BandEquivalenceHoppingLocalityAnalysis) -> None:
        if not isinstance(analysis, BandEquivalenceHoppingLocalityAnalysis):
            raise TypeError("analysis must be BandEquivalenceHoppingLocalityAnalysis")
        self._analysis = analysis

    @property
    def analysis(self) -> BandEquivalenceHoppingLocalityAnalysis:
        """Return the immutable scientific analysis bound to this recorder."""
        return self._analysis

    def result(self) -> BandEquivalenceHoppingLocalityCalculationResult:
        """Return the retained projection without rerunning the analyzer."""
        analysis = self._analysis
        request = analysis.request
        return BandEquivalenceHoppingLocalityCalculationResult(
            request=request,
            diagnostics=BandEquivalenceHoppingLocalityDiagnostics(
                family=request.family,
                status=analysis.status,
                construction_size=request.construction_size,
                evaluation_size=request.evaluation_size,
                cases=tuple(
                    CaseDiagnostic.from_analysis(case) for case in analysis.cases
                ),
            ),
        )


__all__ = [
    "BandEquivalenceHoppingLocalityAnalysisRecorder",
    "BandEquivalenceHoppingLocalityCalculationResult",
]
