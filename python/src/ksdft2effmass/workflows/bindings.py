"""Process-local runtime bindings for declarative Workflow plans."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

from .control.dispatch import AbstractSimulationDispatchEffect
from .definitions import TaskExecutionKind
from .model import TaskInstanceIdentity
from .planning import WorkflowExecutionPlan
from .tasks import (
    AbstractInProcessScientificTask,
    AbstractSimulationTask,
    AbstractTask,
    NestedWorkflowTask,
)


@final
@dataclass(frozen=True, slots=True)
class WorkflowTaskBinding:
    """Bind one planned Task instance to one process-local nominal adapter."""

    task_instance_identity: TaskInstanceIdentity
    task: AbstractTask
    simulation_effect: AbstractSimulationDispatchEffect | None = None

    def __post_init__(self) -> None:
        """Validate exact nominal route shape without performing an effect."""
        if type(self.task_instance_identity) is not TaskInstanceIdentity:
            raise TypeError("task_instance_identity must be TaskInstanceIdentity")
        if not isinstance(self.task, AbstractTask):
            raise TypeError("task must inherit AbstractTask")
        if self.simulation_effect is not None and not isinstance(
            self.simulation_effect, AbstractSimulationDispatchEffect
        ):
            raise TypeError(
                "simulation_effect must inherit "
                "AbstractSimulationDispatchEffect or be None"
            )

        kind = self.task.definition.execution_kind
        if kind is TaskExecutionKind.IN_PROCESS:
            if not isinstance(self.task, AbstractInProcessScientificTask):
                raise TypeError("in-process binding requires its nominal route Task")
            if self.simulation_effect is not None:
                raise ValueError("in-process binding prohibits a simulation effect")
        elif kind is TaskExecutionKind.SIMULATION:
            if not isinstance(self.task, AbstractSimulationTask):
                raise TypeError("simulation binding requires its nominal route Task")
            if self.simulation_effect is None:
                raise ValueError("simulation binding requires a simulation effect")
        elif kind is TaskExecutionKind.NESTED_WORKFLOW:
            if not isinstance(self.task, NestedWorkflowTask):
                raise TypeError("nested binding requires its nominal route Task")
            if self.simulation_effect is not None:
                raise ValueError("nested binding prohibits a simulation effect")
        else:  # pragma: no cover - closed enum defense
            raise TypeError("task definition has an unsupported execution kind")


@final
@dataclass(frozen=True, slots=True)
class WorkflowExecutionBindings:
    """Retain one exact plan and its complete process-local adapter set."""

    plan: WorkflowExecutionPlan
    task_bindings: tuple[WorkflowTaskBinding, ...]

    def __post_init__(self) -> None:
        """Validate exact field types; constructor owns cross-object closure."""
        if type(self.plan) is not WorkflowExecutionPlan:
            raise TypeError("plan must be WorkflowExecutionPlan")
        if type(self.task_bindings) is not tuple or any(
            type(value) is not WorkflowTaskBinding for value in self.task_bindings
        ):
            raise TypeError("task_bindings must be a tuple of WorkflowTaskBinding")


class WorkflowExecutionBindingsConstructor:
    """Correlate one declarative plan with a complete runtime adapter set."""

    __slots__ = ()

    @staticmethod
    def execute(
        plan: WorkflowExecutionPlan,
        task_bindings: tuple[WorkflowTaskBinding, ...],
    ) -> WorkflowExecutionBindings:
        """Validate complete ordered nominal bindings and return them."""
        if type(plan) is not WorkflowExecutionPlan:
            raise TypeError("plan must be WorkflowExecutionPlan")
        if type(task_bindings) is not tuple or any(
            type(value) is not WorkflowTaskBinding for value in task_bindings
        ):
            raise TypeError("task_bindings must be a tuple of WorkflowTaskBinding")

        instances = plan.workflow_definition.composition.task_instances
        if tuple(binding.task_instance_identity for binding in task_bindings) != tuple(
            instance.identity for instance in instances
        ):
            raise ValueError(
                "runtime bindings must match composition identity and order"
            )
        if len(task_bindings) != len(plan.task_definitions):
            raise ValueError("runtime bindings must match every planned definition")

        nested_targets = {
            target.task_instance_identity: target
            for target in plan.nested_workflow_targets
        }
        for binding, instance, definition in zip(
            task_bindings, instances, plan.task_definitions, strict=True
        ):
            if binding.task.identity != instance.definition_identity:
                raise ValueError(
                    "bound Task identity must equal the instance definition identity"
                )
            if binding.task.definition != definition:
                raise ValueError("bound Task definition must equal the plan snapshot")
            if definition.execution_kind is TaskExecutionKind.NESTED_WORKFLOW:
                assert isinstance(binding.task, NestedWorkflowTask)
                target = nested_targets.get(instance.identity)
                if target is None:
                    raise ValueError("nested Task binding requires a plan target")
                if (
                    binding.task.child_workflow_definition
                    != target.child_workflow_definition
                ):
                    raise ValueError(
                        "nested Task child definition must equal the plan target"
                    )

        return WorkflowExecutionBindings(plan=plan, task_bindings=task_bindings)
