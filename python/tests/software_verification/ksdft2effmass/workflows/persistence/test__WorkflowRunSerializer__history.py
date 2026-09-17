r"""Software verification of ``WorkflowRunSerializer``.

Bounded artifact scope: complete firing input and constructor-derived identities.

Evidence profile: claim_bearing

Facet and represented meaning

Synthetic task-origin transitions retain directed selection, recursive expressions,
all three input-inscription modes, output templates and nonempty firing audits.
Literal independent identity preimages fix both selection digests.

Intrinsic and cross-object scope

Wire traversal and constructor identity binding only. The fixture deliberately makes
no claim of complete invocation links or computed replay equality.

VVUQ and scientific exclusions

Software verification, not executed firing, scientific validity or authority.
"""

from dataclasses import replace
from pathlib import Path

import pytest
from ksdft2effmass import workflows as w
from ksdft2effmass.analysis import QuantityOfInterestResultValueSerializer
from ksdft2effmass.petrinet import colored as c
from ksdft2effmass.workflows import WorkflowRunSerializer

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunSerializer


class TestWorkflowRunSerializer:
    """Retained selection state is reconstructed, never assigned over its identity."""

    @staticmethod
    def wire() -> bytes:
        return (
            Path(__file__)
            .with_name("resources")
            .joinpath("workflow-run-selection-v1.json")
            .read_bytes()
        )

    @staticmethod
    def make_run(genesis: w.WorkflowRun) -> w.WorkflowRun:
        transition = c.ColoredPetriNetTransitionIdentity("transition")
        binding = c.ColoredPetriNetBinding(transition, ())
        enablement_id = c.ColoredPetriNetEnablementResultIdentity("a" * 64)
        directive = c.ColoredPetriNetSelectionDirective(enablement_id, binding)
        selection = c.ColoredPetriNetSelectionResult(
            enablement_id,
            c.ColoredPetriNetBindingSelectorIdentity("selector"),
            c.ColoredPetriNetOrderingPolicyIdentity("ordering"),
            c.ColoredPetriNetSelectionOutcomeKind.SELECTED,
            selected_binding=binding,
            directive=directive,
        )
        definition = c.ColoredPetriNetDefinition(
            genesis.initial_marking.definition_identity,
            (),
            (),
            (
                c.ColoredPetriNetTransitionDefinition(
                    transition,
                    (),
                    (),
                    c.ColoredPetriNetGuardExpression(
                        c.ColoredPetriNetGuardOperator.TRUE
                    ),
                ),
            ),
            (),
            (transition,),
            c.ColoredPetriNetSelectionPolicy.DIRECTED_ALLOWED,
        )
        enablement = c.ColoredPetriNetEnablementResult(
            enablement_id,
            definition.identity,
            definition.selection_policy,
            genesis.initial_marking.identity,
            c.ColoredPetriNetExpressionEvaluatorIdentity("expressions"),
            c.ColoredPetriNetOrderingPolicyIdentity("ordering"),
            c.ColoredPetriNetTransitionEnablerIdentity("enabler"),
            enabled_bindings=(binding,),
        )
        firing = c.ColoredPetriNetFiringResult(
            c.ColoredPetriNetFiringResultIdentity("b" * 64),
            c.ColoredPetriNetFiringInput(
                definition,
                transition,
                genesis.initial_marking,
                enablement,
                selection,
                binding,
                directive.identity,
                binding,
            ),
            c.ColoredPetriNetFiringOutcomeKind.SUCCESS,
            genesis.initial_marking,
            c.ColoredPetriNetFiringAudit(
                (),
                (),
                (),
                (),
                c.ColoredPetriNetTransitionFirerIdentity("firer"),
            ),
        )
        record = w.TaskWorkflowTransitionRecord(
            identity=w.TaskWorkflowTransitionRecordIdentity("transition-record"),
            sequence_identity=w.WorkflowTransitionSequenceIdentity("sequence"),
            sequence_index=0,
            workflow_identity=genesis.workflow_identity,
            workflow_run_identity=genesis.identity,
            definition_reference_identity=genesis.definition_reference_identity,
            runtime_bundle_identity=genesis.runtime_bundle_identity,
            activation_identity=w.TaskActivationIdentity("activation"),
            operation_identity=w.OperationIdentity("operation"),
            attempt_identity=w.AttemptIdentity("attempt"),
            terminal_attempt_record_identity=w.TaskAttemptRecordIdentity("terminal"),
            outcome_identity=w.TaskInvocationOutcomeIdentity("outcome"),
            result_production_identities=(
                w.ResultProductionRecordIdentity("production"),
            ),
            firing_result=firing,
        )
        return replace(genesis, transitions=(record,))

    @classmethod
    def make_rich_run(cls, genesis: w.WorkflowRun) -> w.WorkflowRun:
        """Construct representation inputs without evaluating the retained firing."""
        run = cls.make_run(genesis)
        record = run.transitions[0]
        assert type(record) is w.TaskWorkflowTransitionRecord
        firing = record.firing_result
        transition = firing.firing_input.transition_identity
        color = c.ColoredPetriNetColorIdentity("count")
        source = c.ColoredPetriNetPlaceIdentity("source")
        destination = c.ColoredPetriNetPlaceIdentity("destination")
        variable = c.ColoredPetriNetBindingVariableIdentity("input")
        external = c.ColoredPetriNetBindingVariableIdentity("external")
        value = c.ColoredPetriNetValue(c.ColoredPetriNetValueKind.INTEGER, -3)
        expression = c.ColoredPetriNetValueExpression(
            c.ColoredPetriNetValueExpressionKind.VARIABLE,
            variable_identity=external,
        )
        literal = c.ColoredPetriNetValueExpression(
            c.ColoredPetriNetValueExpressionKind.LITERAL, literal=value
        )
        guard = c.ColoredPetriNetGuardExpression(
            c.ColoredPetriNetGuardOperator.ALL,
            operands=(
                c.ColoredPetriNetGuardExpression(
                    c.ColoredPetriNetGuardOperator.NOT,
                    operands=(
                        c.ColoredPetriNetGuardExpression(
                            c.ColoredPetriNetGuardOperator.FALSE
                        ),
                    ),
                ),
                c.ColoredPetriNetGuardExpression(
                    c.ColoredPetriNetGuardOperator.ANY,
                    operands=(
                        c.ColoredPetriNetGuardExpression(
                            c.ColoredPetriNetGuardOperator.TRUE
                        ),
                        c.ColoredPetriNetGuardExpression(
                            c.ColoredPetriNetGuardOperator.EQUAL,
                            left=literal,
                            right=literal,
                        ),
                    ),
                ),
            ),
        )
        pattern = c.ColoredPetriNetTokenPattern(variable, (color,))
        consume = c.ColoredPetriNetArcIdentity("consume")
        inhibit = c.ColoredPetriNetArcIdentity("inhibit")
        produce = c.ColoredPetriNetArcIdentity("produce")
        read = c.ColoredPetriNetArcIdentity("read")
        definition = c.ColoredPetriNetDefinition(
            identity=genesis.initial_marking.definition_identity,
            colors=(
                c.ColoredPetriNetColorDefinition(
                    color, (c.ColoredPetriNetValueKind.INTEGER,)
                ),
            ),
            places=(
                c.ColoredPetriNetPlaceDefinition(destination, (color,)),
                c.ColoredPetriNetPlaceDefinition(source, (color,)),
            ),
            transitions=(
                c.ColoredPetriNetTransitionDefinition(
                    transition, (variable,), (external,), guard
                ),
            ),
            arcs=(
                c.ColoredPetriNetArcDefinition(
                    consume,
                    source,
                    transition,
                    input_inscription=c.ColoredPetriNetInputInscription(
                        c.ColoredPetriNetInputMode.CONSUME, (pattern,)
                    ),
                ),
                c.ColoredPetriNetArcDefinition(
                    inhibit,
                    destination,
                    transition,
                    input_inscription=c.ColoredPetriNetInputInscription(
                        c.ColoredPetriNetInputMode.INHIBIT,
                        (c.ColoredPetriNetInhibitorPattern((color,)),),
                    ),
                ),
                c.ColoredPetriNetArcDefinition(
                    produce,
                    destination,
                    transition,
                    output_inscription=c.ColoredPetriNetOutputInscription(
                        (
                            c.ColoredPetriNetTokenTemplate(
                                color,
                                expression,
                                c.ColoredPetriNetValueExpression(
                                    c.ColoredPetriNetValueExpressionKind.LITERAL,
                                    literal=c.ColoredPetriNetValue(
                                        c.ColoredPetriNetValueKind.STRING, "produced"
                                    ),
                                ),
                            ),
                        )
                    ),
                ),
                c.ColoredPetriNetArcDefinition(
                    read,
                    source,
                    transition,
                    input_inscription=c.ColoredPetriNetInputInscription(
                        c.ColoredPetriNetInputMode.READ, (pattern,)
                    ),
                ),
            ),
            transition_priority=(transition,),
            selection_policy=c.ColoredPetriNetSelectionPolicy.DIRECTED_ALLOWED,
        )
        token = c.ColoredPetriNetToken(color, value)
        audit = c.ColoredPetriNetFiringAudit(
            consumed_occurrences=(
                c.ColoredPetriNetTokenOccurrence(consume, source, 0, 1, token),
            ),
            read_occurrences=(
                c.ColoredPetriNetTokenOccurrence(read, source, 0, 2, token),
            ),
            inhibitor_evaluations=(
                c.ColoredPetriNetInhibitorEvaluation(inhibit, destination, 0, 0),
            ),
            produced_tokens=(
                c.ColoredPetriNetProducedToken(
                    produce,
                    destination,
                    0,
                    c.ColoredPetriNetToken(
                        color, value, c.ColoredPetriNetTokenIdentity("produced")
                    ),
                ),
            ),
            firer_identity=c.ColoredPetriNetTransitionFirerIdentity("firer"),
        )
        return replace(
            run,
            transitions=(
                replace(
                    record,
                    firing_result=replace(
                        firing,
                        audit=audit,
                        firing_input=replace(
                            firing.firing_input,
                            definition=definition,
                            external_output_binding=c.ColoredPetriNetBinding(
                                transition,
                                (c.ColoredPetriNetBindingAssignment(external, value),),
                            ),
                        ),
                    ),
                ),
            ),
        )

    def test_method__serialize__matches_independent_retained_selection_wire(
        self,
        genesis_snapshot: w.WorkflowRunSnapshot,
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-HISTORY-001

        Requirement: Complete retained firing state includes derived selection IDs.

        Method: Encode separately constructed CPN records inside a task transition.

        Oracle: Fixed literal wire with independently evaluated identity preimages.

        Acceptance: Exact full aggregate bytes equal the resource.

        Interpretation: Encoding retains inputs without recomputing firing.

        Limitations: This does not establish invocation link closure or replay equality.
        """
        result = w.WorkflowRunSerializer(
            result_codec=QuantityOfInterestResultValueSerializer(),
        ).serialize(self.make_run(genesis_snapshot.run), genesis_snapshot.binding)
        assert result.status == "encoded", result.failure
        assert result.encoded is not None and result.encoded.payload == self.wire()

    def test_method__deserialize__restores_complete_retained_selection(
        self,
        genesis_snapshot: w.WorkflowRunSnapshot,
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-HISTORY-002

        Requirement: Decode reconstructs every retained firing and selection field.

        Method: Decode the fixed literal and compare independent public constructors.

        Oracle: Exact immutable record graph and independently specified digests.

        Acceptance: Complete run and binding agree; derived identities match literals.

        Interpretation: Historical inputs are retained, not executed by deserialization.

        Limitations: No authority, store observation or scientific result is claimed.
        """
        result = w.WorkflowRunSerializer(
            result_codec=QuantityOfInterestResultValueSerializer(),
        ).deserialize(self.wire())
        assert result.status == "decoded", result.failure
        assert result.run == self.make_run(genesis_snapshot.run)
        assert result.binding == genesis_snapshot.binding
        assert result.run is not None
        selection = result.run.transitions[
            0
        ].firing_result.firing_input.selection_result
        assert (
            selection.identity.value
            == "99cfb5d66fa5cdf6cdc924761026e781df473a71efc9ab5f034e5331a52d4dc8"
        )
        assert selection.directive is not None
        assert (
            selection.directive.identity.value
            == "546c4d0c20d3959846e6d210520c4ccf2f576046c5facbfff4302b3deef08e2d"
        )

    def test_method__serialize__matches_rich_cpn_wire(
        self, genesis_snapshot: w.WorkflowRunSnapshot
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-HISTORY-005

        Requirement: Recursive guards, inscriptions, bindings and complete nonempty
        firing audits survive the aggregate wire without recomputation.

        Method: Serialize an independent graph constructed through public records.

        Oracle: Fixed literal rich CPN wire authored without the production codec.

        Acceptance: Complete canonical aggregate bytes match exactly.

        Interpretation: Nonempty nested fields cannot be replaced by defaults.

        Limitations: Synthetic retained firing inputs do not assert computed firing
        correctness, structurally closed Workflow history or scientific validity.
        """
        expected = (
            Path(__file__)
            .with_name("resources")
            .joinpath("workflow-run-rich-cpn-v1.json")
            .read_bytes()
        )
        encoded = SUT(result_codec=QuantityOfInterestResultValueSerializer()).serialize(
            self.make_rich_run(genesis_snapshot.run), genesis_snapshot.binding
        )
        assert encoded.status == "encoded", encoded.failure
        assert encoded.encoded is not None
        assert encoded.encoded.payload == expected

    def test_method__deserialize__restores_rich_cpn_graph(
        self, genesis_snapshot: w.WorkflowRunSnapshot
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-HISTORY-006

        Requirement: Deserialize every declared field of nonempty recursive CPN
        definition and audit records without evaluating them.

        Method: Decode the literal fixture and compare independent public constructors.

        Oracle: Separately constructed immutable graph, including negative integer
        values, variable and literal expressions, input modes and occurrence ordinals.

        Acceptance: Entire run and binding equal the independent graph exactly.

        Interpretation: Encoding/decoding agreement alone is not the oracle.

        Limitations: No real transition or external effect is executed or verified.
        """
        wire = (
            Path(__file__)
            .with_name("resources")
            .joinpath("workflow-run-rich-cpn-v1.json")
            .read_bytes()
        )
        decoded = SUT(
            result_codec=QuantityOfInterestResultValueSerializer()
        ).deserialize(wire)
        assert decoded.status == "decoded", decoded.failure
        assert decoded.run == self.make_rich_run(genesis_snapshot.run)
        assert decoded.binding == genesis_snapshot.binding

    @pytest.mark.parametrize(
        ("original", "replacement"),
        [
            pytest.param(
                b'"operator":{"fields":{"value":"all"}',
                b'"operator":{"fields":{"value":"not"}',
                id="nested_guard_wrong_arity",
            ),
            pytest.param(
                b'"occurrence_ordinal":{"fields":{"value":"0x1"}',
                b'"occurrence_ordinal":{"fields":{"value":"-0x1"}',
                id="negative_audit_ordinal",
            ),
            pytest.param(
                b'"value":"-0x3"',
                b'"value":true',
                id="boolean_tagged_integer",
            ),
        ],
    )
    def test_method__deserialize__rejects_malformed_rich_cpn(
        self, original: bytes, replacement: bytes
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-HISTORY-007

        Requirement: Nested intrinsic violations must not reconstruct a partial run.

        Method: Mutate one fixed intrinsic field in the rich literal representation.

        Oracle: NOT has one operand; occurrence ordinals are nonnegative integers;
        tagged integers require canonical hexadecimal strings rather than booleans.

        Acceptance: Corrupt result contains a failure and no run or binding.

        Interpretation: A recognized tag does not establish a valid nested record.

        Limitations: This checks represented invariants, not full Workflow closure.
        """
        wire = (
            Path(__file__)
            .with_name("resources")
            .joinpath("workflow-run-rich-cpn-v1.json")
            .read_bytes()
        )
        assert original in wire
        result = SUT(
            result_codec=QuantityOfInterestResultValueSerializer()
        ).deserialize(wire.replace(original, replacement))
        assert result.status == "corrupt"
        assert result.failure is not None
        assert result.run is None and result.binding is None

    @pytest.mark.parametrize(
        ("operator", "wire_value"),
        [
            pytest.param(
                c.ColoredPetriNetGuardOperator.NOT_EQUAL, b"not_equal", id="not_equal"
            ),
            pytest.param(
                c.ColoredPetriNetGuardOperator.LESS_THAN, b"less_than", id="less_than"
            ),
            pytest.param(
                c.ColoredPetriNetGuardOperator.LESS_THAN_OR_EQUAL,
                b"less_than_or_equal",
                id="less_than_or_equal",
            ),
            pytest.param(
                c.ColoredPetriNetGuardOperator.GREATER_THAN,
                b"greater_than",
                id="greater_than",
            ),
            pytest.param(
                c.ColoredPetriNetGuardOperator.GREATER_THAN_OR_EQUAL,
                b"greater_than_or_equal",
                id="greater_than_or_equal",
            ),
        ],
    )
    def test_method__codec__retains_comparison_operators(
        self,
        genesis_snapshot: w.WorkflowRunSnapshot,
        operator: c.ColoredPetriNetGuardOperator,
        wire_value: bytes,
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-HISTORY-009

        Requirement: Every closed comparison operator preserves its own wire label.

        Method: Substitute one explicit literal operator label and construct the
        corresponding immutable nested guard through its public enum.

        Oracle: Independently specified enum-to-wire label pairs.

        Acceptance: Whole encoded wire and independently reconstructed run agree.

        Interpretation: Related comparison operators are not normalized to equality.

        Limitations: The codec preserves expressions; it does not evaluate guards.
        """
        run = self.make_rich_run(genesis_snapshot.run)
        record = run.transitions[0]
        assert type(record) is w.TaskWorkflowTransitionRecord
        firing = record.firing_result
        definition = firing.firing_input.definition
        transition = definition.transitions[0]
        guard = transition.guard
        choice = guard.operands[1]
        comparison = replace(choice.operands[1], operator=operator)
        choice = replace(choice, operands=(choice.operands[0], comparison))
        guard = replace(guard, operands=(guard.operands[0], choice))
        definition = replace(
            definition, transitions=(replace(transition, guard=guard),)
        )
        run = replace(
            run,
            transitions=(
                replace(
                    record,
                    firing_result=replace(
                        firing,
                        firing_input=replace(
                            firing.firing_input, definition=definition
                        ),
                    ),
                ),
            ),
        )
        wire = (
            Path(__file__)
            .with_name("resources")
            .joinpath("workflow-run-rich-cpn-v1.json")
            .read_bytes()
            .replace(b'"value":"equal"', b'"value":"' + wire_value + b'"')
        )
        serializer = SUT(result_codec=QuantityOfInterestResultValueSerializer())
        encoded = serializer.serialize(run, genesis_snapshot.binding)
        assert encoded.status == "encoded", encoded.failure
        assert encoded.encoded is not None and encoded.encoded.payload == wire
        decoded = serializer.deserialize(wire)
        assert decoded.status == "decoded", decoded.failure
        assert decoded.run == run and decoded.binding == genesis_snapshot.binding

    def test_method__codec__retains_nested_enablement_failure(
        self, genesis_snapshot: w.WorkflowRunSnapshot
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-HISTORY-008

        Requirement: Retained enablement failures preserve their bound identities,
        conditions, diagnostics, validation issues and claim boundaries.

        Method: Encode and decode a fixed literal with a separately constructed
        structured failure in the retained firing input.

        Oracle: Exact complete failure record and independent canonical wire.

        Acceptance: Bytes, reconstructed run and binding all match exactly.

        Interpretation: Failure evidence is retained without rerunning enablement.

        Limitations: This intentionally inconsistent historical firing input is
        representation evidence, not a valid firing or replay-equal WorkflowRun.
        """
        run = self.make_rich_run(genesis_snapshot.run)
        record = run.transitions[0]
        assert type(record) is w.TaskWorkflowTransitionRecord
        firing = record.firing_result
        enablement = firing.firing_input.enablement_result
        failure = c.ColoredPetriNetEnablementFailure(
            identity=c.ColoredPetriNetEnablementFailureIdentity(enablement.identity),
            code=c.ColoredPetriNetEnablementFailureCode.INVALID_MARKING,
            operation_phase="marking_validation",
            expected_condition="all declared places",
            observed_condition="empty marking",
            diagnostic="synthetic incomplete marking",
            validation_issues=(
                c.ColoredPetriNetValidationIssue(
                    c.ColoredPetriNetValidationIssueCode.PLACE_SET_MISMATCH,
                    ("definition", "places"),
                    ("definition",),
                    "synthetic missing places",
                ),
            ),
        )
        run = replace(
            run,
            transitions=(
                replace(
                    record,
                    firing_result=replace(
                        firing,
                        firing_input=replace(
                            firing.firing_input,
                            enablement_result=replace(
                                enablement, enabled_bindings=None, failure=failure
                            ),
                        ),
                    ),
                ),
            ),
        )
        wire = (
            Path(__file__)
            .with_name("resources")
            .joinpath("workflow-run-enable-failure-v1.json")
            .read_bytes()
        )
        serializer = SUT(result_codec=QuantityOfInterestResultValueSerializer())
        encoded = serializer.serialize(run, genesis_snapshot.binding)
        assert encoded.status == "encoded", encoded.failure
        assert encoded.encoded is not None
        assert encoded.encoded.payload == wire
        decoded = serializer.deserialize(wire)
        assert decoded.status == "decoded", decoded.failure
        assert decoded.run == run and decoded.binding == genesis_snapshot.binding

    @pytest.mark.parametrize(
        "digest",
        [
            pytest.param(
                "99cfb5d66fa5cdf6cdc924761026e781df473a71efc9ab5f034e5331a52d4dc8",
                id="selection_identity",
            ),
            pytest.param(
                "546c4d0c20d3959846e6d210520c4ccf2f576046c5facbfff4302b3deef08e2d",
                id="directive_identity",
            ),
        ],
    )
    def test_method__deserialize__rejects_forged_derived_identity(
        self, digest: str
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-HISTORY-003

        Requirement: Supplied derived identities cannot override owning constructors.

        Method: Replace all appearances of one digest by a valid but incorrect digest.

        Oracle: Independent fixed identity preimages for the unchanged input fields.

        Acceptance: Corrupt result has failure and no run or binding.

        Interpretation: Internal consistency of copied labels is insufficient.

        Limitations: Content identities do not authenticate a historical process.
        """
        result = w.WorkflowRunSerializer(
            result_codec=QuantityOfInterestResultValueSerializer(),
        ).deserialize(self.wire().replace(digest.encode(), b"c" * 64))
        assert result.status == "corrupt"
        assert result.run is None and result.binding is None
        assert result.failure is not None

    @pytest.mark.parametrize(
        "variant",
        [
            pytest.param("empty", id="empty_selection"),
            pytest.param("no_match", id="directed_no_match"),
            pytest.param("failure", id="failed_selection"),
        ],
    )
    def test_method__codec__preserves_closed_nested_selection_variants(
        self,
        genesis_snapshot: w.WorkflowRunSnapshot,
        variant: str,
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-HISTORY-004

        Requirement: Retained nested selection variants are not silently rewritten.

        Method: Encode and decode independent literals for each nonselected variant.

        Oracle: Direct closed constructors and fixed independently authored bytes.

        Acceptance: Complete run and binding match; encoding equals literal bytes.

        Interpretation: Records are preserved without evaluating firing semantics.

        Limitations: These retained inputs do not assert successful replay or closure.
        """
        run = self.make_run(genesis_snapshot.run)
        record = run.transitions[0]
        assert type(record) is w.TaskWorkflowTransitionRecord
        firing = record.firing_result
        selection = firing.firing_input.selection_result
        if variant == "empty":
            selection = replace(
                selection,
                outcome=c.ColoredPetriNetSelectionOutcomeKind.EMPTY,
                selected_binding=None,
                directive=None,
            )
        elif variant == "no_match":
            selection = replace(
                selection,
                outcome=c.ColoredPetriNetSelectionOutcomeKind.NO_MATCH,
                selected_binding=None,
            )
        else:
            selection = replace(
                selection,
                outcome=c.ColoredPetriNetSelectionOutcomeKind.FAILURE,
                selected_binding=None,
                failure_code=c.ColoredPetriNetSelectionFailureCode.ENABLEMENT_FAILED,
            )
        run = replace(
            run,
            transitions=(
                replace(
                    record,
                    firing_result=replace(
                        firing,
                        firing_input=replace(
                            firing.firing_input, selection_result=selection
                        ),
                    ),
                ),
            ),
        )
        wire = (
            Path(__file__)
            .with_name("resources")
            .joinpath(f"workflow-run-selection-{variant}-v1.json")
            .read_bytes()
        )
        serializer = w.WorkflowRunSerializer(
            result_codec=QuantityOfInterestResultValueSerializer(),
        )
        encoded = serializer.serialize(run, genesis_snapshot.binding)
        assert encoded.status == "encoded", encoded.failure
        assert encoded.encoded is not None and encoded.encoded.payload == wire
        decoded = serializer.deserialize(wire)
        assert decoded.status == "decoded", decoded.failure
        assert decoded.run == run and decoded.binding == genesis_snapshot.binding
