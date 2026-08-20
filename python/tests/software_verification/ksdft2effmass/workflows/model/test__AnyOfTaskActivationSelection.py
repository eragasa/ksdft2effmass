r"""Software verification of ``AnyOfTaskActivationSelection``.

Evidence profile: routine

Bounded artifact scope: the public ``AnyOfTaskActivationSelection`` DataObject.

Facet and represented meaning

The class represents one selected member of an ``any_of`` gate set.

Intrinsic and cross-object scope

Tests cover its exact gate-set, selected-gate, and generic selection-result fields.
Membership and transition agreement are TaskActivation-owned.

VVUQ and scientific exclusions

This is software verification. Construction establishes no generic enablement,
selection permission, Task execution, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetBinding,
    ColoredPetriNetSelectionResultIdentity,
    ColoredPetriNetTransitionIdentity,
)
from ksdft2effmass.workflows import (
    AnyOfTaskActivationSelection,
    TaskGateSelection,
    TaskStartGateIdentity,
    TaskStartGateSetIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = AnyOfTaskActivationSelection


def test_constructor__fields__retains_one_gate_selection_and_correlations() -> None:
    """Test the complete valid ``AnyOfTaskActivationSelection`` field mapping.

    Evidence ID: SV-WFM-ANY-SELECTION-001

    Requirement: ``any_of`` selection stores one exact gate-set identity, one gate
    selection, and one generic selection-result identity.

    Acceptance: Construction retains all three exact supplied objects.
    """
    gate_set = TaskStartGateSetIdentity("set.one")
    selected_gate = TaskGateSelection(
        TaskStartGateIdentity("gate.one"),
        ColoredPetriNetBinding(ColoredPetriNetTransitionIdentity("transition.one"), ()),
    )
    result = ColoredPetriNetSelectionResultIdentity("a" * 64)
    value = SUT(gate_set, selected_gate, result)
    assert value.gate_set_identity is gate_set
    assert value.selected_gate is selected_gate
    assert value.selection_result_identity is result


def test_constructor__selected_gate__rejects_nonselection_object() -> None:
    """Test the selected-gate nominal boundary.

    Evidence ID: SV-WFM-ANY-SELECTION-002

    Requirement: ``selected_gate`` is exactly ``TaskGateSelection``.

    Acceptance: An unowned object raises ``TypeError``.
    """
    with pytest.raises(TypeError):
        SUT(
            TaskStartGateSetIdentity("set.one"),
            object(),  # type: ignore[arg-type]
            ColoredPetriNetSelectionResultIdentity("a" * 64),
        )
