"""Minimum durable project-local Task model.

``HarnessTask`` owns intrinsic Task state, its serializer and deserializer own the
version-3 JSON wire format, and ``HarnessTaskGraphValidator`` owns structural graph
checks. The module performs no
repository discovery, persistence, activation, Markdown rendering, migration
workflow, scientific interpretation, or human review.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, fields
from typing import Any

from ..identity import (
    Identifier,
    ResourcePath,
    _require_builtin_str,
    _require_path,
    _require_tuple,
)
from .models import LocalIssue, LocalValidationResult

_LOCAL_IDENTIFIER = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?\Z", re.ASCII
)


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
class ArchivedTaskSource:
    """Identify the exact archived Markdown source of a migrated Task."""

    path: ResourcePath
    sha256: str

    def __post_init__(self) -> None:
        _require_path(self.path, "archived_source path")
        digest = _require_builtin_str(self.sha256, "archived_source sha256")
        if re.fullmatch(r"[0-9a-f]{64}", digest, re.ASCII) is None:
            raise ValueError("archived_source sha256 must be 64 lowercase hex digits")


@dataclass(frozen=True, slots=True)
class HarnessTask:
    """Represent one canonical project-local Task.

    Parameters
    ----------
    schema_version
        Built-in integer equal to 3.
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
    superseded_by_task_ids
        Sorted unique replacement Task identifiers. The tuple excludes ``task_id``.
        It records identity succession only and grants no activation, prerequisite,
        parent, completion, or acceptance authority.
    explicit_activation_required
        Exact built-in Boolean; it records policy but does not activate work.
    authority_reference_paths
        Nonempty sorted unique accepted resource paths.
    authorized_scope, completion_criteria, exclusions
        Nonempty ordered tuples of unique nonempty text.
    intake_path
        Optional accepted resource path for separate non-executable intake. ``None``
        records that no separate intake artifact exists.
    archived_source
        Exact archive path and SHA-256 identity for a migrated Markdown Task, or
        ``None`` for a JSON-native Task.
    documentation_path
        Optional retained compatibility path for maintained prose.

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
    superseded_by_task_ids: tuple[Identifier, ...]
    explicit_activation_required: bool
    objective: str
    authority_reference_paths: tuple[ResourcePath, ...]
    authorized_scope: tuple[str, ...]
    completion_criteria: tuple[str, ...]
    exclusions: tuple[str, ...]
    intake_path: ResourcePath | None
    archived_source: ArchivedTaskSource | None = None
    documentation_path: ResourcePath | None = None

    def __post_init__(self) -> None:
        version = _require_int(self.schema_version, "schema_version")
        if version != 3:
            raise ValueError("schema_version must equal 3")
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
        superseded_by = _identifier_tuple(
            self.superseded_by_task_ids, "superseded_by_task_ids"
        )
        if self.task_id in task_prerequisites or self.task_id in external_prerequisites:
            raise ValueError("a Task may not require itself")
        if self.task_id in superseded_by:
            raise ValueError("a Task may not supersede itself")
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
        if self.intake_path is not None:
            _require_path(self.intake_path, "intake_path")
        if (
            self.archived_source is not None
            and type(self.archived_source) is not ArchivedTaskSource
        ):
            raise TypeError("archived_source must be ArchivedTaskSource or None")
        if self.documentation_path is not None:
            _require_path(self.documentation_path, "documentation_path")
        object.__setattr__(self, "task_prerequisite_ids", task_prerequisites)
        object.__setattr__(self, "external_prerequisite_ids", external_prerequisites)
        object.__setattr__(self, "superseded_by_task_ids", superseded_by)
        object.__setattr__(self, "authority_reference_paths", authority_paths)
        object.__setattr__(self, "authorized_scope", authorized_scope)
        object.__setattr__(self, "completion_criteria", completion_criteria)
        object.__setattr__(self, "exclusions", exclusions)


class HarnessTaskSerializer:
    """Serialize one :class:`HarnessTask` to canonical UTF-8 JSON bytes.

    The ActionObject is fieldless and performs no discovery or I/O. It emits the
    version-3 field set, tuples as arrays and optional absence as ``null``, uses
    two-space indentation with literal Unicode, and appends exactly one LF without
    a BOM.
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
        obj: dict[str, Any] = {}
        for field in fields(HarnessTask):
            value = getattr(task, field.name)
            if field.name == "documentation_path" and value is None:
                continue
            if type(value) is ArchivedTaskSource:
                value = {"path": value.path, "sha256": value.sha256}
            obj[field.name] = value
        return (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


class HarnessTaskDeserializer:
    """Deserialize strict schema-version-3 Task JSON.

    Noncanonical whitespace and object-key order are accepted. Version 3 requires
    ``superseded_by_task_ids``. BOMs, invalid UTF-8, duplicate, missing, or unknown
    keys, wrong JSON types, invalid lexical values, and unsupported versions are
    rejected. The action performs no file I/O or graph, authority, documentation,
    or activation validation.
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
        version = value.get("schema_version")
        if type(version) is not int or version != 3:
            raise ValueError("schema_version must equal integer 3")
        model_fields = tuple(field.name for field in fields(HarnessTask))
        expected = set(model_fields)
        required = expected - {"documentation_path"}
        missing = required - set(value)
        unknown = set(value) - expected
        if missing:
            raise ValueError(f"missing field {sorted(missing)[0]}")
        if unknown:
            raise ValueError(f"unknown field {sorted(unknown)[0]}")
        tuple_fields = {
            "task_prerequisite_ids",
            "external_prerequisite_ids",
            "superseded_by_task_ids",
            "authority_reference_paths",
            "authorized_scope",
            "completion_criteria",
            "exclusions",
        }
        for name in tuple_fields:
            if type(value[name]) is not list:
                raise TypeError(f"{name} must be a JSON array")
            value[name] = tuple(value[name])
        archived = value["archived_source"]
        if archived is not None:
            if type(archived) is not dict or set(archived) != {"path", "sha256"}:
                raise TypeError("archived_source must be a closed JSON object or null")
            value["archived_source"] = ArchivedTaskSource(**archived)
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
            ``PREREQUISITE_CYCLE``, ``SUPERSESSION_MISSING``,
            ``SUPERSESSION_CYCLE``, ``INTAKE_PATH_DUPLICATE``, and
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
                        task.documentation_path
                        or (
                            task.archived_source.path if task.archived_source else None
                        ),
                        task.parent_task_id,
                    )
                )
            task_path = task.documentation_path or (
                task.archived_source.path if task.archived_source else None
            )
            for dependency in task.task_prerequisite_ids:
                if dependency not in by_id:
                    issues.append(
                        LocalIssue(
                            "PIHL.TASK.PREREQUISITE_MISSING",
                            task_path,
                            dependency,
                        )
                    )
            for replacement in task.superseded_by_task_ids:
                if replacement not in by_id:
                    issues.append(
                        LocalIssue(
                            "PIHL.TASK.SUPERSESSION_MISSING",
                            task_path,
                            replacement,
                        )
                    )
        for attribute, code in (
            ("intake_path", "PIHL.TASK.INTAKE_PATH_DUPLICATE"),
            ("documentation_path", "PIHL.TASK.DOCUMENTATION_PATH_DUPLICATE"),
        ):
            seen: dict[str, str] = {}
            for task in tasks:
                path = getattr(task, attribute)
                if path is None:
                    continue
                if path in seen:
                    issues.append(
                        LocalIssue(code, path, f"{seen[path]},{task.task_id}")
                    )
                else:
                    seen[path] = task.task_id
        issues.extend(self._cycle_issues(by_id, relation="parent"))
        issues.extend(self._cycle_issues(by_id, relation="prerequisite"))
        issues.extend(self._cycle_issues(by_id, relation="supersession"))
        ordered = tuple(
            sorted(set(issues), key=lambda x: (x.code, x.path or "", x.detail))
        )
        return LocalValidationResult("FAIL" if ordered else "PASS", ordered)

    @staticmethod
    def _cycle_issues(
        by_id: dict[str, HarnessTask], *, relation: str
    ) -> list[LocalIssue]:
        code = {
            "parent": "PIHL.TASK.PARENT_CYCLE",
            "prerequisite": "PIHL.TASK.PREREQUISITE_CYCLE",
            "supersession": "PIHL.TASK.SUPERSESSION_CYCLE",
        }[relation]
        graph = {}
        for task_id, task in by_id.items():
            targets: tuple[str, ...]
            if relation == "parent":
                targets = (task.parent_task_id,) if task.parent_task_id in by_id else ()
            elif relation == "prerequisite":
                targets = tuple(x for x in task.task_prerequisite_ids if x in by_id)
            else:
                targets = tuple(x for x in task.superseded_by_task_ids if x in by_id)
            graph[task_id] = targets
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
