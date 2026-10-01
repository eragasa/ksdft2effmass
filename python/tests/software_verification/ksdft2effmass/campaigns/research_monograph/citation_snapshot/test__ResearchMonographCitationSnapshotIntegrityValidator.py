r"""Software verification of ``ResearchMonographCitationSnapshotIntegrityValidator``.

Evidence profile: routine

Bounded artifact scope: complete immutable owner Result identity replay, relation
closure, output bounds, and canonical projection size.

Facet and represented meaning

The validator proves internal software consistency for one already represented
citation snapshot and its durable request/result identities.

Intrinsic and cross-object scope

Evidence mutates public immutable records and passes them only through the supported
Result and validator APIs. It does not inspect private encoder state.

VVUQ and scientific exclusions

This is structural software verification only. It establishes no bibliography truth,
claim support, scientific validation, UQ, rights decision, or human acceptance.
"""

from dataclasses import replace
from pathlib import Path
from typing import Literal

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    ManuscriptCitationSnapshot,
    ResearchMonographCitationSnapshotCompiler,
    ResearchMonographCitationSnapshotIntegrityValidator,
    ResearchMonographCitationSnapshotRequest,
    ResearchMonographCitationSnapshotResult,
)

pytestmark = pytest.mark.software_verification
SUT = ResearchMonographCitationSnapshotIntegrityValidator

type RelationMutation = Literal[
    "missing_call_file",
    "duplicate_group_id",
    "wrong_group_entry",
    "fabricated_todo_links",
]
type IdentityFamily = Literal[
    "snapshot",
    "file",
    "source_content",
    "bibliography_content",
    "entry",
    "entry_content",
    "include",
    "call",
    "occurrence",
    "group",
    "todo",
    "gap",
]
type BoundaryFamily = Literal[
    "identifier", "citation_key", "path", "text", "source_bytes"
]
type CountBoundaryFamily = Literal[
    "source_files", "global_records", "per_record_references"
]


class TestResearchMonographCitationSnapshotIntegrityValidator:
    """Own software evidence for complete result integrity replay."""

    @pytest.mark.parametrize(
        "family",
        (
            pytest.param("missing_call_file", id="nonexistent_call_file"),
            pytest.param("duplicate_group_id", id="duplicate_group_identity"),
            pytest.param("wrong_group_entry", id="wrong_group_entry_binding"),
            pytest.param("fabricated_todo_links", id="fabricated_todo_links"),
        ),
    )
    def test_method__execute__rejects_forged_cross_record_relations(
        self, family: RelationMutation
    ) -> None:
        """Evidence ID: SV-CITATION-SNAPSHOT-INTEGRITY-001

        Requirement: A public Result must reject absent file lineage, duplicate group
        identity, a group bound to another key's entry, and fabricated marker links.

        Acceptance: Every independently constructible forged snapshot raises
        ValueError before a Result can be accepted.
        """
        result = self.compile_result()

        with pytest.raises(ValueError):
            forged = self.mutate_relation(result.snapshot, family)
            ResearchMonographCitationSnapshotResult(
                result.request_id, result.result_id, forged
            )

    @pytest.mark.parametrize(
        "family",
        (
            pytest.param("snapshot", id="snapshot"),
            pytest.param("file", id="source_file"),
            pytest.param("source_content", id="source_content"),
            pytest.param("bibliography_content", id="bibliography_content"),
            pytest.param("include", id="include_instance"),
            pytest.param("entry", id="bibliography_entry"),
            pytest.param("entry_content", id="entry_content"),
            pytest.param("call", id="citation_call"),
            pytest.param("occurrence", id="citation_occurrence"),
            pytest.param("group", id="citation_group"),
            pytest.param("todo", id="editorial_marker"),
            pytest.param("gap", id="source_gap"),
        ),
    )
    def test_method__execute__replays_every_snapshot_identity_family(
        self, family: IdentityFamily
    ) -> None:
        """Evidence ID: SV-CITATION-SNAPSHOT-INTEGRITY-002

        Requirement: Every owner-generated identity family must replay from its exact
        immutable semantic inputs rather than being accepted as an arbitrary string.

        Acceptance: Replacing one identity in each family with a well-formed opaque
        identity causes owner Result construction to raise ValueError.
        """
        result = self.compile_result()

        with pytest.raises(ValueError):
            forged = self.mutate_identity(result.snapshot, family)
            ResearchMonographCitationSnapshotResult(
                result.request_id, result.result_id, forged
            )

    @pytest.mark.parametrize(
        "family",
        (
            pytest.param("identifier", id="identifier_513_utf8_bytes"),
            pytest.param("citation_key", id="citation_key_201_ascii_characters"),
            pytest.param("path", id="path_4097_utf8_bytes"),
            pytest.param("text", id="text_4097_utf8_bytes"),
            pytest.param("source_bytes", id="source_100000001_bytes"),
        ),
    )
    def test_method__execute__rejects_scalar_boundary_plus_one(
        self, family: BoundaryFamily
    ) -> None:
        """Evidence ID: SV-CITATION-SNAPSHOT-INTEGRITY-003

        Requirement: Owner identifiers, paths, descriptive text, and represented
        source sizes must remain within the documented UTF-8 and byte bounds.

        Acceptance: Each exact maximum plus one is rejected by Result validation.
        """
        result = self.compile_result()

        with pytest.raises(ValueError):
            forged = self.mutate_boundary(result.snapshot, family)
            ResearchMonographCitationSnapshotResult(
                result.request_id, result.result_id, forged
            )

    @pytest.mark.parametrize(
        "family",
        (
            pytest.param("source_files", id="source_files_10001"),
            pytest.param("global_records", id="global_records_10001"),
            pytest.param("per_record_references", id="per_record_references_257"),
        ),
    )
    def test_method__execute__rejects_count_and_aggregate_boundary_plus_one(
        self, family: CountBoundaryFamily
    ) -> None:
        """Evidence ID: SV-CITATION-SNAPSHOT-INTEGRITY-004

        Requirement: Source-document, global-record, and per-record-reference
        bounds must reject their exact maximum plus one.

        Acceptance: Each boundary-plus-one snapshot raises ValueError during its
        intrinsic complete integrity replay.
        """
        result = self.compile_result()

        with pytest.raises(ValueError):
            self.mutate_count_boundary(result.snapshot, family)

    def test_method__execute__binds_complete_result_and_request_identities(
        self,
    ) -> None:
        """Evidence ID: SV-CITATION-SNAPSHOT-INTEGRITY-005

        Requirement: The durable request excludes the absolute root, while the Result
        identity binds that request to the complete replay-valid snapshot projection.

        Acceptance: Independent compilations have equal request/result identities,
        exact unversioned grammars, and reject a changed Result identity.
        """
        first = self.compile_result()
        second = self.compile_result()
        repository_root = Path(__file__).resolve().parents[7].as_posix()

        assert first.request_id == second.request_id
        assert first.result_id == second.result_id
        assert first.request_id.startswith("citation-request:")
        assert first.result_id.startswith("citation-result:")
        assert repository_root not in first.request_id
        assert repository_root not in first.result_id
        with pytest.raises(ValueError):
            replace(first, request_id="citation-request:" + "0" * 64)
        with pytest.raises(ValueError):
            replace(first, result_id="citation-result:" + "0" * 64)

    def test_method__execute__enforces_exact_size_boundaries(self) -> None:
        """Evidence ID: SV-CITATION-SNAPSHOT-INTEGRITY-006

        Requirement: The complete canonical owner projection must be bounded before
        its result identity is hashed.

        Acceptance: Exact aggregate-source and projection maxima are accepted and
        each maximum plus one is rejected.
        """
        SUT().validate_aggregate_source_size(100_000_000)
        SUT().validate_canonical_projection_size(20_000_000)

        with pytest.raises(ValueError):
            SUT().validate_aggregate_source_size(100_000_001)
        with pytest.raises(ValueError):
            SUT().validate_canonical_projection_size(20_000_001)

    @staticmethod
    def compile_result() -> ResearchMonographCitationSnapshotResult:
        """Compile the exact maintained repository through the public owner API."""
        repository_root = Path(__file__).resolve().parents[7]
        return ResearchMonographCitationSnapshotCompiler().execute(
            ResearchMonographCitationSnapshotRequest(repository_root.as_posix())
        )

    @staticmethod
    def mutate_relation(
        snapshot: ManuscriptCitationSnapshot, family: RelationMutation
    ) -> ManuscriptCitationSnapshot:
        """Construct one relation forgery that prior validation accepted."""
        if family == "missing_call_file":
            call = replace(snapshot.calls[0], file_id="citation-file:" + "0" * 64)
            return replace(snapshot, calls=(call, *snapshot.calls[1:]))
        if family == "duplicate_group_id":
            group = replace(snapshot.groups[1], group_id=snapshot.groups[0].group_id)
            return replace(
                snapshot, groups=(snapshot.groups[0], group, *snapshot.groups[2:])
            )
        if family == "wrong_group_entry":
            group = snapshot.groups[0]
            assert group.bibliography_entry_index is not None
            wrong_index = 1 if group.bibliography_entry_index == 0 else 0
            forged = replace(group, bibliography_entry_index=wrong_index)
            return replace(snapshot, groups=(forged, *snapshot.groups[1:]))
        todo = replace(
            snapshot.todos[0],
            generated_call_ids=("citation-call:" + "0" * 64,),
            generated_occurrence_ids=("citation-occurrence:" + "0" * 64,),
        )
        return replace(snapshot, todos=(todo, *snapshot.todos[1:]))

    @staticmethod
    def mutate_identity(
        snapshot: ManuscriptCitationSnapshot, family: IdentityFamily
    ) -> ManuscriptCitationSnapshot:
        """Replace exactly one identity in the selected owner family."""
        replacement = "0" * 64
        if family == "snapshot":
            return replace(snapshot, snapshot_id=f"citation-snapshot:{replacement}")
        if family == "file":
            source = replace(
                snapshot.source_files[1], file_id=f"citation-file:{replacement}"
            )
            return replace(
                snapshot,
                source_files=(
                    snapshot.source_files[0],
                    source,
                    *snapshot.source_files[2:],
                ),
            )
        if family == "source_content":
            source = replace(snapshot.source_files[1], sha256=replacement)
            return replace(
                snapshot,
                source_files=(
                    snapshot.source_files[0],
                    source,
                    *snapshot.source_files[2:],
                ),
            )
        if family == "bibliography_content":
            identity = replace(
                snapshot.bibliography_content_identity, digest=replacement
            )
            return replace(snapshot, bibliography_content_identity=identity)
        if family == "include":
            include = replace(
                snapshot.include_instances[-1],
                include_instance_id=f"citation-include:{replacement}",
            )
            return replace(
                snapshot,
                include_instances=(*snapshot.include_instances[:-1], include),
            )
        if family == "entry":
            entry = replace(
                snapshot.bibliography_entries[0],
                bibliography_entry_id=f"citation-entry:{replacement}",
            )
            return replace(
                snapshot,
                bibliography_entries=(entry, *snapshot.bibliography_entries[1:]),
            )
        if family == "entry_content":
            entry = snapshot.bibliography_entries[0]
            identity = replace(entry.entry_content_identity, digest=replacement)
            forged = replace(entry, entry_content_identity=identity)
            return replace(
                snapshot,
                bibliography_entries=(forged, *snapshot.bibliography_entries[1:]),
            )
        if family == "call":
            call = replace(snapshot.calls[0], call_id=f"citation-call:{replacement}")
            return replace(snapshot, calls=(call, *snapshot.calls[1:]))
        if family == "occurrence":
            occurrence = replace(
                snapshot.occurrences[0],
                occurrence_id=f"citation-occurrence:{replacement}",
            )
            return replace(
                snapshot, occurrences=(occurrence, *snapshot.occurrences[1:])
            )
        if family == "group":
            group = replace(
                snapshot.groups[0], group_id=f"citation-group:{replacement}"
            )
            return replace(snapshot, groups=(group, *snapshot.groups[1:]))
        if family == "todo":
            todo = replace(snapshot.todos[0], todo_id=f"citation-todo:{replacement}")
            return replace(snapshot, todos=(todo, *snapshot.todos[1:]))
        gap = replace(
            snapshot.source_gaps[0], source_gap_id=f"citation-gap:{replacement}"
        )
        return replace(snapshot, source_gaps=(gap, *snapshot.source_gaps[1:]))

    @staticmethod
    def mutate_count_boundary(
        snapshot: ManuscriptCitationSnapshot, family: CountBoundaryFamily
    ) -> ManuscriptCitationSnapshot:
        """Exceed one exact public collection or aggregate byte bound."""
        if family == "source_files":
            return replace(snapshot, source_files=snapshot.source_files[:1] * 10_001)
        if family == "global_records":
            return replace(snapshot, calls=snapshot.calls[:1] * 10_001)
        call = replace(snapshot.calls[0], occurrence_indexes=tuple(range(257)))
        return replace(snapshot, calls=(call, *snapshot.calls[1:]))

    @staticmethod
    def mutate_boundary(
        snapshot: ManuscriptCitationSnapshot, family: BoundaryFamily
    ) -> ManuscriptCitationSnapshot:
        """Exceed one exact public scalar bound while preserving constructibility."""
        if family == "identifier":
            return replace(snapshot, contract_id="i" * 513)
        if family == "citation_key":
            entry = replace(snapshot.bibliography_entries[0], key="k" * 201)
            return replace(
                snapshot,
                bibliography_entries=(entry, *snapshot.bibliography_entries[1:]),
            )
        if family == "path":
            source = replace(snapshot.source_files[1], source_path="p" * 4097)
            return replace(
                snapshot,
                source_files=(
                    snapshot.source_files[0],
                    source,
                    *snapshot.source_files[2:],
                ),
            )
        if family == "text":
            gap = replace(snapshot.source_gaps[0], placeholder_identifier="X" * 4097)
            return replace(snapshot, source_gaps=(gap, *snapshot.source_gaps[1:]))
        source = replace(snapshot.source_files[1], byte_size=100_000_001)
        return replace(
            snapshot,
            source_files=(
                snapshot.source_files[0],
                source,
                *snapshot.source_files[2:],
            ),
        )
