"""Effect-free adaptation from Workflow activation policy to generic CPN selection.

The adapter consumes an explicit immutable Workflow-owned mapping, an exact generic
colored-Petri-net definition and marking, and one activation request.  It delegates
pure enablement and selection to :mod:`ksdft2effmass.petrinet.colored` and constructs
an existing :class:`~ksdft2effmass.workflows.TaskActivation` only after every mapping
and identity correlation closes.

The module performs no Task invocation, firing, marking mutation, persistence,
scheduling, external execution, authority decision, scientific calculation, or
scientific acceptance.  Its maintained tests provide software verification only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import StrEnum
from hashlib import sha256
from itertools import product
from string import hexdigits
from typing import final

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetBinding,
    ColoredPetriNetBindingAssignment,
    ColoredPetriNetBindingSelector,
    ColoredPetriNetBindingVariableIdentity,
    ColoredPetriNetDefinition,
    ColoredPetriNetEnablementResult,
    ColoredPetriNetMarking,
    ColoredPetriNetPlaceIdentity,
    ColoredPetriNetSelectionDirective,
    ColoredPetriNetSelectionFailureCode,
    ColoredPetriNetSelectionOutcomeKind,
    ColoredPetriNetSelectionResult,
    ColoredPetriNetToken,
    ColoredPetriNetTokenIdentity,
    ColoredPetriNetTransitionEnabler,
    ColoredPetriNetTransitionIdentity,
    ColoredPetriNetValue,
)

from .model import (
    AllOfTaskActivationSelection,
    AnyOfTaskActivationSelection,
    AttemptIdentity,
    DirectTaskActivationSelection,
    OperationIdentity,
    ResultObjectIdentity,
    TaskActivation,
    TaskActivationIdentity,
    TaskActivationSelection,
    TaskGateSelection,
    TaskInputBinding,
    TaskInstance,
    TaskInstanceIdentity,
    TaskStartGate,
    TaskStartGateSetMode,
    WorkflowIdentity,
    WorkflowRunIdentity,
)


def _generic_value_identity_state(value: ColoredPetriNetValue) -> object:
    """Return JSON-safe exact active state for one generic tagged value."""
    active = value.value
    if type(active) is float:
        return active.hex()
    if type(active) is int:
        return str(active)
    if type(active) is tuple:
        return list(active)
    return active


def _binding_identity_state(binding: ColoredPetriNetBinding) -> dict[str, object]:
    """Return exact generic binding state for adapter result identity."""
    return {
        "transition": binding.transition_identity.value,
        "assignments": [
            {
                "variable": assignment.variable_identity.value,
                "kind": assignment.value.kind.value,
                "value": _generic_value_identity_state(assignment.value),
            }
            for assignment in binding.assignments
        ],
    }


class ColoredPetriNetWorkflowSelectionPolicy(StrEnum):
    """Workflow-owned permission for noncanonical generic selection.

    ``DETERMINISTIC_ONLY`` permits only the generic canonical binding.
    ``DIRECTED_ALLOWED`` permits an exact identity-bound directive when the generic
    definition independently permits directed selection.
    """

    DETERMINISTIC_ONLY = "deterministic_only"
    DIRECTED_ALLOWED = "directed_allowed"


class ColoredPetriNetWorkflowActivationMode(StrEnum):
    """Closed caller intent for automatic or direct Task activation."""

    AUTOMATIC = "automatic"
    DIRECT = "direct"


@dataclass(frozen=True, slots=True)
class WorkflowResultTokenMapping:
    """Correlate one bound Workflow input result with one identified generic token.

    Parameters
    ----------
    input_name
        Exact Task input-binding name.
    result_identity
        Exact identity of the already-existing Workflow-facing result.
    variable_identity
        Generic binding variable to which the represented token value maps.
    place_identity
        Generic place expected to contain the represented token.
    token
        Individually identified generic token representing the result value.  An
        anonymous token is rejected because it cannot close result correlation.

    Notes
    -----
    This record represents an explicit supplied correlation.  It does not convert a
    scientific value, validate units, or assert physical equivalence.
    """

    input_name: str
    result_identity: ResultObjectIdentity
    variable_identity: ColoredPetriNetBindingVariableIdentity
    place_identity: ColoredPetriNetPlaceIdentity
    token: ColoredPetriNetToken

    def __post_init__(self) -> None:
        """Validate exact nominal fields and identified-token correlation."""
        if type(self.input_name) is not str:
            raise TypeError("input_name must be a string")
        if not self.input_name:
            raise ValueError("input_name must not be empty")
        if type(self.result_identity) is not ResultObjectIdentity:
            raise TypeError("result_identity must be ResultObjectIdentity")
        if type(self.variable_identity) is not ColoredPetriNetBindingVariableIdentity:
            raise TypeError(
                "variable_identity must be ColoredPetriNetBindingVariableIdentity"
            )
        if type(self.place_identity) is not ColoredPetriNetPlaceIdentity:
            raise TypeError("place_identity must be ColoredPetriNetPlaceIdentity")
        if type(self.token) is not ColoredPetriNetToken:
            raise TypeError("token must be ColoredPetriNetToken")
        if self.token.token_identity is None:
            raise ValueError("workflow result mapping requires an identified token")

    @property
    def token_identity(self) -> ColoredPetriNetTokenIdentity:
        """Return the required individually identified generic token identity."""
        identity = self.token.token_identity
        assert identity is not None
        return identity


@dataclass(frozen=True, slots=True)
class ColoredPetriNetWorkflowMapping:
    """Immutable Workflow-owned mapping for one run-scoped Task instance.

    Parameters
    ----------
    workflow_identity
        Exact reusable Workflow definition owning this mapping.
    task_instance_identity
        Exact run-scoped Task instance to which the mapping applies.
    selection_policy
        Workflow-owned permission for noncanonical generic selection.  Generic CPN
        permission remains independently necessary.
    direct_transition_identity
        Generic transition permitted for direct invocation, or ``None`` when direct
        activation is not mapped.
    all_of_transition_identity
        Generic activation transition whose binding combines a complete compatible
        ``all_of`` member tuple, or ``None`` when no ``all_of`` mapping exists.

    Notes
    -----
    Individual ``any_of`` member transitions remain identified by
    :class:`~ksdft2effmass.workflows.TaskStartGate`.  This record introduces no wire
    format and stores no mutable runtime state.
    """

    workflow_identity: WorkflowIdentity
    task_instance_identity: TaskInstanceIdentity
    selection_policy: ColoredPetriNetWorkflowSelectionPolicy
    direct_transition_identity: ColoredPetriNetTransitionIdentity | None = None
    all_of_transition_identity: ColoredPetriNetTransitionIdentity | None = None

    def __post_init__(self) -> None:
        """Validate the exact Workflow and generic mapping identities."""
        if type(self.workflow_identity) is not WorkflowIdentity:
            raise TypeError("workflow_identity must be WorkflowIdentity")
        if type(self.task_instance_identity) is not TaskInstanceIdentity:
            raise TypeError("task_instance_identity must be TaskInstanceIdentity")
        if type(self.selection_policy) is not ColoredPetriNetWorkflowSelectionPolicy:
            raise TypeError(
                "selection_policy must be ColoredPetriNetWorkflowSelectionPolicy"
            )
        for name in ("direct_transition_identity", "all_of_transition_identity"):
            value = getattr(self, name)
            if value is not None and (
                type(value) is not ColoredPetriNetTransitionIdentity
            ):
                raise TypeError(
                    f"{name} must be ColoredPetriNetTransitionIdentity or None"
                )


@dataclass(frozen=True, slots=True)
class ColoredPetriNetWorkflowActivationRequest:
    """Exact immutable request for one effect-free Workflow activation selection.

    Parameters
    ----------
    mapping
        Workflow-owned mapping for the requested Task instance.
    definition, marking
        Exact generic CPN definition and predecessor marking supplied to pure
        enablement.
    workflow_run_identity
        Exact represented Workflow run correlation.
    task_instance
        Run-scoped Task instance being considered.
    activation_identity, operation_identity, attempt_identity
        Exact activation, intended operation, and bounded attempt identities.
    inputs
        Already-bound immutable Workflow results.
    result_token_mappings
        Exact one-to-one correlations between ``inputs`` and individually identified
        tokens in ``marking``.
    mode
        Automatic gate selection or caller-identified direct activation.
    direct_binding
        Exact requested direct binding.  Required only for ``DIRECT`` mode.

    Raises
    ------
    TypeError
        A field has the wrong exact nominal type or a collection is mutable.
    ValueError
        Input/result-token correlations are not exact, or direct-mode discrimination
        is invalid.
    """

    mapping: ColoredPetriNetWorkflowMapping
    definition: ColoredPetriNetDefinition
    marking: ColoredPetriNetMarking
    workflow_run_identity: WorkflowRunIdentity
    task_instance: TaskInstance
    activation_identity: TaskActivationIdentity
    operation_identity: OperationIdentity
    attempt_identity: AttemptIdentity
    inputs: tuple[TaskInputBinding, ...]
    result_token_mappings: tuple[WorkflowResultTokenMapping, ...]
    mode: ColoredPetriNetWorkflowActivationMode
    direct_binding: ColoredPetriNetBinding | None = None

    def __post_init__(self) -> None:
        """Validate intrinsic request types, discrimination, and exact input mapping."""
        expected = (
            ("mapping", ColoredPetriNetWorkflowMapping),
            ("definition", ColoredPetriNetDefinition),
            ("marking", ColoredPetriNetMarking),
            ("workflow_run_identity", WorkflowRunIdentity),
            ("task_instance", TaskInstance),
            ("activation_identity", TaskActivationIdentity),
            ("operation_identity", OperationIdentity),
            ("attempt_identity", AttemptIdentity),
            ("mode", ColoredPetriNetWorkflowActivationMode),
        )
        for name, nominal_type in expected:
            if type(getattr(self, name)) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.inputs) is not tuple or any(
            type(item) is not TaskInputBinding for item in self.inputs
        ):
            raise TypeError("inputs must be a tuple of TaskInputBinding")
        if type(self.result_token_mappings) is not tuple or any(
            type(item) is not WorkflowResultTokenMapping
            for item in self.result_token_mappings
        ):
            raise TypeError(
                "result_token_mappings must be a tuple of WorkflowResultTokenMapping"
            )
        if self.direct_binding is not None and (
            type(self.direct_binding) is not ColoredPetriNetBinding
        ):
            raise TypeError("direct_binding must be ColoredPetriNetBinding or None")
        if self.mode is ColoredPetriNetWorkflowActivationMode.DIRECT:
            if self.direct_binding is None:
                raise ValueError("direct mode requires direct_binding")
            gate_set = self.task_instance.start_gate_set
            if gate_set is not None and gate_set.gates:
                raise ValueError("direct mode requires no nonempty gate set")
        elif self.direct_binding is not None:
            raise ValueError("automatic mode prohibits direct_binding")

        input_keys = tuple((item.name, item.result.identity) for item in self.inputs)
        mapping_keys = tuple(
            (item.input_name, item.result_identity)
            for item in self.result_token_mappings
        )
        input_names = tuple(item[0] for item in input_keys)
        input_result_identities = tuple(item[1] for item in input_keys)
        if len(set(input_names)) != len(input_names):
            raise ValueError("input names must be unique")
        if len(set(input_result_identities)) != len(input_result_identities):
            raise ValueError("input result identities must be unique")
        mapping_names = tuple(item[0] for item in mapping_keys)
        mapping_result_identities = tuple(item[1] for item in mapping_keys)
        if len(set(mapping_names)) != len(mapping_names):
            raise ValueError("mapped input names must be unique")
        if len(set(mapping_result_identities)) != len(mapping_result_identities):
            raise ValueError("mapped result identities must be unique")
        if input_keys != mapping_keys:
            raise ValueError(
                "result-token mappings must cover every input in input order"
            )
        token_identities = tuple(
            item.token_identity for item in self.result_token_mappings
        )
        if len(set(token_identities)) != len(token_identities):
            raise ValueError("mapped token identities must be unique")
        variable_identities = tuple(
            item.variable_identity for item in self.result_token_mappings
        )
        if len(set(variable_identities)) != len(variable_identities):
            raise ValueError("mapped variable identities must be unique")


class ColoredPetriNetWorkflowActivationOutcomeKind(StrEnum):
    """Closed effect-free adapter outcomes."""

    ACTIVATED = "activated"
    NOT_ENABLED = "not_enabled"
    FAILURE = "failure"


class ColoredPetriNetWorkflowActivationFailureCode(StrEnum):
    """Stable failure partitions owned by Workflow-to-CPN adaptation."""

    INVALID_WORKFLOW_MAPPING = "invalid_workflow_mapping"
    INVALID_RESULT_TOKEN_MAPPING = "invalid_result_token_mapping"
    INVALID_GATE_MAPPING = "invalid_gate_mapping"
    ENABLEMENT_FAILED = "enablement_failed"
    DIRECTED_SELECTION_PROHIBITED = "directed_selection_prohibited"
    SELECTION_FAILED = "selection_failed"
    SELECTION_CORRELATION_MISMATCH = "selection_correlation_mismatch"


@dataclass(frozen=True, slots=True)
class ColoredPetriNetWorkflowActivationResultIdentity:
    """Content identity of one closed effect-free adapter result.

    ``value`` is an exact lowercase SHA-256 digest of the adapter-owned represented
    request and outcome preimage.  It does not select a public wire format.
    """

    value: str

    def __post_init__(self) -> None:
        """Require one exact lowercase SHA-256 spelling."""
        if type(self.value) is not str:
            raise TypeError("activation result identity value must be a string")
        if (
            len(self.value) != 64
            or self.value != self.value.lower()
            or any(character not in hexdigits for character in self.value)
        ):
            raise ValueError(
                "activation result identity must be a lowercase SHA-256 digest"
            )


@dataclass(frozen=True, slots=True)
class ColoredPetriNetWorkflowActivationResult:
    """Closed adapter result retaining generic evidence and optional activation.

    Parameters
    ----------
    request
        Exact immutable activation request.
    enablement_result
        Complete generic enablement result for the supplied definition and marking.
    outcome
        Exactly ``activated``, ``not_enabled``, or ``failure``.
    selection_result
        Generic selection result when selection was attempted.
    activation
        Constructed Workflow activation only for ``activated``.
    failure_code
        Stable adapter failure code only for ``failure``.
    identity
        Derived content identity of the complete represented result.
    """

    request: ColoredPetriNetWorkflowActivationRequest
    enablement_result: ColoredPetriNetEnablementResult
    outcome: ColoredPetriNetWorkflowActivationOutcomeKind
    selection_result: ColoredPetriNetSelectionResult | None = None
    activation: TaskActivation | None = None
    failure_code: ColoredPetriNetWorkflowActivationFailureCode | None = None
    identity: ColoredPetriNetWorkflowActivationResultIdentity = field(init=False)

    def __post_init__(self) -> None:
        """Enforce the closed outcome and derive its content identity."""
        if type(self.request) is not ColoredPetriNetWorkflowActivationRequest:
            raise TypeError("request must be ColoredPetriNetWorkflowActivationRequest")
        if type(self.enablement_result) is not ColoredPetriNetEnablementResult:
            raise TypeError("enablement_result must be ColoredPetriNetEnablementResult")
        if type(self.outcome) is not ColoredPetriNetWorkflowActivationOutcomeKind:
            raise TypeError(
                "outcome must be ColoredPetriNetWorkflowActivationOutcomeKind"
            )
        if self.selection_result is not None and (
            type(self.selection_result) is not ColoredPetriNetSelectionResult
        ):
            raise TypeError(
                "selection_result must be ColoredPetriNetSelectionResult or None"
            )
        if self.activation is not None and type(self.activation) is not TaskActivation:
            raise TypeError("activation must be TaskActivation or None")
        if self.failure_code is not None and (
            type(self.failure_code) is not ColoredPetriNetWorkflowActivationFailureCode
        ):
            raise TypeError(
                "failure_code must be ColoredPetriNetWorkflowActivationFailureCode "
                "or None"
            )
        if (
            self.enablement_result.definition_identity
            != self.request.definition.identity
        ):
            raise ValueError("enablement result must bind the request definition")
        if self.enablement_result.marking_identity != self.request.marking.identity:
            raise ValueError("enablement result must bind the request marking")

        valid = {
            ColoredPetriNetWorkflowActivationOutcomeKind.ACTIVATED: (
                self.activation is not None
                and self.selection_result is not None
                and self.selection_result.outcome
                is ColoredPetriNetSelectionOutcomeKind.SELECTED
                and self.failure_code is None
            ),
            ColoredPetriNetWorkflowActivationOutcomeKind.NOT_ENABLED: (
                self.activation is None
                and self.failure_code is None
                and (
                    self.selection_result is None
                    or self.selection_result.outcome
                    in (
                        ColoredPetriNetSelectionOutcomeKind.EMPTY,
                        ColoredPetriNetSelectionOutcomeKind.NO_MATCH,
                    )
                )
            ),
            ColoredPetriNetWorkflowActivationOutcomeKind.FAILURE: (
                self.activation is None and self.failure_code is not None
            ),
        }[self.outcome]
        if not valid:
            raise ValueError("activation result fields do not match the outcome")
        if self.selection_result is not None and (
            self.selection_result.enablement_result_identity
            != self.enablement_result.identity
        ):
            raise ValueError("selection result must bind the retained enablement")
        if self.activation is not None:
            activation = self.activation
            expected_activation_fields = (
                (activation.identity, self.request.activation_identity),
                (
                    activation.workflow_identity,
                    self.request.mapping.workflow_identity,
                ),
                (activation.workflow_run_identity, self.request.workflow_run_identity),
                (activation.task_instance, self.request.task_instance),
                (activation.operation_identity, self.request.operation_identity),
                (activation.attempt_identity, self.request.attempt_identity),
                (activation.inputs, self.request.inputs),
            )
            if any(
                actual != expected
                for actual, expected in expected_activation_fields
            ):
                raise ValueError("activation must bind the exact request")
            assert self.selection_result is not None
            if (
                activation.selection.selection_result_identity
                != self.selection_result.identity
            ):
                raise ValueError("activation must bind the retained selection result")

        gate_set = self.request.task_instance.start_gate_set
        direct_binding = self.request.direct_binding
        payload = {
            "domain": "ksdft2effmass.workflows.cpn-activation-result-identity-v1",
            "activation": self.request.activation_identity.value,
            "workflow": self.request.mapping.workflow_identity.value,
            "mapping": {
                "task_instance": self.request.mapping.task_instance_identity.value,
                "selection_policy": self.request.mapping.selection_policy.value,
                "direct_transition": (
                    None
                    if self.request.mapping.direct_transition_identity is None
                    else self.request.mapping.direct_transition_identity.value
                ),
                "all_of_transition": (
                    None
                    if self.request.mapping.all_of_transition_identity is None
                    else self.request.mapping.all_of_transition_identity.value
                ),
            },
            "gate_set": (
                None
                if gate_set is None
                else {
                    "identity": gate_set.identity.value,
                    "mode": gate_set.mode.value,
                    "gates": [
                        [
                            gate.identity.value,
                            str(gate.priority),
                            gate.transition_identity.value,
                        ]
                        for gate in gate_set.gates
                    ],
                }
            ),
            "direct_binding": (
                None
                if direct_binding is None
                else _binding_identity_state(direct_binding)
            ),
            "run": self.request.workflow_run_identity.value,
            "task_instance": self.request.task_instance.identity.value,
            "operation": self.request.operation_identity.value,
            "attempt": self.request.attempt_identity.value,
            "mode": self.request.mode.value,
            "inputs": [
                [item.name, item.result.identity.value] for item in self.request.inputs
            ],
            "tokens": [
                [
                    item.input_name,
                    item.result_identity.value,
                    item.variable_identity.value,
                    item.place_identity.value,
                    item.token_identity.value,
                ]
                for item in self.request.result_token_mappings
            ],
            "enablement": self.enablement_result.identity.value,
            "selection": (
                None
                if self.selection_result is None
                else self.selection_result.identity.value
            ),
            "outcome": self.outcome.value,
            "failure": None if self.failure_code is None else self.failure_code.value,
        }
        encoded = json.dumps(
            payload,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        object.__setattr__(
            self,
            "identity",
            ColoredPetriNetWorkflowActivationResultIdentity(
                sha256(encoded).hexdigest()
            ),
        )

    @property
    def is_activated(self) -> bool:
        """Return whether the result contains one exact Task activation."""
        return self.outcome is ColoredPetriNetWorkflowActivationOutcomeKind.ACTIVATED


@final
class ColoredPetriNetWorkflowAdapter:
    """Effect-free ActionObject adapting Workflow activation policy to generic CPN.

    The adapter validates explicit mappings, delegates generic enablement and
    selection, and returns a closed result.  It has no configurable mutable state and
    does not invoke the selected Task.
    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Reject subclass-injected Workflow mapping or selection policy."""
        raise TypeError("ColoredPetriNetWorkflowAdapter does not support subclasses")

    def execute(
        self, request: ColoredPetriNetWorkflowActivationRequest
    ) -> ColoredPetriNetWorkflowActivationResult:
        """Return one closed effect-free activation-selection result.

        Parameters
        ----------
        request
            Exact Workflow mapping, generic definition/marking, bound results, and
            activation correlations.

        Returns
        -------
        ColoredPetriNetWorkflowActivationResult
            Activated, not-enabled, or fail-closed outcome retaining exact generic
            enablement and optional selection evidence.

        Raises
        ------
        TypeError
            ``request`` is not an exact
            :class:`ColoredPetriNetWorkflowActivationRequest`.
        """
        if type(request) is not ColoredPetriNetWorkflowActivationRequest:
            raise TypeError(
                "request must be ColoredPetriNetWorkflowActivationRequest"
            )
        enablement = ColoredPetriNetTransitionEnabler().execute(
            request.definition, request.marking
        )
        if not enablement.is_success:
            return self._failure(
                request,
                enablement,
                ColoredPetriNetWorkflowActivationFailureCode.ENABLEMENT_FAILED,
            )
        mapping_failure = self._mapping_failure(request)
        if mapping_failure is not None:
            return self._failure(request, enablement, mapping_failure)

        if request.mode is ColoredPetriNetWorkflowActivationMode.DIRECT:
            intended = request.direct_binding
            assert intended is not None
            if (
                request.mapping.direct_transition_identity is None
                or intended.transition_identity
                != request.mapping.direct_transition_identity
            ):
                return self._failure(
                    request,
                    enablement,
                    ColoredPetriNetWorkflowActivationFailureCode.INVALID_WORKFLOW_MAPPING,
                )
            selected_gates: tuple[TaskGateSelection, ...] | None = None
        else:
            gate_set = request.task_instance.start_gate_set
            if gate_set is None or not gate_set.gates:
                return self._not_enabled(request, enablement)
            if gate_set.mode is TaskStartGateSetMode.ANY_OF:
                candidate = self._any_of_candidate(request, enablement)
                if candidate is None:
                    return self._not_enabled(request, enablement)
                gate, intended = candidate
                selected_gates = (TaskGateSelection(gate.identity, intended),)
            else:
                all_of = self._all_of_candidate(request, enablement)
                if all_of is None:
                    return self._not_enabled(request, enablement)
                intended, selected_gates = all_of

        assert enablement.enabled_bindings is not None
        if not self._binding_matches_result_tokens(request, intended):
            return self._failure(
                request,
                enablement,
                ColoredPetriNetWorkflowActivationFailureCode.INVALID_RESULT_TOKEN_MAPPING,
            )
        if intended not in enablement.enabled_bindings:
            return self._not_enabled(request, enablement)
        if (
            intended != enablement.enabled_bindings[0]
            and request.mapping.selection_policy
            is ColoredPetriNetWorkflowSelectionPolicy.DETERMINISTIC_ONLY
        ):
            return self._failure(
                request,
                enablement,
                ColoredPetriNetWorkflowActivationFailureCode.DIRECTED_SELECTION_PROHIBITED,
            )
        selection = self._select(request, enablement, intended)
        if selection.outcome is not ColoredPetriNetSelectionOutcomeKind.SELECTED:
            if selection.outcome in (
                ColoredPetriNetSelectionOutcomeKind.EMPTY,
                ColoredPetriNetSelectionOutcomeKind.NO_MATCH,
            ):
                return self._not_enabled(request, enablement, selection)
            failure_code = (
                ColoredPetriNetWorkflowActivationFailureCode.DIRECTED_SELECTION_PROHIBITED
                if selection.failure_code
                is ColoredPetriNetSelectionFailureCode.DIRECTED_SELECTION_PROHIBITED
                else ColoredPetriNetWorkflowActivationFailureCode.SELECTION_FAILED
            )
            return self._failure(request, enablement, failure_code, selection)
        if selection.selected_binding != intended:
            return self._failure(
                request,
                enablement,
                ColoredPetriNetWorkflowActivationFailureCode.SELECTION_CORRELATION_MISMATCH,
                selection,
            )

        activation_selection: TaskActivationSelection
        if request.mode is ColoredPetriNetWorkflowActivationMode.DIRECT:
            activation_selection = DirectTaskActivationSelection(selection.identity)
        else:
            gate_set = request.task_instance.start_gate_set
            assert gate_set is not None and selected_gates is not None
            if gate_set.mode is TaskStartGateSetMode.ANY_OF:
                activation_selection = AnyOfTaskActivationSelection(
                    gate_set.identity, selected_gates[0], selection.identity
                )
            else:
                activation_selection = AllOfTaskActivationSelection(
                    gate_set.identity, selected_gates, selection.identity
                )
        activation = TaskActivation(
            request.activation_identity,
            request.mapping.workflow_identity,
            request.workflow_run_identity,
            request.task_instance,
            request.operation_identity,
            request.attempt_identity,
            request.inputs,
            activation_selection,
        )
        return ColoredPetriNetWorkflowActivationResult(
            request,
            enablement,
            ColoredPetriNetWorkflowActivationOutcomeKind.ACTIVATED,
            selection_result=selection,
            activation=activation,
        )

    @staticmethod
    def _mapping_failure(
        request: ColoredPetriNetWorkflowActivationRequest,
    ) -> ColoredPetriNetWorkflowActivationFailureCode | None:
        """Return the first deterministic explicit-mapping defect, if any."""
        mapping = request.mapping
        if mapping.task_instance_identity != request.task_instance.identity:
            return ColoredPetriNetWorkflowActivationFailureCode.INVALID_WORKFLOW_MAPPING
        places = {
            place.place_identity: place.tokens for place in request.marking.places
        }
        for item in request.result_token_mappings:
            if item.token not in places.get(item.place_identity, ()):
                return (
                    ColoredPetriNetWorkflowActivationFailureCode.INVALID_RESULT_TOKEN_MAPPING
                )
        transitions = {
            item.identity: item for item in request.definition.transitions
        }
        transition_ids = set(transitions)
        gate_set = request.task_instance.start_gate_set
        if gate_set is not None and any(
            gate.transition_identity not in transition_ids for gate in gate_set.gates
        ):
            return ColoredPetriNetWorkflowActivationFailureCode.INVALID_GATE_MAPPING
        mapped_variables = {
            item.variable_identity for item in request.result_token_mappings
        }
        if request.mode is ColoredPetriNetWorkflowActivationMode.DIRECT:
            if (
                mapping.direct_transition_identity is None
                or mapping.direct_transition_identity not in transition_ids
            ):
                return (
                    ColoredPetriNetWorkflowActivationFailureCode.INVALID_WORKFLOW_MAPPING
                )
            if not set(
                transitions[
                    mapping.direct_transition_identity
                ].input_variable_identities
            ) <= mapped_variables:
                return (
                    ColoredPetriNetWorkflowActivationFailureCode.INVALID_RESULT_TOKEN_MAPPING
                )
        if gate_set is not None and any(
            not set(
                transitions[gate.transition_identity].input_variable_identities
            )
            <= mapped_variables
            for gate in gate_set.gates
        ):
            return (
                ColoredPetriNetWorkflowActivationFailureCode.INVALID_RESULT_TOKEN_MAPPING
            )
        if (
            request.mode is ColoredPetriNetWorkflowActivationMode.AUTOMATIC
            and gate_set is not None
            and gate_set.mode is TaskStartGateSetMode.ALL_OF
        ):
            target_identity = mapping.all_of_transition_identity
            if target_identity is None or target_identity not in transition_ids:
                return ColoredPetriNetWorkflowActivationFailureCode.INVALID_GATE_MAPPING
            member_variables = {
                variable
                for gate in gate_set.gates
                for variable in transitions[
                    gate.transition_identity
                ].input_variable_identities
            }
            if member_variables != set(
                transitions[target_identity].input_variable_identities
            ):
                return ColoredPetriNetWorkflowActivationFailureCode.INVALID_GATE_MAPPING
        return None

    @staticmethod
    def _binding_matches_result_tokens(
        request: ColoredPetriNetWorkflowActivationRequest,
        binding: ColoredPetriNetBinding,
    ) -> bool:
        """Return whether binding variables equal their mapped token values."""
        represented_values = {
            item.variable_identity: item.token.value
            for item in request.result_token_mappings
        }
        return all(
            represented_values.get(assignment.variable_identity) == assignment.value
            for assignment in binding.assignments
        )

    @staticmethod
    def _any_of_candidate(
        request: ColoredPetriNetWorkflowActivationRequest,
        enablement: ColoredPetriNetEnablementResult,
    ) -> tuple[TaskStartGate, ColoredPetriNetBinding] | None:
        """Return the canonical Workflow-priority candidate or explicit absence."""
        gate_set = request.task_instance.start_gate_set
        assert gate_set is not None
        assert enablement.enabled_bindings is not None
        for gate in gate_set.selection_order:
            for binding in enablement.enabled_bindings:
                if (
                    binding.transition_identity == gate.transition_identity
                    and ColoredPetriNetWorkflowAdapter._binding_matches_result_tokens(
                        request, binding
                    )
                ):
                    return gate, binding
        return None

    @staticmethod
    def _all_of_candidate(
        request: ColoredPetriNetWorkflowActivationRequest,
        enablement: ColoredPetriNetEnablementResult,
    ) -> tuple[ColoredPetriNetBinding, tuple[TaskGateSelection, ...]] | None:
        """Return the first compatible complete gate tuple and combined binding."""
        target_identity = request.mapping.all_of_transition_identity
        if target_identity is None:
            return None
        transitions = {
            transition.identity: transition
            for transition in request.definition.transitions
        }
        target = transitions.get(target_identity)
        if target is None:
            return None
        gate_set = request.task_instance.start_gate_set
        assert gate_set is not None
        assert enablement.enabled_bindings is not None
        candidate_groups = tuple(
            tuple(
                binding
                for binding in enablement.enabled_bindings
                if binding.transition_identity == gate.transition_identity
                and ColoredPetriNetWorkflowAdapter._binding_matches_result_tokens(
                    request, binding
                )
            )
            for gate in gate_set.selection_order
        )
        if any(not candidates for candidates in candidate_groups):
            return None
        enabled = set(enablement.enabled_bindings)
        for member_bindings in product(*candidate_groups):
            values: dict[
                ColoredPetriNetBindingVariableIdentity, ColoredPetriNetValue
            ] = {}
            compatible = True
            for binding in member_bindings:
                for assignment in binding.assignments:
                    previous = values.get(assignment.variable_identity)
                    if previous is not None and previous != assignment.value:
                        compatible = False
                        break
                    values[assignment.variable_identity] = assignment.value
                if not compatible:
                    break
            if not compatible or set(values) != set(target.input_variable_identities):
                continue
            combined = ColoredPetriNetBinding(
                target_identity,
                tuple(
                    ColoredPetriNetBindingAssignment(variable, values[variable])
                    for variable in target.input_variable_identities
                ),
            )
            if combined not in enabled:
                continue
            selections = tuple(
                TaskGateSelection(gate.identity, binding)
                for gate, binding in zip(
                    gate_set.selection_order, member_bindings, strict=True
                )
            )
            return combined, selections
        return None

    @staticmethod
    def _select(
        request: ColoredPetriNetWorkflowActivationRequest,
        enablement: ColoredPetriNetEnablementResult,
        intended: ColoredPetriNetBinding,
    ) -> ColoredPetriNetSelectionResult:
        """Select the intended binding canonically or by doubly permitted directive."""
        assert enablement.enabled_bindings is not None
        directive = None
        if (
            not enablement.enabled_bindings
            or intended != enablement.enabled_bindings[0]
        ):
            directive = ColoredPetriNetSelectionDirective(enablement.identity, intended)
        return ColoredPetriNetBindingSelector().execute(
            request.definition, enablement, directive
        )

    @staticmethod
    def _not_enabled(
        request: ColoredPetriNetWorkflowActivationRequest,
        enablement: ColoredPetriNetEnablementResult,
        selection: ColoredPetriNetSelectionResult | None = None,
    ) -> ColoredPetriNetWorkflowActivationResult:
        """Construct an expected no-activation result."""
        return ColoredPetriNetWorkflowActivationResult(
            request,
            enablement,
            ColoredPetriNetWorkflowActivationOutcomeKind.NOT_ENABLED,
            selection_result=selection,
        )

    @staticmethod
    def _failure(
        request: ColoredPetriNetWorkflowActivationRequest,
        enablement: ColoredPetriNetEnablementResult,
        code: ColoredPetriNetWorkflowActivationFailureCode,
        selection: ColoredPetriNetSelectionResult | None = None,
    ) -> ColoredPetriNetWorkflowActivationResult:
        """Construct one stable fail-closed adapter result."""
        return ColoredPetriNetWorkflowActivationResult(
            request,
            enablement,
            ColoredPetriNetWorkflowActivationOutcomeKind.FAILURE,
            selection_result=selection,
            failure_code=code,
        )
