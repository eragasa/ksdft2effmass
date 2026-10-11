r"""Software verification of ``ResearchMonographCitationSnapshotCompiler``.

Evidence profile: routine

Bounded artifact scope: exact repository-owned monograph graph, bibliography,
rendered citation semantics, immutable locators, and target-owned identities.

Facet and represented meaning

The compiler represents one complete citation snapshot without TeX execution or
manuscript excerpts.

Intrinsic and cross-object scope

Evidence covers the accepted repository baseline, deterministic reconstruction,
origin accounting, locator closure, and the supported public import route.

VVUQ and scientific exclusions

This is structural software verification. It establishes no bibliographic metadata
truth, source support for claims, rights or use admission, scientific validation, UQ,
or human acceptance.
"""

from collections import Counter
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    ManuscriptCitationOrigin,
    ManuscriptCitationPriority,
    ManuscriptCitationSnapshot,
    ResearchMonographCitationSnapshotCompiler,
    ResearchMonographCitationSnapshotRequest,
)

pytestmark = pytest.mark.software_verification
SUT = ResearchMonographCitationSnapshotCompiler


class TestResearchMonographCitationSnapshotCompiler:
    """Own software evidence for canonical monograph citation compilation."""

    def test_method__execute__matches_authorized_repository_baseline(self) -> None:
        """Evidence ID: SV-CITATION-SNAPSHOT-COMPILER-001

        Requirement: The compiler must cover the authorized monograph graph and
        rendered citation semantics while recording the exact current repository
        revision.

        Acceptance: The result has 46 files, 131 groups, 245 calls, 307 occurrences,
        45 todos, 131 bibliography entries, two source gaps, and no closure gaps.
        """
        snapshot = self.compile_repository()

        assert len(snapshot.repository_revision) == 40
        assert set(snapshot.repository_revision) <= set("0123456789abcdef")
        assert len(snapshot.source_files) == 46
        assert len(snapshot.include_instances) == 46
        assert len(snapshot.groups) == 131
        assert len(snapshot.calls) == 245
        assert len(snapshot.occurrences) == 307
        assert len(snapshot.todos) == 45
        assert len(snapshot.bibliography_entries) == 131
        assert len(snapshot.source_gaps) == 2
        assert snapshot.missing_keys == ()
        assert snapshot.duplicate_keys == ()
        assert snapshot.uncited_keys == ()

    def test_method__execute__preserves_origin_priority_and_gap_partitions(
        self,
    ) -> None:
        """Evidence ID: SV-CITATION-SNAPSHOT-COMPILER-002

        Requirement: Direct, editorial-generated, priority, and non-key
        unresolved-source records must remain separately countable without conflating
        source gaps with
        missing bibliography keys.

        Acceptance: Exact origin/priority partitions and 14 generated-only groups are
        retained; both source gaps have no invented citation group.
        """
        snapshot = self.compile_repository()

        assert Counter(value.origin for value in snapshot.occurrences) == {
            ManuscriptCitationOrigin.DIRECT: 225,
            ManuscriptCitationOrigin.CITATION_TODO_EXPANSION: 82,
        }
        assert Counter(value.priority for value in snapshot.todos) == {
            ManuscriptCitationPriority.HIGH: 10,
            ManuscriptCitationPriority.MEDIUM: 28,
            ManuscriptCitationPriority.LOW: 7,
        }
        assert (
            sum(group.direct_occurrence_count == 0 for group in snapshot.groups) == 14
        )
        assert (
            sum(
                bool(group.direct_occurrence_count and group.generated_occurrence_count)
                for group in snapshot.groups
            )
            == 32
        )
        assert tuple(
            value.placeholder_identifier for value in snapshot.source_gaps
        ) == ("XXXXXX", "XXXX")

    def test_method__execute__is_deterministic_and_uses_no_references_ids(self) -> None:
        """Evidence ID: SV-CITATION-SNAPSHOT-COMPILER-003

        Requirement: Equal exact repository inputs must produce equal immutable
        snapshots and leave References-owned observation identities unset.

        Acceptance: Two independent compilations compare equal and all 131 target
        bibliography entries have a null source observation binding.
        """
        first = self.compile_repository()
        second = self.compile_repository()

        assert first == second
        assert first.snapshot_id.startswith("citation-snapshot:")
        assert all(
            entry.source_bibliography_observation_id is None
            for entry in first.bibliography_entries
        )

    def test_method__execute__retains_excerpt_free_immutable_locators(self) -> None:
        """Evidence ID: SV-CITATION-SNAPSHOT-COMPILER-004

        Requirement: API-facing locators must use path, content identity, include
        order, byte span, line, and column without manuscript excerpts.

        Acceptance: Every occurrence locator is bounded by its source byte count and
        exposes exactly the documented locator fields.
        """
        snapshot = self.compile_repository()

        assert set(snapshot.occurrences[0].locator.__dataclass_fields__) == {
            "source_path",
            "source_content_identity",
            "include_index",
            "byte_start",
            "byte_end",
            "line",
            "column",
        }
        assert all(
            occurrence.locator.byte_start
            < occurrence.locator.byte_end
            <= occurrence.locator.source_content_identity.byte_count
            for occurrence in snapshot.occurrences
        )
        assert all(
            not value.locator.source_path.startswith("/")
            for value in snapshot.occurrences
        )

    @staticmethod
    def compile_repository() -> ManuscriptCitationSnapshot:
        """Compile the current isolated worktree through the supported API."""
        repository_root = Path(__file__).resolve().parents[7]
        return (
            SUT()
            .execute(
                ResearchMonographCitationSnapshotRequest(repository_root.as_posix())
            )
            .snapshot
        )
