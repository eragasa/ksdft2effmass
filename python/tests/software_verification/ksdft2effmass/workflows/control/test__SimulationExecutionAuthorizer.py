r"""Software verification of ``SimulationExecutionAuthorizer``.

Evidence profile: routine

Bounded artifact scope: the public effect-free simulation authorizer ActionObject.

Facet and represented meaning

This module verifies exact phase/state matching and fail-closed authority outcomes.

Intrinsic and cross-object scope

Cross-object authorization policy belongs to this ActionObject. Cryptographic
verification, persistence, claims, and external execution remain excluded.

VVUQ and scientific exclusions

This is software verification only. It establishes represented authorization under
synthetic inputs, not real execution authority, scientific validity, UQ, or acceptance.
"""

import pytest

from ksdft2effmass.workflows import (
    ScientificExecutionAuthorityVerificationKind,
    ScientificExecutionGrantState,
    SimulationExecutionAuthorizationOutcomeKind,
    SimulationExecutionAuthorizationPhase,
    SimulationExecutionAuthorizer,
)

from .resources.scenarios import ControlScenarioFactory

pytestmark = pytest.mark.software_verification
SUT = SimulationExecutionAuthorizer


class TestSimulationExecutionAuthorizer:
    """Own software evidence for deterministic simulation authorization."""

    def test_methods__execute__authorizes_exact_phase_states(self) -> None:
        """Authorize unused preparation and same-obligation reserved claim.

        Evidence ID: SV-WCI-AUTHORIZER-001

        Requirement: Preparation requires unused and claim requires exactly reserved
        authority for the supplied obligation.

        Acceptance: Both exact requests return authorized with their required states.
        """
        preparation = SUT.execute(
            ControlScenarioFactory.authorization_request(
                phase=SimulationExecutionAuthorizationPhase.PREPARATION,
                state=ScientificExecutionGrantState.UNUSED,
                result_identity="authorization.prepare",
            )
        )
        claim = SUT.execute(ControlScenarioFactory.claim_authorization_request())
        assert (
            preparation.kind is SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED
        )
        assert (
            preparation.authorized_grant_state is ScientificExecutionGrantState.UNUSED
        )
        assert claim.kind is SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED
        assert claim.authorized_grant_state is ScientificExecutionGrantState.RESERVED

    def test_methods__execute__separates_denial_from_indeterminate_error(self) -> None:
        """Distinguish mismatched state from unresolved verification.

        Evidence ID: SV-WCI-AUTHORIZER-002

        Requirement: Established phase mismatch is denied, while indeterminate
        authority verification is an error; neither is authorized.

        Acceptance: Claimed preparation returns denied and indeterminate verification
        returns error with no authorized state.
        """
        denied = SUT.execute(
            ControlScenarioFactory.authorization_request(
                phase=SimulationExecutionAuthorizationPhase.PREPARATION,
                state=ScientificExecutionGrantState.CLAIMED,
                result_identity="authorization.denied",
            )
        )
        snapshot = ControlScenarioFactory.snapshot(
            verification=ScientificExecutionAuthorityVerificationKind.INDETERMINATE
        )
        error = SUT.execute(
            ControlScenarioFactory.authorization_request(
                phase=SimulationExecutionAuthorizationPhase.PREPARATION,
                state=ScientificExecutionGrantState.UNUSED,
                result_identity="authorization.error",
                snapshot=snapshot,
            )
        )
        assert denied.kind is SimulationExecutionAuthorizationOutcomeKind.DENIED
        assert denied.authorized_grant_state is None
        assert error.kind is SimulationExecutionAuthorizationOutcomeKind.ERROR
        assert error.authorized_grant_state is None
