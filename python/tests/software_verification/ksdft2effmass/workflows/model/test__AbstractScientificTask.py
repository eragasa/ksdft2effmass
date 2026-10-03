r"""Software verification of route-less ``AbstractScientificTask`` grouping."""

import inspect

import pytest

from ksdft2effmass.workflows import (
    AbstractScientificTask,
    AbstractTask,
    TaskDefinitionIdentity,
)

pytestmark = pytest.mark.software_verification


class TestAbstractScientificTask:
    """Verify that scientific grouping does not silently select execution."""

    def test_grouping_base_remains_abstract(self) -> None:
        """Retain the inherited stable identity requirement.

        Evidence ID: SV-WFM-ABSTRACT-SCIENTIFIC-TASK-001
        """
        assert inspect.isabstract(AbstractScientificTask)
        assert issubclass(AbstractScientificTask, AbstractTask)

    def test_concrete_direct_subclass_is_rejected(self) -> None:
        """Require a scientific Task to choose an explicit route root.

        Evidence ID: SV-WFM-ABSTRACT-SCIENTIFIC-TASK-002
        """
        with pytest.raises(TypeError, match="exactly one route root"):

            class RouteLessScientificTask(AbstractScientificTask):
                __slots__ = ()

                @property
                def identity(self) -> TaskDefinitionIdentity:
                    return TaskDefinitionIdentity("task.scientific-route-less-test")
