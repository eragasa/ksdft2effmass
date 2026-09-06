r"""Software verification of ``SimulationDispatchResultIngressOutcomeKind``.

Evidence profile: routine

Bounded artifact scope: the public dispatch result-ingress outcome enum.

Facet and represented meaning

The enum closes terminal ingress preparation to admitted or error.

Intrinsic and cross-object scope

This module verifies only the exact public vocabulary.

VVUQ and scientific exclusions

This is software verification only and establishes no persistence, external effect,
scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows import SimulationDispatchResultIngressOutcomeKind

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchResultIngressOutcomeKind


class TestSimulationDispatchResultIngressOutcomeKind:
    """Own closed-enum evidence for result ingress."""

    def test_members__contract__is_closed(self) -> None:
        """Expose only admitted and fail-closed error variants.

        Evidence ID: SV-WCI-RESULT-INGRESS-OUTCOME-KIND-001
        """
        assert tuple(SUT) == (SUT.ADMITTED, SUT.ERROR)
        assert tuple(value.value for value in SUT) == ("admitted", "error")
