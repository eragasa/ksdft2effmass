"""Ad-hoc author-supplied publisher-abstract evidence adaptation."""

from __future__ import annotations

from projectkoios.references.citation_identity import CitationIdentityProjectionResult

from ..ad_hoc_evidence import (
    AdHocEvidenceRetrievalProjection,
    AuthorSuppliedPublisherAbstractEvidence,
)
from .references import ProjectKoiosReferencesAdapter


class AuthorSuppliedPublisherAbstractAdapter:
    """Bind authorized APS abstracts to exact References owner-result lineage.

    The adapter is separate from strict Search and Ingestion owner-result adapters.
    It accepts only evidence whose embedded citation identity equals the projection
    derived from the supplied exact References result. Candidate labels remain local
    and noncanonical. It performs no fetching, full-text access, citation resolution,
    rights determination, or scientific acceptance.
    """

    def project(
        self,
        evidence: tuple[AuthorSuppliedPublisherAbstractEvidence, ...],
        references_result: CitationIdentityProjectionResult,
        /,
        *,
        warning_codes: tuple[str, ...] = (),
    ) -> AdHocEvidenceRetrievalProjection:
        """Return one canonical projection bound to exact owner-result items."""
        if type(evidence) is not tuple:
            raise TypeError("evidence must be a built-in tuple")
        if type(references_result) is not CitationIdentityProjectionResult:
            raise TypeError(
                "references_result must be CitationIdentityProjectionResult"
            )
        references_adapter = ProjectKoiosReferencesAdapter()
        for item in evidence:
            if type(item) is not AuthorSuppliedPublisherAbstractEvidence:
                raise TypeError("evidence must contain publisher-abstract evidence")
            projected = references_adapter.project(
                references_result, item.bibliographic_work_id
            )
            if item.citation_identity != projected:
                raise ValueError(
                    "abstract citation identity differs from exact References lineage"
                )
        canonical_evidence = tuple(
            sorted(
                evidence,
                key=lambda item: (item.bibliographic_work_id, item.evidence_id),
            )
        )
        return AdHocEvidenceRetrievalProjection(
            evidence=canonical_evidence,
            warning_codes=warning_codes,
        )
