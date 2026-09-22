r"""Software verification of ``SimulationDispatchAdapterResultKind``.

Evidence profile: routine

Bounded artifact scope: the public dispatch-adapter result discriminator.

Facet and represented meaning

This module verifies distinct dispatched, denied, error, and indeterminate states.

Intrinsic and cross-object scope

Enum membership belongs here; orchestration behavior belongs to the adapter.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, scientific
validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows import SimulationDispatchAdapterResultKind

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchAdapterResultKind


class TestSimulationDispatchAdapterResultKind:
    """Own software evidence for adapter result discrimination."""

    def test_fields__members__form_exact_closed_set(self) -> None:
        """Retain pre- and post-effect outcomes separately.

        Evidence ID: SV-WCI-DISPATCH-ADAPTER-RESULT-KIND-001

        Requirement: Adapter results distinguish dispatch, denial, pre-effect error,
        and post-invocation indeterminacy.

        Acceptance: Iteration returns the exact values in declaration order.
        """
        assert tuple(SUT) == (
            SUT.DISPATCHED,
            SUT.DENIED,
            SUT.ALREADY_ENTERED,
            SUT.ERROR,
            SUT.INDETERMINATE,
        )
