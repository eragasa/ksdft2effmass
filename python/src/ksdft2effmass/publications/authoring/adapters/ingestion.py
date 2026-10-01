"""Project Koios Ingestion adapter for manuscript authoring."""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.ingestion.transcript.evidence.selection import (
    SelectedTranscriptBlockEvidence,
    SelectedTranscriptPageEvidence,
    TranscriptEvidenceSelectionOutcome,
    TranscriptEvidenceSelectionResult,
)
from projectkoios.ingestion.transcript.evidence.selection import (
    TranscriptEvidenceMappingBasis as OwnerTranscriptEvidenceMappingBasis,
)

from ..evidence import TranscriptEvidenceSelectionReference
from ..statuses import TranscriptEvidenceSelectionOutcomeProjection


@dataclass(frozen=True, slots=True)
class ProjectKoiosIngestionAdapter:
    """Project exact transcript selection state and clean/raw evidence pairs."""

    def project(
        self, result: TranscriptEvidenceSelectionResult, /
    ) -> TranscriptEvidenceSelectionReference:
        """Project one owner result while retaining its identity and outcome."""
        if type(result) is not TranscriptEvidenceSelectionResult:
            raise TypeError("result must be TranscriptEvidenceSelectionResult")
        return TranscriptEvidenceSelectionReference(
            selection_result_id=result.result_id,
            outcome=self.project_outcome(result.outcome),
            warning_codes=result.warnings_requiring_inspection,
        )

    def match_exact_pair(
        self,
        result: TranscriptEvidenceSelectionResult,
        /,
        *,
        transcript_result_id: str,
        page_id: str,
        block_id: str,
        indexed_clean_text: str,
        indexed_clean_text_sha256: str,
        retained_raw_text: str,
        retained_raw_text_sha256: str,
    ) -> tuple[SelectedTranscriptPageEvidence, SelectedTranscriptBlockEvidence] | None:
        """Return one exact selected pair or ``None`` when identities do not match.

        A matching block identity with differing clean/raw text or digest is rejected
        rather than treated as another candidate. Nonavailable selection outcomes can
        never return selectable evidence.
        """
        if type(result) is not TranscriptEvidenceSelectionResult:
            raise TypeError("result must be TranscriptEvidenceSelectionResult")
        if result.outcome is not TranscriptEvidenceSelectionOutcome.EVIDENCE_AVAILABLE:
            return None
        if result.transcript_result_id != transcript_result_id:
            return None
        matches = tuple(
            block
            for block in result.blocks
            if block.page_id == page_id and block.block_id == block_id
        )
        if not matches:
            return None
        if len(matches) != 1:
            raise ValueError("ingestion selection contains ambiguous block identity")
        block = matches[0]
        if block.mapping_basis is not (
            OwnerTranscriptEvidenceMappingBasis.CLEAN_TRANSCRIPT_BLOCK_EXACT_PAIR
        ):
            raise ValueError("ingestion evidence mapping basis is unsupported")
        if (
            block.indexed_clean_text != indexed_clean_text
            or block.indexed_clean_text_sha256 != indexed_clean_text_sha256
            or block.retained_raw_text != retained_raw_text
            or block.retained_raw_text_sha256 != retained_raw_text_sha256
        ):
            raise ValueError(
                "Search text does not match the exact ingestion block pair"
            )
        pages = tuple(
            page
            for page in result.pages
            if page.page_id == page_id
            and block.selected_block_evidence_id in page.selected_block_evidence_ids
        )
        if len(pages) != 1:
            raise ValueError("ingestion selection page correlation is not exact")
        return pages[0], block

    @staticmethod
    def project_outcome(
        outcome: TranscriptEvidenceSelectionOutcome,
    ) -> TranscriptEvidenceSelectionOutcomeProjection:
        """Map the exact closed owner outcome without fallback or coercion."""
        if outcome is TranscriptEvidenceSelectionOutcome.INVALID_SELECTION:
            return TranscriptEvidenceSelectionOutcomeProjection.INVALID_SELECTION
        if outcome is TranscriptEvidenceSelectionOutcome.MISSING_BLOCK:
            return TranscriptEvidenceSelectionOutcomeProjection.MISSING_BLOCK
        if outcome is TranscriptEvidenceSelectionOutcome.TRANSCRIPT_NOT_COMPLETE:
            return TranscriptEvidenceSelectionOutcomeProjection.TRANSCRIPT_NOT_COMPLETE
        if outcome is (TranscriptEvidenceSelectionOutcome.WARNING_INSPECTION_REQUIRED):
            return (
                TranscriptEvidenceSelectionOutcomeProjection.WARNING_INSPECTION_REQUIRED
            )
        if outcome is TranscriptEvidenceSelectionOutcome.EVIDENCE_AVAILABLE:
            return TranscriptEvidenceSelectionOutcomeProjection.EVIDENCE_AVAILABLE
        raise ValueError("unsupported Ingestion transcript selection outcome")
