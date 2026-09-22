"""Private synthetic constructors supporting Workflow CPN-adapter evidence."""

from dataclasses import dataclass

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetArcDefinition,
    ColoredPetriNetArcIdentity,
    ColoredPetriNetBinding,
    ColoredPetriNetBindingAssignment,
    ColoredPetriNetBindingVariableIdentity,
    ColoredPetriNetColorDefinition,
    ColoredPetriNetColorIdentity,
    ColoredPetriNetDefinition,
    ColoredPetriNetDefinitionIdentity,
    ColoredPetriNetGuardExpression,
    ColoredPetriNetGuardOperator,
    ColoredPetriNetInputInscription,
    ColoredPetriNetInputMode,
    ColoredPetriNetMarking,
    ColoredPetriNetMarkingIdentity,
    ColoredPetriNetPlaceDefinition,
    ColoredPetriNetPlaceIdentity,
    ColoredPetriNetPlaceMarking,
    ColoredPetriNetSelectionPolicy,
    ColoredPetriNetToken,
    ColoredPetriNetTokenIdentity,
    ColoredPetriNetTokenPattern,
    ColoredPetriNetTransitionDefinition,
    ColoredPetriNetTransitionIdentity,
    ColoredPetriNetValue,
    ColoredPetriNetValueKind,
)
from ksdft2effmass.workflows import (
    AttemptIdentity,
    ColoredPetriNetWorkflowActivationMode,
    ColoredPetriNetWorkflowActivationRequest,
    ColoredPetriNetWorkflowMapping,
    ColoredPetriNetWorkflowSelectionPolicy,
    OperationIdentity,
    ResultObjectIdentity,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskInputBinding,
    TaskInstance,
    TaskInstanceIdentity,
    TaskStartGate,
    TaskStartGateIdentity,
    TaskStartGateSet,
    TaskStartGateSetIdentity,
    TaskStartGateSetMode,
    WorkflowIdentity,
    WorkflowResultTokenMapping,
    WorkflowRunIdentity,
)


@dataclass(frozen=True, slots=True)
class SyntheticResult:
    """Synthetic test result carrying only its required Workflow identity."""

    identity: ResultObjectIdentity


def adapter_definition() -> ColoredPetriNetDefinition:
    """Return a valid net with two member transitions and one combined transition."""
    color = ColoredPetriNetColorDefinition(
        ColoredPetriNetColorIdentity("integer"),
        (ColoredPetriNetValueKind.INTEGER,),
    )
    place_a = ColoredPetriNetPlaceDefinition(
        ColoredPetriNetPlaceIdentity("place.a"), (color.identity,)
    )
    place_b = ColoredPetriNetPlaceDefinition(
        ColoredPetriNetPlaceIdentity("place.b"), (color.identity,)
    )
    variable_x = ColoredPetriNetBindingVariableIdentity("x")
    variable_y = ColoredPetriNetBindingVariableIdentity("y")
    transition_a = ColoredPetriNetTransitionDefinition(
        ColoredPetriNetTransitionIdentity("transition.a"),
        (variable_x,),
        (),
        ColoredPetriNetGuardExpression(ColoredPetriNetGuardOperator.TRUE),
    )
    transition_b = ColoredPetriNetTransitionDefinition(
        ColoredPetriNetTransitionIdentity("transition.b"),
        (variable_y,),
        (),
        ColoredPetriNetGuardExpression(ColoredPetriNetGuardOperator.TRUE),
    )
    transition_all = ColoredPetriNetTransitionDefinition(
        ColoredPetriNetTransitionIdentity("transition.all"),
        (variable_x, variable_y),
        (),
        ColoredPetriNetGuardExpression(ColoredPetriNetGuardOperator.TRUE),
    )

    def input_arc(
        name: str,
        place: ColoredPetriNetPlaceDefinition,
        transition: ColoredPetriNetTransitionDefinition,
        variable: ColoredPetriNetBindingVariableIdentity,
    ) -> ColoredPetriNetArcDefinition:
        """Build one consuming input arc for the synthetic definition."""
        return ColoredPetriNetArcDefinition(
            ColoredPetriNetArcIdentity(name),
            place.identity,
            transition.identity,
            ColoredPetriNetInputInscription(
                ColoredPetriNetInputMode.CONSUME,
                (ColoredPetriNetTokenPattern(variable, (color.identity,)),),
            ),
        )

    arcs = (
        input_arc("arc.a", place_a, transition_a, variable_x),
        input_arc("arc.b", place_b, transition_b, variable_y),
        input_arc("arc.all.x", place_a, transition_all, variable_x),
        input_arc("arc.all.y", place_b, transition_all, variable_y),
    )
    return ColoredPetriNetDefinition(
        ColoredPetriNetDefinitionIdentity("definition.adapter"),
        (color,),
        (place_a, place_b),
        (transition_a, transition_b, transition_all),
        arcs,
        (transition_a.identity, transition_b.identity, transition_all.identity),
        ColoredPetriNetSelectionPolicy.DIRECTED_ALLOWED,
    )


def adapter_marking(
    definition: ColoredPetriNetDefinition,
) -> ColoredPetriNetMarking:
    """Return one complete marking with two individually identified input tokens."""
    color = definition.colors[0].identity
    token_a = ColoredPetriNetToken(
        color,
        ColoredPetriNetValue(ColoredPetriNetValueKind.INTEGER, 1),
        ColoredPetriNetTokenIdentity("token.a"),
    )
    token_b = ColoredPetriNetToken(
        color,
        ColoredPetriNetValue(ColoredPetriNetValueKind.INTEGER, 2),
        ColoredPetriNetTokenIdentity("token.b"),
    )
    places = {place.identity.value: place.identity for place in definition.places}
    return ColoredPetriNetMarking(
        ColoredPetriNetMarkingIdentity("marking.adapter"),
        definition.identity,
        (
            ColoredPetriNetPlaceMarking(places["place.a"], (token_a,)),
            ColoredPetriNetPlaceMarking(places["place.b"], (token_b,)),
        ),
    )


def adapter_request(
    mode: ColoredPetriNetWorkflowActivationMode,
    gate_mode: TaskStartGateSetMode | None,
    *,
    workflow_policy: ColoredPetriNetWorkflowSelectionPolicy = (
        ColoredPetriNetWorkflowSelectionPolicy.DIRECTED_ALLOWED
    ),
) -> ColoredPetriNetWorkflowActivationRequest:
    """Return an exact synthetic direct or automatic adapter request."""
    definition = adapter_definition()
    marking = adapter_marking(definition)
    transitions = {
        transition.identity.value: transition.identity
        for transition in definition.transitions
    }
    gate_set = None
    if gate_mode is not None:
        gate_set = TaskStartGateSet(
            TaskStartGateSetIdentity("gate-set"),
            gate_mode,
            (
                TaskStartGate(
                    TaskStartGateIdentity("gate.b"), 0, transitions["transition.b"]
                ),
                TaskStartGate(
                    TaskStartGateIdentity("gate.a"), 1, transitions["transition.a"]
                ),
            ),
        )
    task_instance = TaskInstance(
        TaskInstanceIdentity("task-instance"),
        TaskDefinitionIdentity("task-definition"),
        gate_set,
    )
    workflow_identity = WorkflowIdentity("workflow")
    mapping = ColoredPetriNetWorkflowMapping(
        workflow_identity,
        task_instance.identity,
        workflow_policy,
        direct_transition_identity=transitions["transition.all"],
        all_of_transition_identity=transitions["transition.all"],
    )
    result_a = SyntheticResult(ResultObjectIdentity("result.a"))
    result_b = SyntheticResult(ResultObjectIdentity("result.b"))
    inputs = (TaskInputBinding("a", result_a), TaskInputBinding("b", result_b))
    places = {place.place_identity.value: place for place in marking.places}
    result_tokens = (
        WorkflowResultTokenMapping(
            "a",
            result_a.identity,
            ColoredPetriNetBindingVariableIdentity("x"),
            places["place.a"].place_identity,
            places["place.a"].tokens[0],
        ),
        WorkflowResultTokenMapping(
            "b",
            result_b.identity,
            ColoredPetriNetBindingVariableIdentity("y"),
            places["place.b"].place_identity,
            places["place.b"].tokens[0],
        ),
    )
    direct_binding = None
    if mode is ColoredPetriNetWorkflowActivationMode.DIRECT:
        direct_binding = ColoredPetriNetBinding(
            transitions["transition.all"],
            (
                ColoredPetriNetBindingAssignment(
                    ColoredPetriNetBindingVariableIdentity("x"),
                    places["place.a"].tokens[0].value,
                ),
                ColoredPetriNetBindingAssignment(
                    ColoredPetriNetBindingVariableIdentity("y"),
                    places["place.b"].tokens[0].value,
                ),
            ),
        )
    return ColoredPetriNetWorkflowActivationRequest(
        mapping,
        definition,
        marking,
        WorkflowRunIdentity("workflow-run"),
        task_instance,
        TaskActivationIdentity("activation"),
        OperationIdentity("operation"),
        AttemptIdentity("attempt"),
        inputs,
        result_tokens,
        mode,
        direct_binding,
    )
