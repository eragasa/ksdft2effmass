r"""Software verification of ``WorkflowRunSerializer``.

Bounded artifact scope: mixed Task/decision record histories and malformed correlations.

Evidence profile: claim_bearing

Facet and represented meaning

Independent literals retain all attempt states and generic outcome kinds, retries,
child/request failure correlations, ordinary/dispatched Task transitions, and initial
and corrected no-Task decisions in a shared transition sequence.

Intrinsic and cross-object scope

Complete constructor graphs and literal bytes are independent codec oracles. They
preserve append order, lexical collections and supplied correlations without running
Tasks, authorizing decisions or computing a firing. Omitted activation, production
and membership records mean these are not structurally closed histories.

VVUQ and scientific exclusions

Synthetic software verification only; no authentic human response, scientific
result, replay equality, stored presence or effect completion is established.
"""

from base64 import b64encode
from dataclasses import replace
from hashlib import sha256
from pathlib import Path
from typing import Literal

import pytest
from ksdft2effmass import analysis as q
from ksdft2effmass import workflows as w
from ksdft2effmass.application import ApplicationResultValueSerializer
from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoResultValueSerializer,
)
from ksdft2effmass.petrinet import colored as c
from ksdft2effmass.workflows import WorkflowRunSerializer

type HistoryVariant = Literal["ordinary", "dispatched"]

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunSerializer


class TestWorkflowRunSerializer:
    """Own mixed-history representation, not history execution or acceptance."""

    @staticmethod
    def wire(variant: HistoryVariant = "ordinary") -> bytes:
        return (
            Path(__file__)
            .with_name("resources")
            .joinpath(f"workflow-run-task-decision-{variant}-v1.json")
            .read_bytes()
        )

    @staticmethod
    def make_serializer() -> WorkflowRunSerializer:
        qe = QuantumEspressoResultValueSerializer()
        return SUT(
            result_codec=ApplicationResultValueSerializer(
                workflow_codec=w.WorkflowResultValueSerializer(source_codec=qe),
                quantum_espresso_codec=qe,
                quantity_of_interest_codec=q.QuantityOfInterestResultValueSerializer(),
            )
        )

    @staticmethod
    def make_reference() -> w.ResultObjectReference:
        evaluator = q.QuantityOfInterestEvaluatorIdentity("synthetic-evaluator:7")
        value = q.ScalarQuantityOfInterestValue(
            w.ResultObjectIdentity("synthetic-result"),
            q.ScalarQuantityOfInterestDefinition(
                q.QuantityOfInterestIdentity("synthetic-qoi"),
                q.QuantityOfInterestSubjectIdentity("synthetic-subject"),
                q.QuantityOfInterestStateSpaceIdentity("synthetic-space"),
                q.QuantityOfInterestConventionIdentity("synthetic-convention"),
                evaluator,
                (
                    q.NormalizedObservationRequirementIdentity("second"),
                    q.NormalizedObservationRequirementIdentity("first"),
                ),
                q.QuantityOfInterestCompleteness.COMPLETE,
                "synthetic-unit",
            ),
            w.ResultObjectIdentity("synthetic-observations"),
            evaluator,
            -0.0,
        )
        return w.ResultObjectReference(
            identity=w.ResultObjectReferenceIdentity("reference"),
            result=value,
            concrete_type_identity=w.ResultObjectTypeIdentity(
                "ksdft2effmass.analysis.ScalarQuantityOfInterestValue:1"
            ),
            owning_domain_identity=w.ResultObjectDomainIdentity(
                "ksdft2effmass.analysis"
            ),
            content_identity=w.ResultObjectContentIdentity(
                "qoi-result-value:1:sha256:82f1cc1a48c83ff5e3e8a112ef556608a1f181403302bfffa3731cd4be3a98ab"
            ),
            producer_provenance=w.UnknownLegacyResultProducer(
                identity=w.ResultProducerProvenanceIdentity("legacy-producer"),
                source_identity=w.RetainedResultSourceIdentity("synthetic-source"),
                evidence_identities=(
                    w.ResultProducerEvidenceIdentity("synthetic-evidence"),
                ),
                limitations=("synthetic software fixture; not historical evidence",),
            ),
        )

    @staticmethod
    def make_attempt(
        kind: w.TaskInvocationOutcomeKind, terminal: bool
    ) -> w.TaskAttempt:
        label = kind.value
        status = (
            {
                w.TaskInvocationOutcomeKind.CONFIRMED: w.TaskAttemptStatus.CONFIRMED,
                w.TaskInvocationOutcomeKind.REJECTED: w.TaskAttemptStatus.REJECTED,
                w.TaskInvocationOutcomeKind.INDETERMINATE: (
                    w.TaskAttemptStatus.INDETERMINATE
                ),
            }[kind]
            if terminal
            else w.TaskAttemptStatus.STARTED
        )
        return w.TaskAttempt(
            identity=w.TaskAttemptRecordIdentity(
                f"{label}-{'terminal' if terminal else 'started'}"
            ),
            workflow_run_identity=w.WorkflowRunIdentity("run"),
            task_instance_identity=w.TaskInstanceIdentity("task-instance"),
            activation_identity=w.TaskActivationIdentity(f"activation-{label}"),
            operation_identity=w.OperationIdentity(f"operation-{label}"),
            attempt_identity=w.AttemptIdentity(f"attempt-{label}"),
            status=status,
            predecessor_attempt_record_identity=(
                w.TaskAttemptRecordIdentity(f"{label}-started") if terminal else None
            ),
            retry_of_attempt_identity=(
                w.AttemptIdentity("attempt-rejected")
                if not terminal and kind is w.TaskInvocationOutcomeKind.CONFIRMED
                else None
            ),
            child_workflow_run_identity=(
                w.WorkflowRunIdentity("child-run")
                if kind is w.TaskInvocationOutcomeKind.INDETERMINATE
                else None
            ),
        )

    def make_outcome(
        self, kind: w.TaskInvocationOutcomeKind, variant: HistoryVariant
    ) -> w.TaskInvocationOutcome:
        label = kind.value
        return w.TaskInvocationOutcome(
            identity=w.TaskInvocationOutcomeIdentity(f"outcome-{label}"),
            workflow_run_identity=w.WorkflowRunIdentity("run"),
            activation_identity=w.TaskActivationIdentity(f"activation-{label}"),
            operation_identity=w.OperationIdentity(f"operation-{label}"),
            attempt_identity=w.AttemptIdentity(f"attempt-{label}"),
            terminal_attempt_record_identity=w.TaskAttemptRecordIdentity(
                f"{label}-terminal"
            ),
            kind=kind,
            results=(self.make_reference(),)
            if kind is w.TaskInvocationOutcomeKind.CONFIRMED
            else (),
            production_record_identities=(
                w.ResultProductionRecordIdentity("production"),
            )
            if kind is w.TaskInvocationOutcomeKind.CONFIRMED
            else (),
            failure_record_identity=w.TaskFailureRecordIdentity("failure-dispatch")
            if kind is w.TaskInvocationOutcomeKind.REJECTED
            else None,
            dispatch_outcome_record_identity=(
                w.DispatchOutcomeRecordIdentity("dispatch-confirmed")
                if variant == "dispatched"
                and kind is w.TaskInvocationOutcomeKind.CONFIRMED
                else None
            ),
            reconciliation_identity_values=("reconcile-a", "reconcile-b")
            if kind is w.TaskInvocationOutcomeKind.INDETERMINATE
            else (),
        )

    @staticmethod
    def make_failure(nested: bool) -> w.TaskFailureRecord:
        origin = "nested" if nested else "dispatch"
        return w.TaskFailureRecord(
            identity=w.TaskFailureRecordIdentity(f"failure-{origin}"),
            workflow_run_identity=w.WorkflowRunIdentity("run"),
            task_instance_identity=w.TaskInstanceIdentity("task-instance"),
            activation_identity=w.TaskActivationIdentity("activation-rejected"),
            operation_identity=w.OperationIdentity("operation-rejected"),
            attempt_identity=w.AttemptIdentity("attempt-rejected"),
            terminal_attempt_record_identity=w.TaskAttemptRecordIdentity(
                "rejected-terminal"
            ),
            failure=w.TaskInvocationFailure(
                identity=w.TaskInvocationFailureIdentity(f"domain-failure-{origin}"),
                code="synthetic-failure",
                operation_phase=f"synthetic-{origin}",
                diagnostic="retained synthetic diagnostic",
                retryable=False,
                claim_boundary=("no successful firing", "not a physical result"),
            ),
            request_identity=None
            if nested
            else w.SimulationExecutionRequestIdentity("execution-request"),
            child_workflow_run_identity=w.WorkflowRunIdentity("child-run")
            if nested
            else None,
            claim_boundary=("correlation only", "no effect permission"),
        )

    @staticmethod
    def make_resolution(correction: bool) -> w.ScientificDecisionResolution:
        label = "correction" if correction else "initial"
        return w.ScientificDecisionResolution(
            identity=w.ResultObjectIdentity(f"decision-{label}"),
            content_identity=w.ResultObjectContentIdentity(f"opaque:{label}"),
            request_identity=w.ScientificDecisionRequestIdentity("request"),
            verbatim_response="  yes — correction\n\tΩ  "
            if correction
            else "  no — first\n\tΩ  ",
            normalized_option_identity=w.ScientificDecisionOptionIdentity(
                "option-yes" if correction else "option-no"
            ),
            response_source_identity=w.ResponseSourceIdentity("source"),
            authority_context_identity=w.AuthorityContextIdentity("context"),
            boundary_receipt_identity=w.BoundaryReceiptIdentity("boundary-receipt")
            if correction
            else None,
            predecessor_resolution_identity=w.ResultObjectIdentity("decision-initial")
            if correction
            else None,
            supersedes_resolution_identity=w.ResultObjectIdentity("decision-initial")
            if correction
            else None,
            producer_provenance=w.RepresentedScientificDecisionIngressProducer(
                identity=w.ResultProducerProvenanceIdentity(f"producer-{label}"),
                workflow_identity=w.WorkflowIdentity("workflow"),
                workflow_run_identity=w.WorkflowRunIdentity("run"),
                request_identity=w.ScientificDecisionRequestIdentity("request"),
                transition_record_identity=w.ScientificDecisionTransitionRecordIdentity(
                    f"decision-{label}-record"
                ),
                recorder_identity=w.ScientificDecisionRecorderIdentity("recorder:7"),
                response_source_identity=w.ResponseSourceIdentity("source"),
                authority_context_identity=w.AuthorityContextIdentity("context"),
                resolution_identity=w.ResultObjectIdentity(f"decision-{label}"),
            ),
        )

    @staticmethod
    def make_request() -> w.ScientificDecisionRequest:
        return w.ScientificDecisionRequest(
            identity=w.ScientificDecisionRequestIdentity("request"),
            question="Synthetic choice?\nRetain the supplied response.",
            options=(
                w.ScientificDecisionOption(
                    w.ScientificDecisionOptionIdentity("option-no"), "no"
                ),
                w.ScientificDecisionOption(
                    w.ScientificDecisionOptionIdentity("option-yes"), "yes"
                ),
            ),
            declared_scope="synthetic branch; no scientific decision",
            workflow_identity=w.WorkflowIdentity("workflow"),
            workflow_run_identity=w.WorkflowRunIdentity("run"),
            affected_task_instance_identity=w.TaskInstanceIdentity("task-instance"),
            affected_transition_identity=c.ColoredPetriNetTransitionIdentity(
                "transition"
            ),
            required_response_source_identity=w.ResponseSourceIdentity("source"),
            required_authority_context_identity=w.AuthorityContextIdentity("context"),
            definition_identity="synthetic-decision-definition",
            definition_version=1,
        )

    @staticmethod
    def make_firing(genesis: w.WorkflowRun) -> c.ColoredPetriNetFiringResult:
        """Construct retained facts; no enablement, selection or firing is computed."""
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
        return c.ColoredPetriNetFiringResult(
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
                (), (), (), (), c.ColoredPetriNetTransitionFirerIdentity("firer")
            ),
        )

    @staticmethod
    def make_decision_transition(
        genesis: w.WorkflowRun, firing: c.ColoredPetriNetFiringResult, correction: bool
    ) -> w.ScientificDecisionWorkflowTransitionRecord:
        label = "correction" if correction else "initial"
        variable = c.ColoredPetriNetBindingVariableIdentity("option")
        definition = firing.firing_input.definition
        definition = replace(
            definition,
            transitions=(
                replace(
                    definition.transitions[0],
                    external_output_variable_identities=(variable,),
                ),
            ),
        )
        external = c.ColoredPetriNetBinding(
            firing.firing_input.transition_identity,
            (
                c.ColoredPetriNetBindingAssignment(
                    variable,
                    c.ColoredPetriNetValue(
                        c.ColoredPetriNetValueKind.STRING, "yes" if correction else "no"
                    ),
                ),
            ),
        )
        firing = replace(
            firing,
            firing_input=replace(
                firing.firing_input,
                definition=definition,
                external_output_binding=external,
            ),
        )
        return w.ScientificDecisionWorkflowTransitionRecord(
            identity=w.ScientificDecisionTransitionRecordIdentity(
                f"decision-{label}-record"
            ),
            sequence_identity=w.WorkflowTransitionSequenceIdentity(f"sequence-{label}"),
            sequence_index=2 if correction else 1,
            workflow_identity=genesis.workflow_identity,
            workflow_run_identity=genesis.identity,
            definition_reference_identity=genesis.definition_reference_identity,
            runtime_bundle_identity=genesis.runtime_bundle_identity,
            request_identity=w.ScientificDecisionRequestIdentity("request"),
            resolution_identity=w.ResultObjectIdentity(f"decision-{label}"),
            producer_provenance_identity=w.ResultProducerProvenanceIdentity(
                f"producer-{label}"
            ),
            firing_result=firing,
        )

    def make_run(
        self, genesis: w.WorkflowRun, variant: HistoryVariant
    ) -> w.WorkflowRun:
        firing = self.make_firing(genesis)
        transition = w.TaskWorkflowTransitionRecord(
            identity=w.TaskWorkflowTransitionRecordIdentity("task-record"),
            sequence_identity=w.WorkflowTransitionSequenceIdentity("sequence-task"),
            sequence_index=0,
            workflow_identity=genesis.workflow_identity,
            workflow_run_identity=genesis.identity,
            definition_reference_identity=genesis.definition_reference_identity,
            runtime_bundle_identity=genesis.runtime_bundle_identity,
            activation_identity=w.TaskActivationIdentity("activation-confirmed"),
            operation_identity=w.OperationIdentity("operation-confirmed"),
            attempt_identity=w.AttemptIdentity("attempt-confirmed"),
            terminal_attempt_record_identity=w.TaskAttemptRecordIdentity(
                "confirmed-terminal"
            ),
            outcome_identity=w.TaskInvocationOutcomeIdentity("outcome-confirmed"),
            result_production_identities=(
                w.ResultProductionRecordIdentity("production"),
            ),
            firing_result=firing,
            request_correlation_identity=w.SimulationExecutionRequestCorrelationIdentity(
                "request-correlation"
            )
            if variant == "dispatched"
            else None,
            dispatch_outcome_record_identity=w.DispatchOutcomeRecordIdentity(
                "dispatch-confirmed"
            )
            if variant == "dispatched"
            else None,
        )
        return replace(
            genesis,
            attempts=(
                self.make_attempt(w.TaskInvocationOutcomeKind.REJECTED, False),
                self.make_attempt(w.TaskInvocationOutcomeKind.REJECTED, True),
                self.make_attempt(w.TaskInvocationOutcomeKind.CONFIRMED, False),
                self.make_attempt(w.TaskInvocationOutcomeKind.CONFIRMED, True),
                self.make_attempt(w.TaskInvocationOutcomeKind.INDETERMINATE, False),
                self.make_attempt(w.TaskInvocationOutcomeKind.INDETERMINATE, True),
            ),
            outcomes=(
                self.make_outcome(w.TaskInvocationOutcomeKind.CONFIRMED, variant),
                self.make_outcome(w.TaskInvocationOutcomeKind.INDETERMINATE, variant),
                self.make_outcome(w.TaskInvocationOutcomeKind.REJECTED, variant),
            ),
            result_references=(self.make_reference(),),
            failures=(self.make_failure(False), self.make_failure(True)),
            scientific_decision_requests=(self.make_request(),),
            scientific_decision_resolutions=(
                self.make_resolution(True),
                self.make_resolution(False),
            ),
            transitions=(
                transition,
                self.make_decision_transition(genesis, firing, False),
                self.make_decision_transition(genesis, firing, True),
            ),
        )

    @pytest.mark.parametrize(
        "variant",
        [
            pytest.param("ordinary", id="ordinary_task_then_decisions"),
            pytest.param("dispatched", id="dispatched_task_then_decisions"),
        ],
    )
    def test_method__serialize__matches_mixed_history_literal(
        self, genesis_snapshot: w.WorkflowRunSnapshot, variant: HistoryVariant
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-TASK-DECISION-001

        Requirement: Mixed Task/decision history retains full represented state.

        Method: Encode independent constructor graphs for two Task origin variants.

        Oracle: Literal wires composed without production serializers.

        Acceptance: Entire canonical payload equals the selected literal.

        Interpretation: Append order differs from lexical resolution storage order;
        decision transitions retain no Task invocation lineage.

        Limitations: Supplied success labels do not establish firing or closed history.
        """
        result = self.make_serializer().serialize(
            self.make_run(genesis_snapshot.run, variant), genesis_snapshot.binding
        )
        assert result.status == "encoded", result.failure
        assert result.encoded is not None and result.encoded.payload == self.wire(
            variant
        )

    @pytest.mark.parametrize(
        "variant",
        [
            pytest.param("ordinary", id="ordinary_task_then_decisions"),
            pytest.param("dispatched", id="dispatched_task_then_decisions"),
        ],
    )
    def test_method__deserialize__restores_mixed_history_literal(
        self, genesis_snapshot: w.WorkflowRunSnapshot, variant: HistoryVariant
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-TASK-DECISION-002

        Requirement: Decode complete typed histories without replacing supplied values.

        Method: Decode literal bytes; independently construct expected public records.

        Oracle: Full run and binding, including verbatim Unicode and correction links.

        Acceptance: Entire reconstructed run and binding agree exactly.

        Interpretation: Retry, child, failure and no-Task decision origins are retained.

        Limitations: Representation does not authenticate responses or validate replay.
        """
        result = self.make_serializer().deserialize(self.wire(variant))
        assert result.status == "decoded", result.failure
        assert result.run == self.make_run(genesis_snapshot.run, variant)
        assert result.binding == genesis_snapshot.binding

    @pytest.mark.parametrize(
        ("original", "replacement"),
        [
            pytest.param(
                b'"predecessor_attempt_record_identity":{"fields":{"value":"confirmed-started"},"type":"TaskAttemptRecordIdentity"}',
                b'"predecessor_attempt_record_identity":null',
                id="terminal_predecessor_missing",
            ),
            pytest.param(
                b'"retry_of_attempt_identity":{"fields":{"value":"attempt-rejected"},"type":"AttemptIdentity"}',
                b'"retry_of_attempt_identity":{"fields":{"value":"attempt-confirmed"},"type":"AttemptIdentity"}',
                id="started_attempt_retries_itself",
            ),
            pytest.param(
                b'"production_record_identities":[{"fields":{"value":"production"},"type":"ResultProductionRecordIdentity"}]',
                b'"production_record_identities":[]',
                id="confirmed_result_production_unpaired",
            ),
            pytest.param(
                b'"failure_record_identity":{"fields":{"value":"failure-dispatch"},"type":"TaskFailureRecordIdentity"}',
                b'"failure_record_identity":null',
                id="rejected_failure_missing",
            ),
            pytest.param(
                b'"reconciliation_identity_values":["reconcile-a","reconcile-b"]',
                b'"reconciliation_identity_values":[]',
                id="indeterminate_evidence_missing",
            ),
            pytest.param(
                b'"sequence_index":{"fields":{"value":"0x0"},"type":"int"}',
                b'"sequence_index":true',
                id="boolean_task_sequence_index",
            ),
            pytest.param(
                b'"sequence_index":{"fields":{"value":"0x2"},"type":"int"}',
                b'"sequence_index":{"fields":{"value":"0x1"},"type":"int"}',
                id="duplicate_mixed_sequence_index",
            ),
            pytest.param(
                b'"request_correlation_identity":null',
                b'"request_correlation_identity":{"fields":{"value":"unpaired"},"type":"SimulationExecutionRequestCorrelationIdentity"}',
                id="task_dispatch_pair_incomplete",
            ),
            pytest.param(
                b'"value":"option-yes"',
                b'"value":"option-no"',
                id="duplicate_decision_option_identity",
            ),
            pytest.param(
                b'"definition_version":{"fields":{"value":"0x1"},"type":"int"}',
                b'"definition_version":true',
                id="boolean_decision_definition_version",
            ),
            pytest.param(
                b'"definition_version":{"fields":{"value":"0x1"},"type":"int"}',
                b'"definition_version":{"fields":{"value":"0x0"},"type":"int"}',
                id="nonpositive_decision_definition_version",
            ),
            pytest.param(
                b'"fields":{"definition_reference_identity":',
                b'"fields":{"attempt_identity":{"fields":{"value":"invented"},'
                b'"type":"AttemptIdentity"},"definition_reference_identity":',
                id="decision_transition_forbids_task_lineage",
            ),
        ],
    )
    def test_method__deserialize__rejects_intrinsic_history_drift(
        self, original: bytes, replacement: bytes
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-TASK-DECISION-003

        Requirement: Retained history obeys intrinsic variants and nominal correlations.

        Method: Mutate a named literal pattern, leaving all concrete envelopes intact.

        Oracle: Public attempt, outcome, sequence, dispatch-pair and decision rules.

        Acceptance: Corrupt failure with no partial run or binding.

        Interpretation: Valid JSON alone does not establish a valid record graph.

        Limitations: No cross-history validator or replay is exercised.
        """
        wire = self.wire()
        assert original in wire
        result = self.make_serializer().deserialize(wire.replace(original, replacement))
        assert result.status == "corrupt"
        assert result.failure is not None
        assert result.run is None and result.binding is None

    @pytest.mark.parametrize(
        ("original", "replacement"),
        [
            pytest.param(
                b'"supersedes_resolution_identity":{"fields":{"value":"decision-initial"},"type":"ResultObjectIdentity"}',
                b'"supersedes_resolution_identity":null',
                id="correction_pair_incomplete",
            ),
            pytest.param(
                b'"value":"decision-initial"',
                b'"value":"decision-correction"',
                id="correction_supersedes_itself",
            ),
            pytest.param(
                b'"resolution_identity":{"fields":{"value":"decision-correction"},"type":"ResultObjectIdentity"}',
                b'"resolution_identity":{"fields":{"value":"detached"},"type":"ResultObjectIdentity"}',
                id="producer_resolution_detached",
            ),
        ],
    )
    def test_method__deserialize__rejects_rehashed_invalid_decision(
        self, original: bytes, replacement: bytes
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-TASK-DECISION-004

        Requirement: Digest-consistent decisions obey intrinsic correction rules.

        Method: Mutate the independent correction literal and update its base64 payload
        and SHA-256 envelope binding using standard-library primitives only.

        Oracle: Public paired-predecessor, no-self-supersession and producer rules.

        Acceptance: Corrupt failure with no reconstructed run or binding.

        Interpretation: Rejection is not caused by retaining an obsolete payload digest.

        Limitations: No authentic response, acceptance or history closure is tested.
        """
        payload = (
            Path(__file__)
            .with_name("resources")
            .joinpath("task-decision-correction-value-v1.json")
            .read_bytes()
        )
        assert original in payload
        changed = payload.replace(original, replacement)
        wire = self.wire()
        assert (
            b64encode(payload) in wire and sha256(payload).hexdigest().encode() in wire
        )
        wire = wire.replace(b64encode(payload), b64encode(changed)).replace(
            sha256(payload).hexdigest().encode(), sha256(changed).hexdigest().encode()
        )
        result = self.make_serializer().deserialize(wire)
        assert result.status == "corrupt"
        assert result.failure is not None
        assert result.run is None and result.binding is None
