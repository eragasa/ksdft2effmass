r"""Software verification of ``AuthorSuppliedPublisherAbstractAdapter``.

Evidence profile: routine

Bounded artifact scope: explicit APS publisher-abstract evidence adaptation.

Facet and represented meaning

The adapter preserves author-supplied ad-hoc provenance, abstract-only scope, exact
References lineage, and owner-projected accepted-versus-prospective status.

Intrinsic and cross-object scope

Immutable evidence records own exact source/content and projected-citation identities;
the adapter owns owner-result matching and canonical ordering, and the manuscript
author owns warning admission and marker-bearing proposal composition.

VVUQ and scientific exclusions

Synthetic abstract text verifies software behavior only. It does not establish
full-paper review, rights determination, citation correctness, scientific validation,
uncertainty quantification, publication readiness, or human acceptance.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace

import pytest
from projectkoios.references.citation_identity import (
    CitationIdentityProjectionRequest,
    CitationIdentityProjectionResult,
    CitationIdentityProjector,
)
from projectkoios.references.identity import (
    ActorAuthorityScope,
    ActorKind,
    ActorProvenance,
    IdentityDecision,
    ProducerIdentity,
    ReferenceCandidate,
    SourceBibliographyObservation,
    replay_identity_decisions,
)

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
    ProjectedCitationIdentity,
    ProjectKoiosReferencesAdapter,
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
                inference_implementation_id="synthetic-ad-hoc-inference",
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

    ABSTRACT_SPECS = (
        (
            "https://journals.aps.org/pr/abstract/10.1103/PhysRev.97.869",
            "10.1103/PhysRev.97.869",
            "Synthetic representation abstract",
            "ownerRepresentationDraft",
            "luttingerKohn1955",
            None,
        ),
        (
            "https://journals.aps.org/pr/abstract/10.1103/PhysRev.98.915",
            "10.1103/PhysRev.98.915",
            "Synthetic donor abstract",
            "ownerDonorDraft",
            None,
            "kohnLuttinger1955donor",
        ),
        (
            "https://journals.aps.org/prb/abstract/10.1103/PhysRevB.8.2697",
            "10.1103/PhysRevB.8.2697",
            "Synthetic acceptor abstract",
            "ownerAcceptorDraft",
            None,
            "baldereschiLipari1973",
        ),
    )

    @classmethod
    def make_references_result(
        cls,
    ) -> tuple[CitationIdentityProjectionResult, dict[str, ProjectedCitationIdentity]]:
        """Return one exact owner result and its strict local item projections."""
        observations = tuple(
            SourceBibliographyObservation.create(
                source_id="synthetic-abstract-adapter-test",
                asserted_source_revision="synthetic-revision",
                source_path="synthetic-references.bib",
                bibliography_bytes=f"@article{{{owner_key}}}\n".encode(),
                entry_index=index,
                observed_citekey=owner_key,
                verbatim_entry=f"@article{{{owner_key}}}\n",
                parser=ProducerIdentity("synthetic-parser", "1"),
            )
            for index, (_, _, _, owner_key, _, _) in enumerate(cls.ABSTRACT_SPECS)
        )
        candidates = tuple(
            ReferenceCandidate.create(
                proposed_citekey=owner_key,
                entry_type="article",
                title=title,
                authors=("A. Synthetic",),
                year="1955",
                source_observation_ids=(observation.observation_id,),
                generator=ProducerIdentity("synthetic-normalizer", "1"),
            )
            for (_, _, title, owner_key, _, _), observation in zip(
                cls.ABSTRACT_SPECS, observations, strict=True
            )
        )
        actor = ActorProvenance(
            actor_id="person:synthetic-reference-curator",
            actor_kind=ActorKind.PERSON,
            authority_scope=ActorAuthorityScope.REFERENCE_IDENTITY_CURATOR,
            verification_record_id="actor-verification:sha256:" + "a" * 64,
            verification_method="synthetic-authentication-record",
        )
        promotion = IdentityDecision.promotion(
            candidate_ids=(candidates[0].candidate_id,),
            canonical_citekey="luttingerKohn1955",
            actor=actor,
            evidence_ids=tuple(
                sorted(
                    (
                        actor.verification_record_id,
                        candidates[0].candidate_id,
                        observations[0].observation_id,
                    )
                )
            ),
            rationale="Accept one synthetic identity for adapter verification.",
        )
        projection = replay_identity_decisions(candidates, (promotion,))
        work_ids = (
            projection.active_reference_ids[0],
            candidates[1].candidate_id,
            candidates[2].candidate_id,
        )
        result = CitationIdentityProjector().project(
            request=CitationIdentityProjectionRequest(
                projection=projection,
                identity_ids=tuple(sorted(work_ids)),
            )
        )
        adapter = ProjectKoiosReferencesAdapter()
        by_url = {
            spec[0]: adapter.project(result, work_id)
            for spec, work_id in zip(cls.ABSTRACT_SPECS, work_ids, strict=True)
        }
        return result, by_url

    @classmethod
    def make_evidence(
        cls,
        url: str,
        *,
        citation_identity: ProjectedCitationIdentity | None = None,
        warning_codes: tuple[str, ...] = (),
    ) -> AuthorSuppliedPublisherAbstractEvidence:
        """Return synthetic abstract evidence bound to one exact owner projection."""
        specs = {spec[0]: spec[1:] for spec in cls.ABSTRACT_SPECS}
        doi, title, _, _, proposed = specs[url]
        if citation_identity is None:
            _, identities = cls.make_references_result()
            citation_identity = identities[url]
        abstract = f"Author-supplied synthetic publisher abstract for {doi}."
        return AuthorSuppliedPublisherAbstractEvidence(
            bibliographic_work_id=citation_identity.bibliographic_work_id,
            source_url=url,
            doi=doi,
            title=title,
            authors=("A. Synthetic", "B. Synthetic"),
            publication_date="1955-01-01",
            abstract_text=abstract,
            source_document_sha256=hashlib.sha256(
                f"synthetic publisher page for {doi}".encode()
            ).hexdigest(),
            citation_identity=citation_identity,
            proposed_citekey=proposed,
            warning_codes=warning_codes,
        )

    @classmethod
    def make_projection(cls) -> AdHocEvidenceRetrievalProjection:
        """Return the canonical three-abstract synthetic projection."""
        result, identities = cls.make_references_result()
        evidence = tuple(
            cls.make_evidence(url, citation_identity=identities[url])
            for url, *_ in cls.ABSTRACT_SPECS
        )
        return DefiningAdapter().project(evidence, result)

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
        accepted = next(
            item
            for item in projection.evidence
            if item.citation_key_status is CitationKeyStatus.ACCEPTED_ACTIVE_CANONICAL
        )
        with pytest.raises(ValueError, match="authorized APS abstract"):
            AuthorSuppliedPublisherAbstractEvidence(
                bibliographic_work_id=accepted.bibliographic_work_id,
                source_url="https://journals.aps.org/pr/pdf/10.1103/PhysRev.97.869",
                doi="10.1103/PhysRev.97.869",
                title="Forbidden full text",
                authors=("A. Synthetic",),
                publication_date="1955-01-01",
                abstract_text="Synthetic text.",
                source_document_sha256="0" * 64,
                citation_identity=accepted.citation_identity,
                proposed_citekey=None,
            )

    def test_method__project__preserves_owner_key_dispositions(self) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-023

        Requirement: Canonical status and key come only from the exact References
        result while local candidate labels remain explicitly noncanonical.

        Acceptance: Exact owner lineage projects; a locally forged accepted donor
        identity is rejected against the supplied References result.
        """
        projection = self.make_projection()
        accepted = tuple(
            item
            for item in projection.evidence
            if item.citation_key_status is CitationKeyStatus.ACCEPTED_ACTIVE_CANONICAL
        )
        candidates = tuple(
            item
            for item in projection.evidence
            if item.citation_key_status
            is CitationKeyStatus.CANDIDATE_PROPOSED_NONCANONICAL
        )
        assert tuple(item.canonical_citekey for item in accepted) == (
            "luttingerKohn1955",
        )
        assert tuple(item.canonical_citekey for item in candidates) == (None, None)

        result, identities = self.make_references_result()
        donor_url = self.ABSTRACT_SPECS[1][0]
        owner_donor = identities[donor_url]
        forged_identity = ProjectedCitationIdentity(
            projection_result_id=owner_donor.projection_result_id,
            projection_id=owner_donor.projection_id,
            projection_item_id=owner_donor.projection_item_id,
            bibliographic_work_id=owner_donor.bibliographic_work_id,
            status=CitationKeyStatus.ACCEPTED_ACTIVE_CANONICAL,
            canonical_citekey="kohnLuttinger1955donor",
        )
        owner_evidence = self.make_evidence(
            donor_url,
            citation_identity=owner_donor,
        )
        forged = replace(
            owner_evidence,
            citation_identity=forged_identity,
            proposed_citekey=None,
        )
        with pytest.raises(ValueError, match="exact References lineage"):
            DefiningAdapter().project((forged,), result)

    def test_constructor__evidence__rejects_mismatched_owner_work_lineage(self) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-037

        Requirement: Abstract work identity must equal its exact projected References
        work identity rather than a locally asserted replacement.

        Acceptance: Changing only the abstract work ID is rejected at construction.
        """
        _, identities = self.make_references_result()
        url = self.ABSTRACT_SPECS[0][0]
        exact = self.make_evidence(url, citation_identity=identities[url])
        with pytest.raises(ValueError, match="bibliographic work IDs differ"):
            replace(exact, bibliographic_work_id="forged-work-id")

    def test_method__project__canonicalizes_caller_evidence_order(self) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-038

        Requirement: One bounded abstract set must yield one prompt order regardless
        of caller tuple order.

        Acceptance: Forward and reversed tuples project to equal canonical evidence
        order and equal projection identity.
        """
        result, identities = self.make_references_result()
        evidence = tuple(
            self.make_evidence(url, citation_identity=identities[url])
            for url, *_ in self.ABSTRACT_SPECS
        )
        forward = DefiningAdapter().project(evidence, result)
        reversed_projection = DefiningAdapter().project(
            tuple(reversed(evidence)), result
        )
        assert forward == reversed_projection
        assert forward.evidence == tuple(
            sorted(
                forward.evidence,
                key=lambda item: (item.bibliographic_work_id, item.evidence_id),
            )
        )
        with pytest.raises(ValueError, match="canonical work and evidence order"):
            AdHocEvidenceRetrievalProjection(evidence=tuple(reversed(forward.evidence)))

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
        accepted_id = next(
            item.evidence_id
            for item in projection.evidence
            if item.citation_key_status is CitationKeyStatus.ACCEPTED_ACTIVE_CANONICAL
        )
        gap_ids = tuple(
            sorted(
                item.evidence_id
                for item in projection.evidence
                if item.citation_key_status
                is CitationKeyStatus.CANDIDATE_PROPOSED_NONCANONICAL
            )
        )
        port = self.InferenceStub(
            accepted_id=accepted_id,
            gap_ids=gap_ids,
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
        references_result, identities = self.make_references_result()
        first_url = self.ABSTRACT_SPECS[0][0]
        warned = self.make_evidence(
            first_url,
            citation_identity=identities[first_url],
            warning_codes=("ABSTRACT_EXTRACTION_REVIEW",),
        )
        projection = DefiningAdapter().project((warned,), references_result)
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
        authoring_result = EvidenceGroundedManuscriptAuthor().execute(
            request, target.revision_id, port
        )
        assert (
            authoring_result.outcome is ManuscriptAuthoringOutcome.INSPECTION_REQUIRED
        )
        assert authoring_result.issues == (ManuscriptAuthoringIssue.EVIDENCE_WARNING,)
        assert authoring_result.proposal is None
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
        assert all(
            item["provenance_status"] == "AUTHOR_SUPPLIED_AD_HOC" for item in payload
        )
        assert all(item["source_scope"] == "PUBLISHER_ABSTRACT" for item in payload)
        assert all(
            "no full-paper" in item["abstract_only_limitation"] for item in payload
        )
        donor = next(
            item
            for item in payload
            if item["proposed_noncanonical_citekey"] == "kohnLuttinger1955donor"
        )
        assert donor["canonical_citekey"] == ""
        assert donor["evidence_marker"].startswith("[[EVIDENCE:")
        assert donor["citation_identity_projection_result_id"]
        assert donor["citation_identity_projection_item_id"]
        assert donor["projected_citation_identity_id"].startswith(
            "projected-citation-identity:sha256:"
        )
        assert (
            "Set warning_codes to [] when output complies with the declared scope"
            in prompt
        )
        assert "Nonempty warnings fail closed." in prompt
