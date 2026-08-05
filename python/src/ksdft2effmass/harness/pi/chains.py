"""Immutable chain views and deterministic structural state evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .checkpoints import CheckpointRecord, ValidateCheckpointSet
from .identity import (
    Identifier,
    ResourcePath,
    _require_identifier,
    _require_path,
    _require_sorted_unique,
    _require_tuple,
    _require_version,
)
from .validation import ChainEvaluationResult, _issue, _result

if TYPE_CHECKING:
    from .profiles import ProjectProfile


@dataclass(frozen=True, slots=True)
class TaskReference:
    """Narrow task graph reference with separate prerequisite kinds."""

    schema_version: int
    task_id: Identifier
    record_path: ResourcePath
    task_prerequisite_ids: tuple[Identifier, ...]
    external_prerequisite_ids: tuple[Identifier, ...]
    status: Identifier
    explicit_activation_required: bool

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        _require_identifier(self.task_id, "task_id")
        _require_path(self.record_path, "record_path")
        _require_identifier(self.status, "status")
        for name in ("task_prerequisite_ids", "external_prerequisite_ids"):
            values = getattr(self, name)
            _require_tuple(values, name)
            for x in values:
                _require_identifier(x, name)
            _require_sorted_unique(values, name)
        if self.task_id in self.task_prerequisite_ids:
            raise ValueError("task cannot depend on itself")
        if set(self.task_prerequisite_ids) & set(self.external_prerequisite_ids):
            raise ValueError("task and external prerequisites must be disjoint")
        if type(self.explicit_activation_required) is not bool:
            raise TypeError("explicit_activation_required must be bool")


@dataclass(frozen=True, slots=True)
class ChainView:
    """Immutable task graph and declared control-plane facts."""

    schema_version: int
    chain_id: Identifier
    active_task_id: Identifier | None
    tasks: tuple[TaskReference, ...]
    explicitly_activated_task_ids: tuple[Identifier, ...]
    production_execution_authorized: bool
    package_publication_authorized: bool

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        _require_identifier(self.chain_id, "chain_id")
        if self.active_task_id is not None:
            _require_identifier(self.active_task_id, "active_task_id")
        _require_tuple(self.tasks, "tasks")
        if not self.tasks or any(type(t) is not TaskReference for t in self.tasks):
            raise TypeError("tasks must be a nonempty tuple of TaskReference")
        ids = tuple(t.task_id for t in self.tasks)
        if ids != tuple(sorted(ids)) or len(set(ids)) != len(ids):
            raise ValueError("tasks must be unique and task-ID sorted")
        _require_tuple(
            self.explicitly_activated_task_ids, "explicitly_activated_task_ids"
        )
        for x in self.explicitly_activated_task_ids:
            _require_identifier(x, "activated task ID")
        _require_sorted_unique(
            self.explicitly_activated_task_ids, "explicitly_activated_task_ids"
        )
        if not set(self.explicitly_activated_task_ids) <= set(ids):
            raise ValueError("activated task is absent")
        for name in (
            "production_execution_authorized",
            "package_publication_authorized",
        ):
            if type(getattr(self, name)) is not bool:
                raise TypeError(f"{name} must be bool")


class EvaluateChainState:
    """Derive active, blocked, and structurally ready task facts."""

    __slots__ = ()

    def execute(
        self,
        chain: ChainView,
        checkpoints: tuple[CheckpointRecord, ...],
        known_external_prerequisite_ids: tuple[Identifier, ...],
        satisfied_external_prerequisite_ids: tuple[Identifier, ...],
        profile: ProjectProfile,
    ) -> ChainEvaluationResult:
        from .profiles import ProjectProfile

        if type(chain) is not ChainView or type(profile) is not ProjectProfile:
            raise TypeError("chain/profile has wrong type")
        _require_tuple(checkpoints, "checkpoints")
        _require_tuple(
            known_external_prerequisite_ids, "known_external_prerequisite_ids"
        )
        _require_tuple(
            satisfied_external_prerequisite_ids, "satisfied_external_prerequisite_ids"
        )
        if any(type(c) is not CheckpointRecord for c in checkpoints):
            raise TypeError("checkpoints have wrong type")
        for values, name in (
            (known_external_prerequisite_ids, "known external IDs"),
            (satisfied_external_prerequisite_ids, "satisfied external IDs"),
        ):
            for x in values:
                _require_identifier(x, name)
            _require_sorted_unique(values, name)
        issues = []
        taskmap = {t.task_id: t for t in chain.tasks}
        known = set(known_external_prerequisite_ids)
        satisfied = set(satisfied_external_prerequisite_ids)
        if not satisfied <= known:
            issues.append(
                _issue(
                    "PIH.CHAIN.PREREQUISITE_MISSING",
                    "Satisfied external prerequisite is not known.",
                    related_ids=tuple(sorted(satisfied - known)),
                )
            )
        graph = {t.task_id: t.task_prerequisite_ids for t in chain.tasks}
        for t in chain.tasks:
            for dep in t.task_prerequisite_ids:
                if dep not in taskmap:
                    issues.append(
                        _issue(
                            "PIH.CHAIN.PREREQUISITE_MISSING",
                            "Task prerequisite is absent.",
                            t.task_id,
                            related_ids=(dep,),
                        )
                    )
            for dep in t.external_prerequisite_ids:
                if dep not in known:
                    issues.append(
                        _issue(
                            "PIH.CHAIN.PREREQUISITE_MISSING",
                            "External prerequisite is unknown.",
                            t.task_id,
                            related_ids=(dep,),
                        )
                    )
            if t.status not in set(profile.task_active_statuses) | set(
                profile.task_blocked_statuses
            ) | set(profile.task_satisfied_statuses):
                issues.append(
                    _issue(
                        "PIH.CHAIN.STATUS_UNKNOWN", "Task status is unknown.", t.task_id
                    )
                )
            if (
                t.task_id in chain.explicitly_activated_task_ids
                and not t.explicit_activation_required
            ):
                issues.append(
                    _issue(
                        "PIH.CHAIN.ACTIVATION_UNEXPECTED",
                        "Unexpected explicit activation.",
                        t.task_id,
                    )
                )
            if (
                t.status in profile.task_active_statuses
                and t.explicit_activation_required
                and t.task_id not in chain.explicitly_activated_task_ids
            ):
                issues.append(
                    _issue(
                        "PIH.CHAIN.ACTIVATION_MISSING",
                        "Active task lacks required activation.",
                        t.task_id,
                    )
                )
        visiting: set[Identifier] = set()
        done: set[Identifier] = set()

        def visit(n: Identifier) -> None:
            if n in visiting:
                issues.append(
                    _issue(
                        "PIH.CHAIN.PREREQUISITE_CYCLE", "Task prerequisite cycle.", n
                    )
                )
                return
            if n in done:
                return
            visiting.add(n)
            for d in graph.get(n, ()):
                if d in graph:
                    visit(d)
            visiting.remove(n)
            done.add(n)

        for n in sorted(graph):
            visit(n)
        active = tuple(
            sorted(
                t.task_id
                for t in chain.tasks
                if t.status in profile.task_active_statuses
            )
        )
        if len(active) > 1 or ((active[0] if active else None) != chain.active_task_id):
            issues.append(
                _issue(
                    "PIH.CHAIN.ACTIVE_CONTRADICTION",
                    "Declared active task contradicts statuses.",
                    chain.active_task_id,
                )
            )
        cpvalidation = ValidateCheckpointSet().execute(
            checkpoints, tuple(sorted(taskmap)), profile
        )
        issues.extend(cpvalidation.issues)
        validation = _result(tuple(issues))
        if validation.status == "FAIL":
            return ChainEvaluationResult((), (), (), validation)
        unresolved = {
            c.task_id
            for c in checkpoints
            if c.task_id is not None
            and c.status in profile.checkpoint_unresolved_statuses
        }
        blocked: list[Identifier] = []
        ready: list[Identifier] = []
        for t in chain.tasks:
            if t.status in profile.task_satisfied_statuses:
                continue
            unsatisfied = any(
                taskmap[d].status not in profile.task_satisfied_statuses
                for d in t.task_prerequisite_ids
            ) or any(d not in satisfied for d in t.external_prerequisite_ids)
            activation = (
                t.explicit_activation_required
                and t.task_id not in chain.explicitly_activated_task_ids
            )
            isblocked = t.task_id in unresolved or unsatisfied or activation
            if isblocked:
                blocked.append(t.task_id)
            elif t.task_id not in active:
                ready.append(t.task_id)
        return ChainEvaluationResult(
            active, tuple(sorted(blocked)), tuple(sorted(ready)), validation
        )
