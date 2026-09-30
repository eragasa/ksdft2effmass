"""Bounded evidence-grounded publication-authoring contracts.

The package exposes immutable in-memory records, one structural local-inference port,
and one stateless proposal composer.  It performs no retrieval, ranking, filesystem,
shell, database, browser, network, manuscript, bibliography, or publication action.
"""

from .authoring import (
    CitationKeyStatus,
    EvidenceGroundedManuscriptAuthor,
    EvidenceRetrievalOutcomeProjection,
    EvidenceRetrievalProjection,
    HumanAcceptanceStatus,
    LocalManuscriptInferencePort,
    ManuscriptAuthoringIssue,
    ManuscriptAuthoringOutcome,
    ManuscriptAuthoringRequest,
    ManuscriptAuthoringResult,
    ManuscriptInferenceRequest,
    ManuscriptInferenceResponse,
    ManuscriptProposal,
    ManuscriptTargetContext,
    ProposedCitation,
    RetrievedEvidenceExcerpt,
    TranscriptEvidenceMappingBasis,
    TranscriptEvidenceSelectionOutcomeProjection,
    TranscriptEvidenceSelectionReference,
)

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
    "ProposedCitation",
    "RetrievedEvidenceExcerpt",
    "TranscriptEvidenceMappingBasis",
    "TranscriptEvidenceSelectionOutcomeProjection",
    "TranscriptEvidenceSelectionReference",
)
