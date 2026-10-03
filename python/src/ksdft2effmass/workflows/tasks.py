"""Nominal Workflow Task routes and definition-only Workflow owners."""

from __future__ import annotations

import inspect
from abc import ABC, abstractmethod
from typing import final

from .definitions import TaskDefinition, TaskExecutionKind, WorkflowDefinition
from .model import (
    TaskDefinitionIdentity,
    TaskExecutionContext,
    TaskExecutionResults,
    TaskInputBinding,
    WorkflowComposition,
    WorkflowIdentity,
)


def _class_has_abstract_members(cls: type[object]) -> bool:
    """Return whether a class still has any effective abstract member."""
    names: set[str] = set()
    for base in cls.__mro__[1:]:
        names.update(getattr(base, "__abstractmethods__", ()))
    for name, value in cls.__dict__.items():
        if getattr(value, "__isabstractmethod__", False):
            names.add(name)
        else:
            names.discard(name)
    return any(
        getattr(inspect.getattr_static(cls, name), "__isabstractmethod__", False)
        for name in names
    )


class AbstractTask(ABC):
    """Nominal base for one Workflow engine node with exactly one route."""

    __slots__ = ()
    _task_execution_kind: TaskExecutionKind

    def __init_subclass__(
        cls,
        *,
        task_execution_kind: TaskExecutionKind | None = None,
        **kwargs: object,
    ) -> None:
        """Reject route overlap and overrides at subclass construction."""
        super().__init_subclass__(**kwargs)
        if "definition" in cls.__dict__:
            raise TypeError("Task subclasses must not override definition")
        if "execution_kind" in cls.__dict__:
            raise TypeError("Task subclasses must not define execution_kind")
        if "_task_execution_kind" in cls.__dict__ and task_execution_kind is None:
            raise TypeError("Task subclasses must not override the route kind")

        inherited_route_roots = tuple(
            base
            for base in cls.__mro__[1:]
            if type(base.__dict__.get("_task_execution_kind")) is TaskExecutionKind
        )
        inherited_kinds = {
            base.__dict__["_task_execution_kind"] for base in inherited_route_roots
        }
        if len(inherited_kinds) > 1:
            raise TypeError("Task subclasses must inherit exactly one route root")

        if task_execution_kind is not None:
            allowed_roots = {
                "AbstractInProcessScientificTask",
                "AbstractSimulationTask",
                "NestedWorkflowTask",
            }
            if cls.__module__ != __name__ or cls.__name__ not in allowed_roots:
                raise TypeError("only Workflow route-root ABCs may select a route kind")
            if type(task_execution_kind) is not TaskExecutionKind:
                raise TypeError("task_execution_kind must be TaskExecutionKind")
            if inherited_kinds:
                raise TypeError("route roots must not inherit another route root")
            cls._task_execution_kind = task_execution_kind
            inherited_kinds = {task_execution_kind}

        if not inherited_kinds and not _class_has_abstract_members(cls):
            raise TypeError("a concrete Task must inherit exactly one route root")

    @property
    @abstractmethod
    def identity(self) -> TaskDefinitionIdentity:
        """Return the stable reusable Task-definition identity."""
        raise NotImplementedError

    @property
    @final
    def definition(self) -> TaskDefinition:
        """Construct the immutable generic Task definition."""
        identity = self.identity
        if type(identity) is not TaskDefinitionIdentity:
            raise TypeError("identity must be TaskDefinitionIdentity")
        kind = getattr(type(self), "_task_execution_kind", None)
        if type(kind) is not TaskExecutionKind:
            raise TypeError("Task class must inherit exactly one route root")
        return TaskDefinition(identity=identity, execution_kind=kind)


class AbstractScientificTask(AbstractTask):
    """Route-less nominal grouping base for scientific Tasks."""

    __slots__ = ()


class AbstractInProcessScientificTask(
    AbstractScientificTask,
    task_execution_kind=TaskExecutionKind.IN_PROCESS,
):
    """Nominal route for ordinary in-process scientific operations."""

    __slots__ = ()

    @abstractmethod
    def execute(
        self,
        inputs: tuple[TaskInputBinding, ...],
        context: TaskExecutionContext,
    ) -> TaskExecutionResults:
        """Execute one correlated in-process operation."""
        raise NotImplementedError


class AbstractSimulationTask(
    AbstractScientificTask,
    task_execution_kind=TaskExecutionKind.SIMULATION,
):
    """Definition-only nominal route for authority-controlled simulations."""

    __slots__ = ()


class NestedWorkflowTask(
    AbstractTask,
    task_execution_kind=TaskExecutionKind.NESTED_WORKFLOW,
):
    """Definition-only nominal route targeting one child Workflow definition."""

    __slots__ = ()

    @property
    @abstractmethod
    def child_workflow_definition(self) -> WorkflowDefinition:
        """Return the immutable child Workflow definition."""
        raise NotImplementedError


class AbstractWorkflow(ABC):
    """Nominal definition-only owner for one reusable Workflow."""

    __slots__ = ()

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Reject per-Workflow definition construction overrides."""
        super().__init_subclass__(**kwargs)
        if "definition" in cls.__dict__:
            raise TypeError("Workflow subclasses must not override definition")

    @property
    @abstractmethod
    def identity(self) -> WorkflowIdentity:
        """Return the stable reusable Workflow identity."""
        raise NotImplementedError

    @property
    @abstractmethod
    def composition(self) -> WorkflowComposition:
        """Return the immutable Task-instance composition."""
        raise NotImplementedError

    @property
    @final
    def definition(self) -> WorkflowDefinition:
        """Construct the immutable generic Workflow definition."""
        identity = self.identity
        composition = self.composition
        if type(identity) is not WorkflowIdentity:
            raise TypeError("identity must be WorkflowIdentity")
        if type(composition) is not WorkflowComposition:
            raise TypeError("composition must be WorkflowComposition")
        return WorkflowDefinition(identity=identity, composition=composition)
