"""Ad-hoc author-supplied publisher-abstract evidence adaptation."""

from __future__ import annotations

from typing import ClassVar

from ..ad_hoc_evidence import (
    AdHocEvidenceRetrievalProjection,
    AuthorSuppliedPublisherAbstractEvidence,
)
from ..statuses import CitationKeyStatus


class AuthorSuppliedPublisherAbstractAdapter:
    """Project authorized APS abstracts without promoting prospective citekeys.

    The adapter is separate from strict Project Koios owner-result adapters. It accepts
    only the three explicitly authorized APS abstract URLs and enforces the target
    snapshot's citation disposition for each work. It performs no fetching, full-text
    access, citation resolution, rights determination, or scientific acceptance.
    """

    EXPECTED_CITATION_STATES: ClassVar[
        tuple[tuple[str, CitationKeyStatus, str], ...]
    ] = (
        (
            "https://journals.aps.org/pr/abstract/10.1103/PhysRev.97.869",
            CitationKeyStatus.ACCEPTED_ACTIVE_CANONICAL,
            "luttingerKohn1955",
        ),
        (
            "https://journals.aps.org/pr/abstract/10.1103/PhysRev.98.915",
            CitationKeyStatus.CANDIDATE_PROPOSED_NONCANONICAL,
            "kohnLuttinger1955donor",
        ),
        (
            "https://journals.aps.org/prb/abstract/10.1103/PhysRevB.8.2697",
            CitationKeyStatus.CANDIDATE_PROPOSED_NONCANONICAL,
            "baldereschiLipari1973",
        ),
    )

    def project(
        self,
        evidence: tuple[AuthorSuppliedPublisherAbstractEvidence, ...],
        /,
        *,
        warning_codes: tuple[str, ...] = (),
    ) -> AdHocEvidenceRetrievalProjection:
        """Return one bounded ad-hoc projection with exact citation dispositions."""
        if type(evidence) is not tuple:
            raise TypeError("evidence must be a built-in tuple")
        expected_by_url = {
            url: (status, citekey)
            for url, status, citekey in self.EXPECTED_CITATION_STATES
        }
        for item in evidence:
            if type(item) is not AuthorSuppliedPublisherAbstractEvidence:
                raise TypeError("evidence must contain publisher-abstract evidence")
            status, citekey = expected_by_url[item.source_url]
            if item.citation_key_status is not status:
                raise ValueError(
                    "abstract citation status differs from target snapshot"
                )
            if status is CitationKeyStatus.ACCEPTED_ACTIVE_CANONICAL:
                if (
                    item.canonical_citekey != citekey
                    or item.proposed_citekey is not None
                ):
                    raise ValueError(
                        "accepted abstract must preserve its canonical key"
                    )
            elif item.canonical_citekey is not None or item.proposed_citekey != citekey:
                raise ValueError("prospective abstract key must remain noncanonical")
        return AdHocEvidenceRetrievalProjection(
            evidence=evidence,
            warning_codes=warning_codes,
        )
