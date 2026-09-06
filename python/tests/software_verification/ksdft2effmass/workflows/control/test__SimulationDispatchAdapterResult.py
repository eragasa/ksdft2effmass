r"""Software verification of ``SimulationDispatchAdapterResult``.

Evidence profile: routine

Bounded artifact scope: the public dispatch-adapter ResultObject.

Facet and represented meaning

This module verifies exact authorization, outcome, effect-entry, and diagnostic
variant state.

Intrinsic and cross-object scope

Result discrimination belongs here; production of each variant belongs to the
adapter.

VVUQ and scientific exclusions

This is software verification only. It establishes no real execution, scientific
validation, uncertainty quantification, or human acceptance.
"""

from dataclasses import fields, replace

import pytest

from ksdft2effmass.workflows import (
    SimulationDispatchAdapterResult,
    SimulationDispatchAdapterResultKind,
    SimulationDispatchEntryOutcomeKind,
    SimulationDispatchEntryResult,
    SimulationExecutionAuthorizer,
)

from .resources.scenarios import ControlScenarioFactory

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchAdapterResult


class TestSimulationDispatchAdapterResult:
    """Own software evidence for the closed adapter result."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose exact authorization, outcome, invocation flag, and diagnostics.

        Evidence ID: SV-WCI-DISPATCH-ADAPTER-RESULT-001

        Requirement: The result declares exactly its documented fields.

        Acceptance: ``dataclasses.fields`` returns the exact constructor order.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "kind",
            "request",
            "authorization_result",
            "entry_result",
            "outcome",
            "effect_invoked",
            "diagnostics",
        )

    def test_constructor__dispatched__requires_outcome_and_effect_entry(self) -> None:
        """Prohibit a dispatched claim without an actual runtime outcome.

        Evidence ID: SV-WCI-DISPATCH-ADAPTER-RESULT-002

        Requirement: Dispatched means the effect was entered and returned an outcome.

        Acceptance: The exact variant constructs and removing its outcome raises
        ``ValueError``.
        """
        dispatch = ControlScenarioFactory.dispatch_request()
        entry = SimulationDispatchEntryResult(
            kind=SimulationDispatchEntryOutcomeKind.ENTERED,
            request=dispatch,
            receipt=ControlScenarioFactory.dispatch_entry_receipt(dispatch),
            diagnostics=(),
        )
        result = SUT(
            kind=SimulationDispatchAdapterResultKind.DISPATCHED,
            request=dispatch,
            authorization_result=SimulationExecutionAuthorizer.execute(
                dispatch.claim_authorization_request
            ),
            entry_result=entry,
            outcome=ControlScenarioFactory.outcome(),
            effect_invoked=True,
            diagnostics=(),
        )
        with pytest.raises(ValueError):
            replace(result, outcome=None)
