"""Bounded evidence-grounded manuscript proposal contracts and composition.

The package represents immutable read-only target and evidence projections, an
injected local-inference boundary, and one stateless proposal composer. The package
performs no retrieval, ranking, shell, database, browser, remote-network, manuscript,
bibliography, or publication action. Its concrete inference adapter contacts only a
fixed-model Ollama service on literal IPv4 loopback, and its bounded retention owner
writes only mode-0600 ignored-cache response observability artifacts.
"""

from .ad_hoc_evidence import (
    AdHocEvidenceRetrievalProjection,
    AuthorSuppliedPublisherAbstractEvidence,
)
from .adapters import (
    AuthorSuppliedPublisherAbstractAdapter,
    OllamaLoopbackManuscriptInferenceAdapter,
    OllamaRawResponseArtifact,
    OllamaResponseRetention,
    ProjectedCitationIdentity,
    ProjectKoiosIngestionAdapter,
    ProjectKoiosReferencesAdapter,
    ProjectKoiosSearchAdapter,
)
from .author import EvidenceGroundedManuscriptAuthor
from .contracts import ManuscriptAuthoringRequest
from .evidence import (
    EvidenceRetrievalProjection,
    RetrievedEvidenceExcerpt,
    TranscriptEvidenceSelectionReference,
)
from .inference import (
    LocalManuscriptInferencePort,
    ManuscriptInferenceRequest,
    ManuscriptInferenceResponse,
)
from .local_run import RetainedLocalManuscriptAuthoringRun
from .proposal import (
    ManuscriptAuthoringResult,
    ManuscriptProposal,
    ProposedCitation,
    ProposedEvidenceMarker,
)
from .statuses import (
    CitationKeyStatus,
    EvidenceProvenanceStatus,
    EvidenceRetrievalOutcomeProjection,
    EvidenceSourceScope,
    HumanAcceptanceStatus,
    ManuscriptAuthoringIssue,
    ManuscriptAuthoringOutcome,
    TranscriptEvidenceMappingBasis,
    TranscriptEvidenceSelectionOutcomeProjection,
)
from .target import ManuscriptTargetContext

__all__ = (
    "AdHocEvidenceRetrievalProjection",
    "AuthorSuppliedPublisherAbstractAdapter",
    "AuthorSuppliedPublisherAbstractEvidence",
    "CitationKeyStatus",
    "EvidenceGroundedManuscriptAuthor",
    "EvidenceProvenanceStatus",
    "EvidenceRetrievalOutcomeProjection",
    "EvidenceRetrievalProjection",
    "EvidenceSourceScope",
    "HumanAcceptanceStatus",
    "LocalManuscriptInferencePort",
    "ManuscriptAuthoringIssue",
    "ManuscriptAuthoringOutcome",
    "ManuscriptAuthoringRequest",
    "ManuscriptAuthoringResult",
    "ManuscriptInferenceRequest",
    "ManuscriptInferenceResponse",
    "ManuscriptProposal",
    "ManuscriptTargetContext",
    "OllamaLoopbackManuscriptInferenceAdapter",
    "OllamaRawResponseArtifact",
    "OllamaResponseRetention",
    "ProjectedCitationIdentity",
    "ProjectKoiosIngestionAdapter",
    "ProjectKoiosReferencesAdapter",
    "ProjectKoiosSearchAdapter",
    "ProposedCitation",
    "ProposedEvidenceMarker",
    "RetainedLocalManuscriptAuthoringRun",
    "RetrievedEvidenceExcerpt",
    "TranscriptEvidenceMappingBasis",
    "TranscriptEvidenceSelectionOutcomeProjection",
    "TranscriptEvidenceSelectionReference",
)
