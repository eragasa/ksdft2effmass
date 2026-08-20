r"""Software verification of ``TaskStartGate``.

Evidence profile: routine

Bounded artifact scope: the public ``TaskStartGate`` DataObject.

Facet and represented meaning

The class binds one Workflow gate identity and priority to one generic transition.

Intrinsic and cross-object scope

Tests cover exact nominal fields, nonnegative integer priority, and immutability.

VVUQ and scientific exclusions

This is software verification. It establishes no enablement, selection, firing,
Task execution, scientific validity, or human acceptance.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.petrinet.colored import ColoredPetriNetTransitionIdentity
from ksdft2effmass.workflows import TaskStartGate, TaskStartGateIdentity

pytestmark = pytest.mark.software_verification
SUT = TaskStartGate


def test_constructor__fields__retains_exact_gate_state() -> None:
    """Test the complete valid ``TaskStartGate`` field mapping.

    Evidence ID: SV-WFM-GATE-001

    Requirement: A gate stores its nominal identity, nonnegative priority, and exact
    generic transition identity.

    Acceptance: Construction retains all three supplied objects exactly.
    """
    identity = TaskStartGateIdentity("gate.one")
    transition = ColoredPetriNetTransitionIdentity("transition.one")
    value = SUT(identity, 2, transition)
    assert value.identity is identity
    assert value.priority == 2
    assert value.transition_identity is transition


def test_constructor__priority__rejects_boolean_negative_and_noninteger_values() -> (
    None
):
    """Test the public numeric boundary of ``TaskStartGate.priority``.

    Evidence ID: SV-WFM-GATE-002

    Requirement: Priority is an exact nonnegative built-in integer; Boolean values
    do not satisfy the contract.

    Acceptance: Boolean and float values raise ``TypeError`` and a negative integer
    raises ``ValueError``.
    """
    identity = TaskStartGateIdentity("gate.one")
    transition = ColoredPetriNetTransitionIdentity("transition.one")
    with pytest.raises(TypeError):
        SUT(identity, True, transition)
    with pytest.raises(TypeError):
        SUT(identity, 1.0, transition)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT(identity, -1, transition)


def test_method__setattr__rejects_gate_mutation() -> None:
    """Test that a constructed ``TaskStartGate`` cannot be mutated.

    Evidence ID: SV-WFM-GATE-003

    Requirement: Gate definition state is operationally immutable.

    Acceptance: Assigning ``priority`` raises ``FrozenInstanceError``.
    """
    value = SUT(
        TaskStartGateIdentity("gate.one"),
        0,
        ColoredPetriNetTransitionIdentity("transition.one"),
    )
    with pytest.raises(FrozenInstanceError):
        value.priority = 1  # type: ignore[misc]
