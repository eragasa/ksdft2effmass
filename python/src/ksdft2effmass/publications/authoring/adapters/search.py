"""Project Koios Search adapter for manuscript authoring."""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.ingestion.transcript.evidence.selection import (
    TranscriptEvidenceSelectionResult,
)
from projectkoios.references.citation_identity import (
    CitationIdentityProjectionResult,
)
from projectkoios.search.evidence_retrieval import (
    EvidenceItem,
    EvidenceRetrievalOutcome,
    EvidenceRetrievalResult,
    RankedEvidenceItem,
    ReferenceIdentityStatus,
)

from ..evidence import EvidenceRetrievalProjection, RetrievedEvidenceExcerpt
from ..statuses import (
    CitationKeyStatus,
    EvidenceRetrievalOutcomeProjection,
    TranscriptEvidenceMappingBasis,
)
from .ingestion import ProjectKoiosIngestionAdapter
from .references import ProjectedCitationIdentity, ProjectKoiosReferencesAdapter


@dataclass(frozen=True, slots=True)
class ProjectKoiosSearchAdapter:
    """Project Search results in owner rank order through exact owner joins."""

    def project(
        self,
        result: EvidenceRetrievalResult,
        citation_identity: CitationIdentityProjectionResult,
        transcript_selections: tuple[TranscriptEvidenceSelectionResult, ...],
        /,
    ) -> EvidenceRetrievalProjection:
        """Return one local projection without retrieval or reranking."""
        if type(result) is not EvidenceRetrievalResult:
            raise TypeError("result must be EvidenceRetrievalResult")
        if type(citation_identity) is not CitationIdentityProjectionResult:
            raise TypeError(
                "citation_identity must be CitationIdentityProjectionResult"
            )
        if type(transcript_selections) is not tuple:
            raise TypeError("transcript_selections must be a built-in tuple")
        if not transcript_selections or any(
            type(selection) is not TranscriptEvidenceSelectionResult
            for selection in transcript_selections
        ):
            raise TypeError(
                "transcript_selections must contain selection result values"
            )
        result_ids = tuple(selection.result_id for selection in transcript_selections)
        if len(set(result_ids)) != len(result_ids):
            raise ValueError("transcript selection result identities must be unique")

        ingestion_adapter = ProjectKoiosIngestionAdapter()
        selection_references = tuple(
            ingestion_adapter.project(selection) for selection in transcript_selections
        )
        excerpts = tuple(
            self.project_ranked_item(
                ranked,
                citation_identity,
                transcript_selections,
            )
            for ranked in result.evidence
        )
        return EvidenceRetrievalProjection(
            retrieval_result_id=result.result_id,
            citation_identity_projection_id=citation_identity.projection_id,
            citation_identity_projection_result_id=citation_identity.result_id,
            transcript_selections=selection_references,
            outcome=self.project_outcome(result.outcome),
            evidence=excerpts,
            warning_codes=result.warnings,
        )

    def project_ranked_item(
        self,
        ranked: RankedEvidenceItem,
        citation_identity: CitationIdentityProjectionResult,
        transcript_selections: tuple[TranscriptEvidenceSelectionResult, ...],
        /,
    ) -> RetrievedEvidenceExcerpt:
        """Project one owner-ranked item while retaining its exact rank and IDs."""
        if type(ranked) is not RankedEvidenceItem:
            raise TypeError("ranked must be RankedEvidenceItem")
        item = ranked.item
        citation = ProjectKoiosReferencesAdapter().project(
            citation_identity, item.bibliographic_work_id
        )
        self.validate_reference_consistency(item, citation)
        ingestion_adapter = ProjectKoiosIngestionAdapter()
        matches = tuple(
            matched
            for selection in transcript_selections
            if (
                matched := ingestion_adapter.match_exact_pair(
                    selection,
                    transcript_result_id=item.transcript_id,
                    page_id=item.page_id,
                    block_id=item.block_id,
                    indexed_clean_text=item.indexed_text,
                    indexed_clean_text_sha256=item.indexed_text_sha256,
                    retained_raw_text=item.retained_text,
                    retained_raw_text_sha256=item.retained_text_sha256,
                )
            )
            is not None
        )
        if len(matches) != 1:
            raise ValueError(
                "Search evidence must match exactly one available ingestion block"
            )
        page, block = matches[0]
        selection_result_id = next(
            selection.result_id
            for selection in transcript_selections
            if selection.transcript_result_id == block.transcript_result_id
            and block in selection.blocks
        )
        warning_codes = tuple(warning.code for warning in item.warnings)
        return RetrievedEvidenceExcerpt(
            evidence_id=item.evidence_item_id,
            bibliographic_work_id=item.bibliographic_work_id,
            citation_key_status=citation.status,
            canonical_citekey=citation.canonical_citekey,
            citation_identity_projection_item_id=citation.projection_item_id,
            transcript_selection_result_id=selection_result_id,
            transcript_result_id=block.transcript_result_id,
            transcript_selected_page_evidence_id=page.selected_page_evidence_id,
            transcript_selected_block_evidence_id=(block.selected_block_evidence_id),
            page_id=block.page_id,
            block_id=block.block_id,
            block_record_id=block.block_record_id,
            search_ranked_evidence_item_id=ranked.ranked_evidence_item_id,
            search_rank=ranked.rank,
            indexed_clean_text=block.indexed_clean_text,
            indexed_clean_text_sha256=block.indexed_clean_text_sha256,
            retained_raw_text=block.retained_raw_text,
            retained_raw_text_sha256=block.retained_raw_text_sha256,
            mapping_basis=(
                TranscriptEvidenceMappingBasis.CLEAN_TRANSCRIPT_BLOCK_EXACT_PAIR
            ),
            source_span_ids=item.source_span_ids,
            warning_codes=warning_codes,
        )

    @staticmethod
    def validate_reference_consistency(
        item: EvidenceItem, citation: ProjectedCitationIdentity
    ) -> None:
        """Fail closed when Search and References identity projections disagree."""
        active = citation.status is CitationKeyStatus.ACCEPTED_ACTIVE_CANONICAL
        accepted_without_key = citation.status in {
            CitationKeyStatus.ACCEPTED_WITHOUT_ACTIVE_CITEKEY,
            CitationKeyStatus.INACTIVE_SUPERSEDED,
        }
        if active:
            if (
                item.reference_identity_status is not ReferenceIdentityStatus.ACCEPTED
                or item.accepted_citekey != citation.canonical_citekey
            ):
                raise ValueError("Search active citekey disagrees with References")
            return
        if accepted_without_key:
            if (
                item.reference_identity_status is not ReferenceIdentityStatus.ACCEPTED
                or item.accepted_citekey is not None
            ):
                raise ValueError("Search accepted identity disagrees with References")
            return
        if (
            item.reference_identity_status is not ReferenceIdentityStatus.CANDIDATE
            or item.accepted_citekey is not None
        ):
            raise ValueError("Search candidate identity disagrees with References")

    @staticmethod
    def project_outcome(
        outcome: EvidenceRetrievalOutcome,
    ) -> EvidenceRetrievalOutcomeProjection:
        """Map the exact closed owner outcome without fallback or coercion."""
        if outcome is EvidenceRetrievalOutcome.EVIDENCE_AVAILABLE:
            return EvidenceRetrievalOutcomeProjection.EVIDENCE_AVAILABLE
        if outcome is EvidenceRetrievalOutcome.INSUFFICIENT_EVIDENCE:
            return EvidenceRetrievalOutcomeProjection.INSUFFICIENT_EVIDENCE
        if outcome is EvidenceRetrievalOutcome.INVALID_REQUEST:
            return EvidenceRetrievalOutcomeProjection.INVALID_REQUEST
        if outcome is EvidenceRetrievalOutcome.INFRASTRUCTURE_FAILURE:
            return EvidenceRetrievalOutcomeProjection.INFRASTRUCTURE_FAILURE
        raise ValueError("unsupported Search evidence retrieval outcome")
