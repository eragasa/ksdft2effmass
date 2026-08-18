"""Minimum durable project-local Task model.

``HarnessTask`` owns intrinsic Task state, its serializer and deserializer own the
version-3 JSON wire format, and ``HarnessTaskRegistry`` owns immutable derived graph
queries. Structural normalized-state validation remains a separate boundary. The
module performs no repository discovery, persistence, activation, Markdown rendering,
migration workflow, scientific interpretation, or human review.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, fields
from typing import Any, TypeAlias

Identifier: TypeAlias = str  # noqa: UP040 - public contract uses built-in strings
ResourcePath: TypeAlias = str  # noqa: UP040

_DRIVE_RE = re.compile(r"^[A-Za-z]:")
_DEVICE_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def _require_builtin_str(value: object, field: str, *, nonempty: bool = True) -> str:
    if type(value) is not str:
        raise TypeError(f"{field} must be a built-in str")
    if nonempty and not value:
        raise ValueError(f"{field} must be nonempty")
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise ValueError(f"{field} contains an unpaired surrogate")
    return value


def _require_tuple(value: object, field: str) -> tuple[object, ...]:
    if type(value) is not tuple:
        raise TypeError(f"{field} must be a tuple")
    return value


def _require_path(value: object, field: str) -> str:
    if type(value) is not str:
        raise TypeError(f"{field} must be a built-in str")
    if not value:
        raise ValueError(f"PIH.PATH.EMPTY: {field} must be nonempty")
    if value.startswith("/"):
        raise ValueError(f"PIH.PATH.ABSOLUTE: {field} must be relative")
    if unicodedata.normalize("NFC", value) != value:
        raise ValueError(f"PIH.PATH.NONCANONICAL_UNICODE: {field} must be NFC")
    if _DRIVE_RE.match(value):
        raise ValueError(f"PIH.PATH.WINDOWS_SYNTAX: {field} has a drive prefix")
    if "\\" in value:
        code = (
            "PIH.PATH.WINDOWS_SYNTAX"
            if value.startswith("\\\\")
            else "PIH.PATH.INVALID_CHARACTER"
        )
        raise ValueError(f"{code}: {field} contains a backslash")
    if value.endswith("/") or "//" in value:
        raise ValueError(f"PIH.PATH.INVALID_SEGMENT: {field} has an empty segment")
    for part in value.split("/"):
        if part in {"", ".", ".."}:
            raise ValueError(
                f"PIH.PATH.INVALID_SEGMENT: {field} has a traversal segment"
            )
        stem = part.split(".", 1)[0].upper()
        if stem in _DEVICE_NAMES:
            raise ValueError(f"PIH.PATH.WINDOWS_SYNTAX: {field} has a device name")
    if any(
        ord(character) < 32
        or 0x7F <= ord(character) <= 0x9F
        or ord(character) in {0x2028, 0x2029}
        or 0xD800 <= ord(character) <= 0xDFFF
        for character in value
    ):
        raise ValueError(
            f"PIH.PATH.INVALID_CHARACTER: {field} has a prohibited character"
        )
    return value

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


@dataclass(frozen=True, slots=True)
class HarnessTaskRegistry:
    """Provide one immutable index over explicitly supplied canonical Tasks.

    Parameters
    ----------
    schema_version
        Registry contract version, fixed to ``1``.
    tasks
        Nonempty tuple of exact :class:`HarnessTask` values in increasing Task-ID
        order. Task records remain the authority for every represented field and
        graph edge; the registry stores no child list or independent topology.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If the version, ordering, uniqueness, or nonempty invariant fails.

    Notes
    -----
    The registry is an in-memory derived aggregate, not a serialized membership
    record, persistence boundary, selection state, chain, or activation authority.
    Cross-Task reference existence and cycle checks remain owned by
    :class:`HarnessTaskGraphValidator`.
    """

    schema_version: int
    tasks: tuple[HarnessTask, ...]

    def __post_init__(self) -> None:
        version = _require_int(self.schema_version, "schema_version")
        if version != 1:
            raise ValueError("schema_version must equal 1")
        _require_tuple(self.tasks, "tasks")
        if not self.tasks:
            raise ValueError("tasks must be nonempty")
        if any(type(task) is not HarnessTask for task in self.tasks):
            raise TypeError("tasks must contain HarnessTask")
        task_ids = tuple(task.task_id for task in self.tasks)
        if task_ids != tuple(sorted(set(task_ids))):
            raise ValueError("tasks must be unique and sorted by task_id")

    @property
    def task_ids(self) -> tuple[Identifier, ...]:
        """Return all registered identities in deterministic order."""
        return tuple(task.task_id for task in self.tasks)

    def task_by_id(self, task_id: Identifier) -> HarnessTask:
        """Return the exact registered Task identified by ``task_id``.

        Parameters
        ----------
        task_id
            Project-local identity of the required Task.

        Returns
        -------
        HarnessTask
            The exact object retained by the registry.

        Raises
        ------
        TypeError
            If ``task_id`` is not a built-in string.
        ValueError
            If ``task_id`` is lexically invalid or absent from the registry.
        """
        selected_id = _require_local_identifier(task_id, "task_id")
        for task in self.tasks:
            if task.task_id == selected_id:
                return task
        raise ValueError(f"unknown task_id {selected_id}")

    def child_task_ids(self, parent_task_id: Identifier) -> tuple[Identifier, ...]:
        """Return identities whose canonical ``parent_task_id`` names the parent.

        Parameters
        ----------
        parent_task_id
            Project-local identity of the registered parent Task.

        Returns
        -------
        tuple[Identifier, ...]
            Child identities in registry order. The result is derived on demand and
            is never stored as a second hierarchy representation.

        Raises
        ------
        TypeError
            If ``parent_task_id`` is not a built-in string.
        ValueError
            If ``parent_task_id`` is lexically invalid or absent from the registry.
        """
        parent = self.task_by_id(parent_task_id)
        return tuple(
            task.task_id for task in self.tasks if task.parent_task_id == parent.task_id
        )

    def descendant_task_ids(
        self, root_task_id: Identifier
    ) -> tuple[Identifier, ...]:
        """Return proper descendants in deterministic depth-first pre-order.

        Parameters
        ----------
        root_task_id
            Project-local identity of the registered root Task.

        Returns
        -------
        tuple[Identifier, ...]
            Every distinct Task reachable by one or more canonical
            ``parent_task_id`` edges. The root is excluded. Direct children are
            visited in registry order before each child's descendants.

        Raises
        ------
        TypeError
            If ``root_task_id`` is not a built-in string.
        ValueError
            If ``root_task_id`` is lexically invalid or absent, or reachable parent
            relations contain a cycle.

        Notes
        -----
        The query derives a read-only planning scope. It performs no repository
        discovery, graph validation, lifecycle interpretation, prerequisite
        resolution, selection, activation, or authority inference.
        """
        root = self.task_by_id(root_task_id)
        children_by_parent: dict[Identifier, list[Identifier]] = {}
        for task in self.tasks:
            if task.parent_task_id is not None:
                children_by_parent.setdefault(task.parent_task_id, []).append(
                    task.task_id
                )

        result: list[Identifier] = []
        visited = {root.task_id}
        stack = list(reversed(children_by_parent.get(root.task_id, ())))
        while stack:
            task_id = stack.pop()
            if task_id in visited:
                raise ValueError("reachable parent relations must not contain a cycle")
            visited.add(task_id)
            result.append(task_id)
            stack.extend(reversed(children_by_parent.get(task_id, ())))
        return tuple(result)

    def prerequisite_task_ids(self, task_id: Identifier) -> tuple[Identifier, ...]:
        """Return the canonical Task-prerequisite identities for one Task.

        Parameters
        ----------
        task_id
            Project-local identity of the registered Task.

        Returns
        -------
        tuple[Identifier, ...]
            The exact canonical ``task_prerequisite_ids`` tuple.

        Raises
        ------
        TypeError
            If ``task_id`` is not a built-in string.
        ValueError
            If ``task_id`` is lexically invalid or absent from the registry.
        """
        return self.task_by_id(task_id).task_prerequisite_ids


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


