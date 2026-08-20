r"""Software verification of ``TaskInstance``.

Evidence profile: routine

Bounded artifact scope: the public ``TaskInstance`` DataObject.

Facet and represented meaning

The class distinguishes a run-scoped Task instance from its reusable definition.

Intrinsic and cross-object scope

Tests cover exact identities and zero-or-one start-gate policy.

VVUQ and scientific exclusions

This is software verification. Instance construction grants no activation, execution,
scientific validity, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows import (
    TaskDefinitionIdentity,
    TaskInstance,
    TaskInstanceIdentity,
    TaskStartGateSet,
    TaskStartGateSetIdentity,
    TaskStartGateSetMode,
)

pytestmark = pytest.mark.software_verification
SUT = TaskInstance


def test_constructor__start_gate_set__accepts_absence_or_one_exact_policy() -> None:
    """Test both valid ``TaskInstance.start_gate_set`` partitions.

    Evidence ID: SV-WFM-TASK-INSTANCE-001

    Requirement: One instance binds one definition and has either no gate set or one
    exact immutable gate set.

    Acceptance: Both constructions retain their exact identity and optional policy.
    """
    identity = TaskInstanceIdentity("instance.one")
    definition = TaskDefinitionIdentity("task.one")
    without_gates = SUT(identity, definition, None)
    gate_set = TaskStartGateSet(
        TaskStartGateSetIdentity("set.one"), TaskStartGateSetMode.ANY_OF, ()
    )
    with_gates = SUT(identity, definition, gate_set)
    assert without_gates.start_gate_set is None
    assert with_gates.start_gate_set is gate_set


def test_constructor__start_gate_set__rejects_nonpolicy_object() -> None:
    """Test the nominal boundary of ``TaskInstance.start_gate_set``.

    Evidence ID: SV-WFM-TASK-INSTANCE-002

    Requirement: A present gate policy is exactly ``TaskStartGateSet``.

    Acceptance: An equal-looking unowned object raises ``TypeError``.
    """
    with pytest.raises(TypeError):
        SUT(
            TaskInstanceIdentity("instance.one"),
            TaskDefinitionIdentity("task.one"),
            object(),  # type: ignore[arg-type]
        )
