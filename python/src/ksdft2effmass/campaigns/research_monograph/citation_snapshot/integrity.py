"""Replay and bound the complete research-monograph citation result.

This module owns the single deterministic integrity path used both when the compiler
creates a result and whenever a result is constructed.  It validates all identities,
cross-record relations, source-size and record-count limits, and a canonical complete
snapshot projection before deriving the unversioned result identity.  It does not read
source files, mutate records, or establish bibliographic or scientific correctness.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .records import (
    CitationContentIdentity,
    ManuscriptBibliographyEntrySnapshot,
    ManuscriptCitationCall,
    ManuscriptCitationGroup,
    ManuscriptCitationOccurrence,
    ManuscriptCitationOrigin,
    ManuscriptCitationSnapshot,
    ManuscriptCitationSourceGap,
    ManuscriptCitationTodo,
    ManuscriptIncludeInstance,
    ManuscriptSourceFileSnapshot,
    ManuscriptSourceLocator,
)

CONTRACT_ID = "ksdft2effmass.research-monograph.citation-snapshot"
ENTRYPOINT_PATH = "docs/publications/research-monograph/manuscript.tex"
BIBLIOGRAPHY_PATH = "docs/publications/research-monograph/references.bib"
PARSER_IDENTITY = "ksdft2effmass.research-monograph.tex-biblatex-citation-parser"
GENERATOR_IDENTITY = "ksdft2effmass.research-monograph.citation-snapshot-compiler"

MAX_IDENTIFIER_UTF8_BYTES = 512
MAX_CITATION_KEY_ASCII_CHARACTERS = 200
MAX_TEXT_UTF8_BYTES = 4096
MAX_PATH_UTF8_BYTES = 4096
MAX_SOURCE_BYTES = 100_000_000
MAX_AGGREGATE_SOURCE_BYTES = 100_000_000
MAX_GLOBAL_RECORDS = 10_000
MAX_PER_RECORD_REFERENCES = 256
MAX_SOURCE_FILES = 10_000
MAX_CANONICAL_PROJECTION_BYTES = 20_000_000


type IdentityPart = str | int | None


@dataclass(frozen=True, slots=True)
class CitationIdentityGenerator:
    """Generate deterministic opaque identities from explicit semantic parts."""

    def execute(self, prefix: str, parts: tuple[IdentityPart, ...]) -> str:
        """Return a length-framed SHA-256 identity with an unversioned prefix."""
        if type(prefix) is not str or not prefix or prefix.endswith(":"):
            raise ValueError("identity prefix must be nonempty without trailing colon")
        if type(parts) is not tuple:
            raise TypeError("identity parts must be a tuple")
        digest = hashlib.sha256()
        digest.update(prefix.encode("utf-8"))
        for part in parts:
            if part is None:
                encoded = b""
                tag = b"n"
            elif type(part) is str:
                encoded = part.encode("utf-8")
                tag = b"s"
            elif type(part) is int:
                if part < 0:
                    raise ValueError("integer identity parts must be nonnegative")
                encoded = str(part).encode("ascii")
                tag = b"i"
            else:
                raise TypeError("identity parts must be str, int, or None")
            digest.update(tag)
            digest.update(len(encoded).to_bytes(8, "big"))
            digest.update(encoded)
        return f"{prefix}:{digest.hexdigest()}"


@dataclass(frozen=True, slots=True)
class ResearchMonographCitationSnapshotIntegrityValidator:
    """Validate and identify one complete owner result projection.

    The validator is the authoritative replay path for every identity-bearing record
    and every cross-record relation.  It also enforces the public output limits:
    identifiers are at most 512 UTF-8 bytes; citation keys match the ASCII grammar
    ``[A-Za-z0-9._-]{1,200}``; paths and descriptive text are at most 4096 UTF-8
    bytes; a source and all source bytes together are at most
    100,000,000 bytes; per-record references are at most 256; source files, global
    record families, and their aggregate are at most 10,000; and the complete canonical
    projection is at most 20,000,000 bytes before hashing.
    """

    def request_identity(self) -> str:
        """Return the durable request identity without the machine-local root path."""
        return CitationIdentityGenerator().execute(
            "citation-request", (CONTRACT_ID, ENTRYPOINT_PATH, BIBLIOGRAPHY_PATH)
        )

    def execute(self, snapshot: ManuscriptCitationSnapshot, request_id: str) -> str:
        """Validate ``snapshot`` completely and return its exact result identity.

        Parameters
        ----------
        snapshot
            Complete immutable owner snapshot.
        request_id
            Durable request identity.  The absolute repository root is intentionally
            excluded.

        Returns
        -------
        str
            ``citation-result:`` followed by 64 lowercase hexadecimal characters.

        Raises
        ------
        TypeError
            If either input has the wrong semantic type.
        ValueError
            If a bound, identity replay, or cross-record relation fails.
        """
        if type(snapshot) is not ManuscriptCitationSnapshot:
            raise TypeError("snapshot must be ManuscriptCitationSnapshot")
        self._require_identifier(request_id, "request_id")
        if request_id != self.request_identity():
            raise ValueError("request_id does not identify the canonical request")
        self._validate_bounds(snapshot)
        self._validate_relations_and_identities(snapshot)
        projection = self._canonical_projection(snapshot, request_id)
        self.validate_canonical_projection_size(len(projection))
        return f"citation-result:{hashlib.sha256(projection).hexdigest()}"

    def validate_canonical_projection_size(self, byte_count: int) -> None:
        """Require a canonical projection size from zero through 20,000,000 bytes."""
        if type(byte_count) is not int:
            raise TypeError("byte_count must be a built-in integer")
        if byte_count < 0 or byte_count > MAX_CANONICAL_PROJECTION_BYTES:
            raise ValueError("canonical projection exceeds 20,000,000 bytes")

    def validate_aggregate_source_size(self, byte_count: int) -> None:
        """Require aggregate consumed source size through 100,000,000 bytes."""
        if type(byte_count) is not int:
            raise TypeError("byte_count must be a built-in integer")
        if byte_count < 1 or byte_count > MAX_AGGREGATE_SOURCE_BYTES:
            raise ValueError("aggregate source bytes exceed 100,000,000")

    def _validate_bounds(self, snapshot: ManuscriptCitationSnapshot) -> None:
        for value, name in (
            (snapshot.contract_id, "contract_id"),
            (snapshot.snapshot_id, "snapshot_id"),
            (snapshot.repository_revision, "repository_revision"),
            (snapshot.parser_identity, "parser_identity"),
            (snapshot.generator_identity, "generator_identity"),
        ):
            self._require_identifier(value, name)
        self._require_path(snapshot.entrypoint_path, "entrypoint_path")
        self._require_path(snapshot.bibliography_path, "bibliography_path")
        self._require_source_size(
            snapshot.bibliography_content_identity.byte_count,
            "bibliography byte_count",
        )
        self._require_count(snapshot.source_files, MAX_SOURCE_FILES, "source_files")
        for values, name in (
            (snapshot.include_instances, "include_instances"),
            (snapshot.bibliography_entries, "bibliography_entries"),
            (snapshot.calls, "calls"),
            (snapshot.occurrences, "occurrences"),
            (snapshot.groups, "groups"),
            (snapshot.todos, "todos"),
            (snapshot.source_gaps, "source_gaps"),
            (snapshot.missing_keys, "missing_keys"),
            (snapshot.duplicate_keys, "duplicate_keys"),
            (snapshot.uncited_keys, "uncited_keys"),
        ):
            self._require_count(values, MAX_GLOBAL_RECORDS, name)
        global_count = sum(
            len(values)
            for values in (
                snapshot.source_files,
                snapshot.include_instances,
                snapshot.bibliography_entries,
                snapshot.calls,
                snapshot.occurrences,
                snapshot.groups,
                snapshot.todos,
                snapshot.source_gaps,
            )
        )
        if global_count > MAX_GLOBAL_RECORDS:
            raise ValueError("aggregate citation record count exceeds 10,000")
        aggregate_source_bytes = snapshot.bibliography_content_identity.byte_count
        for source in snapshot.source_files:
            self._require_identifier(source.file_id, "file_id")
            self._require_path(source.source_path, "source_path")
            self._require_monograph_source_path(source.source_path)
            self._require_source_size(source.byte_size, "source byte_size")
            aggregate_source_bytes += source.byte_size
        self.validate_aggregate_source_size(aggregate_source_bytes)
        for instance in snapshot.include_instances:
            self._require_identifier(
                instance.include_instance_id, "include_instance_id"
            )
            self._require_identifier(instance.child_file_id, "child_file_id")
            self._require_optional_identifier(instance.parent_file_id, "parent_file_id")
            self._require_optional_identifier(
                instance.parent_include_instance_id, "parent_include_instance_id"
            )
            self._require_path(instance.source_path, "include source_path")
            self._require_monograph_source_path(instance.source_path)
        for entry in snapshot.bibliography_entries:
            self._require_identifier(entry.bibliography_entry_id, "entry_id")
            self._require_citation_key(entry.key, "bibliography key")
            self._require_identifier(entry.entry_type, "entry_type")
            self._require_optional_identifier(
                entry.source_bibliography_observation_id,
                "source_bibliography_observation_id",
            )
            self._validate_locator_bounds(entry.locator)
        for call in snapshot.calls:
            self._require_identifier(call.call_id, "call_id")
            self._require_identifier(call.include_instance_id, "include_instance_id")
            self._require_identifier(call.file_id, "file_id")
            self._require_count(
                call.occurrence_indexes,
                MAX_PER_RECORD_REFERENCES,
                "call occurrence_indexes",
            )
            self._validate_locator_bounds(call.locator)
        for occurrence in snapshot.occurrences:
            self._require_identifier(occurrence.occurrence_id, "occurrence_id")
            self._require_citation_key(occurrence.key, "citation key")
            self._validate_locator_bounds(occurrence.locator)
        for group in snapshot.groups:
            self._require_identifier(group.group_id, "group_id")
            self._require_citation_key(group.key, "group key")
            self._require_count(
                group.occurrence_indexes,
                MAX_PER_RECORD_REFERENCES,
                "group occurrence_indexes",
            )
        for todo in snapshot.todos:
            self._require_identifier(todo.todo_id, "todo_id")
            self._require_count(
                todo.generated_call_ids,
                MAX_PER_RECORD_REFERENCES,
                "todo generated_call_ids",
            )
            self._require_count(
                todo.generated_occurrence_ids,
                MAX_PER_RECORD_REFERENCES,
                "todo generated_occurrence_ids",
            )
            for value in (*todo.generated_call_ids, *todo.generated_occurrence_ids):
                self._require_identifier(value, "todo generated identity")
            self._validate_locator_bounds(todo.locator)
            self._validate_locator_bounds(todo.priority_locator)
        for gap in snapshot.source_gaps:
            self._require_identifier(gap.source_gap_id, "source_gap_id")
            self._require_text(gap.placeholder_identifier, "placeholder_identifier")
            self._validate_locator_bounds(gap.locator)
        for key in (
            *snapshot.missing_keys,
            *snapshot.duplicate_keys,
            *snapshot.uncited_keys,
        ):
            self._require_citation_key(key, "closure key")

    def _validate_relations_and_identities(
        self, snapshot: ManuscriptCitationSnapshot
    ) -> None:
        if snapshot.contract_id != CONTRACT_ID:
            raise ValueError("snapshot contract_id is not canonical")
        if snapshot.entrypoint_path != ENTRYPOINT_PATH:
            raise ValueError("snapshot entrypoint_path is not canonical")
        if snapshot.bibliography_path != BIBLIOGRAPHY_PATH:
            raise ValueError("snapshot bibliography_path is not canonical")
        if snapshot.parser_identity != PARSER_IDENTITY:
            raise ValueError("snapshot parser_identity is not canonical")
        if snapshot.generator_identity != GENERATOR_IDENTITY:
            raise ValueError("snapshot generator_identity is not canonical")
        identities = CitationIdentityGenerator()
        expected_snapshot_id = self._snapshot_identity(snapshot, identities)
        if snapshot.snapshot_id != expected_snapshot_id:
            raise ValueError("snapshot_id does not replay from source lineage")

        self._require_contiguous(
            tuple(value.graph_order for value in snapshot.source_files), "source graph"
        )
        self._require_unique(
            tuple(value.source_path for value in snapshot.source_files), "source paths"
        )
        self._require_unique(
            tuple(value.file_id for value in snapshot.source_files), "file identities"
        )
        if not snapshot.source_files or not snapshot.include_instances:
            raise ValueError("snapshot requires a root source and include instance")
        source_by_id = {value.file_id: value for value in snapshot.source_files}
        source_by_path = {value.source_path: value for value in snapshot.source_files}
        for source in snapshot.source_files:
            expected = identities.execute(
                "citation-file", (source.source_path, source.sha256, source.byte_size)
            )
            if source.file_id != expected:
                raise ValueError("file_id does not replay from source lineage")
        if snapshot.source_files[0].source_path != ENTRYPOINT_PATH:
            raise ValueError("first source file is not the canonical entrypoint")

        self._require_contiguous(
            tuple(value.include_index for value in snapshot.include_instances),
            "include",
        )
        self._require_unique(
            tuple(value.include_instance_id for value in snapshot.include_instances),
            "include identities",
        )
        include_by_id = {
            value.include_instance_id: value for value in snapshot.include_instances
        }
        expected_ordinals: dict[str | None, int] = {None: 0}
        for instance in snapshot.include_instances:
            child = source_by_id.get(instance.child_file_id)
            if child is None or instance.source_path != child.source_path:
                raise ValueError("include child lineage is inconsistent")
            expected = identities.execute(
                "citation-include",
                (
                    instance.child_file_id,
                    instance.parent_include_instance_id,
                    instance.source_byte_start,
                    instance.source_byte_end,
                    instance.ordinal,
                    instance.depth,
                    instance.include_index,
                ),
            )
            if instance.include_instance_id != expected:
                raise ValueError("include_instance_id does not replay")
            parent_id = instance.parent_include_instance_id
            if instance.include_index == 0:
                if (
                    instance.parent_file_id is not None
                    or parent_id is not None
                    or instance.child_file_id != snapshot.source_files[0].file_id
                    or instance.source_byte_start != 0
                    or instance.source_byte_end != 0
                    or instance.ordinal != 0
                    or instance.depth != 0
                ):
                    raise ValueError("root include instance is inconsistent")
            else:
                parent = include_by_id.get(parent_id or "")
                if parent is None or parent.include_index >= instance.include_index:
                    raise ValueError("include parent must be an earlier instance")
                if instance.parent_file_id != parent.child_file_id:
                    raise ValueError("include parent file lineage is inconsistent")
                if instance.depth != parent.depth + 1:
                    raise ValueError("include depth is inconsistent")
                parent_source = source_by_id[parent.child_file_id]
                if (
                    instance.source_byte_start >= instance.source_byte_end
                    or instance.source_byte_end > parent_source.byte_size
                ):
                    raise ValueError("include source span is outside its parent source")
            expected_ordinal = expected_ordinals.get(parent_id, 0)
            if instance.ordinal != expected_ordinal:
                raise ValueError("include ordinals must be contiguous per parent")
            expected_ordinals[parent_id] = expected_ordinal + 1
        if set(source_by_id) != {
            value.child_file_id for value in snapshot.include_instances
        }:
            raise ValueError("every source file must have an include instance")

        self._require_contiguous(
            tuple(value.entry_index for value in snapshot.bibliography_entries), "entry"
        )
        self._require_unique(
            tuple(
                value.bibliography_entry_id for value in snapshot.bibliography_entries
            ),
            "bibliography entry identities",
        )
        self._require_unique(
            tuple(value.key for value in snapshot.bibliography_entries),
            "bibliography keys",
        )
        entry_by_key = {value.key: value for value in snapshot.bibliography_entries}
        for entry in snapshot.bibliography_entries:
            self._validate_bibliography_locator(snapshot, entry)
            if entry.entry_content_identity.byte_count != (
                entry.locator.byte_end - entry.locator.byte_start
            ):
                raise ValueError("entry content byte count does not match its span")
            if entry.source_bibliography_observation_id is not None:
                raise ValueError("owner result cannot assign a References observation")
            expected = identities.execute(
                "citation-entry",
                (
                    snapshot.snapshot_id,
                    entry.entry_index,
                    entry.key,
                    snapshot.bibliography_content_identity.digest,
                    entry.locator.byte_start,
                    entry.locator.byte_end,
                    entry.entry_content_identity.digest,
                ),
            )
            if entry.bibliography_entry_id != expected:
                raise ValueError("bibliography_entry_id does not replay")

        self._require_contiguous(
            tuple(value.call_index for value in snapshot.calls), "call"
        )
        self._require_unique(
            tuple(value.call_id for value in snapshot.calls), "call identities"
        )
        self._require_contiguous(
            tuple(value.occurrence_index for value in snapshot.occurrences),
            "occurrence",
        )
        self._require_unique(
            tuple(value.occurrence_id for value in snapshot.occurrences),
            "occurrence identities",
        )
        for occurrence in snapshot.occurrences:
            if occurrence.call_index >= len(snapshot.calls):
                raise ValueError("occurrence call index is outside calls")
        for call in snapshot.calls:
            if call.todo_marker_index is not None and call.todo_marker_index >= len(
                snapshot.todos
            ):
                raise ValueError("call todo marker index is outside todos")
            call_instance = include_by_id.get(call.include_instance_id)
            call_source = source_by_id.get(call.file_id)
            if (
                call_instance is None
                or call_source is None
                or call_instance.child_file_id != call.file_id
            ):
                raise ValueError("call source/include lineage is inconsistent")
            self._validate_manuscript_locator(call.locator, call_source, call_instance)
            expected_call = identities.execute(
                "citation-call",
                (
                    snapshot.snapshot_id,
                    call.include_instance_id,
                    call.locator.source_content_identity.digest,
                    call.locator.byte_start,
                    call.locator.byte_end,
                    call.command_kind.value,
                    call.origin.value,
                    call.call_index,
                ),
            )
            if call.call_id != expected_call:
                raise ValueError("call_id does not replay")
            selected = tuple(
                value
                for value in snapshot.occurrences
                if value.call_index == call.call_index
            )
            if call.occurrence_indexes != tuple(
                value.occurrence_index for value in selected
            ):
                raise ValueError("call occurrence indexes are inconsistent")
            if tuple(value.key_index for value in selected) != tuple(
                range(len(selected))
            ):
                raise ValueError("occurrence key indexes must be contiguous per call")
            for occurrence in selected:
                if occurrence.origin is not call.origin:
                    raise ValueError("call and occurrence origins disagree")
                if occurrence.todo_marker_index != call.todo_marker_index:
                    raise ValueError("call and occurrence todo bindings disagree")
                self._validate_manuscript_locator(
                    occurrence.locator, call_source, call_instance
                )
                if not (
                    call.locator.byte_start
                    <= occurrence.locator.byte_start
                    < occurrence.locator.byte_end
                    <= call.locator.byte_end
                ):
                    raise ValueError("occurrence span must lie within its call")
                bound_entry = entry_by_key.get(occurrence.key)
                expected_entry_index = (
                    None if bound_entry is None else bound_entry.entry_index
                )
                if occurrence.bibliography_entry_index != expected_entry_index:
                    raise ValueError("occurrence bibliography binding is inconsistent")
                expected_occurrence = identities.execute(
                    "citation-occurrence",
                    (
                        snapshot.snapshot_id,
                        call.include_instance_id,
                        occurrence.locator.source_content_identity.digest,
                        occurrence.locator.byte_start,
                        occurrence.locator.byte_end,
                        call.command_kind.value,
                        occurrence.key_index,
                        occurrence.origin.value,
                    ),
                )
                if occurrence.occurrence_id != expected_occurrence:
                    raise ValueError("occurrence_id does not replay")

        self._require_contiguous(
            tuple(value.group_index for value in snapshot.groups), "group"
        )
        self._require_unique(
            tuple(value.group_id for value in snapshot.groups), "group identities"
        )
        expected_group_keys = tuple(
            sorted({value.key for value in snapshot.occurrences})
        )
        if tuple(value.key for value in snapshot.groups) != expected_group_keys:
            raise ValueError("citation groups must be the sorted occurrence key set")
        for group in snapshot.groups:
            selected = tuple(
                value for value in snapshot.occurrences if value.key == group.key
            )
            if group.occurrence_indexes != tuple(
                value.occurrence_index for value in selected
            ):
                raise ValueError("group occurrence indexes are inconsistent")
            generated = sum(
                value.origin is ManuscriptCitationOrigin.CITATION_TODO_EXPANSION
                for value in selected
            )
            if group.generated_occurrence_count != generated or (
                group.direct_occurrence_count != len(selected) - generated
            ):
                raise ValueError("group origin counts are inconsistent")
            bound_entry = entry_by_key.get(group.key)
            expected_entry_index = (
                None if bound_entry is None else bound_entry.entry_index
            )
            if group.bibliography_entry_index != expected_entry_index:
                raise ValueError("group bibliography binding is inconsistent")
            expected = identities.execute(
                "citation-group", (snapshot.snapshot_id, group.key, group.group_index)
            )
            if group.group_id != expected:
                raise ValueError("group_id does not replay")

        self._require_contiguous(
            tuple(value.todo_marker_index for value in snapshot.todos), "todo"
        )
        self._require_unique(
            tuple(value.todo_id for value in snapshot.todos), "todo identities"
        )
        for todo in snapshot.todos:
            if todo.locator.include_index >= len(snapshot.include_instances):
                raise ValueError("todo include index is outside include instances")
            todo_source = source_by_path.get(todo.locator.source_path)
            if todo_source is None:
                raise ValueError("todo locator source is unknown")
            todo_instance = snapshot.include_instances[todo.locator.include_index]
            self._validate_manuscript_locator(todo.locator, todo_source, todo_instance)
            self._validate_manuscript_locator(
                todo.priority_locator, todo_source, todo_instance
            )
            if not (
                todo.locator.byte_start
                <= todo.priority_locator.byte_start
                < todo.priority_locator.byte_end
                <= todo.locator.byte_end
            ):
                raise ValueError("todo priority span must lie within the marker")
            generated_calls = tuple(
                value
                for value in snapshot.calls
                if value.todo_marker_index == todo.todo_marker_index
            )
            generated_occurrences = tuple(
                value
                for value in snapshot.occurrences
                if value.todo_marker_index == todo.todo_marker_index
            )
            if todo.generated_call_ids != tuple(
                value.call_id for value in generated_calls
            ) or todo.generated_occurrence_ids != tuple(
                value.occurrence_id for value in generated_occurrences
            ):
                raise ValueError("todo generated identity bindings are inconsistent")
            if len(generated_calls) != len(generated_occurrences):
                raise ValueError("each todo-generated call must own one occurrence")
            expected = identities.execute(
                "citation-todo",
                (
                    snapshot.snapshot_id,
                    todo.locator.source_content_identity.digest,
                    todo.locator.byte_start,
                    todo.locator.byte_end,
                    todo.priority.value,
                    todo.todo_marker_index,
                ),
            )
            if todo.todo_id != expected:
                raise ValueError("todo_id does not replay")

        self._require_contiguous(
            tuple(value.source_gap_index for value in snapshot.source_gaps),
            "source gap",
        )
        self._require_unique(
            tuple(value.source_gap_id for value in snapshot.source_gaps),
            "source-gap identities",
        )
        for gap in snapshot.source_gaps:
            if gap.locator.include_index >= len(snapshot.include_instances):
                raise ValueError(
                    "source-gap include index is outside include instances"
                )
            gap_source = source_by_path.get(gap.locator.source_path)
            if gap_source is None:
                raise ValueError("source-gap locator source is unknown")
            gap_instance = snapshot.include_instances[gap.locator.include_index]
            self._validate_manuscript_locator(gap.locator, gap_source, gap_instance)
            expected = identities.execute(
                "citation-gap",
                (
                    snapshot.snapshot_id,
                    gap.locator.source_content_identity.digest,
                    gap.locator.byte_start,
                    gap.locator.byte_end,
                    gap.reason.value,
                    gap.source_gap_index,
                ),
            )
            if gap.source_gap_id != expected:
                raise ValueError("source_gap_id does not replay")

        expected_missing = tuple(
            sorted(
                value.key
                for value in snapshot.groups
                if value.bibliography_entry_index is None
            )
        )
        if snapshot.missing_keys != expected_missing:
            raise ValueError("missing_keys do not replay")
        if snapshot.duplicate_keys:
            raise ValueError("successful snapshots cannot contain duplicate keys")
        expected_uncited = tuple(
            sorted(set(entry_by_key) - {value.key for value in snapshot.groups})
        )
        if snapshot.uncited_keys != expected_uncited:
            raise ValueError("uncited_keys do not replay")

    def _snapshot_identity(
        self,
        snapshot: ManuscriptCitationSnapshot,
        identities: CitationIdentityGenerator,
    ) -> str:
        parts: list[IdentityPart] = [
            snapshot.contract_id,
            snapshot.repository_revision,
            snapshot.entrypoint_path,
            snapshot.bibliography_path,
            snapshot.parser_identity,
            snapshot.generator_identity,
        ]
        for source in snapshot.source_files:
            parts.extend(
                (
                    source.source_path,
                    source.byte_size,
                    source.sha256,
                    source.graph_order,
                )
            )
        parts.extend(
            (
                snapshot.bibliography_path,
                snapshot.bibliography_content_identity.byte_count,
                snapshot.bibliography_content_identity.digest,
            )
        )
        return identities.execute("citation-snapshot", tuple(parts))

    def _validate_bibliography_locator(
        self,
        snapshot: ManuscriptCitationSnapshot,
        entry: ManuscriptBibliographyEntrySnapshot,
    ) -> None:
        locator = entry.locator
        if (
            locator.source_path != snapshot.bibliography_path
            or locator.source_content_identity != snapshot.bibliography_content_identity
            or locator.include_index != 0
            or locator.byte_start >= locator.byte_end
        ):
            raise ValueError("bibliography locator lineage is inconsistent")

    def _validate_manuscript_locator(
        self,
        locator: ManuscriptSourceLocator,
        source: ManuscriptSourceFileSnapshot,
        instance: ManuscriptIncludeInstance,
    ) -> None:
        if (
            locator.source_path != source.source_path
            or locator.source_content_identity != source.content_identity
            or locator.include_index != instance.include_index
            or instance.child_file_id != source.file_id
            or locator.byte_start >= locator.byte_end
            or locator.line > source.byte_size + 1
            or locator.column > source.byte_size + 1
        ):
            raise ValueError("manuscript locator lineage is inconsistent")

    def _canonical_projection(
        self, snapshot: ManuscriptCitationSnapshot, request_id: str
    ) -> bytes:
        buffer = bytearray(b"citation-result-projection\x00")
        self._append_text(buffer, "request_id", request_id)
        self._append_text(buffer, "contract_id", snapshot.contract_id)
        self._append_text(buffer, "snapshot_id", snapshot.snapshot_id)
        self._append_text(buffer, "repository_revision", snapshot.repository_revision)
        self._append_text(buffer, "entrypoint_path", snapshot.entrypoint_path)
        self._append_text(buffer, "bibliography_path", snapshot.bibliography_path)
        self._append_text(buffer, "parser_identity", snapshot.parser_identity)
        self._append_text(buffer, "generator_identity", snapshot.generator_identity)
        self._append_content_identity(
            buffer,
            "bibliography_content_identity",
            snapshot.bibliography_content_identity,
        )
        self._append_sequence(buffer, "source_files", len(snapshot.source_files))
        for source_value in snapshot.source_files:
            self._append_source_file(buffer, source_value)
        self._append_sequence(
            buffer, "include_instances", len(snapshot.include_instances)
        )
        for include_value in snapshot.include_instances:
            self._append_include(buffer, include_value)
        self._append_sequence(
            buffer, "bibliography_entries", len(snapshot.bibliography_entries)
        )
        for entry_value in snapshot.bibliography_entries:
            self._append_entry(buffer, entry_value)
        self._append_sequence(buffer, "calls", len(snapshot.calls))
        for call_value in snapshot.calls:
            self._append_call(buffer, call_value)
        self._append_sequence(buffer, "occurrences", len(snapshot.occurrences))
        for occurrence_value in snapshot.occurrences:
            self._append_occurrence(buffer, occurrence_value)
        self._append_sequence(buffer, "groups", len(snapshot.groups))
        for group_value in snapshot.groups:
            self._append_group(buffer, group_value)
        self._append_sequence(buffer, "todos", len(snapshot.todos))
        for todo_value in snapshot.todos:
            self._append_todo(buffer, todo_value)
        self._append_sequence(buffer, "source_gaps", len(snapshot.source_gaps))
        for gap_value in snapshot.source_gaps:
            self._append_gap(buffer, gap_value)
        self._append_text_tuple(buffer, "missing_keys", snapshot.missing_keys)
        self._append_text_tuple(buffer, "duplicate_keys", snapshot.duplicate_keys)
        self._append_text_tuple(buffer, "uncited_keys", snapshot.uncited_keys)
        return bytes(buffer)

    def _append_source_file(
        self, buffer: bytearray, value: ManuscriptSourceFileSnapshot
    ) -> None:
        self._append_text(buffer, "file_id", value.file_id)
        self._append_text(buffer, "source_path", value.source_path)
        self._append_int(buffer, "byte_size", value.byte_size)
        self._append_text(buffer, "sha256", value.sha256)
        self._append_int(buffer, "graph_order", value.graph_order)

    def _append_include(
        self, buffer: bytearray, value: ManuscriptIncludeInstance
    ) -> None:
        self._append_text(buffer, "include_instance_id", value.include_instance_id)
        self._append_int(buffer, "include_index", value.include_index)
        self._append_optional_text(buffer, "parent_file_id", value.parent_file_id)
        self._append_optional_text(
            buffer, "parent_include_instance_id", value.parent_include_instance_id
        )
        self._append_text(buffer, "child_file_id", value.child_file_id)
        self._append_text(buffer, "source_path", value.source_path)
        self._append_int(buffer, "source_byte_start", value.source_byte_start)
        self._append_int(buffer, "source_byte_end", value.source_byte_end)
        self._append_int(buffer, "ordinal", value.ordinal)
        self._append_int(buffer, "depth", value.depth)

    def _append_entry(
        self, buffer: bytearray, value: ManuscriptBibliographyEntrySnapshot
    ) -> None:
        self._append_text(buffer, "bibliography_entry_id", value.bibliography_entry_id)
        self._append_int(buffer, "entry_index", value.entry_index)
        self._append_text(buffer, "key", value.key)
        self._append_text(buffer, "entry_type", value.entry_type)
        self._append_locator(buffer, "locator", value.locator)
        self._append_content_identity(
            buffer, "entry_content_identity", value.entry_content_identity
        )
        self._append_optional_text(
            buffer,
            "source_bibliography_observation_id",
            value.source_bibliography_observation_id,
        )

    def _append_call(self, buffer: bytearray, value: ManuscriptCitationCall) -> None:
        self._append_text(buffer, "call_id", value.call_id)
        self._append_int(buffer, "call_index", value.call_index)
        self._append_text(buffer, "include_instance_id", value.include_instance_id)
        self._append_text(buffer, "file_id", value.file_id)
        self._append_text(buffer, "command_kind", value.command_kind.value)
        self._append_text(buffer, "origin", value.origin.value)
        self._append_locator(buffer, "locator", value.locator)
        self._append_int_tuple(buffer, "occurrence_indexes", value.occurrence_indexes)
        self._append_optional_int(buffer, "todo_marker_index", value.todo_marker_index)

    def _append_occurrence(
        self, buffer: bytearray, value: ManuscriptCitationOccurrence
    ) -> None:
        self._append_text(buffer, "occurrence_id", value.occurrence_id)
        self._append_int(buffer, "occurrence_index", value.occurrence_index)
        self._append_int(buffer, "call_index", value.call_index)
        self._append_int(buffer, "key_index", value.key_index)
        self._append_text(buffer, "key", value.key)
        self._append_text(buffer, "origin", value.origin.value)
        self._append_locator(buffer, "locator", value.locator)
        self._append_optional_int(
            buffer, "bibliography_entry_index", value.bibliography_entry_index
        )
        self._append_optional_int(buffer, "todo_marker_index", value.todo_marker_index)

    def _append_group(self, buffer: bytearray, value: ManuscriptCitationGroup) -> None:
        self._append_text(buffer, "group_id", value.group_id)
        self._append_int(buffer, "group_index", value.group_index)
        self._append_text(buffer, "key", value.key)
        self._append_int_tuple(buffer, "occurrence_indexes", value.occurrence_indexes)
        self._append_int(
            buffer, "direct_occurrence_count", value.direct_occurrence_count
        )
        self._append_int(
            buffer, "generated_occurrence_count", value.generated_occurrence_count
        )
        self._append_optional_int(
            buffer, "bibliography_entry_index", value.bibliography_entry_index
        )

    def _append_todo(self, buffer: bytearray, value: ManuscriptCitationTodo) -> None:
        self._append_text(buffer, "todo_id", value.todo_id)
        self._append_int(buffer, "todo_marker_index", value.todo_marker_index)
        self._append_locator(buffer, "locator", value.locator)
        self._append_locator(buffer, "priority_locator", value.priority_locator)
        self._append_text(buffer, "priority", value.priority.value)
        self._append_text_tuple(buffer, "generated_call_ids", value.generated_call_ids)
        self._append_text_tuple(
            buffer, "generated_occurrence_ids", value.generated_occurrence_ids
        )

    def _append_gap(
        self, buffer: bytearray, value: ManuscriptCitationSourceGap
    ) -> None:
        self._append_text(buffer, "source_gap_id", value.source_gap_id)
        self._append_int(buffer, "source_gap_index", value.source_gap_index)
        self._append_locator(buffer, "locator", value.locator)
        self._append_text(buffer, "reason", value.reason.value)
        self._append_text(
            buffer, "placeholder_identifier", value.placeholder_identifier
        )

    def _append_locator(
        self, buffer: bytearray, label: str, value: ManuscriptSourceLocator
    ) -> None:
        self._append_text(buffer, "locator_label", label)
        self._append_text(buffer, "source_path", value.source_path)
        self._append_content_identity(
            buffer, "source_content_identity", value.source_content_identity
        )
        self._append_int(buffer, "include_index", value.include_index)
        self._append_int(buffer, "byte_start", value.byte_start)
        self._append_int(buffer, "byte_end", value.byte_end)
        self._append_int(buffer, "line", value.line)
        self._append_int(buffer, "column", value.column)

    def _append_content_identity(
        self, buffer: bytearray, label: str, value: CitationContentIdentity
    ) -> None:
        self._append_text(buffer, "content_identity_label", label)
        self._append_text(buffer, "algorithm", value.algorithm.value)
        self._append_text(buffer, "digest", value.digest)
        self._append_int(buffer, "byte_count", value.byte_count)

    def _append_text_tuple(
        self, buffer: bytearray, label: str, values: tuple[str, ...]
    ) -> None:
        self._append_sequence(buffer, label, len(values))
        for value in values:
            self._append_text(buffer, "item", value)

    def _append_int_tuple(
        self, buffer: bytearray, label: str, values: tuple[int, ...]
    ) -> None:
        self._append_sequence(buffer, label, len(values))
        for value in values:
            self._append_int(buffer, "item", value)

    def _append_sequence(self, buffer: bytearray, label: str, count: int) -> None:
        self._append_field(buffer, b"q", label, str(count).encode("ascii"))

    def _append_text(self, buffer: bytearray, label: str, value: str) -> None:
        self._append_field(buffer, b"s", label, value.encode("utf-8"))

    def _append_optional_text(
        self, buffer: bytearray, label: str, value: str | None
    ) -> None:
        if value is None:
            self._append_field(buffer, b"n", label, b"")
        else:
            self._append_text(buffer, label, value)

    def _append_int(self, buffer: bytearray, label: str, value: int) -> None:
        self._append_field(buffer, b"i", label, str(value).encode("ascii"))

    def _append_optional_int(
        self, buffer: bytearray, label: str, value: int | None
    ) -> None:
        if value is None:
            self._append_field(buffer, b"n", label, b"")
        else:
            self._append_int(buffer, label, value)

    def _append_field(
        self, buffer: bytearray, tag: bytes, label: str, encoded: bytes
    ) -> None:
        label_bytes = label.encode("ascii")
        buffer.extend(tag)
        buffer.extend(len(label_bytes).to_bytes(2, "big"))
        buffer.extend(label_bytes)
        buffer.extend(len(encoded).to_bytes(8, "big"))
        buffer.extend(encoded)
        if len(buffer) > MAX_CANONICAL_PROJECTION_BYTES:
            raise ValueError("canonical projection exceeds 20,000,000 bytes")

    def _validate_locator_bounds(self, locator: ManuscriptSourceLocator) -> None:
        self._require_path(locator.source_path, "locator source_path")
        self._require_source_size(
            locator.source_content_identity.byte_count,
            "locator source byte_count",
        )
        if locator.line > MAX_SOURCE_BYTES + 1 or locator.column > MAX_SOURCE_BYTES + 1:
            raise ValueError("locator line or column exceeds source bounds")

    @staticmethod
    def _require_contiguous(values: tuple[int, ...], label: str) -> None:
        if values != tuple(range(len(values))):
            raise ValueError(f"{label} indexes must be contiguous from zero")

    @staticmethod
    def _require_unique(values: tuple[str, ...], label: str) -> None:
        if len(set(values)) != len(values):
            raise ValueError(f"{label} must be unique")

    @staticmethod
    def _require_count[T](values: tuple[T, ...], maximum: int, label: str) -> None:
        if len(values) > maximum:
            raise ValueError(f"{label} exceeds its maximum count")

    def _require_identifier(self, value: str, label: str) -> None:
        self._require_utf8(value, MAX_IDENTIFIER_UTF8_BYTES, label)

    @staticmethod
    def _require_citation_key(value: str, label: str) -> None:
        if type(value) is not str:
            raise TypeError(f"{label} must be a string")
        allowed = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-"
        if (
            not value
            or len(value) > MAX_CITATION_KEY_ASCII_CHARACTERS
            or any(character not in allowed for character in value)
        ):
            raise ValueError(f"{label} must match ASCII [A-Za-z0-9._-]{{1,200}}")

    def _require_optional_identifier(self, value: str | None, label: str) -> None:
        if value is not None:
            self._require_identifier(value, label)

    def _require_text(self, value: str, label: str) -> None:
        self._require_utf8(value, MAX_TEXT_UTF8_BYTES, label)

    def _require_path(self, value: str, label: str) -> None:
        self._require_utf8(value, MAX_PATH_UTF8_BYTES, label)

    @staticmethod
    def _require_monograph_source_path(value: str) -> None:
        parts = value.split("/")
        if (
            not value.startswith("docs/publications/research-monograph/")
            or value.startswith("/")
            or "\\" in value
            or any(part in {"", ".", ".."} for part in parts)
        ):
            raise ValueError(
                "source paths must be normalized within the monograph directory"
            )

    @staticmethod
    def _require_utf8(value: str, maximum: int, label: str) -> None:
        if type(value) is not str:
            raise TypeError(f"{label} must be a string")
        if not value or len(value.encode("utf-8")) > maximum:
            raise ValueError(f"{label} is empty or exceeds its UTF-8 byte limit")

    @staticmethod
    def _require_source_size(value: int, label: str) -> None:
        if type(value) is not int:
            raise TypeError(f"{label} must be a built-in integer")
        if value < 1 or value > MAX_SOURCE_BYTES:
            raise ValueError(f"{label} must be from 1 through 100,000,000")
