"""Bounded evidence-grounded manuscript proposal contracts and composition.

The package represents immutable read-only target and evidence projections, an
injected local-inference boundary, and one stateless proposal composer.  It performs
no retrieval, ranking, filesystem, shell, database, browser, network, manuscript,
bibliography, or publication action.
"""

from .adapters import (
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
from .proposal import ManuscriptAuthoringResult, ManuscriptProposal, ProposedCitation
from .statuses import (
    CitationKeyStatus,
    EvidenceRetrievalOutcomeProjection,
    HumanAcceptanceStatus,
    ManuscriptAuthoringIssue,
    ManuscriptAuthoringOutcome,
    TranscriptEvidenceMappingBasis,
    TranscriptEvidenceSelectionOutcomeProjection,
)
from .target import ManuscriptTargetContext

__all__ = (
    "CitationKeyStatus",
    "EvidenceGroundedManuscriptAuthor",
    "EvidenceRetrievalOutcomeProjection",
    "EvidenceRetrievalProjection",
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
    "ProjectedCitationIdentity",
    "ProjectKoiosIngestionAdapter",
    "ProjectKoiosReferencesAdapter",
    "ProjectKoiosSearchAdapter",
    "ProposedCitation",
    "RetrievedEvidenceExcerpt",
    "TranscriptEvidenceMappingBasis",
    "TranscriptEvidenceSelectionOutcomeProjection",
    "TranscriptEvidenceSelectionReference",
)
