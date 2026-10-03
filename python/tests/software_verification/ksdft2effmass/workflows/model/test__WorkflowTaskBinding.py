r"""Software verification of process-local Workflow execution bindings."""

import pytest

from ksdft2effmass.workflows import (
    AbstractInProcessScientificTask,
    AbstractSimulationDispatchEffect,
    AbstractSimulationTask,
    NestedWorkflowTarget,
    NestedWorkflowTask,
    ScientificExecutorIdentity,
    SimulationDispatchEffectRequest,
    SimulationDispatchOutcome,
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
    WorkflowExecutionBindings,
    WorkflowExecutionBindingsConstructor,
    WorkflowExecutionPlanConstructor,
    WorkflowIdentity,
    WorkflowTaskBinding,
)

pytestmark = pytest.mark.software_verification


class TestWorkflowTaskBinding:
    """Verify route-closed runtime records and whole-plan correlation."""

    class InProcessTask(AbstractInProcessScientificTask):
        __slots__ = ("_identity",)

        def __init__(self, identity: TaskDefinitionIdentity) -> None:
            self._identity = identity

        @property
        def identity(self) -> TaskDefinitionIdentity:
            return self._identity

        def execute(
            self,
            inputs: tuple[TaskInputBinding, ...],
            context: TaskExecutionContext,
        ) -> TaskExecutionResults:
            del inputs, context
            raise AssertionError("binding construction must not execute a Task")

    class SimulationTask(AbstractSimulationTask):
        __slots__ = ("_identity",)

        def __init__(self, identity: TaskDefinitionIdentity) -> None:
            self._identity = identity

        @property
        def identity(self) -> TaskDefinitionIdentity:
            return self._identity

    class Effect(AbstractSimulationDispatchEffect):
        __slots__ = ()

        @property
        def executor_identity(self) -> ScientificExecutorIdentity:
            return ScientificExecutorIdentity("executor.binding-test")

        def execute(
            self, request: SimulationDispatchEffectRequest
        ) -> SimulationDispatchOutcome:
            del request
            raise AssertionError("binding construction must not invoke an effect")

    class NestedTask(NestedWorkflowTask):
        __slots__ = ("_identity", "_child")

        def __init__(
            self,
            identity: TaskDefinitionIdentity,
            child: WorkflowDefinition,
        ) -> None:
            self._identity = identity
            self._child = child

        @property
        def identity(self) -> TaskDefinitionIdentity:
            return self._identity

        @property
        def child_workflow_definition(self) -> WorkflowDefinition:
            return self._child

    @staticmethod
    def _instance(value: str, definition: str) -> TaskInstance:
        return TaskInstance(
            TaskInstanceIdentity(value), TaskDefinitionIdentity(definition), None
        )

    def test_binding_record_enforces_route_shape(self) -> None:
        """Require effects only and exactly for the simulation route.

        Evidence ID: SV-WFM-WORKFLOW-TASK-BINDING-001
        """
        identity = TaskDefinitionIdentity("task.binding-test")
        instance_identity = TaskInstanceIdentity("instance.binding-test")
        direct = self.InProcessTask(identity)
        simulation = self.SimulationTask(identity)
        effect = self.Effect()

        assert WorkflowTaskBinding(instance_identity, direct).task is direct
        assert (
            WorkflowTaskBinding(instance_identity, simulation, effect).simulation_effect
            is effect
        )
        with pytest.raises(ValueError, match="prohibits a simulation effect"):
            WorkflowTaskBinding(instance_identity, direct, effect)
        with pytest.raises(ValueError, match="requires a simulation effect"):
            WorkflowTaskBinding(instance_identity, simulation)

    def test_constructor_accepts_complete_ordered_nominal_bindings(self) -> None:
        """Bind each plan snapshot to one exact nominal runtime adapter.

        Evidence ID: SV-WFM-WORKFLOW-TASK-BINDING-002
        """
        workflow_identity = WorkflowIdentity("workflow.binding-test")
        direct_instance = self._instance("instance.direct", "task.direct")
        simulation_instance = self._instance("instance.simulation", "task.simulation")
        nested_instance = self._instance("instance.nested", "task.nested")
        workflow_definition = WorkflowDefinition(
            workflow_identity,
            WorkflowComposition(
                workflow_identity,
                (direct_instance, simulation_instance, nested_instance),
            ),
        )
        definitions = (
            TaskDefinition(
                direct_instance.definition_identity, TaskExecutionKind.IN_PROCESS
            ),
            TaskDefinition(
                simulation_instance.definition_identity, TaskExecutionKind.SIMULATION
            ),
            TaskDefinition(
                nested_instance.definition_identity,
                TaskExecutionKind.NESTED_WORKFLOW,
            ),
        )
        child_identity = WorkflowIdentity("workflow.child-binding-test")
        child = WorkflowDefinition(
            child_identity, WorkflowComposition(child_identity, ())
        )
        plan = WorkflowExecutionPlanConstructor().execute(
            workflow_definition,
            definitions,
            (NestedWorkflowTarget(nested_instance.identity, child),),
        )
        runtime_bindings = (
            WorkflowTaskBinding(
                direct_instance.identity,
                self.InProcessTask(direct_instance.definition_identity),
            ),
            WorkflowTaskBinding(
                simulation_instance.identity,
                self.SimulationTask(simulation_instance.definition_identity),
                self.Effect(),
            ),
            WorkflowTaskBinding(
                nested_instance.identity,
                self.NestedTask(nested_instance.definition_identity, child),
            ),
        )

        bindings = WorkflowExecutionBindingsConstructor().execute(
            plan, runtime_bindings
        )

        assert type(bindings) is WorkflowExecutionBindings
        assert bindings.plan is plan
        assert bindings.task_bindings is runtime_bindings

    def test_constructor_rejects_definition_or_order_mismatch(self) -> None:
        """Reject a runtime adapter that does not equal its declarative slot.

        Evidence ID: SV-WFM-WORKFLOW-TASK-BINDING-003
        """
        workflow_identity = WorkflowIdentity("workflow.binding-test")
        instance = self._instance("instance.direct", "task.direct")
        workflow_definition = WorkflowDefinition(
            workflow_identity, WorkflowComposition(workflow_identity, (instance,))
        )
        plan = WorkflowExecutionPlanConstructor().execute(
            workflow_definition,
            (
                TaskDefinition(
                    instance.definition_identity, TaskExecutionKind.IN_PROCESS
                ),
            ),
            (),
        )
        wrong = WorkflowTaskBinding(
            instance.identity,
            self.InProcessTask(TaskDefinitionIdentity("task.other")),
        )
        with pytest.raises(ValueError, match="identity must equal"):
            WorkflowExecutionBindingsConstructor().execute(plan, (wrong,))
