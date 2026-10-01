r"""Software verification of ``ResearchMonographCitationTargetSnapshotAdapter``.

Evidence profile: routine

Bounded artifact scope: the one-way optional mapping from an exact replay-valid owner
Result to canonical Project Koios References target DTOs.

Facet and represented meaning

The adapter represents only neutral citation target occurrences, groups, bibliography
entry locators/content identities, source gaps, and closure tuples.

Intrinsic and cross-object scope

Evidence covers the supported import route, public dependency direction, owner-order
mapping, deliberate field renames, null observation bindings, and pre-adaptation
integrity replay.

VVUQ and scientific exclusions

This is structural software verification. It establishes no bibliography observation,
identity decision, availability evidence, rights or use admission, processing status,
scientific validation, UQ, or human acceptance.
"""

from hashlib import sha256
from pathlib import Path

import pytest
from projectkoios.references.citations import CitationTargetSnapshot

from ksdft2effmass.campaigns.research_monograph import (
    ResearchMonographCitationSnapshotCompiler,
    ResearchMonographCitationSnapshotRequest,
    ResearchMonographCitationSnapshotResult,
)
from ksdft2effmass.integration.projectkoios import (
    ResearchMonographCitationTargetSnapshotAdapter,
)

pytestmark = pytest.mark.software_verification
SUT = ResearchMonographCitationTargetSnapshotAdapter


class TestResearchMonographCitationTargetSnapshotAdapter:
    """Own software evidence for the neutral Project Koios target mapping."""

    def test_method__execute__maps_complete_real_snapshot_in_owner_order(self) -> None:
        """Evidence ID: SV-KOIOS-CITATION-TARGET-ADAPTER-001

        Requirement: The adapter must map all neutral target records from the exact
        owner Result without reordering or rescanning sources.

        Acceptance: The Project Koios snapshot preserves 277 occurrences, 122 groups,
        122 entries, two gaps, source identities and order, and empty closure failures.
        """
        result = self.compile_repository()

        target = SUT().execute(result)

        assert type(target) is CitationTargetSnapshot
        same_occurrence_order = self.same_text_sequence(
            tuple(value.occurrence_id for value in target.occurrences),
            tuple(value.occurrence_id for value in result.snapshot.occurrences),
        )
        same_group_order = self.same_text_sequence(
            tuple(value.group_id for value in target.groups),
            tuple(value.group_id for value in result.snapshot.groups),
        )
        same_entry_order = self.same_text_sequence(
            tuple(value.entry_id for value in target.bibliography_entries),
            tuple(
                value.bibliography_entry_id
                for value in result.snapshot.bibliography_entries
            ),
        )
        same_gap_order = self.same_text_sequence(
            tuple(value.source_gap_id for value in target.source_gaps),
            tuple(value.source_gap_id for value in result.snapshot.source_gaps),
        )
        same_bibliography_path = self.same_text(
            target.bibliography_source_path, result.snapshot.bibliography_path
        )

        assert target.snapshot_id == result.snapshot.snapshot_id
        assert same_bibliography_path
        assert target.bibliography_content_identity.digest == (
            result.snapshot.bibliography_content_identity.digest
        )
        assert same_occurrence_order
        assert same_group_order
        assert same_entry_order
        assert same_gap_order
        assert len(target.occurrences) == 277
        assert len(target.groups) == 122
        assert len(target.bibliography_entries) == 122
        assert len(target.source_gaps) == 2
        assert len(target.missing_keys) == 0
        assert len(target.duplicate_keys) == 0
        assert len(target.uncited_keys) == 0

    def test_method__execute__uses_reviewed_neutral_field_mapping(self) -> None:
        """Evidence ID: SV-KOIOS-CITATION-TARGET-ADAPTER-002

        Requirement: The target mapping must apply only the reviewed bibliography
        field renames and preserve target-owned locator and identity values exactly.

        Acceptance: ``bibliography_entry_id`` maps to ``entry_id``,
        ``bibliography_path`` maps to ``bibliography_source_path``, and representative
        occurrence, entry, and gap fields equal their owner records.
        """
        result = self.compile_repository()
        target = SUT().execute(result)
        source_occurrence = result.snapshot.occurrences[0]
        target_occurrence = target.occurrences[0]
        source_entry = result.snapshot.bibliography_entries[0]
        target_entry = target.bibliography_entries[0]
        source_gap = result.snapshot.source_gaps[0]
        target_gap = target.source_gaps[0]
        same_bibliography_path = self.same_text(
            target.bibliography_source_path, result.snapshot.bibliography_path
        )
        same_key = self.same_text(target_occurrence.key, source_occurrence.key)
        same_locator_path = self.same_text(
            target_occurrence.locator.source_path,
            source_occurrence.locator.source_path,
        )
        same_gap_reason = self.same_text(target_gap.reason, source_gap.reason.value)
        same_placeholder = self.same_text(
            target_gap.placeholder_identifier, source_gap.placeholder_identifier
        )

        assert same_bibliography_path
        assert same_key
        assert target_occurrence.origin == source_occurrence.origin.value
        assert same_locator_path
        assert target_occurrence.locator.source_content_identity.digest == (
            source_occurrence.locator.source_content_identity.digest
        )
        assert target_entry.entry_id == source_entry.bibliography_entry_id
        assert target_entry.entry_content_identity.digest == (
            source_entry.entry_content_identity.digest
        )
        assert same_gap_reason
        assert same_placeholder

    def test_method__execute__leaves_references_observation_binding_absent(
        self,
    ) -> None:
        """Evidence ID: SV-KOIOS-CITATION-TARGET-ADAPTER-003

        Requirement: Target adaptation must not fabricate a References-owned
        bibliography observation identity or intake result.

        Acceptance: Every target entry retains a null observation binding and the
        target DTO exposes no intake, availability, rights, processing, or projection
        status field.
        """
        target = SUT().execute(self.compile_repository())

        assert all(
            value.source_bibliography_observation_id is None
            for value in target.bibliography_entries
        )
        assert set(target.__dataclass_fields__) == {
            "snapshot_id",
            "bibliography_source_path",
            "bibliography_content_identity",
            "occurrences",
            "groups",
            "bibliography_entries",
            "source_gaps",
            "missing_keys",
            "duplicate_keys",
            "uncited_keys",
            "target_projection_id",
        }

    def test_method__execute__replays_owner_result_before_adaptation(self) -> None:
        """Evidence ID: SV-KOIOS-CITATION-TARGET-ADAPTER-004

        Requirement: The optional boundary must replay owner integrity rather than
        trusting stored Result identity text.

        Acceptance: A deliberately forged exact Result instance with the valid
        snapshot but wrong ``result_id`` raises ``ValueError``.
        """
        result = self.compile_repository()
        forged = object.__new__(ResearchMonographCitationSnapshotResult)
        object.__setattr__(forged, "request_id", result.request_id)
        object.__setattr__(forged, "result_id", "citation-result:" + "0" * 64)
        object.__setattr__(forged, "snapshot", result.snapshot)

        with pytest.raises(ValueError, match="result_id"):
            SUT().execute(forged)

    def test_method__execute__rejects_non_result_input(self) -> None:
        """Evidence ID: SV-KOIOS-CITATION-TARGET-ADAPTER-005

        Requirement: The integration accepts only the exact owner Result type.

        Acceptance: A string value is rejected without conversion or source lookup.
        """
        invalid: str | ResearchMonographCitationSnapshotResult = "not a result"

        with pytest.raises(TypeError, match="must be"):
            SUT().execute(invalid)  # type: ignore[arg-type]

    @staticmethod
    def same_text(left: str, right: str) -> bool:
        """Compare confidential text through fixed-size SHA-256 digests."""
        return sha256(left.encode()).digest() == sha256(right.encode()).digest()

    @staticmethod
    def same_text_sequence(left: tuple[str, ...], right: tuple[str, ...]) -> bool:
        """Compare ordered confidential text sequences without assertion display."""
        if len(left) != len(right):
            return False
        left_digest = sha256()
        right_digest = sha256()
        for left_value, right_value in zip(left, right, strict=True):
            left_bytes = left_value.encode()
            right_bytes = right_value.encode()
            left_digest.update(len(left_bytes).to_bytes(8, "big"))
            left_digest.update(left_bytes)
            right_digest.update(len(right_bytes).to_bytes(8, "big"))
            right_digest.update(right_bytes)
        return left_digest.digest() == right_digest.digest()

    @staticmethod
    def compile_repository() -> ResearchMonographCitationSnapshotResult:
        """Compile the current isolated worktree through the supported API."""
        repository_root = Path(__file__).resolve().parents[6]
        return ResearchMonographCitationSnapshotCompiler().execute(
            ResearchMonographCitationSnapshotRequest(repository_root.as_posix())
        )
