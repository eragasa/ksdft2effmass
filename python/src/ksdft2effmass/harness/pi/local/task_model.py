"""Project-local immutable Task model and explicit migration-review actions.

This module implements the human-accepted schema-version-2 ``HarnessTask``
contract.  It owns no repository discovery, persistence, activation, migration,
selection state, scientific meaning, or human interpretation.  All cross-object
operations consume explicit immutable inputs.  The byte comparator provides
software-verification evidence only; mapped differences do not establish semantic
correctness or human acceptance.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
from dataclasses import dataclass, fields
from enum import StrEnum
from typing import Any

from ..human_review import (
    HumanReviewDecision,
    HumanReviewFinding,
    HumanReviewPacket,
    HumanReviewPreparer,
)
from ..identity import (
    ArtifactIdentity,
    Identifier,
    ResourcePath,
    _require_builtin_str,
    _require_path,
    _require_tuple,
)
from .models import LocalIssue, LocalValidationResult

_GIT_OBJECT = re.compile(r"[0-9a-f]{40}\Z", re.ASCII)
_LOCAL_IDENTIFIER = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?\Z", re.ASCII
)
_TEMPLATE_TOKEN = re.compile(
    rb"\{\{(task|content)\.([A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?)\}\}"
)
_COMPARISON_STATUSES = {"EXACT", "MAPPED_DIFFERENCES", "UNMAPPED_DIFFERENCES"}


def _sha256(content: bytes) -> ArtifactIdentity:
    """Return the accepted exact-byte identity."""
    return ArtifactIdentity(1, "sha256", hashlib.sha256(content).hexdigest())


def _require_local_identifier(value: object, field: str) -> str:
    """Return one value satisfying the frozen project-local Identifier grammar."""
    result = _require_builtin_str(value, field)
    if _LOCAL_IDENTIFIER.fullmatch(result) is None:
        raise ValueError(f"{field} must satisfy the project-local Identifier grammar")
    return result


def _require_int(value: object, field: str, *, minimum: int | None = None) -> int:
    if type(value) is not int:
        raise TypeError(f"{field} must be a built-in int")
    if minimum is not None and value < minimum:
        raise ValueError(f"{field} must be at least {minimum}")
    return value


def _require_bool(value: object, field: str) -> bool:
    if type(value) is not bool:
        raise TypeError(f"{field} must be a built-in bool")
    return value


def _identifier_tuple(value: tuple[object, ...], field: str) -> tuple[str, ...]:
    _require_tuple(value, field)
    result = tuple(_require_local_identifier(item, f"{field} item") for item in value)
    if result != tuple(sorted(set(result))):
        raise ValueError(f"{field} must be sorted and unique")
    return result


def _path_tuple(
    value: tuple[object, ...], field: str, *, nonempty: bool = False
) -> tuple[str, ...]:
    _require_tuple(value, field)
    result = tuple(_require_path(item, f"{field} item") for item in value)
    if nonempty and not result:
        raise ValueError(f"{field} must be nonempty")
    if result != tuple(sorted(set(result))):
        raise ValueError(f"{field} must be sorted and unique")
    return result


def _text_tuple(
    value: tuple[object, ...], field: str, *, nonempty: bool = True
) -> tuple[str, ...]:
    _require_tuple(value, field)
    result = tuple(_require_builtin_str(item, f"{field} item") for item in value)
    if nonempty and not result:
        raise ValueError(f"{field} must be nonempty")
    if len(set(result)) != len(result):
        raise ValueError(f"{field} must contain unique values")
    return result


@dataclass(frozen=True, slots=True)
class HarnessTask:
    """Represent one canonical project-local Task.

    Parameters
    ----------
    schema_version
        Built-in integer equal to 2.
    task_id, status
        Project-local identifiers. ``status`` is opaque lifecycle text.
    title, objective
        Nonempty human-readable text.
    status_detail
        Optional nonempty exact lifecycle detail.
    parent_task_id
        Optional identifier distinct from ``task_id``.
    task_prerequisite_ids, external_prerequisite_ids
        Sorted unique identifier tuples. Both exclude ``task_id`` and are disjoint.
    explicit_activation_required
        Exact built-in Boolean; it records policy but does not activate work.
    authority_reference_paths
        Nonempty sorted unique accepted resource paths.
    authorized_scope, completion_criteria, exclusions
        Nonempty ordered tuples of unique nonempty text.
    intake_path, documentation_path
        Accepted resource paths for non-executable intake and maintained prose.

    Raises
    ------
    TypeError
        If a field has the wrong semantic built-in type.
    ValueError
        If a lexical, nonempty, ordering, uniqueness, or cross-field intrinsic
        invariant fails.

    Notes
    -----
    Graph existence, lifecycle compatibility, authority, activation, documentation
    agreement, completion, and repository state are intentionally not constructor
    concerns.
    """

    schema_version: int
    task_id: Identifier
    title: str
    status: Identifier
    status_detail: str | None
    parent_task_id: Identifier | None
    task_prerequisite_ids: tuple[Identifier, ...]
    external_prerequisite_ids: tuple[Identifier, ...]
    explicit_activation_required: bool
    objective: str
    authority_reference_paths: tuple[ResourcePath, ...]
    authorized_scope: tuple[str, ...]
    completion_criteria: tuple[str, ...]
    exclusions: tuple[str, ...]
    intake_path: ResourcePath
    documentation_path: ResourcePath

    def __post_init__(self) -> None:
        if _require_int(self.schema_version, "schema_version") != 2:
            raise ValueError("schema_version must equal 2")
        _require_local_identifier(self.task_id, "task_id")
        _require_builtin_str(self.title, "title")
        _require_local_identifier(self.status, "status")
        if self.status_detail is not None:
            _require_builtin_str(self.status_detail, "status_detail")
        if self.parent_task_id is not None:
            _require_local_identifier(self.parent_task_id, "parent_task_id")
            if self.parent_task_id == self.task_id:
                raise ValueError("parent_task_id must differ from task_id")
        task_prerequisites = _identifier_tuple(
            self.task_prerequisite_ids, "task_prerequisite_ids"
        )
        external_prerequisites = _identifier_tuple(
            self.external_prerequisite_ids, "external_prerequisite_ids"
        )
        if self.task_id in task_prerequisites or self.task_id in external_prerequisites:
            raise ValueError("a Task may not require itself")
        if set(task_prerequisites) & set(external_prerequisites):
            raise ValueError("Task and external prerequisites must be disjoint")
        _require_bool(self.explicit_activation_required, "explicit_activation_required")
        _require_builtin_str(self.objective, "objective")
        authority_paths = _path_tuple(
            self.authority_reference_paths,
            "authority_reference_paths",
            nonempty=True,
        )
        authorized_scope = _text_tuple(self.authorized_scope, "authorized_scope")
        completion_criteria = _text_tuple(
            self.completion_criteria, "completion_criteria"
        )
        exclusions = _text_tuple(self.exclusions, "exclusions")
        _require_path(self.intake_path, "intake_path")
        _require_path(self.documentation_path, "documentation_path")
        object.__setattr__(self, "task_prerequisite_ids", task_prerequisites)
        object.__setattr__(self, "external_prerequisite_ids", external_prerequisites)
        object.__setattr__(self, "authority_reference_paths", authority_paths)
        object.__setattr__(self, "authorized_scope", authorized_scope)
        object.__setattr__(self, "completion_criteria", completion_criteria)
        object.__setattr__(self, "exclusions", exclusions)


class HarnessTaskSerializer:
    """Serialize one :class:`HarnessTask` to canonical UTF-8 JSON bytes.

    The ActionObject is fieldless and performs no discovery or I/O. It preserves
    the accepted 16-field order, emits tuples as arrays and optional absence as
    ``null``, uses two-space indentation with literal Unicode, and appends exactly
    one LF without a BOM.
    """

    __slots__ = ()

    def execute(self, task: HarnessTask) -> bytes:
        """Return canonical Task JSON.

        Parameters
        ----------
        task
            Exact immutable Task to serialize.

        Returns
        -------
        bytes
            Canonical UTF-8 JSON with exactly one final LF.

        Raises
        ------
        TypeError
            If ``task`` is not exactly :class:`HarnessTask`.
        """
        if type(task) is not HarnessTask:
            raise TypeError("task must be HarnessTask")
        obj = {field.name: getattr(task, field.name) for field in fields(HarnessTask)}
        return (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


class HarnessTaskDeserializer:
    """Deserialize strict schema-version-2 Task JSON from explicit bytes.

    Noncanonical whitespace and object-key order are accepted. BOMs, invalid UTF-8,
    duplicate, missing, or unknown keys, wrong JSON types, invalid lexical values,
    and unsupported versions are rejected. The action performs no file I/O or graph,
    authority, documentation, or activation validation.
    """

    __slots__ = ()

    def execute(self, payload: bytes) -> HarnessTask:
        """Return the represented Task.

        Parameters
        ----------
        payload
            Exact built-in bytes containing one UTF-8 JSON object.

        Returns
        -------
        HarnessTask
            Immutable validated Task.

        Raises
        ------
        TypeError
            If bytes or represented JSON fields have wrong semantic types.
        ValueError
            If decoding, key closure, lexical, or intrinsic value checks fail.
        """
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        if payload.startswith(b"\xef\xbb\xbf"):
            raise ValueError("payload must not contain a UTF-8 BOM")

        def object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
            result: dict[str, Any] = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f"duplicate JSON key {key}")
                result[key] = value
            return result

        try:
            value = json.loads(payload.decode("utf-8"), object_pairs_hook=object_pairs)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("payload must be one UTF-8 JSON value") from exc
        if type(value) is not dict:
            raise TypeError("payload must represent a JSON object")
        expected = tuple(field.name for field in fields(HarnessTask))
        missing = set(expected) - set(value)
        unknown = set(value) - set(expected)
        if missing:
            raise ValueError(f"missing field {sorted(missing)[0]}")
        if unknown:
            raise ValueError(f"unknown field {sorted(unknown)[0]}")
        tuple_fields = {
            "task_prerequisite_ids",
            "external_prerequisite_ids",
            "authority_reference_paths",
            "authorized_scope",
            "completion_criteria",
            "exclusions",
        }
        for name in tuple_fields:
            if type(value[name]) is not list:
                raise TypeError(f"{name} must be a JSON array")
            value[name] = tuple(value[name])
        return HarnessTask(**value)


class HarnessTaskGraphValidator:
    """Validate structural relations among explicitly supplied Tasks.

    Results use existing project-local :class:`LocalValidationResult` and
    ``PIHL.TASK.*`` issue codes.  Codes are ordered lexically by the existing
    result contract; no lifecycle, chain-selection, or repository policy is
    inferred.
    """

    __slots__ = ()

    def execute(self, tasks: tuple[HarnessTask, ...]) -> LocalValidationResult:
        """Return deterministic findings for one complete explicit Task graph.

        Parameters
        ----------
        tasks
            Exact nonempty tuple treated as the complete graph.

        Returns
        -------
        LocalValidationResult
            ``PASS`` or lexically ordered issues using ``PIHL.TASK.DUPLICATE_ID``,
            ``PARENT_MISSING``, ``PARENT_CYCLE``, ``PREREQUISITE_MISSING``,
            ``PREREQUISITE_CYCLE``, ``INTAKE_PATH_DUPLICATE``, and
            ``DOCUMENTATION_PATH_DUPLICATE`` under the ``PIHL.TASK`` namespace.

        Raises
        ------
        TypeError
            If the tuple or a member has the wrong semantic type.
        ValueError
            If the explicit Task tuple is empty.

        Notes
        -----
        Issue precedence is lexical ``(code, path-or-empty, detail)`` order. Status
        meaning, chain selection, activation, repository discovery, and I/O are
        excluded.
        """
        _require_tuple(tasks, "tasks")
        if not tasks:
            raise ValueError("tasks must be nonempty")
        if any(type(task) is not HarnessTask for task in tasks):
            raise TypeError("tasks must contain HarnessTask")
        issues: list[LocalIssue] = []
        by_id: dict[str, HarnessTask] = {}
        for task in tasks:
            if task.task_id in by_id:
                issues.append(LocalIssue("PIHL.TASK.DUPLICATE_ID", None, task.task_id))
            else:
                by_id[task.task_id] = task
        for task in tasks:
            if task.parent_task_id is not None and task.parent_task_id not in by_id:
                issues.append(
                    LocalIssue(
                        "PIHL.TASK.PARENT_MISSING",
                        task.documentation_path,
                        task.parent_task_id,
                    )
                )
            for dependency in task.task_prerequisite_ids:
                if dependency not in by_id:
                    issues.append(
                        LocalIssue(
                            "PIHL.TASK.PREREQUISITE_MISSING",
                            task.documentation_path,
                            dependency,
                        )
                    )
        for attribute, code in (
            ("intake_path", "PIHL.TASK.INTAKE_PATH_DUPLICATE"),
            ("documentation_path", "PIHL.TASK.DOCUMENTATION_PATH_DUPLICATE"),
        ):
            seen: dict[str, str] = {}
            for task in tasks:
                path = getattr(task, attribute)
                if path in seen:
                    issues.append(
                        LocalIssue(code, path, f"{seen[path]},{task.task_id}")
                    )
                else:
                    seen[path] = task.task_id
        issues.extend(self._cycle_issues(by_id, parent=True))
        issues.extend(self._cycle_issues(by_id, parent=False))
        ordered = tuple(
            sorted(set(issues), key=lambda x: (x.code, x.path or "", x.detail))
        )
        return LocalValidationResult("FAIL" if ordered else "PASS", ordered)

    @staticmethod
    def _cycle_issues(
        by_id: dict[str, HarnessTask], *, parent: bool
    ) -> list[LocalIssue]:
        code = "PIHL.TASK.PARENT_CYCLE" if parent else "PIHL.TASK.PREREQUISITE_CYCLE"
        graph = {
            task_id: (
                (task.parent_task_id,)
                if parent and task.parent_task_id in by_id
                else ()
            )
            if parent
            else tuple(x for x in task.task_prerequisite_ids if x in by_id)
            for task_id, task in by_id.items()
        }
        cycles: set[tuple[str, ...]] = set()
        completed: set[str] = set()
        for root in sorted(graph):
            if root in completed:
                continue
            path: list[str] = [root]
            positions = {root: 0}
            stack: list[tuple[str, int]] = [(root, 0)]
            while stack:
                node, child_index = stack[-1]
                children = graph[node]
                if child_index >= len(children):
                    completed.add(node)
                    stack.pop()
                    positions.pop(node)
                    path.pop()
                    continue
                child = children[child_index]
                stack[-1] = (node, child_index + 1)
                if child in positions:
                    cycle = path[positions[child] :]
                    rotations = [
                        tuple(cycle[index:] + cycle[:index])
                        for index in range(len(cycle))
                    ]
                    cycles.add(min(rotations))
                elif child not in completed:
                    positions[child] = len(path)
                    path.append(child)
                    stack.append((child, 0))
        return [LocalIssue(code, None, ",".join(cycle)) for cycle in sorted(cycles)]


@dataclass(frozen=True, slots=True)
class HarnessTaskDocumentSource:
    """Bind exact source bytes to repository-facing identity metadata.

    Parameters
    ----------
    path
        Accepted resource path naming the source.
    revision
        Project-local identifier for the retained source revision.
    git_object
        Optional 40-character lowercase hexadecimal Git object name.
    content
        Exact built-in source bytes.
    byte_count
        Nonnegative built-in integer equal to ``len(content)``.
    artifact_identity
        SHA-256 identity that must match ``content``.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If lexical, count, Git-object, or identity agreement fails.
    """

    path: ResourcePath
    revision: Identifier
    git_object: str | None
    content: bytes
    byte_count: int
    artifact_identity: ArtifactIdentity

    def __post_init__(self) -> None:
        _require_path(self.path, "path")
        _require_local_identifier(self.revision, "revision")
        if self.git_object is not None:
            _require_builtin_str(self.git_object, "git_object")
            if _GIT_OBJECT.fullmatch(self.git_object) is None:
                raise ValueError(
                    "git_object must contain 40 lowercase hexadecimal characters"
                )
        if type(self.content) is not bytes:
            raise TypeError("content must be bytes")
        if _require_int(self.byte_count, "byte_count", minimum=0) != len(self.content):
            raise ValueError("byte_count must equal len(content)")
        if type(self.artifact_identity) is not ArtifactIdentity:
            raise TypeError("artifact_identity must be ArtifactIdentity")
        if self.artifact_identity != _sha256(self.content):
            raise ValueError("artifact_identity must identify content")


class HarnessTaskSourceDisposition(StrEnum):
    """Classify the primary ownership of one exact source span.

    ``CANONICAL_TASK_INFORMATION`` maps operational Task data;
    ``DOCUMENTATION_OWNED_CONTENT`` requires exact byte preservation;
    ``HISTORICAL_EVIDENCE`` retains evidentiary material; and
    ``PROPOSED_REMOVAL`` is only a proposal requiring file-specific human review.
    """

    CANONICAL_TASK_INFORMATION = "CANONICAL_TASK_INFORMATION"
    DOCUMENTATION_OWNED_CONTENT = "DOCUMENTATION_OWNED_CONTENT"
    HISTORICAL_EVIDENCE = "HISTORICAL_EVIDENCE"
    PROPOSED_REMOVAL = "PROPOSED_REMOVAL"


@dataclass(frozen=True, slots=True)
class HarnessTaskSourceMapping:
    """Represent one half-open exact source span and proposed destinations.

    Parameters
    ----------
    mapping_id
        Unique project-local identifier within a prepared request.
    source_identity, span_identity
        Identities for the complete source and exact selected span.
    start_byte, end_byte
        Nonnegative built-in integer bounds with ``end_byte > start_byte``.
    disposition
        Closed primary-ownership classification.
    target_references
        Ordered unique nonempty destination references.
    transformation, rationale
        Nonempty exact proposed transformation and explanation text.

    Notes
    -----
    Source bounds and identities are checked against source bytes by the comparator
    and packet preparer rather than this intrinsic constructor.
    """

    mapping_id: Identifier
    source_identity: ArtifactIdentity
    start_byte: int
    end_byte: int
    span_identity: ArtifactIdentity
    disposition: HarnessTaskSourceDisposition
    target_references: tuple[str, ...]
    transformation: str
    rationale: str

    def __post_init__(self) -> None:
        _require_local_identifier(self.mapping_id, "mapping_id")
        if type(self.source_identity) is not ArtifactIdentity:
            raise TypeError("source_identity must be ArtifactIdentity")
        start = _require_int(self.start_byte, "start_byte", minimum=0)
        end = _require_int(self.end_byte, "end_byte", minimum=0)
        if end <= start:
            raise ValueError("end_byte must be greater than start_byte")
        if type(self.span_identity) is not ArtifactIdentity:
            raise TypeError("span_identity must be ArtifactIdentity")
        if type(self.disposition) is not HarnessTaskSourceDisposition:
            raise TypeError("disposition must be HarnessTaskSourceDisposition")
        target_references = _text_tuple(self.target_references, "target_references")
        _require_builtin_str(self.transformation, "transformation")
        _require_builtin_str(self.rationale, "rationale")
        object.__setattr__(self, "target_references", target_references)


@dataclass(frozen=True, slots=True)
class HarnessTaskDocumentationContent:
    """Store exact documentation-owned byte blocks in source order.

    Parameters
    ----------
    source_identity
        Identity of the complete source from which blocks were selected.
    documentation_path
        Accepted destination resource path.
    content_mapping_ids
        Ordered unique nonempty identifiers aligned one-to-one with blocks.
    content_blocks
        Ordered nonempty tuple of exact nonempty built-in bytes. Blocks are opaque:
        they need not be UTF-8 and are not template-parsed.
    """

    source_identity: ArtifactIdentity
    documentation_path: ResourcePath
    content_mapping_ids: tuple[Identifier, ...]
    content_blocks: tuple[bytes, ...]

    def __post_init__(self) -> None:
        if type(self.source_identity) is not ArtifactIdentity:
            raise TypeError("source_identity must be ArtifactIdentity")
        _require_path(self.documentation_path, "documentation_path")
        _require_tuple(self.content_mapping_ids, "content_mapping_ids")
        mapping_ids = tuple(self.content_mapping_ids)
        if not mapping_ids:
            raise ValueError("content_mapping_ids must be nonempty")
        for mapping_id in mapping_ids:
            _require_local_identifier(mapping_id, "content_mapping_ids item")
        if len(set(mapping_ids)) != len(mapping_ids):
            raise ValueError("content_mapping_ids must be unique")
        _require_tuple(self.content_blocks, "content_blocks")
        blocks = tuple(self.content_blocks)
        if not blocks:
            raise ValueError("content_blocks must be nonempty")
        if any(type(block) is not bytes for block in blocks):
            raise TypeError("content_blocks must contain bytes")
        if any(not block for block in blocks):
            raise ValueError("content_blocks must be nonempty")
        if len(mapping_ids) != len(blocks):
            raise ValueError("content_mapping_ids and content_blocks must align")
        object.__setattr__(self, "content_mapping_ids", mapping_ids)
        object.__setattr__(self, "content_blocks", blocks)


@dataclass(frozen=True, slots=True)
class HarnessTaskProjectionProfile:
    """Represent one explicit authoritative Markdown template.

    Parameters
    ----------
    schema_version
        Built-in integer equal to 1.
    profile_id
        Project-local profile identifier.
    template_bytes
        Sole authoritative exact nonempty template representation.
    template_identity
        SHA-256 identity matching ``template_bytes``.
    final_lf
        Exact Boolean policy for one final LF versus no final LF.

    Notes
    -----
    Syntax parsing and Task/content compatibility belong to the renderer. No
    template or parser state is discovered from files or globals.
    """

    schema_version: int
    profile_id: Identifier
    template_bytes: bytes
    template_identity: ArtifactIdentity
    final_lf: bool

    def __post_init__(self) -> None:
        if _require_int(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        _require_local_identifier(self.profile_id, "profile_id")
        if type(self.template_bytes) is not bytes:
            raise TypeError("template_bytes must be bytes")
        if not self.template_bytes:
            raise ValueError("template_bytes must be nonempty")
        if type(self.template_identity) is not ArtifactIdentity:
            raise TypeError("template_identity must be ArtifactIdentity")
        if self.template_identity != _sha256(self.template_bytes):
            raise ValueError("template_identity must identify template_bytes")
        _require_bool(self.final_lf, "final_lf")


@dataclass(frozen=True, slots=True)
class HarnessTaskDocumentation:
    """Represent complete rendered Markdown and its exact byte identity.

    Parameters
    ----------
    path
        Accepted destination resource path.
    content
        Exact complete rendered built-in bytes.
    artifact_identity
        SHA-256 identity matching ``content``.
    """

    path: ResourcePath
    content: bytes
    artifact_identity: ArtifactIdentity

    def __post_init__(self) -> None:
        _require_path(self.path, "path")
        if type(self.content) is not bytes:
            raise TypeError("content must be bytes")
        if type(self.artifact_identity) is not ArtifactIdentity:
            raise TypeError("artifact_identity must be ArtifactIdentity")
        if self.artifact_identity != _sha256(self.content):
            raise ValueError("artifact_identity must identify content")


class HarnessTaskDocumentationRenderer:
    """Render complete Markdown from explicit Task, content, and profile inputs.

    Template tokens use ``{{task.FIELD}}`` and ``{{content.MAPPING_ID}}``.  Every
    documentation content block must occur exactly once; Task values use stable
    plain-text formatting.  This implementation does not claim that rendering is
    a human-accepted migration.
    """

    __slots__ = ()

    def execute(
        self,
        task: HarnessTask,
        content: HarnessTaskDocumentationContent,
        profile: HarnessTaskProjectionProfile,
    ) -> HarnessTaskDocumentation:
        """Return complete rendered Markdown from explicit inputs.

        Parameters
        ----------
        task
            Canonical Task values referenced by ``{{task.FIELD}}`` tokens.
        content
            Opaque blocks referenced once each by ``{{content.MAPPING_ID}}`` tokens.
        profile
            UTF-8 template bytes and exact final-LF policy.

        Returns
        -------
        HarnessTaskDocumentation
            Complete rendered bytes and recalculated identity.

        Raises
        ------
        TypeError
            If an input has the wrong exact public type.
        ValueError
            If paths disagree; template UTF-8, token grammar, token names, content
            cardinality, or final-LF policy fails.

        Notes
        -----
        Task tuples format as Markdown bullets, Booleans as lowercase JSON text,
        ``None`` as ``None``, and other values as exact strings. Only template bytes
        are parsed. Inserted documentation blocks remain byte-opaque and are never
        reparsed. Rendering establishes no migration or human acceptance.
        """
        if type(task) is not HarnessTask:
            raise TypeError("task must be HarnessTask")
        if type(content) is not HarnessTaskDocumentationContent:
            raise TypeError("content must be HarnessTaskDocumentationContent")
        if type(profile) is not HarnessTaskProjectionProfile:
            raise TypeError("profile must be HarnessTaskProjectionProfile")
        if task.documentation_path != content.documentation_path:
            raise ValueError("Task and documentation paths must agree")
        try:
            profile.template_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("template_bytes must be UTF-8") from exc
        blocks = dict(
            zip(content.content_mapping_ids, content.content_blocks, strict=True)
        )
        counts = {identifier: 0 for identifier in blocks}
        task_fields = {field.name for field in fields(HarnessTask)}

        def replace(match: re.Match[bytes]) -> bytes:
            kind = match.group(1).decode("ascii")
            name = match.group(2).decode("ascii")
            if kind == "content":
                if name not in blocks:
                    raise ValueError(f"template names unknown content mapping {name}")
                counts[name] += 1
                return blocks[name]
            if name not in task_fields:
                raise ValueError(f"template names unknown Task field {name}")
            return self._format_task_value(getattr(task, name)).encode("utf-8")

        template_without_tokens = _TEMPLATE_TOKEN.sub(b"", profile.template_bytes)
        if b"{{" in template_without_tokens or b"}}" in template_without_tokens:
            raise ValueError("template contains unsupported or unclosed token")
        payload = _TEMPLATE_TOKEN.sub(replace, profile.template_bytes)
        if any(count != 1 for count in counts.values()):
            raise ValueError("every documentation block must occur exactly once")
        if profile.final_lf:
            if not payload.endswith(b"\n") or payload.endswith(b"\n\n"):
                raise ValueError("rendered bytes must have exactly one final LF")
        elif payload.endswith(b"\n"):
            raise ValueError("rendered bytes must not have a final LF")
        return HarnessTaskDocumentation(
            task.documentation_path, payload, _sha256(payload)
        )

    @staticmethod
    def _format_task_value(value: object) -> str:
        if value is None:
            return "None"
        if type(value) is bool:
            return "true" if value else "false"
        if type(value) is tuple:
            return "\n".join(f"- {item}" for item in value) if value else "- None"
        return str(value)


@dataclass(frozen=True, slots=True)
class HarnessTaskDocumentationComparisonResult:
    """Record exact byte differences and mapping-coverage findings.

    Parameters
    ----------
    status
        One of ``EXACT``, ``MAPPED_DIFFERENCES``, or ``UNMAPPED_DIFFERENCES``.
    source_identity, rendered_identity
        Exact identities of compared source and rendered bytes.
    differences
        Ordered unique byte-opcode descriptions in source order.
    findings
        Findings sorted by unique finding identifier.
    unmapped_spans
        Sorted unique nonempty half-open source-byte ranges.
    limitations
        Sorted unique claim-boundary statements.
    """

    status: Identifier
    source_identity: ArtifactIdentity
    rendered_identity: ArtifactIdentity
    differences: tuple[str, ...]
    findings: tuple[HumanReviewFinding, ...]
    unmapped_spans: tuple[tuple[int, int], ...]
    limitations: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_builtin_str(self.status, "status")
        if self.status not in _COMPARISON_STATUSES:
            raise ValueError("unsupported comparison status")
        if type(self.source_identity) is not ArtifactIdentity:
            raise TypeError("source_identity must be ArtifactIdentity")
        if type(self.rendered_identity) is not ArtifactIdentity:
            raise TypeError("rendered_identity must be ArtifactIdentity")
        differences = _text_tuple(self.differences, "differences", nonempty=False)
        if len(set(differences)) != len(differences):
            raise ValueError("differences must be unique")
        _require_tuple(self.findings, "findings")
        findings = tuple(self.findings)
        if any(type(item) is not HumanReviewFinding for item in findings):
            raise TypeError("findings must contain HumanReviewFinding")
        finding_ids = tuple(item.finding_id for item in findings)
        if finding_ids != tuple(sorted(set(finding_ids))):
            raise ValueError("findings must have sorted unique finding IDs")
        _require_tuple(self.unmapped_spans, "unmapped_spans")
        spans = tuple(self.unmapped_spans)
        for span in spans:
            if type(span) is not tuple or len(span) != 2:
                raise TypeError("unmapped_spans entries must be pairs")
            start = _require_int(span[0], "unmapped span start", minimum=0)
            end = _require_int(span[1], "unmapped span end", minimum=0)
            if end <= start:
                raise ValueError("unmapped spans must be nonempty")
        if spans != tuple(sorted(set(spans))):
            raise ValueError("unmapped_spans must be sorted and unique")
        limitations = _text_tuple(self.limitations, "limitations", nonempty=False)
        if limitations != tuple(sorted(limitations)):
            raise ValueError("limitations must be sorted")
        object.__setattr__(self, "differences", differences)
        object.__setattr__(self, "findings", findings)
        object.__setattr__(self, "unmapped_spans", spans)
        object.__setattr__(self, "limitations", limitations)


class HarnessTaskDocumentationComparator:
    """Compare source and rendered bytes without semantic-acceptance claims."""

    __slots__ = ()

    def execute(
        self,
        source: HarnessTaskDocumentSource,
        rendered: HarnessTaskDocumentation,
        mappings: tuple[HarnessTaskSourceMapping, ...],
    ) -> HarnessTaskDocumentationComparisonResult:
        """Report exact diffs, coverage, and block preservation.

        Parameters
        ----------
        source, rendered
            Exact source and rendered byte objects.
        mappings
            Nonempty ordered source mappings. They must be nonoverlapping, in range,
            source-identity compatible, and span-identity compatible.

        Returns
        -------
        HarnessTaskDocumentationComparisonResult
            SequenceMatcher byte opcodes, coverage gaps, ordered block-preservation
            failures, deterministic findings, and explicit limitations.

        Raises
        ------
        TypeError
            If inputs have wrong semantic types.
        ValueError
            If mappings are empty, overlap, exceed source bytes, or disagree with
            exact source identities.

        Notes
        -----
        With complete valid source mappings, zero-width rendered insertions and
        represented replacements are mechanically mapped. Coverage gaps or changed
        documentation-owned blocks are unmapped. This structural result cannot
        establish semantic correctness or human acceptance.
        """
        if type(source) is not HarnessTaskDocumentSource:
            raise TypeError("source must be HarnessTaskDocumentSource")
        if type(rendered) is not HarnessTaskDocumentation:
            raise TypeError("rendered must be HarnessTaskDocumentation")
        _require_tuple(mappings, "mappings")
        if not mappings:
            raise ValueError("mappings must be nonempty")
        if any(type(x) is not HarnessTaskSourceMapping for x in mappings):
            raise TypeError("mappings must contain HarnessTaskSourceMapping")
        coverage_gaps = self._coverage_gaps(source, mappings)
        matcher = difflib.SequenceMatcher(
            None, source.content, rendered.content, autojunk=False
        )
        differences: list[str] = []
        unmapped = list(coverage_gaps)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                continue
            differences.append(f"{tag}:source[{i1}:{i2}]->rendered[{j1}:{j2}]")
            if i1 != i2 and not self._covered(i1, i2, mappings):
                unmapped.append((i1, i2))
        rendered_cursor = 0
        for mapping in mappings:
            if (
                mapping.disposition
                is HarnessTaskSourceDisposition.DOCUMENTATION_OWNED_CONTENT
            ):
                block = source.content[mapping.start_byte : mapping.end_byte]
                occurrence = rendered.content.find(block, rendered_cursor)
                if occurrence < 0:
                    differences.append(
                        f"documentation-block-changed:{mapping.mapping_id}"
                    )
                    unmapped.append((mapping.start_byte, mapping.end_byte))
                else:
                    rendered_cursor = occurrence + len(block)
        unmapped_tuple = tuple(sorted(set(unmapped)))
        findings: tuple[HumanReviewFinding, ...] = ()
        if unmapped_tuple:
            findings = (
                HumanReviewFinding(
                    "harness-task-documentation-unmapped-difference",
                    "high",
                    "Rendered documentation contains differences outside "
                    "accepted mechanical coverage.",
                    rendered.path,
                    (),
                    "Human review is required; byte comparison does not "
                    "establish semantic correctness.",
                ),
            )
        if source.content == rendered.content:
            status = "EXACT"
        elif unmapped_tuple:
            status = "UNMAPPED_DIFFERENCES"
        else:
            status = "MAPPED_DIFFERENCES"
        limitations = (
            "Mapped differences are mechanical coverage only and do not establish "
            "semantic correctness or human acceptance.",
        )
        return HarnessTaskDocumentationComparisonResult(
            status,
            source.artifact_identity,
            rendered.artifact_identity,
            tuple(differences),
            findings,
            unmapped_tuple,
            limitations,
        )

    @staticmethod
    def _coverage_gaps(
        source: HarnessTaskDocumentSource,
        mappings: tuple[HarnessTaskSourceMapping, ...],
    ) -> tuple[tuple[int, int], ...]:
        gaps: list[tuple[int, int]] = []
        position = 0
        for mapping in mappings:
            if mapping.source_identity != source.artifact_identity:
                raise ValueError("mapping source identity differs from source")
            if mapping.start_byte > position:
                gaps.append((position, mapping.start_byte))
            if mapping.start_byte < position:
                raise ValueError("mappings must be ordered and nonoverlapping")
            if mapping.end_byte > source.byte_count:
                raise ValueError("mapping exceeds source bytes")
            span = source.content[mapping.start_byte : mapping.end_byte]
            if mapping.span_identity != _sha256(span):
                raise ValueError("mapping span identity differs from source bytes")
            position = mapping.end_byte
        if position < source.byte_count:
            gaps.append((position, source.byte_count))
        return tuple(gaps)

    @staticmethod
    def _covered(
        start: int,
        end: int,
        mappings: tuple[HarnessTaskSourceMapping, ...],
    ) -> bool:
        position = start
        for mapping in mappings:
            if mapping.end_byte <= position:
                continue
            if mapping.start_byte > position:
                return False
            position = min(end, mapping.end_byte)
            if position == end:
                return True
        return position == end


@dataclass(frozen=True, slots=True)
class HarnessTaskMigrationReviewPacketRequest:
    """Contain every explicit runtime input needed to prepare one packet.

    Parameters
    ----------
    source, mappings
        Exact source and its nonempty proposed source mapping tuple.
    candidate_task, canonical_task_json
        Candidate Task and claimed canonical serialized bytes.
    documentation_content, projection_profile, rendered_documentation
        Explicit rendering inputs and claimed output.
    comparison
        Claimed deterministic byte comparison.
    human_review_packet
        Exact generic immutable packet to present for human disposition.

    Notes
    -----
    This runtime-only DataObject checks exact member types. Cross-object agreement
    belongs exclusively to :class:`HarnessTaskMigrationReviewPacketPreparer`.
    """

    source: HarnessTaskDocumentSource
    mappings: tuple[HarnessTaskSourceMapping, ...]
    candidate_task: HarnessTask
    canonical_task_json: bytes
    documentation_content: HarnessTaskDocumentationContent
    projection_profile: HarnessTaskProjectionProfile
    rendered_documentation: HarnessTaskDocumentation
    comparison: HarnessTaskDocumentationComparisonResult
    human_review_packet: HumanReviewPacket

    def __post_init__(self) -> None:
        expected = (
            (self.source, HarnessTaskDocumentSource, "source"),
            (self.candidate_task, HarnessTask, "candidate_task"),
            (
                self.documentation_content,
                HarnessTaskDocumentationContent,
                "documentation_content",
            ),
            (
                self.projection_profile,
                HarnessTaskProjectionProfile,
                "projection_profile",
            ),
            (
                self.rendered_documentation,
                HarnessTaskDocumentation,
                "rendered_documentation",
            ),
            (self.comparison, HarnessTaskDocumentationComparisonResult, "comparison"),
            (self.human_review_packet, HumanReviewPacket, "human_review_packet"),
        )
        for value, kind, name in expected:
            if type(value) is not kind:
                raise TypeError(f"{name} must be {kind.__name__}")
        _require_tuple(self.mappings, "mappings")
        if not self.mappings:
            raise ValueError("mappings must be nonempty")
        if any(type(x) is not HarnessTaskSourceMapping for x in self.mappings):
            raise TypeError("mappings must contain HarnessTaskSourceMapping")
        if type(self.canonical_task_json) is not bytes:
            raise TypeError("canonical_task_json must be bytes")


class HarnessTaskMigrationReviewPacketPreparer:
    """Validate one explicit request and produce an immutable packet."""

    __slots__ = ()

    def execute(
        self, request: HarnessTaskMigrationReviewPacketRequest
    ) -> HarnessTaskMigrationReviewPacket:
        """Return a packet after all accepted cross-object checks pass.

        Parameters
        ----------
        request
            Exact explicit runtime request bundle.

        Returns
        -------
        HarnessTaskMigrationReviewPacket
            Immutable packet retaining the exact request.

        Raises
        ------
        TypeError
            If ``request`` has the wrong exact type.
        ValueError
            If mapping identifiers, complete coverage, source/span identities,
            canonical JSON, documentation IDs/blocks/targets, rendering, comparison,
            generic packet canonicality, target revision, or target paths disagree.

        Notes
        -----
        Preparation performs no discovery, persistence, mutation, activation,
        migration, successor selection, or human-response interpretation.
        """
        if type(request) is not HarnessTaskMigrationReviewPacketRequest:
            raise TypeError("request must be HarnessTaskMigrationReviewPacketRequest")
        source = request.source
        mapping_ids = tuple(mapping.mapping_id for mapping in request.mappings)
        if len(set(mapping_ids)) != len(mapping_ids):
            raise ValueError("mapping IDs must be unique")
        comparator = HarnessTaskDocumentationComparator()
        comparator._coverage_gaps(source, request.mappings)
        if (
            request.mappings[0].start_byte != 0
            or request.mappings[-1].end_byte != source.byte_count
        ):
            raise ValueError("mappings must completely cover source bytes")
        canonical = HarnessTaskSerializer().execute(request.candidate_task)
        if request.canonical_task_json != canonical:
            raise ValueError("canonical_task_json differs from serializer output")
        content = request.documentation_content
        if content.source_identity != source.artifact_identity:
            raise ValueError("documentation content source identity differs")
        expected_documentation = tuple(
            mapping
            for mapping in request.mappings
            if mapping.disposition
            is HarnessTaskSourceDisposition.DOCUMENTATION_OWNED_CONTENT
        )
        if content.content_mapping_ids != tuple(
            x.mapping_id for x in expected_documentation
        ):
            raise ValueError("documentation mapping IDs differ from source mappings")
        if any(
            content.documentation_path not in mapping.target_references
            for mapping in expected_documentation
        ):
            raise ValueError(
                "documentation mapping targets must include documentation_path"
            )
        expected_blocks = tuple(
            source.content[x.start_byte : x.end_byte] for x in expected_documentation
        )
        if content.content_blocks != expected_blocks:
            raise ValueError("documentation blocks differ from source spans")
        rendered = HarnessTaskDocumentationRenderer().execute(
            request.candidate_task, content, request.projection_profile
        )
        if rendered != request.rendered_documentation:
            raise ValueError("rendered documentation differs from renderer output")
        comparison = comparator.execute(source, rendered, request.mappings)
        if comparison != request.comparison:
            raise ValueError("comparison differs from comparator output")
        review = request.human_review_packet
        canonical_review = HumanReviewPreparer().execute(
            review.target, review.observations, review.findings, review.limitations
        )
        if review != canonical_review:
            raise ValueError("human review packet is not canonical")
        if review.target.revision != source.revision:
            raise ValueError("human review target revision differs from source")
        if (
            source.path not in review.target.paths
            or rendered.path not in review.target.paths
        ):
            raise ValueError(
                "human review target paths must include source and rendered paths"
            )
        return HarnessTaskMigrationReviewPacket(request)


@dataclass(frozen=True, slots=True)
class HarnessTaskMigrationReviewPacket:
    """Represent one validated exact migration-review request bundle.

    Parameters
    ----------
    request
        Exact request already validated by the packet preparer.

    Notes
    -----
    Direct construction checks only type. Use the preparer for cross-object
    validation. Packet existence does not authorize migration.
    """

    request: HarnessTaskMigrationReviewPacketRequest

    def __post_init__(self) -> None:
        if type(self.request) is not HarnessTaskMigrationReviewPacketRequest:
            raise TypeError("request must be HarnessTaskMigrationReviewPacketRequest")


class HarnessTaskMigrationDisposition(StrEnum):
    """Represent the closed migration-specific human disposition.

    ``ACCEPT_FILE_MIGRATION`` accepts only the reviewed file;
    ``REVISE_CONTRACT_OR_MAPPING`` requests bounded correction;
    ``RETAIN_DOCUMENTATION_OWNERSHIP`` rejects the
    proposed transfer; and ``DEFER_FILE`` records no present decision. Enum values do
    not themselves establish human authority or mutate files.
    """

    ACCEPT_FILE_MIGRATION = "ACCEPT_FILE_MIGRATION"
    REVISE_CONTRACT_OR_MAPPING = "REVISE_CONTRACT_OR_MAPPING"
    RETAIN_DOCUMENTATION_OWNERSHIP = "RETAIN_DOCUMENTATION_OWNERSHIP"
    DEFER_FILE = "DEFER_FILE"


@dataclass(frozen=True, slots=True)
class HarnessTaskMigrationFileDisposition:
    """Record an exact packet, generic human decision, and migration outcome.

    Parameters
    ----------
    packet
        Exact prepared migration-review packet.
    human_decision
        Generic immutable decision retaining the packet's generic review packet.
    migration_disposition
        Explicit migration-specific closed outcome.

    Notes
    -----
    Constructor ownership is type-only. Exact packet binding and compatibility belong
    to :class:`HarnessTaskMigrationFileDispositionRecorder`.
    """

    packet: HarnessTaskMigrationReviewPacket
    human_decision: HumanReviewDecision
    migration_disposition: HarnessTaskMigrationDisposition

    def __post_init__(self) -> None:
        if type(self.packet) is not HarnessTaskMigrationReviewPacket:
            raise TypeError("packet must be HarnessTaskMigrationReviewPacket")
        if type(self.human_decision) is not HumanReviewDecision:
            raise TypeError("human_decision must be HumanReviewDecision")
        if type(self.migration_disposition) is not HarnessTaskMigrationDisposition:
            raise TypeError(
                "migration_disposition must be HarnessTaskMigrationDisposition"
            )


class HarnessTaskMigrationFileDispositionRecorder:
    """Validate exact generic/migration decision agreement without interpretation."""

    __slots__ = ()

    _COMPATIBILITY = {
        "accepted": HarnessTaskMigrationDisposition.ACCEPT_FILE_MIGRATION,
        "bounded_correction": (
            HarnessTaskMigrationDisposition.REVISE_CONTRACT_OR_MAPPING
        ),
        "rejected": HarnessTaskMigrationDisposition.RETAIN_DOCUMENTATION_OWNERSHIP,
        "deferred": HarnessTaskMigrationDisposition.DEFER_FILE,
    }

    def execute(
        self,
        packet: HarnessTaskMigrationReviewPacket,
        human_decision: HumanReviewDecision,
        migration_disposition: HarnessTaskMigrationDisposition,
    ) -> HarnessTaskMigrationFileDisposition:
        """Return the exact compatible disposition without mutation.

        Parameters
        ----------
        packet, human_decision, migration_disposition
            Exact explicit packet, generic decision, and migration outcome.

        Returns
        -------
        HarnessTaskMigrationFileDisposition
            Immutable exact decision record.

        Raises
        ------
        TypeError
            If any input has the wrong exact public type.
        ValueError
            If the generic decision does not retain the packet's exact generic review
            packet or the dispositions violate the frozen compatibility table:
            accepted/accept, bounded-correction/revise, rejected/retain, and
            deferred/defer.

        Notes
        -----
        This action performs no text interpretation, authentication, persistence,
        filesystem mutation, migration, activation, or successor action.
        """
        if type(packet) is not HarnessTaskMigrationReviewPacket:
            raise TypeError("packet must be HarnessTaskMigrationReviewPacket")
        if type(human_decision) is not HumanReviewDecision:
            raise TypeError("human_decision must be HumanReviewDecision")
        if type(migration_disposition) is not HarnessTaskMigrationDisposition:
            raise TypeError(
                "migration_disposition must be HarnessTaskMigrationDisposition"
            )
        if human_decision.packet != packet.request.human_review_packet:
            raise ValueError(
                "human decision must retain the packet's exact review packet"
            )
        if self._COMPATIBILITY[human_decision.disposition] is not migration_disposition:
            raise ValueError("generic and migration dispositions are incompatible")
        return HarnessTaskMigrationFileDisposition(
            packet, human_decision, migration_disposition
        )
