r"""Software verification of ``SimulationDispatchEntryResult``.

Evidence profile: routine

Bounded artifact scope: the public dispatch-entry ResultObject.

Facet and represented meaning

This module verifies winner-receipt discrimination at the persistence boundary.

Intrinsic and cross-object scope

CAS execution and effect-entry suppression remain with adapter evidence.

VVUQ and scientific exclusions

This is software verification only. It invokes no persistence implementation or
external scientific effect and establishes no scientific acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.workflows import (
    SimulationDispatchEntryOutcomeKind,
    SimulationDispatchEntryResult,
)

from .resources.scenarios import ControlScenarioFactory

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchEntryResult


class TestSimulationDispatchEntryResult:
    """Own software evidence for dispatch-entry result discrimination."""

    def test_constructor__entered__requires_exact_winner_receipt(self) -> None:
        """Require a receipt only for the newly successful CAS result.

        Evidence ID: SV-WCI-DISPATCH-ENTRY-RESULT-001
        """
        request = ControlScenarioFactory.dispatch_request()
        result = SUT(
            kind=SimulationDispatchEntryOutcomeKind.ENTERED,
            request=request,
            receipt=ControlScenarioFactory.dispatch_entry_receipt(request),
            diagnostics=(),
        )
        with pytest.raises(ValueError):
            replace(result, receipt=None)
        with pytest.raises(ValueError):
            replace(
                result,
                kind=SimulationDispatchEntryOutcomeKind.ALREADY_ENTERED,
            )
