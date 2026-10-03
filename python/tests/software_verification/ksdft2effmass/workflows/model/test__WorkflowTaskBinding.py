r"""Software verification of ``WorkflowTaskBinding``.

Evidence profile: routine

Bounded artifact scope: the immutable engine relation between one run-scoped Task
instance and one concrete nominal Task.

Facet and represented meaning

The record binds execution behavior explicitly without a registry or structural Task
acceptance.

Intrinsic and cross-object scope

Tests cover exact TaskInstance ownership, nominal AbstractTask inheritance, and
Task-definition identity agreement.

VVUQ and scientific exclusions

This is software verification. Construction performs no Task execution, scientific
calculation, validation, uncertainty quantification, or acceptance.
"""

import pytest

from ksdft2effmass.workflows import (
    AbstractScientificTask,
    ResultObject,
    TaskDefinitionIdentity,
    TaskExecutionContext,
    TaskInputBinding,
    TaskInstance,
    TaskInstanceIdentity,
    WorkflowTaskBinding,
)

pytestmark = pytest.mark.software_verification


class TestWorkflowTaskBinding:
    """Verify exact nominal Task binding for one Workflow instance."""

    @staticmethod
    def _task(identity: TaskDefinitionIdentity) -> AbstractScientificTask:
        class ConcreteScientificTask(AbstractScientificTask):
            __slots__ = ()

            @property
            def identity(self) -> TaskDefinitionIdentity:
                return identity

            def execute(
                self,
                inputs: tuple[TaskInputBinding, ...],
                context: TaskExecutionContext,
            ) -> tuple[ResultObject, ...]:
                return tuple(binding.result for binding in inputs)

        return ConcreteScientificTask()

    @staticmethod
    def _instance(identity: TaskDefinitionIdentity) -> TaskInstance:
        return TaskInstance(
            TaskInstanceIdentity("instance.binding-test"), identity, None
        )

    def test_constructor_accepts_matching_nominal_task(self) -> None:
        """Bind one concrete scientific Task with the declared definition identity.

        Evidence ID: SV-WFM-WORKFLOW-TASK-BINDING-001
        """
        identity = TaskDefinitionIdentity("task.binding-test")
        instance = self._instance(identity)
        task = self._task(identity)

        binding = WorkflowTaskBinding(instance, task)

        assert binding.task_instance is instance
        assert binding.task is task

    def test_constructor_rejects_non_task_value(self) -> None:
        """Reject values outside the nominal AbstractTask hierarchy.

        Evidence ID: SV-WFM-WORKFLOW-TASK-BINDING-002
        """
        identity = TaskDefinitionIdentity("task.binding-test")
        with pytest.raises(TypeError, match="task must inherit AbstractTask"):
            WorkflowTaskBinding(
                self._instance(identity),
                "not-a-task",  # type: ignore[arg-type]
            )

    def test_constructor_rejects_definition_identity_mismatch(self) -> None:
        """Reject a concrete Task belonging to another reusable definition.

        Evidence ID: SV-WFM-WORKFLOW-TASK-BINDING-003
        """
        instance = self._instance(TaskDefinitionIdentity("task.binding-test"))
        task = self._task(TaskDefinitionIdentity("task.other"))

        with pytest.raises(ValueError, match="task identity must equal"):
            WorkflowTaskBinding(instance, task)
