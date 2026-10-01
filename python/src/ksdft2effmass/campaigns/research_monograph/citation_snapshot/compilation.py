"""Deterministic compilation of the repository-owned monograph citation snapshot.

The compiler reads one closed manuscript root and bibliography, resolves the TeX
include graph, parses supported citation constructs, and returns immutable source and
citation records. It performs no TeX build, network access, persistence, external
source ingestion, or scholarly acceptance operation.
"""

from __future__ import annotations

import hashlib
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .integrity import (
    BIBLIOGRAPHY_PATH,
    CONTRACT_ID,
    ENTRYPOINT_PATH,
    GENERATOR_IDENTITY,
    MAX_SOURCE_BYTES,
    PARSER_IDENTITY,
    CitationIdentityGenerator,
    IdentityPart,
    ResearchMonographCitationSnapshotIntegrityValidator,
)
from .parsing import (
    BiblatexSourceParser,
    ParsedBibliography,
    ParsedCitationCall,
    ParsedCitationTodo,
    ParsedInclude,
    ParsedSourceGap,
    ParsedTexSource,
    TexCitationSourceParser,
)
from .records import (
    CitationContentAlgorithm,
    CitationContentIdentity,
    CitationSnapshotError,
    CitationSnapshotErrorCode,
    ManuscriptBibliographyEntrySnapshot,
    ManuscriptCitationCall,
    ManuscriptCitationGroup,
    ManuscriptCitationOccurrence,
    ManuscriptCitationOrigin,
    ManuscriptCitationSnapshot,
    ManuscriptCitationSourceGap,
    ManuscriptCitationSourceGapReason,
    ManuscriptCitationTodo,
    ManuscriptIncludeInstance,
    ManuscriptSourceFileSnapshot,
    ManuscriptSourceLocator,
    ResearchMonographCitationSnapshotRequest,
    ResearchMonographCitationSnapshotResult,
)

_MANUSCRIPT_PATH = PurePosixPath(ENTRYPOINT_PATH)
_BIBLIOGRAPHY_PATH = PurePosixPath(BIBLIOGRAPHY_PATH)
_CONTRACT_ID = CONTRACT_ID
_PARSER_IDENTITY = PARSER_IDENTITY
_GENERATOR_IDENTITY = GENERATOR_IDENTITY

type ParsedEvent = (
    ParsedCitationCall | ParsedCitationTodo | ParsedInclude | ParsedSourceGap
)


@dataclass(frozen=True, slots=True)
class RepositoryRevisionInspector:
    """Read the exact Git HEAD identity without invoking Git or changing state."""

    def execute(self, repository_root: Path) -> str:
        """Return the lowercase 40-character object ID for a worktree HEAD."""
        if not isinstance(repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        dot_git = repository_root / ".git"
        try:
            if dot_git.is_file():
                marker = dot_git.read_text(encoding="utf-8").strip()
                if not marker.startswith("gitdir: "):
                    return self._fail()
                git_dir = Path(marker.removeprefix("gitdir: "))
                if not git_dir.is_absolute():
                    git_dir = (repository_root / git_dir).resolve()
            elif dot_git.is_dir():
                git_dir = dot_git
            else:
                return self._fail()
            head = (git_dir / "HEAD").read_text(encoding="utf-8").strip()
            if head.startswith("ref: "):
                reference = head.removeprefix("ref: ")
                common = git_dir
                common_marker = git_dir / "commondir"
                if common_marker.is_file():
                    common_path = common_marker.read_text(encoding="utf-8").strip()
                    common = (git_dir / common_path).resolve()
                loose = common / reference
                if loose.is_file():
                    revision = loose.read_text(encoding="utf-8").strip()
                else:
                    revision = self._packed_reference(common, reference)
            else:
                revision = head
        except OSError:
            return self._fail()
        if len(revision) != 40 or any(
            character not in "0123456789abcdef" for character in revision
        ):
            return self._fail()
        return revision

    def _packed_reference(self, common: Path, reference: str) -> str:
        packed = common / "packed-refs"
        if not packed.is_file():
            return self._fail()
        try:
            lines = packed.read_text(encoding="utf-8").splitlines()
        except OSError:
            return self._fail()
        for line in lines:
            if not line or line.startswith(("#", "^")):
                continue
            fields = line.split(" ", 1)
            if len(fields) == 2 and fields[1] == reference:
                return fields[0]
        return self._fail()

    @staticmethod
    def _fail() -> str:
        raise CitationSnapshotError(
            CitationSnapshotErrorCode.REPOSITORY_REVISION_UNAVAILABLE,
            None,
            None,
            "exact repository HEAD revision is unavailable",
        )


@dataclass(frozen=True, slots=True)
class CitationSourceDocument:
    """Retain exact bytes and parsed structure for one unique TeX file."""

    path: Path
    relative_path: str
    source_bytes: bytes
    parsed: ParsedTexSource
    content_identity: CitationContentIdentity
    file_id: str
    graph_order: int


@dataclass(frozen=True, slots=True)
class RepositoryHeadSourceVerifier:
    """Require every consumed source byte sequence to equal one exact HEAD blob."""

    def execute(
        self,
        repository_root: Path,
        revision: str,
        sources: tuple[CitationSourceDocument, ...],
        bibliography_path: str,
        bibliography_bytes: bytes,
    ) -> None:
        """Fail when a source is dirty, untracked, absent, or unreadable at HEAD."""
        for source in sources:
            self._verify_blob(
                repository_root, revision, source.relative_path, source.source_bytes
            )
        self._verify_blob(
            repository_root, revision, bibliography_path, bibliography_bytes
        )

    @staticmethod
    def _verify_blob(
        repository_root: Path, revision: str, source_path: str, source_bytes: bytes
    ) -> None:
        try:
            completed = subprocess.run(
                [
                    "git",
                    "-C",
                    repository_root.as_posix(),
                    "cat-file",
                    "blob",
                    f"{revision}:{source_path}",
                ],
                check=False,
                capture_output=True,
                timeout=30,
            )
        except OSError, subprocess.TimeoutExpired:
            completed = None
        if (
            completed is None
            or completed.returncode != 0
            or completed.stdout != source_bytes
        ):
            raise CitationSnapshotError(
                CitationSnapshotErrorCode.SOURCE_DIFFERS_FROM_REVISION,
                source_path,
                None,
                "consumed source bytes do not equal the exact repository revision",
            )


@dataclass(frozen=True, slots=True)
class CitationCallDraft:
    """Bind one parsed call to its source and include instance."""

    parsed: ParsedCitationCall
    source: CitationSourceDocument
    include_instance_id: str
    include_index: int
    todo_marker_index: int | None


@dataclass(frozen=True, slots=True)
class CitationTodoDraft:
    """Bind one parsed todo marker to its source and generated draft calls."""

    parsed: ParsedCitationTodo
    source: CitationSourceDocument
    include_index: int
    generated_call_indexes: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class CitationSourceGapDraft:
    """Bind one parsed placeholder gap to its source and include instance."""

    parsed: ParsedSourceGap
    source: CitationSourceDocument
    include_index: int


@dataclass(frozen=True, slots=True)
class CitationGraphCompilation:
    """Retain the complete deterministic include traversal before final records."""

    sources: tuple[CitationSourceDocument, ...]
    include_instances: tuple[ManuscriptIncludeInstance, ...]
    calls: tuple[CitationCallDraft, ...]
    todos: tuple[CitationTodoDraft, ...]
    gaps: tuple[CitationSourceGapDraft, ...]


@dataclass(frozen=True, slots=True)
class ResearchMonographCitationGraphCompiler:
    """Resolve the exact research-monograph TeX graph and citation event order."""

    parser: TexCitationSourceParser
    identities: CitationIdentityGenerator

    def __post_init__(self) -> None:
        if type(self.parser) is not TexCitationSourceParser:
            raise TypeError("parser must be TexCitationSourceParser")
        if type(self.identities) is not CitationIdentityGenerator:
            raise TypeError("identities must be CitationIdentityGenerator")

    def execute(self, repository_root: Path) -> CitationGraphCompilation:
        """Compile the entrypoint graph with fail-closed path and cycle handling."""
        monograph_root = (repository_root / _BIBLIOGRAPHY_PATH.parent).resolve()
        entrypoint = (repository_root / _MANUSCRIPT_PATH).resolve()
        sources: list[CitationSourceDocument] = []
        source_by_path: dict[Path, CitationSourceDocument] = {}
        instances: list[ManuscriptIncludeInstance] = []
        calls: list[CitationCallDraft] = []
        todos: list[CitationTodoDraft] = []
        gaps: list[CitationSourceGapDraft] = []
        self._visit(
            repository_root.resolve(),
            monograph_root,
            entrypoint,
            None,
            None,
            0,
            0,
            0,
            (),
            sources,
            source_by_path,
            instances,
            calls,
            todos,
            gaps,
        )
        return CitationGraphCompilation(
            tuple(sources), tuple(instances), tuple(calls), tuple(todos), tuple(gaps)
        )

    def _visit(
        self,
        repository_root: Path,
        monograph_root: Path,
        path: Path,
        parent_file_id: str | None,
        parent_instance_id: str | None,
        source_start: int,
        source_end: int,
        ordinal: int,
        active_paths: tuple[Path, ...],
        sources: list[CitationSourceDocument],
        source_by_path: dict[Path, CitationSourceDocument],
        instances: list[ManuscriptIncludeInstance],
        calls: list[CitationCallDraft],
        todos: list[CitationTodoDraft],
        gaps: list[CitationSourceGapDraft],
    ) -> None:
        resolved = path.resolve()
        if not resolved.is_relative_to(monograph_root):
            raise CitationSnapshotError(
                CitationSnapshotErrorCode.PATH_ESCAPE,
                self._relative_or_none(repository_root, resolved),
                None,
                "included TeX path escapes the monograph root",
            )
        if resolved in active_paths:
            raise CitationSnapshotError(
                CitationSnapshotErrorCode.INCLUDE_CYCLE,
                self._relative_or_none(repository_root, resolved),
                None,
                "TeX include graph contains a cycle",
            )
        source = source_by_path.get(resolved)
        if source is None:
            if not resolved.is_file():
                raise CitationSnapshotError(
                    CitationSnapshotErrorCode.SOURCE_MISSING,
                    self._relative_or_none(repository_root, resolved),
                    None,
                    "required TeX source is missing",
                )
            try:
                byte_size = resolved.stat().st_size
                if byte_size < 1 or byte_size > MAX_SOURCE_BYTES:
                    raise CitationSnapshotError(
                        CitationSnapshotErrorCode.OUTPUT_LIMIT_EXCEEDED,
                        self._relative_or_none(repository_root, resolved),
                        None,
                        "TeX source size is outside 1 through 100,000,000 bytes",
                    )
                source_bytes = resolved.read_bytes()
            except CitationSnapshotError:
                raise
            except OSError:
                raise CitationSnapshotError(
                    CitationSnapshotErrorCode.SOURCE_MISSING,
                    self._relative_or_none(repository_root, resolved),
                    None,
                    "required TeX source cannot be read",
                ) from None
            relative = resolved.relative_to(repository_root).as_posix()
            identity = self._content_identity(source_bytes)
            file_id = self.identities.execute(
                "citation-file", (relative, identity.digest, identity.byte_count)
            )
            source = CitationSourceDocument(
                resolved,
                relative,
                source_bytes,
                self.parser.execute(source_bytes, relative),
                identity,
                file_id,
                len(sources),
            )
            sources.append(source)
            source_by_path[resolved] = source
        include_index = len(instances)
        instance_id = self.identities.execute(
            "citation-include",
            (
                source.file_id,
                parent_instance_id,
                source_start,
                source_end,
                ordinal,
                len(active_paths),
                include_index,
            ),
        )
        instances.append(
            ManuscriptIncludeInstance(
                instance_id,
                include_index,
                parent_file_id,
                parent_instance_id,
                source.file_id,
                source.relative_path,
                source_start,
                source_end,
                ordinal,
                len(active_paths),
            )
        )
        events: list[tuple[int, int, ParsedEvent]] = []
        events.extend((value.char_start, 1, value) for value in source.parsed.calls)
        events.extend((value.char_start, 0, value) for value in source.parsed.todos)
        events.extend((value.char_start, 2, value) for value in source.parsed.includes)
        events.extend((value.char_start, 3, value) for value in source.parsed.gaps)
        for _, _, event in sorted(events, key=lambda item: (item[0], item[1])):
            if type(event) is ParsedCitationCall:
                calls.append(
                    CitationCallDraft(event, source, instance_id, include_index, None)
                )
            elif type(event) is ParsedCitationTodo:
                todo_index = len(todos)
                generated_indexes: list[int] = []
                for parsed_call in event.calls:
                    generated_indexes.append(len(calls))
                    calls.append(
                        CitationCallDraft(
                            parsed_call,
                            source,
                            instance_id,
                            include_index,
                            todo_index,
                        )
                    )
                todos.append(
                    CitationTodoDraft(
                        event, source, include_index, tuple(generated_indexes)
                    )
                )
            elif type(event) is ParsedInclude:
                # The canonical composition root is kept in ``manuscript/`` but is
                # built from the monograph root, so its authored chapter and appendix
                # targets are monograph-root relative. Nested sources retain
                # including-file-relative resolution.
                include_root = monograph_root if not active_paths else resolved.parent
                child = include_root / event.relative_path
                if child.suffix == "":
                    child = child.with_suffix(".tex")
                self._visit(
                    repository_root,
                    monograph_root,
                    child,
                    source.file_id,
                    instance_id,
                    source.parsed.byte_offset(event.char_start),
                    source.parsed.byte_offset(event.char_end),
                    event.ordinal,
                    (*active_paths, resolved),
                    sources,
                    source_by_path,
                    instances,
                    calls,
                    todos,
                    gaps,
                )
            else:
                assert type(event) is ParsedSourceGap
                gaps.append(CitationSourceGapDraft(event, source, include_index))

    @staticmethod
    def _relative_or_none(repository_root: Path, path: Path) -> str | None:
        try:
            return path.relative_to(repository_root).as_posix()
        except ValueError:
            return None

    @staticmethod
    def _content_identity(source_bytes: bytes) -> CitationContentIdentity:
        return CitationContentIdentity(
            CitationContentAlgorithm.SHA256,
            hashlib.sha256(source_bytes).hexdigest(),
            len(source_bytes),
        )


@dataclass(frozen=True, slots=True)
class ResearchMonographCitationSnapshotCompiler:
    """Compile the canonical unversioned research-monograph citation snapshot.

    This semantic performer owns exact repository path selection, include traversal,
    structural parsing, deterministic identities, bibliography reconciliation, and
    immutable result assembly. Success means complete parser coverage; every failure
    raises :class:`CitationSnapshotError` and returns no partial snapshot.
    """

    def execute(
        self, request: ResearchMonographCitationSnapshotRequest
    ) -> ResearchMonographCitationSnapshotResult:
        """Compile one complete snapshot from the exact repository-owned sources.

        Parameters
        ----------
        request
            Absolute repository root. The manuscript and bibliography paths are
            fixed by this contract and are not caller-selectable.

        Returns
        -------
        ResearchMonographCitationSnapshotResult
            Complete deterministic snapshot.

        Raises
        ------
        TypeError
            If ``request`` has the wrong semantic type.
        CitationSnapshotError
            If repository identity, graph closure, parsing, path safety, or
            bibliography uniqueness cannot be established.
        """
        if type(request) is not ResearchMonographCitationSnapshotRequest:
            raise TypeError("request must be ResearchMonographCitationSnapshotRequest")
        repository_root = Path(request.repository_root)
        if not repository_root.is_dir():
            raise CitationSnapshotError(
                CitationSnapshotErrorCode.INVALID_REQUEST,
                None,
                None,
                "repository_root must identify an existing directory",
            )
        identities = CitationIdentityGenerator()
        revision = RepositoryRevisionInspector().execute(repository_root)
        graph = ResearchMonographCitationGraphCompiler(
            TexCitationSourceParser(), identities
        ).execute(repository_root)
        bibliography_path = repository_root / _BIBLIOGRAPHY_PATH
        if not bibliography_path.is_file():
            raise CitationSnapshotError(
                CitationSnapshotErrorCode.SOURCE_MISSING,
                _BIBLIOGRAPHY_PATH.as_posix(),
                None,
                "required bibliography source is missing",
            )
        try:
            bibliography_size = bibliography_path.stat().st_size
            if bibliography_size < 1 or bibliography_size > MAX_SOURCE_BYTES:
                raise CitationSnapshotError(
                    CitationSnapshotErrorCode.OUTPUT_LIMIT_EXCEEDED,
                    _BIBLIOGRAPHY_PATH.as_posix(),
                    None,
                    "bibliography size is outside 1 through 100,000,000 bytes",
                )
            bibliography_bytes = bibliography_path.read_bytes()
        except CitationSnapshotError:
            raise
        except OSError:
            raise CitationSnapshotError(
                CitationSnapshotErrorCode.SOURCE_MISSING,
                _BIBLIOGRAPHY_PATH.as_posix(),
                None,
                "required bibliography source cannot be read",
            ) from None
        RepositoryHeadSourceVerifier().execute(
            repository_root,
            revision,
            graph.sources,
            _BIBLIOGRAPHY_PATH.as_posix(),
            bibliography_bytes,
        )
        bibliography_identity = self._content_identity(bibliography_bytes)
        bibliography = BiblatexSourceParser().execute(
            bibliography_bytes, _BIBLIOGRAPHY_PATH.as_posix()
        )
        snapshot_id = self._snapshot_identity(
            identities, revision, graph.sources, bibliography_identity
        )
        source_files = tuple(
            ManuscriptSourceFileSnapshot(
                source.file_id,
                source.relative_path,
                source.content_identity.byte_count,
                source.content_identity.digest,
                source.graph_order,
            )
            for source in graph.sources
        )
        entries = self._bibliography_entries(
            bibliography,
            bibliography_bytes,
            bibliography_identity,
            snapshot_id,
            identities,
        )
        calls, occurrences = self._citation_records(
            graph, entries, snapshot_id, identities
        )
        groups = self._groups(occurrences, entries, snapshot_id, identities)
        todos = self._todos(graph, calls, occurrences, snapshot_id, identities)
        gaps = self._gaps(graph, snapshot_id, identities)
        entry_keys = {entry.key for entry in entries}
        group_keys = {group.key for group in groups}
        missing = tuple(sorted(group_keys - entry_keys))
        uncited = tuple(sorted(entry_keys - group_keys))
        try:
            snapshot = ManuscriptCitationSnapshot(
                _CONTRACT_ID,
                snapshot_id,
                revision,
                _MANUSCRIPT_PATH.as_posix(),
                _BIBLIOGRAPHY_PATH.as_posix(),
                _PARSER_IDENTITY,
                _GENERATOR_IDENTITY,
                bibliography_identity,
                source_files,
                graph.include_instances,
                entries,
                calls,
                occurrences,
                groups,
                todos,
                gaps,
                missing,
                (),
                uncited,
            )
            request_id = request.request_id
            result_id = ResearchMonographCitationSnapshotIntegrityValidator().execute(
                snapshot, request_id
            )
            return ResearchMonographCitationSnapshotResult(
                request_id, result_id, snapshot
            )
        except ValueError as error:
            raise CitationSnapshotError(
                CitationSnapshotErrorCode.INTEGRITY_REPLAY_FAILED,
                None,
                None,
                str(error),
            ) from None

    def _bibliography_entries(
        self,
        parsed: ParsedBibliography,
        source_bytes: bytes,
        source_identity: CitationContentIdentity,
        snapshot_id: str,
        identities: CitationIdentityGenerator,
    ) -> tuple[ManuscriptBibliographyEntrySnapshot, ...]:
        entries: list[ManuscriptBibliographyEntrySnapshot] = []
        for entry_index, parsed_entry in enumerate(parsed.entries):
            byte_start = parsed.byte_offset(parsed_entry.char_start)
            byte_end = parsed.byte_offset(parsed_entry.char_end)
            entry_bytes = source_bytes[byte_start:byte_end]
            entry_identity = self._content_identity(entry_bytes)
            line, column = parsed.line_column(parsed_entry.char_start)
            locator = ManuscriptSourceLocator(
                _BIBLIOGRAPHY_PATH.as_posix(),
                source_identity,
                0,
                byte_start,
                byte_end,
                line,
                column,
            )
            entry_id = identities.execute(
                "citation-entry",
                (
                    snapshot_id,
                    entry_index,
                    parsed_entry.key,
                    source_identity.digest,
                    byte_start,
                    byte_end,
                    entry_identity.digest,
                ),
            )
            entries.append(
                ManuscriptBibliographyEntrySnapshot(
                    entry_id,
                    entry_index,
                    parsed_entry.key,
                    parsed_entry.entry_type,
                    locator,
                    entry_identity,
                    None,
                )
            )
        return tuple(entries)

    def _citation_records(
        self,
        graph: CitationGraphCompilation,
        entries: tuple[ManuscriptBibliographyEntrySnapshot, ...],
        snapshot_id: str,
        identities: CitationIdentityGenerator,
    ) -> tuple[
        tuple[ManuscriptCitationCall, ...],
        tuple[ManuscriptCitationOccurrence, ...],
    ]:
        entry_indexes = {entry.key: entry.entry_index for entry in entries}
        calls: list[ManuscriptCitationCall] = []
        occurrences: list[ManuscriptCitationOccurrence] = []
        for call_index, draft in enumerate(graph.calls):
            call_locator = self._locator(
                draft.source,
                draft.include_index,
                draft.parsed.char_start,
                draft.parsed.char_end,
            )
            call_id = identities.execute(
                "citation-call",
                (
                    snapshot_id,
                    draft.include_instance_id,
                    call_locator.source_content_identity.digest,
                    call_locator.byte_start,
                    call_locator.byte_end,
                    draft.parsed.command_kind.value,
                    draft.parsed.origin.value,
                    call_index,
                ),
            )
            occurrence_indexes: list[int] = []
            for key_index, key in enumerate(draft.parsed.keys):
                occurrence_index = len(occurrences)
                occurrence_indexes.append(occurrence_index)
                key_locator = self._locator(
                    draft.source,
                    draft.include_index,
                    key.char_start,
                    key.char_end,
                )
                occurrence_id = identities.execute(
                    "citation-occurrence",
                    (
                        snapshot_id,
                        draft.include_instance_id,
                        key_locator.source_content_identity.digest,
                        key_locator.byte_start,
                        key_locator.byte_end,
                        draft.parsed.command_kind.value,
                        key_index,
                        draft.parsed.origin.value,
                    ),
                )
                occurrences.append(
                    ManuscriptCitationOccurrence(
                        occurrence_id,
                        occurrence_index,
                        call_index,
                        key_index,
                        key.key,
                        draft.parsed.origin,
                        key_locator,
                        entry_indexes.get(key.key),
                        draft.todo_marker_index,
                    )
                )
            calls.append(
                ManuscriptCitationCall(
                    call_id,
                    call_index,
                    draft.include_instance_id,
                    draft.source.file_id,
                    draft.parsed.command_kind,
                    draft.parsed.origin,
                    call_locator,
                    tuple(occurrence_indexes),
                    draft.todo_marker_index,
                )
            )
        return tuple(calls), tuple(occurrences)

    def _groups(
        self,
        occurrences: tuple[ManuscriptCitationOccurrence, ...],
        entries: tuple[ManuscriptBibliographyEntrySnapshot, ...],
        snapshot_id: str,
        identities: CitationIdentityGenerator,
    ) -> tuple[ManuscriptCitationGroup, ...]:
        entry_indexes = {entry.key: entry.entry_index for entry in entries}
        groups: list[ManuscriptCitationGroup] = []
        for group_index, key in enumerate(sorted({value.key for value in occurrences})):
            selected = tuple(value for value in occurrences if value.key == key)
            occurrence_indexes = tuple(value.occurrence_index for value in selected)
            generated = sum(
                value.origin is ManuscriptCitationOrigin.CITATION_TODO_EXPANSION
                for value in selected
            )
            group_id = identities.execute(
                "citation-group", (snapshot_id, key, group_index)
            )
            groups.append(
                ManuscriptCitationGroup(
                    group_id,
                    group_index,
                    key,
                    occurrence_indexes,
                    len(selected) - generated,
                    generated,
                    entry_indexes.get(key),
                )
            )
        return tuple(groups)

    def _todos(
        self,
        graph: CitationGraphCompilation,
        calls: tuple[ManuscriptCitationCall, ...],
        occurrences: tuple[ManuscriptCitationOccurrence, ...],
        snapshot_id: str,
        identities: CitationIdentityGenerator,
    ) -> tuple[ManuscriptCitationTodo, ...]:
        todos: list[ManuscriptCitationTodo] = []
        for todo_index, draft in enumerate(graph.todos):
            locator = self._locator(
                draft.source,
                draft.include_index,
                draft.parsed.char_start,
                draft.parsed.char_end,
            )
            priority_locator = self._locator(
                draft.source,
                draft.include_index,
                draft.parsed.priority_start,
                draft.parsed.priority_end,
            )
            todo_id = identities.execute(
                "citation-todo",
                (
                    snapshot_id,
                    locator.source_content_identity.digest,
                    locator.byte_start,
                    locator.byte_end,
                    draft.parsed.priority.value,
                    todo_index,
                ),
            )
            generated_calls = tuple(
                calls[index] for index in draft.generated_call_indexes
            )
            generated_occurrences = tuple(
                occurrences[call.occurrence_indexes[0]] for call in generated_calls
            )
            todos.append(
                ManuscriptCitationTodo(
                    todo_id,
                    todo_index,
                    locator,
                    priority_locator,
                    draft.parsed.priority,
                    tuple(call.call_id for call in generated_calls),
                    tuple(value.occurrence_id for value in generated_occurrences),
                )
            )
        return tuple(todos)

    def _gaps(
        self,
        graph: CitationGraphCompilation,
        snapshot_id: str,
        identities: CitationIdentityGenerator,
    ) -> tuple[ManuscriptCitationSourceGap, ...]:
        gaps: list[ManuscriptCitationSourceGap] = []
        for gap_index, draft in enumerate(graph.gaps):
            locator = self._locator(
                draft.source,
                draft.include_index,
                draft.parsed.char_start,
                draft.parsed.char_end,
            )
            gap_id = identities.execute(
                "citation-gap",
                (
                    snapshot_id,
                    locator.source_content_identity.digest,
                    locator.byte_start,
                    locator.byte_end,
                    ManuscriptCitationSourceGapReason.PLACEHOLDER_IDENTIFIER.value,
                    gap_index,
                ),
            )
            gaps.append(
                ManuscriptCitationSourceGap(
                    gap_id,
                    gap_index,
                    locator,
                    ManuscriptCitationSourceGapReason.PLACEHOLDER_IDENTIFIER,
                    draft.parsed.placeholder_identifier,
                )
            )
        return tuple(gaps)

    def _snapshot_identity(
        self,
        identities: CitationIdentityGenerator,
        revision: str,
        sources: tuple[CitationSourceDocument, ...],
        bibliography_identity: CitationContentIdentity,
    ) -> str:
        parts: list[IdentityPart] = [
            _CONTRACT_ID,
            revision,
            _MANUSCRIPT_PATH.as_posix(),
            _BIBLIOGRAPHY_PATH.as_posix(),
            _PARSER_IDENTITY,
            _GENERATOR_IDENTITY,
        ]
        for source in sources:
            parts.extend(
                (
                    source.relative_path,
                    source.content_identity.byte_count,
                    source.content_identity.digest,
                    source.graph_order,
                )
            )
        parts.extend(
            (
                _BIBLIOGRAPHY_PATH.as_posix(),
                bibliography_identity.byte_count,
                bibliography_identity.digest,
            )
        )
        return identities.execute("citation-snapshot", tuple(parts))

    @staticmethod
    def _locator(
        source: CitationSourceDocument,
        include_index: int,
        char_start: int,
        char_end: int,
    ) -> ManuscriptSourceLocator:
        byte_start = source.parsed.byte_offset(char_start)
        byte_end = source.parsed.byte_offset(char_end)
        line, column = source.parsed.line_column(char_start)
        return ManuscriptSourceLocator(
            source.relative_path,
            source.content_identity,
            include_index,
            byte_start,
            byte_end,
            line,
            column,
        )

    @staticmethod
    def _content_identity(source_bytes: bytes) -> CitationContentIdentity:
        return CitationContentIdentity(
            CitationContentAlgorithm.SHA256,
            hashlib.sha256(source_bytes).hexdigest(),
            len(source_bytes),
        )
