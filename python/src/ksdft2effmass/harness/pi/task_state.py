"""Bounded inspection of one explicitly selected durable task state."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

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
from .validation import ValidationResult

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
        Requested identity, resolved status, and chain-declared active identity. A
        JSON-backed Task supplies its status from the exact referenced Task record;
        bootstrap Markdown Tasks retain their chain-entry status. Status is absent
        when the requested task cannot be resolved.
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


class TaskStateInspector:
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
        ownership manifest names it exactly. A JSON Task record is read only through
        that exact chain reference and identity disagreement fails closed. Generated
        documentation is never an input. The action never performs recursive discovery.
        """
        if type(request) is not TaskStateInspectionRequest:
            raise TypeError("request must be TaskStateInspectionRequest")

        from .dbcontrol.inspection import _TaskStateQuery

        result = _TaskStateQuery(
            request.repository_root,
            request.chain_path,
            request.task_id,
        ).execute()
        return TaskStateInspectionResult(
            1,
            request.repository_root,
            request.task_id,
            result.task_status,
            result.active_task_id,
            request.chain_path,
            result.task_record_path,
            result.ownership_manifest_path,
            result.completion_validator_path,
            result.completion_command,
            result.writers,
            result.reviewers,
            result.artifact_paths,
            result.run_record_paths,
            result.handoff_record_paths,
            result.durable_run_record_status,
            result.durable_handoff_record_status,
            result.inspected_paths,
            result.read_paths,
            result.limitations,
            result.validation,
        )
