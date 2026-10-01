"""Immutable citation, proposal, and closed authoring-result records."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import ClassVar

from .contracts import ManuscriptAuthoringRequest
from .statuses import (
    HumanAcceptanceStatus,
    ManuscriptAuthoringIssue,
    ManuscriptAuthoringOutcome,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class ProposedCitation:
    """Represent one structured citation proposed from identified evidence.

    Parameters
    ----------
    citation_key
        Accepted bibliography key to cite.
    evidence_ids
        Lexically sorted, unique evidence identities supporting this citation.
    citation_id
        Deterministic init-false identity of the key and evidence set.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If key grammar, bounds, uniqueness, or canonical ordering fail.
    """

    MAX_EVIDENCE_IDS: ClassVar[int] = 32
    MAX_ID_CHARACTERS: ClassVar[int] = 512
    CITATION_KEY_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"[A-Za-z0-9][A-Za-z0-9:._+\-]{0,255}\Z"
    )

    citation_key: str
    evidence_ids: tuple[str, ...]
    citation_id: str = field(init=False)

    def __post_init__(self) -> None:
        """Validate the structured citation and assign its identity."""
        if type(self.citation_key) is not str:
            raise TypeError("citation_key must be a built-in str")
        if self.CITATION_KEY_PATTERN.fullmatch(self.citation_key) is None:
            raise ValueError("citation_key must use the bounded citation-key grammar")
        if type(self.evidence_ids) is not tuple:
            raise TypeError("evidence_ids must be a built-in tuple")
        if not 1 <= len(self.evidence_ids) <= self.MAX_EVIDENCE_IDS:
            raise ValueError("evidence_ids must contain 1 to 32 values")
        for evidence_id in self.evidence_ids:
            if type(evidence_id) is not str:
                raise TypeError("evidence_ids must contain built-in strings")
            if (
                not evidence_id
                or evidence_id != evidence_id.strip()
                or len(evidence_id) > self.MAX_ID_CHARACTERS
            ):
                raise ValueError("evidence_ids must be nonempty, trimmed, and bounded")
        if self.evidence_ids != tuple(sorted(set(self.evidence_ids))):
            raise ValueError("evidence_ids must be unique and lexically sorted")
        object.__setattr__(
            self,
            "citation_id",
            self.identity_for(
                citation_key=self.citation_key, evidence_ids=self.evidence_ids
            ),
        )

    @staticmethod
    def identity_for(*, citation_key: str, evidence_ids: tuple[str, ...]) -> str:
        """Return the deterministic identity of one structured citation."""
        payload: dict[str, str | tuple[str, ...]] = {
            "citation_key": citation_key,
            "evidence_ids": evidence_ids,
            "type": "ksdft2effmass.publications.proposed-citation",
        }
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
        return f"proposed-citation:sha256:{hashlib.sha256(encoded).hexdigest()}"


@dataclass(frozen=True, slots=True, kw_only=True)
class ProposedEvidenceMarker:
    """Represent one explicit draft marker for evidence lacking a canonical citekey."""

    MAX_ID_CHARACTERS: ClassVar[int] = 512

    evidence_id: str
    marker_text: str = field(init=False)
    marker_id: str = field(init=False)

    def __post_init__(self) -> None:
        """Validate the evidence identity and assign exact marker identities."""
        if type(self.evidence_id) is not str:
            raise TypeError("evidence_id must be a built-in str")
        if (
            not self.evidence_id
            or self.evidence_id != self.evidence_id.strip()
            or len(self.evidence_id) > self.MAX_ID_CHARACTERS
        ):
            raise ValueError("evidence_id must be nonempty, trimmed, and bounded")
        marker_text = f"[[EVIDENCE:{self.evidence_id}]]"
        object.__setattr__(self, "marker_text", marker_text)
        encoded = json.dumps(
            {
                "evidence_id": self.evidence_id,
                "marker_text": marker_text,
                "type": "ksdft2effmass.publications.proposed-evidence-marker",
            },
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        object.__setattr__(
            self,
            "marker_id",
            f"proposed-evidence-marker:sha256:{hashlib.sha256(encoded).hexdigest()}",
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class ManuscriptProposal:
    """Represent an immutable replacement proposal awaiting human inspection.

    Parameters
    ----------
    request_id
        Exact originating authoring-request identity.
    target_id, revision_id, span_id
        Exact target correlation copied from the request.
    replacement_text
        Proposed text for the selected span only.
    citations
        Structured citations admitted by the composer.
    evidence_ids
        Lexically sorted evidence identities used by the proposal.
    evidence_markers
        Lexically ordered explicit draft markers for evidence without accepted keys.
    human_acceptance_status
        Explicitly :attr:`HumanAcceptanceStatus.NOT_EVALUATED`.
    proposal_id
        Deterministic init-false identity binding all proposal content.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If fields are empty, unordered, duplicated, or claim evaluated acceptance.

    Notes
    -----
    This object is neither a patch nor authorization to write a manuscript or
    bibliography.
    """

    MAX_ID_CHARACTERS: ClassVar[int] = 512

    request_id: str
    target_id: str
    revision_id: str
    span_id: str
    replacement_text: str
    citations: tuple[ProposedCitation, ...]
    evidence_ids: tuple[str, ...]
    human_acceptance_status: HumanAcceptanceStatus
    evidence_markers: tuple[ProposedEvidenceMarker, ...] = ()
    proposal_id: str = field(init=False)

    def __post_init__(self) -> None:
        """Validate proposal structure and assign its deterministic identity."""
        for name, value in (
            ("request_id", self.request_id),
            ("target_id", self.target_id),
            ("revision_id", self.revision_id),
            ("span_id", self.span_id),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if (
                not value
                or value != value.strip()
                or len(value) > self.MAX_ID_CHARACTERS
            ):
                raise ValueError(f"{name} must be nonempty, trimmed, and bounded")
        if type(self.replacement_text) is not str:
            raise TypeError("replacement_text must be a built-in str")
        if (
            not self.replacement_text.strip()
            or len(self.replacement_text)
            > ManuscriptAuthoringRequest.MAX_OUTPUT_CHARACTERS
        ):
            raise ValueError(
                "replacement_text must contain bounded non-whitespace text"
            )
        if type(self.citations) is not tuple:
            raise TypeError("citations must be a built-in tuple")
        if any(type(citation) is not ProposedCitation for citation in self.citations):
            raise TypeError("citations must contain ProposedCitation values")
        if type(self.evidence_markers) is not tuple:
            raise TypeError("evidence_markers must be a built-in tuple")
        if any(
            type(marker) is not ProposedEvidenceMarker
            for marker in self.evidence_markers
        ):
            raise TypeError(
                "evidence_markers must contain ProposedEvidenceMarker values"
            )
        marker_evidence_ids = tuple(
            marker.evidence_id for marker in self.evidence_markers
        )
        if marker_evidence_ids != tuple(sorted(set(marker_evidence_ids))):
            raise ValueError("evidence markers must be unique and lexically sorted")
        if any(
            self.replacement_text.count(marker.marker_text) != 1
            for marker in self.evidence_markers
        ):
            raise ValueError("each evidence marker must occur exactly once in text")
        if type(self.evidence_ids) is not tuple:
            raise TypeError("evidence_ids must be a built-in tuple")
        if not self.evidence_ids or self.evidence_ids != tuple(
            sorted(set(self.evidence_ids))
        ):
            raise ValueError(
                "evidence_ids must be nonempty, unique, and lexically sorted"
            )
        represented_evidence_ids = {
            evidence_id
            for citation in self.citations
            for evidence_id in citation.evidence_ids
        } | set(marker_evidence_ids)
        if represented_evidence_ids != set(self.evidence_ids):
            raise ValueError("citations and markers must represent every evidence ID")
        if self.human_acceptance_status is not HumanAcceptanceStatus.NOT_EVALUATED:
            raise ValueError("human acceptance must remain not_evaluated")
        object.__setattr__(
            self,
            "proposal_id",
            self.identity_for(
                request_id=self.request_id,
                target_id=self.target_id,
                revision_id=self.revision_id,
                span_id=self.span_id,
                replacement_text=self.replacement_text,
                citations=self.citations,
                evidence_ids=self.evidence_ids,
                evidence_markers=self.evidence_markers,
                human_acceptance_status=self.human_acceptance_status,
            ),
        )

    @staticmethod
    def identity_for(
        *,
        request_id: str,
        target_id: str,
        revision_id: str,
        span_id: str,
        replacement_text: str,
        citations: tuple[ProposedCitation, ...],
        evidence_ids: tuple[str, ...],
        evidence_markers: tuple[ProposedEvidenceMarker, ...],
        human_acceptance_status: HumanAcceptanceStatus,
    ) -> str:
        """Return the deterministic identity of an exact proposal."""
        payload: dict[str, str | tuple[str, ...]] = {
            "citation_ids": tuple(citation.citation_id for citation in citations),
            "evidence_ids": evidence_ids,
            "evidence_marker_ids": tuple(
                marker.marker_id for marker in evidence_markers
            ),
            "human_acceptance_status": human_acceptance_status.value,
            "replacement_text": replacement_text,
            "request_id": request_id,
            "revision_id": revision_id,
            "span_id": span_id,
            "target_id": target_id,
            "type": "ksdft2effmass.publications.manuscript-proposal",
        }
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
        return f"manuscript-proposal:sha256:{hashlib.sha256(encoded).hexdigest()}"


@dataclass(frozen=True, slots=True, kw_only=True)
class ManuscriptAuthoringResult:
    """Represent the closed result of one authoring request.

    Parameters
    ----------
    request
        Exact immutable request.
    author_implementation_id
        Versioned identity of the composing ActionObject implementation.
    outcome
        Closed composition outcome.
    issues
        Unique issue members in :class:`ManuscriptAuthoringIssue` declaration order.
    inference_response_id
        Response identity when inference ran, otherwise ``None``.
    proposal
        Proposal for a fully keyed or citation-gap-ready outcome only.
    human_acceptance_status
        Explicitly :attr:`HumanAcceptanceStatus.NOT_EVALUATED` for every outcome.
    result_id
        Deterministic init-false identity binding the complete result.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If issue ordering or outcome-dependent fields are inconsistent.
    """

    MAX_ID_CHARACTERS: ClassVar[int] = 512

    request: ManuscriptAuthoringRequest
    author_implementation_id: str
    outcome: ManuscriptAuthoringOutcome
    issues: tuple[ManuscriptAuthoringIssue, ...]
    inference_response_id: str | None
    proposal: ManuscriptProposal | None
    human_acceptance_status: HumanAcceptanceStatus
    result_id: str = field(init=False)

    def __post_init__(self) -> None:
        """Validate the closed outcome and assign its deterministic identity."""
        if type(self.request) is not ManuscriptAuthoringRequest:
            raise TypeError("request must be ManuscriptAuthoringRequest")
        if type(self.author_implementation_id) is not str:
            raise TypeError("author_implementation_id must be a built-in str")
        if (
            not self.author_implementation_id
            or self.author_implementation_id != self.author_implementation_id.strip()
            or len(self.author_implementation_id) > self.MAX_ID_CHARACTERS
        ):
            raise ValueError(
                "author_implementation_id must be nonempty, trimmed, and bounded"
            )
        if type(self.outcome) is not ManuscriptAuthoringOutcome:
            raise TypeError("outcome must be ManuscriptAuthoringOutcome")
        if type(self.issues) is not tuple:
            raise TypeError("issues must be a built-in tuple")
        if any(type(issue) is not ManuscriptAuthoringIssue for issue in self.issues):
            raise TypeError("issues must contain ManuscriptAuthoringIssue values")
        canonical = tuple(
            issue for issue in ManuscriptAuthoringIssue if issue in self.issues
        )
        if self.issues != canonical or len(set(self.issues)) != len(self.issues):
            raise ValueError("issues must be unique and in declaration order")
        if self.inference_response_id is not None:
            if type(self.inference_response_id) is not str:
                raise TypeError("inference_response_id must be a built-in str or None")
            if (
                not self.inference_response_id
                or self.inference_response_id != self.inference_response_id.strip()
                or len(self.inference_response_id) > self.MAX_ID_CHARACTERS
            ):
                raise ValueError(
                    "inference_response_id must be nonempty, trimmed, and bounded"
                )
        if self.human_acceptance_status is not HumanAcceptanceStatus.NOT_EVALUATED:
            raise ValueError("human acceptance must remain not_evaluated")

        ready_outcomes = (
            ManuscriptAuthoringOutcome.PROPOSAL_READY,
            ManuscriptAuthoringOutcome.PROPOSAL_READY_WITH_CITATION_GAPS,
        )
        if self.outcome in ready_outcomes:
            if type(self.proposal) is not ManuscriptProposal:
                raise TypeError("ready result requires ManuscriptProposal")
            if self.proposal.request_id != self.request.request_id:
                raise ValueError(
                    "proposal request identity must match the result request"
                )
            if self.inference_response_id is None:
                raise ValueError("ready result requires an inference response ID")
            if self.outcome is ManuscriptAuthoringOutcome.PROPOSAL_READY:
                if self.issues or self.proposal.evidence_markers:
                    raise ValueError(
                        "fully keyed proposal cannot contain gaps or issues"
                    )
            elif (
                self.issues
                != (ManuscriptAuthoringIssue.CITATION_GAPS_REQUIRE_INSPECTION,)
                or not self.proposal.evidence_markers
            ):
                raise ValueError("citation-gap-ready result requires gap inspection")
        else:
            if not self.issues:
                raise ValueError("failed-closed result requires at least one issue")
            if self.proposal is not None:
                raise ValueError("failed-closed result must not contain a proposal")

        object.__setattr__(
            self,
            "result_id",
            self.identity_for(
                request=self.request,
                author_implementation_id=self.author_implementation_id,
                outcome=self.outcome,
                issues=self.issues,
                inference_response_id=self.inference_response_id,
                proposal=self.proposal,
                human_acceptance_status=self.human_acceptance_status,
            ),
        )

    @staticmethod
    def identity_for(
        *,
        request: ManuscriptAuthoringRequest,
        author_implementation_id: str,
        outcome: ManuscriptAuthoringOutcome,
        issues: tuple[ManuscriptAuthoringIssue, ...],
        inference_response_id: str | None,
        proposal: ManuscriptProposal | None,
        human_acceptance_status: HumanAcceptanceStatus,
    ) -> str:
        """Return the deterministic identity of one closed authoring result."""
        payload: dict[str, str | tuple[str, ...] | None] = {
            "author_implementation_id": author_implementation_id,
            "human_acceptance_status": human_acceptance_status.value,
            "inference_response_id": inference_response_id,
            "issue_codes": tuple(issue.value for issue in issues),
            "outcome": outcome.value,
            "proposal_id": None if proposal is None else proposal.proposal_id,
            "request_id": request.request_id,
            "type": "ksdft2effmass.publications.manuscript-authoring-result",
        }
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
        return (
            f"manuscript-authoring-result:sha256:{hashlib.sha256(encoded).hexdigest()}"
        )
