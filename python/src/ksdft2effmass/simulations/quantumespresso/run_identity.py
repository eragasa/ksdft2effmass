"""Portable run identities for project-owned Quantum ESPRESSO simulations.

This module represents the naming and relative-directory contract for one bundled
Quantum ESPRESSO example Workflow simulation.  The canonical identity extends an exact
Harness Task identity with an upstream QE release and an explicitly supplied UTC
creation time.  The same fields map to a relative directory hierarchy without
consulting the clock, filesystem, repository, executable, or process environment.

The representation is operational metadata.  It does not create a workspace, grant
execution authority, identify executable or input bytes, establish cross-version
compatibility, or provide numerical verification or scientific validation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import PurePosixPath

from ksdft2effmass.integration.quantum_espresso import (
    LocalQuantumEspressoAttemptWorkspaceName,
)
from ksdft2effmass.workflows import WorkflowRunIdentity

_TASK_PREFIX = (
    "quantumespresso",
    "simulations",
    "qe_examples",
)
_TASK_SEGMENT_PATTERN = re.compile(r"[a-z0-9](?:[a-z0-9_-]*[a-z0-9])?\Z", re.ASCII)
_RELEASE_PATTERN = re.compile(
    r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:\.(?:0|[1-9][0-9]*))?\Z",
    re.ASCII,
)


@dataclass(frozen=True, slots=True)
class QuantumEspressoBundledExampleRunIdentity:
    """Represent one Task-derived bundled-example run identity and path.

    Parameters
    ----------
    task_id
        Exact canonical Task identity.  It must have the form
        ``quantumespresso.simulations.qe_examples.COMPONENT.EXAMPLE`` with lowercase
        ASCII component and example segments.
    release
        Exact upstream QE release in ``MAJOR.MINOR`` or ``MAJOR.MINOR.PATCH`` form.
        Components are nonnegative canonical decimal integers without leading zeros.
    workspace_created_at
        Time assigned to the run workspace.  It must be a timezone-aware UTC
        :class:`datetime.datetime` with whole-second precision.

    Notes
    -----
    The canonical value is
    ``TASK-ID.vMAJOR-MINOR[-PATCH].YYYYMMDDTHHMMSSZ``.  Its relative path begins with
    ``simulations/quantumespresso``, retains the remaining Task hierarchy, and appends
    the version and timestamp segments.  Exact executable, input, pseudopotential,
    scientific-setting, resource, authorization, and attempt identities remain
    separate manifest fields.

    Construction performs no clock or filesystem access.  Existing-path rejection is
    owned by the local execution preparer when the derived parent path and workspace
    name are used to prepare an attempt.
    """

    task_id: str
    release: str
    workspace_created_at: datetime

    def __post_init__(self) -> None:
        """Validate the exact Task, release, and UTC timestamp fields."""
        if type(self.task_id) is not str:
            raise TypeError("task_id must be a built-in str")
        segments = tuple(self.task_id.split("."))
        if len(segments) != 5 or segments[:3] != _TASK_PREFIX:
            raise ValueError(
                "task_id must identify one Quantum ESPRESSO bundled example"
            )
        if any(
            _TASK_SEGMENT_PATTERN.fullmatch(segment) is None for segment in segments
        ):
            raise ValueError("task_id segments must use canonical lowercase ASCII")

        if type(self.release) is not str:
            raise TypeError("release must be a built-in str")
        if _RELEASE_PATTERN.fullmatch(self.release) is None:
            raise ValueError(
                "release must be canonical MAJOR.MINOR or MAJOR.MINOR.PATCH text"
            )

        if type(self.workspace_created_at) is not datetime:
            raise TypeError("workspace_created_at must be a datetime")
        offset = self.workspace_created_at.utcoffset()
        if offset != timedelta(0):
            raise ValueError("workspace_created_at must be timezone-aware UTC")
        if self.workspace_created_at.microsecond != 0:
            raise ValueError("workspace_created_at must have whole-second precision")

    @property
    def version_segment(self) -> str:
        """Return the canonical path-safe release segment."""
        return "v" + self.release.replace(".", "-")

    @property
    def timestamp_segment(self) -> str:
        """Return the canonical whole-second UTC timestamp segment."""
        value = self.workspace_created_at
        return (
            f"{value.year:04d}{value.month:02d}{value.day:02d}T"
            f"{value.hour:02d}{value.minute:02d}{value.second:02d}Z"
        )

    @property
    def value(self) -> str:
        """Return the canonical portable run-identity text."""
        return f"{self.task_id}.{self.version_segment}.{self.timestamp_segment}"

    @property
    def workflow_run_identity(self) -> WorkflowRunIdentity:
        """Return the generic Workflow identity carrying the canonical text."""
        return WorkflowRunIdentity(self.value)

    @property
    def relative_parent_path(self) -> PurePosixPath:
        """Return the Task and release hierarchy above the run workspace."""
        task_segments = self.task_id.split(".")
        return PurePosixPath(
            "simulations",
            "quantumespresso",
            *task_segments[2:],
            self.version_segment,
        )

    @property
    def attempt_workspace_name(self) -> LocalQuantumEspressoAttemptWorkspaceName:
        """Return the final parent-free timestamp workspace name."""
        return LocalQuantumEspressoAttemptWorkspaceName(self.timestamp_segment)

    @property
    def relative_workspace_path(self) -> PurePosixPath:
        """Return the complete relative Task/release/timestamp directory path."""
        return self.relative_parent_path / self.attempt_workspace_name.value
