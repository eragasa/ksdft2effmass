"""Strict parsers for chain and ownership task-state documents."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from ..identity import Identifier, ResourcePath, _require_identifier, _require_path
from ..validation import ValidationIssue, _issue


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


def _declared_paths(value: object, field: str) -> tuple[ResourcePath, ...]:
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


@dataclass(slots=True)
class _SelectedTask:
    status: Identifier | None = None
    task_record_path: ResourcePath | None = None
    ownership_path: ResourcePath | None = None
    artifact_paths: tuple[ResourcePath, ...] = ()
    run_paths: tuple[ResourcePath, ...] = ()
    handoff_paths: tuple[ResourcePath, ...] = ()


@dataclass(slots=True)
class _ChainState:
    active_task: Identifier | None = None
    selected_task: _SelectedTask | None = None


@dataclass(frozen=True, slots=True)
class _OwnershipState:
    completion_path: ResourcePath
    completion_command: tuple[str, ...]
    writers: tuple[tuple[Identifier, Identifier], ...]
    reviewers: tuple[tuple[Identifier, Identifier], ...]


def _parse_chain(
    payload: bytes,
    task_id: Identifier,
    chain_path: ResourcePath,
    issues: list[ValidationIssue],
) -> _ChainState:
    """Parse in declaration order while retaining valid fields before a failure."""
    state = _ChainState()
    try:
        chain = _json_object(payload)
        active_task = chain.get("active_task")
        if active_task is not None:
            state.active_task = _require_identifier(active_task, "active_task")
        entries = chain.get("task_sequence")
        if type(entries) is not list:
            raise TypeError("task_sequence must be an array")
        matches = [
            item for item in entries if type(item) is dict and item.get("id") == task_id
        ]
        if len(matches) != 1:
            issues.append(
                _issue(
                    "PIH.TASK_STATE.TASK_MISSING",
                    "Exact task identity does not occur once in the chain.",
                    task_id,
                    chain_path,
                )
            )
            return state

        task_entry = matches[0]
        selected = _SelectedTask()
        state.selected_task = selected
        raw_record = task_entry.get("record")
        if raw_record is not None:
            selected.task_record_path = _require_path(raw_record, "task record")
        if selected.task_record_path is None or not selected.task_record_path.endswith(
            ".json"
        ):
            selected.status = _require_identifier(
                task_entry.get("status"), "task status"
            )
        raw_ownership = task_entry.get("ownership_manifest")
        if raw_ownership is not None:
            selected.ownership_path = _require_path(raw_ownership, "ownership manifest")
        selected.artifact_paths = _declared_paths(
            task_entry.get("artifact_paths"), "artifact_paths"
        )
        selected.run_paths = _declared_paths(
            task_entry.get("run_record_paths"), "run_record_paths"
        )
        selected.handoff_paths = _declared_paths(
            task_entry.get("handoff_record_paths"), "handoff_record_paths"
        )
    except _PARSE_ERRORS as exc:
        issues.append(
            _issue(
                "PIH.TASK_STATE.CHAIN_INVALID",
                f"Chain state is malformed: {exc}.",
                task_id,
                chain_path,
            )
        )
    return state


def _assignments(
    values: object,
    kind: str,
) -> tuple[tuple[Identifier, Identifier], ...]:
    if type(values) is not list:
        raise TypeError(f"{kind}s must be arrays")
    assignments = []
    for value in values:
        if type(value) is not dict:
            raise TypeError(f"{kind} must be an object")
        agent = _require_identifier(value.get("agent"), f"{kind} agent")
        default_role = agent if kind == "reviewer" else None
        role = _require_identifier(value.get("role", default_role), f"{kind} role")
        assignments.append((role, agent))
    if len(assignments) != len(set(assignments)):
        raise ValueError(f"{kind} assignments must be unique")
    return tuple(sorted(assignments))


def _parse_json_task(
    payload: bytes,
    task_id: Identifier,
) -> Identifier:
    """Return status from one exact JSON Task after identity agreement."""
    task = _json_object(payload)
    if _require_identifier(task.get("task_id"), "task record id") != task_id:
        raise ValueError("JSON Task identity differs from requested task")
    return _require_identifier(task.get("status"), "task status")


def _parse_ownership(
    payload: bytes,
    task_id: Identifier,
    task_record_path: ResourcePath | None,
    ownership_path: ResourcePath,
    issues: list[ValidationIssue],
) -> _OwnershipState:
    ownership = _json_object(payload)
    if ownership.get("task_id") != task_id:
        raise ValueError("ownership task_id differs from requested task")
    declared_task_record = ownership.get(
        "task_record", ownership.get("task_record_path")
    )
    if declared_task_record != task_record_path:
        issues.append(
            _issue(
                "PIH.TASK_STATE.REFERENCE_CONFLICT",
                "Chain and ownership task-record paths disagree.",
                task_id,
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
        test_ownership: Any = ownership.get("test_ownership", {})
        completion = test_ownership.get("completion_validator")
    else:
        raise ValueError("unsupported ownership schema_version")

    if type(raw_writers) is not list or type(raw_reviewers) is not list:
        raise TypeError("writers and reviewers must be arrays")
    writers = _assignments(raw_writers, "writer")
    reviewers = _assignments(raw_reviewers, "reviewer")
    if type(completion) is not dict:
        raise TypeError("completion_validator must be an object")
    completion_path = _require_path(completion.get("path"), "completion validator path")
    raw_command = completion.get("command")
    completion_command = (
        tuple(raw_command.split())
        if type(raw_command) is str
        else tuple(raw_command)
        if type(raw_command) is list
        else ()
    )
    if not completion_command or any(
        type(value) is not str or not value for value in completion_command
    ):
        raise TypeError("completion command must contain strings")
    if completion_path not in completion_command:
        issues.append(
            _issue(
                "PIH.TASK_STATE.REFERENCE_CONFLICT",
                "Completion command does not reference its declared validator path.",
                task_id,
                ownership_path,
            )
        )
    return _OwnershipState(
        completion_path,
        completion_command,
        writers,
        reviewers,
    )


_PARSE_ERRORS = (
    _DuplicateKey,
    UnicodeError,
    json.JSONDecodeError,
    TypeError,
    ValueError,
)
