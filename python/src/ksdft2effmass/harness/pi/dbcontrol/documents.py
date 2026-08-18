"""Strict parsers for explicit Task, selection, and ownership inputs."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from ..identity import (
    Identifier,
    ResourcePath,
    _require_builtin_str,
    _require_identifier,
    _require_path,
)
from ..validation import ValidationIssue, _issue


class _DuplicateKey(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class _TaskState:
    status: Identifier


@dataclass(frozen=True, slots=True)
class _SelectionState:
    selected_task_id: Identifier | None


@dataclass(frozen=True, slots=True)
class _OwnershipState:
    completion_path: ResourcePath
    completion_command: tuple[str, ...]
    writers: tuple[tuple[Identifier, Identifier], ...]
    reviewers: tuple[tuple[Identifier, Identifier], ...]


class _TaskStateDocumentParser:
    """Parse only exact documents supplied to one bounded inspection."""

    __slots__ = ()

    def _pairs(self, values: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in values:
            if key in result:
                raise _DuplicateKey(key)
            result[key] = value
        return result

    def _json_object(self, payload: bytes) -> dict[str, Any]:
        value = json.loads(payload.decode("utf-8"), object_pairs_hook=self._pairs)
        if type(value) is not dict:
            raise TypeError("top-level JSON value must be an object")
        return value

    def _task_array(
        self,
        task: dict[str, Any],
        name: str,
        item_parser: Any,
        *,
        nonempty: bool = False,
        sorted_unique: bool = False,
    ) -> tuple[str, ...]:
        values = task[name]
        if type(values) is not list:
            raise TypeError(f"{name} must be a JSON array")
        result = tuple(item_parser(value, f"{name} item") for value in values)
        if nonempty and not result:
            raise ValueError(f"{name} must be nonempty")
        if len(set(result)) != len(result):
            raise ValueError(f"{name} must contain unique values")
        if sorted_unique and result != tuple(sorted(result)):
            raise ValueError(f"{name} must be sorted")
        return result

    def parse_task(self, payload: bytes, task_id: Identifier) -> _TaskState:
        """Return state from one closed canonical HarnessTask wire record."""
        task = self._json_object(payload)
        expected = {
            "schema_version",
            "task_id",
            "title",
            "status",
            "status_detail",
            "parent_task_id",
            "task_prerequisite_ids",
            "external_prerequisite_ids",
            "superseded_by_task_ids",
            "explicit_activation_required",
            "objective",
            "authority_reference_paths",
            "authorized_scope",
            "completion_criteria",
            "exclusions",
            "intake_path",
            "archived_source",
            "documentation_path",
        }
        required = expected - {"documentation_path"}
        missing = required - set(task)
        unknown = set(task) - expected
        if missing:
            raise ValueError(f"missing field {sorted(missing)[0]}")
        if unknown:
            raise ValueError(f"unknown field {sorted(unknown)[0]}")
        if type(task["schema_version"]) is not int or task["schema_version"] != 3:
            raise ValueError("schema_version must equal integer 3")

        represented_id = _require_identifier(task["task_id"], "task_id")
        if represented_id != task_id:
            raise ValueError("Task record identity differs from requested task")
        status = _require_identifier(task["status"], "status")
        _require_builtin_str(task["title"], "title")
        _require_builtin_str(task["objective"], "objective")
        if task["status_detail"] is not None:
            _require_builtin_str(task["status_detail"], "status_detail")

        parent = task["parent_task_id"]
        if parent is not None:
            parent = _require_identifier(parent, "parent_task_id")
            if parent == represented_id:
                raise ValueError("parent_task_id must differ from task_id")
        task_prerequisites = self._task_array(
            task,
            "task_prerequisite_ids",
            _require_identifier,
            sorted_unique=True,
        )
        external_prerequisites = self._task_array(
            task,
            "external_prerequisite_ids",
            _require_identifier,
            sorted_unique=True,
        )
        superseded_by = self._task_array(
            task,
            "superseded_by_task_ids",
            _require_identifier,
            sorted_unique=True,
        )
        if (
            represented_id in task_prerequisites
            or represented_id in external_prerequisites
        ):
            raise ValueError("a Task may not require itself")
        if represented_id in superseded_by:
            raise ValueError("a Task may not supersede itself")
        if set(task_prerequisites) & set(external_prerequisites):
            raise ValueError("Task and external prerequisites must be disjoint")
        if type(task["explicit_activation_required"]) is not bool:
            raise TypeError("explicit_activation_required must be a built-in bool")

        self._task_array(
            task,
            "authority_reference_paths",
            _require_path,
            nonempty=True,
            sorted_unique=True,
        )
        for name in ("authorized_scope", "completion_criteria", "exclusions"):
            self._task_array(
                task,
                name,
                _require_builtin_str,
                nonempty=True,
            )
        for name in ("intake_path", "documentation_path"):
            value = task.get(name)
            if value is not None:
                _require_path(value, name)
        archived = task["archived_source"]
        if archived is not None:
            if type(archived) is not dict or set(archived) != {"path", "sha256"}:
                raise TypeError("archived_source must be a closed object or null")
            _require_path(archived["path"], "archived_source path")
            digest = _require_builtin_str(archived["sha256"], "archived_source sha256")
            if re.fullmatch(r"[0-9a-f]{64}", digest, re.ASCII) is None:
                raise ValueError("archived_source sha256 must be lowercase hexadecimal")
        return _TaskState(status)

    def parse_selection(self, payload: bytes) -> _SelectionState:
        """Return current selection from the closed version-1 selection record."""
        selection = self._json_object(payload)
        expected = {
            "schema_version",
            "active_task_id",
            "explicit_activation_receipt_ids",
            "automatic_successor_activation",
        }
        if set(selection) != expected:
            missing = sorted(expected - set(selection))
            unknown = sorted(set(selection) - expected)
            detail = (
                f"missing field {missing[0]}"
                if missing
                else f"unknown field {unknown[0]}"
            )
            raise ValueError(f"selection record is not closed: {detail}")
        if (
            selection["schema_version"] != 1
            or type(selection["schema_version"]) is not int
        ):
            raise ValueError("selection schema_version must equal integer 1")
        selected = selection["active_task_id"]
        if selected is not None:
            selected = _require_identifier(selected, "active_task_id")
        receipts = selection["explicit_activation_receipt_ids"]
        if type(receipts) is not list:
            raise TypeError("explicit_activation_receipt_ids must be an array")
        normalized = tuple(
            _require_identifier(value, "explicit_activation_receipt_id")
            for value in receipts
        )
        if normalized != tuple(sorted(set(normalized))):
            raise ValueError(
                "explicit_activation_receipt_ids must be sorted and unique"
            )
        automatic = selection["automatic_successor_activation"]
        if type(automatic) is not bool or automatic:
            raise ValueError("automatic_successor_activation must be false")
        return _SelectionState(selected)

    def _assignments(
        self, values: object, kind: str
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

    def parse_ownership(
        self,
        payload: bytes,
        task_id: Identifier,
        task_path: ResourcePath,
        ownership_path: ResourcePath,
        issues: list[ValidationIssue],
    ) -> _OwnershipState:
        """Parse one explicitly supplied operation-scoped ownership manifest."""
        ownership = self._json_object(payload)
        if ownership.get("task_id") != task_id:
            raise ValueError("ownership task_id differs from requested task")
        declared_task = ownership.get("task_record", ownership.get("task_record_path"))
        if declared_task != task_path:
            issues.append(
                _issue(
                    "PIH.TASK_STATE.REFERENCE_CONFLICT",
                    "Ownership manifest and explicit Task paths disagree.",
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
        writers = self._assignments(raw_writers, "writer")
        reviewers = self._assignments(raw_reviewers, "reviewer")
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
            type(value) is not str or not value for value in completion_command
        ):
            raise TypeError("completion command must contain strings")
        if completion_path not in completion_command:
            issues.append(
                _issue(
                    "PIH.TASK_STATE.REFERENCE_CONFLICT",
                    "Completion command does not reference its declared "
                    "validator path.",
                    task_id,
                    ownership_path,
                )
            )
        return _OwnershipState(completion_path, completion_command, writers, reviewers)


_PARSE_ERRORS = (
    _DuplicateKey,
    UnicodeError,
    json.JSONDecodeError,
    TypeError,
    ValueError,
)
