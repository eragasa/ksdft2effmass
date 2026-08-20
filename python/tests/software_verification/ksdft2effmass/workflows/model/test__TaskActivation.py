r"""Software verification of ``TaskActivation``.

Evidence profile: routine

Bounded artifact scope: the public ``TaskActivation`` DataObject.

Facet and represented meaning

The class closes one direct, ``any_of``, or ``all_of`` activation around exact
Workflow, run, Task-instance, input, operation, attempt, and generic selection state.

Intrinsic and cross-object scope

Tests cover input uniqueness and every discriminated selection correlation against
the Task instance's start-gate policy.

VVUQ and scientific exclusions

This is software verification. Activation construction does not prove generic
enablement, authorize or invoke a Task, validate science, quantify uncertainty, or
provide human acceptance.
"""

from dataclasses import dataclass

import pytest

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetBinding,
    ColoredPetriNetSelectionResultIdentity,
    ColoredPetriNetTransitionIdentity,
)
from ksdft2effmass.workflows import (
    AllOfTaskActivationSelection,
    AnyOfTaskActivationSelection,
    AttemptIdentity,
    DirectTaskActivationSelection,
    OperationIdentity,
    ResultObjectIdentity,
    TaskActivation,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskGateSelection,
    TaskInputBinding,
    TaskInstance,
    TaskInstanceIdentity,
    TaskStartGate,
    TaskStartGateIdentity,
    TaskStartGateSet,
    TaskStartGateSetIdentity,
    TaskStartGateSetMode,
    WorkflowIdentity,
    WorkflowRunIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = TaskActivation


def test_constructor__direct_selection__requires_no_nonempty_gate_set() -> None:
    """Test both valid and invalid direct-activation gate-policy partitions.

    Evidence ID: SV-WFM-ACTIVATION-001

    Requirement: Direct activation is valid for no gate set or an empty gate set and
    invalid when the Task instance has an automatic-start member.

    Acceptance: The ungated activation constructs and the nonempty-gated activation
    raises ``ValueError``.
    """
    selection = DirectTaskActivationSelection(
        ColoredPetriNetSelectionResultIdentity("a" * 64)
    )
    ungated = TaskInstance(
        TaskInstanceIdentity("instance.one"), TaskDefinitionIdentity("task.one"), None
    )
    value = SUT(
        TaskActivationIdentity("activation.one"),
        WorkflowIdentity("workflow.one"),
        WorkflowRunIdentity("run.one"),
        ungated,
        OperationIdentity("operation.one"),
        AttemptIdentity("attempt.one"),
        (),
        selection,
    )
    assert value.selection is selection

    gate = TaskStartGate(
        TaskStartGateIdentity("gate.one"),
        0,
        ColoredPetriNetTransitionIdentity("transition.one"),
    )
    gated = TaskInstance(
        TaskInstanceIdentity("instance.one"),
        TaskDefinitionIdentity("task.one"),
        TaskStartGateSet(
            TaskStartGateSetIdentity("set.one"),
            TaskStartGateSetMode.ANY_OF,
            (gate,),
        ),
    )
    with pytest.raises(ValueError):
        SUT(
            TaskActivationIdentity("activation.one"),
            WorkflowIdentity("workflow.one"),
            WorkflowRunIdentity("run.one"),
            gated,
            OperationIdentity("operation.one"),
            AttemptIdentity("attempt.one"),
            (),
            selection,
        )


def test_constructor__any_of_selection__requires_exact_member_and_transition() -> None:
    """Test all ``any_of`` membership and transition correlations.

    Evidence ID: SV-WFM-ACTIVATION-002

    Requirement: ``any_of`` activation names the instance's exact gate set and one
    member whose generic binding uses that member's transition.

    Acceptance: The correlated selection constructs; a nonmember selection and a
    member bound to another transition each raise ``ValueError``.
    """
    gate = TaskStartGate(
        TaskStartGateIdentity("gate.one"),
        0,
        ColoredPetriNetTransitionIdentity("transition.one"),
    )
    gate_set = TaskStartGateSet(
        TaskStartGateSetIdentity("set.one"),
        TaskStartGateSetMode.ANY_OF,
        (gate,),
    )
    task_instance = TaskInstance(
        TaskInstanceIdentity("instance.one"),
        TaskDefinitionIdentity("task.one"),
        gate_set,
    )
    selection_result = ColoredPetriNetSelectionResultIdentity("a" * 64)
    selected = AnyOfTaskActivationSelection(
        gate_set.identity,
        TaskGateSelection(
            gate.identity, ColoredPetriNetBinding(gate.transition_identity, ())
        ),
        selection_result,
    )
    common = (
        TaskActivationIdentity("activation.one"),
        WorkflowIdentity("workflow.one"),
        WorkflowRunIdentity("run.one"),
        task_instance,
        OperationIdentity("operation.one"),
        AttemptIdentity("attempt.one"),
        (),
    )
    assert SUT(*common, selected).selection is selected

    with pytest.raises(ValueError):
        SUT(
            *common,
            AnyOfTaskActivationSelection(
                gate_set.identity,
                TaskGateSelection(
                    TaskStartGateIdentity("gate.outside"),
                    ColoredPetriNetBinding(gate.transition_identity, ()),
                ),
                selection_result,
            ),
        )
    with pytest.raises(ValueError):
        SUT(
            *common,
            AnyOfTaskActivationSelection(
                gate_set.identity,
                TaskGateSelection(
                    gate.identity,
                    ColoredPetriNetBinding(
                        ColoredPetriNetTransitionIdentity("transition.other"), ()
                    ),
                ),
                selection_result,
            ),
        )


def test_constructor__all_of_selection__requires_complete_canonical_member_tuple() -> (
    None
):
    """Test complete canonical ``all_of`` selection correlation.

    Evidence ID: SV-WFM-ACTIVATION-003

    Requirement: ``all_of`` activation contains every member exactly once in
    priority-then-gate-identity order with matching transitions.

    Acceptance: The canonical tuple constructs and the same members in storage order
    rather than canonical order raise ``ValueError``.
    """
    later = TaskStartGate(
        TaskStartGateIdentity("later"),
        2,
        ColoredPetriNetTransitionIdentity("transition.later"),
    )
    first = TaskStartGate(
        TaskStartGateIdentity("first"),
        1,
        ColoredPetriNetTransitionIdentity("transition.first"),
    )
    gate_set = TaskStartGateSet(
        TaskStartGateSetIdentity("set.all"),
        TaskStartGateSetMode.ALL_OF,
        (later, first),
    )
    task_instance = TaskInstance(
        TaskInstanceIdentity("instance.one"),
        TaskDefinitionIdentity("task.one"),
        gate_set,
    )
    selection_result = ColoredPetriNetSelectionResultIdentity("a" * 64)
    canonical = AllOfTaskActivationSelection(
        gate_set.identity,
        (
            TaskGateSelection(
                first.identity, ColoredPetriNetBinding(first.transition_identity, ())
            ),
            TaskGateSelection(
                later.identity, ColoredPetriNetBinding(later.transition_identity, ())
            ),
        ),
        selection_result,
    )
    common = (
        TaskActivationIdentity("activation.one"),
        WorkflowIdentity("workflow.one"),
        WorkflowRunIdentity("run.one"),
        task_instance,
        OperationIdentity("operation.one"),
        AttemptIdentity("attempt.one"),
        (),
    )
    assert SUT(*common, canonical).selection is canonical

    with pytest.raises(ValueError):
        SUT(
            *common,
            AllOfTaskActivationSelection(
                gate_set.identity,
                (
                    TaskGateSelection(
                        later.identity,
                        ColoredPetriNetBinding(later.transition_identity, ()),
                    ),
                    TaskGateSelection(
                        first.identity,
                        ColoredPetriNetBinding(first.transition_identity, ()),
                    ),
                ),
                selection_result,
            ),
        )


def test_constructor__inputs__requires_unique_names_and_result_identities() -> None:
    """Test both Task-input uniqueness dimensions on activation.

    Evidence ID: SV-WFM-ACTIVATION-004

    Requirement: Input names and ``ResultObjectIdentity`` values are independently
    unique within one activation.

    Acceptance: Duplicate names and duplicate result identities each raise
    ``ValueError`` before any Task is invoked.
    """

    @dataclass(frozen=True, slots=True)
    class ConcreteResult:
        identity: ResultObjectIdentity

    first = ConcreteResult(ResultObjectIdentity("result.one"))
    second = ConcreteResult(ResultObjectIdentity("result.two"))
    task_instance = TaskInstance(
        TaskInstanceIdentity("instance.one"), TaskDefinitionIdentity("task.one"), None
    )
    common = (
        TaskActivationIdentity("activation.one"),
        WorkflowIdentity("workflow.one"),
        WorkflowRunIdentity("run.one"),
        task_instance,
        OperationIdentity("operation.one"),
        AttemptIdentity("attempt.one"),
    )
    selection = DirectTaskActivationSelection(
        ColoredPetriNetSelectionResultIdentity("a" * 64)
    )
    with pytest.raises(ValueError):
        SUT(
            *common,
            (TaskInputBinding("input", first), TaskInputBinding("input", second)),
            selection,
        )
    with pytest.raises(ValueError):
        SUT(
            *common,
            (
                TaskInputBinding("first", first),
                TaskInputBinding("second", first),
            ),
            selection,
        )
