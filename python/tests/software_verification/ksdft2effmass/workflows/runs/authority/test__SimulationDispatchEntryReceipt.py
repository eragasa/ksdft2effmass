r"""Software verification of ``SimulationDispatchEntryReceipt``.

Evidence profile: routine

Bounded artifact scope: the public dispatch-entry receipt DataObject.

Facet and represented meaning

This module verifies exact receipt fields and distinct revision invariants.

Intrinsic and cross-object scope

Request and adapter correlation remain with their owning control evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes typed receipt invariants, not a
persistence implementation, external execution, or scientific acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.workflows import WorkflowRunIdentity
from ksdft2effmass.workflows.runs import (
    AuthorityReservationOutcomeIdentity,
    ObligationIdentity,
    SimulationDispatchEntryIdentity,
    SimulationDispatchEntryReceipt,
    SimulationDispatchEntryReceiptIdentity,
    SimulationDispatchOutcomeIdentity,
    WorkflowRunClaimCommitReceiptIdentity,
    WorkflowRunRevisionIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchEntryReceipt


class TestSimulationDispatchEntryReceipt:
    """Own software evidence for dispatch-entry receipt invariants."""

    @staticmethod
    def receipt() -> SimulationDispatchEntryReceipt:
        """Construct one synthetic typed receipt without persistence."""
        return SUT(
            identity=SimulationDispatchEntryReceiptIdentity("receipt.one"),
            dispatch_entry_identity=SimulationDispatchEntryIdentity("entry.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            claim_commit_receipt_identity=WorkflowRunClaimCommitReceiptIdentity(
                "claim-receipt.one"
            ),
            predecessor_revision_identity=WorkflowRunRevisionIdentity(
                "revision.claimed"
            ),
            committed_revision_identity=WorkflowRunRevisionIdentity("revision.entered"),
            claimed_reservation_identity=AuthorityReservationOutcomeIdentity(
                "claim.one"
            ),
            obligation_identity=ObligationIdentity("obligation.one"),
            outcome_identity=SimulationDispatchOutcomeIdentity("outcome.one"),
            workflow_run_content_identity="content.one",
            persistence_operation_identity="operation.one",
            persistence_implementation_identity="implementation.one",
        )

    def test_constructor__receipt__requires_distinct_revisions(self) -> None:
        """Reject a receipt that does not represent a new committed revision.

        Evidence ID: SV-WFR-DISPATCH-ENTRY-RECEIPT-001
        """
        receipt = self.receipt()
        assert receipt.committed_revision_identity.value == "revision.entered"
        with pytest.raises(ValueError):
            replace(
                receipt,
                committed_revision_identity=receipt.predecessor_revision_identity,
            )
