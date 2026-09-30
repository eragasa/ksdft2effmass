"""Closed status vocabularies for bounded manuscript authoring."""

from __future__ import annotations

from enum import StrEnum


class CitationKeyStatus(StrEnum):
    """Represent the projected citation-identity status of one work.

    Values align structurally with the Project Koios References citation projection
    without importing that package.

    Attributes
    ----------
    ACCEPTED_ACTIVE_CANONICAL
        An active accepted reference has one canonical citekey.
    ACCEPTED_WITHOUT_ACTIVE_CITEKEY
        An accepted reference has no active citekey.
    CANDIDATE_PROPOSED_NONCANONICAL
        A candidate has only a proposed noncanonical key, never an accepted key.
    INACTIVE_SUPERSEDED
        An accepted reference is inactive and superseded.
    UNRESOLVED
        The requested bibliographic identity is unresolved.
    """

    ACCEPTED_ACTIVE_CANONICAL = "accepted-active-canonical"
    ACCEPTED_WITHOUT_ACTIVE_CITEKEY = "accepted-without-active-citekey"
    CANDIDATE_PROPOSED_NONCANONICAL = "candidate-proposed-noncanonical"
    INACTIVE_SUPERSEDED = "inactive-superseded"
    UNRESOLVED = "unresolved"


class HumanAcceptanceStatus(StrEnum):
    """Represent human or principal-investigator acceptance for this prototype.

    Attributes
    ----------
    NOT_EVALUATED
        No human or principal-investigator acceptance has been evaluated.

    Notes
    -----
    This first vertical deliberately exposes no accepted or rejected constructor state.
    A later owner-approved human-acceptance contract and review boundary must own
    any evaluated status.
    """

    NOT_EVALUATED = "not_evaluated"


class EvidenceRetrievalOutcomeProjection(StrEnum):
    """Represent the external retrieval outcome needed at composition time.

    Attributes
    ----------
    EVIDENCE_AVAILABLE
        The projection contains one or more ranked evidence excerpts.
    INSUFFICIENT_EVIDENCE
        Retrieval reported a mechanical evidence shortfall.
    INVALID_REQUEST
        Retrieval rejected its request.
    INFRASTRUCTURE_FAILURE
        Retrieval could not complete because of an infrastructure failure.
    """

    EVIDENCE_AVAILABLE = "EVIDENCE_AVAILABLE"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    INVALID_REQUEST = "INVALID_REQUEST"
    INFRASTRUCTURE_FAILURE = "INFRASTRUCTURE_FAILURE"


class TranscriptEvidenceSelectionOutcomeProjection(StrEnum):
    """Represent the closed ingestion evidence-selection outcome.

    Values align structurally with the Project Koios Ingestion transcript evidence
    selection boundary without importing that package.
    """

    INVALID_SELECTION = "INVALID_SELECTION"
    MISSING_BLOCK = "MISSING_BLOCK"
    TRANSCRIPT_NOT_COMPLETE = "TRANSCRIPT_NOT_COMPLETE"
    WARNING_INSPECTION_REQUIRED = "WARNING_INSPECTION_REQUIRED"
    EVIDENCE_AVAILABLE = "EVIDENCE_AVAILABLE"


class TranscriptEvidenceMappingBasis(StrEnum):
    """Identify the retained clean-to-raw transcript mapping basis.

    Attributes
    ----------
    CLEAN_TRANSCRIPT_BLOCK_EXACT_PAIR
        Indexed clean text and retained raw text come from one exact selected block.
    """

    CLEAN_TRANSCRIPT_BLOCK_EXACT_PAIR = "CLEAN_TRANSCRIPT_BLOCK_EXACT_PAIR"


class ManuscriptAuthoringOutcome(StrEnum):
    """Represent the closed outcome of bounded manuscript proposal composition.

    Attributes
    ----------
    PROPOSAL_READY
        A bounded proposal passed the structural authoring checks.
    INSUFFICIENT_EVIDENCE
        Evidence is absent or does not cover every required bibliographic work.
    INSPECTION_REQUIRED
        A warning, unresolved citation key, or citation inconsistency needs inspection.
    STALE_TARGET
        The caller's current revision differs from the requested target revision.
    OUTPUT_REJECTED
        Generated text or citation counts violate request bounds.
    EVIDENCE_MISMATCH
        Inference correlation or evidence identities do not match the request.
    """

    PROPOSAL_READY = "proposal_ready"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    INSPECTION_REQUIRED = "inspection_required"
    STALE_TARGET = "stale_target"
    OUTPUT_REJECTED = "output_rejected"
    EVIDENCE_MISMATCH = "evidence_mismatch"


class ManuscriptAuthoringIssue(StrEnum):
    """Identify deterministic reasons why composition failed closed.

    Members are declared in the canonical order used by
    :class:`ManuscriptAuthoringResult`.
    """

    RETRIEVAL_INSUFFICIENT = "retrieval_insufficient"
    RETRIEVAL_FAILED = "retrieval_failed"
    REQUIRED_WORK_MISSING = "required_work_missing"
    EVIDENCE_WARNING = "evidence_warning"
    CITATION_KEY_UNRESOLVED = "citation_key_unresolved"
    TARGET_REVISION_STALE = "target_revision_stale"
    INFERENCE_REQUEST_MISMATCH = "inference_request_mismatch"
    INFERENCE_WARNING = "inference_warning"
    OUTPUT_EMPTY = "output_empty"
    OUTPUT_TEXT_LIMIT_EXCEEDED = "output_text_limit_exceeded"
    OUTPUT_CITATION_LIMIT_EXCEEDED = "output_citation_limit_exceeded"
    EVIDENCE_ID_MISMATCH = "evidence_id_mismatch"
    CITATION_EVIDENCE_MISMATCH = "citation_evidence_mismatch"
    CITATION_KEY_MISMATCH = "citation_key_mismatch"
