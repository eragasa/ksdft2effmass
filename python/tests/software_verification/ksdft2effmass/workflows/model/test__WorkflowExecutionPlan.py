r"""Software verification of declarative ``WorkflowExecutionPlan`` compilation."""

import pytest

from ksdft2effmass.workflows import (
    NestedWorkflowTarget,
    TaskDefinition,
    TaskDefinitionIdentity,
    TaskExecutionKind,
    TaskInstance,
    TaskInstanceIdentity,
    WorkflowComposition,
    WorkflowDefinition,
    WorkflowExecutionPlan,
    WorkflowExecutionPlanConstructor,
    WorkflowIdentity,
)

pytestmark = pytest.mark.software_verification


class TestWorkflowExecutionPlan:
    """Verify immutable definition snapshots without live runtime owners."""

    @staticmethod
    def _instance(value: str, definition: str) -> TaskInstance:
        return TaskInstance(
            TaskInstanceIdentity(value), TaskDefinitionIdentity(definition), None
        )

    def test_constructor_accepts_complete_ordered_definitions(self) -> None:
        """Compile exact composition order and one applicable nested target.

        Evidence ID: SV-WFM-WORKFLOW-EXECUTION-PLAN-001
        """
        workflow_identity = WorkflowIdentity("workflow.execution-plan-test")
        direct = self._instance("instance.direct", "task.direct")
        nested = self._instance("instance.nested", "task.nested")
        workflow_definition = WorkflowDefinition(
            workflow_identity,
            WorkflowComposition(workflow_identity, (direct, nested)),
        )
        definitions = (
            TaskDefinition(direct.definition_identity, TaskExecutionKind.IN_PROCESS),
            TaskDefinition(
                nested.definition_identity, TaskExecutionKind.NESTED_WORKFLOW
            ),
        )
        child_identity = WorkflowIdentity("workflow.child")
        child_definition = WorkflowDefinition(
            child_identity, WorkflowComposition(child_identity, ())
        )
        target = NestedWorkflowTarget(nested.identity, child_definition)

        plan = WorkflowExecutionPlanConstructor().execute(
            workflow_definition, definitions, (target,)
        )

        assert type(plan) is WorkflowExecutionPlan
        assert plan.workflow_definition is workflow_definition
        assert plan.task_definitions is definitions
        assert plan.nested_workflow_targets == (target,)

    def test_constructor_rejects_definition_membership_or_order_mismatch(self) -> None:
        """Reject missing and reordered definition snapshots.

        Evidence ID: SV-WFM-WORKFLOW-EXECUTION-PLAN-002
        """
        workflow_identity = WorkflowIdentity("workflow.execution-plan-test")
        first = self._instance("instance.first", "task.first")
        second = self._instance("instance.second", "task.second")
        workflow_definition = WorkflowDefinition(
            workflow_identity,
            WorkflowComposition(workflow_identity, (first, second)),
        )
        definitions = (
            TaskDefinition(first.definition_identity, TaskExecutionKind.IN_PROCESS),
            TaskDefinition(second.definition_identity, TaskExecutionKind.SIMULATION),
        )

        with pytest.raises(ValueError, match="composition membership"):
            WorkflowExecutionPlanConstructor().execute(
                workflow_definition, definitions[:1], ()
            )
        with pytest.raises(ValueError, match="composition identity and order"):
            WorkflowExecutionPlanConstructor().execute(
                workflow_definition, tuple(reversed(definitions)), ()
            )

    def test_constructor_rejects_missing_or_inapplicable_nested_target(self) -> None:
        """Require targets exactly for nested-route Task instances.

        Evidence ID: SV-WFM-WORKFLOW-EXECUTION-PLAN-003
        """
        workflow_identity = WorkflowIdentity("workflow.execution-plan-test")
        nested = self._instance("instance.nested", "task.nested")
        workflow_definition = WorkflowDefinition(
            workflow_identity, WorkflowComposition(workflow_identity, (nested,))
        )
        nested_definition = TaskDefinition(
            nested.definition_identity, TaskExecutionKind.NESTED_WORKFLOW
        )

        with pytest.raises(ValueError, match="nested targets must exactly match"):
            WorkflowExecutionPlanConstructor().execute(
                workflow_definition, (nested_definition,), ()
            )

        direct_definition = TaskDefinition(
            nested.definition_identity, TaskExecutionKind.IN_PROCESS
        )
        child_identity = WorkflowIdentity("workflow.child")
        target = NestedWorkflowTarget(
            nested.identity,
            WorkflowDefinition(child_identity, WorkflowComposition(child_identity, ())),
        )
        with pytest.raises(ValueError, match="nested targets must exactly match"):
            WorkflowExecutionPlanConstructor().execute(
                workflow_definition, (direct_definition,), (target,)
            )
