"""Immutable scientific Task, Workflow, gate, and activation contracts.

This module represents calculator-independent scientific composition.  Concrete
scientific packages own concrete :class:`ResultObject` implementations and their
intrinsic scientific invariants.  Workflow composition owns run-scoped Task
instances and start gates, while generic transition bindings and selection-result
identities remain owned by :mod:`ksdft2effmass.petrinet.colored`.

The records and protocols perform no scheduling, Task invocation, enablement,
firing, persistence, external effect, scientific calculation, acceptance, or
historical migration.  Their tests provide software verification only.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, runtime_checkable

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetBinding,
    ColoredPetriNetSelectionResultIdentity,
    ColoredPetriNetTransitionIdentity,
)


def _require_identity_value(value: object, owner: str) -> None:
    """Require one nonempty exact built-in string without selecting a wire grammar."""
    if type(value) is not str:
        raise TypeError(f"{owner} value must be a string")
    if not value:
        raise ValueError(f"{owner} value must not be empty")


@dataclass(frozen=True, slots=True)
class ResultObjectIdentity:
    """Nominal identity of one immutable workflow-facing result.

    Parameters
    ----------
    value
        Nonempty owner-local lexical identity.  Digest algorithms, canonical
        encodings, and wire formats are deliberately not selected here.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity value."""
        _require_identity_value(self.value, "result object identity")


@dataclass(frozen=True, slots=True)
class TaskDefinitionIdentity:
    """Nominal identity of one reusable Task contract.

    Parameters
    ----------
    value
        Nonempty owner-local lexical identity.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity value."""
        _require_identity_value(self.value, "task definition identity")


@dataclass(frozen=True, slots=True)
class TaskInstanceIdentity:
    """Nominal identity of one run-scoped Task instance.

    Parameters
    ----------
    value
        Nonempty owner-local lexical identity.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity value."""
        _require_identity_value(self.value, "task instance identity")


@dataclass(frozen=True, slots=True)
class WorkflowIdentity:
    """Nominal identity of one reusable Workflow definition.

    Parameters
    ----------
    value
        Nonempty owner-local lexical identity.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity value."""
        _require_identity_value(self.value, "workflow identity")


@dataclass(frozen=True, slots=True)
class WorkflowRunIdentity:
    """Nominal identity of one represented Workflow run.

    Parameters
    ----------
    value
        Nonempty owner-local lexical identity.  This identity does not itself
        claim that a run aggregate exists or has been persisted.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity value."""
        _require_identity_value(self.value, "workflow run identity")


@dataclass(frozen=True, slots=True)
class TaskStartGateIdentity:
    """Nominal identity of one Workflow-owned Task start gate.

    Parameters
    ----------
    value
        Nonempty owner-local lexical identity.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity value."""
        _require_identity_value(self.value, "task start gate identity")


@dataclass(frozen=True, slots=True)
class TaskStartGateSetIdentity:
    """Nominal identity of one immutable Task start-gate policy.

    Parameters
    ----------
    value
        Nonempty owner-local lexical identity.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity value."""
        _require_identity_value(self.value, "task start gate set identity")


@dataclass(frozen=True, slots=True)
class TaskActivationIdentity:
    """Nominal identity of one exact Task activation.

    Parameters
    ----------
    value
        Nonempty owner-local lexical identity.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity value."""
        _require_identity_value(self.value, "task activation identity")


@dataclass(frozen=True, slots=True)
class OperationIdentity:
    """Nominal identity of one intended Task operation.

    Parameters
    ----------
    value
        Nonempty owner-local lexical identity.  A retry or new execution uses a
        different operation identity under the surrounding authority contract.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity value."""
        _require_identity_value(self.value, "operation identity")


@dataclass(frozen=True, slots=True)
class AttemptIdentity:
    """Nominal identity of one bounded operation attempt.

    Parameters
    ----------
    value
        Nonempty owner-local lexical identity.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity value."""
        _require_identity_value(self.value, "attempt identity")


@runtime_checkable
class ResultObject(Protocol):
    """Structural protocol for an immutable workflow-facing result.

    Concrete scientific domains own implementations, fields, units, provenance,
    and intrinsic invariants.  Protocol conformance does not establish scientific
    validity or authorize use of the represented result.
    """

    @property
    def identity(self) -> ResultObjectIdentity:
        """Return the exact workflow-facing result identity."""
        ...


@dataclass(frozen=True, slots=True)
class TaskInputBinding:
    """Bind one Task input name to one already-existing result.

    Parameters
    ----------
    name
        Nonempty exact built-in string interpreted by the concrete Task contract.
    result
        Concrete immutable :class:`ResultObject`.  The binding neither produces
        nor validates the scientific meaning of the result.
    """

    name: str
    result: ResultObject

    def __post_init__(self) -> None:
        """Validate the name and structural result identity boundary."""
        if type(self.name) is not str:
            raise TypeError("input binding name must be a string")
        if not self.name:
            raise ValueError("input binding name must not be empty")
        if not isinstance(self.result, ResultObject):
            raise TypeError("result must implement ResultObject")
        if type(self.result.identity) is not ResultObjectIdentity:
            raise TypeError("result identity must be ResultObjectIdentity")


@dataclass(frozen=True, slots=True)
class TaskExecutionContext:
    """Explicit correlation context supplied to one Task operation.

    Parameters
    ----------
    workflow_identity
        Reusable Workflow definition containing the run-scoped Task instance.
    workflow_run_identity
        Exact represented Workflow run.
    task_instance_identity
        Run-scoped Task instance being invoked.
    task_activation_identity
        Exact activation selected for this operation.
    operation_identity
        Intended operation identity.
    attempt_identity
        Exact bounded attempt identity.

    Notes
    -----
    Context is correlation state, not execution authority, a scheduler, a run
    aggregate, or a durable invocation outcome.
    """

    workflow_identity: WorkflowIdentity
    workflow_run_identity: WorkflowRunIdentity
    task_instance_identity: TaskInstanceIdentity
    task_activation_identity: TaskActivationIdentity
    operation_identity: OperationIdentity
    attempt_identity: AttemptIdentity

    def __post_init__(self) -> None:
        """Require exact Workflow-owned nominal identity types."""
        expected = (
            ("workflow_identity", WorkflowIdentity),
            ("workflow_run_identity", WorkflowRunIdentity),
            ("task_instance_identity", TaskInstanceIdentity),
            ("task_activation_identity", TaskActivationIdentity),
            ("operation_identity", OperationIdentity),
            ("attempt_identity", AttemptIdentity),
        )
        for name, nominal_type in expected:
            if type(getattr(self, name)) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")


@runtime_checkable
class Task(Protocol):
    """Structural ActionObject protocol for one reusable scientific operation.

    A Task consumes named, already-bound ResultObjects plus explicit operation
    context and returns newly produced ResultObjects.  It does not discover
    prerequisites, inspect a complete marking, schedule itself, own start-gate
    policy, or construct a durable invocation outcome.
    """

    @property
    def identity(self) -> TaskDefinitionIdentity:
        """Return the exact reusable Task-definition identity."""
        ...

    def execute(
        self,
        inputs: tuple[TaskInputBinding, ...],
        context: TaskExecutionContext,
    ) -> tuple[ResultObject, ...]:
        """Execute the concrete operation under separately established authority.

        Parameters
        ----------
        inputs
            Named immutable results already bound by the enclosing caller.
        context
            Exact Workflow, run, instance, activation, operation, and attempt
            correlation identities.

        Returns
        -------
        tuple[ResultObject, ...]
            Newly returned concrete immutable results.  Workflow control, not the
            Task, constructs any durable invocation outcome.
        """
        ...


class TaskStartGateSetMode(StrEnum):
    """Closed composition modes for a Task start-gate set."""

    ANY_OF = "any_of"
    ALL_OF = "all_of"


@dataclass(frozen=True, slots=True)
class TaskStartGate:
    """One Workflow-owned automatic-start gate.

    Parameters
    ----------
    identity
        Stable gate identity within its owning Workflow definition.
    priority
        Nonnegative exact built-in integer.  Lower values are selected first for
        ``any_of``; Boolean values are rejected.
    transition_identity
        Exact generic transition represented by this gate.
    """

    identity: TaskStartGateIdentity
    priority: int
    transition_identity: ColoredPetriNetTransitionIdentity

    def __post_init__(self) -> None:
        """Validate gate identity, priority, and transition identity."""
        if type(self.identity) is not TaskStartGateIdentity:
            raise TypeError("identity must be TaskStartGateIdentity")
        if type(self.priority) is not int:
            raise TypeError("priority must be an integer")
        if self.priority < 0:
            raise ValueError("priority must be nonnegative")
        if type(self.transition_identity) is not ColoredPetriNetTransitionIdentity:
            raise TypeError(
                "transition_identity must be ColoredPetriNetTransitionIdentity"
            )


@dataclass(frozen=True, slots=True)
class TaskStartGateSet:
    """Immutable ``any_of`` or ``all_of`` automatic-start policy.

    Parameters
    ----------
    identity
        Exact identity of this gate-set policy.
    mode
        Exactly :attr:`TaskStartGateSetMode.ANY_OF` or
        :attr:`TaskStartGateSetMode.ALL_OF`.
    gates
        Tuple of unique member gates.  Storage order is retained and is not
        selection order.  An empty tuple is valid but enables no automatic start.
    """

    identity: TaskStartGateSetIdentity
    mode: TaskStartGateSetMode
    gates: tuple[TaskStartGate, ...]

    def __post_init__(self) -> None:
        """Validate immutable members and unique gate identities."""
        if type(self.identity) is not TaskStartGateSetIdentity:
            raise TypeError("identity must be TaskStartGateSetIdentity")
        if type(self.mode) is not TaskStartGateSetMode:
            raise TypeError("mode must be TaskStartGateSetMode")
        if type(self.gates) is not tuple or any(
            type(gate) is not TaskStartGate for gate in self.gates
        ):
            raise TypeError("gates must be a tuple of TaskStartGate")
        identities = tuple(gate.identity for gate in self.gates)
        if len(set(identities)) != len(identities):
            raise ValueError("gate identities must be unique")

    @property
    def selection_order(self) -> tuple[TaskStartGate, ...]:
        """Return gates in deterministic priority-then-identity order."""
        return tuple(
            sorted(self.gates, key=lambda gate: (gate.priority, gate.identity.value))
        )


@dataclass(frozen=True, slots=True)
class TaskInstance:
    """Run-scoped instance of one reusable Task definition.

    Parameters
    ----------
    identity
        Exact run-scoped Task-instance identity.
    definition_identity
        Reusable Task contract represented by the instance.
    start_gate_set
        Zero or one immutable Workflow-owned automatic-start policy.  ``None``
        and an empty gate set both provide no automatic activation.
    """

    identity: TaskInstanceIdentity
    definition_identity: TaskDefinitionIdentity
    start_gate_set: TaskStartGateSet | None

    def __post_init__(self) -> None:
        """Validate the exact Task identities and optional gate set."""
        if type(self.identity) is not TaskInstanceIdentity:
            raise TypeError("identity must be TaskInstanceIdentity")
        if type(self.definition_identity) is not TaskDefinitionIdentity:
            raise TypeError("definition_identity must be TaskDefinitionIdentity")
        if self.start_gate_set is not None and (
            type(self.start_gate_set) is not TaskStartGateSet
        ):
            raise TypeError("start_gate_set must be TaskStartGateSet or None")


@dataclass(frozen=True, slots=True)
class WorkflowComposition:
    """Immutable Task-instance membership for one Workflow definition.

    Parameters
    ----------
    workflow_identity
        Exact reusable Workflow definition represented by this composition.
    task_instances
        Tuple of run-scoped Task instances with unique identities.  Membership
        does not imply prerequisite closure, activation, or execution authority.
    """

    workflow_identity: WorkflowIdentity
    task_instances: tuple[TaskInstance, ...]

    def __post_init__(self) -> None:
        """Validate immutable members and unique Task-instance identities."""
        if type(self.workflow_identity) is not WorkflowIdentity:
            raise TypeError("workflow_identity must be WorkflowIdentity")
        if type(self.task_instances) is not tuple or any(
            type(instance) is not TaskInstance for instance in self.task_instances
        ):
            raise TypeError("task_instances must be a tuple of TaskInstance")
        identities = tuple(instance.identity for instance in self.task_instances)
        if len(set(identities)) != len(identities):
            raise ValueError("task instance identities must be unique")


@runtime_checkable
class Workflow(Task, Protocol):
    """Structural Task protocol for one reusable composite scientific operation.

    A nested Workflow may be accepted wherever a Task is accepted.  The later
    WorkflowRun owner creates a distinct child run for each nested invocation;
    this protocol stores no marking, history, persistence, or runtime engine.
    """

    @property
    def workflow_identity(self) -> WorkflowIdentity:
        """Return the exact reusable Workflow-definition identity."""
        ...

    @property
    def composition(self) -> WorkflowComposition:
        """Return the immutable Task-instance composition."""
        ...


@dataclass(frozen=True, slots=True)
class TaskGateSelection:
    """Bind one selected Workflow gate to one generic transition binding.

    Parameters
    ----------
    gate_identity
        Exact selected member-gate identity.
    binding
        Immutable generic binding whose transition must agree with that gate when
        correlated by :class:`TaskActivation`.
    """

    gate_identity: TaskStartGateIdentity
    binding: ColoredPetriNetBinding

    def __post_init__(self) -> None:
        """Validate the owner-local gate and generic binding types."""
        if type(self.gate_identity) is not TaskStartGateIdentity:
            raise TypeError("gate_identity must be TaskStartGateIdentity")
        if type(self.binding) is not ColoredPetriNetBinding:
            raise TypeError("binding must be ColoredPetriNetBinding")


@dataclass(frozen=True, slots=True)
class DirectTaskActivationSelection:
    """Direct activation with no gate-set or selected-gate identity.

    Parameters
    ----------
    selection_result_identity
        Exact generic selection result correlated to the direct activation.
    """

    selection_result_identity: ColoredPetriNetSelectionResultIdentity

    def __post_init__(self) -> None:
        """Validate the exact generic selection-result identity."""
        if type(self.selection_result_identity) is not (
            ColoredPetriNetSelectionResultIdentity
        ):
            raise TypeError(
                "selection_result_identity must be "
                "ColoredPetriNetSelectionResultIdentity"
            )


@dataclass(frozen=True, slots=True)
class AnyOfTaskActivationSelection:
    """Activation selecting exactly one member of an ``any_of`` gate set.

    Parameters
    ----------
    gate_set_identity
        Exact selected gate-set identity.
    selected_gate
        One member gate and its generic binding.
    selection_result_identity
        Exact generic selection result correlated to this choice.
    """

    gate_set_identity: TaskStartGateSetIdentity
    selected_gate: TaskGateSelection
    selection_result_identity: ColoredPetriNetSelectionResultIdentity

    def __post_init__(self) -> None:
        """Validate the discriminant-owned nominal fields."""
        if type(self.gate_set_identity) is not TaskStartGateSetIdentity:
            raise TypeError("gate_set_identity must be TaskStartGateSetIdentity")
        if type(self.selected_gate) is not TaskGateSelection:
            raise TypeError("selected_gate must be TaskGateSelection")
        if type(self.selection_result_identity) is not (
            ColoredPetriNetSelectionResultIdentity
        ):
            raise TypeError(
                "selection_result_identity must be "
                "ColoredPetriNetSelectionResultIdentity"
            )


@dataclass(frozen=True, slots=True)
class AllOfTaskActivationSelection:
    """Activation selecting a complete canonical ``all_of`` member tuple.

    Parameters
    ----------
    gate_set_identity
        Exact selected gate-set identity.
    selected_gates
        Complete tuple containing one binding for every member gate.  The owning
        :class:`TaskActivation` requires priority-then-gate-identity order.
    selection_result_identity
        Exact generic selection result correlated to the collective choice.
    """

    gate_set_identity: TaskStartGateSetIdentity
    selected_gates: tuple[TaskGateSelection, ...]
    selection_result_identity: ColoredPetriNetSelectionResultIdentity

    def __post_init__(self) -> None:
        """Validate the discriminant-owned nominal fields and tuple shape."""
        if type(self.gate_set_identity) is not TaskStartGateSetIdentity:
            raise TypeError("gate_set_identity must be TaskStartGateSetIdentity")
        if type(self.selected_gates) is not tuple or any(
            type(selection) is not TaskGateSelection
            for selection in self.selected_gates
        ):
            raise TypeError("selected_gates must be a tuple of TaskGateSelection")
        identities = tuple(item.gate_identity for item in self.selected_gates)
        if len(set(identities)) != len(identities):
            raise ValueError("selected gate identities must be unique")
        if type(self.selection_result_identity) is not (
            ColoredPetriNetSelectionResultIdentity
        ):
            raise TypeError(
                "selection_result_identity must be "
                "ColoredPetriNetSelectionResultIdentity"
            )


type TaskActivationSelection = (
    DirectTaskActivationSelection
    | AnyOfTaskActivationSelection
    | AllOfTaskActivationSelection
)


@dataclass(frozen=True, slots=True)
class TaskActivation:
    """One exact discriminated activation of a run-scoped Task instance.

    Parameters
    ----------
    identity
        Exact activation identity.
    workflow_identity, workflow_run_identity
        Reusable Workflow and exact represented run correlation.
    task_instance
        Exact run-scoped Task instance being activated.
    operation_identity, attempt_identity
        Intended operation and bounded attempt identities.
    inputs
        Named, already-bound ResultObjects.  Names and result identities must each
        be unique.
    selection
        Exactly one direct, ``any_of``, or ``all_of`` selection variant.

    Notes
    -----
    Construction verifies intrinsic composition correlations.  It does not prove
    generic enablement, authorize execution, invoke the Task, or create a durable
    invocation outcome.
    """

    identity: TaskActivationIdentity
    workflow_identity: WorkflowIdentity
    workflow_run_identity: WorkflowRunIdentity
    task_instance: TaskInstance
    operation_identity: OperationIdentity
    attempt_identity: AttemptIdentity
    inputs: tuple[TaskInputBinding, ...]
    selection: TaskActivationSelection

    def __post_init__(self) -> None:
        """Validate identities, input uniqueness, and selection discrimination."""
        expected = (
            ("identity", TaskActivationIdentity),
            ("workflow_identity", WorkflowIdentity),
            ("workflow_run_identity", WorkflowRunIdentity),
            ("task_instance", TaskInstance),
            ("operation_identity", OperationIdentity),
            ("attempt_identity", AttemptIdentity),
        )
        for name, nominal_type in expected:
            if type(getattr(self, name)) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.inputs) is not tuple or any(
            type(item) is not TaskInputBinding for item in self.inputs
        ):
            raise TypeError("inputs must be a tuple of TaskInputBinding")
        names = tuple(item.name for item in self.inputs)
        if len(set(names)) != len(names):
            raise ValueError("input binding names must be unique")
        result_identities = tuple(item.result.identity for item in self.inputs)
        if len(set(result_identities)) != len(result_identities):
            raise ValueError("input result identities must be unique")

        gate_set = self.task_instance.start_gate_set
        if type(self.selection) is DirectTaskActivationSelection:
            if gate_set is not None and gate_set.gates:
                raise ValueError("direct activation requires no nonempty gate set")
            return
        selection: AnyOfTaskActivationSelection | AllOfTaskActivationSelection
        if type(self.selection) is AnyOfTaskActivationSelection:
            selection = self.selection
        elif type(self.selection) is AllOfTaskActivationSelection:
            selection = self.selection
        else:
            raise TypeError("selection must be a TaskActivationSelection variant")
        if gate_set is None:
            raise ValueError("automatic activation requires a gate set")
        if selection.gate_set_identity != gate_set.identity:
            raise ValueError(
                "activation gate-set identity must match the Task instance"
            )

        gates_by_identity = {gate.identity: gate for gate in gate_set.gates}
        if type(selection) is AnyOfTaskActivationSelection:
            if gate_set.mode is not TaskStartGateSetMode.ANY_OF:
                raise ValueError("any_of activation requires an any_of gate set")
            selected = selection.selected_gate
            gate = gates_by_identity.get(selected.gate_identity)
            if gate is None:
                raise ValueError("selected gate must be a gate-set member")
            if selected.binding.transition_identity != gate.transition_identity:
                raise ValueError("selected binding transition must match its gate")
            return

        if gate_set.mode is not TaskStartGateSetMode.ALL_OF:
            raise ValueError("all_of activation requires an all_of gate set")
        assert type(selection) is AllOfTaskActivationSelection
        expected_gate_order = tuple(gate.identity for gate in gate_set.selection_order)
        selected_gate_order = tuple(
            selected.gate_identity for selected in selection.selected_gates
        )
        if selected_gate_order != expected_gate_order:
            raise ValueError(
                "all_of selections must contain every gate in canonical order"
            )
        for selected in selection.selected_gates:
            gate = gates_by_identity[selected.gate_identity]
            if selected.binding.transition_identity != gate.transition_identity:
                raise ValueError("selected binding transition must match its gate")
