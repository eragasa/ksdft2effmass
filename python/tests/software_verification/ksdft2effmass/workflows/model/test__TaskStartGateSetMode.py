r"""Software verification of ``TaskStartGateSetMode``.

Evidence profile: routine

Bounded artifact scope: the public ``TaskStartGateSetMode`` enum.

Facet and represented meaning

The enum discriminates the two accepted start-gate composition policies.

Intrinsic and cross-object scope

Tests cover exact closed string-valued membership only.

VVUQ and scientific exclusions

This is software verification. It establishes no gate enablement, Task execution,
scientific validity, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows import TaskStartGateSetMode

pytestmark = pytest.mark.software_verification
SUT = TaskStartGateSetMode


def test_property__members__contains_exact_composition_modes() -> None:
    """Test the complete public ``TaskStartGateSetMode`` vocabulary.

    Evidence ID: SV-WFM-GATE-MODE-001

    Requirement: Gate-set composition is closed to ``any_of`` and ``all_of``.

    Acceptance: Iteration returns exactly those members and string values in order.
    """
    assert tuple(SUT) == (SUT.ANY_OF, SUT.ALL_OF)
    assert tuple(member.value for member in SUT) == ("any_of", "all_of")
