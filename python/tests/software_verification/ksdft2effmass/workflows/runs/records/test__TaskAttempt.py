r"""Software verification of ``TaskAttempt``.

Evidence profile: routine

Bounded artifact scope: the public ``TaskAttempt`` contract.

Facet and represented meaning

This module verifies intrinsic represented behavior owned by ``TaskAttempt``.

Intrinsic and cross-object scope

Constructor and field invariants belong to this class. Complete cross-record replay
and package-export agreement remain with their separate owners.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows import (
    AttemptIdentity,
    OperationIdentity,
    TaskActivationIdentity,
    TaskInstanceIdentity,
    WorkflowRunIdentity,
)
from ksdft2effmass.workflows.runs import (
    TaskAttempt,
    TaskAttemptRecordIdentity,
    TaskAttemptStatus,
)

pytestmark = pytest.mark.software_verification
SUT = TaskAttempt


class TestTaskAttempt:
    """Own software evidence for ``TaskAttempt``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-TASK-ATTEMPT-001

        Requirement: ``TaskAttempt`` declares exactly its documented public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "workflow_run_identity",
            "task_instance_identity",
            "activation_identity",
            "operation_identity",
            "attempt_identity",
            "status",
            "predecessor_attempt_record_identity",
            "retry_of_attempt_identity",
            "child_workflow_run_identity",
        )

    def test_constructor__task_attempt__rejects_self_record_predecessor(self) -> None:
        """Reject a terminal state record that names itself as predecessor.

        Evidence ID: SV-WFR-RECORDS-002

        Requirement: Attempt state is append-only and a terminal state record names
        an earlier distinct record for the same stable attempt.

        Acceptance: Equal state-record and predecessor identities raise ``ValueError``.
        """
        record_identity = TaskAttemptRecordIdentity("attempt.one.confirmed")
        with pytest.raises(ValueError):
            TaskAttempt(
                identity=record_identity,
                workflow_run_identity=WorkflowRunIdentity("run.one"),
                task_instance_identity=TaskInstanceIdentity("instance.one"),
                activation_identity=self.make_activation_identity(),
                operation_identity=OperationIdentity("operation.one"),
                attempt_identity=AttemptIdentity("attempt.one"),
                status=TaskAttemptStatus.CONFIRMED,
                predecessor_attempt_record_identity=record_identity,
            )

    @staticmethod
    def make_activation_identity() -> TaskActivationIdentity:
        """Construct the exact activation identity used by record tests."""
        return TaskActivationIdentity("activation.one")
