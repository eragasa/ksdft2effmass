r"""Software verification of ``SimulationDispatchReconciliationOutcomeKind``.

Evidence profile: routine

Bounded artifact scope: the public dispatch-reconciliation outcome discriminator.

Facet and represented meaning

This module verifies established dispatch variants remain separate from conflict and
reconciliation error.

Intrinsic and cross-object scope

Enum membership belongs here; observation comparison belongs to the reconciler.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, scientific
validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows import SimulationDispatchReconciliationOutcomeKind

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchReconciliationOutcomeKind


class TestSimulationDispatchReconciliationOutcomeKind:
    """Own software evidence for reconciliation outcome discrimination."""

    def test_fields__members__form_exact_closed_set(self) -> None:
        """Retain confirmed, rejected, indeterminate, conflict, and error.

        Evidence ID: SV-WCI-RECONCILIATION-OUTCOME-KIND-001

        Requirement: Reconciliation has exactly the five documented outcomes.

        Acceptance: Iteration returns the exact values in declaration order.
        """
        assert tuple(SUT) == (
            SUT.CONFIRMED,
            SUT.REJECTED,
            SUT.INDETERMINATE,
            SUT.CONFLICT,
            SUT.ERROR,
        )
