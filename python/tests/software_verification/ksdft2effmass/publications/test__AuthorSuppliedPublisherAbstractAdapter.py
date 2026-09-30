r"""Software verification of ``AuthorSuppliedPublisherAbstractAdapter``.

Evidence profile: routine

Bounded artifact scope: explicit APS publisher-abstract evidence adaptation.

Facet and represented meaning

The adapter preserves author-supplied ad-hoc provenance, abstract-only scope, and the
target snapshot's accepted-versus-prospective citekey states.

Intrinsic and cross-object scope

Immutable evidence records own exact source/content identities; the adapter owns
cross-record citation disposition, and the manuscript author owns warning admission and
marker-bearing proposal composition.

VVUQ and scientific exclusions

Synthetic abstract text verifies software behavior only. It does not establish
full-paper review, rights determination, citation correctness, scientific validation,
uncertainty quantification, publication readiness, or human acceptance.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

import pytest

import ksdft2effmass.publications as publications
from ksdft2effmass.publications import (
    AdHocEvidenceRetrievalProjection,
    AuthorSuppliedPublisherAbstractAdapter,
    AuthorSuppliedPublisherAbstractEvidence,
    CitationKeyStatus,
    EvidenceGroundedManuscriptAuthor,
    EvidenceProvenanceStatus,
    EvidenceSourceScope,
    HumanAcceptanceStatus,
    ManuscriptAuthoringIssue,
    ManuscriptAuthoringOutcome,
    ManuscriptAuthoringRequest,
    ManuscriptInferenceRequest,
    ManuscriptInferenceResponse,
    ManuscriptProposal,
    ManuscriptTargetContext,
    ProposedCitation,
    ProposedEvidenceMarker,
)
from ksdft2effmass.publications.authoring.adapters.ad_hoc import (
    AuthorSuppliedPublisherAbstractAdapter as DefiningAdapter,
)

pytestmark = pytest.mark.software_verification
SUT = AuthorSuppliedPublisherAbstractAdapter


class TestAuthorSuppliedPublisherAbstractAdapter:
    """Verify the explicit ad-hoc publisher-abstract path."""

    @dataclass(slots=True)
    class InferenceStub:
        """Return a marker-bearing draft without a model invocation."""

        accepted_id: str
        gap_ids: tuple[str, ...]
        calls: list[ManuscriptInferenceRequest]

        def infer(
            self, request: ManuscriptInferenceRequest, /
        ) -> ManuscriptInferenceResponse:
            """Return one response using all evidence IDs exactly once."""
            self.calls.append(request)
            markers = tuple(
                ProposedEvidenceMarker(evidence_id=evidence_id)
                for evidence_id in self.gap_ids
            )
            replacement = (
                "Synthetic abstract-bounded statement \\cite{luttingerKohn1955}. "
                + " ".join(marker.marker_text for marker in markers)
            )
            return ManuscriptInferenceResponse(
                inference_request_id=request.inference_request_id,
                inference_implementation_id="synthetic-ad-hoc-inference:v1",
                replacement_text=replacement,
                citations=(
                    ProposedCitation(
                        citation_key="luttingerKohn1955",
                        evidence_ids=(self.accepted_id,),
                    ),
                ),
                evidence_ids=request.allowed_evidence_ids,
                warning_codes=(),
                evidence_marker_ids=self.gap_ids,
            )

    @staticmethod
    def make_evidence(
        url: str,
        *,
        warning_codes: tuple[str, ...] = (),
    ) -> AuthorSuppliedPublisherAbstractEvidence:
        """Return one synthetic record with the authorized URL's exact key state."""
        states = {
            "https://journals.aps.org/pr/abstract/10.1103/PhysRev.97.869": (
                "10.1103/PhysRev.97.869",
                "doi:10.1103/PhysRev.97.869",
                "Synthetic representation abstract",
                CitationKeyStatus.ACCEPTED_ACTIVE_CANONICAL,
                "luttingerKohn1955",
                None,
            ),
            "https://journals.aps.org/pr/abstract/10.1103/PhysRev.98.915": (
                "10.1103/PhysRev.98.915",
                "doi:10.1103/PhysRev.98.915",
                "Synthetic donor abstract",
                CitationKeyStatus.CANDIDATE_PROPOSED_NONCANONICAL,
                None,
                "kohnLuttinger1955donor",
            ),
            "https://journals.aps.org/prb/abstract/10.1103/PhysRevB.8.2697": (
                "10.1103/PhysRevB.8.2697",
                "doi:10.1103/PhysRevB.8.2697",
                "Synthetic acceptor abstract",
                CitationKeyStatus.CANDIDATE_PROPOSED_NONCANONICAL,
                None,
                "baldereschiLipari1973",
            ),
        }
        doi, work_id, title, status, canonical, proposed = states[url]
        abstract = f"Author-supplied synthetic publisher abstract for {doi}."
        return AuthorSuppliedPublisherAbstractEvidence(
            bibliographic_work_id=work_id,
            source_url=url,
            doi=doi,
            title=title,
            authors=("A. Synthetic", "B. Synthetic"),
            publication_date="1955-01-01",
            abstract_text=abstract,
            source_document_sha256=hashlib.sha256(
                f"synthetic publisher page for {doi}".encode()
            ).hexdigest(),
            citation_key_status=status,
            canonical_citekey=canonical,
            proposed_citekey=proposed,
            warning_codes=warning_codes,
        )

    @classmethod
    def make_projection(cls) -> AdHocEvidenceRetrievalProjection:
        """Return the ordered three-abstract synthetic projection."""
        return DefiningAdapter().project(
            tuple(
                cls.make_evidence(url)
                for url, _, _ in DefiningAdapter.EXPECTED_CITATION_STATES
            )
        )

    @staticmethod
    def make_target() -> ManuscriptTargetContext:
        """Return one synthetic read-only target."""
        selected = "Synthetic citation gap."
        section = f"\\section{{Synthetic}}\n\\label{{sec:synthetic}}\n\n{selected}\n"
        return ManuscriptTargetContext(
            relative_path="docs/synthetic/chapter.tex",
            section_heading="\\section{Synthetic}",
            section_label="sec:synthetic",
            base_git_blob_sha1="a" * 40,
            document_sha256="b" * 64,
            section_text=section,
            selected_text=selected,
        )

    def test_constructor__evidence__preserves_ad_hoc_abstract_only_provenance(
        self,
    ) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-022

        Requirement: Ad-hoc inputs must state author-supplied provenance and
        publisher-abstract scope without implying full-paper or rights review.

        Acceptance: Every projected record has exact statuses, source digest, and an
        identity bound to abstract text; a full-text URL is rejected.
        """
        projection = self.make_projection()
        assert all(
            item.provenance_status is EvidenceProvenanceStatus.AUTHOR_SUPPLIED_AD_HOC
            for item in projection.evidence
        )
        assert all(
            item.source_scope is EvidenceSourceScope.PUBLISHER_ABSTRACT
            for item in projection.evidence
        )
        assert all(
            len(item.source_document_sha256) == 64 for item in projection.evidence
        )
        assert len({item.evidence_id for item in projection.evidence}) == 3
        assert all(
            item.evidence_id.startswith("author-supplied-evidence:sha256:")
            for item in projection.evidence
        )
        with pytest.raises(ValueError, match="authorized APS abstract"):
            AuthorSuppliedPublisherAbstractEvidence(
                bibliographic_work_id="doi:10.1103/PhysRev.97.869",
                source_url="https://journals.aps.org/pr/pdf/10.1103/PhysRev.97.869",
                doi="10.1103/PhysRev.97.869",
                title="Forbidden full text",
                authors=("A. Synthetic",),
                publication_date="1955-01-01",
                abstract_text="Synthetic text.",
                source_document_sha256="0" * 64,
                citation_key_status=CitationKeyStatus.ACCEPTED_ACTIVE_CANONICAL,
                canonical_citekey="luttingerKohn1955",
                proposed_citekey=None,
            )

    def test_method__project__preserves_target_key_dispositions(self) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-023

        Requirement: The accepted Luttinger--Kohn key remains canonical while donor
        and acceptor keys remain prospective and cannot be promoted locally.

        Acceptance: Exact valid states project; presenting the donor key as accepted
        is rejected even though the evidence record is otherwise structurally valid.
        """
        projection = self.make_projection()
        assert projection.evidence[0].canonical_citekey == "luttingerKohn1955"
        assert tuple(item.canonical_citekey for item in projection.evidence[1:]) == (
            None,
            None,
        )
        donor_url = DefiningAdapter.EXPECTED_CITATION_STATES[1][0]
        donor = self.make_evidence(donor_url)
        promoted = AuthorSuppliedPublisherAbstractEvidence(
            bibliographic_work_id=donor.bibliographic_work_id,
            source_url=donor.source_url,
            doi=donor.doi,
            title=donor.title,
            authors=donor.authors,
            publication_date=donor.publication_date,
            abstract_text=donor.abstract_text,
            source_document_sha256=donor.source_document_sha256,
            citation_key_status=CitationKeyStatus.ACCEPTED_ACTIVE_CANONICAL,
            canonical_citekey="kohnLuttinger1955donor",
            proposed_citekey=None,
        )
        with pytest.raises(ValueError, match="target snapshot"):
            DefiningAdapter().project((promoted,))

    def test_method__execute__returns_marker_draft_with_citation_gaps(self) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-024

        Requirement: Prospective keys must not block a bounded draft or render as
        canonical citations; their exact evidence markers require inspection.

        Acceptance: The result is ready-with-citation-gaps, cites only the accepted
        key, includes two exact markers, and remains ``NOT_EVALUATED``.
        """
        projection = self.make_projection()
        target = self.make_target()
        request = ManuscriptAuthoringRequest(
            target=target,
            retrieval=projection,
            required_bibliographic_work_ids=tuple(
                item.bibliographic_work_id for item in projection.evidence
            ),
            instruction=(
                "Draft only from publisher abstracts and preserve citation gaps."
            ),
            max_output_characters=2_000,
            max_citations=3,
        )
        port = self.InferenceStub(
            accepted_id=projection.evidence[0].evidence_id,
            gap_ids=tuple(sorted(item.evidence_id for item in projection.evidence[1:])),
            calls=[],
        )
        result = EvidenceGroundedManuscriptAuthor().execute(
            request, target.revision_id, port
        )
        assert result.outcome is (
            ManuscriptAuthoringOutcome.PROPOSAL_READY_WITH_CITATION_GAPS
        )
        assert result.issues == (
            ManuscriptAuthoringIssue.CITATION_GAPS_REQUIRE_INSPECTION,
        )
        assert type(result.proposal) is ManuscriptProposal
        assert tuple(
            citation.citation_key for citation in result.proposal.citations
        ) == ("luttingerKohn1955",)
        assert len(result.proposal.evidence_markers) == 2
        assert "kohnLuttinger1955donor" not in result.proposal.replacement_text
        assert "baldereschiLipari1973" not in result.proposal.replacement_text
        assert result.human_acceptance_status is HumanAcceptanceStatus.NOT_EVALUATED
        assert len(port.calls) == 1

    def test_method__execute__fails_closed_on_abstract_source_warning(self) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-025

        Requirement: Extraction or source warnings remain pre-inference failures.

        Acceptance: One warning yields inspection-required with no proposal and no
        inference call, even though citation gaps themselves permit drafting.
        """
        first_url = DefiningAdapter.EXPECTED_CITATION_STATES[0][0]
        warned = self.make_evidence(
            first_url, warning_codes=("ABSTRACT_EXTRACTION_REVIEW",)
        )
        projection = DefiningAdapter().project((warned,))
        target = self.make_target()
        request = ManuscriptAuthoringRequest(
            target=target,
            retrieval=projection,
            required_bibliographic_work_ids=(warned.bibliographic_work_id,),
            instruction="Draft only from the publisher abstract.",
            max_output_characters=1_000,
            max_citations=1,
        )
        port = self.InferenceStub(
            accepted_id=warned.evidence_id,
            gap_ids=(),
            calls=[],
        )
        result = EvidenceGroundedManuscriptAuthor().execute(
            request, target.revision_id, port
        )
        assert result.outcome is ManuscriptAuthoringOutcome.INSPECTION_REQUIRED
        assert result.issues == (ManuscriptAuthoringIssue.EVIDENCE_WARNING,)
        assert result.proposal is None
        assert port.calls == []

    def test_public_api__adapter__preserves_defining_object_identity(self) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-026

        Requirement: The curated facade must expose the exact defining adapter class.

        Acceptance: Defining and root-facade class objects are identical.
        """
        assert AuthorSuppliedPublisherAbstractAdapter is DefiningAdapter
        assert publications.AuthorSuppliedPublisherAbstractAdapter is DefiningAdapter

    def test_method__prompt_for__labels_abstract_limitations(self) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-027

        Requirement: The model prompt must carry explicit ad-hoc and abstract-only
        limitations together with exact markers and no promoted candidate key.

        Acceptance: Parsed evidence JSON contains exact provenance/scope, the
        limitation, two prospective markers, and no canonical value for those keys.
        """
        projection = self.make_projection()
        target = self.make_target()
        request = ManuscriptAuthoringRequest(
            target=target,
            retrieval=projection,
            required_bibliographic_work_ids=tuple(
                item.bibliographic_work_id for item in projection.evidence
            ),
            instruction="Draft only from publisher abstracts.",
            max_output_characters=2_000,
            max_citations=3,
        )
        prompt = EvidenceGroundedManuscriptAuthor().prompt_for(request)
        lines = prompt.splitlines()
        payload = json.loads(lines[lines.index("UNTRUSTED_QUOTED_EVIDENCE_JSON") + 1])
        assert payload[0]["provenance_status"] == "AUTHOR_SUPPLIED_AD_HOC"
        assert payload[0]["source_scope"] == "PUBLISHER_ABSTRACT"
        assert "no full-paper" in payload[0]["abstract_only_limitation"]
        assert payload[1]["canonical_citekey"] == ""
        assert payload[1]["proposed_noncanonical_citekey"] == ("kohnLuttinger1955donor")
        assert payload[1]["evidence_marker"].startswith("[[EVIDENCE:")
