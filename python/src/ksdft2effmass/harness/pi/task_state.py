"""Bounded inspection of one explicitly supplied Task and selection revision."""

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


@dataclass(frozen=True, slots=True)
class TaskStateInspectionRequest:
    """Identify every repository input for one bounded Task-state inspection.

    Parameters
    ----------
    schema_version
        Request schema version, fixed to ``2``.
    repository_root
        Absolute caller-selected repository boundary.
    task_path
        Root-relative path of the exact canonical ``HarnessTask`` JSON record.
    selection_path
        Root-relative path of the exact canonical
        ``DevelopmentTaskSelection`` JSON record.
    task_id
        Exact Task identity expected in ``task_path``.
    ownership_manifest_path
        Optional root-relative operation-scoped ownership manifest. Ownership is
        never discovered from a Task, selection, registry, or ambient binding.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If the version, root, path, or identity is invalid.
    """

    schema_version: int
    repository_root: Path
    task_path: ResourcePath
    selection_path: ResourcePath
    task_id: Identifier
    ownership_manifest_path: ResourcePath | None = None

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 2:
            raise ValueError("schema_version must equal 2")
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")
        _require_path(self.task_path, "task_path")
        _require_path(self.selection_path, "selection_path")
        _require_identifier(self.task_id, "task_id")
        if self.ownership_manifest_path is not None:
            _require_path(self.ownership_manifest_path, "ownership_manifest_path")


@dataclass(frozen=True, slots=True)
class TaskStateInspectionResult:
    """Immutable result of one explicit-input Task-state inspection.

    Attributes
    ----------
    schema_version
        Result schema version, fixed to ``2``.
    repository_root
        Exact filesystem boundary supplied by the caller.
    task_id, task_status, selected_task_id
        Requested Task identity, canonical Task lifecycle status, and selection
        record's requested current identity. Selection grants no authority.
    task_path, selection_path, ownership_manifest_path
        Exact explicit input paths; ownership may be absent.
    completion_validator_path, completion_command
        Optional operation-scoped ownership completion declaration.
    writers, reviewers
        Deterministically sorted ownership assignments.
    inspected_paths, read_paths
        Sorted exact paths observed and successfully read.
    limitations
        Sorted statements about intentionally unobserved state.
    validation
        Deterministically ordered structured findings.
    """

    schema_version: int
    repository_root: Path
    task_id: Identifier
    task_status: Identifier | None
    selected_task_id: Identifier | None
    task_path: ResourcePath
    selection_path: ResourcePath
    ownership_manifest_path: ResourcePath | None
    completion_validator_path: ResourcePath | None
    completion_command: tuple[str, ...]
    writers: tuple[tuple[Identifier, Identifier], ...]
    reviewers: tuple[tuple[Identifier, Identifier], ...]
    inspected_paths: tuple[ResourcePath, ...]
    read_paths: tuple[ResourcePath, ...]
    limitations: tuple[str, ...]
    validation: ValidationResult

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 2:
            raise ValueError("schema_version must equal 2")
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")
        _require_identifier(self.task_id, "task_id")
        for name in ("task_status", "selected_task_id"):
            value = getattr(self, name)
            if value is not None:
                _require_identifier(value, name)
        for name in (
            "task_path",
            "selection_path",
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
            if values != tuple(sorted(set(values))):
                raise ValueError(f"{name} must be unique and sorted")
            for role, agent in values:
                _require_identifier(role, f"{name} role")
                _require_identifier(agent, f"{name} agent")
        for name in ("inspected_paths", "read_paths"):
            values = getattr(self, name)
            _require_tuple(values, name)
            for value in values:
                _require_path(value, f"{name} item")
            _require_sorted_unique(values, name)
        if not set(self.read_paths) <= set(self.inspected_paths):
            raise ValueError("read_paths must be a subset of inspected_paths")
        _require_tuple(self.limitations, "limitations")
        if any(type(value) is not str or not value for value in self.limitations):
            raise TypeError("limitations must contain nonempty strings")
        _require_sorted_unique(self.limitations, "limitations")
        if type(self.validation) is not ValidationResult:
            raise TypeError("validation must be ValidationResult")


class TaskStateInspector:
    """Inspect one Task through exact caller-supplied durable references only."""

    __slots__ = ()

    def execute(self, request: TaskStateInspectionRequest) -> TaskStateInspectionResult:
        """Return bounded state without discovery, persistence, or mutation.

        Parameters
        ----------
        request
            Exact root, Task, selection, identity, and optional ownership input.

        Returns
        -------
        TaskStateInspectionResult
            Explicitly observed state and structured reference findings.

        Raises
        ------
        TypeError
            If ``request`` is not exactly :class:`TaskStateInspectionRequest`.

        Notes
        -----
        The action does not read ``.pi/chains``, configuration, SQLite, generated
        projections, or a manifest registry. It does not infer authority or activate
        work. The selection and optional ownership manifest are independent inputs;
        neither is a field of ``HarnessTask``.
        """
        if type(request) is not TaskStateInspectionRequest:
            raise TypeError("request must be TaskStateInspectionRequest")

        from .dbcontrol.inspection import _TaskStateQuery

        result = _TaskStateQuery(
            request.repository_root,
            request.task_path,
            request.selection_path,
            request.task_id,
            request.ownership_manifest_path,
        ).execute()
        return TaskStateInspectionResult(
            2,
            request.repository_root,
            request.task_id,
            result.task_status,
            result.selected_task_id,
            request.task_path,
            request.selection_path,
            request.ownership_manifest_path,
            result.completion_validator_path,
            result.completion_command,
            result.writers,
            result.reviewers,
            result.inspected_paths,
            result.read_paths,
            result.limitations,
            result.validation,
        )
