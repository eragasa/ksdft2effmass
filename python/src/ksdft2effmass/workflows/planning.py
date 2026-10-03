"""Pure declarative Workflow execution-plan records and construction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

from .definitions import TaskDefinition, TaskExecutionKind, WorkflowDefinition
from .model import TaskInstanceIdentity


@final
@dataclass(frozen=True, slots=True)
class NestedWorkflowTarget:
    """Correlate one nested Task instance with one child Workflow definition."""

    task_instance_identity: TaskInstanceIdentity
    child_workflow_definition: WorkflowDefinition

    def __post_init__(self) -> None:
        """Validate exact declarative target fields."""
        if type(self.task_instance_identity) is not TaskInstanceIdentity:
            raise TypeError("task_instance_identity must be TaskInstanceIdentity")
        if type(self.child_workflow_definition) is not WorkflowDefinition:
            raise TypeError("child_workflow_definition must be WorkflowDefinition")


@final
@dataclass(frozen=True, slots=True)
class WorkflowExecutionPlan:
    """Retain one Workflow definition and complete declarative Task snapshots."""

    workflow_definition: WorkflowDefinition
    task_definitions: tuple[TaskDefinition, ...]
    nested_workflow_targets: tuple[NestedWorkflowTarget, ...]

    def __post_init__(self) -> None:
        """Validate exact immutable field shapes."""
        if type(self.workflow_definition) is not WorkflowDefinition:
            raise TypeError("workflow_definition must be WorkflowDefinition")
        if type(self.task_definitions) is not tuple or any(
            type(value) is not TaskDefinition for value in self.task_definitions
        ):
            raise TypeError("task_definitions must be a tuple of TaskDefinition")
        if type(self.nested_workflow_targets) is not tuple or any(
            type(value) is not NestedWorkflowTarget
            for value in self.nested_workflow_targets
        ):
            raise TypeError(
                "nested_workflow_targets must be a tuple of NestedWorkflowTarget"
            )


class WorkflowExecutionPlanConstructor:
    """Compile one complete immutable declarative Workflow execution plan."""

    __slots__ = ()

    @staticmethod
    def execute(
        workflow_definition: WorkflowDefinition,
        task_definitions: tuple[TaskDefinition, ...],
        nested_workflow_targets: tuple[NestedWorkflowTarget, ...],
    ) -> WorkflowExecutionPlan:
        """Validate complete definition closure and return one plan."""
        if type(workflow_definition) is not WorkflowDefinition:
            raise TypeError("workflow_definition must be WorkflowDefinition")
        if type(task_definitions) is not tuple or any(
            type(value) is not TaskDefinition for value in task_definitions
        ):
            raise TypeError("task_definitions must be a tuple of TaskDefinition")
        if type(nested_workflow_targets) is not tuple or any(
            type(value) is not NestedWorkflowTarget for value in nested_workflow_targets
        ):
            raise TypeError(
                "nested_workflow_targets must be a tuple of NestedWorkflowTarget"
            )

        instances = workflow_definition.composition.task_instances
        if len(task_definitions) != len(instances):
            raise ValueError("task definitions must match composition membership")
        if tuple(value.identity for value in task_definitions) != tuple(
            instance.definition_identity for instance in instances
        ):
            raise ValueError(
                "task definitions must match composition identity and order"
            )

        nested_instances = tuple(
            instance
            for instance, definition in zip(instances, task_definitions, strict=True)
            if definition.execution_kind is TaskExecutionKind.NESTED_WORKFLOW
        )
        target_identities = tuple(
            target.task_instance_identity for target in nested_workflow_targets
        )
        if target_identities != tuple(
            instance.identity for instance in nested_instances
        ):
            raise ValueError(
                "nested targets must exactly match nested Task order and membership"
            )
        if len(set(target_identities)) != len(target_identities):
            raise ValueError("nested target Task-instance identities must be unique")
        if any(
            target.child_workflow_definition.identity == workflow_definition.identity
            for target in nested_workflow_targets
        ):
            raise ValueError("nested target must not identify the owning Workflow")

        return WorkflowExecutionPlan(
            workflow_definition=workflow_definition,
            task_definitions=task_definitions,
            nested_workflow_targets=nested_workflow_targets,
        )
