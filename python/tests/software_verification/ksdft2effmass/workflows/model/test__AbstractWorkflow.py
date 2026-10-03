r"""Software verification of definition-only ``AbstractWorkflow`` ownership."""

import inspect

import pytest

from ksdft2effmass.workflows import (
    AbstractTask,
    AbstractWorkflow,
    WorkflowComposition,
    WorkflowDefinition,
    WorkflowIdentity,
)

pytestmark = pytest.mark.software_verification


class TestAbstractWorkflow:
    """Verify nominal ownership and generic immutable definition construction."""

    def test_incomplete_subclass_cannot_be_instantiated(self) -> None:
        """Require complete Workflow identity and composition properties.

        Evidence ID: SV-WFM-ABSTRACT-WORKFLOW-001
        """

        class IncompleteWorkflow(AbstractWorkflow):
            __slots__ = ()

        assert inspect.isabstract(AbstractWorkflow)
        assert inspect.isabstract(IncompleteWorkflow)

    def test_complete_subclass_builds_definition_and_has_no_execution(self) -> None:
        """Keep a complete Workflow separate from live Tasks and execution.

        Evidence ID: SV-WFM-ABSTRACT-WORKFLOW-002
        """

        class ConcreteWorkflow(AbstractWorkflow):
            __slots__ = ()

            @property
            def identity(self) -> WorkflowIdentity:
                return WorkflowIdentity("workflow.abstract-workflow-test")

            @property
            def composition(self) -> WorkflowComposition:
                return WorkflowComposition(self.identity, ())

        workflow = ConcreteWorkflow()
        assert isinstance(workflow, AbstractWorkflow)
        assert not isinstance(workflow, AbstractTask)
        assert workflow.definition == WorkflowDefinition(
            workflow.identity, workflow.composition
        )
        assert not hasattr(workflow, "execute")
        assert not hasattr(workflow, "__dict__")

    def test_definition_override_is_rejected(self) -> None:
        """Reserve generic definition construction to the nominal base.

        Evidence ID: SV-WFM-ABSTRACT-WORKFLOW-003
        """
        with pytest.raises(TypeError, match="must not override definition"):

            class OverridingWorkflow(AbstractWorkflow):
                __slots__ = ()

                @property
                def identity(self) -> WorkflowIdentity:
                    return WorkflowIdentity("workflow.override-test")

                @property
                def composition(self) -> WorkflowComposition:
                    return WorkflowComposition(self.identity, ())

                @property
                def definition(self) -> WorkflowDefinition:
                    return WorkflowDefinition(self.identity, self.composition)
