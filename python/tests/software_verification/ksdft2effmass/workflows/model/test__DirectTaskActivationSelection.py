r"""Software verification of ``DirectTaskActivationSelection``.

Evidence profile: routine

Bounded artifact scope: the public ``DirectTaskActivationSelection`` DataObject.

Facet and represented meaning

The class represents direct activation without gate-set or selected-gate identity.

Intrinsic and cross-object scope

Tests cover its sole exact generic selection-result identity field.

VVUQ and scientific exclusions

This is software verification. Construction establishes no selection permission,
Task execution, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.petrinet.colored import ColoredPetriNetSelectionResultIdentity
from ksdft2effmass.workflows import DirectTaskActivationSelection

pytestmark = pytest.mark.software_verification
SUT = DirectTaskActivationSelection


def test_constructor__selection_result_identity__requires_exact_generic_identity() -> (
    None
):
    """Test the sole direct-selection field and nominal rejection boundary.

    Evidence ID: SV-WFM-DIRECT-SELECTION-001

    Requirement: Direct selection carries exactly one
    ``ColoredPetriNetSelectionResultIdentity`` and no gate identity.

    Acceptance: The exact identity is retained and a plain string raises ``TypeError``.
    """
    identity = ColoredPetriNetSelectionResultIdentity("a" * 64)
    value = SUT(identity)
    assert value.selection_result_identity is identity
    assert set(value.__slots__) == {"selection_result_identity"}
    with pytest.raises(TypeError):
        SUT("a" * 64)  # type: ignore[arg-type]
