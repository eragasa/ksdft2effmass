r"""Software verification of ``AbstractWorkflow``.

Evidence profile: routine

Bounded artifact scope: the public nominal base for maintained composite Workflows.

Facet and represented meaning

The base retains the Task contract and requires exact Workflow identity and immutable
Task-instance composition.

Intrinsic and cross-object scope

Tests cover abstract-member enforcement, nominal inheritance, and structural ``Task``
and ``Workflow`` conformance through the supported package import.

VVUQ and scientific exclusions

This is software verification. The synthetic Workflow executes no member Task,
scientific calculation, validation, uncertainty quantification, or external effect.
"""

import inspect

import pytest

from ksdft2effmass.workflows import (
    AbstractTask,
    AbstractWorkflow,
    ResultObject,
    Task,
    TaskDefinitionIdentity,
    TaskExecutionContext,
    TaskInputBinding,
    Workflow,
    WorkflowComposition,
    WorkflowIdentity,
)

pytestmark = pytest.mark.software_verification


class TestAbstractWorkflow:
    """Verify the nominal base for maintained composite Workflows."""

    def test_incomplete_subclass_cannot_be_instantiated(self) -> None:
        """Require the complete inherited Task and Workflow property contract.

        Evidence ID: SV-WFM-ABSTRACT-WORKFLOW-001
        """

        class IncompleteWorkflow(AbstractWorkflow):
            __slots__ = ()

        assert inspect.isabstract(AbstractWorkflow)
        assert inspect.isabstract(IncompleteWorkflow)
        with pytest.raises(TypeError, match="abstract"):
            IncompleteWorkflow()  # type: ignore[abstract]

    def test_complete_subclass_is_nominal_and_structural_workflow(self) -> None:
        """Accept one complete subclass through all supported Workflow boundaries.

        Evidence ID: SV-WFM-ABSTRACT-WORKFLOW-002
        """

        class ConcreteWorkflow(AbstractWorkflow):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return TaskDefinitionIdentity("task.abstract-workflow-test")

            @property
            def workflow_identity(self) -> WorkflowIdentity:
                return WorkflowIdentity("workflow.abstract-workflow-test")

            @property
            def composition(self) -> WorkflowComposition:
                return WorkflowComposition(self.workflow_identity, ())

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                return tuple(binding.result for binding in inputs)

        workflow = ConcreteWorkflow()
        assert isinstance(workflow, AbstractWorkflow)
        assert isinstance(workflow, AbstractTask)
        assert isinstance(workflow, Workflow)
        assert isinstance(workflow, Task)
        assert workflow.composition == WorkflowComposition(
            workflow.workflow_identity, ()
        )
        assert not hasattr(workflow, "__dict__")
