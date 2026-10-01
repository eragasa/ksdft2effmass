"""Immutable records for one exact research-monograph citation snapshot.

The records represent source and bibliography structure only. They contain no
manuscript excerpts, rights or use decisions, external ingestion state, scholarly
acceptance, or References-owned observation identities unless a later independent
binding explicitly supplies one.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class CitationContentAlgorithm(StrEnum):
    """Supported exact source-content digest algorithms."""

    SHA256 = "sha256"


class ManuscriptCitationCommandKind(StrEnum):
    """Rendered citation command kinds supported by the monograph contract."""

    CITE = "cite"
    EQINCITE = "eqincite"


class ManuscriptCitationOrigin(StrEnum):
    """Source construct responsible for one rendered citation occurrence."""

    DIRECT = "direct"
    EQINCITE_EXPANSION = "eqincite_expansion"
    CITATION_TODO_EXPANSION = "citation_todo_expansion"


class ManuscriptCitationPriority(StrEnum):
    """Editorial priority encoded by ``citationtodo`` markers."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ManuscriptCitationSourceGapReason(StrEnum):
    """Closed reasons for a source gap without an invented citation key."""

    PLACEHOLDER_IDENTIFIER = "placeholder_identifier"


class CitationSnapshotErrorCode(StrEnum):
    """Fail-closed citation snapshot error codes."""

    INVALID_REQUEST = "invalid_request"
    REPOSITORY_REVISION_UNAVAILABLE = "repository_revision_unavailable"
    SOURCE_MISSING = "source_missing"
    SOURCE_NOT_UTF8 = "source_not_utf8"
    PATH_ESCAPE = "path_escape"
    INCLUDE_CYCLE = "include_cycle"
    MALFORMED_TEX = "malformed_tex"
    UNKNOWN_CITATION_MACRO = "unknown_citation_macro"
    UNSAFE_DEFINITION = "unsafe_definition"
    BIBLIOGRAPHY_DUPLICATE_KEY = "bibliography_duplicate_key"
    MALFORMED_BIBLIOGRAPHY = "malformed_bibliography"


@dataclass(frozen=True, slots=True)
class CitationSnapshotError(Exception):
    """Represent one fail-closed structural citation extraction failure.

    Parameters
    ----------
    code
        Stable failure classification.
    source_path
        Root-relative source path when a source was identified, otherwise ``None``.
    byte_offset
        Zero-based UTF-8 byte offset when identified, otherwise ``None``.
    detail
        Sanitized diagnostic without manuscript or bibliography excerpts.
    """

    code: CitationSnapshotErrorCode
    source_path: str | None
    byte_offset: int | None
    detail: str

    def __post_init__(self) -> None:
        if type(self.code) is not CitationSnapshotErrorCode:
            raise TypeError("code must be CitationSnapshotErrorCode")
        if self.source_path is not None and (
            type(self.source_path) is not str or not self.source_path
        ):
            raise TypeError("source_path must be a nonempty string or None")
        if self.byte_offset is not None and (
            type(self.byte_offset) is not int or self.byte_offset < 0
        ):
            raise TypeError("byte_offset must be a nonnegative integer or None")
        if type(self.detail) is not str or not self.detail:
            raise TypeError("detail must be a nonempty string")
        Exception.__init__(self, f"{self.code.value}: {self.detail}")


@dataclass(frozen=True, slots=True)
class CitationContentIdentity:
    """Identify exact immutable bytes without assigning a domain observation ID.

    Parameters
    ----------
    algorithm
        Digest algorithm. The unversioned contract currently accepts SHA-256 only.
    digest
        Lowercase hexadecimal digest.
    byte_count
        Exact number of bytes represented by the digest.
    """

    algorithm: CitationContentAlgorithm
    digest: str
    byte_count: int

    def __post_init__(self) -> None:
        if type(self.algorithm) is not CitationContentAlgorithm:
            raise TypeError("algorithm must be CitationContentAlgorithm")
        if (
            type(self.digest) is not str
            or len(self.digest) != 64
            or any(character not in "0123456789abcdef" for character in self.digest)
        ):
            raise ValueError("digest must be 64 lowercase hexadecimal characters")
        if type(self.byte_count) is not int or self.byte_count < 0:
            raise ValueError("byte_count must be a nonnegative built-in integer")


@dataclass(frozen=True, slots=True)
class ManuscriptSourceLocator:
    """Locate a construct without retaining an excerpt.

    Parameters
    ----------
    source_path
        POSIX path relative to the repository root.
    source_content_identity
        Identity of the complete source file.
    include_index
        Zero-based include-instance order.
    byte_start, byte_end
        Half-open UTF-8 byte span in the exact source bytes.
    line, column
        One-based display location of ``byte_start``.
    """

    source_path: str
    source_content_identity: CitationContentIdentity
    include_index: int
    byte_start: int
    byte_end: int
    line: int
    column: int

    def __post_init__(self) -> None:
        if type(self.source_path) is not str or not self.source_path:
            raise TypeError("source_path must be a nonempty string")
        if self.source_path.startswith("/") or ".." in self.source_path.split("/"):
            raise ValueError("source_path must be a root-relative POSIX path")
        if type(self.source_content_identity) is not CitationContentIdentity:
            raise TypeError("source_content_identity must be CitationContentIdentity")
        for value, name in (
            (self.include_index, "include_index"),
            (self.byte_start, "byte_start"),
            (self.byte_end, "byte_end"),
        ):
            if type(value) is not int or value < 0:
                raise ValueError(f"{name} must be a nonnegative built-in integer")
        if self.byte_end < self.byte_start:
            raise ValueError("byte_end must not precede byte_start")
        if self.byte_end > self.source_content_identity.byte_count:
            raise ValueError("locator span must lie within source bytes")
        for value, name in ((self.line, "line"), (self.column, "column")):
            if type(value) is not int or value < 1:
                raise ValueError(f"{name} must be a positive built-in integer")


@dataclass(frozen=True, slots=True)
class ManuscriptSourceFileSnapshot:
    """Retain exact identity and graph order for one unique TeX source file."""

    file_id: str
    source_path: str
    byte_size: int
    sha256: str
    graph_order: int

    def __post_init__(self) -> None:
        for value, name in (
            (self.file_id, "file_id"),
            (self.source_path, "source_path"),
        ):
            if type(value) is not str or not value:
                raise TypeError(f"{name} must be a nonempty string")
        CitationContentIdentity(
            CitationContentAlgorithm.SHA256, self.sha256, self.byte_size
        )
        if type(self.graph_order) is not int or self.graph_order < 0:
            raise ValueError("graph_order must be nonnegative")

    @property
    def content_identity(self) -> CitationContentIdentity:
        """Return the structured identity of the complete source bytes."""
        return CitationContentIdentity(
            CitationContentAlgorithm.SHA256, self.sha256, self.byte_size
        )


@dataclass(frozen=True, slots=True)
class ManuscriptIncludeInstance:
    """Represent one root or included-file instance in deterministic graph order."""

    include_instance_id: str
    include_index: int
    parent_file_id: str | None
    parent_include_instance_id: str | None
    child_file_id: str
    source_path: str
    source_byte_start: int
    source_byte_end: int
    ordinal: int
    depth: int

    def __post_init__(self) -> None:
        for text_value, name in (
            (self.include_instance_id, "include_instance_id"),
            (self.child_file_id, "child_file_id"),
            (self.source_path, "source_path"),
        ):
            if type(text_value) is not str or not text_value:
                raise TypeError(f"{name} must be a nonempty string")
        for numeric_value, name in (
            (self.include_index, "include_index"),
            (self.source_byte_start, "source_byte_start"),
            (self.source_byte_end, "source_byte_end"),
            (self.ordinal, "ordinal"),
            (self.depth, "depth"),
        ):
            if type(numeric_value) is not int or numeric_value < 0:
                raise ValueError(f"{name} must be nonnegative")
        if self.source_byte_end < self.source_byte_start:
            raise ValueError("source include span is reversed")
        root = self.parent_file_id is None and self.parent_include_instance_id is None
        if root:
            if self.depth != 0 or self.include_index != 0:
                raise ValueError("root include instance must have zero depth and index")
        elif self.parent_file_id is None or self.parent_include_instance_id is None:
            raise ValueError("nonroot include instance requires both parent identities")


@dataclass(frozen=True, slots=True)
class ManuscriptBibliographyEntrySnapshot:
    """Retain one exact BibLaTeX entry without source prose.

    ``source_bibliography_observation_id`` is reserved for an independent exact
    References binding. This package always emits ``None`` and never fabricates it.
    """

    bibliography_entry_id: str
    entry_index: int
    key: str
    entry_type: str
    locator: ManuscriptSourceLocator
    entry_content_identity: CitationContentIdentity
    source_bibliography_observation_id: str | None

    def __post_init__(self) -> None:
        for value, name in (
            (self.bibliography_entry_id, "bibliography_entry_id"),
            (self.key, "key"),
            (self.entry_type, "entry_type"),
        ):
            if type(value) is not str or not value:
                raise TypeError(f"{name} must be a nonempty string")
        if type(self.entry_index) is not int or self.entry_index < 0:
            raise ValueError("entry_index must be nonnegative")
        if type(self.locator) is not ManuscriptSourceLocator:
            raise TypeError("locator must be ManuscriptSourceLocator")
        if type(self.entry_content_identity) is not CitationContentIdentity:
            raise TypeError("entry_content_identity must be CitationContentIdentity")
        if self.source_bibliography_observation_id is not None and (
            type(self.source_bibliography_observation_id) is not str
            or not self.source_bibliography_observation_id
        ):
            raise TypeError(
                "source_bibliography_observation_id must be nonempty or None"
            )

    @property
    def entry_id(self) -> str:
        """Return the target-owned bibliography entry identity."""
        return self.bibliography_entry_id


@dataclass(frozen=True, slots=True)
class ManuscriptCitationCall:
    """Represent one rendered citation call and its ordered key occurrences."""

    call_id: str
    call_index: int
    include_instance_id: str
    file_id: str
    command_kind: ManuscriptCitationCommandKind
    origin: ManuscriptCitationOrigin
    locator: ManuscriptSourceLocator
    occurrence_indexes: tuple[int, ...]
    todo_marker_index: int | None

    def __post_init__(self) -> None:
        for value, name in (
            (self.call_id, "call_id"),
            (self.include_instance_id, "include_instance_id"),
            (self.file_id, "file_id"),
        ):
            if type(value) is not str or not value:
                raise TypeError(f"{name} must be a nonempty string")
        if type(self.call_index) is not int or self.call_index < 0:
            raise ValueError("call_index must be nonnegative")
        if type(self.command_kind) is not ManuscriptCitationCommandKind:
            raise TypeError("command_kind must be ManuscriptCitationCommandKind")
        if type(self.origin) is not ManuscriptCitationOrigin:
            raise TypeError("origin must be ManuscriptCitationOrigin")
        if type(self.locator) is not ManuscriptSourceLocator:
            raise TypeError("locator must be ManuscriptSourceLocator")
        if type(self.occurrence_indexes) is not tuple or not self.occurrence_indexes:
            raise TypeError("occurrence_indexes must be a nonempty tuple")
        if tuple(sorted(set(self.occurrence_indexes))) != self.occurrence_indexes:
            raise ValueError("occurrence_indexes must be sorted and unique")
        if self.todo_marker_index is not None and (
            type(self.todo_marker_index) is not int or self.todo_marker_index < 0
        ):
            raise ValueError("todo_marker_index must be nonnegative or None")
        generated = self.origin is ManuscriptCitationOrigin.CITATION_TODO_EXPANSION
        if generated != (self.todo_marker_index is not None):
            raise ValueError("todo binding must agree with citation origin")


@dataclass(frozen=True, slots=True)
class ManuscriptCitationOccurrence:
    """Represent one exact citation key token within one rendered call."""

    occurrence_id: str
    occurrence_index: int
    call_index: int
    key_index: int
    key: str
    origin: ManuscriptCitationOrigin
    locator: ManuscriptSourceLocator
    bibliography_entry_index: int | None
    todo_marker_index: int | None

    def __post_init__(self) -> None:
        if type(self.occurrence_id) is not str or not self.occurrence_id:
            raise TypeError("occurrence_id must be nonempty")
        for value, name in (
            (self.occurrence_index, "occurrence_index"),
            (self.call_index, "call_index"),
            (self.key_index, "key_index"),
        ):
            if type(value) is not int or value < 0:
                raise ValueError(f"{name} must be nonnegative")
        if type(self.key) is not str or not self.key:
            raise TypeError("key must be nonempty")
        if type(self.origin) is not ManuscriptCitationOrigin:
            raise TypeError("origin must be ManuscriptCitationOrigin")
        if type(self.locator) is not ManuscriptSourceLocator:
            raise TypeError("locator must be ManuscriptSourceLocator")
        for optional_index, name in (
            (self.bibliography_entry_index, "bibliography_entry_index"),
            (self.todo_marker_index, "todo_marker_index"),
        ):
            if optional_index is not None and (
                type(optional_index) is not int or optional_index < 0
            ):
                raise ValueError(f"{name} must be nonnegative or None")
        generated = self.origin is ManuscriptCitationOrigin.CITATION_TODO_EXPANSION
        if generated != (self.todo_marker_index is not None):
            raise ValueError("todo binding must agree with citation origin")

    @property
    def literal_citekey(self) -> str:
        """Return the exact case-sensitive citation key token."""
        return self.key


@dataclass(frozen=True, slots=True)
class ManuscriptCitationGroup:
    """Group every occurrence of one exact case-sensitive citation key."""

    group_id: str
    group_index: int
    key: str
    occurrence_indexes: tuple[int, ...]
    direct_occurrence_count: int
    generated_occurrence_count: int
    bibliography_entry_index: int | None

    def __post_init__(self) -> None:
        if type(self.group_id) is not str or not self.group_id:
            raise TypeError("group_id must be nonempty")
        if type(self.group_index) is not int or self.group_index < 0:
            raise ValueError("group_index must be nonnegative")
        if type(self.key) is not str or not self.key:
            raise TypeError("key must be nonempty")
        if type(self.occurrence_indexes) is not tuple or not self.occurrence_indexes:
            raise TypeError("occurrence_indexes must be a nonempty tuple")
        if tuple(sorted(set(self.occurrence_indexes))) != self.occurrence_indexes:
            raise ValueError("occurrence_indexes must be sorted and unique")
        for value, name in (
            (self.direct_occurrence_count, "direct_occurrence_count"),
            (self.generated_occurrence_count, "generated_occurrence_count"),
        ):
            if type(value) is not int or value < 0:
                raise ValueError(f"{name} must be nonnegative")
        if self.direct_occurrence_count + self.generated_occurrence_count != len(
            self.occurrence_indexes
        ):
            raise ValueError("group origin counts must equal occurrence count")
        if self.bibliography_entry_index is not None and (
            type(self.bibliography_entry_index) is not int
            or self.bibliography_entry_index < 0
        ):
            raise ValueError("bibliography_entry_index must be nonnegative or None")


@dataclass(frozen=True, slots=True)
class ManuscriptCitationTodo:
    """Represent one prospective citation marker and generated rendered calls."""

    todo_id: str
    todo_marker_index: int
    locator: ManuscriptSourceLocator
    priority_locator: ManuscriptSourceLocator
    priority: ManuscriptCitationPriority
    generated_call_ids: tuple[str, ...]
    generated_occurrence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.todo_id) is not str or not self.todo_id:
            raise TypeError("todo_id must be nonempty")
        if type(self.todo_marker_index) is not int or self.todo_marker_index < 0:
            raise ValueError("todo_marker_index must be nonnegative")
        if (
            type(self.locator) is not ManuscriptSourceLocator
            or type(self.priority_locator) is not ManuscriptSourceLocator
        ):
            raise TypeError("todo locators must be ManuscriptSourceLocator")
        if type(self.priority) is not ManuscriptCitationPriority:
            raise TypeError("priority must be ManuscriptCitationPriority")
        for values, name in (
            (self.generated_call_ids, "generated_call_ids"),
            (self.generated_occurrence_ids, "generated_occurrence_ids"),
        ):
            if (
                type(values) is not tuple
                or not values
                or any(type(value) is not str or not value for value in values)
            ):
                raise TypeError(f"{name} must be a nonempty tuple of strings")
            if len(set(values)) != len(values):
                raise ValueError(f"{name} must contain unique identities")
        if len(self.generated_call_ids) != len(self.generated_occurrence_ids):
            raise ValueError("each generated todo call must own one occurrence")


@dataclass(frozen=True, slots=True)
class ManuscriptCitationSourceGap:
    """Represent an unresolved source placeholder without inventing a cite key."""

    source_gap_id: str
    source_gap_index: int
    locator: ManuscriptSourceLocator
    reason: ManuscriptCitationSourceGapReason
    placeholder_identifier: str

    def __post_init__(self) -> None:
        if type(self.source_gap_id) is not str or not self.source_gap_id:
            raise TypeError("source_gap_id must be nonempty")
        if type(self.source_gap_index) is not int or self.source_gap_index < 0:
            raise ValueError("source_gap_index must be nonnegative")
        if type(self.locator) is not ManuscriptSourceLocator:
            raise TypeError("locator must be ManuscriptSourceLocator")
        if type(self.reason) is not ManuscriptCitationSourceGapReason:
            raise TypeError("reason must be ManuscriptCitationSourceGapReason")
        if (
            type(self.placeholder_identifier) is not str
            or not self.placeholder_identifier
        ):
            raise TypeError("placeholder_identifier must be nonempty")


@dataclass(frozen=True, slots=True)
class ManuscriptCitationSnapshot:
    """Retain one complete deterministic citation snapshot for the monograph graph."""

    contract_id: str
    snapshot_id: str
    repository_revision: str
    entrypoint_path: str
    bibliography_path: str
    parser_identity: str
    generator_identity: str
    bibliography_content_identity: CitationContentIdentity
    source_files: tuple[ManuscriptSourceFileSnapshot, ...]
    include_instances: tuple[ManuscriptIncludeInstance, ...]
    bibliography_entries: tuple[ManuscriptBibliographyEntrySnapshot, ...]
    calls: tuple[ManuscriptCitationCall, ...]
    occurrences: tuple[ManuscriptCitationOccurrence, ...]
    groups: tuple[ManuscriptCitationGroup, ...]
    todos: tuple[ManuscriptCitationTodo, ...]
    source_gaps: tuple[ManuscriptCitationSourceGap, ...]
    missing_keys: tuple[str, ...]
    duplicate_keys: tuple[str, ...]
    uncited_keys: tuple[str, ...]

    def __post_init__(self) -> None:
        for value, name in (
            (self.contract_id, "contract_id"),
            (self.snapshot_id, "snapshot_id"),
            (self.repository_revision, "repository_revision"),
            (self.entrypoint_path, "entrypoint_path"),
            (self.bibliography_path, "bibliography_path"),
            (self.parser_identity, "parser_identity"),
            (self.generator_identity, "generator_identity"),
        ):
            if type(value) is not str or not value:
                raise TypeError(f"{name} must be a nonempty string")
        if len(self.repository_revision) != 40 or any(
            character not in "0123456789abcdef"
            for character in self.repository_revision
        ):
            raise ValueError("repository_revision must be a lowercase Git object ID")
        if type(self.bibliography_content_identity) is not CitationContentIdentity:
            raise TypeError(
                "bibliography_content_identity must be CitationContentIdentity"
            )
        self._validate_sequences()
        self._validate_relations()

    def _validate_sequences(self) -> None:
        if type(self.source_files) is not tuple or any(
            type(value) is not ManuscriptSourceFileSnapshot
            for value in self.source_files
        ):
            raise TypeError("source_files must contain ManuscriptSourceFileSnapshot")
        if type(self.include_instances) is not tuple or any(
            type(value) is not ManuscriptIncludeInstance
            for value in self.include_instances
        ):
            raise TypeError("include_instances must contain ManuscriptIncludeInstance")
        if type(self.bibliography_entries) is not tuple or any(
            type(value) is not ManuscriptBibliographyEntrySnapshot
            for value in self.bibliography_entries
        ):
            raise TypeError(
                "bibliography_entries must contain ManuscriptBibliographyEntrySnapshot"
            )
        if type(self.calls) is not tuple or any(
            type(value) is not ManuscriptCitationCall for value in self.calls
        ):
            raise TypeError("calls must contain ManuscriptCitationCall")
        if type(self.occurrences) is not tuple or any(
            type(value) is not ManuscriptCitationOccurrence
            for value in self.occurrences
        ):
            raise TypeError("occurrences must contain ManuscriptCitationOccurrence")
        if type(self.groups) is not tuple or any(
            type(value) is not ManuscriptCitationGroup for value in self.groups
        ):
            raise TypeError("groups must contain ManuscriptCitationGroup")
        if type(self.todos) is not tuple or any(
            type(value) is not ManuscriptCitationTodo for value in self.todos
        ):
            raise TypeError("todos must contain ManuscriptCitationTodo")
        if type(self.source_gaps) is not tuple or any(
            type(value) is not ManuscriptCitationSourceGap for value in self.source_gaps
        ):
            raise TypeError("source_gaps must contain ManuscriptCitationSourceGap")
        for key_values, name in (
            (self.missing_keys, "missing_keys"),
            (self.duplicate_keys, "duplicate_keys"),
            (self.uncited_keys, "uncited_keys"),
        ):
            if type(key_values) is not tuple or any(
                type(value) is not str or not value for value in key_values
            ):
                raise TypeError(f"{name} must be a tuple of nonempty strings")
            if tuple(sorted(set(key_values))) != key_values:
                raise ValueError(f"{name} must be sorted and unique")

    def _validate_relations(self) -> None:
        indexed = (
            (tuple(value.graph_order for value in self.source_files), "source graph"),
            (tuple(value.include_index for value in self.include_instances), "include"),
            (tuple(value.entry_index for value in self.bibliography_entries), "entry"),
            (tuple(value.call_index for value in self.calls), "call"),
            (tuple(value.occurrence_index for value in self.occurrences), "occurrence"),
            (tuple(value.group_index for value in self.groups), "group"),
            (tuple(value.todo_marker_index for value in self.todos), "todo"),
            (tuple(value.source_gap_index for value in self.source_gaps), "source gap"),
        )
        for indexes, name in indexed:
            if indexes != tuple(range(len(indexes))):
                raise ValueError(f"{name} indexes must be contiguous from zero")
        if not self.source_files or not self.include_instances:
            raise ValueError("snapshot requires a root source and include instance")
        if self.source_files[0].source_path != self.entrypoint_path:
            raise ValueError("first source file must be the entrypoint")
        if self.include_instances[0].child_file_id != self.source_files[0].file_id:
            raise ValueError("root include instance must bind the entrypoint file")
        entry_by_key = {entry.key: entry for entry in self.bibliography_entries}
        if len(entry_by_key) != len(self.bibliography_entries):
            raise ValueError("bibliography entry keys must be unique in a snapshot")
        for occurrence in self.occurrences:
            if occurrence.call_index >= len(self.calls):
                raise ValueError("occurrence call index is outside calls")
            bound_entry = entry_by_key.get(occurrence.key)
            expected_index = None if bound_entry is None else bound_entry.entry_index
            if occurrence.bibliography_entry_index != expected_index:
                raise ValueError("occurrence bibliography binding is inconsistent")
        for call in self.calls:
            call_expected = tuple(
                occurrence.occurrence_index
                for occurrence in self.occurrences
                if occurrence.call_index == call.call_index
            )
            if call.occurrence_indexes != call_expected:
                raise ValueError("call occurrence indexes are inconsistent")
        for group in self.groups:
            group_expected = tuple(
                occurrence.occurrence_index
                for occurrence in self.occurrences
                if occurrence.key == group.key
            )
            if group.occurrence_indexes != group_expected:
                raise ValueError("group occurrence indexes are inconsistent")
        expected_missing = {
            group.key for group in self.groups if group.bibliography_entry_index is None
        }
        if set(self.missing_keys) != expected_missing:
            raise ValueError("missing_keys must equal unbound citation groups")
        if self.duplicate_keys:
            raise ValueError("successful snapshots cannot retain duplicate keys")
        cited = {group.key for group in self.groups}
        if set(self.uncited_keys) != set(entry_by_key) - cited:
            raise ValueError("uncited_keys must equal bibliography keys without groups")


@dataclass(frozen=True, slots=True)
class ResearchMonographCitationSnapshotRequest:
    """Request the exact repository-owned research-monograph citation snapshot.

    Parameters
    ----------
    repository_root
        Absolute repository root containing the contract-owned manuscript paths.
    """

    repository_root: str

    def __post_init__(self) -> None:
        if type(self.repository_root) is not str or not self.repository_root:
            raise TypeError("repository_root must be a nonempty string")
        if not self.repository_root.startswith("/"):
            raise ValueError("repository_root must be absolute")


@dataclass(frozen=True, slots=True)
class ResearchMonographCitationSnapshotResult:
    """Represent one successful complete snapshot operation result."""

    snapshot: ManuscriptCitationSnapshot

    def __post_init__(self) -> None:
        if type(self.snapshot) is not ManuscriptCitationSnapshot:
            raise TypeError("snapshot must be ManuscriptCitationSnapshot")
