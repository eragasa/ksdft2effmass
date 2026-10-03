r"""Software verification of ``AbstractInProcessScientificTask``."""

import inspect
from dataclasses import dataclass, field

import pytest

from ksdft2effmass.workflows import (
    AbstractInProcessScientificTask,
    AbstractResultObject,
    AbstractScientificTask,
    ResultObjectIdentity,
    TaskDefinition,
    TaskDefinitionIdentity,
    TaskExecutionContext,
    TaskExecutionKind,
    TaskExecutionResults,
    TaskInputBinding,
)

pytestmark = pytest.mark.software_verification


class TestAbstractInProcessScientificTask:
    """Verify the sole ordinary in-process scientific route."""

    @dataclass(frozen=True, slots=True)
    class SyntheticResult(AbstractResultObject):
        identity: ResultObjectIdentity = field()

    def test_incomplete_subclass_remains_abstract(self) -> None:
        """Require stable identity and the exact execute operation.

        Evidence ID: SV-WFM-IN-PROCESS-SCIENTIFIC-TASK-001
        """

        class IncompleteTask(AbstractInProcessScientificTask):
            __slots__ = ()

        assert inspect.isabstract(IncompleteTask)

    def test_complete_subclass_owns_fixed_route_and_nonempty_results(self) -> None:
        """Construct the generic definition and return the concrete result boundary.

        Evidence ID: SV-WFM-IN-PROCESS-SCIENTIFIC-TASK-002
        """
        result = self.SyntheticResult(ResultObjectIdentity("result.in-process-test"))

        class ConcreteTask(AbstractInProcessScientificTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return TaskDefinitionIdentity("task.in-process-test")

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> TaskExecutionResults:
                del inputs, context
                return TaskExecutionResults((result,))

        task = ConcreteTask()
        assert isinstance(task, AbstractScientificTask)
        assert task.definition == TaskDefinition(
            TaskDefinitionIdentity("task.in-process-test"),
            TaskExecutionKind.IN_PROCESS,
        )
