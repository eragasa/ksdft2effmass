"""Bounded inspection of one explicitly selected durable task state."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .identity import (
    Identifier,
    ResourcePath,
    _require_builtin_str,
    _require_identifier,
    _require_path,
    _require_sorted_unique,
    _require_tuple,
    _require_version,
)
from .validation import ValidationIssue, ValidationResult, _issue, _result

_RECORD_STATUSES = {"not_declared", "declared_missing", "inspected"}


@dataclass(frozen=True, slots=True)
class TaskStateInspectionRequest:
    """Explicit filesystem boundary and exact task selection.

    Parameters
    ----------
    schema_version
        Request schema version, fixed to ``1``.
    repository_root
        Absolute, caller-selected repository boundary. The action rejects missing,
        noncanonical, and symlinked roots.
    chain_path
        Root-relative path of the one chain document to inspect.
    task_id
        Exact task identity to resolve from that chain.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If the version, root form, chain path, or task identity is invalid.
    """

    schema_version: int
    repository_root: Path
    chain_path: ResourcePath
    task_id: Identifier

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")
        _require_path(self.chain_path, "chain_path")
        _require_identifier(self.task_id, "task_id")


@dataclass(frozen=True, slots=True)
class TaskStateInspectionResult:
    """Immutable durable state and diagnostics from one bounded inspection.

    Attributes
    ----------
    schema_version
        Result schema version, fixed to ``1``.
    repository_root
        Absolute filesystem boundary used by the inspection.
    task_id, task_status, active_task_id
        Requested identity, resolved status, and chain-declared active identity. Status
        is absent when the requested task cannot be resolved.
    chain_path, task_record_path, ownership_manifest_path
        Exact declared root-relative control paths, when present.
    completion_validator_path, completion_command
        Exact completion declaration obtained from the ownership manifest.
    writers, reviewers
        Deterministically role/agent-sorted declared assignments.
    artifact_paths, run_record_paths, handoff_record_paths
        Sorted exact task-entry declarations; empty means no such path was declared.
    durable_run_record_status, durable_handoff_record_status
        ``not_declared``, ``declared_missing``, or ``inspected`` for each record kind.
    inspected_paths
        Sorted paths whose bounded filesystem state was inspected.
    read_paths
        Sorted subset of ``inspected_paths`` whose bytes were read.
    limitations
        Sorted conclusions explicitly outside declared repository state.
    validation
        Deterministically ordered structured invalid-reference findings.
    """

    schema_version: int
    repository_root: Path
    task_id: Identifier
    task_status: Identifier | None
    active_task_id: Identifier | None
    chain_path: ResourcePath
    task_record_path: ResourcePath | None
    ownership_manifest_path: ResourcePath | None
    completion_validator_path: ResourcePath | None
    completion_command: tuple[str, ...]
    writers: tuple[tuple[Identifier, Identifier], ...]
    reviewers: tuple[tuple[Identifier, Identifier], ...]
    artifact_paths: tuple[ResourcePath, ...]
    run_record_paths: tuple[ResourcePath, ...]
    handoff_record_paths: tuple[ResourcePath, ...]
    durable_run_record_status: str
    durable_handoff_record_status: str
    inspected_paths: tuple[ResourcePath, ...]
    read_paths: tuple[ResourcePath, ...]
    limitations: tuple[str, ...]
    validation: ValidationResult

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        if (
            not isinstance(self.repository_root, Path)
            or not self.repository_root.is_absolute()
        ):
            raise ValueError("repository_root must be an absolute pathlib.Path")
        _require_identifier(self.task_id, "task_id")
        if self.task_status is not None:
            _require_identifier(self.task_status, "task_status")
        if self.active_task_id is not None:
            _require_identifier(self.active_task_id, "active_task_id")
        for name in (
            "chain_path",
            "task_record_path",
            "ownership_manifest_path",
            "completion_validator_path",
        ):
            value = getattr(self, name)
            if value is not None:
                _require_path(value, name)
        _require_tuple(self.completion_command, "completion_command")
        for argument in self.completion_command:
            _require_builtin_str(argument, "completion_command item", nonempty=False)
        for name in ("writers", "reviewers"):
            values = getattr(self, name)
            _require_tuple(values, name)
            if tuple(sorted(values)) != values or len(set(values)) != len(values):
                raise ValueError(f"{name} must be unique and sorted")
            for role, agent in values:
                _require_identifier(role, f"{name} role")
                _require_identifier(agent, f"{name} agent")
        for name in (
            "artifact_paths",
            "run_record_paths",
            "handoff_record_paths",
            "inspected_paths",
            "read_paths",
        ):
            values = getattr(self, name)
            _require_tuple(values, name)
            for value in values:
                _require_path(value, f"{name} item")
            _require_sorted_unique(values, name)
        if not set(self.read_paths) <= set(self.inspected_paths):
            raise ValueError("read_paths must be a subset of inspected_paths")
        for name in ("durable_run_record_status", "durable_handoff_record_status"):
            value = getattr(self, name)
            _require_builtin_str(value, name)
            if value not in _RECORD_STATUSES:
                raise ValueError(f"{name} is invalid")
        _require_tuple(self.limitations, "limitations")
        if any(type(value) is not str or not value for value in self.limitations):
            raise TypeError("limitations must contain nonempty strings")
        _require_sorted_unique(self.limitations, "limitations")
        if type(self.validation) is not ValidationResult:
            raise TypeError("validation must be ValidationResult")


class _DuplicateKey(ValueError):
    pass


def _pairs(values: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in values:
        if key in result:
            raise _DuplicateKey(key)
        result[key] = value
    return result


def _json_object(payload: bytes) -> dict[str, Any]:
    value = json.loads(payload.decode("utf-8"), object_pairs_hook=_pairs)
    if type(value) is not dict:
        raise TypeError("top-level JSON value must be an object")
    return value


def _path_code(exc: ValueError) -> str:
    code = str(exc).split(":", 1)[0]
    return code if code.startswith("PIH.PATH.") else "PIH.TASK_STATE.REFERENCE_INVALID"


def _declared_paths(value: object, field: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if type(value) is not list:
        raise TypeError(f"{field} must be an array")
    paths = []
    for item in value:
        _require_path(item, field)
        paths.append(item)
    if len(paths) != len(set(paths)):
        raise ValueError(f"{field} must not contain duplicates")
    return tuple(sorted(paths))


def _record_status(paths: tuple[str, ...], missing: set[str]) -> str:
    if not paths:
        return "not_declared"
    return "declared_missing" if set(paths) & missing else "inspected"


class InspectTaskState:
    """Inspect one task through exact root-confined durable references only."""

    __slots__ = ()

    def execute(self, request: TaskStateInspectionRequest) -> TaskStateInspectionResult:
        """Return bounded durable task state without discovery or mutation.

        Parameters
        ----------
        request
            Exact root, chain path, and task identity to inspect.

        Returns
        -------
        TaskStateInspectionResult
            Declared state, exact inspected/read paths, limitations, and structured
            invalid-reference findings.

        Raises
        ------
        TypeError
            If ``request`` is not exactly :class:`TaskStateInspectionRequest`.

        Notes
        -----
        The action reads no path unless the request, selected chain entry, or selected
        ownership manifest names it exactly. It never performs recursive discovery.
        """
        if type(request) is not TaskStateInspectionRequest:
            raise TypeError("request must be TaskStateInspectionRequest")

        root = request.repository_root
        issues: list[ValidationIssue] = []
        inspected: set[str] = set()
        read: set[str] = set()
        missing: set[str] = set()

        def inspect_file(path: str) -> bytes | None:
            inspected.add(path)
            try:
                _require_path(path, "referenced path")
            except ValueError as exc:
                issues.append(
                    _issue(_path_code(exc), str(exc), request.task_id, path=None)
                )
                return None
            current = root
            for part in path.split("/"):
                current = current / part
                if current.is_symlink():
                    issues.append(
                        _issue(
                            "PIH.PATH.SYMLINK",
                            "Referenced path contains a symlink.",
                            request.task_id,
                            path,
                        )
                    )
                    return None
                if not current.exists():
                    missing.add(path)
                    issues.append(
                        _issue(
                            "PIH.PATH.MISSING",
                            "Referenced durable file is missing.",
                            request.task_id,
                            path,
                        )
                    )
                    return None
            if not current.is_file():
                issues.append(
                    _issue(
                        "PIH.PATH.NOT_FILE",
                        "Referenced durable path is not a regular file.",
                        request.task_id,
                        path,
                    )
                )
                return None
            try:
                payload = current.read_bytes()
            except OSError as exc:
                issues.append(
                    _issue(
                        "PIH.TASK_STATE.REFERENCE_INVALID",
                        f"Referenced durable file could not be read: {exc}.",
                        request.task_id,
                        path,
                    )
                )
                return None
            read.add(path)
            return payload

        root_valid = True
        try:
            if (
                not root.exists()
                or not root.is_dir()
                or root.is_symlink()
                or root.resolve(strict=True) != root
            ):
                root_valid = False
        except OSError:
            root_valid = False
        if not root_valid:
            issues.append(
                _issue(
                    "PIH.PATH.ROOT_INVALID",
                    "repository_root must be an existing canonical "
                    "nonsymlink directory.",
                    request.task_id,
                )
            )

        task_status: str | None = None
        active_task: str | None = None
        task_record_path: str | None = None
        ownership_path: str | None = None
        completion_path: str | None = None
        completion_command: tuple[str, ...] = ()
        writers: tuple[tuple[str, str], ...] = ()
        reviewers: tuple[tuple[str, str], ...] = ()
        artifact_paths: tuple[str, ...] = ()
        run_paths: tuple[str, ...] = ()
        handoff_paths: tuple[str, ...] = ()

        chain_payload = inspect_file(request.chain_path) if root_valid else None
        task_entry: dict[str, Any] | None = None
        if chain_payload is not None:
            try:
                chain = _json_object(chain_payload)
                active_task = chain.get("active_task")
                if active_task is not None:
                    _require_identifier(active_task, "active_task")
                entries = chain.get("task_sequence")
                if type(entries) is not list:
                    raise TypeError("task_sequence must be an array")
                matches = [
                    item
                    for item in entries
                    if type(item) is dict and item.get("id") == request.task_id
                ]
                if len(matches) != 1:
                    issues.append(
                        _issue(
                            "PIH.TASK_STATE.TASK_MISSING",
                            "Exact task identity does not occur once in the chain.",
                            request.task_id,
                            request.chain_path,
                        )
                    )
                else:
                    task_entry = matches[0]
                    task_status = task_entry.get("status")
                    _require_identifier(task_status, "task status")
                    raw_record = task_entry.get("record")
                    if raw_record is not None:
                        _require_path(raw_record, "task record")
                        task_record_path = raw_record
                    raw_ownership = task_entry.get("ownership_manifest")
                    if raw_ownership is not None:
                        _require_path(raw_ownership, "ownership manifest")
                        ownership_path = raw_ownership
                    artifact_paths = _declared_paths(
                        task_entry.get("artifact_paths"), "artifact_paths"
                    )
                    run_paths = _declared_paths(
                        task_entry.get("run_record_paths"), "run_record_paths"
                    )
                    handoff_paths = _declared_paths(
                        task_entry.get("handoff_record_paths"), "handoff_record_paths"
                    )
            except (
                _DuplicateKey,
                UnicodeError,
                json.JSONDecodeError,
                TypeError,
                ValueError,
            ) as exc:
                issues.append(
                    _issue(
                        "PIH.TASK_STATE.CHAIN_INVALID",
                        f"Chain state is malformed: {exc}.",
                        request.task_id,
                        request.chain_path,
                    )
                )

        if task_entry is not None:
            if task_record_path is not None:
                inspect_file(task_record_path)
            if ownership_path is not None:
                ownership_payload = inspect_file(ownership_path)
                if ownership_payload is not None:
                    try:
                        ownership = _json_object(ownership_payload)
                        if ownership.get("task_id") != request.task_id:
                            raise ValueError(
                                "ownership task_id differs from requested task"
                            )
                        declared_task_record = ownership.get(
                            "task_record", ownership.get("task_record_path")
                        )
                        if declared_task_record != task_record_path:
                            issues.append(
                                _issue(
                                    "PIH.TASK_STATE.REFERENCE_CONFLICT",
                                    "Chain and ownership task-record paths disagree.",
                                    request.task_id,
                                    ownership_path,
                                )
                            )
                        owners = ownership.get("owners")
                        if type(owners) is not dict:
                            raise TypeError("owners must be an object")
                        if ownership.get("schema_version") == 2:
                            raw_writers = owners.get("writers")
                            raw_reviewers = owners.get("reviewers")
                            completion = ownership.get("completion_validator")
                        elif ownership.get("schema_version") == 1:
                            raw_writers = [
                                {"role": role, "agent": value.get("agent")}
                                for role, value in owners.items()
                                if role != "reviewers" and type(value) is dict
                            ]
                            raw_reviewers = owners.get("reviewers")
                            completion = ownership.get("test_ownership", {}).get(
                                "completion_validator"
                            )
                        else:
                            raise ValueError("unsupported ownership schema_version")
                        if (
                            type(raw_writers) is not list
                            or type(raw_reviewers) is not list
                        ):
                            raise TypeError("writers and reviewers must be arrays")
                        writer_values = []
                        for value in raw_writers:
                            if type(value) is not dict:
                                raise TypeError("writer must be an object")
                            role = _require_identifier(value.get("role"), "writer role")
                            agent = _require_identifier(
                                value.get("agent"), "writer agent"
                            )
                            writer_values.append((role, agent))
                        reviewer_values = []
                        for value in raw_reviewers:
                            if type(value) is not dict:
                                raise TypeError("reviewer must be an object")
                            agent = _require_identifier(
                                value.get("agent"), "reviewer agent"
                            )
                            role = _require_identifier(
                                value.get("role", agent), "reviewer role"
                            )
                            reviewer_values.append((role, agent))
                        if len(writer_values) != len(set(writer_values)):
                            raise ValueError("writer assignments must be unique")
                        if len(reviewer_values) != len(set(reviewer_values)):
                            raise ValueError("reviewer assignments must be unique")
                        writers = tuple(sorted(writer_values))
                        reviewers = tuple(sorted(reviewer_values))
                        if type(completion) is not dict:
                            raise TypeError("completion_validator must be an object")
                        completion_path = _require_path(
                            completion.get("path"), "completion validator path"
                        )
                        raw_command = completion.get("command")
                        completion_command = (
                            tuple(raw_command.split())
                            if type(raw_command) is str
                            else tuple(raw_command)
                            if type(raw_command) is list
                            else ()
                        )
                        if not completion_command or any(
                            type(value) is not str or not value
                            for value in completion_command
                        ):
                            raise TypeError("completion command must contain strings")
                        if completion_path not in completion_command:
                            issues.append(
                                _issue(
                                    "PIH.TASK_STATE.REFERENCE_CONFLICT",
                                    "Completion command does not reference its "
                                    "declared validator path.",
                                    request.task_id,
                                    ownership_path,
                                )
                            )
                        inspect_file(completion_path)
                    except (
                        _DuplicateKey,
                        UnicodeError,
                        json.JSONDecodeError,
                        TypeError,
                        ValueError,
                    ) as exc:
                        issues.append(
                            _issue(
                                "PIH.TASK_STATE.OWNERSHIP_INVALID",
                                f"Ownership state is malformed: {exc}.",
                                request.task_id,
                                ownership_path,
                            )
                        )
            for path in tuple(
                sorted(set((*artifact_paths, *run_paths, *handoff_paths)))
            ):
                inspect_file(path)

        limitations = {
            "Interactive runtime execution and reviewer-launch counts are outside "
            "declared repository state and were not inspected.",
            "Only the chain and exact durable paths declared by the selected task "
            "and ownership manifest were inspected.",
        }
        if task_entry is not None and task_record_path is None:
            limitations.add("No task record is declared by the selected chain entry.")
        if task_entry is not None and ownership_path is None:
            limitations.add(
                "No ownership manifest is declared by the selected chain entry."
            )
        if not run_paths:
            limitations.add(
                "No durable run record is declared by the selected chain entry."
            )
        if not handoff_paths:
            limitations.add(
                "No durable handoff record is declared by the selected chain entry."
            )

        return TaskStateInspectionResult(
            1,
            root,
            request.task_id,
            task_status,
            active_task,
            request.chain_path,
            task_record_path,
            ownership_path,
            completion_path,
            completion_command,
            writers,
            reviewers,
            artifact_paths,
            run_paths,
            handoff_paths,
            _record_status(run_paths, missing),
            _record_status(handoff_paths, missing),
            tuple(sorted(inspected)),
            tuple(sorted(read)),
            tuple(sorted(limitations)),
            _result(tuple(issues)),
        )
