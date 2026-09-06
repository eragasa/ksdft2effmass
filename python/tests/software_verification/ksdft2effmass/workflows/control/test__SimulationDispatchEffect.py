r"""Software verification of ``SimulationDispatchEffect``.

Evidence profile: routine

Bounded artifact scope: the public architecture-facing simulation effect Protocol.

Facet and represented meaning

This module verifies structural conformance of an application-supplied effect port.

Intrinsic and cross-object scope

Protocol shape belongs here; calculator adaptation and real execution belong to each
application and calculator owner.

VVUQ and scientific exclusions

This is software verification only. It invokes no calculator and establishes no real
authority, scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows import (
    SimulationDispatchEffect,
    SimulationDispatchOutcome,
)

from .resources.scenarios import (
    ControlScenarioFactory,
    RecordingSimulationDispatchEffect,
)

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchEffect


class TestSimulationDispatchEffect:
    """Own software evidence for the typed effect-port protocol."""

    def test_protocols__runtime__accepts_exact_application_effect(self) -> None:
        """Recognize an executor-identified effect with the exact execute method.

        Evidence ID: SV-WCI-DISPATCH-EFFECT-001

        Requirement: Application effects expose executor identity and one typed
        dispatch operation through the runtime-checkable Protocol.

        Acceptance: The recording synthetic effect conforms and returns its configured
        immutable outcome when invoked directly with an exact effect request.
        """
        dispatch = ControlScenarioFactory.dispatch_request()
        outcome = ControlScenarioFactory.outcome()
        effect = RecordingSimulationDispatchEffect(
            executor_identity=outcome.executor_identity,
            outcome=outcome,
        )
        assert isinstance(effect, SUT)
        from ksdft2effmass.workflows import (
            SimulationDispatchEffectRequest,
            SimulationExecutionAuthorizer,
        )

        effect_request = SimulationDispatchEffectRequest(
            execution_request=dispatch.execution_request,
            claim_authorization=SimulationExecutionAuthorizer.execute(
                dispatch.claim_authorization_request
            ),
            claimed_reservation=dispatch.claimed_reservation,
            claim_commit_receipt=dispatch.claim_commit_receipt,
            dispatch_entry_receipt=(
                ControlScenarioFactory.dispatch_entry_receipt(dispatch)
            ),
            outcome_identity=dispatch.outcome_identity,
        )
        assert isinstance(effect.execute(effect_request), SimulationDispatchOutcome)
