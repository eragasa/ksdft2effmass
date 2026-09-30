"""Immutable projections of selected and retrieved external evidence."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import ClassVar

from .statuses import (
    CitationKeyStatus,
    EvidenceRetrievalOutcomeProjection,
    TranscriptEvidenceMappingBasis,
    TranscriptEvidenceSelectionOutcomeProjection,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class TranscriptEvidenceSelectionReference:
    """Retain one exact ingestion selection outcome used by retrieval.

    Parameters
    ----------
    selection_result_id
        Exact Project Koios Ingestion transcript-selection result identity.
    outcome
        Closed projected selection outcome.
    warning_codes
        Sorted warning codes requiring inspection for the warning outcome.
    reference_id
        Deterministic init-false identity binding the projected result state.

    Raises
    ------
    TypeError
        If fields have incorrect semantic types.
    ValueError
        If identities, ordering, or outcome-dependent warnings are inconsistent.
    """

    MAX_ID_CHARACTERS: ClassVar[int] = 512
    MAX_WARNINGS: ClassVar[int] = 64

    selection_result_id: str
    outcome: TranscriptEvidenceSelectionOutcomeProjection
    warning_codes: tuple[str, ...]
    reference_id: str = field(init=False)

    def __post_init__(self) -> None:
        """Validate exact selection state and assign its deterministic identity."""
        if type(self.selection_result_id) is not str:
            raise TypeError("selection_result_id must be a built-in str")
        if (
            not self.selection_result_id
            or self.selection_result_id != self.selection_result_id.strip()
            or len(self.selection_result_id) > self.MAX_ID_CHARACTERS
        ):
            raise ValueError(
                "selection_result_id must be nonempty, trimmed, and bounded"
            )
        if type(self.outcome) is not TranscriptEvidenceSelectionOutcomeProjection:
            raise TypeError(
                "outcome must be TranscriptEvidenceSelectionOutcomeProjection"
            )
        if type(self.warning_codes) is not tuple:
            raise TypeError("warning_codes must be a built-in tuple")
        if len(self.warning_codes) > self.MAX_WARNINGS:
            raise ValueError("warning_codes exceeds the fixed selection bound")
        for warning_code in self.warning_codes:
            if type(warning_code) is not str:
                raise TypeError("warning_codes must contain built-in strings")
            if (
                not warning_code
                or warning_code != warning_code.strip()
                or len(warning_code) > 128
            ):
                raise ValueError("warning_codes must be nonempty, trimmed, and bounded")
        if self.warning_codes != tuple(sorted(set(self.warning_codes))):
            raise ValueError("warning_codes must be unique and lexically sorted")
        requires_warning = (
            self.outcome
            is TranscriptEvidenceSelectionOutcomeProjection.WARNING_INSPECTION_REQUIRED
        )
        if requires_warning != bool(self.warning_codes):
            raise ValueError(
                "warning codes are present exactly for warning-inspection outcome"
            )
        object.__setattr__(
            self,
            "reference_id",
            self.identity_for(
                selection_result_id=self.selection_result_id,
                outcome=self.outcome,
                warning_codes=self.warning_codes,
            ),
        )

    @staticmethod
    def identity_for(
        *,
        selection_result_id: str,
        outcome: TranscriptEvidenceSelectionOutcomeProjection,
        warning_codes: tuple[str, ...],
    ) -> str:
        """Return the deterministic identity of projected ingestion selection state."""
        payload: dict[str, str | tuple[str, ...]] = {
            "outcome": outcome.value,
            "selection_result_id": selection_result_id,
            "type": (
                "ksdft2effmass.publications.transcript-evidence-selection-reference"
            ),
            "warning_codes": warning_codes,
        }
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
        digest = hashlib.sha256(encoded).hexdigest()
        return f"transcript-evidence-selection-reference:sha256:{digest}"


@dataclass(frozen=True, slots=True, kw_only=True)
class RetrievedEvidenceExcerpt:
    """Represent one source-linked excerpt projected from external retrieval.

    Parameters
    ----------
    evidence_id
        Stable evidence-item identity from the external retrieval result.
    bibliographic_work_id
        Stable identity of the represented bibliographic work.
    citation_key_status
        Exact projected citation-identity status.
    canonical_citekey
        Canonical citekey only for active accepted status; otherwise ``None``.
    citation_identity_projection_item_id
        Exact Project Koios References projection-item identity.
    transcript_selection_result_id, transcript_result_id
        Exact ingestion selection and clean-transcript result identities.
    transcript_selected_page_evidence_id, transcript_selected_block_evidence_id
        Exact Project Koios Ingestion selected-evidence identities.
    page_id, block_id, block_record_id
        Exact selected page and block identities.
    search_ranked_evidence_item_id, search_rank
        Exact Project Koios Search ranked-record identity and one-based rank.
    indexed_clean_text, indexed_clean_text_sha256
        Search-index text and matching lowercase SHA-256 digest.
    retained_raw_text, retained_raw_text_sha256
        Exact quotation/inspection text and matching lowercase SHA-256 digest.
    mapping_basis
        Exact-pair relationship between clean indexed and retained raw block text.
    source_span_ids
        Ordered, nonempty source-span identities supporting the excerpt.
    warning_codes
        Ordered extraction or transformation warnings requiring inspection.
    excerpt_id
        Deterministic init-false identity binding every represented field.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If bounds, uniqueness, or citation-status invariants fail.
    """

    MAX_ID_CHARACTERS: ClassVar[int] = 512
    MAX_CITATION_KEY_CHARACTERS: ClassVar[int] = 256
    MAX_INDEXED_TEXT_CHARACTERS: ClassVar[int] = 8_000
    MAX_RETAINED_TEXT_CHARACTERS: ClassVar[int] = 16_000
    MAX_SOURCE_SPANS: ClassVar[int] = 32
    MAX_WARNINGS: ClassVar[int] = 32
    CITATION_KEY_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"[A-Za-z0-9][A-Za-z0-9:._+\-]{0,255}\Z"
    )
    SHA256_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"[0-9a-f]{64}\Z")

    evidence_id: str
    bibliographic_work_id: str
    citation_key_status: CitationKeyStatus
    canonical_citekey: str | None
    citation_identity_projection_item_id: str
    transcript_selection_result_id: str
    transcript_result_id: str
    transcript_selected_page_evidence_id: str
    transcript_selected_block_evidence_id: str
    page_id: str
    block_id: str
    block_record_id: str
    search_ranked_evidence_item_id: str
    search_rank: int
    indexed_clean_text: str
    indexed_clean_text_sha256: str
    retained_raw_text: str
    retained_raw_text_sha256: str
    mapping_basis: TranscriptEvidenceMappingBasis
    source_span_ids: tuple[str, ...]
    warning_codes: tuple[str, ...]
    excerpt_id: str = field(init=False)

    def __post_init__(self) -> None:
        """Validate projected evidence and assign its deterministic identity."""
        for name, value in (
            ("evidence_id", self.evidence_id),
            ("bibliographic_work_id", self.bibliographic_work_id),
            (
                "citation_identity_projection_item_id",
                self.citation_identity_projection_item_id,
            ),
            (
                "transcript_selection_result_id",
                self.transcript_selection_result_id,
            ),
            ("transcript_result_id", self.transcript_result_id),
            (
                "transcript_selected_page_evidence_id",
                self.transcript_selected_page_evidence_id,
            ),
            (
                "transcript_selected_block_evidence_id",
                self.transcript_selected_block_evidence_id,
            ),
            ("page_id", self.page_id),
            ("block_id", self.block_id),
            ("block_record_id", self.block_record_id),
            ("search_ranked_evidence_item_id", self.search_ranked_evidence_item_id),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if (
                not value
                or value != value.strip()
                or len(value) > self.MAX_ID_CHARACTERS
            ):
                raise ValueError(f"{name} must be nonempty, trimmed, and bounded")
        if type(self.search_rank) is not int:
            raise TypeError("search_rank must be a built-in int excluding bool")
        if self.search_rank < 1:
            raise ValueError("search_rank must be positive")
        if type(self.citation_key_status) is not CitationKeyStatus:
            raise TypeError("citation_key_status must be CitationKeyStatus")
        if self.citation_key_status is CitationKeyStatus.ACCEPTED_ACTIVE_CANONICAL:
            if type(self.canonical_citekey) is not str:
                raise TypeError("active accepted evidence requires canonical_citekey")
            if self.CITATION_KEY_PATTERN.fullmatch(self.canonical_citekey) is None:
                raise ValueError(
                    "canonical_citekey must use the bounded citekey grammar"
                )
        elif self.canonical_citekey is not None:
            raise ValueError(
                "only active accepted evidence may carry canonical_citekey"
            )

        for name, text, digest, maximum in (
            (
                "indexed_clean_text",
                self.indexed_clean_text,
                self.indexed_clean_text_sha256,
                self.MAX_INDEXED_TEXT_CHARACTERS,
            ),
            (
                "retained_raw_text",
                self.retained_raw_text,
                self.retained_raw_text_sha256,
                self.MAX_RETAINED_TEXT_CHARACTERS,
            ),
        ):
            if type(text) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not text.strip() or len(text) > maximum:
                raise ValueError(f"{name} must contain bounded non-whitespace text")
            if type(digest) is not str:
                raise TypeError(f"{name}_sha256 must be a built-in str")
            if self.SHA256_PATTERN.fullmatch(digest) is None:
                raise ValueError(f"{name}_sha256 must be lowercase SHA-256")
            expected_digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
            if digest != expected_digest:
                raise ValueError(f"{name}_sha256 must match exact text")
        if type(self.mapping_basis) is not TranscriptEvidenceMappingBasis:
            raise TypeError("mapping_basis must be TranscriptEvidenceMappingBasis")
        if (
            self.mapping_basis
            is not TranscriptEvidenceMappingBasis.CLEAN_TRANSCRIPT_BLOCK_EXACT_PAIR
        ):
            raise ValueError("mapping_basis must retain the exact clean/raw block pair")

        if type(self.source_span_ids) is not tuple:
            raise TypeError("source_span_ids must be a built-in tuple")
        if not 1 <= len(self.source_span_ids) <= self.MAX_SOURCE_SPANS:
            raise ValueError("source_span_ids must contain between 1 and 32 values")
        for source_span_id in self.source_span_ids:
            if type(source_span_id) is not str:
                raise TypeError("source_span_ids must contain built-in strings")
            if (
                not source_span_id
                or source_span_id != source_span_id.strip()
                or len(source_span_id) > self.MAX_ID_CHARACTERS
            ):
                raise ValueError(
                    "source_span_ids must be nonempty, trimmed, and bounded"
                )
        if len(set(self.source_span_ids)) != len(self.source_span_ids):
            raise ValueError("source_span_ids must be unique")

        if type(self.warning_codes) is not tuple:
            raise TypeError("warning_codes must be a built-in tuple")
        if len(self.warning_codes) > self.MAX_WARNINGS:
            raise ValueError("warning_codes exceeds the fixed bound")
        for warning_code in self.warning_codes:
            if type(warning_code) is not str:
                raise TypeError("warning_codes must contain built-in strings")
            if (
                not warning_code
                or warning_code != warning_code.strip()
                or len(warning_code) > 128
            ):
                raise ValueError("warning_codes must be nonempty, trimmed, and bounded")
        if len(set(self.warning_codes)) != len(self.warning_codes):
            raise ValueError("warning_codes must be unique")

        object.__setattr__(
            self,
            "excerpt_id",
            self.identity_for(
                evidence_id=self.evidence_id,
                bibliographic_work_id=self.bibliographic_work_id,
                citation_key_status=self.citation_key_status,
                canonical_citekey=self.canonical_citekey,
                citation_identity_projection_item_id=(
                    self.citation_identity_projection_item_id
                ),
                transcript_selection_result_id=(self.transcript_selection_result_id),
                transcript_result_id=self.transcript_result_id,
                transcript_selected_page_evidence_id=(
                    self.transcript_selected_page_evidence_id
                ),
                transcript_selected_block_evidence_id=(
                    self.transcript_selected_block_evidence_id
                ),
                page_id=self.page_id,
                block_id=self.block_id,
                block_record_id=self.block_record_id,
                search_ranked_evidence_item_id=(self.search_ranked_evidence_item_id),
                search_rank=self.search_rank,
                indexed_clean_text=self.indexed_clean_text,
                indexed_clean_text_sha256=self.indexed_clean_text_sha256,
                retained_raw_text=self.retained_raw_text,
                retained_raw_text_sha256=self.retained_raw_text_sha256,
                mapping_basis=self.mapping_basis,
                source_span_ids=self.source_span_ids,
                warning_codes=self.warning_codes,
            ),
        )

    @staticmethod
    def identity_for(
        *,
        evidence_id: str,
        bibliographic_work_id: str,
        citation_key_status: CitationKeyStatus,
        canonical_citekey: str | None,
        citation_identity_projection_item_id: str,
        transcript_selection_result_id: str,
        transcript_result_id: str,
        transcript_selected_page_evidence_id: str,
        transcript_selected_block_evidence_id: str,
        page_id: str,
        block_id: str,
        block_record_id: str,
        search_ranked_evidence_item_id: str,
        search_rank: int,
        indexed_clean_text: str,
        indexed_clean_text_sha256: str,
        retained_raw_text: str,
        retained_raw_text_sha256: str,
        mapping_basis: TranscriptEvidenceMappingBasis,
        source_span_ids: tuple[str, ...],
        warning_codes: tuple[str, ...],
    ) -> str:
        """Return the deterministic identity of an exact retrieval projection."""
        payload: dict[str, str | int | tuple[str, ...] | None] = {
            "bibliographic_work_id": bibliographic_work_id,
            "canonical_citekey": canonical_citekey,
            "citation_identity_projection_item_id": (
                citation_identity_projection_item_id
            ),
            "citation_key_status": citation_key_status.value,
            "evidence_id": evidence_id,
            "transcript_selection_result_id": transcript_selection_result_id,
            "transcript_result_id": transcript_result_id,
            "transcript_selected_page_evidence_id": (
                transcript_selected_page_evidence_id
            ),
            "transcript_selected_block_evidence_id": (
                transcript_selected_block_evidence_id
            ),
            "page_id": page_id,
            "block_id": block_id,
            "block_record_id": block_record_id,
            "search_ranked_evidence_item_id": search_ranked_evidence_item_id,
            "search_rank": search_rank,
            "indexed_clean_text": indexed_clean_text,
            "indexed_clean_text_sha256": indexed_clean_text_sha256,
            "retained_raw_text": retained_raw_text,
            "retained_raw_text_sha256": retained_raw_text_sha256,
            "mapping_basis": mapping_basis.value,
            "source_span_ids": source_span_ids,
            "type": "ksdft2effmass.publications.retrieved-evidence-excerpt",
            "warning_codes": warning_codes,
        }
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
        return (
            f"retrieved-evidence-excerpt:sha256:{hashlib.sha256(encoded).hexdigest()}"
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class EvidenceRetrievalProjection:
    """Represent the minimal external retrieval result needed for authoring.

    Parameters
    ----------
    retrieval_result_id
        Stable identity of the complete external retrieval result.
    citation_identity_projection_id
        Exact source References projection identity used to resolve citation status.
    citation_identity_projection_result_id
        Exact Project Koios References projection-result identity.
    transcript_selections
        Exact projected ingestion selection results underlying retrieved excerpts.
    outcome
        Projected closed retrieval outcome.
    evidence
        Ranked excerpts in the order supplied by external retrieval.
    warning_codes
        Ordered result-level warnings requiring inspection.
    projection_id
        Deterministic init-false identity binding result identity and excerpts.

    Raises
    ------
    TypeError
        If values have the wrong semantic types.
    ValueError
        If outcome, evidence presence, bounds, or uniqueness are inconsistent.

    Notes
    -----
    This record neither imports Project Koios Search nor reproduces retrieval or
    ranking.  ``ProjectKoiosSearchAdapter`` maps one exact Search result into this
    projection without reranking or rewriting excerpts.
    """

    MAX_EVIDENCE: ClassVar[int] = 32
    MAX_ID_CHARACTERS: ClassVar[int] = 512
    MAX_WARNINGS: ClassVar[int] = 64

    retrieval_result_id: str
    citation_identity_projection_id: str
    citation_identity_projection_result_id: str
    transcript_selections: tuple[TranscriptEvidenceSelectionReference, ...]
    outcome: EvidenceRetrievalOutcomeProjection
    evidence: tuple[RetrievedEvidenceExcerpt, ...]
    warning_codes: tuple[str, ...]
    projection_id: str = field(init=False)

    def __post_init__(self) -> None:
        """Validate the projected result and assign its deterministic identity."""
        for name, value in (
            ("retrieval_result_id", self.retrieval_result_id),
            (
                "citation_identity_projection_id",
                self.citation_identity_projection_id,
            ),
            (
                "citation_identity_projection_result_id",
                self.citation_identity_projection_result_id,
            ),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if (
                not value
                or value != value.strip()
                or len(value) > self.MAX_ID_CHARACTERS
            ):
                raise ValueError(f"{name} must be nonempty, trimmed, and bounded")
        if type(self.transcript_selections) is not tuple:
            raise TypeError("transcript_selections must be a built-in tuple")
        if not 1 <= len(self.transcript_selections) <= self.MAX_EVIDENCE:
            raise ValueError("transcript_selections must contain 1 to 32 values")
        if any(
            type(selection) is not TranscriptEvidenceSelectionReference
            for selection in self.transcript_selections
        ):
            raise TypeError("transcript_selections must contain selection references")
        selection_result_ids = tuple(
            selection.selection_result_id for selection in self.transcript_selections
        )
        if len(set(selection_result_ids)) != len(selection_result_ids):
            raise ValueError("transcript selection result IDs must be unique")

        if type(self.outcome) is not EvidenceRetrievalOutcomeProjection:
            raise TypeError("outcome must be EvidenceRetrievalOutcomeProjection")
        if type(self.evidence) is not tuple:
            raise TypeError("evidence must be a built-in tuple")
        if len(self.evidence) > self.MAX_EVIDENCE:
            raise ValueError("evidence exceeds the fixed projection bound")
        if any(
            type(excerpt) is not RetrievedEvidenceExcerpt for excerpt in self.evidence
        ):
            raise TypeError("evidence must contain RetrievedEvidenceExcerpt values")
        evidence_ids = tuple(excerpt.evidence_id for excerpt in self.evidence)
        if len(set(evidence_ids)) != len(evidence_ids):
            raise ValueError("projected evidence IDs must be unique")
        ranked_ids = tuple(
            excerpt.search_ranked_evidence_item_id for excerpt in self.evidence
        )
        if len(set(ranked_ids)) != len(ranked_ids):
            raise ValueError("projected ranked evidence IDs must be unique")
        if tuple(excerpt.search_rank for excerpt in self.evidence) != tuple(
            range(1, len(self.evidence) + 1)
        ):
            raise ValueError("projected evidence must preserve contiguous Search ranks")
        available = (
            self.outcome is EvidenceRetrievalOutcomeProjection.EVIDENCE_AVAILABLE
        )
        if available != bool(self.evidence):
            raise ValueError("evidence is present exactly when retrieval is available")
        if available and any(
            selection.outcome
            is not TranscriptEvidenceSelectionOutcomeProjection.EVIDENCE_AVAILABLE
            for selection in self.transcript_selections
        ):
            raise ValueError(
                "available retrieval requires available transcript selections"
            )
        if any(
            excerpt.transcript_selection_result_id not in selection_result_ids
            for excerpt in self.evidence
        ):
            raise ValueError(
                "evidence must reference a retained transcript selection result"
            )

        if type(self.warning_codes) is not tuple:
            raise TypeError("warning_codes must be a built-in tuple")
        if len(self.warning_codes) > self.MAX_WARNINGS:
            raise ValueError("warning_codes exceeds the fixed projection bound")
        for warning_code in self.warning_codes:
            if type(warning_code) is not str:
                raise TypeError("warning_codes must contain built-in strings")
            if (
                not warning_code
                or warning_code != warning_code.strip()
                or len(warning_code) > 128
            ):
                raise ValueError("warning_codes must be nonempty, trimmed, and bounded")
        if len(set(self.warning_codes)) != len(self.warning_codes):
            raise ValueError("warning_codes must be unique")

        object.__setattr__(
            self,
            "projection_id",
            self.identity_for(
                retrieval_result_id=self.retrieval_result_id,
                citation_identity_projection_id=(self.citation_identity_projection_id),
                citation_identity_projection_result_id=(
                    self.citation_identity_projection_result_id
                ),
                transcript_selections=self.transcript_selections,
                outcome=self.outcome,
                evidence=self.evidence,
                warning_codes=self.warning_codes,
            ),
        )

    @staticmethod
    def identity_for(
        *,
        retrieval_result_id: str,
        citation_identity_projection_id: str,
        citation_identity_projection_result_id: str,
        transcript_selections: tuple[TranscriptEvidenceSelectionReference, ...],
        outcome: EvidenceRetrievalOutcomeProjection,
        evidence: tuple[RetrievedEvidenceExcerpt, ...],
        warning_codes: tuple[str, ...],
    ) -> str:
        """Return the deterministic identity for an exact retrieval projection."""
        payload: dict[str, str | tuple[str, ...]] = {
            "evidence_excerpt_ids": tuple(excerpt.excerpt_id for excerpt in evidence),
            "citation_identity_projection_id": citation_identity_projection_id,
            "citation_identity_projection_result_id": (
                citation_identity_projection_result_id
            ),
            "outcome": outcome.value,
            "retrieval_result_id": retrieval_result_id,
            "transcript_selection_reference_ids": tuple(
                selection.reference_id for selection in transcript_selections
            ),
            "type": "ksdft2effmass.publications.evidence-retrieval-projection",
            "warning_codes": warning_codes,
        }
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
        digest = hashlib.sha256(encoded).hexdigest()
        return f"evidence-retrieval-projection:sha256:{digest}"
