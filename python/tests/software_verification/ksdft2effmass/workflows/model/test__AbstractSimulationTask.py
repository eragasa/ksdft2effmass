r"""Software verification of definition-only ``AbstractSimulationTask``."""

import inspect

import pytest

from ksdft2effmass.workflows import (
    AbstractScientificTask,
    AbstractSimulationTask,
    AbstractTask,
    NestedWorkflowTask,
    TaskDefinition,
    TaskDefinitionIdentity,
    TaskExecutionKind,
)

pytestmark = pytest.mark.software_verification


class TestAbstractSimulationTask:
    """Verify the nominal simulation route without direct execution."""

    def test_incomplete_subclass_cannot_be_instantiated(self) -> None:
        """Require the inherited stable Task identity.

        Evidence ID: SV-WFM-ABSTRACT-SIMULATION-TASK-001
        """

        class IncompleteSimulationTask(AbstractSimulationTask):
            __slots__ = ()

        assert inspect.isabstract(AbstractSimulationTask)
        assert inspect.isabstract(IncompleteSimulationTask)

    def test_complete_subclass_has_fixed_definition_only_route(self) -> None:
        """Construct the generic definition and expose no direct execute method.

        Evidence ID: SV-WFM-ABSTRACT-SIMULATION-TASK-002
        """

        class ConcreteSimulationTask(AbstractSimulationTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return TaskDefinitionIdentity("task.simulation-test")

        task = ConcreteSimulationTask()
        assert isinstance(task, AbstractSimulationTask)
        assert isinstance(task, AbstractScientificTask)
        assert isinstance(task, AbstractTask)
        assert not isinstance(task, NestedWorkflowTask)
        assert task.definition == TaskDefinition(
            TaskDefinitionIdentity("task.simulation-test"),
            TaskExecutionKind.SIMULATION,
        )
        assert not hasattr(task, "execute")
        assert not hasattr(task, "__dict__")
