r"""Software verification of ``SimulationExecutionAuthorizationResult``.

Evidence profile: routine

Bounded artifact scope: the public closed authorization ResultObject.

Facet and represented meaning

This module verifies exact request binding and closed result discrimination.

Intrinsic and cross-object scope

Result field invariants and deterministic reproduction belong here; the authorizer
ActionObject delegates to that class-owned evaluator.

VVUQ and scientific exclusions

This is software verification only. It creates no authority or effect and establishes
no scientific validation, uncertainty quantification, or human acceptance.
"""

from dataclasses import fields, replace

import pytest

from ksdft2effmass.workflows import (
    SimulationExecutionAuthorizationOutcomeKind,
    SimulationExecutionAuthorizationResult,
)

from .resources.scenarios import ControlScenarioFactory

pytestmark = pytest.mark.software_verification
SUT = SimulationExecutionAuthorizationResult


class TestSimulationExecutionAuthorizationResult:
    """Own software evidence for the closed authorization result."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose exact input, outcome, state, diagnostics, and implementation.

        Evidence ID: SV-WCI-AUTHORIZATION-RESULT-001

        Requirement: The result declares exactly its documented fields.

        Acceptance: ``dataclasses.fields`` returns the exact constructor order.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "request",
            "kind",
            "authorized_grant_state",
            "diagnostics",
            "authorizer_implementation_identity",
        )

    def test_constructor__outcome_variant__prohibits_authorized_diagnostics(
        self,
    ) -> None:
        """Keep authorized and non-authorized payloads disjoint.

        Evidence ID: SV-WCI-AUTHORIZATION-RESULT-002

        Requirement: Authorized results carry usable grant state and no diagnostic.

        Acceptance: Adding a diagnostic to an authorized result raises ``ValueError``.
        """
        result = ControlScenarioFactory.preparation_authorization()
        assert result.kind is SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED
        with pytest.raises(ValueError):
            replace(result, diagnostics=("not permitted",))

    def test_classmethod__evaluate__reproduces_exact_authorization(self) -> None:
        """Reproduce retained evidence from the complete request.

        Evidence ID: SV-WCI-AUTHORIZATION-RESULT-003

        Requirement: Replay and the public authorizer share one deterministic,
        class-owned authorization evaluator.

        Acceptance: Evaluating the synthetic preparation request exactly reproduces
        its retained authorization result.
        """
        retained = ControlScenarioFactory.preparation_authorization()
        assert SUT.evaluate(retained.request) == retained
