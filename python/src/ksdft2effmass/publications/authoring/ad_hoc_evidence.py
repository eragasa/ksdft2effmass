"""Author-supplied publisher-abstract evidence for bounded drafting."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import ClassVar

from .evidence import EvidenceRetrievalProjection, RetrievedEvidenceExcerpt
from .statuses import (
    CitationKeyStatus,
    EvidenceProvenanceStatus,
    EvidenceRetrievalOutcomeProjection,
    EvidenceSourceScope,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class AuthorSuppliedPublisherAbstractEvidence:
    """Represent one author-supplied publisher abstract and its exact provenance.

    This record represents only metadata and abstract text displayed on one of the
    explicitly authorized APS abstract pages. It never represents full-paper review,
    rights determination, citation acceptance, scientific validation, or human
    acceptance.
    """

    ALLOWED_SOURCE_URLS: ClassVar[frozenset[str]] = frozenset(
        {
            "https://journals.aps.org/pr/abstract/10.1103/PhysRev.97.869",
            "https://journals.aps.org/pr/abstract/10.1103/PhysRev.98.915",
            "https://journals.aps.org/prb/abstract/10.1103/PhysRevB.8.2697",
        }
    )
    MAX_ID_CHARACTERS: ClassVar[int] = 512
    MAX_TITLE_CHARACTERS: ClassVar[int] = 1_000
    MAX_ABSTRACT_CHARACTERS: ClassVar[int] = 20_000
    CITEKEY_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"[A-Za-z0-9][A-Za-z0-9:._+\-]{0,255}\Z"
    )

    bibliographic_work_id: str
    source_url: str
    doi: str
    title: str
    authors: tuple[str, ...]
    publication_date: str
    abstract_text: str
    source_document_sha256: str
    citation_key_status: CitationKeyStatus
    canonical_citekey: str | None
    proposed_citekey: str | None
    provenance_status: EvidenceProvenanceStatus = (
        EvidenceProvenanceStatus.AUTHOR_SUPPLIED_AD_HOC
    )
    source_scope: EvidenceSourceScope = EvidenceSourceScope.PUBLISHER_ABSTRACT
    warning_codes: tuple[str, ...] = ()
    evidence_id: str = field(init=False)

    def __post_init__(self) -> None:
        """Validate abstract-only provenance, citation status, and content identity."""
        for name, value, maximum in (
            (
                "bibliographic_work_id",
                self.bibliographic_work_id,
                self.MAX_ID_CHARACTERS,
            ),
            ("doi", self.doi, self.MAX_ID_CHARACTERS),
            ("title", self.title, self.MAX_TITLE_CHARACTERS),
            ("publication_date", self.publication_date, 128),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value or value != value.strip() or len(value) > maximum:
                raise ValueError(f"{name} must be nonempty, trimmed, and bounded")
        if type(self.source_url) is not str:
            raise TypeError("source_url must be a built-in str")
        if self.source_url not in self.ALLOWED_SOURCE_URLS:
            raise ValueError("source_url must be an explicitly authorized APS abstract")
        if not self.source_url.endswith(self.doi):
            raise ValueError("source_url and DOI must identify the same abstract page")
        if type(self.authors) is not tuple:
            raise TypeError("authors must be a built-in tuple")
        if not 1 <= len(self.authors) <= 32:
            raise ValueError("authors must contain 1 to 32 values")
        for author in self.authors:
            if type(author) is not str:
                raise TypeError("authors must contain built-in strings")
            if not author or author != author.strip() or len(author) > 512:
                raise ValueError("authors must contain nonempty trimmed bounded values")
        if type(self.abstract_text) is not str:
            raise TypeError("abstract_text must be a built-in str")
        if (
            not self.abstract_text
            or self.abstract_text != self.abstract_text.strip()
            or len(self.abstract_text) > self.MAX_ABSTRACT_CHARACTERS
        ):
            raise ValueError("abstract_text must be nonempty, trimmed, and bounded")
        if type(self.source_document_sha256) is not str:
            raise TypeError("source_document_sha256 must be a built-in str")
        if re.fullmatch(r"[0-9a-f]{64}", self.source_document_sha256) is None:
            raise ValueError("source_document_sha256 must be lowercase SHA-256")
        if (
            self.provenance_status
            is not EvidenceProvenanceStatus.AUTHOR_SUPPLIED_AD_HOC
        ):
            raise ValueError("provenance_status must be AUTHOR_SUPPLIED_AD_HOC")
        if self.source_scope is not EvidenceSourceScope.PUBLISHER_ABSTRACT:
            raise ValueError("source_scope must be PUBLISHER_ABSTRACT")
        if type(self.citation_key_status) is not CitationKeyStatus:
            raise TypeError("citation_key_status must be CitationKeyStatus")
        self._validate_citekeys()
        if type(self.warning_codes) is not tuple:
            raise TypeError("warning_codes must be a built-in tuple")
        for warning in self.warning_codes:
            if type(warning) is not str:
                raise TypeError("warning_codes must contain built-in strings")
            if not warning or warning != warning.strip() or len(warning) > 128:
                raise ValueError("warning codes must be nonempty, trimmed, and bounded")
        if self.warning_codes != tuple(sorted(set(self.warning_codes))):
            raise ValueError("warning_codes must be unique and lexically sorted")
        object.__setattr__(
            self,
            "evidence_id",
            self.identity_for(
                bibliographic_work_id=self.bibliographic_work_id,
                source_url=self.source_url,
                doi=self.doi,
                title=self.title,
                authors=self.authors,
                publication_date=self.publication_date,
                abstract_text=self.abstract_text,
                source_document_sha256=self.source_document_sha256,
                citation_key_status=self.citation_key_status,
                canonical_citekey=self.canonical_citekey,
                proposed_citekey=self.proposed_citekey,
                provenance_status=self.provenance_status,
                source_scope=self.source_scope,
                warning_codes=self.warning_codes,
            ),
        )

    def _validate_citekeys(self) -> None:
        """Enforce accepted-key and proposed-key separation."""
        for name, value in (
            ("canonical_citekey", self.canonical_citekey),
            ("proposed_citekey", self.proposed_citekey),
        ):
            if value is not None:
                if type(value) is not str:
                    raise TypeError(f"{name} must be a built-in str or None")
                if self.CITEKEY_PATTERN.fullmatch(value) is None:
                    raise ValueError(f"{name} must use the bounded citekey grammar")
        if self.citation_key_status is CitationKeyStatus.ACCEPTED_ACTIVE_CANONICAL:
            if self.canonical_citekey is None or self.proposed_citekey is not None:
                raise ValueError("accepted status requires only a canonical citekey")
        elif (
            self.citation_key_status
            is CitationKeyStatus.CANDIDATE_PROPOSED_NONCANONICAL
        ):
            if self.canonical_citekey is not None or self.proposed_citekey is None:
                raise ValueError("candidate status requires only a proposed citekey")
        elif self.canonical_citekey is not None:
            raise ValueError("non-active citation status cannot carry a canonical key")

    @staticmethod
    def identity_for(
        *,
        bibliographic_work_id: str,
        source_url: str,
        doi: str,
        title: str,
        authors: tuple[str, ...],
        publication_date: str,
        abstract_text: str,
        source_document_sha256: str,
        citation_key_status: CitationKeyStatus,
        canonical_citekey: str | None,
        proposed_citekey: str | None,
        provenance_status: EvidenceProvenanceStatus,
        source_scope: EvidenceSourceScope,
        warning_codes: tuple[str, ...],
    ) -> str:
        """Return the identity of exact abstract-only author-supplied evidence."""
        payload: dict[str, str | tuple[str, ...] | None] = {
            "abstract_text": abstract_text,
            "authors": authors,
            "bibliographic_work_id": bibliographic_work_id,
            "canonical_citekey": canonical_citekey,
            "citation_key_status": citation_key_status.value,
            "doi": doi,
            "proposed_citekey": proposed_citekey,
            "provenance_status": provenance_status.value,
            "publication_date": publication_date,
            "source_document_sha256": source_document_sha256,
            "source_scope": source_scope.value,
            "source_url": source_url,
            "title": title,
            "type": "ksdft2effmass.publications.author-supplied-publisher-abstract.v1",
            "warning_codes": warning_codes,
        }
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
        return f"author-supplied-evidence:sha256:{hashlib.sha256(encoded).hexdigest()}"


@dataclass(frozen=True, slots=True, kw_only=True)
class AdHocEvidenceRetrievalProjection:
    """Represent a bounded projection of author-supplied publisher abstracts."""

    evidence: tuple[AuthorSuppliedPublisherAbstractEvidence, ...]
    warning_codes: tuple[str, ...] = ()
    outcome: EvidenceRetrievalOutcomeProjection = (
        EvidenceRetrievalOutcomeProjection.EVIDENCE_AVAILABLE
    )
    projection_id: str = field(init=False)

    def __post_init__(self) -> None:
        """Validate ad-hoc evidence cohesion and assign the projection identity."""
        if type(self.evidence) is not tuple:
            raise TypeError("evidence must be a built-in tuple")
        if not 1 <= len(self.evidence) <= 32:
            raise ValueError("evidence must contain 1 to 32 abstracts")
        if any(
            type(item) is not AuthorSuppliedPublisherAbstractEvidence
            for item in self.evidence
        ):
            raise TypeError("evidence must contain publisher-abstract evidence")
        evidence_ids = tuple(item.evidence_id for item in self.evidence)
        work_ids = tuple(item.bibliographic_work_id for item in self.evidence)
        if len(set(evidence_ids)) != len(evidence_ids):
            raise ValueError("ad-hoc evidence IDs must be unique")
        if len(set(work_ids)) != len(work_ids):
            raise ValueError("ad-hoc bibliographic work IDs must be unique")
        if type(self.warning_codes) is not tuple:
            raise TypeError("warning_codes must be a built-in tuple")
        for warning in self.warning_codes:
            if type(warning) is not str:
                raise TypeError("warning_codes must contain built-in strings")
            if not warning or warning != warning.strip() or len(warning) > 128:
                raise ValueError("warning codes must be nonempty, trimmed, and bounded")
        if self.warning_codes != tuple(sorted(set(self.warning_codes))):
            raise ValueError("warning_codes must be unique and lexically sorted")
        if self.outcome is not EvidenceRetrievalOutcomeProjection.EVIDENCE_AVAILABLE:
            raise ValueError("ad-hoc projection outcome must be EVIDENCE_AVAILABLE")
        object.__setattr__(
            self,
            "projection_id",
            self.identity_for(evidence=self.evidence, warning_codes=self.warning_codes),
        )

    @staticmethod
    def identity_for(
        *,
        evidence: tuple[AuthorSuppliedPublisherAbstractEvidence, ...],
        warning_codes: tuple[str, ...],
    ) -> str:
        """Return the identity of one ordered ad-hoc evidence projection."""
        payload: dict[str, tuple[str, ...] | str] = {
            "evidence_ids": tuple(item.evidence_id for item in evidence),
            "type": "ksdft2effmass.publications.ad-hoc-evidence-projection.v1",
            "warning_codes": warning_codes,
        }
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
        return (
            f"ad-hoc-evidence-projection:sha256:{hashlib.sha256(encoded).hexdigest()}"
        )


type AuthoringEvidenceExcerpt = (
    RetrievedEvidenceExcerpt | AuthorSuppliedPublisherAbstractEvidence
)
type AuthoringEvidenceRetrievalProjection = (
    EvidenceRetrievalProjection | AdHocEvidenceRetrievalProjection
)
