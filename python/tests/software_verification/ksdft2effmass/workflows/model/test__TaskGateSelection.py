r"""Software verification of ``TaskGateSelection``.

Evidence profile: routine

Bounded artifact scope: the public ``TaskGateSelection`` DataObject.

Facet and represented meaning

The class correlates one selected Workflow gate to one generic transition binding.

Intrinsic and cross-object scope

Tests cover exact nominal field admission; transition agreement is TaskActivation-owned.

VVUQ and scientific exclusions

This is software verification. Construction establishes no enablement, selection,
firing, Task execution, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetBinding,
    ColoredPetriNetTransitionIdentity,
)
from ksdft2effmass.workflows import TaskGateSelection, TaskStartGateIdentity

pytestmark = pytest.mark.software_verification
SUT = TaskGateSelection


def test_constructor__fields__retains_gate_and_generic_binding() -> None:
    """Test the complete valid ``TaskGateSelection`` field mapping.

    Evidence ID: SV-WFM-GATE-SELECTION-001

    Requirement: Selection stores one exact Workflow gate identity and one immutable
    generic binding.

    Acceptance: Both supplied objects are retained by identity.
    """
    gate = TaskStartGateIdentity("gate.one")
    binding = ColoredPetriNetBinding(
        ColoredPetriNetTransitionIdentity("transition.one"), ()
    )
    value = SUT(gate, binding)
    assert value.gate_identity is gate
    assert value.binding is binding


def test_constructor__binding__rejects_nonbinding_object() -> None:
    """Test the generic binding nominal boundary.

    Evidence ID: SV-WFM-GATE-SELECTION-002

    Requirement: ``binding`` is exactly ``ColoredPetriNetBinding``.

    Acceptance: An unowned object raises ``TypeError``.
    """
    with pytest.raises(TypeError):
        SUT(TaskStartGateIdentity("gate.one"), object())  # type: ignore[arg-type]
