r"""Software verification of bindings-only in-process Workflow execution."""

from dataclasses import dataclass, field
from typing import cast

import pytest

from ksdft2effmass.petrinet.colored import ColoredPetriNetSelectionResultIdentity
from ksdft2effmass.workflows import (
    AbstractInProcessScientificTask,
    AbstractResultObject,
    AbstractSimulationDispatchEffect,
    AbstractSimulationTask,
    AttemptIdentity,
    DirectTaskActivationSelection,
    OperationIdentity,
    ResultObjectIdentity,
    ScientificExecutorIdentity,
    SimulationDispatchEffectRequest,
    SimulationDispatchOutcome,
    TaskActivation,
    TaskActivationIdentity,
    TaskDefinition,
    TaskDefinitionIdentity,
    TaskExecutionContext,
    TaskExecutionKind,
    TaskExecutionResults,
    TaskInputBinding,
    TaskInstance,
    TaskInstanceIdentity,
    WorkflowComposition,
    WorkflowDefinition,
    WorkflowEngine,
    WorkflowExecutionBindings,
    WorkflowExecutionBindingsConstructor,
    WorkflowExecutionPlanConstructor,
    WorkflowIdentity,
    WorkflowRunIdentity,
    WorkflowTaskBinding,
)

pytestmark = pytest.mark.software_verification


class TestWorkflowEngine:
    """Verify exact route selection, context construction, and result boundary."""

    @dataclass(frozen=True, slots=True)
    class SyntheticResult(AbstractResultObject):
        identity: ResultObjectIdentity = field()

    class Effect(AbstractSimulationDispatchEffect):
        __slots__ = ()

        @property
        def executor_identity(self) -> ScientificExecutorIdentity:
            return ScientificExecutorIdentity("executor.engine-test")

        def execute(
            self, request: SimulationDispatchEffectRequest
        ) -> SimulationDispatchOutcome:
            del request
            raise AssertionError("the in-process engine must not invoke an effect")

    @staticmethod
    def _instance(definition_identity: TaskDefinitionIdentity) -> TaskInstance:
        return TaskInstance(
            TaskInstanceIdentity("instance.engine-test"), definition_identity, None
        )

    @staticmethod
    def _activation(
        workflow_identity: WorkflowIdentity,
        instance: TaskInstance,
    ) -> TaskActivation:
        return TaskActivation(
            TaskActivationIdentity("activation.engine-test"),
            workflow_identity,
            WorkflowRunIdentity("run.engine-test"),
            instance,
            OperationIdentity("operation.engine-test"),
            AttemptIdentity("attempt.engine-test"),
            (),
            DirectTaskActivationSelection(
                ColoredPetriNetSelectionResultIdentity("a" * 64)
            ),
        )

    @staticmethod
    def _bindings(
        workflow_identity: WorkflowIdentity,
        instance: TaskInstance,
        task: AbstractInProcessScientificTask | AbstractSimulationTask,
        execution_kind: TaskExecutionKind,
    ) -> WorkflowExecutionBindings:
        workflow_definition = WorkflowDefinition(
            workflow_identity, WorkflowComposition(workflow_identity, (instance,))
        )
        plan = WorkflowExecutionPlanConstructor().execute(
            workflow_definition,
            (TaskDefinition(instance.definition_identity, execution_kind),),
            (),
        )
        if execution_kind is TaskExecutionKind.SIMULATION:
            binding = WorkflowTaskBinding(
                instance.identity, task, TestWorkflowEngine.Effect()
            )
        else:
            binding = WorkflowTaskBinding(instance.identity, task)
        return WorkflowExecutionBindingsConstructor().execute(plan, (binding,))

    def test_execute_in_process_invokes_exact_bound_task(self) -> None:
        """Derive exact context and return the Task's concrete result collection.

        Evidence ID: SV-WFM-WORKFLOW-ENGINE-001
        """
        contexts: list[TaskExecutionContext] = []
        result = self.SyntheticResult(ResultObjectIdentity("result.engine-test"))
        definition_identity = TaskDefinitionIdentity("task.engine-test")

        class ConcreteTask(AbstractInProcessScientificTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return definition_identity

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> TaskExecutionResults:
                assert inputs == ()
                contexts.append(context)
                return TaskExecutionResults((result,))

        workflow_identity = WorkflowIdentity("workflow.engine-test")
        instance = self._instance(definition_identity)
        returned = WorkflowEngine().execute_in_process(
            self._bindings(
                workflow_identity,
                instance,
                ConcreteTask(),
                TaskExecutionKind.IN_PROCESS,
            ),
            self._activation(workflow_identity, instance),
        )

        assert returned == TaskExecutionResults((result,))
        assert contexts == [
            TaskExecutionContext(
                workflow_identity,
                WorkflowRunIdentity("run.engine-test"),
                instance.identity,
                TaskActivationIdentity("activation.engine-test"),
                OperationIdentity("operation.engine-test"),
                AttemptIdentity("attempt.engine-test"),
            )
        ]

    def test_execute_in_process_rejects_other_workflow_or_instance(self) -> None:
        """Require exact activation correlation before invoking a Task.

        Evidence ID: SV-WFM-WORKFLOW-ENGINE-002
        """
        definition_identity = TaskDefinitionIdentity("task.engine-test")

        class ConcreteTask(AbstractInProcessScientificTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return definition_identity

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> TaskExecutionResults:
                del inputs, context
                raise AssertionError("uncorrelated activation must not execute")

        workflow_identity = WorkflowIdentity("workflow.engine-test")
        instance = self._instance(definition_identity)
        bindings = self._bindings(
            workflow_identity,
            instance,
            ConcreteTask(),
            TaskExecutionKind.IN_PROCESS,
        )
        with pytest.raises(ValueError, match="bound Workflow"):
            WorkflowEngine().execute_in_process(
                bindings,
                self._activation(WorkflowIdentity("workflow.other"), instance),
            )
        changed_instance = TaskInstance(
            instance.identity, TaskDefinitionIdentity("task.changed"), None
        )
        with pytest.raises(ValueError, match="equal the planned instance"):
            WorkflowEngine().execute_in_process(
                bindings, self._activation(workflow_identity, changed_instance)
            )

    def test_execute_in_process_rejects_simulation_route_before_effect(self) -> None:
        """Keep authority-bearing simulation effects off the direct route.

        Evidence ID: SV-WFM-WORKFLOW-ENGINE-003
        """
        definition_identity = TaskDefinitionIdentity("task.simulation-engine-test")

        class SimulationTask(AbstractSimulationTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return definition_identity

        workflow_identity = WorkflowIdentity("workflow.engine-test")
        instance = self._instance(definition_identity)
        with pytest.raises(ValueError, match="external-dispatch path"):
            WorkflowEngine().execute_in_process(
                self._bindings(
                    workflow_identity,
                    instance,
                    SimulationTask(),
                    TaskExecutionKind.SIMULATION,
                ),
                self._activation(workflow_identity, instance),
            )

    def test_execute_in_process_requires_exact_results_container(self) -> None:
        """Reject a raw tuple even when its member is nominally valid.

        Evidence ID: SV-WFM-WORKFLOW-ENGINE-004
        """
        result = self.SyntheticResult(ResultObjectIdentity("result.engine-test"))
        definition_identity = TaskDefinitionIdentity("task.bad-result-test")

        class SpecializedResults(TaskExecutionResults):  # type: ignore[misc]
            pass

        class BadTask(AbstractInProcessScientificTask):
            __slots__ = ("_returned",)

            def __init__(
                self,
                returned: TaskExecutionResults | tuple[AbstractResultObject, ...],
            ) -> None:
                self._returned = returned

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return definition_identity

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> TaskExecutionResults:
                del inputs, context
                return cast(TaskExecutionResults, self._returned)

        workflow_identity = WorkflowIdentity("workflow.engine-test")
        instance = self._instance(definition_identity)
        for returned in ((result,), SpecializedResults((result,))):
            with pytest.raises(TypeError, match="TaskExecutionResults"):
                WorkflowEngine().execute_in_process(
                    self._bindings(
                        workflow_identity,
                        instance,
                        BadTask(returned),
                        TaskExecutionKind.IN_PROCESS,
                    ),
                    self._activation(workflow_identity, instance),
                )
