r"""Software verification of ``AbstractSimulationTask``.

Evidence profile: routine

Bounded artifact scope: the public nominal ABC identifying externally dispatched
scientific engine Tasks.

Facet and represented meaning

The class specializes ``AbstractScientificTask`` semantically without adding an
execution signature, authority, dispatcher, scheduler, registry, or result wrapper.

Intrinsic and cross-object scope

Tests cover inherited abstract-member enforcement and nominal separation from ordinary
in-process scientific Tasks and nested Workflow control.

VVUQ and scientific exclusions

This is software verification. The synthetic Tasks perform no scientific calculation,
external effect, validation, uncertainty quantification, or acceptance.
"""

import inspect

import pytest

from ksdft2effmass.workflows import (
    AbstractScientificTask,
    AbstractSimulationTask,
    AbstractTask,
    NestedWorkflowTask,
    ResultObject,
    TaskDefinitionIdentity,
    TaskExecutionContext,
    TaskInputBinding,
)

pytestmark = pytest.mark.software_verification


class TestAbstractSimulationTask:
    """Verify the nominal ABC for externally dispatched scientific Tasks."""

    def test_incomplete_subclass_cannot_be_instantiated(self) -> None:
        """Retain the inherited identity and execution requirements.

        Evidence ID: SV-WFM-ABSTRACT-SIMULATION-TASK-001
        """

        class IncompleteSimulationTask(AbstractSimulationTask):
            __slots__ = ()

        assert inspect.isabstract(AbstractSimulationTask)
        assert inspect.isabstract(IncompleteSimulationTask)
        with pytest.raises(TypeError, match="abstract"):
            IncompleteSimulationTask()  # type: ignore[abstract]

    def test_complete_subclass_has_only_simulation_specialization(self) -> None:
        """Separate a simulation Task from ordinary and nested execution branches.

        Evidence ID: SV-WFM-ABSTRACT-SIMULATION-TASK-002
        """

        class ConcreteSimulationTask(AbstractSimulationTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return TaskDefinitionIdentity("task.simulation-test")

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                return tuple(binding.result for binding in inputs)

        class ConcreteScientificTask(AbstractScientificTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return TaskDefinitionIdentity("task.in-process-test")

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                return tuple(binding.result for binding in inputs)

        task = ConcreteSimulationTask()
        ordinary_task = ConcreteScientificTask()

        assert isinstance(task, AbstractSimulationTask)
        assert isinstance(task, AbstractScientificTask)
        assert isinstance(task, AbstractTask)
        assert not isinstance(task, NestedWorkflowTask)
        assert not isinstance(ordinary_task, AbstractSimulationTask)
        assert task.identity == TaskDefinitionIdentity("task.simulation-test")
        assert not hasattr(task, "__dict__")
