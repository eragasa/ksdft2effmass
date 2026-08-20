r"""Software verification of ``AllOfTaskActivationSelection``.

Evidence profile: routine

Bounded artifact scope: the public ``AllOfTaskActivationSelection`` DataObject.

Facet and represented meaning

The class represents the complete selected member tuple of an ``all_of`` gate set.

Intrinsic and cross-object scope

Tests cover tuple-only selections, unique selected gate identities, and exact
correlation fields. Completeness and canonical order are TaskActivation-owned.

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
    AllOfTaskActivationSelection,
    TaskGateSelection,
    TaskStartGateIdentity,
    TaskStartGateSetIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = AllOfTaskActivationSelection


def test_constructor__selected_gates__retains_unique_tuple_membership() -> None:
    """Test the complete valid ``AllOfTaskActivationSelection`` field mapping.

    Evidence ID: SV-WFM-ALL-SELECTION-001

    Requirement: ``all_of`` selection stores an exact gate set, tuple of uniquely
    identified selected gates, and generic selection-result identity.

    Acceptance: Construction retains all exact supplied objects.
    """
    selected = TaskGateSelection(
        TaskStartGateIdentity("gate.one"),
        ColoredPetriNetBinding(ColoredPetriNetTransitionIdentity("transition.one"), ()),
    )
    result = ColoredPetriNetSelectionResultIdentity("a" * 64)
    value = SUT(TaskStartGateSetIdentity("set.one"), (selected,), result)
    assert value.selected_gates == (selected,)
    assert value.selection_result_identity is result


def test_constructor__selected_gates__rejects_mutable_or_duplicate_membership() -> None:
    """Test the collection and identity boundaries of ``selected_gates``.

    Evidence ID: SV-WFM-ALL-SELECTION-002

    Requirement: Selected gates are supplied as a tuple and each gate identity occurs
    exactly once.

    Acceptance: A list raises ``TypeError`` and a repeated gate raises ``ValueError``.
    """
    selected = TaskGateSelection(
        TaskStartGateIdentity("gate.one"),
        ColoredPetriNetBinding(ColoredPetriNetTransitionIdentity("transition.one"), ()),
    )
    result = ColoredPetriNetSelectionResultIdentity("a" * 64)
    with pytest.raises(TypeError):
        SUT(
            TaskStartGateSetIdentity("set.one"),
            [selected],  # type: ignore[arg-type]
            result,
        )
    with pytest.raises(ValueError):
        SUT(TaskStartGateSetIdentity("set.one"), (selected, selected), result)
