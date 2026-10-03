r"""Software verification of ``AbstractTask``.

Evidence profile: routine

Bounded artifact scope: the public nominal base for maintained scientific Tasks.

Facet and represented meaning

The base requires the exact Task identity and execution contract without supplying
scientific or Workflow-control behavior.

Intrinsic and cross-object scope

Tests cover abstract-member enforcement, nominal inheritance, and structural ``Task``
conformance through the supported package import.

VVUQ and scientific exclusions

This is software verification. The synthetic Task performs no scientific calculation,
validation, uncertainty quantification, external effect, or acceptance.
"""

import inspect

import pytest

from ksdft2effmass.workflows import (
    AbstractTask,
    AttemptIdentity,
    OperationIdentity,
    ResultObject,
    Task,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskExecutionContext,
    TaskInputBinding,
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)

pytestmark = pytest.mark.software_verification


class TestAbstractTask:
    """Verify the nominal base for maintained scientific Tasks."""

    @staticmethod
    def _context() -> TaskExecutionContext:
        return TaskExecutionContext(
            WorkflowIdentity("workflow.abstract-task-test"),
            WorkflowRunIdentity("run.abstract-task-test"),
            TaskInstanceIdentity("instance.abstract-task-test"),
            TaskActivationIdentity("activation.abstract-task-test"),
            OperationIdentity("operation.abstract-task-test"),
            AttemptIdentity("attempt.abstract-task-test"),
        )

    def test_incomplete_subclass_cannot_be_instantiated(self) -> None:
        """Require concrete subclasses to implement identity and execution.

        Evidence ID: SV-WFM-ABSTRACT-TASK-001
        """

        class IncompleteTask(AbstractTask):
            __slots__ = ()

        assert inspect.isabstract(AbstractTask)
        assert inspect.isabstract(IncompleteTask)
        with pytest.raises(TypeError, match="abstract"):
            IncompleteTask()  # type: ignore[abstract]

    def test_complete_subclass_is_nominal_and_structural_task(self) -> None:
        """Accept one complete subclass through both supported Task boundaries.

        Evidence ID: SV-WFM-ABSTRACT-TASK-002
        """

        class ConcreteTask(AbstractTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return TaskDefinitionIdentity("task.abstract-task-test")

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                assert context == TestAbstractTask._context()
                return tuple(binding.result for binding in inputs)

        task = ConcreteTask()
        assert isinstance(task, AbstractTask)
        assert isinstance(task, Task)
        assert task.identity == TaskDefinitionIdentity("task.abstract-task-test")
        assert task.execute((), self._context()) == ()
        assert not hasattr(task, "__dict__")
