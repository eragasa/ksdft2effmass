r"""Software verification of ``SimulationDispatchClaimPreparer``.

Evidence profile: routine

Bounded artifact scope: the public effect-free claim-candidate ActionObject.

Facet and represented meaning

The preparer appends a distinct claim-phase authorization result and claimed record to
one exact replay-equal prepared WorkflowRun candidate.

Intrinsic and cross-object scope

The test composes the already verified public preparation action, exact runtime bundle,
authorizer, and replayer. No repository implementation or effect is used.

VVUQ and scientific exclusions

This is software verification only. It establishes no persistence, external execution,
scientific validation, uncertainty quantification, authority issuance, or acceptance.
"""

import pytest

from ksdft2effmass.workflows import (
    AuthorityReservationOutcomeIdentity,
    ScientificExecutionGrantState,
    SimulationDispatchClaimOutcomeKind,
    SimulationDispatchClaimPreparer,
    SimulationDispatchClaimRequest,
    SimulationDispatchPreparer,
    SimulationExecutionAuthorizationPhase,
    SimulationExecutionAuthorizer,
    SimulationExecutionRequest,
    WorkflowRunReplayer,
    WorkflowRunRevisionIdentity,
)

from .resources.scenarios import ControlScenarioFactory
from .test__SimulationDispatchPreparer import (
    TestSimulationDispatchPreparer as _PreparationEvidenceFactory,
)

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchClaimPreparer


class TestSimulationDispatchClaimPreparer:
    """Own software evidence for effect-free claim preparation."""

    def test_execute__prepared_candidate__returns_replay_equal_claim(self) -> None:
        """Append distinct claim evidence without persistence or an effect.

        Evidence ID: SV-WFC-DISPATCH-CLAIM-PREPARER-001

        Requirement: One exact prepared predecessor and reserved grant view produce a
        new revision containing a distinct claim authorization and append-only claim.

        Acceptance: The result is ``claimed`` and its candidate replays equally with
        two authorization results and reserved-then-claimed records.
        """
        preparation = SimulationDispatchPreparer(
            SimulationExecutionAuthorizer(), WorkflowRunReplayer()
        ).execute(_PreparationEvidenceFactory.make_request())
        assert preparation.candidate_run is not None
        run = preparation.candidate_run
        execution = SimulationExecutionRequest(
            correlation=run.execution_request_correlations[0],
            obligation=run.dispatch_obligations[0],
            preparation_authorization=run.authorization_results[0],
        )
        request = SimulationDispatchClaimRequest(
            predecessor_run=run,
            runtime_bundle=preparation.request.runtime_bundle,
            execution_request=execution,
            claim_authorization_request=(
                ControlScenarioFactory.authorization_request(
                    phase=SimulationExecutionAuthorizationPhase.CLAIM,
                    state=ScientificExecutionGrantState.RESERVED,
                    result_identity="authorization.claim.one",
                    input_result_reference_identities=(),
                )
            ),
            next_revision_identity=WorkflowRunRevisionIdentity("revision.claimed"),
            claimed_reservation_identity=AuthorityReservationOutcomeIdentity(
                "claim.one"
            ),
        )

        result = SUT(SimulationExecutionAuthorizer(), WorkflowRunReplayer()).execute(
            request
        )

        assert result.kind is SimulationDispatchClaimOutcomeKind.CLAIMED
        assert result.candidate_run is not None
        assert len(result.candidate_run.authorization_results) == 2
        assert tuple(
            value.kind.value for value in result.candidate_run.authority_reservations
        ) == ("claimed", "reserved")
        assert result.candidate_replay_result is not None
        assert result.candidate_replay_result.outcome.value == "equal"
