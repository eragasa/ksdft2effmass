r"""Software verification of ``WorkflowRunClaimCommitReceipt``.

Evidence profile: routine

Bounded artifact scope: typed evidence for one externally committed claimed revision.

Facet and represented meaning

The record correlates one exact claimed WorkflowRun revision to supplied persistence
operation and content identities.

Intrinsic and cross-object scope

This module verifies immutable receipt construction only; no repository is invoked.

VVUQ and scientific exclusions

This is software verification only and establishes no persistence implementation,
external effect, scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows import (
    AuthorityReservationOutcomeIdentity,
    SimulationExecutionAuthorizationResultIdentity,
    WorkflowRunClaimCommitReceipt,
    WorkflowRunClaimCommitReceiptIdentity,
    WorkflowRunIdentity,
    WorkflowRunRevisionIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunClaimCommitReceipt


class TestWorkflowRunClaimCommitReceipt:
    """Own construction evidence for typed committed-claim proof."""

    def test_constructor__exact_commit_evidence__retains_revision_closure(self) -> None:
        """Retain exact claimed revision and persistence evidence without an effect.

        Evidence ID: SV-WFR-CLAIM-COMMIT-RECEIPT-001
        """
        receipt = SUT(
            identity=WorkflowRunClaimCommitReceiptIdentity("receipt.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            committed_revision_identity=WorkflowRunRevisionIdentity("revision.two"),
            predecessor_revision_identity=WorkflowRunRevisionIdentity("revision.one"),
            claimed_reservation_identity=AuthorityReservationOutcomeIdentity(
                "reservation.claimed"
            ),
            claim_authorization_result_identity=(
                SimulationExecutionAuthorizationResultIdentity("authorization.claim")
            ),
            workflow_run_content_identity="sha256:content",
            persistence_operation_identity="operation.cas",
            commit_idempotency_identity="idempotency.cas",
            persistence_implementation_identity="repository.v1",
        )
        assert receipt.committed_revision_identity.value == "revision.two"
        assert receipt.predecessor_revision_identity.value == "revision.one"
