r"""Software verification of ``SimulationDispatchEntry``.

Evidence profile: routine

Bounded artifact scope: the public durable dispatch-entry DataObject.

Facet and represented meaning

This module verifies exact lifecycle-state fields and revision separation.

Intrinsic and cross-object scope

Receipt, request, and aggregate replay correlations remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no persistence implementation,
external execution, scientific validation, uncertainty quantification, or acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.workflows import WorkflowRunIdentity
from ksdft2effmass.workflows.runs import (
    AuthorityReservationOutcomeIdentity,
    ObligationIdentity,
    SimulationDispatchEntry,
    SimulationDispatchEntryIdentity,
    SimulationDispatchEntryReceiptIdentity,
    SimulationDispatchOutcomeIdentity,
    SimulationExecutionRequestIdentity,
    WorkflowRunRevisionIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchEntry


class TestSimulationDispatchEntry:
    """Own software evidence for durable dispatch-entry state."""

    @staticmethod
    def entry() -> SimulationDispatchEntry:
        """Construct one synthetic represented entry without persistence."""
        return SUT(
            identity=SimulationDispatchEntryIdentity("entry.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            predecessor_revision_identity=WorkflowRunRevisionIdentity(
                "revision.claimed"
            ),
            committed_revision_identity=WorkflowRunRevisionIdentity("revision.entered"),
            claimed_reservation_identity=AuthorityReservationOutcomeIdentity(
                "claim.one"
            ),
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            obligation_identity=ObligationIdentity("obligation.one"),
            receipt_identity=SimulationDispatchEntryReceiptIdentity("receipt.one"),
            outcome_identity=SimulationDispatchOutcomeIdentity("outcome.one"),
        )

    def test_constructor__entry__requires_distinct_revisions(self) -> None:
        """Reject entry state that does not advance the claimed revision.

        Evidence ID: SV-WFR-DISPATCH-ENTRY-001
        """
        entry = self.entry()
        assert entry.committed_revision_identity.value == "revision.entered"
        with pytest.raises(ValueError):
            replace(
                entry, committed_revision_identity=entry.predecessor_revision_identity
            )
