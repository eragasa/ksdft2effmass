r"""Software verification of ``SimulationExecutionAuthorizationOutcomeKind``.

Evidence profile: routine

Bounded artifact scope: the public closed authorization-outcome discriminator.

Facet and represented meaning

This module verifies authorized, denied, and error remain distinct outcomes.

Intrinsic and cross-object scope

Enum membership belongs here; outcome production belongs to the authorizer.

VVUQ and scientific exclusions

This is software verification only. It establishes no authority, execution,
scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows import SimulationExecutionAuthorizationOutcomeKind

pytestmark = pytest.mark.software_verification
SUT = SimulationExecutionAuthorizationOutcomeKind


class TestSimulationExecutionAuthorizationOutcomeKind:
    """Own software evidence for closed authorization outcomes."""

    def test_fields__members__form_exact_closed_set(self) -> None:
        """Retain authorization, denial, and inability to decide separately.

        Evidence ID: SV-WCI-AUTHORIZATION-OUTCOME-KIND-001

        Requirement: Authorization has exactly three documented outcomes.

        Acceptance: Iteration returns the exact values in declaration order.
        """
        assert tuple(SUT) == (SUT.AUTHORIZED, SUT.DENIED, SUT.ERROR)
