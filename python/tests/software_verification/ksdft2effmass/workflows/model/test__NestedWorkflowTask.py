r"""Software verification of ``NestedWorkflowTask``.

Evidence profile: routine

Bounded artifact scope: the public ABC for controlled child-Workflow Task adapters.

Facet and represented meaning

The adapter remains an executable ``AbstractTask`` while explicitly targeting one
separate definition-only ``AbstractWorkflow``.

Intrinsic and cross-object scope

Tests cover abstract-member enforcement, nominal inheritance, target identity, and the
absence of Workflow-definition inheritance.

VVUQ and scientific exclusions

This is software verification. The synthetic adapter creates no child run, invokes no
Task, performs no scientific calculation, and exports no result.
"""

import inspect

import pytest

from ksdft2effmass.workflows import (
    AbstractScientificTask,
    AbstractTask,
    AbstractWorkflow,
    NestedWorkflowTask,
    ResultObject,
    TaskDefinitionIdentity,
    TaskExecutionContext,
    TaskInputBinding,
    WorkflowComposition,
    WorkflowIdentity,
)

pytestmark = pytest.mark.software_verification


class TestNestedWorkflowTask:
    """Verify the nominal ABC for controlled nested-Workflow adapters."""

    def test_incomplete_subclass_cannot_be_instantiated(self) -> None:
        """Require Task execution and an exact child Workflow definition.

        Evidence ID: SV-WFM-NESTED-WORKFLOW-TASK-001
        """

        class IncompleteNestedWorkflowTask(NestedWorkflowTask):
            __slots__ = ()

        assert inspect.isabstract(NestedWorkflowTask)
        assert inspect.isabstract(IncompleteNestedWorkflowTask)
        with pytest.raises(TypeError, match="abstract"):
            IncompleteNestedWorkflowTask()  # type: ignore[abstract]

    def test_complete_subclass_is_task_targeting_separate_workflow(self) -> None:
        """Keep the adapter nominally executable and its target definition-only.

        Evidence ID: SV-WFM-NESTED-WORKFLOW-TASK-002
        """

        class ChildWorkflow(AbstractWorkflow):
            __slots__ = ()

            @property
            def workflow_identity(self) -> WorkflowIdentity:
                return WorkflowIdentity("workflow.nested-child-test")

            @property
            def composition(self) -> WorkflowComposition:
                return WorkflowComposition(self.workflow_identity, ())

        class ConcreteNestedWorkflowTask(NestedWorkflowTask):
            __slots__ = ("_workflow",)

            def __init__(self, workflow: AbstractWorkflow) -> None:
                self._workflow = workflow

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return TaskDefinitionIdentity("task.nested-workflow-test")

            @property
            def workflow(self) -> AbstractWorkflow:
                return self._workflow

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                return tuple(binding.result for binding in inputs)

        child = ChildWorkflow()
        adapter = ConcreteNestedWorkflowTask(child)
        assert isinstance(adapter, NestedWorkflowTask)
        assert isinstance(adapter, AbstractTask)
        assert not isinstance(adapter, AbstractScientificTask)
        assert not isinstance(adapter, AbstractWorkflow)
        assert adapter.workflow is child
        assert adapter.identity == TaskDefinitionIdentity("task.nested-workflow-test")
        assert not hasattr(adapter, "__dict__")
