r"""Software verification of ``ObligationDisposition``.

Evidence profile: routine

Bounded artifact scope: the public ``ObligationDisposition`` contract.

Facet and represented meaning

This module verifies intrinsic represented behavior owned by ``ObligationDisposition``.

Intrinsic and cross-object scope

Constructor and field invariants belong to this class. Complete cross-record replay
and package-export agreement remain with their separate owners.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows.runs import (
    DispatchOutcomeRecordIdentity,
    ObligationDisposition,
    ObligationDispositionIdentity,
    ObligationDispositionKind,
    ObligationIdentity,
    SimulationExecutionRequestIdentity,
    TaskAttemptRecordIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = ObligationDisposition


class TestObligationDisposition:
    """Own software evidence for ``ObligationDisposition``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-OBLIGATION-DISPOSITION-001

        Requirement: ``ObligationDisposition`` declares exactly its documented
        public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "obligation_identity",
            "request_identity",
            "dispatch_outcome_record_identity",
            "attempt_record_identity",
            "kind",
            "predecessor_disposition_identity",
            "reconciliation_identity_values",
        )

    def test_constructor__obligation_disposition__requires_completed_predecessor(
        self,
    ) -> None:
        """Require completed disposition to preserve earlier append-only state.

        Evidence ID: SV-WFR-CONTROL-004

        Requirement: Completion appends after an exact earlier disposition and cannot
        erase or authorize redispatch of that record.

        Acceptance: Confirmed then completed records construct, while completed with no
        predecessor raises ``ValueError``.
        """
        confirmed = self.make_disposition(
            identity="disposition.one",
            kind=ObligationDispositionKind.CONFIRMED,
        )
        completed = self.make_disposition(
            identity="disposition.two",
            kind=ObligationDispositionKind.COMPLETED,
            predecessor=confirmed.identity,
        )

        assert completed.predecessor_disposition_identity == confirmed.identity
        with pytest.raises(ValueError):
            self.make_disposition(
                identity="disposition.invalid",
                kind=ObligationDispositionKind.COMPLETED,
            )

    @staticmethod
    def make_disposition(
        *,
        identity: str,
        kind: ObligationDispositionKind,
        predecessor: ObligationDispositionIdentity | None = None,
    ) -> ObligationDisposition:
        """Construct one append-only obligation disposition."""
        return ObligationDisposition(
            identity=ObligationDispositionIdentity(identity),
            obligation_identity=ObligationIdentity("obligation.one"),
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            dispatch_outcome_record_identity=DispatchOutcomeRecordIdentity(
                "dispatch.confirmed"
            ),
            attempt_record_identity=TaskAttemptRecordIdentity("attempt.one.confirmed"),
            kind=kind,
            predecessor_disposition_identity=predecessor,
        )
