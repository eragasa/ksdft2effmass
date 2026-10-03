r"""Software verification of ``WorkflowEngine`` in-process execution.

Evidence profile: routine

Bounded artifact scope: one stateless ActionObject executing an exact ordinary
scientific Task activation from a validated immutable Workflow execution plan.

Facet and represented meaning

The engine correlates explicit Workflow, Task-instance, activation, operation, and
attempt identities; derives Task context; and validates returned ResultObjects.

Intrinsic and cross-object scope

Tests cover exact plan correlation, one successful direct invocation, fail-closed
simulation/nested/unknown branches, return validation, and unchanged Task failures.

VVUQ and scientific exclusions

This is software verification using synthetic in-memory Tasks. It performs no external
execution and establishes no numerical verification, scientific validation,
uncertainty quantification, convergence, or acceptance.
"""

from dataclasses import dataclass

import pytest

from ksdft2effmass.petrinet.colored import ColoredPetriNetSelectionResultIdentity
from ksdft2effmass.workflows import (
    AbstractScientificTask,
    AbstractSimulationTask,
    AbstractTask,
    AbstractWorkflow,
    AttemptIdentity,
    DirectTaskActivationSelection,
    NestedWorkflowTask,
    OperationIdentity,
    ResultObject,
    ResultObjectIdentity,
    TaskActivation,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskExecutionContext,
    TaskInputBinding,
    TaskInstance,
    TaskInstanceIdentity,
    WorkflowComposition,
    WorkflowEngine,
    WorkflowExecutionPlan,
    WorkflowIdentity,
    WorkflowRunIdentity,
    WorkflowTaskBinding,
)

pytestmark = pytest.mark.software_verification


class TestWorkflowEngine:
    """Verify one exact ordinary in-process scientific invocation."""

    @dataclass(frozen=True, slots=True)
    class SyntheticResult:
        """Minimal immutable synthetic result used only by this test owner."""

        identity: ResultObjectIdentity

    @staticmethod
    def _workflow(
        workflow_identity: WorkflowIdentity,
        composition: WorkflowComposition,
    ) -> AbstractWorkflow:
        class ConcreteWorkflow(AbstractWorkflow):
            __slots__ = ()

            @property
            def workflow_identity(self) -> WorkflowIdentity:
                return workflow_identity

            @property
            def composition(self) -> WorkflowComposition:
                return composition

        return ConcreteWorkflow()

    @classmethod
    def _plan(
        cls,
        workflow_identity: WorkflowIdentity,
        task_instance: TaskInstance,
        task: AbstractTask,
    ) -> WorkflowExecutionPlan:
        composition = WorkflowComposition(workflow_identity, (task_instance,))
        return WorkflowExecutionPlan(
            cls._workflow(workflow_identity, composition),
            (WorkflowTaskBinding(task_instance, task),),
        )

    @staticmethod
    def _activation(
        workflow_identity: WorkflowIdentity,
        task_instance: TaskInstance,
        inputs: tuple[TaskInputBinding, ...] = (),
    ) -> TaskActivation:
        return TaskActivation(
            TaskActivationIdentity("activation.engine-test"),
            workflow_identity,
            WorkflowRunIdentity("run.engine-test"),
            task_instance,
            OperationIdentity("operation.engine-test"),
            AttemptIdentity("attempt.engine-test"),
            inputs,
            DirectTaskActivationSelection(
                ColoredPetriNetSelectionResultIdentity("a" * 64)
            ),
        )

    @staticmethod
    def _instance(
        definition_identity: TaskDefinitionIdentity,
    ) -> TaskInstance:
        return TaskInstance(
            TaskInstanceIdentity("instance.engine-test"), definition_identity, None
        )

    def test_execute_in_process_invokes_exact_direct_scientific_task(self) -> None:
        """Derive exact context and return the direct Task's immutable results.

        Evidence ID: SV-WFM-WORKFLOW-ENGINE-001
        """
        contexts: list[TaskExecutionContext] = []
        result = self.SyntheticResult(ResultObjectIdentity("result.engine-test"))
        definition_identity = TaskDefinitionIdentity("task.engine-test")

        class ConcreteScientificTask(AbstractScientificTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return definition_identity

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                contexts.append(context)
                return (result,)

        workflow_identity = WorkflowIdentity("workflow.engine-test")
        task = ConcreteScientificTask()
        instance = self._instance(definition_identity)
        activation = self._activation(workflow_identity, instance)

        returned = WorkflowEngine().execute_in_process(
            self._plan(workflow_identity, instance, task), activation
        )

        assert returned == (result,)
        assert contexts == [
            TaskExecutionContext(
                workflow_identity=workflow_identity,
                workflow_run_identity=activation.workflow_run_identity,
                task_instance_identity=instance.identity,
                task_activation_identity=activation.identity,
                operation_identity=activation.operation_identity,
                attempt_identity=activation.attempt_identity,
            )
        ]

    def test_execute_in_process_rejects_other_workflow(self) -> None:
        """Reject an activation naming a Workflow other than the plan owner.

        Evidence ID: SV-WFM-WORKFLOW-ENGINE-002
        """
        definition_identity = TaskDefinitionIdentity("task.engine-test")

        class ConcreteScientificTask(AbstractScientificTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return definition_identity

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                raise AssertionError("mismatched Workflow must not execute")

        instance = self._instance(definition_identity)
        plan = self._plan(
            WorkflowIdentity("workflow.engine-test"),
            instance,
            ConcreteScientificTask(),
        )
        activation = self._activation(WorkflowIdentity("workflow.other"), instance)

        with pytest.raises(ValueError, match="plan Workflow"):
            WorkflowEngine().execute_in_process(plan, activation)

    def test_execute_in_process_rejects_changed_task_instance(self) -> None:
        """Reject an equal-identity activation instance with different definition.

        Evidence ID: SV-WFM-WORKFLOW-ENGINE-003
        """
        definition_identity = TaskDefinitionIdentity("task.engine-test")

        class ConcreteScientificTask(AbstractScientificTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return definition_identity

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                raise AssertionError("changed Task instance must not execute")

        workflow_identity = WorkflowIdentity("workflow.engine-test")
        planned_instance = self._instance(definition_identity)
        changed_instance = TaskInstance(
            planned_instance.identity,
            TaskDefinitionIdentity("task.changed"),
            None,
        )

        with pytest.raises(ValueError, match="equal the planned instance"):
            WorkflowEngine().execute_in_process(
                self._plan(
                    workflow_identity, planned_instance, ConcreteScientificTask()
                ),
                self._activation(workflow_identity, changed_instance),
            )

    def test_execute_in_process_rejects_simulation_task_before_invocation(self) -> None:
        """Keep externally dispatched simulation Tasks off the direct path.

        Evidence ID: SV-WFM-WORKFLOW-ENGINE-004
        """
        definition_identity = TaskDefinitionIdentity("task.simulation-engine-test")
        invoked = False

        class ConcreteSimulationTask(AbstractSimulationTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return definition_identity

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                nonlocal invoked
                invoked = True
                return ()

        workflow_identity = WorkflowIdentity("workflow.engine-test")
        instance = self._instance(definition_identity)

        with pytest.raises(ValueError, match="external-dispatch path"):
            WorkflowEngine().execute_in_process(
                self._plan(workflow_identity, instance, ConcreteSimulationTask()),
                self._activation(workflow_identity, instance),
            )
        assert not invoked

    def test_execute_in_process_rejects_nested_task_before_invocation(self) -> None:
        """Keep child Workflow Tasks off the direct scientific path.

        Evidence ID: SV-WFM-WORKFLOW-ENGINE-005
        """
        definition_identity = TaskDefinitionIdentity("task.nested-engine-test")
        child_identity = WorkflowIdentity("workflow.child-engine-test")
        child = self._workflow(child_identity, WorkflowComposition(child_identity, ()))
        invoked = False

        class ConcreteNestedTask(NestedWorkflowTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return definition_identity

            @property
            def workflow(self) -> AbstractWorkflow:
                return child

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                nonlocal invoked
                invoked = True
                return ()

        workflow_identity = WorkflowIdentity("workflow.engine-test")
        instance = self._instance(definition_identity)

        with pytest.raises(ValueError, match="child-run path"):
            WorkflowEngine().execute_in_process(
                self._plan(workflow_identity, instance, ConcreteNestedTask()),
                self._activation(workflow_identity, instance),
            )
        assert not invoked

    def test_execute_in_process_rejects_unknown_task_specialization(self) -> None:
        """Fail closed for generic Tasks without an implemented engine path.

        Evidence ID: SV-WFM-WORKFLOW-ENGINE-006
        """
        definition_identity = TaskDefinitionIdentity("task.generic-engine-test")

        class ConcreteGenericTask(AbstractTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return definition_identity

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                raise AssertionError("unknown Task specialization must not execute")

        workflow_identity = WorkflowIdentity("workflow.engine-test")
        instance = self._instance(definition_identity)

        with pytest.raises(ValueError, match="no in-process scientific path"):
            WorkflowEngine().execute_in_process(
                self._plan(workflow_identity, instance, ConcreteGenericTask()),
                self._activation(workflow_identity, instance),
            )

    def test_execute_in_process_rejects_non_tuple_results(self) -> None:
        """Reject a Task return outside the exact immutable result tuple contract.

        Evidence ID: SV-WFM-WORKFLOW-ENGINE-007
        """
        definition_identity = TaskDefinitionIdentity("task.bad-return-engine-test")

        class BadReturnTask(AbstractScientificTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return definition_identity

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                return []  # type: ignore[return-value]

        workflow_identity = WorkflowIdentity("workflow.engine-test")
        instance = self._instance(definition_identity)

        with pytest.raises(TypeError, match="tuple of ResultObject"):
            WorkflowEngine().execute_in_process(
                self._plan(workflow_identity, instance, BadReturnTask()),
                self._activation(workflow_identity, instance),
            )

    def test_execute_in_process_rejects_duplicate_result_identities(self) -> None:
        """Reject multiple returned results sharing one exact identity.

        Evidence ID: SV-WFM-WORKFLOW-ENGINE-008
        """
        definition_identity = TaskDefinitionIdentity("task.duplicate-engine-test")
        first = self.SyntheticResult(ResultObjectIdentity("result.duplicate"))
        second = self.SyntheticResult(ResultObjectIdentity("result.duplicate"))

        class DuplicateResultTask(AbstractScientificTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return definition_identity

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                return (first, second)

        workflow_identity = WorkflowIdentity("workflow.engine-test")
        instance = self._instance(definition_identity)

        with pytest.raises(ValueError, match="identities must be unique"):
            WorkflowEngine().execute_in_process(
                self._plan(workflow_identity, instance, DuplicateResultTask()),
                self._activation(workflow_identity, instance),
            )

    def test_execute_in_process_propagates_task_failure(self) -> None:
        """Leave Task exception translation to later Workflow control.

        Evidence ID: SV-WFM-WORKFLOW-ENGINE-009
        """
        definition_identity = TaskDefinitionIdentity("task.failure-engine-test")

        class FailingTask(AbstractScientificTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return definition_identity

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                raise RuntimeError("synthetic task failure")

        workflow_identity = WorkflowIdentity("workflow.engine-test")
        instance = self._instance(definition_identity)

        with pytest.raises(RuntimeError, match="synthetic task failure"):
            WorkflowEngine().execute_in_process(
                self._plan(workflow_identity, instance, FailingTask()),
                self._activation(workflow_identity, instance),
            )
