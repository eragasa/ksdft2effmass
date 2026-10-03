r"""Software verification of ``WorkflowExecutionPlan``.

Evidence profile: routine

Bounded artifact scope: one immutable explicit binding of a nominal Workflow definition
to its complete concrete Task set.

Facet and represented meaning

The plan closes Task membership and order before engine execution without introducing a
registry, discovery, alternate DAG, or scientific result wrapper.

Intrinsic and cross-object scope

Tests cover nominal Workflow ownership, Workflow/composition identity agreement, exact
ordered binding closure, and both scientific and nested Task specializations.

VVUQ and scientific exclusions

This is software verification. Plan construction performs no Task execution, run
mutation, persistence, scientific calculation, validation, or acceptance.
"""

from typing import Literal

import pytest

from ksdft2effmass.workflows import (
    AbstractScientificTask,
    AbstractSimulationTask,
    AbstractWorkflow,
    NestedWorkflowTask,
    ResultObject,
    TaskDefinitionIdentity,
    TaskExecutionContext,
    TaskInputBinding,
    TaskInstance,
    TaskInstanceIdentity,
    WorkflowComposition,
    WorkflowExecutionPlan,
    WorkflowIdentity,
    WorkflowTaskBinding,
)

pytestmark = pytest.mark.software_verification


class TestWorkflowExecutionPlan:
    """Verify complete ordered executable binding of one Workflow definition."""

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

    @staticmethod
    def _scientific_task(identity: TaskDefinitionIdentity) -> AbstractScientificTask:
        class ConcreteScientificTask(AbstractScientificTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return identity

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                return tuple(binding.result for binding in inputs)

        return ConcreteScientificTask()

    @staticmethod
    def _simulation_task(identity: TaskDefinitionIdentity) -> AbstractSimulationTask:
        class ConcreteSimulationTask(AbstractSimulationTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return identity

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                return tuple(binding.result for binding in inputs)

        return ConcreteSimulationTask()

    @staticmethod
    def _nested_task(
        identity: TaskDefinitionIdentity, child: AbstractWorkflow
    ) -> NestedWorkflowTask:
        class ConcreteNestedWorkflowTask(NestedWorkflowTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return identity

            @property
            def workflow(self) -> AbstractWorkflow:
                return child

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                return tuple(binding.result for binding in inputs)

        return ConcreteNestedWorkflowTask()

    @staticmethod
    def _instance(name: str, definition: TaskDefinitionIdentity) -> TaskInstance:
        return TaskInstance(TaskInstanceIdentity(name), definition, None)

    def test_constructor_accepts_complete_ordered_specialization_bindings(self) -> None:
        """Bind direct, simulation, and nested Tasks in composition order.

        Evidence ID: SV-WFM-WORKFLOW-EXECUTION-PLAN-001
        """
        workflow_identity = WorkflowIdentity("workflow.execution-plan-test")
        scientific_identity = TaskDefinitionIdentity("task.scientific-plan-test")
        simulation_identity = TaskDefinitionIdentity("task.simulation-plan-test")
        nested_identity = TaskDefinitionIdentity("task.nested-plan-test")
        scientific_instance = self._instance(
            "instance.scientific-plan-test", scientific_identity
        )
        simulation_instance = self._instance(
            "instance.simulation-plan-test", simulation_identity
        )
        nested_instance = self._instance("instance.nested-plan-test", nested_identity)
        composition = WorkflowComposition(
            workflow_identity,
            (scientific_instance, simulation_instance, nested_instance),
        )
        workflow = self._workflow(workflow_identity, composition)
        child_identity = WorkflowIdentity("workflow.child-plan-test")
        child = self._workflow(child_identity, WorkflowComposition(child_identity, ()))
        bindings = (
            WorkflowTaskBinding(
                scientific_instance, self._scientific_task(scientific_identity)
            ),
            WorkflowTaskBinding(
                simulation_instance, self._simulation_task(simulation_identity)
            ),
            WorkflowTaskBinding(
                nested_instance, self._nested_task(nested_identity, child)
            ),
        )

        plan = WorkflowExecutionPlan(workflow, bindings)

        assert plan.workflow is workflow
        assert plan.task_bindings is bindings

    def test_constructor_rejects_non_workflow_value(self) -> None:
        """Reject values outside the nominal AbstractWorkflow hierarchy.

        Evidence ID: SV-WFM-WORKFLOW-EXECUTION-PLAN-002
        """
        with pytest.raises(TypeError, match="workflow must inherit AbstractWorkflow"):
            WorkflowExecutionPlan(
                "not-a-workflow",  # type: ignore[arg-type]
                (),
            )

    def test_constructor_rejects_composition_for_another_workflow(self) -> None:
        """Reject a composition whose Workflow identity differs from its owner.

        Evidence ID: SV-WFM-WORKFLOW-EXECUTION-PLAN-003
        """
        workflow = self._workflow(
            WorkflowIdentity("workflow.execution-plan-test"),
            WorkflowComposition(WorkflowIdentity("workflow.other"), ()),
        )

        with pytest.raises(ValueError, match="composition must identify"):
            WorkflowExecutionPlan(workflow, ())

    @pytest.mark.parametrize(
        "mode",
        ("missing", "extra", "reordered"),
        ids=("missing-binding", "extra-binding", "reordered-bindings"),
    )
    def test_constructor_rejects_nonexact_binding_membership_or_order(
        self, mode: Literal["missing", "extra", "reordered"]
    ) -> None:
        """Reject missing, additional, and reordered Task-instance bindings.

        Evidence ID: SV-WFM-WORKFLOW-EXECUTION-PLAN-004
        """
        workflow_identity = WorkflowIdentity("workflow.execution-plan-test")
        first_identity = TaskDefinitionIdentity("task.plan-first")
        second_identity = TaskDefinitionIdentity("task.plan-second")
        first_instance = self._instance("instance.plan-first", first_identity)
        second_instance = self._instance("instance.plan-second", second_identity)
        workflow = self._workflow(
            workflow_identity,
            WorkflowComposition(workflow_identity, (first_instance, second_instance)),
        )
        first = WorkflowTaskBinding(
            first_instance, self._scientific_task(first_identity)
        )
        second = WorkflowTaskBinding(
            second_instance, self._scientific_task(second_identity)
        )
        bindings: tuple[WorkflowTaskBinding, ...]
        if mode == "missing":
            bindings = (first,)
        elif mode == "extra":
            extra_identity = TaskDefinitionIdentity("task.plan-extra")
            extra_instance = self._instance("instance.plan-extra", extra_identity)
            bindings = (
                first,
                second,
                WorkflowTaskBinding(
                    extra_instance, self._scientific_task(extra_identity)
                ),
            )
        else:
            bindings = (second, first)

        with pytest.raises(ValueError, match="exactly match"):
            WorkflowExecutionPlan(workflow, bindings)
