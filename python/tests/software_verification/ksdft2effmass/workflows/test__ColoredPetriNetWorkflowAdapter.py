r"""Software verification of ``ColoredPetriNetWorkflowAdapter``.

Evidence profile: routine

Bounded artifact scope: the public ``ColoredPetriNetWorkflowAdapter`` ActionObject.

Facet and represented meaning

The adapter represents deterministic, effect-free translation from explicit
Workflow-owned activation mapping to generic colored-Petri-net enablement and
selection.

Intrinsic and cross-object scope

Tests cover direct, ``any_of``, and ``all_of`` mapping, double permission for a
directed selection, exact result-token correlation, and expected no-activation.

VVUQ and scientific exclusions

This is software verification. Selection does not invoke a Task, fire a transition,
authorize execution, validate scientific meaning, or quantify uncertainty.
"""

from dataclasses import replace

import pytest
from _cpn_adapter_fixtures import adapter_request

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetDefinition,
    ColoredPetriNetMarking,
    ColoredPetriNetPlaceMarking,
    ColoredPetriNetSelectionPolicy,
    ColoredPetriNetToken,
    ColoredPetriNetTokenIdentity,
    ColoredPetriNetValue,
    ColoredPetriNetValueKind,
)
from ksdft2effmass.workflows import (
    AllOfTaskActivationSelection,
    AnyOfTaskActivationSelection,
    ColoredPetriNetWorkflowActivationFailureCode,
    ColoredPetriNetWorkflowActivationMode,
    ColoredPetriNetWorkflowActivationOutcomeKind,
    ColoredPetriNetWorkflowAdapter,
    ColoredPetriNetWorkflowSelectionPolicy,
    DirectTaskActivationSelection,
    TaskStartGateSetMode,
)

pytestmark = pytest.mark.software_verification
SUT = ColoredPetriNetWorkflowAdapter


def test_workflow__any_of_activation__uses_workflow_gate_priority() -> None:
    """Exercise deterministic ``any_of`` selection across two enabled gates.

    Evidence ID: SV-WFA-ADAPTER-001

    Requirement: ``any_of`` selects by gate priority and identity before generic
    binding order and retains the exact directed generic selection.

    Acceptance: Gate ``gate.b`` is activated with a directive-bound selected
    ``transition.b`` binding and no Task effect is performed.
    """
    result = SUT().execute(
        adapter_request(
            ColoredPetriNetWorkflowActivationMode.AUTOMATIC,
            TaskStartGateSetMode.ANY_OF,
        )
    )

    assert result.outcome is ColoredPetriNetWorkflowActivationOutcomeKind.ACTIVATED
    assert result.selection_result is not None
    assert result.selection_result.directive is not None
    assert result.selection_result.selected_binding is not None
    assert result.selection_result.selected_binding.transition_identity.value == (
        "transition.b"
    )
    assert result.activation is not None
    assert type(result.activation.selection) is AnyOfTaskActivationSelection
    assert result.activation.selection.selected_gate.gate_identity.value == "gate.b"


def test_workflow__all_of_activation__combines_compatible_member_bindings() -> None:
    """Exercise one complete compatible ``all_of`` member tuple.

    Evidence ID: SV-WFA-ADAPTER-002

    Requirement: ``all_of`` selects one binding per canonically ordered gate, merges
    compatible assignments in the mapped activation-transition order, and performs
    one generic selection.

    Acceptance: The activation retains gates ``gate.b`` then ``gate.a`` while the
    generic result selects ``transition.all`` with ordered ``x`` and ``y`` values.
    """
    result = SUT().execute(
        adapter_request(
            ColoredPetriNetWorkflowActivationMode.AUTOMATIC,
            TaskStartGateSetMode.ALL_OF,
        )
    )

    assert result.is_activated
    assert result.activation is not None
    assert type(result.activation.selection) is AllOfTaskActivationSelection
    assert tuple(
        item.gate_identity.value
        for item in result.activation.selection.selected_gates
    ) == ("gate.b", "gate.a")
    assert result.selection_result is not None
    assert result.selection_result.selected_binding is not None
    assert result.selection_result.selected_binding.transition_identity.value == (
        "transition.all"
    )
    assert tuple(
        item.variable_identity.value
        for item in result.selection_result.selected_binding.assignments
    ) == ("x", "y")


def test_workflow__direct_activation__uses_explicit_operation_mapping() -> None:
    """Exercise caller-identified direct selection without automatic gates.

    Evidence ID: SV-WFA-ADAPTER-003

    Requirement: Direct activation uses the exact mapped transition and supplied
    binding while retaining the generic selection-result identity.

    Acceptance: The result is activated with the direct discriminant and exact
    ``transition.all`` binding.
    """
    result = SUT().execute(
        adapter_request(ColoredPetriNetWorkflowActivationMode.DIRECT, None)
    )

    assert result.is_activated
    assert result.activation is not None
    assert type(result.activation.selection) is DirectTaskActivationSelection
    assert result.selection_result is not None
    assert result.selection_result.selected_binding is not None
    assert result.selection_result.selected_binding.transition_identity.value == (
        "transition.all"
    )


def test_workflow__automatic_activation__returns_expected_not_enabled() -> None:
    """Exercise automatic activation with no represented gate policy.

    Evidence ID: SV-WFA-ADAPTER-004

    Requirement: Absence of a nonempty automatic gate policy is an expected
    not-enabled result and never becomes direct activation.

    Acceptance: The closed result is ``not_enabled`` with no selection, activation,
    or failure code.
    """
    result = SUT().execute(
        adapter_request(ColoredPetriNetWorkflowActivationMode.AUTOMATIC, None)
    )

    assert result.outcome is ColoredPetriNetWorkflowActivationOutcomeKind.NOT_ENABLED
    assert result.selection_result is None
    assert result.activation is None
    assert result.failure_code is None


def test_workflow__result_token_mapping__selects_the_correlated_value() -> None:
    """Exercise value correlation when another generic binding orders first.

    Evidence ID: SV-WFA-ADAPTER-008

    Requirement: Gate candidates must equal the explicit result-token value for every
    represented binding variable rather than selecting an unrelated canonical value.

    Acceptance: Adding a lower-valued token at ``place.b`` still selects mapped value
    ``2`` for variable ``y``.
    """
    request = adapter_request(
        ColoredPetriNetWorkflowActivationMode.AUTOMATIC,
        TaskStartGateSetMode.ANY_OF,
    )
    places = {place.place_identity.value: place for place in request.marking.places}
    place_b = places["place.b"]
    unrelated = ColoredPetriNetToken(
        place_b.tokens[0].color_identity,
        ColoredPetriNetValue(ColoredPetriNetValueKind.INTEGER, 0),
        ColoredPetriNetTokenIdentity("token.unrelated"),
    )
    expanded = ColoredPetriNetMarking(
        request.marking.identity,
        request.marking.definition_identity,
        (
            places["place.a"],
            ColoredPetriNetPlaceMarking(
                place_b.place_identity, (unrelated, *place_b.tokens)
            ),
        ),
    )

    result = SUT().execute(replace(request, marking=expanded))

    assert result.selection_result is not None
    assert result.selection_result.selected_binding is not None
    assert result.selection_result.selected_binding.assignments[0].value.value == 2


def test_workflow__directed_selection__requires_workflow_permission() -> None:
    """Exercise the Workflow-owned half of directed-selection permission.

    Evidence ID: SV-WFA-ADAPTER-005

    Requirement: A noncanonical intended binding requires explicit Workflow mapping
    permission even when the generic definition permits a directive.

    Acceptance: Deterministic-only Workflow policy returns the stable directed-
    selection-prohibited failure without constructing an activation.
    """
    request = adapter_request(
        ColoredPetriNetWorkflowActivationMode.AUTOMATIC,
        TaskStartGateSetMode.ANY_OF,
        workflow_policy=ColoredPetriNetWorkflowSelectionPolicy.DETERMINISTIC_ONLY,
    )
    result = SUT().execute(request)

    assert result.outcome is ColoredPetriNetWorkflowActivationOutcomeKind.FAILURE
    assert result.failure_code is (
        ColoredPetriNetWorkflowActivationFailureCode.DIRECTED_SELECTION_PROHIBITED
    )
    assert result.activation is None


def test_workflow__directed_selection__requires_generic_permission() -> None:
    """Exercise the generic-definition half of directed-selection permission.

    Evidence ID: SV-WFA-ADAPTER-006

    Requirement: Workflow permission cannot override a generic definition that
    prohibits directed selection.

    Acceptance: The adapter retains generic selection failure and returns the stable
    directed-selection-prohibited adapter failure.
    """
    request = adapter_request(
        ColoredPetriNetWorkflowActivationMode.AUTOMATIC,
        TaskStartGateSetMode.ANY_OF,
    )
    definition = ColoredPetriNetDefinition(
        request.definition.identity,
        request.definition.colors,
        request.definition.places,
        request.definition.transitions,
        request.definition.arcs,
        request.definition.transition_priority,
        ColoredPetriNetSelectionPolicy.DETERMINISTIC_ONLY,
    )
    result = SUT().execute(replace(request, definition=definition))

    assert result.outcome is ColoredPetriNetWorkflowActivationOutcomeKind.FAILURE
    assert result.failure_code is (
        ColoredPetriNetWorkflowActivationFailureCode.DIRECTED_SELECTION_PROHIBITED
    )
    assert result.selection_result is not None
    assert result.selection_result.failure_code is not None


def test_workflow__result_token_mapping__fails_closed_when_token_is_absent() -> None:
    """Exercise exact Workflow-result to predecessor-token correlation.

    Evidence ID: SV-WFA-ADAPTER-007

    Requirement: Every explicitly mapped identified token must occur at its exact
    mapped place in the supplied predecessor marking.

    Acceptance: Removing mapped tokens yields ``invalid_result_token_mapping`` and
    no activation while generic enablement remains a closed successful result.
    """
    request = adapter_request(
        ColoredPetriNetWorkflowActivationMode.AUTOMATIC,
        TaskStartGateSetMode.ANY_OF,
    )
    empty_marking = ColoredPetriNetMarking(
        request.marking.identity,
        request.marking.definition_identity,
        tuple(
            ColoredPetriNetPlaceMarking(place.place_identity, ())
            for place in request.marking.places
        ),
    )
    result = SUT().execute(replace(request, marking=empty_marking))

    assert result.outcome is ColoredPetriNetWorkflowActivationOutcomeKind.FAILURE
    assert result.failure_code is (
        ColoredPetriNetWorkflowActivationFailureCode.INVALID_RESULT_TOKEN_MAPPING
    )
    assert result.enablement_result.is_success
    assert result.activation is None
