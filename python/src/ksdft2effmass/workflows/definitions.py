"""Immutable generic Workflow and Task definitions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import final

from .model import (
    TaskDefinitionIdentity,
    WorkflowComposition,
    WorkflowIdentity,
)


class TaskExecutionKind(StrEnum):
    """Closed engine routes for nominal Tasks."""

    IN_PROCESS = "in_process"
    SIMULATION = "simulation"
    NESTED_WORKFLOW = "nested_workflow"


@final
@dataclass(frozen=True, slots=True)
class TaskDefinition:
    """Identify one reusable Task operation and its fixed execution route."""

    identity: TaskDefinitionIdentity
    execution_kind: TaskExecutionKind

    def __post_init__(self) -> None:
        """Validate exact generic definition fields."""
        if type(self.identity) is not TaskDefinitionIdentity:
            raise TypeError("identity must be TaskDefinitionIdentity")
        if type(self.execution_kind) is not TaskExecutionKind:
            raise TypeError("execution_kind must be TaskExecutionKind")


@final
@dataclass(frozen=True, slots=True)
class WorkflowDefinition:
    """Represent one reusable declarative Workflow composition."""

    identity: WorkflowIdentity
    composition: WorkflowComposition

    def __post_init__(self) -> None:
        """Validate exact identity and composition correlation."""
        if type(self.identity) is not WorkflowIdentity:
            raise TypeError("identity must be WorkflowIdentity")
        if type(self.composition) is not WorkflowComposition:
            raise TypeError("composition must be WorkflowComposition")
        if self.composition.workflow_identity != self.identity:
            raise ValueError("composition must identify this Workflow definition")
