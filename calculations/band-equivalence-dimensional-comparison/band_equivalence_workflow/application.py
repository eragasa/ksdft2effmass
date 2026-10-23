"""Application actions for canonical band-equivalence/locality artifacts."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    calculation as analysis_calculation,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    definitions as analysis_definitions,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.records import (
    BandEquivalenceLocalityDiagnostics,
    BandEquivalenceLocalityVerificationDiagnostics,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.refinement import (
    BandEquivalenceLocalityRefinementAnalyzer,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.refinement_records import (
    BandEquivalenceLocalityRefinementAssessment,
)

from .serialization import (
    BandEquivalenceLocalityRefinementSerializer,
    BandEquivalenceLocalityRequestSerializer,
    BandEquivalenceLocalityResultSerializer,
    BandEquivalenceLocalityVerificationSerializer,
    CanonicalJsonDocument,
)


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityResult:
    """Bind scientific diagnostics to their complete canonical request and result."""

    analysis_request: analysis_definitions.BandEquivalenceLocalityRequest
    diagnostics: BandEquivalenceLocalityDiagnostics
    request_document: CanonicalJsonDocument
    document: CanonicalJsonDocument

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not analysis_definitions.BandEquivalenceLocalityRequest
        ):
            raise TypeError("analysis_request must be a BandEquivalenceLocalityRequest")
        if type(self.diagnostics) is not BandEquivalenceLocalityDiagnostics:
            raise TypeError("diagnostics must be BandEquivalenceLocalityDiagnostics")
        if type(self.request_document) is not CanonicalJsonDocument:
            raise TypeError("request_document must be CanonicalJsonDocument")
        if type(self.document) is not CanonicalJsonDocument:
            raise TypeError("document must be CanonicalJsonDocument")
        expected_request = BandEquivalenceLocalityRequestSerializer().execute(
            self.analysis_request
        )
        if self.request_document != expected_request:
            raise ValueError("request_document does not encode the analysis request")
        expected_diagnostics = (
            analysis_calculation.BandEquivalenceLocalityCalculator().execute(
                self.analysis_request
            )
        )
        if self.diagnostics != expected_diagnostics:
            raise ValueError("diagnostics do not belong to the analysis request")
        expected = BandEquivalenceLocalityResultSerializer().execute(
            self.diagnostics,
            self.request_document,
        )
        if self.document != expected:
            raise ValueError("document does not encode the supplied diagnostics")


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityVerificationRequest:
    """Bind one canonical analysis request to the result being verified."""

    analysis_request: analysis_definitions.BandEquivalenceLocalityRequest
    result: BandEquivalenceLocalityResult

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not analysis_definitions.BandEquivalenceLocalityRequest
        ):
            raise TypeError("analysis_request must be a BandEquivalenceLocalityRequest")
        if type(self.result) is not BandEquivalenceLocalityResult:
            raise TypeError("result must be a BandEquivalenceLocalityResult")
        if self.result.analysis_request != self.analysis_request:
            raise ValueError("result does not belong to the supplied analysis request")
        expected_request = BandEquivalenceLocalityRequestSerializer().execute(
            self.analysis_request
        )
        if self.result.request_document != expected_request:
            raise ValueError("result does not belong to the supplied analysis request")


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityVerificationResult:
    """Bind verification diagnostics to both complete canonical input artifacts."""

    verification_request: BandEquivalenceLocalityVerificationRequest
    diagnostics: BandEquivalenceLocalityVerificationDiagnostics
    input_document: CanonicalJsonDocument
    result_document: CanonicalJsonDocument
    document: CanonicalJsonDocument

    def __post_init__(self) -> None:
        if (
            type(self.verification_request)
            is not BandEquivalenceLocalityVerificationRequest
        ):
            raise TypeError(
                "verification_request must be a "
                "BandEquivalenceLocalityVerificationRequest"
            )
        if type(self.diagnostics) is not BandEquivalenceLocalityVerificationDiagnostics:
            raise TypeError(
                "diagnostics must be BandEquivalenceLocalityVerificationDiagnostics"
            )
        if type(self.input_document) is not CanonicalJsonDocument:
            raise TypeError("input_document must be CanonicalJsonDocument")
        if type(self.result_document) is not CanonicalJsonDocument:
            raise TypeError("result_document must be CanonicalJsonDocument")
        if type(self.document) is not CanonicalJsonDocument:
            raise TypeError("document must be CanonicalJsonDocument")
        source_result = self.verification_request.result
        if self.input_document != source_result.request_document:
            raise ValueError("input_document does not belong to verification_request")
        if self.result_document != source_result.document:
            raise ValueError("result_document does not belong to verification_request")
        verifier = analysis_calculation.BandEquivalenceLocalityVerifier()
        expected_diagnostics = verifier.execute(
            self.verification_request.analysis_request,
            source_result.diagnostics,
        )
        if self.diagnostics != expected_diagnostics:
            raise ValueError("diagnostics do not belong to verification_request")
        expected = BandEquivalenceLocalityVerificationSerializer().execute(
            self.diagnostics,
            self.input_document,
            self.result_document,
        )
        if self.document != expected:
            raise ValueError("document does not encode the supplied verification")


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityRefinementRequest:
    """Supply the ordered canonical analysis results compared by refinement."""

    results: tuple[BandEquivalenceLocalityResult, ...]

    def __post_init__(self) -> None:
        if type(self.results) is not tuple or len(self.results) < 3:
            raise ValueError("results must contain at least three analysis results")
        if any(
            type(result) is not BandEquivalenceLocalityResult for result in self.results
        ):
            raise TypeError("results must contain BandEquivalenceLocalityResult values")


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityRefinementResult:
    """Bind a refinement assessment to its ordered canonical source results."""

    refinement_request: BandEquivalenceLocalityRefinementRequest
    assessment: BandEquivalenceLocalityRefinementAssessment
    source_result_documents: tuple[CanonicalJsonDocument, ...]
    document: CanonicalJsonDocument

    def __post_init__(self) -> None:
        if (
            type(self.refinement_request)
            is not BandEquivalenceLocalityRefinementRequest
        ):
            raise TypeError(
                "refinement_request must be a BandEquivalenceLocalityRefinementRequest"
            )
        if type(self.assessment) is not BandEquivalenceLocalityRefinementAssessment:
            raise TypeError(
                "assessment must be BandEquivalenceLocalityRefinementAssessment"
            )
        if type(self.source_result_documents) is not tuple or any(
            type(document) is not CanonicalJsonDocument
            for document in self.source_result_documents
        ):
            raise TypeError(
                "source_result_documents must contain CanonicalJsonDocument values"
            )
        if type(self.document) is not CanonicalJsonDocument:
            raise TypeError("document must be CanonicalJsonDocument")
        expected_sources = tuple(
            result.document for result in self.refinement_request.results
        )
        if self.source_result_documents != expected_sources:
            raise ValueError(
                "source_result_documents do not belong to refinement_request"
            )
        expected_assessment = BandEquivalenceLocalityRefinementAnalyzer().execute(
            tuple(result.diagnostics for result in self.refinement_request.results)
        )
        if self.assessment != expected_assessment:
            raise ValueError("assessment does not belong to refinement_request")
        expected = BandEquivalenceLocalityRefinementSerializer().execute(
            self.assessment,
            self.source_result_documents,
        )
        if self.document != expected:
            raise ValueError("document does not encode the supplied refinement")


class BandEquivalenceLocalityResultConstructor:
    """Construct one canonical result artifact from one analysis request."""

    __slots__ = ("_calculator", "_request_serializer", "_result_serializer")

    def __init__(self) -> None:
        self._calculator = analysis_calculation.BandEquivalenceLocalityCalculator()
        self._request_serializer = BandEquivalenceLocalityRequestSerializer()
        self._result_serializer = BandEquivalenceLocalityResultSerializer()

    def execute(
        self, request: analysis_definitions.BandEquivalenceLocalityRequest
    ) -> BandEquivalenceLocalityResult:
        if type(request) is not analysis_definitions.BandEquivalenceLocalityRequest:
            raise TypeError("request must be a BandEquivalenceLocalityRequest")
        request_document = self._request_serializer.execute(request)
        diagnostics = self._calculator.execute(request)
        return BandEquivalenceLocalityResult(
            analysis_request=request,
            diagnostics=diagnostics,
            request_document=request_document,
            document=self._result_serializer.execute(diagnostics, request_document),
        )


class BandEquivalenceLocalityResultVerifier:
    """Verify one result and construct its canonical verification artifact."""

    __slots__ = ("_serializer", "_verifier")

    def __init__(self) -> None:
        self._verifier = analysis_calculation.BandEquivalenceLocalityVerifier()
        self._serializer = BandEquivalenceLocalityVerificationSerializer()

    def execute(
        self,
        request: BandEquivalenceLocalityVerificationRequest,
    ) -> BandEquivalenceLocalityVerificationResult:
        if type(request) is not BandEquivalenceLocalityVerificationRequest:
            raise TypeError(
                "request must be a BandEquivalenceLocalityVerificationRequest"
            )
        diagnostics = self._verifier.execute(
            request.analysis_request,
            request.result.diagnostics,
        )
        return BandEquivalenceLocalityVerificationResult(
            verification_request=request,
            diagnostics=diagnostics,
            input_document=request.result.request_document,
            result_document=request.result.document,
            document=self._serializer.execute(
                diagnostics,
                request.result.request_document,
                request.result.document,
            ),
        )


class BandEquivalenceLocalityRefinementAssessor:
    """Assess ordered results and construct their canonical refinement artifact."""

    __slots__ = ("_analyzer", "_serializer")

    def __init__(self) -> None:
        self._analyzer = BandEquivalenceLocalityRefinementAnalyzer()
        self._serializer = BandEquivalenceLocalityRefinementSerializer()

    def execute(
        self,
        request: BandEquivalenceLocalityRefinementRequest,
    ) -> BandEquivalenceLocalityRefinementResult:
        if type(request) is not BandEquivalenceLocalityRefinementRequest:
            raise TypeError(
                "request must be a BandEquivalenceLocalityRefinementRequest"
            )
        source_documents = tuple(result.document for result in request.results)
        assessment = self._analyzer.execute(
            tuple(result.diagnostics for result in request.results)
        )
        return BandEquivalenceLocalityRefinementResult(
            refinement_request=request,
            assessment=assessment,
            source_result_documents=source_documents,
            document=self._serializer.execute(assessment, source_documents),
        )


__all__ = [
    "BandEquivalenceLocalityRefinementAssessor",
    "BandEquivalenceLocalityRefinementRequest",
    "BandEquivalenceLocalityRefinementResult",
    "BandEquivalenceLocalityResult",
    "BandEquivalenceLocalityResultConstructor",
    "BandEquivalenceLocalityResultVerifier",
    "BandEquivalenceLocalityVerificationRequest",
    "BandEquivalenceLocalityVerificationResult",
]
