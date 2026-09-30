r"""Software verification of Project Koios owner-result authoring adapters.

Evidence profile: routine

Bounded artifact scope: canonical References, Ingestion, and Search owner results
projected into the local manuscript-authoring composition boundary.

Facet and represented meaning

The module verifies sanitized synthetic in-memory owner objects and deterministic
injected inference. It performs no network, model, corpus, manuscript, bibliography,
or persistence action.

Intrinsic and cross-object scope

Owner constructors and Actions produce the synthetic inputs. The local adapters own
cross-owner correlation and the manuscript author owns final proposal admission.

VVUQ and scientific exclusions

This is software verification only. Passing does not establish historical accuracy,
citation correctness, scientific validity, publication readiness, or human/PI
acceptance.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

import pytest
from projectkoios.ingestion.clean_transcript import (
    CleanTranscript,
    CleanTranscriptBlock,
    CleanTranscriptPage,
    CleanTranscriptStatus,
)
from projectkoios.ingestion.identity import stable_id
from projectkoios.ingestion.transcript.evidence.selection import (
    TranscriptEvidenceSelectionOutcome,
    TranscriptEvidenceSelectionRequest,
    TranscriptEvidenceSelectionResult,
    TranscriptEvidenceSelector,
)
from projectkoios.references.citation_identity import (
    CitationIdentityProjectionRequest,
    CitationIdentityProjectionResult,
    CitationIdentityProjectionStatus,
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
from projectkoios.search.evidence_retrieval import (
    AuthoringCorpusRole,
    AuthoringPurpose,
    DeterministicLexicalEvidenceRetriever,
    EvidenceCorpus,
    EvidenceItem,
    EvidenceRetrievalRequest,
    EvidenceRetrievalResult,
    ReferenceIdentityStatus,
)

from ksdft2effmass.publications import (
    CitationKeyStatus,
    EvidenceGroundedManuscriptAuthor,
    HumanAcceptanceStatus,
    ManuscriptAuthoringOutcome,
    ManuscriptAuthoringRequest,
    ManuscriptInferenceRequest,
    ManuscriptInferenceResponse,
    ManuscriptTargetContext,
    ProjectKoiosIngestionAdapter,
    ProjectKoiosSearchAdapter,
    ProposedCitation,
    TranscriptEvidenceSelectionOutcomeProjection,
)

pytestmark = pytest.mark.software_verification


class TestProjectKoiosAuthoringAdapters:
    """Own sanitized synthetic evidence for the three owner adapters."""

    @dataclass(slots=True)
    class InferenceStub:
        """Return one deterministic typed response without invoking a model."""

        citation_key: str
        evidence_id: str
        calls: list[ManuscriptInferenceRequest]

        def infer(
            self, request: ManuscriptInferenceRequest, /
        ) -> ManuscriptInferenceResponse:
            """Return output correlated to the exact local inference request."""
            self.calls.append(request)
            return ManuscriptInferenceResponse(
                inference_request_id=request.inference_request_id,
                inference_implementation_id="synthetic-adapter-inference:v1",
                replacement_text=(
                    f"Synthetic evidence-grounded prose \\cite{{{self.citation_key}}}."
                ),
                citations=(
                    ProposedCitation(
                        citation_key=self.citation_key,
                        evidence_ids=(self.evidence_id,),
                    ),
                ),
                evidence_ids=(self.evidence_id,),
                warning_codes=(),
            )

    @staticmethod
    def make_reference_projection(
        *, promote: bool
    ) -> tuple[CitationIdentityProjectionResult, str, str | None]:
        """Build one real References projection from sanitized synthetic records."""
        citekey = "syntheticCanonical"
        entry = "@article{syntheticDraft}\n"
        observation = SourceBibliographyObservation.create(
            source_id="synthetic-adapter-test",
            asserted_source_revision="synthetic-revision",
            source_path="synthetic-references.bib",
            bibliography_bytes=entry.encode("utf-8"),
            entry_index=0,
            observed_citekey="syntheticDraft",
            verbatim_entry=entry,
            parser=ProducerIdentity("synthetic-parser", "1"),
        )
        candidate = ReferenceCandidate.create(
            proposed_citekey="syntheticDraft",
            entry_type="article",
            title="Synthetic adapter evidence",
            authors=("A. Synthetic",),
            year="2026",
            source_observation_ids=(observation.observation_id,),
            generator=ProducerIdentity("synthetic-normalizer", "1"),
        )
        decisions: tuple[IdentityDecision, ...] = ()
        if promote:
            actor = ActorProvenance(
                actor_id="person:synthetic-reference-curator",
                actor_kind=ActorKind.PERSON,
                authority_scope=ActorAuthorityScope.REFERENCE_IDENTITY_CURATOR,
                verification_record_id="actor-verification:sha256:" + "a" * 64,
                verification_method="synthetic-authentication-record",
            )
            decisions = (
                IdentityDecision.promotion(
                    candidate_ids=(candidate.candidate_id,),
                    canonical_citekey=citekey,
                    actor=actor,
                    evidence_ids=tuple(
                        sorted(
                            (
                                actor.verification_record_id,
                                candidate.candidate_id,
                                observation.observation_id,
                            )
                        )
                    ),
                    rationale="Promote synthetic identity for adapter verification.",
                ),
            )
        projection = replay_identity_decisions((candidate,), decisions)
        work_id = (
            projection.active_reference_ids[0] if promote else candidate.candidate_id
        )
        request = CitationIdentityProjectionRequest(
            projection=projection,
            identity_ids=(work_id,),
        )
        result = CitationIdentityProjector().project(request=request)
        return result, work_id, citekey if promote else None

    @staticmethod
    def make_transcript_selection(
        *, warnings: tuple[str, ...] = ()
    ) -> tuple[CleanTranscript, TranscriptEvidenceSelectionResult]:
        """Build one real Ingestion selection over an exact synthetic block pair."""
        raw_text = "Synthetic continuum evidence from a retained raw block."
        clean_text = "Synthetic continuum evidence from a retained raw block."
        block = CleanTranscriptBlock.create(
            block_id="block:synthetic:1",
            page_index=0,
            printed_page_label="1",
            order_index=0,
            raw_text=raw_text,
            clean_text=clean_text,
            source_spans=(),
            transformations=(),
            dehyphenation_decision_ids=(),
            page_number_classification_id=None,
            publisher_classification_id=None,
            private_use_finding_ids=(),
        )
        page_text = f'[[PAGE physical=1 printed="1"]]\n\n{clean_text}'
        page = CleanTranscriptPage.create(
            page_index=0,
            printed_page_label="1",
            block_record_ids=(block.record_id,),
            text=page_text,
        )
        text = f"{page_text}\n"
        text_digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        normalized_warnings = tuple(sorted(set(warnings)))
        identity_parts = (
            "transcription-result:synthetic:1",
            "document:synthetic:1",
            "source:synthetic:1",
            "blob:synthetic:1",
            "sha256:" + "b" * 64,
            (),
            (page.page_id,),
            (block.record_id,),
            (),
            (),
            (),
            (),
            (),
            text_digest,
            len(text.encode("utf-8")),
            CleanTranscriptStatus.AUTOMATED_UNREVIEWED,
            normalized_warnings,
            "synthetic-clean-transcript",
            "1",
            "configuration:synthetic:1",
        )
        transcript = CleanTranscript(
            result_id=stable_id("clean-transcript-result", *identity_parts),
            transcription_result_id="transcription-result:synthetic:1",
            document_id="document:synthetic:1",
            source_id="source:synthetic:1",
            source_blob_id="blob:synthetic:1",
            source_content_hash="sha256:" + "b" * 64,
            layout_result_ids=(),
            pages=(page,),
            blocks=(block,),
            exclusions=(),
            dehyphenation_decisions=(),
            page_number_classifications=(),
            publisher_front_matter=(),
            private_use_glyph_findings=(),
            text=text,
            text_sha256=text_digest,
            utf8_byte_length=len(text.encode("utf-8")),
            status=CleanTranscriptStatus.AUTOMATED_UNREVIEWED,
            warnings=normalized_warnings,
            processor_name="synthetic-clean-transcript",
            processor_version="1",
            configuration_digest="configuration:synthetic:1",
        )
        request = TranscriptEvidenceSelectionRequest(
            transcript=transcript,
            selected_block_record_ids=(block.record_id,),
        )
        result = TranscriptEvidenceSelector().select(request=request)
        return transcript, result

    @staticmethod
    def make_search_result(
        *,
        transcript: CleanTranscript,
        bibliographic_work_id: str,
        canonical_citekey: str | None,
    ) -> EvidenceRetrievalResult:
        """Run real deterministic Search over one synthetic evidence item."""
        block = transcript.blocks[0]
        page = transcript.pages[0]
        accepted = canonical_citekey is not None
        item = EvidenceItem(
            corpus_role=AuthoringCorpusRole.REFERENCE_EVIDENCE,
            bibliographic_work_id=bibliographic_work_id,
            reference_identity_status=(
                ReferenceIdentityStatus.ACCEPTED
                if accepted
                else ReferenceIdentityStatus.CANDIDATE
            ),
            accepted_citekey=canonical_citekey,
            source_asset_id=transcript.source_id,
            transcript_id=transcript.result_id,
            page_id=page.page_id,
            page_index=page.page_index,
            printed_page_label=page.printed_page_label,
            block_id=block.block_id,
            source_span_ids=("source-span:synthetic:1",),
            indexed_text=block.clean_text,
            indexed_text_sha256=hashlib.sha256(
                block.clean_text.encode("utf-8")
            ).hexdigest(),
            retained_text=block.raw_text,
            retained_text_sha256=hashlib.sha256(
                block.raw_text.encode("utf-8")
            ).hexdigest(),
            warnings=(),
        )
        corpus = EvidenceCorpus(
            admitted_role=AuthoringCorpusRole.REFERENCE_EVIDENCE,
            items=(item,),
        )
        request = EvidenceRetrievalRequest(
            purpose=AuthoringPurpose.MANUSCRIPT_AUTHORING,
            query="synthetic continuum evidence",
            target_id="manuscript-target:synthetic:1",
            bibliographic_work_ids=(bibliographic_work_id,),
            required_bibliographic_work_ids=(bibliographic_work_id,),
            result_limit=1,
            per_work_limit=1,
            max_total_text_characters=1_000,
        )
        return DeterministicLexicalEvidenceRetriever(corpus=corpus).retrieve(
            request=request
        )

    @staticmethod
    def make_target() -> ManuscriptTargetContext:
        """Build a synthetic read-only target for local proposal composition."""
        selected_text = "Synthetic citation gap."
        section_text = (
            "\\section{Synthetic adapter section}\n"
            "\\label{sec:synthetic-adapter}\n\n"
            f"{selected_text}\n"
        )
        return ManuscriptTargetContext(
            relative_path="docs/synthetic/adapter-chapter.tex",
            section_heading="\\section{Synthetic adapter section}",
            section_label="sec:synthetic-adapter",
            base_git_blob_sha1="c" * 40,
            document_sha256="d" * 64,
            section_text=section_text,
            selected_text=selected_text,
        )

    def test_method__project__preserves_owner_identities_in_local_proposal(
        self,
    ) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-014

        Requirement: Canonical References, Ingestion, and Search results compose into
        local authoring without reranking, identity loss, model calls, or writes.

        Acceptance: Exact owner result/item/selection/rank identities reach a bounded
        proposal through deterministic injected inference; human acceptance remains
        not evaluated.
        """
        citation_result, work_id, canonical_citekey = self.make_reference_projection(
            promote=True
        )
        assert canonical_citekey is not None
        transcript, selection_result = self.make_transcript_selection()
        search_result = self.make_search_result(
            transcript=transcript,
            bibliographic_work_id=work_id,
            canonical_citekey=canonical_citekey,
        )
        retrieval = ProjectKoiosSearchAdapter().project(
            search_result,
            citation_result,
            (selection_result,),
        )
        target = self.make_target()
        request = ManuscriptAuthoringRequest(
            target=target,
            retrieval=retrieval,
            required_bibliographic_work_ids=(work_id,),
            instruction="Replace only the synthetic citation gap.",
            max_output_characters=500,
            max_citations=1,
        )
        excerpt = retrieval.evidence[0]
        inference = self.InferenceStub(canonical_citekey, excerpt.evidence_id, [])

        result = EvidenceGroundedManuscriptAuthor().execute(
            request,
            target.revision_id,
            inference,
        )

        assert result.outcome is ManuscriptAuthoringOutcome.PROPOSAL_READY
        assert result.human_acceptance_status is HumanAcceptanceStatus.NOT_EVALUATED
        assert retrieval.retrieval_result_id == search_result.result_id
        assert (
            retrieval.citation_identity_projection_result_id
            == citation_result.result_id
        )
        assert excerpt.search_ranked_evidence_item_id == (
            search_result.evidence[0].ranked_evidence_item_id
        )
        assert excerpt.search_rank == search_result.evidence[0].rank == 1
        assert excerpt.transcript_selection_result_id == selection_result.result_id
        assert excerpt.citation_identity_projection_item_id == (
            citation_result.items[0].item_id
        )
        assert len(inference.calls) == 1

    def test_method__project__never_promotes_candidate_citekey(self) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-015

        Requirement: A References candidate remains noncanonical across Search and the
        local projection even when the owner candidate carries a proposed citekey.

        Acceptance: The local excerpt has candidate status and no canonical citekey,
        so authoring fails closed before deterministic inference is called.
        """
        citation_result, work_id, canonical_citekey = self.make_reference_projection(
            promote=False
        )
        assert citation_result.items[0].status is (
            CitationIdentityProjectionStatus.CANDIDATE_PROPOSED_NONCANONICAL
        )
        assert canonical_citekey is None
        transcript, selection_result = self.make_transcript_selection()
        search_result = self.make_search_result(
            transcript=transcript,
            bibliographic_work_id=work_id,
            canonical_citekey=None,
        )
        retrieval = ProjectKoiosSearchAdapter().project(
            search_result,
            citation_result,
            (selection_result,),
        )
        excerpt = retrieval.evidence[0]
        target = self.make_target()
        request = ManuscriptAuthoringRequest(
            target=target,
            retrieval=retrieval,
            required_bibliographic_work_ids=(work_id,),
            instruction="Replace only the synthetic citation gap.",
            max_output_characters=500,
            max_citations=1,
        )
        inference = self.InferenceStub("mustNotRun", excerpt.evidence_id, [])

        result = EvidenceGroundedManuscriptAuthor().execute(
            request,
            target.revision_id,
            inference,
        )

        assert excerpt.citation_key_status is (
            CitationKeyStatus.CANDIDATE_PROPOSED_NONCANONICAL
        )
        assert excerpt.canonical_citekey is None
        assert result.outcome is ManuscriptAuthoringOutcome.INSPECTION_REQUIRED
        assert inference.calls == []

    def test_method__project__never_admits_warning_selection_evidence(self) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-016

        Requirement: An Ingestion warning not resolved to a nonselected block exposes
        no selectable local evidence.

        Acceptance: The owner returns warning-inspection with no evidence, the local
        selection projection retains that outcome, and Search projection fails closed.
        """
        citation_result, work_id, canonical_citekey = self.make_reference_projection(
            promote=True
        )
        assert canonical_citekey is not None
        transcript, selection_result = self.make_transcript_selection(
            warnings=("synthetic_unresolved_transcript_warning",)
        )
        assert selection_result.outcome is (
            TranscriptEvidenceSelectionOutcome.WARNING_INSPECTION_REQUIRED
        )
        selection_projection = ProjectKoiosIngestionAdapter().project(selection_result)
        search_result = self.make_search_result(
            transcript=transcript,
            bibliographic_work_id=work_id,
            canonical_citekey=canonical_citekey,
        )

        assert selection_projection.outcome is (
            TranscriptEvidenceSelectionOutcomeProjection.WARNING_INSPECTION_REQUIRED
        )
        assert selection_result.blocks == ()
        with pytest.raises(ValueError, match="exactly one available ingestion block"):
            ProjectKoiosSearchAdapter().project(
                search_result,
                citation_result,
                (selection_result,),
            )
