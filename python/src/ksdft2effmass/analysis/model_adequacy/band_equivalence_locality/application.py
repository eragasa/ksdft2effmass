"""Public application entry point for band-equivalence/locality analysis."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .calculation import (
    BandEquivalenceLocalityCalculator,
    BandEquivalenceLocalityVerifier,
)
from .definitions import BandEquivalenceLocalityRequest
from .records import (
    BandEquivalenceLocalityResult,
    BandEquivalenceLocalityVerificationResult,
)
from .refinement import BandEquivalenceLocalityRefinementAnalyzer
from .refinement_records import BandEquivalenceLocalityRefinementResult
from .serialization import (
    band_equivalence_locality_request_document,
    canonical_json_bytes,
)


def _analysis_request_sha256(request: BandEquivalenceLocalityRequest) -> str:
    encoded = canonical_json_bytes(band_equivalence_locality_request_document(request))
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityVerificationRequest:
    """Bind one definition to the calculated result that must be verified."""

    analysis_request: BandEquivalenceLocalityRequest
    result: BandEquivalenceLocalityResult

    def __post_init__(self) -> None:
        if type(self.analysis_request) is not BandEquivalenceLocalityRequest:
            raise TypeError("analysis_request must be BandEquivalenceLocalityRequest")
        if type(self.result) is not BandEquivalenceLocalityResult:
            raise TypeError("result must be BandEquivalenceLocalityResult")
        if self.result.analysis_request_sha256 != _analysis_request_sha256(
            self.analysis_request
        ):
            raise ValueError("result does not belong to the analysis request")
        if self.result.family is not self.analysis_request.family:
            raise ValueError("result family must match the analysis request")
        if (
            self.result.construction_size != self.analysis_request.construction_size
            or self.result.evaluation_size != self.analysis_request.evaluation_size
        ):
            raise ValueError("result mesh sizes must match the analysis request")


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityRefinementRequest:
    """Bind ordered mesh results to their exact source-document hashes."""

    results: tuple[BandEquivalenceLocalityResult, ...]

    def __post_init__(self) -> None:
        if type(self.results) is not tuple or len(self.results) < 3:
            raise ValueError("results must contain at least three mesh levels")
        if any(
            type(result) is not BandEquivalenceLocalityResult for result in self.results
        ):
            raise TypeError("results must contain BandEquivalenceLocalityResult values")


class BandEquivalenceLocalityAnalysis:
    """Expose calculation, verification, and refinement as one stable entry point."""

    __slots__ = ()

    def calculate(
        self, request: BandEquivalenceLocalityRequest
    ) -> BandEquivalenceLocalityResult:
        """Calculate one bounded, non-evidentiary analysis result."""
        return BandEquivalenceLocalityCalculator().execute(
            request,
            _analysis_request_sha256(request),
        )

    def verify(
        self, request: BandEquivalenceLocalityVerificationRequest
    ) -> BandEquivalenceLocalityVerificationResult:
        """Independently verify one correlated definition and result."""
        if type(request) is not BandEquivalenceLocalityVerificationRequest:
            raise TypeError(
                "request must be BandEquivalenceLocalityVerificationRequest"
            )
        return BandEquivalenceLocalityVerifier().execute(
            request.analysis_request, request.result
        )

    def assess_refinement(
        self, request: BandEquivalenceLocalityRefinementRequest
    ) -> BandEquivalenceLocalityRefinementResult:
        """Assess an ordered refinement ladder without inventing tolerances."""
        if type(request) is not BandEquivalenceLocalityRefinementRequest:
            raise TypeError("request must be BandEquivalenceLocalityRefinementRequest")
        return BandEquivalenceLocalityRefinementAnalyzer().execute(request.results)


__all__ = [
    "BandEquivalenceLocalityAnalysis",
    "BandEquivalenceLocalityRefinementRequest",
    "BandEquivalenceLocalityVerificationRequest",
]
