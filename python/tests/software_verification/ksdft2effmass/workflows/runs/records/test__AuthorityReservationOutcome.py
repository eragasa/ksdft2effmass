r"""Software verification of ``AuthorityReservationOutcome``.

Evidence profile: routine

Bounded artifact scope: the public ``AuthorityReservationOutcome`` contract.

Facet and represented meaning

This module verifies intrinsic represented behavior owned by
``AuthorityReservationOutcome``.

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
    WorkflowRunIdentity,
)
from ksdft2effmass.workflows.runs import (
    AuthorityReservationOutcome,
    AuthorityReservationOutcomeIdentity,
    AuthorityReservationOutcomeKind,
    ExecutionGrantIdentity,
    ExecutionGrantRevisionIdentity,
    ObligationIdentity,
    ScientificExecutionAuthorityReference,
    ScientificExecutionAuthoritySnapshotIdentity,
    ScientificExecutionAuthorityStateIdentity,
    SimulationExecutionAuthorizationResultIdentity,
    SimulationExecutionRequestIdentity,
    TaskAttemptRecordIdentity,
    WorkflowRunRevisionIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = AuthorityReservationOutcome


class TestAuthorityReservationOutcome:
    """Own software evidence for ``AuthorityReservationOutcome``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-AUTHORITY-RESERVATION-OUTCOME-001

        Requirement: ``AuthorityReservationOutcome`` declares exactly its
        documented public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "workflow_run_identity",
            "workflow_run_revision_identity",
            "authority_reference",
            "authorization_result_identity",
            "request_identity",
            "activation_identity",
            "operation_identity",
            "attempt_identity",
            "attempt_record_identity",
            "obligation_identity",
            "expected_revision_identity",
            "kind",
            "predecessor_reservation_identity",
        )

    def test_constructor__authority_reservation__requires_append_only_claim(
        self,
    ) -> None:
        """Require a claimed grant state to append after one exact reservation.

        Evidence ID: SV-WFR-CONTROL-001

        Requirement: Reserved and claimed authority states are distinct immutable
        records; claimed names its exact reservation predecessor and performs no effect.

        Acceptance: Reserved and successor claimed records construct, while claimed
        without a predecessor raises ``ValueError``.
        """
        reserved = self.make_reservation(
            identity="reservation.one",
            kind=AuthorityReservationOutcomeKind.RESERVED,
        )
        claimed = self.make_reservation(
            identity="reservation.two",
            kind=AuthorityReservationOutcomeKind.CLAIMED,
            predecessor=reserved.identity,
        )

        assert claimed.predecessor_reservation_identity == reserved.identity
        with pytest.raises(ValueError):
            self.make_reservation(
                identity="reservation.invalid",
                kind=AuthorityReservationOutcomeKind.CLAIMED,
            )

    @staticmethod
    def make_authority_reference() -> ScientificExecutionAuthorityReference:
        """Construct one exact externally supplied authority reference."""
        return ScientificExecutionAuthorityReference(
            grant_identity=ExecutionGrantIdentity("grant.one"),
            grant_revision_identity=ExecutionGrantRevisionIdentity(
                "grant-revision.one"
            ),
            snapshot_identity=ScientificExecutionAuthoritySnapshotIdentity(
                "authority-snapshot.one"
            ),
            state_identity=ScientificExecutionAuthorityStateIdentity(
                "authority-state.unused"
            ),
        )

    @classmethod
    def make_reservation(
        cls,
        *,
        identity: str,
        kind: AuthorityReservationOutcomeKind,
        predecessor: AuthorityReservationOutcomeIdentity | None = None,
    ) -> AuthorityReservationOutcome:
        """Construct one reservation-state record for variant evidence."""
        return AuthorityReservationOutcome(
            identity=AuthorityReservationOutcomeIdentity(identity),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            workflow_run_revision_identity=WorkflowRunRevisionIdentity("revision.one"),
            authority_reference=cls.make_authority_reference(),
            authorization_result_identity=(
                SimulationExecutionAuthorizationResultIdentity("authorization.one")
            ),
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            activation_identity=TaskActivationIdentity("activation.one"),
            operation_identity=OperationIdentity("operation.one"),
            attempt_identity=AttemptIdentity("attempt.one"),
            attempt_record_identity=TaskAttemptRecordIdentity("attempt.one.started"),
            obligation_identity=ObligationIdentity("obligation.one"),
            expected_revision_identity=WorkflowRunRevisionIdentity("revision.one"),
            kind=kind,
            predecessor_reservation_identity=predecessor,
        )
