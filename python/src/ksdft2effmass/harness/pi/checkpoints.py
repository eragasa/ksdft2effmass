"""Checkpoint record and profile-relative set validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

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
from .validation import ValidationResult, _issue, _result

if TYPE_CHECKING:
    from .profiles import ProjectProfile


def _timestamp(value: str, field: str) -> None:
    _require_builtin_str(value, field)
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z", value) is None:
        raise ValueError(f"{field} must be RFC 3339 UTC text")
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError(f"{field} must be RFC 3339 UTC text") from exc


@dataclass(frozen=True, slots=True)
class CheckpointRecord:
    """Immutable checkpoint decision content and lifecycle facts."""

    schema_version: int
    checkpoint_id: Identifier
    task_id: Identifier | None
    episode_id: Identifier | None
    status: Identifier
    decision_class: Identifier | None
    created_at: str | None
    question: str | None
    options: tuple[tuple[Identifier, str, str | None], ...]
    human_response: str | None
    normalized_decision: str | None
    resolved_at: str | None
    authorized_scope: str | None
    record_paths: tuple[ResourcePath, ...]
    resumption_status: Identifier | None

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        _require_identifier(self.checkpoint_id, "checkpoint_id")
        _require_identifier(self.status, "status")
        for name in ("task_id", "episode_id", "decision_class", "resumption_status"):
            value = getattr(self, name)
            if value is not None:
                _require_identifier(value, name)
        for name in ("created_at", "resolved_at"):
            value = getattr(self, name)
            if value is not None:
                _timestamp(value, name)
        for name in (
            "question",
            "human_response",
            "normalized_decision",
            "authorized_scope",
        ):
            value = getattr(self, name)
            if value is not None:
                _require_builtin_str(value, name, nonempty=False)
        _require_tuple(self.options, "options")
        seen = set()
        for option in self.options:
            if type(option) is not tuple or len(option) != 3:
                raise TypeError("options entries must be triples")
            oid, label, detail = option
            _require_identifier(oid, "option_id")
            _require_builtin_str(label, "option label", nonempty=False)
            if detail is not None:
                _require_builtin_str(detail, "option detail", nonempty=False)
            if oid in seen:
                raise ValueError("option IDs must be unique")
            seen.add(oid)
        _require_tuple(self.record_paths, "record_paths")
        for path in self.record_paths:
            _require_path(path, "record_path")
        _require_sorted_unique(self.record_paths, "record_paths")


class ValidateCheckpointSet:
    """Validate checkpoint identities and lifecycle state without resolving them."""

    __slots__ = ()

    def execute(
        self,
        checkpoints: tuple[CheckpointRecord, ...],
        task_ids: tuple[Identifier, ...],
        profile: ProjectProfile,
    ) -> ValidationResult:
        from .profiles import ProjectProfile

        _require_tuple(checkpoints, "checkpoints")
        _require_tuple(task_ids, "task_ids")
        if (
            any(type(c) is not CheckpointRecord for c in checkpoints)
            or type(profile) is not ProjectProfile
        ):
            raise TypeError("invalid checkpoint validator arguments")
        for t in task_ids:
            _require_identifier(t, "task_id")
        issues = []
        seen = {}
        taskset = set(task_ids)
        for c in sorted(checkpoints, key=lambda x: x.checkpoint_id):
            if c.checkpoint_id in seen:
                issues.append(
                    _issue(
                        "PIH.CHECKPOINT.DUPLICATE_ID",
                        "Duplicate checkpoint ID.",
                        c.checkpoint_id,
                    )
                )
            seen[c.checkpoint_id] = c
            if c.task_id is not None and c.task_id not in taskset:
                issues.append(
                    _issue(
                        "PIH.CHECKPOINT.TASK_UNKNOWN",
                        "Linked task is unknown.",
                        c.checkpoint_id,
                        related_ids=(c.task_id,),
                    )
                )
            unresolved = c.status in profile.checkpoint_unresolved_statuses
            resolved = c.status in profile.checkpoint_resolved_statuses
            if unresolved == resolved:
                issues.append(
                    _issue(
                        "PIH.CHECKPOINT.STATUS_UNKNOWN",
                        "Checkpoint status is outside one lifecycle set.",
                        c.checkpoint_id,
                    )
                )
            elif unresolved:
                if (
                    not c.question
                    or not c.options
                    or any(
                        x is not None
                        for x in (
                            c.human_response,
                            c.normalized_decision,
                            c.resolved_at,
                            c.authorized_scope,
                        )
                    )
                ):
                    issues.append(
                        _issue(
                            "PIH.CHECKPOINT.STATE_CONTRADICTION",
                            "Unresolved checkpoint fields contradict lifecycle.",
                            c.checkpoint_id,
                        )
                    )
            elif not all(
                x is not None and x != ""
                for x in (
                    c.human_response,
                    c.normalized_decision,
                    c.resolved_at,
                    c.authorized_scope,
                )
            ):
                issues.append(
                    _issue(
                        "PIH.CHECKPOINT.STATE_CONTRADICTION",
                        "Resolved checkpoint fields are incomplete.",
                        c.checkpoint_id,
                    )
                )
        groups: dict[str, list[str]] = {}
        for c in checkpoints:
            if c.normalized_decision is not None:
                groups.setdefault(c.checkpoint_id, []).append(c.normalized_decision)
        for cid, values in groups.items():
            if len(values) != len(set(values)):
                issues.append(
                    _issue(
                        "PIH.CHECKPOINT.DECISION_DUPLICATE",
                        "Duplicate normalized decision for checkpoint identity.",
                        cid,
                    )
                )
        return _result(tuple(issues))
