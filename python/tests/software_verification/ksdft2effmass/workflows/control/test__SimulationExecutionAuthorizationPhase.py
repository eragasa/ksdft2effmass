r"""Software verification of ``SimulationExecutionAuthorizationPhase``.

Evidence profile: routine

Bounded artifact scope: the public simulation authorization-phase discriminator.

Facet and represented meaning

This module verifies separate preparation and immediate claim authorization phases.

Intrinsic and cross-object scope

Enum membership belongs here; grant-state requirements belong to the authorizer.

VVUQ and scientific exclusions

This is software verification only. It establishes no authority, execution,
scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows import SimulationExecutionAuthorizationPhase

pytestmark = pytest.mark.software_verification
SUT = SimulationExecutionAuthorizationPhase


class TestSimulationExecutionAuthorizationPhase:
    """Own software evidence for the authorization-phase discriminator."""

    def test_fields__members__separate_preparation_and_claim(self) -> None:
        """Retain exactly the two required authorization phases.

        Evidence ID: SV-WCI-AUTHORIZATION-PHASE-001

        Requirement: Preparation and claim are distinct closed phases.

        Acceptance: Iteration returns the exact values in declaration order.
        """
        assert tuple(SUT) == (SUT.PREPARATION, SUT.CLAIM)
