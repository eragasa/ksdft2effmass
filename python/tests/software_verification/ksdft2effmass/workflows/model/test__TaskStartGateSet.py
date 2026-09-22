r"""Software verification of ``TaskStartGateSet``.

Evidence profile: routine

Bounded artifact scope: the public ``TaskStartGateSet`` DataObject.

Facet and represented meaning

The class represents one immutable ``any_of`` or ``all_of`` start policy.

Intrinsic and cross-object scope

Tests cover tuple membership, unique identities, empty policy, and deterministic
priority-then-identity selection order.

VVUQ and scientific exclusions

This is software verification. It establishes no generic enablement, selection,
Task execution, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.petrinet.colored import ColoredPetriNetTransitionIdentity
from ksdft2effmass.workflows import (
    TaskStartGate,
    TaskStartGateIdentity,
    TaskStartGateSet,
    TaskStartGateSetIdentity,
    TaskStartGateSetMode,
)

pytestmark = pytest.mark.software_verification
SUT = TaskStartGateSet


def test_constructor__empty_membership__accepts_both_inactive_modes() -> None:
    """Test the explicitly accepted empty gate-set partition.

    Evidence ID: SV-WFM-GATE-SET-001

    Requirement: Empty ``any_of`` and ``all_of`` sets are valid immutable policies
    that provide no member gate for automatic activation.

    Acceptance: Both modes construct with an exact empty tuple.
    """
    any_of = SUT(TaskStartGateSetIdentity("set.any"), TaskStartGateSetMode.ANY_OF, ())
    all_of = SUT(TaskStartGateSetIdentity("set.all"), TaskStartGateSetMode.ALL_OF, ())
    assert any_of.gates == ()
    assert all_of.gates == ()


def test_constructor__gates__requires_tuple_with_unique_gate_identities() -> None:
    """Test the collection boundary of ``TaskStartGateSet.gates``.

    Evidence ID: SV-WFM-GATE-SET-002

    Requirement: Members are supplied as a tuple of ``TaskStartGate`` values and
    each member identity occurs exactly once.

    Acceptance: A list raises ``TypeError`` and duplicate identities raise
    ``ValueError``.
    """
    gate = TaskStartGate(
        TaskStartGateIdentity("gate.one"),
        0,
        ColoredPetriNetTransitionIdentity("transition.one"),
    )
    with pytest.raises(TypeError):
        SUT(
            TaskStartGateSetIdentity("set.one"),
            TaskStartGateSetMode.ANY_OF,
            [gate],  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError):
        SUT(
            TaskStartGateSetIdentity("set.one"),
            TaskStartGateSetMode.ANY_OF,
            (gate, gate),
        )


def test_property__selection_order__sorts_by_priority_then_gate_identity() -> None:
    """Test the documented deterministic gate-selection order.

    Evidence ID: SV-WFM-GATE-SET-003

    Requirement: Caller storage order does not determine selection order; lower
    priority precedes higher priority and identity breaks equal-priority ties.

    Acceptance: The property returns ``a``, ``b``, then ``z`` while ``gates`` retains
    the deliberately different caller order.
    """
    later = TaskStartGate(
        TaskStartGateIdentity("z"),
        2,
        ColoredPetriNetTransitionIdentity("transition.z"),
    )
    lexical_second = TaskStartGate(
        TaskStartGateIdentity("b"),
        1,
        ColoredPetriNetTransitionIdentity("transition.b"),
    )
    lexical_first = TaskStartGate(
        TaskStartGateIdentity("a"),
        1,
        ColoredPetriNetTransitionIdentity("transition.a"),
    )
    value = SUT(
        TaskStartGateSetIdentity("set.one"),
        TaskStartGateSetMode.ANY_OF,
        (later, lexical_second, lexical_first),
    )
    assert value.gates == (later, lexical_second, lexical_first)
    assert value.selection_order == (lexical_first, lexical_second, later)
