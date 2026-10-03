r"""Software verification of ``AbstractScientificTask``.

Evidence profile: routine

Bounded artifact scope: the public nominal ABC identifying scientific engine Tasks.

Facet and represented meaning

The class specializes ``AbstractTask`` semantically without adding a second identity,
execution signature, scheduler, registry, or result wrapper.

Intrinsic and cross-object scope

Tests cover inherited abstract-member enforcement and nominal separation from the
engine-control ``NestedWorkflowTask`` specialization.

VVUQ and scientific exclusions

This is software verification. The synthetic Task performs no scientific calculation,
validation, uncertainty quantification, external effect, or acceptance.
"""

import inspect

import pytest

from ksdft2effmass.workflows import (
    AbstractScientificTask,
    AbstractTask,
    NestedWorkflowTask,
    ResultObject,
    TaskDefinitionIdentity,
    TaskExecutionContext,
    TaskInputBinding,
)

pytestmark = pytest.mark.software_verification


class TestAbstractScientificTask:
    """Verify the nominal ABC for executable scientific operations."""

    def test_incomplete_subclass_cannot_be_instantiated(self) -> None:
        """Retain the inherited identity and execution requirements.

        Evidence ID: SV-WFM-ABSTRACT-SCIENTIFIC-TASK-001
        """

        class IncompleteScientificTask(AbstractScientificTask):
            __slots__ = ()

        assert inspect.isabstract(AbstractScientificTask)
        assert inspect.isabstract(IncompleteScientificTask)
        with pytest.raises(TypeError, match="abstract"):
            IncompleteScientificTask()  # type: ignore[abstract]

    def test_complete_subclass_is_only_scientific_task_specialization(self) -> None:
        """Separate a concrete scientific Task from nested Workflow control.

        Evidence ID: SV-WFM-ABSTRACT-SCIENTIFIC-TASK-002
        """

        class ConcreteScientificTask(AbstractScientificTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return TaskDefinitionIdentity("task.scientific-test")

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                return tuple(binding.result for binding in inputs)

        task = ConcreteScientificTask()
        assert isinstance(task, AbstractScientificTask)
        assert isinstance(task, AbstractTask)
        assert not isinstance(task, NestedWorkflowTask)
        assert task.identity == TaskDefinitionIdentity("task.scientific-test")
        assert not hasattr(task, "__dict__")
