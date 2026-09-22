r"""Software verification of ``ScientificExecutionGrantState``.

Evidence profile: routine

Bounded artifact scope: the public execution-grant state discriminator.

Facet and represented meaning

This module verifies the closed represented grant lifecycle states.

Intrinsic and cross-object scope

Enum membership belongs here; authorization comparisons belong to the authorizer.

VVUQ and scientific exclusions

This is software verification only. It establishes no authority, execution,
scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows import ScientificExecutionGrantState

pytestmark = pytest.mark.software_verification
SUT = ScientificExecutionGrantState


class TestScientificExecutionGrantState:
    """Own software evidence for the execution-grant discriminator."""

    def test_fields__members__form_exact_closed_set(self) -> None:
        """Retain unused, reserved, claimed, and revoked as distinct states.

        Evidence ID: SV-WCI-GRANT-STATE-001

        Requirement: Grant state has exactly the four documented alternatives.

        Acceptance: Iteration returns the exact values in declaration order.
        """
        assert tuple(SUT) == (
            SUT.UNUSED,
            SUT.RESERVED,
            SUT.CLAIMED,
            SUT.REVOKED,
        )
