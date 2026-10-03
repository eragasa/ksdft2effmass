r"""Software verification of definition-only ``NestedWorkflowTask`` routing."""

import inspect

import pytest

from ksdft2effmass.workflows import (
    AbstractScientificTask,
    AbstractTask,
    AbstractWorkflow,
    NestedWorkflowTask,
    TaskDefinition,
    TaskDefinitionIdentity,
    TaskExecutionKind,
    WorkflowComposition,
    WorkflowDefinition,
    WorkflowIdentity,
)

pytestmark = pytest.mark.software_verification


class TestNestedWorkflowTask:
    """Verify immutable child-definition ownership and route separation."""

    def test_incomplete_subclass_cannot_be_instantiated(self) -> None:
        """Require stable Task identity and child Workflow definition.

        Evidence ID: SV-WFM-NESTED-WORKFLOW-TASK-001
        """

        class IncompleteNestedWorkflowTask(NestedWorkflowTask):
            __slots__ = ()

        assert inspect.isabstract(NestedWorkflowTask)
        assert inspect.isabstract(IncompleteNestedWorkflowTask)

    def test_complete_subclass_retains_only_child_definition(self) -> None:
        """Keep the nested route free of a live child owner and direct execution.

        Evidence ID: SV-WFM-NESTED-WORKFLOW-TASK-002
        """
        child_identity = WorkflowIdentity("workflow.nested-child-test")
        child_definition = WorkflowDefinition(
            child_identity, WorkflowComposition(child_identity, ())
        )

        class ConcreteNestedWorkflowTask(NestedWorkflowTask):
            __slots__ = ("_child_definition",)

            def __init__(self, definition: WorkflowDefinition) -> None:
                self._child_definition = definition

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return TaskDefinitionIdentity("task.nested-workflow-test")

            @property
            def child_workflow_definition(self) -> WorkflowDefinition:
                return self._child_definition

        adapter = ConcreteNestedWorkflowTask(child_definition)
        assert isinstance(adapter, NestedWorkflowTask)
        assert isinstance(adapter, AbstractTask)
        assert not isinstance(adapter, AbstractScientificTask)
        assert not isinstance(adapter, AbstractWorkflow)
        assert adapter.child_workflow_definition is child_definition
        assert adapter.definition == TaskDefinition(
            TaskDefinitionIdentity("task.nested-workflow-test"),
            TaskExecutionKind.NESTED_WORKFLOW,
        )
        assert not hasattr(adapter, "execute")
        assert not hasattr(adapter, "__dict__")
