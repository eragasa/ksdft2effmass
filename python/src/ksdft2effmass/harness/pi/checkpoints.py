"""Checkpoint records, pure decision transformation, and set validation."""

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


@dataclass(frozen=True, slots=True)
class CheckpointDecisionResolutionRequest:
    """Explicit inputs for deterministic checkpoint decision transformation.

    Parameters
    ----------
    checkpoint
        Exact immutable generic checkpoint decision view to transform.
    expected_unresolved_status
        Status that permits a new resolution.
    resolved_status
        Distinct status assigned to the resolved record.
    human_response
        Exact nonempty decision-bearing human text, preserved verbatim.
    normalized_decision
        Exact declared checkpoint option identifier selected before this action.
    resolved_at
        Explicit RFC 3339 UTC timestamp ending in ``Z``. The action never reads a
        clock.
    authorized_scope
        Exact nonempty scope already determined by human-intent interpretation.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If a correctly typed value violates an intrinsic request invariant.

    Notes
    -----
    This runtime DataObject is not a member of ``HarnessWireRecord``. It neither
    interprets human prose nor represents project-local checkpoint-only fields.
    """

    checkpoint: CheckpointRecord
    expected_unresolved_status: Identifier
    resolved_status: Identifier
    human_response: str
    normalized_decision: Identifier
    resolved_at: str
    authorized_scope: str

    def __post_init__(self) -> None:
        if type(self.checkpoint) is not CheckpointRecord:
            raise TypeError("checkpoint must be CheckpointRecord")
        _require_identifier(
            self.expected_unresolved_status, "expected_unresolved_status"
        )
        _require_identifier(self.resolved_status, "resolved_status")
        if self.expected_unresolved_status == self.resolved_status:
            raise ValueError("expected and resolved statuses must differ")
        _require_builtin_str(self.human_response, "human_response")
        _require_identifier(self.normalized_decision, "normalized_decision")
        _timestamp(self.resolved_at, "resolved_at")
        _require_builtin_str(self.authorized_scope, "authorized_scope")


@dataclass(frozen=True, slots=True)
class CheckpointDecisionResolutionResult:
    """Immutable result of deterministic checkpoint decision transformation.

    Attributes
    ----------
    checkpoint
        Newly resolved checkpoint, unchanged idempotent checkpoint, or ``None``
        when validation fails.
    changed
        Exact Boolean indicating whether a new resolved record was constructed.
    validation
        Deterministically ordered transformation findings.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If checkpoint presence, changed state, and validation status conflict.

    Notes
    -----
    This runtime ResultObject is not a member of ``HarnessWireRecord`` and owns no
    persistence, Git, task-resumption, or successor-activation behavior.
    """

    checkpoint: CheckpointRecord | None
    changed: bool
    validation: ValidationResult

    def __post_init__(self) -> None:
        if (
            self.checkpoint is not None
            and type(self.checkpoint) is not CheckpointRecord
        ):
            raise TypeError("checkpoint must be CheckpointRecord or None")
        if type(self.changed) is not bool:
            raise TypeError("changed must be bool")
        if type(self.validation) is not ValidationResult:
            raise TypeError("validation must be ValidationResult")
        failed = self.validation.status == "FAIL"
        if failed == (self.checkpoint is not None):
            raise ValueError("checkpoint presence must agree with validation status")
        if self.changed and failed:
            raise ValueError("changed result must be successful")


class CheckpointDecisionResolver:
    """Transform one generic checkpoint after intent is already interpreted.

    The fieldless action consumes only explicit request state. It performs no
    prose interpretation, option choice, scope inference, filesystem access,
    clock access, serialization, persistence, Git operation, task resumption, or
    successor activation.
    """

    __slots__ = ()

    def execute(
        self, request: CheckpointDecisionResolutionRequest
    ) -> CheckpointDecisionResolutionResult:
        """Resolve, repeat idempotently, or reject one explicit decision.

        Parameters
        ----------
        request
            Exact checkpoint and all decision-bearing resolution values.

        Returns
        -------
        CheckpointDecisionResolutionResult
            A changed resolved record, unchanged idempotent record, or structured
            failure without a partial checkpoint.

        Raises
        ------
        TypeError
            If ``request`` is not exactly
            ``CheckpointDecisionResolutionRequest``.

        Notes
        -----
        Expected invalid states use ``PIH.CHECKPOINT.DECISION_UNKNOWN``,
        ``PIH.CHECKPOINT.STATE_CONTRADICTION``,
        ``PIH.CHECKPOINT.RESOLUTION_CONFLICT``, or
        ``PIH.CHECKPOINT.STATUS_CONFLICT``. Findings are deterministically
        ordered and a failed result contains no checkpoint.
        """
        if type(request) is not CheckpointDecisionResolutionRequest:
            raise TypeError("request must be CheckpointDecisionResolutionRequest")

        checkpoint = request.checkpoint
        issues = []
        option_ids = tuple(option[0] for option in checkpoint.options)
        if request.normalized_decision not in option_ids:
            issues.append(
                _issue(
                    "PIH.CHECKPOINT.DECISION_UNKNOWN",
                    "Normalized decision is not a declared checkpoint option.",
                    checkpoint.checkpoint_id,
                    related_ids=(request.normalized_decision,),
                )
            )

        if checkpoint.status == request.expected_unresolved_status:
            resolution_fields = (
                ("authorized_scope", checkpoint.authorized_scope),
                ("human_response", checkpoint.human_response),
                ("normalized_decision", checkpoint.normalized_decision),
                ("resolved_at", checkpoint.resolved_at),
            )
            contradictory = tuple(
                name for name, value in resolution_fields if value is not None
            )
            if contradictory:
                issues.append(
                    _issue(
                        "PIH.CHECKPOINT.STATE_CONTRADICTION",
                        "Unresolved checkpoint already contains resolution fields.",
                        checkpoint.checkpoint_id,
                        related_ids=contradictory,
                    )
                )
        elif checkpoint.status == request.resolved_status:
            expected_fields = (
                (
                    "authorized_scope",
                    checkpoint.authorized_scope,
                    request.authorized_scope,
                ),
                ("human_response", checkpoint.human_response, request.human_response),
                (
                    "normalized_decision",
                    checkpoint.normalized_decision,
                    request.normalized_decision,
                ),
                ("resolved_at", checkpoint.resolved_at, request.resolved_at),
            )
            conflicting = tuple(
                name for name, actual, expected in expected_fields if actual != expected
            )
            if conflicting:
                issues.append(
                    _issue(
                        "PIH.CHECKPOINT.RESOLUTION_CONFLICT",
                        "Resolved checkpoint differs from the explicit request.",
                        checkpoint.checkpoint_id,
                        related_ids=conflicting,
                    )
                )
        else:
            issues.append(
                _issue(
                    "PIH.CHECKPOINT.STATUS_CONFLICT",
                    "Checkpoint status matches neither explicit request status.",
                    checkpoint.checkpoint_id,
                    related_ids=tuple(
                        sorted(
                            {
                                checkpoint.status,
                                request.expected_unresolved_status,
                                request.resolved_status,
                            }
                        )
                    ),
                )
            )

        validation = _result(tuple(issues))
        if validation.status == "FAIL":
            return CheckpointDecisionResolutionResult(None, False, validation)
        if checkpoint.status == request.resolved_status:
            return CheckpointDecisionResolutionResult(checkpoint, False, validation)

        resolved = CheckpointRecord(
            checkpoint.schema_version,
            checkpoint.checkpoint_id,
            checkpoint.task_id,
            checkpoint.episode_id,
            request.resolved_status,
            checkpoint.decision_class,
            checkpoint.created_at,
            checkpoint.question,
            checkpoint.options,
            request.human_response,
            request.normalized_decision,
            request.resolved_at,
            request.authorized_scope,
            checkpoint.record_paths,
            checkpoint.resumption_status,
        )
        return CheckpointDecisionResolutionResult(resolved, True, validation)


class CheckpointSetValidator:
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
