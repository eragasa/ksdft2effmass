r"""Software verification of ``AbstractWorkflow``.

Evidence profile: routine

Bounded artifact scope: the public nominal ABC for maintained Workflow definitions.

Facet and represented meaning

The base requires exact Workflow identity and immutable Task-instance composition while
remaining separate from executable Tasks.

Intrinsic and cross-object scope

Tests cover abstract-member enforcement, nominal inheritance, composition, and absence
of inherited Task execution through the supported package import.

VVUQ and scientific exclusions

This is software verification. The synthetic Workflow executes no Task, scientific
calculation, validation, uncertainty quantification, or external effect.
"""

import inspect

import pytest

from ksdft2effmass.workflows import (
    AbstractTask,
    AbstractWorkflow,
    WorkflowComposition,
    WorkflowIdentity,
)

pytestmark = pytest.mark.software_verification


class TestAbstractWorkflow:
    """Verify the nominal ABC for maintained Workflow definitions."""

    def test_incomplete_subclass_cannot_be_instantiated(self) -> None:
        """Require the complete Workflow identity and composition contract.

        Evidence ID: SV-WFM-ABSTRACT-WORKFLOW-001
        """

        class IncompleteWorkflow(AbstractWorkflow):
            __slots__ = ()

        assert inspect.isabstract(AbstractWorkflow)
        assert inspect.isabstract(IncompleteWorkflow)
        with pytest.raises(TypeError, match="abstract"):
            IncompleteWorkflow()  # type: ignore[abstract]

    def test_complete_subclass_is_definition_only_workflow(self) -> None:
        """Keep one complete Workflow nominally separate from executable Tasks.

        Evidence ID: SV-WFM-ABSTRACT-WORKFLOW-002
        """

        class ConcreteWorkflow(AbstractWorkflow):
            __slots__ = ()

            @property
            def workflow_identity(self) -> WorkflowIdentity:
                return WorkflowIdentity("workflow.abstract-workflow-test")

            @property
            def composition(self) -> WorkflowComposition:
                return WorkflowComposition(self.workflow_identity, ())

        workflow = ConcreteWorkflow()
        assert isinstance(workflow, AbstractWorkflow)
        assert not isinstance(workflow, AbstractTask)
        assert workflow.composition == WorkflowComposition(
            workflow.workflow_identity, ()
        )
        assert not hasattr(workflow, "identity")
        assert not hasattr(workflow, "execute")
        assert not hasattr(workflow, "__dict__")
