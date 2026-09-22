"""Bounded petrinet values in the WorkflowRun wire representation."""

from __future__ import annotations

from ksdft2effmass.petrinet.colored.definitions import (
    ColoredPetriNetArcDefinition,
    ColoredPetriNetArcIdentity,
    ColoredPetriNetColorDefinition,
    ColoredPetriNetDefinition,
    ColoredPetriNetPlaceDefinition,
    ColoredPetriNetSelectionPolicy,
    ColoredPetriNetTransitionDefinition,
)
from ksdft2effmass.petrinet.colored.enablement import (
    ColoredPetriNetEnablementFailure,
    ColoredPetriNetEnablementFailureCode,
    ColoredPetriNetEnablementFailureIdentity,
    ColoredPetriNetEnablementResult,
    ColoredPetriNetEnablementResultIdentity,
    ColoredPetriNetExpressionEvaluatorIdentity,
    ColoredPetriNetOrderingPolicyIdentity,
    ColoredPetriNetTransitionEnablerIdentity,
)
from ksdft2effmass.petrinet.colored.expressions import (
    ColoredPetriNetGuardExpression,
    ColoredPetriNetGuardOperator,
    ColoredPetriNetInhibitorPattern,
    ColoredPetriNetInputInscription,
    ColoredPetriNetInputMode,
    ColoredPetriNetOutputInscription,
    ColoredPetriNetTokenPattern,
    ColoredPetriNetTokenTemplate,
    ColoredPetriNetValueExpression,
    ColoredPetriNetValueExpressionKind,
)
from ksdft2effmass.petrinet.colored.firing import (
    ColoredPetriNetFiringAudit,
    ColoredPetriNetFiringFailure,
    ColoredPetriNetFiringFailureCode,
    ColoredPetriNetFiringFailureIdentity,
    ColoredPetriNetFiringInput,
    ColoredPetriNetFiringOutcomeKind,
    ColoredPetriNetFiringResult,
    ColoredPetriNetFiringResultIdentity,
    ColoredPetriNetInhibitorEvaluation,
    ColoredPetriNetProducedToken,
    ColoredPetriNetTokenOccurrence,
    ColoredPetriNetTransitionFirerIdentity,
)
from ksdft2effmass.petrinet.colored.markings import (
    ColoredPetriNetBinding,
    ColoredPetriNetBindingAssignment,
    ColoredPetriNetBindingVariableIdentity,
    ColoredPetriNetDefinitionIdentity,
    ColoredPetriNetMarking,
    ColoredPetriNetMarkingIdentity,
    ColoredPetriNetPlaceIdentity,
    ColoredPetriNetPlaceMarking,
    ColoredPetriNetTransitionIdentity,
)
from ksdft2effmass.petrinet.colored.selection import (
    ColoredPetriNetBindingSelectorIdentity,
    ColoredPetriNetSelectionDirective,
    ColoredPetriNetSelectionDirectiveIdentity,
    ColoredPetriNetSelectionFailureCode,
    ColoredPetriNetSelectionOutcomeKind,
    ColoredPetriNetSelectionResult,
    ColoredPetriNetSelectionResultIdentity,
)
from ksdft2effmass.petrinet.colored.validation import (
    ColoredPetriNetValidationIssue,
    ColoredPetriNetValidationIssueCode,
)
from ksdft2effmass.petrinet.colored.values import (
    ColoredPetriNetColorIdentity,
    ColoredPetriNetToken,
    ColoredPetriNetTokenIdentity,
    ColoredPetriNetValue,
    ColoredPetriNetValueKind,
)

from ..records import (
    WorkflowEncodedResultValue,
    WorkflowPersistenceFailureCode,
)
from ._base import (
    _ResultJson,
    _RunValue,
    _WorkflowRunWireSerializer,
    _WorkflowRunWireUnsupported,
)


class _WorkflowRunPetrinetWireSerializer(_WorkflowRunWireSerializer):
    """Encode and decode the closed petrinet value family."""

    def _encode_petrinet(
        self, value: _RunValue, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _ResultJson:
        if type(value) is ColoredPetriNetEnablementFailureCode:
            return self._record(
                "ColoredPetriNetEnablementFailureCode", {"value": value.value}
            )
        if type(value) is ColoredPetriNetFiringFailureCode:
            return self._record(
                "ColoredPetriNetFiringFailureCode", {"value": value.value}
            )
        if type(value) is ColoredPetriNetFiringOutcomeKind:
            return self._record(
                "ColoredPetriNetFiringOutcomeKind", {"value": value.value}
            )
        if type(value) is ColoredPetriNetGuardOperator:
            return self._record("ColoredPetriNetGuardOperator", {"value": value.value})
        if type(value) is ColoredPetriNetInputMode:
            return self._record("ColoredPetriNetInputMode", {"value": value.value})
        if type(value) is ColoredPetriNetSelectionFailureCode:
            return self._record(
                "ColoredPetriNetSelectionFailureCode", {"value": value.value}
            )
        if type(value) is ColoredPetriNetSelectionOutcomeKind:
            return self._record(
                "ColoredPetriNetSelectionOutcomeKind", {"value": value.value}
            )
        if type(value) is ColoredPetriNetSelectionPolicy:
            return self._record(
                "ColoredPetriNetSelectionPolicy", {"value": value.value}
            )
        if type(value) is ColoredPetriNetValidationIssueCode:
            return self._record(
                "ColoredPetriNetValidationIssueCode", {"value": value.value}
            )
        if type(value) is ColoredPetriNetValueExpressionKind:
            return self._record(
                "ColoredPetriNetValueExpressionKind", {"value": value.value}
            )
        if type(value) is ColoredPetriNetValueKind:
            return self._record("ColoredPetriNetValueKind", {"value": value.value})
        if type(value) is ColoredPetriNetArcDefinition:
            return self._record(
                "ColoredPetriNetArcDefinition",
                {
                    "identity": self._encode(value.identity, seen),
                    "place_identity": self._encode(value.place_identity, seen),
                    "transition_identity": self._encode(
                        value.transition_identity, seen
                    ),
                    "input_inscription": self._encode(value.input_inscription, seen),
                    "output_inscription": self._encode(value.output_inscription, seen),
                },
            )
        if type(value) is ColoredPetriNetArcIdentity:
            return self._record(
                "ColoredPetriNetArcIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetBinding:
            return self._record(
                "ColoredPetriNetBinding",
                {
                    "transition_identity": self._encode(
                        value.transition_identity, seen
                    ),
                    "assignments": self._encode(value.assignments, seen),
                },
            )
        if type(value) is ColoredPetriNetBindingAssignment:
            return self._record(
                "ColoredPetriNetBindingAssignment",
                {
                    "variable_identity": self._encode(value.variable_identity, seen),
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetBindingSelectorIdentity:
            return self._record(
                "ColoredPetriNetBindingSelectorIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetBindingVariableIdentity:
            return self._record(
                "ColoredPetriNetBindingVariableIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetColorDefinition:
            return self._record(
                "ColoredPetriNetColorDefinition",
                {
                    "identity": self._encode(value.identity, seen),
                    "allowed_value_kinds": self._encode(
                        value.allowed_value_kinds, seen
                    ),
                },
            )
        if type(value) is ColoredPetriNetColorIdentity:
            return self._record(
                "ColoredPetriNetColorIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetDefinition:
            return self._record(
                "ColoredPetriNetDefinition",
                {
                    "identity": self._encode(value.identity, seen),
                    "colors": self._encode(value.colors, seen),
                    "places": self._encode(value.places, seen),
                    "transitions": self._encode(value.transitions, seen),
                    "arcs": self._encode(value.arcs, seen),
                    "transition_priority": self._encode(
                        value.transition_priority, seen
                    ),
                    "selection_policy": self._encode(value.selection_policy, seen),
                },
            )
        if type(value) is ColoredPetriNetDefinitionIdentity:
            return self._record(
                "ColoredPetriNetDefinitionIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetEnablementFailure:
            return self._record(
                "ColoredPetriNetEnablementFailure",
                {
                    "identity": self._encode(value.identity, seen),
                    "code": self._encode(value.code, seen),
                    "operation_phase": self._encode(value.operation_phase, seen),
                    "expected_condition": self._encode(value.expected_condition, seen),
                    "observed_condition": self._encode(value.observed_condition, seen),
                    "diagnostic": self._encode(value.diagnostic, seen),
                    "validation_issues": self._encode(value.validation_issues, seen),
                    "claim_boundary": self._encode(value.claim_boundary, seen),
                },
            )
        if type(value) is ColoredPetriNetEnablementFailureIdentity:
            return self._record(
                "ColoredPetriNetEnablementFailureIdentity",
                {
                    "result_identity": self._encode(value.result_identity, seen),
                },
            )
        if type(value) is ColoredPetriNetEnablementResult:
            return self._record(
                "ColoredPetriNetEnablementResult",
                {
                    "identity": self._encode(value.identity, seen),
                    "definition_identity": self._encode(
                        value.definition_identity, seen
                    ),
                    "selection_policy": self._encode(value.selection_policy, seen),
                    "marking_identity": self._encode(value.marking_identity, seen),
                    "expression_evaluator_identity": self._encode(
                        value.expression_evaluator_identity, seen
                    ),
                    "ordering_policy_identity": self._encode(
                        value.ordering_policy_identity, seen
                    ),
                    "transition_enabler_identity": self._encode(
                        value.transition_enabler_identity, seen
                    ),
                    "enabled_bindings": self._encode(value.enabled_bindings, seen),
                    "failure": self._encode(value.failure, seen),
                },
            )
        if type(value) is ColoredPetriNetEnablementResultIdentity:
            return self._record(
                "ColoredPetriNetEnablementResultIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetExpressionEvaluatorIdentity:
            return self._record(
                "ColoredPetriNetExpressionEvaluatorIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetFiringAudit:
            return self._record(
                "ColoredPetriNetFiringAudit",
                {
                    "consumed_occurrences": self._encode(
                        value.consumed_occurrences, seen
                    ),
                    "read_occurrences": self._encode(value.read_occurrences, seen),
                    "inhibitor_evaluations": self._encode(
                        value.inhibitor_evaluations, seen
                    ),
                    "produced_tokens": self._encode(value.produced_tokens, seen),
                    "firer_identity": self._encode(value.firer_identity, seen),
                },
            )
        if type(value) is ColoredPetriNetFiringFailure:
            return self._record(
                "ColoredPetriNetFiringFailure",
                {
                    "identity": self._encode(value.identity, seen),
                    "code": self._encode(value.code, seen),
                    "operation_phase": self._encode(value.operation_phase, seen),
                    "expected_condition": self._encode(value.expected_condition, seen),
                    "observed_condition": self._encode(value.observed_condition, seen),
                    "diagnostic": self._encode(value.diagnostic, seen),
                    "validation_issues": self._encode(value.validation_issues, seen),
                    "claim_boundary": self._encode(value.claim_boundary, seen),
                },
            )
        if type(value) is ColoredPetriNetFiringFailureIdentity:
            return self._record(
                "ColoredPetriNetFiringFailureIdentity",
                {
                    "result_identity": self._encode(value.result_identity, seen),
                },
            )
        if type(value) is ColoredPetriNetFiringInput:
            return self._record(
                "ColoredPetriNetFiringInput",
                {
                    "definition": self._encode(value.definition, seen),
                    "transition_identity": self._encode(
                        value.transition_identity, seen
                    ),
                    "predecessor_marking": self._encode(
                        value.predecessor_marking, seen
                    ),
                    "enablement_result": self._encode(value.enablement_result, seen),
                    "selection_result": self._encode(value.selection_result, seen),
                    "selected_binding": self._encode(value.selected_binding, seen),
                    "directive_identity": self._encode(value.directive_identity, seen),
                    "external_output_binding": self._encode(
                        value.external_output_binding, seen
                    ),
                },
            )
        if type(value) is ColoredPetriNetFiringResult:
            return self._record(
                "ColoredPetriNetFiringResult",
                {
                    "identity": self._encode(value.identity, seen),
                    "firing_input": self._encode(value.firing_input, seen),
                    "outcome": self._encode(value.outcome, seen),
                    "successor_marking": self._encode(value.successor_marking, seen),
                    "audit": self._encode(value.audit, seen),
                    "failure": self._encode(value.failure, seen),
                },
            )
        if type(value) is ColoredPetriNetFiringResultIdentity:
            return self._record(
                "ColoredPetriNetFiringResultIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetGuardExpression:
            return self._record(
                "ColoredPetriNetGuardExpression",
                {
                    "operator": self._encode(value.operator, seen),
                    "operands": self._encode(value.operands, seen),
                    "left": self._encode(value.left, seen),
                    "right": self._encode(value.right, seen),
                },
            )
        if type(value) is ColoredPetriNetInhibitorEvaluation:
            return self._record(
                "ColoredPetriNetInhibitorEvaluation",
                {
                    "arc_identity": self._encode(value.arc_identity, seen),
                    "place_identity": self._encode(value.place_identity, seen),
                    "pattern_index": self._encode(value.pattern_index, seen),
                    "matching_count": self._encode(value.matching_count, seen),
                },
            )
        if type(value) is ColoredPetriNetInhibitorPattern:
            return self._record(
                "ColoredPetriNetInhibitorPattern",
                {
                    "allowed_color_identities": self._encode(
                        value.allowed_color_identities, seen
                    ),
                },
            )
        if type(value) is ColoredPetriNetInputInscription:
            return self._record(
                "ColoredPetriNetInputInscription",
                {
                    "mode": self._encode(value.mode, seen),
                    "patterns": self._encode(value.patterns, seen),
                },
            )
        if type(value) is ColoredPetriNetMarking:
            return self._record(
                "ColoredPetriNetMarking",
                {
                    "identity": self._encode(value.identity, seen),
                    "definition_identity": self._encode(
                        value.definition_identity, seen
                    ),
                    "places": self._encode(value.places, seen),
                },
            )
        if type(value) is ColoredPetriNetMarkingIdentity:
            return self._record(
                "ColoredPetriNetMarkingIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetOrderingPolicyIdentity:
            return self._record(
                "ColoredPetriNetOrderingPolicyIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetOutputInscription:
            return self._record(
                "ColoredPetriNetOutputInscription",
                {
                    "templates": self._encode(value.templates, seen),
                },
            )
        if type(value) is ColoredPetriNetPlaceDefinition:
            return self._record(
                "ColoredPetriNetPlaceDefinition",
                {
                    "identity": self._encode(value.identity, seen),
                    "allowed_color_identities": self._encode(
                        value.allowed_color_identities, seen
                    ),
                },
            )
        if type(value) is ColoredPetriNetPlaceIdentity:
            return self._record(
                "ColoredPetriNetPlaceIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetPlaceMarking:
            return self._record(
                "ColoredPetriNetPlaceMarking",
                {
                    "place_identity": self._encode(value.place_identity, seen),
                    "tokens": self._encode(value.tokens, seen),
                },
            )
        if type(value) is ColoredPetriNetProducedToken:
            return self._record(
                "ColoredPetriNetProducedToken",
                {
                    "arc_identity": self._encode(value.arc_identity, seen),
                    "place_identity": self._encode(value.place_identity, seen),
                    "template_index": self._encode(value.template_index, seen),
                    "token": self._encode(value.token, seen),
                },
            )
        if type(value) is ColoredPetriNetSelectionDirective:
            return self._record(
                "ColoredPetriNetSelectionDirective",
                {
                    "enablement_result_identity": self._encode(
                        value.enablement_result_identity, seen
                    ),
                    "binding": self._encode(value.binding, seen),
                    "identity": self._encode(value.identity, seen),
                },
            )
        if type(value) is ColoredPetriNetSelectionDirectiveIdentity:
            return self._record(
                "ColoredPetriNetSelectionDirectiveIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetSelectionResult:
            return self._record(
                "ColoredPetriNetSelectionResult",
                {
                    "enablement_result_identity": self._encode(
                        value.enablement_result_identity, seen
                    ),
                    "selector_identity": self._encode(value.selector_identity, seen),
                    "ordering_policy_identity": self._encode(
                        value.ordering_policy_identity, seen
                    ),
                    "outcome": self._encode(value.outcome, seen),
                    "selected_binding": self._encode(value.selected_binding, seen),
                    "directive": self._encode(value.directive, seen),
                    "failure_code": self._encode(value.failure_code, seen),
                    "identity": self._encode(value.identity, seen),
                },
            )
        if type(value) is ColoredPetriNetSelectionResultIdentity:
            return self._record(
                "ColoredPetriNetSelectionResultIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetToken:
            return self._record(
                "ColoredPetriNetToken",
                {
                    "color_identity": self._encode(value.color_identity, seen),
                    "value": self._encode(value.value, seen),
                    "token_identity": self._encode(value.token_identity, seen),
                },
            )
        if type(value) is ColoredPetriNetTokenIdentity:
            return self._record(
                "ColoredPetriNetTokenIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetTokenOccurrence:
            return self._record(
                "ColoredPetriNetTokenOccurrence",
                {
                    "arc_identity": self._encode(value.arc_identity, seen),
                    "place_identity": self._encode(value.place_identity, seen),
                    "pattern_index": self._encode(value.pattern_index, seen),
                    "occurrence_ordinal": self._encode(value.occurrence_ordinal, seen),
                    "token": self._encode(value.token, seen),
                },
            )
        if type(value) is ColoredPetriNetTokenPattern:
            return self._record(
                "ColoredPetriNetTokenPattern",
                {
                    "variable_identity": self._encode(value.variable_identity, seen),
                    "allowed_color_identities": self._encode(
                        value.allowed_color_identities, seen
                    ),
                },
            )
        if type(value) is ColoredPetriNetTokenTemplate:
            return self._record(
                "ColoredPetriNetTokenTemplate",
                {
                    "color_identity": self._encode(value.color_identity, seen),
                    "value_expression": self._encode(value.value_expression, seen),
                    "token_identity_expression": self._encode(
                        value.token_identity_expression, seen
                    ),
                },
            )
        if type(value) is ColoredPetriNetTransitionDefinition:
            return self._record(
                "ColoredPetriNetTransitionDefinition",
                {
                    "identity": self._encode(value.identity, seen),
                    "input_variable_identities": self._encode(
                        value.input_variable_identities, seen
                    ),
                    "external_output_variable_identities": self._encode(
                        value.external_output_variable_identities, seen
                    ),
                    "guard": self._encode(value.guard, seen),
                },
            )
        if type(value) is ColoredPetriNetTransitionEnablerIdentity:
            return self._record(
                "ColoredPetriNetTransitionEnablerIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetTransitionFirerIdentity:
            return self._record(
                "ColoredPetriNetTransitionFirerIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetTransitionIdentity:
            return self._record(
                "ColoredPetriNetTransitionIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetValidationIssue:
            return self._record(
                "ColoredPetriNetValidationIssue",
                {
                    "code": self._encode(value.code, seen),
                    "path": self._encode(value.path, seen),
                    "related_identities": self._encode(value.related_identities, seen),
                    "message": self._encode(value.message, seen),
                },
            )
        if type(value) is ColoredPetriNetValue:
            return self._record(
                "ColoredPetriNetValue",
                {
                    "kind": self._encode(value.kind, seen),
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetValueExpression:
            return self._record(
                "ColoredPetriNetValueExpression",
                {
                    "kind": self._encode(value.kind, seen),
                    "literal": self._encode(value.literal, seen),
                    "variable_identity": self._encode(value.variable_identity, seen),
                },
            )
        raise _WorkflowRunWireUnsupported

    def _decode_petrinet(
        self, tag: str, wire: _ResultJson, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _RunValue:
        record: _RunValue
        if tag == "ColoredPetriNetEnablementFailureCode":
            return ColoredPetriNetEnablementFailureCode(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetFiringFailureCode":
            return ColoredPetriNetFiringFailureCode(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetFiringOutcomeKind":
            return ColoredPetriNetFiringOutcomeKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetGuardOperator":
            return ColoredPetriNetGuardOperator(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetInputMode":
            return ColoredPetriNetInputMode(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetSelectionFailureCode":
            return ColoredPetriNetSelectionFailureCode(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetSelectionOutcomeKind":
            return ColoredPetriNetSelectionOutcomeKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetSelectionPolicy":
            return ColoredPetriNetSelectionPolicy(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetValidationIssueCode":
            return ColoredPetriNetValidationIssueCode(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetValueExpressionKind":
            return ColoredPetriNetValueExpressionKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetValueKind":
            return ColoredPetriNetValueKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetArcDefinition":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "place_identity",
                    "transition_identity",
                    "input_inscription",
                    "output_inscription",
                ),
            )
            record = ColoredPetriNetArcDefinition(
                identity=self._exact(
                    self._decode(fields["identity"], seen), ColoredPetriNetArcIdentity
                ),
                place_identity=self._exact(
                    self._decode(fields["place_identity"], seen),
                    ColoredPetriNetPlaceIdentity,
                ),
                transition_identity=self._exact(
                    self._decode(fields["transition_identity"], seen),
                    ColoredPetriNetTransitionIdentity,
                ),
                input_inscription=self._parse_ColoredPetriNetArcDefinition_input_inscription(
                    self._decode(fields["input_inscription"], seen)
                ),
                output_inscription=self._parse_ColoredPetriNetArcDefinition_output_inscription(
                    self._decode(fields["output_inscription"], seen)
                ),
            )
            return record
        if tag == "ColoredPetriNetArcIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetArcIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetBinding":
            fields = self._fields(wire, tag, ("transition_identity", "assignments"))
            record = ColoredPetriNetBinding(
                transition_identity=self._exact(
                    self._decode(fields["transition_identity"], seen),
                    ColoredPetriNetTransitionIdentity,
                ),
                assignments=tuple(
                    self._exact(item, ColoredPetriNetBindingAssignment)
                    for item in self._items(self._decode(fields["assignments"], seen))
                ),
            )
            return record
        if tag == "ColoredPetriNetBindingAssignment":
            fields = self._fields(wire, tag, ("variable_identity", "value"))
            record = ColoredPetriNetBindingAssignment(
                variable_identity=self._exact(
                    self._decode(fields["variable_identity"], seen),
                    ColoredPetriNetBindingVariableIdentity,
                ),
                value=self._exact(
                    self._decode(fields["value"], seen), ColoredPetriNetValue
                ),
            )
            return record
        if tag == "ColoredPetriNetBindingSelectorIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetBindingSelectorIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetBindingVariableIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetBindingVariableIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetColorDefinition":
            fields = self._fields(wire, tag, ("identity", "allowed_value_kinds"))
            record = ColoredPetriNetColorDefinition(
                identity=self._exact(
                    self._decode(fields["identity"], seen), ColoredPetriNetColorIdentity
                ),
                allowed_value_kinds=tuple(
                    self._exact(item, ColoredPetriNetValueKind)
                    for item in self._items(
                        self._decode(fields["allowed_value_kinds"], seen)
                    )
                ),
            )
            return record
        if tag == "ColoredPetriNetColorIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetColorIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetDefinition":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "colors",
                    "places",
                    "transitions",
                    "arcs",
                    "transition_priority",
                    "selection_policy",
                ),
            )
            record = ColoredPetriNetDefinition(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ColoredPetriNetDefinitionIdentity,
                ),
                colors=tuple(
                    self._exact(item, ColoredPetriNetColorDefinition)
                    for item in self._items(self._decode(fields["colors"], seen))
                ),
                places=tuple(
                    self._exact(item, ColoredPetriNetPlaceDefinition)
                    for item in self._items(self._decode(fields["places"], seen))
                ),
                transitions=tuple(
                    self._exact(item, ColoredPetriNetTransitionDefinition)
                    for item in self._items(self._decode(fields["transitions"], seen))
                ),
                arcs=tuple(
                    self._exact(item, ColoredPetriNetArcDefinition)
                    for item in self._items(self._decode(fields["arcs"], seen))
                ),
                transition_priority=tuple(
                    self._exact(item, ColoredPetriNetTransitionIdentity)
                    for item in self._items(
                        self._decode(fields["transition_priority"], seen)
                    )
                ),
                selection_policy=self._exact(
                    self._decode(fields["selection_policy"], seen),
                    ColoredPetriNetSelectionPolicy,
                ),
            )
            return record
        if tag == "ColoredPetriNetDefinitionIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetDefinitionIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetEnablementFailure":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "code",
                    "operation_phase",
                    "expected_condition",
                    "observed_condition",
                    "diagnostic",
                    "validation_issues",
                    "claim_boundary",
                ),
            )
            record = ColoredPetriNetEnablementFailure(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ColoredPetriNetEnablementFailureIdentity,
                ),
                code=self._exact(
                    self._decode(fields["code"], seen),
                    ColoredPetriNetEnablementFailureCode,
                ),
                operation_phase=self._exact(
                    self._decode(fields["operation_phase"], seen), str
                ),
                expected_condition=self._exact(
                    self._decode(fields["expected_condition"], seen), str
                ),
                observed_condition=self._exact(
                    self._decode(fields["observed_condition"], seen), str
                ),
                diagnostic=self._exact(self._decode(fields["diagnostic"], seen), str),
                validation_issues=tuple(
                    self._exact(item, ColoredPetriNetValidationIssue)
                    for item in self._items(
                        self._decode(fields["validation_issues"], seen)
                    )
                ),
                claim_boundary=tuple(
                    self._exact(item, str)
                    for item in self._items(
                        self._decode(fields["claim_boundary"], seen)
                    )
                ),
            )
            return record
        if tag == "ColoredPetriNetEnablementFailureIdentity":
            fields = self._fields(wire, tag, ("result_identity",))
            record = ColoredPetriNetEnablementFailureIdentity(
                result_identity=self._exact(
                    self._decode(fields["result_identity"], seen),
                    ColoredPetriNetEnablementResultIdentity,
                ),
            )
            return record
        if tag == "ColoredPetriNetEnablementResult":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "definition_identity",
                    "selection_policy",
                    "marking_identity",
                    "expression_evaluator_identity",
                    "ordering_policy_identity",
                    "transition_enabler_identity",
                    "enabled_bindings",
                    "failure",
                ),
            )
            record = ColoredPetriNetEnablementResult(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ColoredPetriNetEnablementResultIdentity,
                ),
                definition_identity=self._exact(
                    self._decode(fields["definition_identity"], seen),
                    ColoredPetriNetDefinitionIdentity,
                ),
                selection_policy=self._exact(
                    self._decode(fields["selection_policy"], seen),
                    ColoredPetriNetSelectionPolicy,
                ),
                marking_identity=self._exact(
                    self._decode(fields["marking_identity"], seen),
                    ColoredPetriNetMarkingIdentity,
                ),
                expression_evaluator_identity=self._exact(
                    self._decode(fields["expression_evaluator_identity"], seen),
                    ColoredPetriNetExpressionEvaluatorIdentity,
                ),
                ordering_policy_identity=self._exact(
                    self._decode(fields["ordering_policy_identity"], seen),
                    ColoredPetriNetOrderingPolicyIdentity,
                ),
                transition_enabler_identity=self._exact(
                    self._decode(fields["transition_enabler_identity"], seen),
                    ColoredPetriNetTransitionEnablerIdentity,
                ),
                enabled_bindings=self._parse_ColoredPetriNetEnablementResult_enabled_bindings(
                    self._decode(fields["enabled_bindings"], seen)
                ),
                failure=self._parse_ColoredPetriNetEnablementResult_failure(
                    self._decode(fields["failure"], seen)
                ),
            )
            return record
        if tag == "ColoredPetriNetEnablementResultIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetEnablementResultIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetExpressionEvaluatorIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetExpressionEvaluatorIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetFiringAudit":
            fields = self._fields(
                wire,
                tag,
                (
                    "consumed_occurrences",
                    "read_occurrences",
                    "inhibitor_evaluations",
                    "produced_tokens",
                    "firer_identity",
                ),
            )
            record = ColoredPetriNetFiringAudit(
                consumed_occurrences=tuple(
                    self._exact(item, ColoredPetriNetTokenOccurrence)
                    for item in self._items(
                        self._decode(fields["consumed_occurrences"], seen)
                    )
                ),
                read_occurrences=tuple(
                    self._exact(item, ColoredPetriNetTokenOccurrence)
                    for item in self._items(
                        self._decode(fields["read_occurrences"], seen)
                    )
                ),
                inhibitor_evaluations=tuple(
                    self._exact(item, ColoredPetriNetInhibitorEvaluation)
                    for item in self._items(
                        self._decode(fields["inhibitor_evaluations"], seen)
                    )
                ),
                produced_tokens=tuple(
                    self._exact(item, ColoredPetriNetProducedToken)
                    for item in self._items(
                        self._decode(fields["produced_tokens"], seen)
                    )
                ),
                firer_identity=self._exact(
                    self._decode(fields["firer_identity"], seen),
                    ColoredPetriNetTransitionFirerIdentity,
                ),
            )
            return record
        if tag == "ColoredPetriNetFiringFailure":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "code",
                    "operation_phase",
                    "expected_condition",
                    "observed_condition",
                    "diagnostic",
                    "validation_issues",
                    "claim_boundary",
                ),
            )
            record = ColoredPetriNetFiringFailure(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ColoredPetriNetFiringFailureIdentity,
                ),
                code=self._exact(
                    self._decode(fields["code"], seen), ColoredPetriNetFiringFailureCode
                ),
                operation_phase=self._exact(
                    self._decode(fields["operation_phase"], seen), str
                ),
                expected_condition=self._exact(
                    self._decode(fields["expected_condition"], seen), str
                ),
                observed_condition=self._exact(
                    self._decode(fields["observed_condition"], seen), str
                ),
                diagnostic=self._exact(self._decode(fields["diagnostic"], seen), str),
                validation_issues=tuple(
                    self._exact(item, ColoredPetriNetValidationIssue)
                    for item in self._items(
                        self._decode(fields["validation_issues"], seen)
                    )
                ),
                claim_boundary=tuple(
                    self._exact(item, str)
                    for item in self._items(
                        self._decode(fields["claim_boundary"], seen)
                    )
                ),
            )
            return record
        if tag == "ColoredPetriNetFiringFailureIdentity":
            fields = self._fields(wire, tag, ("result_identity",))
            record = ColoredPetriNetFiringFailureIdentity(
                result_identity=self._exact(
                    self._decode(fields["result_identity"], seen),
                    ColoredPetriNetFiringResultIdentity,
                ),
            )
            return record
        if tag == "ColoredPetriNetFiringInput":
            fields = self._fields(
                wire,
                tag,
                (
                    "definition",
                    "transition_identity",
                    "predecessor_marking",
                    "enablement_result",
                    "selection_result",
                    "selected_binding",
                    "directive_identity",
                    "external_output_binding",
                ),
            )
            record = ColoredPetriNetFiringInput(
                definition=self._exact(
                    self._decode(fields["definition"], seen), ColoredPetriNetDefinition
                ),
                transition_identity=self._exact(
                    self._decode(fields["transition_identity"], seen),
                    ColoredPetriNetTransitionIdentity,
                ),
                predecessor_marking=self._exact(
                    self._decode(fields["predecessor_marking"], seen),
                    ColoredPetriNetMarking,
                ),
                enablement_result=self._exact(
                    self._decode(fields["enablement_result"], seen),
                    ColoredPetriNetEnablementResult,
                ),
                selection_result=self._exact(
                    self._decode(fields["selection_result"], seen),
                    ColoredPetriNetSelectionResult,
                ),
                selected_binding=self._exact(
                    self._decode(fields["selected_binding"], seen),
                    ColoredPetriNetBinding,
                ),
                directive_identity=self._parse_ColoredPetriNetFiringInput_directive_identity(
                    self._decode(fields["directive_identity"], seen)
                ),
                external_output_binding=self._exact(
                    self._decode(fields["external_output_binding"], seen),
                    ColoredPetriNetBinding,
                ),
            )
            return record
        if tag == "ColoredPetriNetFiringResult":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "firing_input",
                    "outcome",
                    "successor_marking",
                    "audit",
                    "failure",
                ),
            )
            record = ColoredPetriNetFiringResult(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ColoredPetriNetFiringResultIdentity,
                ),
                firing_input=self._exact(
                    self._decode(fields["firing_input"], seen),
                    ColoredPetriNetFiringInput,
                ),
                outcome=self._exact(
                    self._decode(fields["outcome"], seen),
                    ColoredPetriNetFiringOutcomeKind,
                ),
                successor_marking=self._parse_ColoredPetriNetFiringResult_successor_marking(
                    self._decode(fields["successor_marking"], seen)
                ),
                audit=self._parse_ColoredPetriNetFiringResult_audit(
                    self._decode(fields["audit"], seen)
                ),
                failure=self._parse_ColoredPetriNetFiringResult_failure(
                    self._decode(fields["failure"], seen)
                ),
            )
            return record
        if tag == "ColoredPetriNetFiringResultIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetFiringResultIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetGuardExpression":
            fields = self._fields(wire, tag, ("operator", "operands", "left", "right"))
            record = ColoredPetriNetGuardExpression(
                operator=self._exact(
                    self._decode(fields["operator"], seen), ColoredPetriNetGuardOperator
                ),
                operands=tuple(
                    self._exact(item, ColoredPetriNetGuardExpression)
                    for item in self._items(self._decode(fields["operands"], seen))
                ),
                left=self._parse_ColoredPetriNetGuardExpression_left(
                    self._decode(fields["left"], seen)
                ),
                right=self._parse_ColoredPetriNetGuardExpression_left(
                    self._decode(fields["right"], seen)
                ),
            )
            return record
        if tag == "ColoredPetriNetInhibitorEvaluation":
            fields = self._fields(
                wire,
                tag,
                ("arc_identity", "place_identity", "pattern_index", "matching_count"),
            )
            record = ColoredPetriNetInhibitorEvaluation(
                arc_identity=self._exact(
                    self._decode(fields["arc_identity"], seen),
                    ColoredPetriNetArcIdentity,
                ),
                place_identity=self._exact(
                    self._decode(fields["place_identity"], seen),
                    ColoredPetriNetPlaceIdentity,
                ),
                pattern_index=self._exact(
                    self._decode(fields["pattern_index"], seen), int
                ),
                matching_count=self._exact(
                    self._decode(fields["matching_count"], seen), int
                ),
            )
            return record
        if tag == "ColoredPetriNetInhibitorPattern":
            fields = self._fields(wire, tag, ("allowed_color_identities",))
            record = ColoredPetriNetInhibitorPattern(
                allowed_color_identities=tuple(
                    self._exact(item, ColoredPetriNetColorIdentity)
                    for item in self._items(
                        self._decode(fields["allowed_color_identities"], seen)
                    )
                ),
            )
            return record
        if tag == "ColoredPetriNetInputInscription":
            fields = self._fields(wire, tag, ("mode", "patterns"))
            record = ColoredPetriNetInputInscription(
                mode=self._exact(
                    self._decode(fields["mode"], seen), ColoredPetriNetInputMode
                ),
                patterns=tuple(
                    self._parse_ColoredPetriNetInputInscription_patterns_item(item)
                    for item in self._items(self._decode(fields["patterns"], seen))
                ),
            )
            return record
        if tag == "ColoredPetriNetMarking":
            fields = self._fields(
                wire, tag, ("identity", "definition_identity", "places")
            )
            record = ColoredPetriNetMarking(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ColoredPetriNetMarkingIdentity,
                ),
                definition_identity=self._exact(
                    self._decode(fields["definition_identity"], seen),
                    ColoredPetriNetDefinitionIdentity,
                ),
                places=tuple(
                    self._exact(item, ColoredPetriNetPlaceMarking)
                    for item in self._items(self._decode(fields["places"], seen))
                ),
            )
            return record
        if tag == "ColoredPetriNetMarkingIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetMarkingIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetOrderingPolicyIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetOrderingPolicyIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetOutputInscription":
            fields = self._fields(wire, tag, ("templates",))
            record = ColoredPetriNetOutputInscription(
                templates=tuple(
                    self._exact(item, ColoredPetriNetTokenTemplate)
                    for item in self._items(self._decode(fields["templates"], seen))
                ),
            )
            return record
        if tag == "ColoredPetriNetPlaceDefinition":
            fields = self._fields(wire, tag, ("identity", "allowed_color_identities"))
            record = ColoredPetriNetPlaceDefinition(
                identity=self._exact(
                    self._decode(fields["identity"], seen), ColoredPetriNetPlaceIdentity
                ),
                allowed_color_identities=tuple(
                    self._exact(item, ColoredPetriNetColorIdentity)
                    for item in self._items(
                        self._decode(fields["allowed_color_identities"], seen)
                    )
                ),
            )
            return record
        if tag == "ColoredPetriNetPlaceIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetPlaceIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetPlaceMarking":
            fields = self._fields(wire, tag, ("place_identity", "tokens"))
            record = ColoredPetriNetPlaceMarking(
                place_identity=self._exact(
                    self._decode(fields["place_identity"], seen),
                    ColoredPetriNetPlaceIdentity,
                ),
                tokens=tuple(
                    self._exact(item, ColoredPetriNetToken)
                    for item in self._items(self._decode(fields["tokens"], seen))
                ),
            )
            return record
        if tag == "ColoredPetriNetProducedToken":
            fields = self._fields(
                wire, tag, ("arc_identity", "place_identity", "template_index", "token")
            )
            record = ColoredPetriNetProducedToken(
                arc_identity=self._exact(
                    self._decode(fields["arc_identity"], seen),
                    ColoredPetriNetArcIdentity,
                ),
                place_identity=self._exact(
                    self._decode(fields["place_identity"], seen),
                    ColoredPetriNetPlaceIdentity,
                ),
                template_index=self._exact(
                    self._decode(fields["template_index"], seen), int
                ),
                token=self._exact(
                    self._decode(fields["token"], seen), ColoredPetriNetToken
                ),
            )
            return record
        if tag == "ColoredPetriNetSelectionDirective":
            fields = self._fields(
                wire, tag, ("enablement_result_identity", "binding", "identity")
            )
            record = ColoredPetriNetSelectionDirective(
                enablement_result_identity=self._exact(
                    self._decode(fields["enablement_result_identity"], seen),
                    ColoredPetriNetEnablementResultIdentity,
                ),
                binding=self._exact(
                    self._decode(fields["binding"], seen), ColoredPetriNetBinding
                ),
            )
            if record.identity != self._exact(
                self._decode(fields["identity"], seen),
                ColoredPetriNetSelectionDirectiveIdentity,
            ):
                raise self._failure(
                    "decode", WorkflowPersistenceFailureCode.IDENTITY_MISMATCH
                )
            return record
        if tag == "ColoredPetriNetSelectionDirectiveIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetSelectionDirectiveIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetSelectionResult":
            fields = self._fields(
                wire,
                tag,
                (
                    "enablement_result_identity",
                    "selector_identity",
                    "ordering_policy_identity",
                    "outcome",
                    "selected_binding",
                    "directive",
                    "failure_code",
                    "identity",
                ),
            )
            record = ColoredPetriNetSelectionResult(
                enablement_result_identity=self._exact(
                    self._decode(fields["enablement_result_identity"], seen),
                    ColoredPetriNetEnablementResultIdentity,
                ),
                selector_identity=self._exact(
                    self._decode(fields["selector_identity"], seen),
                    ColoredPetriNetBindingSelectorIdentity,
                ),
                ordering_policy_identity=self._exact(
                    self._decode(fields["ordering_policy_identity"], seen),
                    ColoredPetriNetOrderingPolicyIdentity,
                ),
                outcome=self._exact(
                    self._decode(fields["outcome"], seen),
                    ColoredPetriNetSelectionOutcomeKind,
                ),
                selected_binding=self._parse_ColoredPetriNetSelectionResult_selected_binding(
                    self._decode(fields["selected_binding"], seen)
                ),
                directive=self._parse_ColoredPetriNetSelectionResult_directive(
                    self._decode(fields["directive"], seen)
                ),
                failure_code=self._parse_ColoredPetriNetSelectionResult_failure_code(
                    self._decode(fields["failure_code"], seen)
                ),
            )
            if record.identity != self._exact(
                self._decode(fields["identity"], seen),
                ColoredPetriNetSelectionResultIdentity,
            ):
                raise self._failure(
                    "decode", WorkflowPersistenceFailureCode.IDENTITY_MISMATCH
                )
            return record
        if tag == "ColoredPetriNetSelectionResultIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetSelectionResultIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetToken":
            fields = self._fields(
                wire, tag, ("color_identity", "value", "token_identity")
            )
            record = ColoredPetriNetToken(
                color_identity=self._exact(
                    self._decode(fields["color_identity"], seen),
                    ColoredPetriNetColorIdentity,
                ),
                value=self._exact(
                    self._decode(fields["value"], seen), ColoredPetriNetValue
                ),
                token_identity=self._parse_ColoredPetriNetToken_token_identity(
                    self._decode(fields["token_identity"], seen)
                ),
            )
            return record
        if tag == "ColoredPetriNetTokenIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetTokenIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetTokenOccurrence":
            fields = self._fields(
                wire,
                tag,
                (
                    "arc_identity",
                    "place_identity",
                    "pattern_index",
                    "occurrence_ordinal",
                    "token",
                ),
            )
            record = ColoredPetriNetTokenOccurrence(
                arc_identity=self._exact(
                    self._decode(fields["arc_identity"], seen),
                    ColoredPetriNetArcIdentity,
                ),
                place_identity=self._exact(
                    self._decode(fields["place_identity"], seen),
                    ColoredPetriNetPlaceIdentity,
                ),
                pattern_index=self._exact(
                    self._decode(fields["pattern_index"], seen), int
                ),
                occurrence_ordinal=self._exact(
                    self._decode(fields["occurrence_ordinal"], seen), int
                ),
                token=self._exact(
                    self._decode(fields["token"], seen), ColoredPetriNetToken
                ),
            )
            return record
        if tag == "ColoredPetriNetTokenPattern":
            fields = self._fields(
                wire, tag, ("variable_identity", "allowed_color_identities")
            )
            record = ColoredPetriNetTokenPattern(
                variable_identity=self._exact(
                    self._decode(fields["variable_identity"], seen),
                    ColoredPetriNetBindingVariableIdentity,
                ),
                allowed_color_identities=tuple(
                    self._exact(item, ColoredPetriNetColorIdentity)
                    for item in self._items(
                        self._decode(fields["allowed_color_identities"], seen)
                    )
                ),
            )
            return record
        if tag == "ColoredPetriNetTokenTemplate":
            fields = self._fields(
                wire,
                tag,
                ("color_identity", "value_expression", "token_identity_expression"),
            )
            record = ColoredPetriNetTokenTemplate(
                color_identity=self._exact(
                    self._decode(fields["color_identity"], seen),
                    ColoredPetriNetColorIdentity,
                ),
                value_expression=self._exact(
                    self._decode(fields["value_expression"], seen),
                    ColoredPetriNetValueExpression,
                ),
                token_identity_expression=self._parse_ColoredPetriNetGuardExpression_left(
                    self._decode(fields["token_identity_expression"], seen)
                ),
            )
            return record
        if tag == "ColoredPetriNetTransitionDefinition":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "input_variable_identities",
                    "external_output_variable_identities",
                    "guard",
                ),
            )
            record = ColoredPetriNetTransitionDefinition(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ColoredPetriNetTransitionIdentity,
                ),
                input_variable_identities=tuple(
                    self._exact(item, ColoredPetriNetBindingVariableIdentity)
                    for item in self._items(
                        self._decode(fields["input_variable_identities"], seen)
                    )
                ),
                external_output_variable_identities=tuple(
                    self._exact(item, ColoredPetriNetBindingVariableIdentity)
                    for item in self._items(
                        self._decode(
                            fields["external_output_variable_identities"], seen
                        )
                    )
                ),
                guard=self._exact(
                    self._decode(fields["guard"], seen), ColoredPetriNetGuardExpression
                ),
            )
            return record
        if tag == "ColoredPetriNetTransitionEnablerIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetTransitionEnablerIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetTransitionFirerIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetTransitionFirerIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetTransitionIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetTransitionIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetValidationIssue":
            fields = self._fields(
                wire, tag, ("code", "path", "related_identities", "message")
            )
            record = ColoredPetriNetValidationIssue(
                code=self._exact(
                    self._decode(fields["code"], seen),
                    ColoredPetriNetValidationIssueCode,
                ),
                path=tuple(
                    self._exact(item, str)
                    for item in self._items(self._decode(fields["path"], seen))
                ),
                related_identities=tuple(
                    self._exact(item, str)
                    for item in self._items(
                        self._decode(fields["related_identities"], seen)
                    )
                ),
                message=self._exact(self._decode(fields["message"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetValue":
            fields = self._fields(wire, tag, ("kind", "value"))
            record = ColoredPetriNetValue(
                kind=self._exact(
                    self._decode(fields["kind"], seen), ColoredPetriNetValueKind
                ),
                value=self._parse_ColoredPetriNetValue_value(
                    self._decode(fields["value"], seen)
                ),
            )
            return record
        if tag == "ColoredPetriNetValueExpression":
            fields = self._fields(wire, tag, ("kind", "literal", "variable_identity"))
            record = ColoredPetriNetValueExpression(
                kind=self._exact(
                    self._decode(fields["kind"], seen),
                    ColoredPetriNetValueExpressionKind,
                ),
                literal=self._parse_ColoredPetriNetValueExpression_literal(
                    self._decode(fields["literal"], seen)
                ),
                variable_identity=self._parse_ColoredPetriNetValueExpression_variable_identity(
                    self._decode(fields["variable_identity"], seen)
                ),
            )
            return record
        raise _WorkflowRunWireUnsupported

    def _parse_ColoredPetriNetArcDefinition_input_inscription(
        self, value: _RunValue
    ) -> ColoredPetriNetInputInscription | None:
        if type(value) is ColoredPetriNetInputInscription:
            return self._exact(value, ColoredPetriNetInputInscription)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetArcDefinition_output_inscription(
        self, value: _RunValue
    ) -> ColoredPetriNetOutputInscription | None:
        if type(value) is ColoredPetriNetOutputInscription:
            return self._exact(value, ColoredPetriNetOutputInscription)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetEnablementResult_enabled_bindings(
        self, value: _RunValue
    ) -> tuple[ColoredPetriNetBinding, ...] | None:
        if type(value) is tuple:
            return tuple(
                self._exact(item, ColoredPetriNetBinding) for item in self._items(value)
            )
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetEnablementResult_failure(
        self, value: _RunValue
    ) -> ColoredPetriNetEnablementFailure | None:
        if type(value) is ColoredPetriNetEnablementFailure:
            return self._exact(value, ColoredPetriNetEnablementFailure)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetFiringInput_directive_identity(
        self, value: _RunValue
    ) -> ColoredPetriNetSelectionDirectiveIdentity | None:
        if type(value) is ColoredPetriNetSelectionDirectiveIdentity:
            return self._exact(value, ColoredPetriNetSelectionDirectiveIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetFiringResult_successor_marking(
        self, value: _RunValue
    ) -> ColoredPetriNetMarking | None:
        if type(value) is ColoredPetriNetMarking:
            return self._exact(value, ColoredPetriNetMarking)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetFiringResult_audit(
        self, value: _RunValue
    ) -> ColoredPetriNetFiringAudit | None:
        if type(value) is ColoredPetriNetFiringAudit:
            return self._exact(value, ColoredPetriNetFiringAudit)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetFiringResult_failure(
        self, value: _RunValue
    ) -> ColoredPetriNetFiringFailure | None:
        if type(value) is ColoredPetriNetFiringFailure:
            return self._exact(value, ColoredPetriNetFiringFailure)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetGuardExpression_left(
        self, value: _RunValue
    ) -> ColoredPetriNetValueExpression | None:
        if type(value) is ColoredPetriNetValueExpression:
            return self._exact(value, ColoredPetriNetValueExpression)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetInputInscription_patterns_item(
        self, value: _RunValue
    ) -> ColoredPetriNetTokenPattern | ColoredPetriNetInhibitorPattern:
        if type(value) is ColoredPetriNetTokenPattern:
            return self._exact(value, ColoredPetriNetTokenPattern)
        if type(value) is ColoredPetriNetInhibitorPattern:
            return self._exact(value, ColoredPetriNetInhibitorPattern)
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetSelectionResult_selected_binding(
        self, value: _RunValue
    ) -> ColoredPetriNetBinding | None:
        if type(value) is ColoredPetriNetBinding:
            return self._exact(value, ColoredPetriNetBinding)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetSelectionResult_directive(
        self, value: _RunValue
    ) -> ColoredPetriNetSelectionDirective | None:
        if type(value) is ColoredPetriNetSelectionDirective:
            return self._exact(value, ColoredPetriNetSelectionDirective)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetSelectionResult_failure_code(
        self, value: _RunValue
    ) -> ColoredPetriNetSelectionFailureCode | None:
        if type(value) is ColoredPetriNetSelectionFailureCode:
            return self._exact(value, ColoredPetriNetSelectionFailureCode)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetToken_token_identity(
        self, value: _RunValue
    ) -> ColoredPetriNetTokenIdentity | None:
        if type(value) is ColoredPetriNetTokenIdentity:
            return self._exact(value, ColoredPetriNetTokenIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetValue_value(
        self, value: _RunValue
    ) -> None | bool | int | float | str | tuple[str, ...]:
        if value is None:
            return None
        if type(value) is bool:
            return self._exact(value, bool)
        if type(value) is int:
            return self._exact(value, int)
        if type(value) is float:
            return self._exact(value, float)
        if type(value) is str:
            return self._exact(value, str)
        if type(value) is tuple:
            return tuple(self._exact(item, str) for item in self._items(value))
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetValueExpression_literal(
        self, value: _RunValue
    ) -> ColoredPetriNetValue | None:
        if type(value) is ColoredPetriNetValue:
            return self._exact(value, ColoredPetriNetValue)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetValueExpression_variable_identity(
        self, value: _RunValue
    ) -> ColoredPetriNetBindingVariableIdentity | None:
        if type(value) is ColoredPetriNetBindingVariableIdentity:
            return self._exact(value, ColoredPetriNetBindingVariableIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")
