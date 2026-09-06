r"""Software verification of ``SimulationDispatchClaimOutcomeKind``.

Evidence profile: routine

Bounded artifact scope: the public dispatch-claim outcome enum.

Facet and represented meaning

The enum closes claim preparation to claimed, denied, or error.

Intrinsic and cross-object scope

This module verifies only the exact public vocabulary.

VVUQ and scientific exclusions

This is software verification only and establishes no persistence, effect, scientific
validation, uncertainty quantification, authority issuance, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows import SimulationDispatchClaimOutcomeKind

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchClaimOutcomeKind


class TestSimulationDispatchClaimOutcomeKind:
    """Own software evidence for the claim outcome vocabulary."""

    def test_members__public_contract__is_closed(self) -> None:
        """Keep the exact closed outcome values.

        Evidence ID: SV-WFC-DISPATCH-CLAIM-OUTCOME-KIND-001
        """
        assert tuple(value.value for value in SUT) == (
            "claimed",
            "denied",
            "error",
        )
