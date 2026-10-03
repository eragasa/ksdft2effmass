r"""Software verification of the closed nominal ``AbstractTask`` hierarchy.

These tests exercise software contracts only. They perform no scientific calculation,
external effect, validation, uncertainty quantification, or acceptance.
"""

import inspect

import pytest

from ksdft2effmass.workflows import (
    AbstractInProcessScientificTask,
    AbstractSimulationTask,
    AbstractTask,
    TaskDefinitionIdentity,
    TaskExecutionKind,
)

pytestmark = pytest.mark.software_verification


class TestAbstractTask:
    """Verify abstract membership and closed route construction."""

    def test_incomplete_base_remains_abstract(self) -> None:
        """Require a stable identity and one concrete route.

        Evidence ID: SV-WFM-ABSTRACT-TASK-001
        """

        class IncompleteTask(AbstractTask):
            __slots__ = ()

        assert inspect.isabstract(AbstractTask)
        assert inspect.isabstract(IncompleteTask)

    def test_concrete_route_less_task_is_rejected(self) -> None:
        """Reject concrete Tasks that bypass all closed route roots.

        Evidence ID: SV-WFM-ABSTRACT-TASK-002
        """
        with pytest.raises(TypeError, match="exactly one route root"):

            class RouteLessTask(AbstractTask):
                __slots__ = ()

                @property
                def identity(self) -> TaskDefinitionIdentity:
                    return TaskDefinitionIdentity("task.route-less-test")

    def test_multiple_route_roots_are_rejected(self) -> None:
        """Reject incompatible route overlap at class construction.

        Evidence ID: SV-WFM-ABSTRACT-TASK-003
        """
        with pytest.raises(TypeError, match="exactly one route root"):

            class OverlappingTask(
                AbstractInProcessScientificTask, AbstractSimulationTask
            ):
                __slots__ = ()

                @property
                def identity(self) -> TaskDefinitionIdentity:
                    return TaskDefinitionIdentity("task.overlap-test")

    def test_route_kind_override_is_rejected(self) -> None:
        """Prevent concrete Tasks from replacing their route-owned kind.

        Evidence ID: SV-WFM-ABSTRACT-TASK-004
        """
        with pytest.raises(TypeError, match="route kind"):

            class OverridingTask(AbstractSimulationTask):
                __slots__ = ()
                _task_execution_kind = TaskExecutionKind.IN_PROCESS

                @property
                def identity(self) -> TaskDefinitionIdentity:
                    return TaskDefinitionIdentity("task.override-test")
