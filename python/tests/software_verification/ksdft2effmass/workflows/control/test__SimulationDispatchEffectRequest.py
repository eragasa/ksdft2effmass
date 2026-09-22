r"""Software verification of ``SimulationDispatchEffectRequest``.

Evidence profile: routine

Bounded artifact scope: the public request supplied to a simulation dispatch effect.

Facet and represented meaning

This module verifies that the effect receives an authorized claim-phase result and
claimed reservation.

Intrinsic and cross-object scope

Effect-request variant invariants belong here; complete operation correlation belongs
to the adapter.

VVUQ and scientific exclusions

This is software verification only. It performs no effect and establishes no real
authority, scientific validation, UQ, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows import (
    SimulationDispatchEffectRequest,
    SimulationExecutionAuthorizer,
)

from .resources.scenarios import ControlScenarioFactory

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchEffectRequest


class TestSimulationDispatchEffectRequest:
    """Own software evidence for the dispatch-effect request."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose only the exact prepared, authorized, and claimed inputs.

        Evidence ID: SV-WCI-DISPATCH-EFFECT-REQUEST-001

        Requirement: The effect request declares exactly its documented fields.

        Acceptance: ``dataclasses.fields`` returns the exact constructor order.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "execution_request",
            "claim_authorization",
            "claimed_reservation",
            "claim_commit_receipt",
            "dispatch_entry_receipt",
            "outcome_identity",
        )

    def test_constructor__authorization__accepts_exact_reserved_claim(self) -> None:
        """Construct only from the immediately authorized claim phase.

        Evidence ID: SV-WCI-DISPATCH-EFFECT-REQUEST-002

        Requirement: The effect request carries an authorized reserved-grant result.

        Acceptance: The exact synthetic claim authorization constructs unchanged.
        """
        dispatch = ControlScenarioFactory.dispatch_request()
        authorization = SimulationExecutionAuthorizer.execute(
            dispatch.claim_authorization_request
        )
        request = SUT(
            execution_request=dispatch.execution_request,
            claim_authorization=authorization,
            claimed_reservation=dispatch.claimed_reservation,
            claim_commit_receipt=dispatch.claim_commit_receipt,
            dispatch_entry_receipt=(
                ControlScenarioFactory.dispatch_entry_receipt(dispatch)
            ),
            outcome_identity=dispatch.outcome_identity,
        )
        assert request.claim_authorization is authorization
