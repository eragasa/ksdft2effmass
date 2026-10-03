"""Nominal Workflow engine actions over explicit immutable execution plans."""

from __future__ import annotations

from ksdft2effmass.workflows.model import (
    AbstractScientificTask,
    AbstractSimulationTask,
    NestedWorkflowTask,
    ResultObject,
    ResultObjectIdentity,
    TaskActivation,
    TaskExecutionContext,
    WorkflowExecutionPlan,
)


class WorkflowEngine:
    """Execute exact ordinary in-process scientific Task activations.

    The engine consumes an explicit validated :class:`WorkflowExecutionPlan`; it does
    not discover Tasks or construct authority. Simulation Tasks and nested Workflow
    Tasks fail closed before invocation because they require separate dispatch and
    child-run paths.
    """

    __slots__ = ()

    def execute_in_process(
        self,
        plan: WorkflowExecutionPlan,
        activation: TaskActivation,
    ) -> tuple[ResultObject, ...]:
        """Execute one direct in-process scientific Task activation.

        Parameters
        ----------
        plan
            Complete immutable binding of the Workflow definition to concrete nominal
            Tasks.
        activation
            Exact activation containing the run correlation and already-bound inputs.

        Returns
        -------
        tuple[ResultObject, ...]
            Concrete immutable results returned by the selected scientific Task.

        Raises
        ------
        TypeError
            If either argument or the Task return shape has the wrong semantic type.
        ValueError
            If Workflow or Task-instance correlation fails, the selected Task requires
            a different engine path, or returned result identities are not unique.

        Notes
        -----
        The method derives :class:`TaskExecutionContext` from the activation. It does
        not select activation, authorize an effect, translate Task exceptions, create
        a durable invocation outcome, mutate a Workflow run, or persist state.
        """
        if type(plan) is not WorkflowExecutionPlan:
            raise TypeError("plan must be WorkflowExecutionPlan")
        if type(activation) is not TaskActivation:
            raise TypeError("activation must be TaskActivation")
        if plan.workflow.workflow_identity != activation.workflow_identity:
            raise ValueError("activation must identify the plan Workflow")

        matching = tuple(
            binding
            for binding in plan.task_bindings
            if binding.task_instance.identity == activation.task_instance.identity
        )
        if len(matching) != 1:
            raise ValueError("activation Task instance must be a plan member")
        binding = matching[0]
        if binding.task_instance != activation.task_instance:
            raise ValueError("activation Task instance must equal the planned instance")

        task = binding.task
        if isinstance(task, AbstractSimulationTask):
            raise ValueError("simulation Task requires the external-dispatch path")
        if isinstance(task, NestedWorkflowTask):
            raise ValueError("nested Workflow Task requires the child-run path")
        if not isinstance(task, AbstractScientificTask):
            raise ValueError("Task specialization has no in-process scientific path")

        context = TaskExecutionContext(
            workflow_identity=activation.workflow_identity,
            workflow_run_identity=activation.workflow_run_identity,
            task_instance_identity=activation.task_instance.identity,
            task_activation_identity=activation.identity,
            operation_identity=activation.operation_identity,
            attempt_identity=activation.attempt_identity,
        )
        results = task.execute(activation.inputs, context)
        if type(results) is not tuple or any(
            not isinstance(result, ResultObject) for result in results
        ):
            raise TypeError("Task results must be a tuple of ResultObject")
        identities = tuple(result.identity for result in results)
        if any(type(identity) is not ResultObjectIdentity for identity in identities):
            raise TypeError("Task result identity must be ResultObjectIdentity")
        if len(set(identities)) != len(identities):
            raise ValueError("Task result identities must be unique")
        return results
