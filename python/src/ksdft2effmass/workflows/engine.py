"""Nominal Workflow engine action over validated process-local bindings."""

from __future__ import annotations

from .bindings import WorkflowExecutionBindings
from .definitions import TaskExecutionKind
from .model import TaskActivation, TaskExecutionContext, TaskExecutionResults
from .tasks import AbstractInProcessScientificTask


class WorkflowEngine:
    """Execute exact ordinary in-process scientific Task activations."""

    __slots__ = ()

    def execute_in_process(
        self,
        bindings: WorkflowExecutionBindings,
        activation: TaskActivation,
    ) -> TaskExecutionResults:
        """Execute one direct in-process activation from validated bindings.

        Parameters
        ----------
        bindings
            Complete process-local bindings containing the exact declarative plan.
        activation
            Exact activation containing run correlation and already-bound inputs.

        Returns
        -------
        TaskExecutionResults
            Ordered nonempty nominal results returned by the selected Task.

        Raises
        ------
        TypeError
            An argument, bound adapter, or return value has the wrong semantic type.
        ValueError
            Workflow, Task-instance, or route correlation fails.
        """
        if type(bindings) is not WorkflowExecutionBindings:
            raise TypeError("bindings must be WorkflowExecutionBindings")
        if type(activation) is not TaskActivation:
            raise TypeError("activation must be TaskActivation")

        plan = bindings.plan
        if plan.workflow_definition.identity != activation.workflow_identity:
            raise ValueError("activation must identify the bound Workflow")

        matches = tuple(
            (runtime_binding, definition, instance)
            for runtime_binding, definition, instance in zip(
                bindings.task_bindings,
                plan.task_definitions,
                plan.workflow_definition.composition.task_instances,
                strict=True,
            )
            if instance.identity == activation.task_instance.identity
        )
        if len(matches) != 1:
            raise ValueError("activation Task instance must be a plan member")
        runtime_binding, definition, instance = matches[0]
        if instance != activation.task_instance:
            raise ValueError("activation Task instance must equal the planned instance")
        if definition.execution_kind is not TaskExecutionKind.IN_PROCESS:
            if definition.execution_kind is TaskExecutionKind.SIMULATION:
                raise ValueError("simulation Task requires the external-dispatch path")
            if definition.execution_kind is TaskExecutionKind.NESTED_WORKFLOW:
                raise ValueError("nested Workflow Task requires the child-run path")
            raise ValueError("Task definition has no in-process route")

        task = runtime_binding.task
        if not isinstance(task, AbstractInProcessScientificTask):
            raise TypeError("in-process binding must contain its nominal route Task")
        context = TaskExecutionContext(
            workflow_identity=activation.workflow_identity,
            workflow_run_identity=activation.workflow_run_identity,
            task_instance_identity=activation.task_instance.identity,
            task_activation_identity=activation.identity,
            operation_identity=activation.operation_identity,
            attempt_identity=activation.attempt_identity,
        )
        results = task.execute(activation.inputs, context)
        if type(results) is not TaskExecutionResults:
            raise TypeError("Task must return TaskExecutionResults")
        return results
