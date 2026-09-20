r"""Software verification of ``WorkflowRunSerializer``.

Bounded artifact scope: six result-producer variants, production and native admission.

Evidence profile: claim_bearing

Facet and represented meaning

Independent literals retain represented Task/decision, external, imported, declared
human and unknown-legacy provenance around complete concrete values. The Task literal
also retains production relations, output binding and native-admission correlations.

Intrinsic and cross-object scope

The codec preserves supplied records without resolving their evidence or reading
native artifacts. Missing Task, dispatch and transition history is explicit; these
fixtures do not establish structural closure or historical provenance truth.

VVUQ and scientific exclusions

Synthetic software verification only. Declared authors, external producers, receipts
and native artifacts are invented test inputs, not actual people, execution evidence,
authority, scientific results or accepted data.
"""

from dataclasses import replace
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

type ProducerKind = Literal[
    "task", "decision", "external", "imported", "human", "legacy"
]
type EvidenceMutation = Literal["no_evidence", "duplicate_evidence", "no_limitations"]
type Producer = (
    w.RepresentedTaskResultProducer
    | w.RepresentedScientificDecisionIngressProducer
    | w.ExternalResultProducer
    | w.ImportedRetainedResultProducer
    | w.HumanAuthoredResultProducer
    | w.UnknownLegacyResultProducer
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunSerializer


class TestWorkflowRunSerializer:
    """Own producer representation checks without asserting provenance truth."""

    @staticmethod
    def wire(kind: ProducerKind) -> bytes:
        return (
            Path(__file__)
            .with_name("resources")
            .joinpath(f"workflow-run-producer-{kind}-v1.json")
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
    def make_scalar() -> q.ScalarQuantityOfInterestValue:
        evaluator = q.QuantityOfInterestEvaluatorIdentity("synthetic-evaluator:7")
        return q.ScalarQuantityOfInterestValue(
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

    @staticmethod
    def make_decision() -> w.ScientificDecisionResolution:
        return w.ScientificDecisionResolution(
            identity=w.ResultObjectIdentity("decision-correction"),
            content_identity=w.ResultObjectContentIdentity("opaque:historical-content"),
            request_identity=w.ScientificDecisionRequestIdentity("request"),
            verbatim_response="  yes — retain\nverbatim\tΩ  ",
            normalized_option_identity=w.ScientificDecisionOptionIdentity("option-yes"),
            response_source_identity=w.ResponseSourceIdentity("source"),
            authority_context_identity=w.AuthorityContextIdentity("context"),
            boundary_receipt_identity=w.BoundaryReceiptIdentity("boundary-receipt"),
            predecessor_resolution_identity=w.ResultObjectIdentity("decision-initial"),
            supersedes_resolution_identity=w.ResultObjectIdentity("decision-initial"),
            producer_provenance=w.RepresentedScientificDecisionIngressProducer(
                identity=w.ResultProducerProvenanceIdentity("producer"),
                workflow_identity=w.WorkflowIdentity("workflow"),
                workflow_run_identity=w.WorkflowRunIdentity("run"),
                request_identity=w.ScientificDecisionRequestIdentity("request"),
                transition_record_identity=w.ScientificDecisionTransitionRecordIdentity(
                    "transition"
                ),
                recorder_identity=w.ScientificDecisionRecorderIdentity("recorder:7"),
                response_source_identity=w.ResponseSourceIdentity("source"),
                authority_context_identity=w.AuthorityContextIdentity("context"),
                resolution_identity=w.ResultObjectIdentity("decision-correction"),
            ),
        )

    def make_producer(self, kind: ProducerKind) -> Producer:
        if kind == "task":
            return w.RepresentedTaskResultProducer(
                identity=w.ResultProducerProvenanceIdentity("producer-task"),
                workflow_identity=w.WorkflowIdentity("workflow"),
                workflow_run_identity=w.WorkflowRunIdentity("run"),
                task_instance_identity=w.TaskInstanceIdentity("task"),
                activation_identity=w.TaskActivationIdentity("activation"),
                operation_identity=w.OperationIdentity("operation"),
                attempt_identity=w.AttemptIdentity("attempt"),
                terminal_attempt_record_identity=w.TaskAttemptRecordIdentity(
                    "terminal"
                ),
                outcome_identity=w.TaskInvocationOutcomeIdentity("outcome"),
                production_identity=w.ResultProductionRecordIdentity("production"),
            )
        if kind == "decision":
            return self.make_decision().producer_provenance
        identity = w.ResultProducerProvenanceIdentity(f"producer-{kind}")
        evidence = (
            w.ResultProducerEvidenceIdentity("evidence-a"),
            w.ResultProducerEvidenceIdentity("evidence-b"),
        )
        limitations = ("synthetic evidence only", "no authentic provenance claim")
        source = w.RetainedResultSourceIdentity("synthetic-source")
        if kind == "external":
            return w.ExternalResultProducer(
                identity=identity,
                external_producer_identity=w.ExternalResultProducerIdentity(
                    "synthetic-external"
                ),
                producer_attempt_identity=w.ExternalProducerAttemptIdentity(
                    "synthetic-external-attempt"
                ),
                evidence_identities=evidence,
                limitations=limitations,
            )
        if kind == "imported":
            return w.ImportedRetainedResultProducer(
                identity=identity,
                source_identity=source,
                evidence_identities=evidence,
                limitations=limitations,
            )
        if kind == "human":
            return w.HumanAuthoredResultProducer(
                identity=identity,
                author_identity=w.HumanResultAuthorIdentity("synthetic-author"),
                source_identity=source,
                evidence_identities=evidence,
                limitations=limitations,
            )
        return w.UnknownLegacyResultProducer(
            identity=identity,
            source_identity=source,
            evidence_identities=evidence,
            limitations=limitations,
        )

    @staticmethod
    def make_production() -> w.ResultProductionRecord:
        return w.ResultProductionRecord(
            identity=w.ResultProductionRecordIdentity("production"),
            workflow_run_identity=w.WorkflowRunIdentity("run"),
            task_instance_identity=w.TaskInstanceIdentity("task"),
            activation_identity=w.TaskActivationIdentity("activation"),
            operation_identity=w.OperationIdentity("operation"),
            attempt_identity=w.AttemptIdentity("attempt"),
            terminal_attempt_record_identity=w.TaskAttemptRecordIdentity("terminal"),
            outcome_identity=w.TaskInvocationOutcomeIdentity("outcome"),
            result_reference_identity=w.ResultObjectReferenceIdentity("reference"),
            result_artifact_relation_identities=(
                w.ResultArtifactRelationIdentity("relation-a"),
                w.ResultArtifactRelationIdentity("relation-b"),
            ),
            external_output_binding=c.ColoredPetriNetBinding(
                c.ColoredPetriNetTransitionIdentity("transition"),
                (
                    c.ColoredPetriNetBindingAssignment(
                        c.ColoredPetriNetBindingVariableIdentity("result"),
                        c.ColoredPetriNetValue(
                            c.ColoredPetriNetValueKind.STRING, "synthetic-result"
                        ),
                    ),
                ),
            ),
        )

    @staticmethod
    def make_admission() -> w.NativeOutputAdmission:
        return w.NativeOutputAdmission(
            identity=w.NativeOutputAdmissionIdentity("admission"),
            workflow_run_identity=w.WorkflowRunIdentity("run"),
            dispatch_outcome_record_identity=w.DispatchOutcomeRecordIdentity(
                "dispatch-record"
            ),
            dispatch_envelope_identity=w.SimulationDispatchObservationIdentity(
                "dispatch-envelope"
            ),
            production_record_identity=w.ResultProductionRecordIdentity("production"),
            result_reference_identity=w.ResultObjectReferenceIdentity("reference"),
            manifest_identity=w.ArtifactManifestIdentity("native-manifest"),
            manifest_entry_identities=(
                w.ArtifactManifestEntryIdentity("native-a"),
                w.ArtifactManifestEntryIdentity("native-b"),
            ),
        )

    def make_run(self, genesis: w.WorkflowRun, kind: ProducerKind) -> w.WorkflowRun:
        decision = kind == "decision"
        reference = w.ResultObjectReference(
            identity=w.ResultObjectReferenceIdentity("reference"),
            result=self.make_decision() if decision else self.make_scalar(),
            concrete_type_identity=w.ResultObjectTypeIdentity(
                "ksdft2effmass.workflows.ScientificDecisionResolution:1"
                if decision
                else "ksdft2effmass.analysis.ScalarQuantityOfInterestValue:1"
            ),
            owning_domain_identity=w.ResultObjectDomainIdentity(
                "ksdft2effmass.workflows" if decision else "ksdft2effmass.analysis"
            ),
            content_identity=w.ResultObjectContentIdentity(
                "opaque:historical-content"
                if decision
                else (
                    "qoi-result-value:1:sha256:"
                    "82f1cc1a48c83ff5e3e8a112ef556608a1f181403302bfffa3731cd4be3a98ab"
                )
            ),
            producer_provenance=self.make_producer(kind),
        )
        return replace(
            genesis,
            result_references=(reference,),
            result_productions=(self.make_production(),) if kind == "task" else (),
            native_output_admissions=(self.make_admission(),) if kind == "task" else (),
        )

    @pytest.mark.parametrize(
        "kind",
        [
            pytest.param("task", id="represented_task"),
            pytest.param("decision", id="represented_decision"),
            pytest.param("external", id="external_producer"),
            pytest.param("imported", id="imported_source"),
            pytest.param("human", id="declared_human"),
            pytest.param("legacy", id="unknown_legacy"),
        ],
    )
    def test_method__serialize__matches_provenance_literal(
        self, genesis_snapshot: w.WorkflowRunSnapshot, kind: ProducerKind
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-PROVENANCE-001

        Requirement: Producer variants retain complete provenance and result values.

        Method: Serialize an independently constructed public aggregate for each kind.

        Oracle: Fixed literals composed without production serialization.

        Acceptance: Entire canonical payload equals the selected literal bytes.

        Interpretation: Task production and native admission remain explicit records.

        Limitations: No provenance authentication, native file access or replay occurs.
        """
        result = self.make_serializer().serialize(
            self.make_run(genesis_snapshot.run, kind), genesis_snapshot.binding
        )
        assert result.status == "encoded", result.failure
        assert result.encoded is not None and result.encoded.payload == self.wire(kind)

    @pytest.mark.parametrize(
        "kind",
        [
            pytest.param("task", id="represented_task"),
            pytest.param("decision", id="represented_decision"),
            pytest.param("external", id="external_producer"),
            pytest.param("imported", id="imported_source"),
            pytest.param("human", id="declared_human"),
            pytest.param("legacy", id="unknown_legacy"),
        ],
    )
    def test_method__deserialize__restores_provenance_literal(
        self, genesis_snapshot: w.WorkflowRunSnapshot, kind: ProducerKind
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-PROVENANCE-002

        Requirement: Decode concrete values with their exact distinct producer records.

        Method: Decode fixed literals and compare independently constructed records.

        Oracle: Full expected run and commit binding, not a re-encoding round trip.

        Acceptance: Run and binding compare equal with all provenance fields preserved.

        Interpretation: Supplied evidence limitations and native correlations survive.

        Limitations: Record equality does not establish truthful provenance or science.
        """
        result = self.make_serializer().deserialize(self.wire(kind))
        assert result.status == "decoded", result.failure
        assert result.run == self.make_run(genesis_snapshot.run, kind)
        assert result.binding == genesis_snapshot.binding

    @pytest.mark.parametrize(
        ("kind", "mutation"),
        [
            pytest.param("external", "no_evidence", id="external_evidence_missing"),
            pytest.param(
                "external", "duplicate_evidence", id="external_evidence_duplicate"
            ),
            pytest.param(
                "external", "no_limitations", id="external_limitations_missing"
            ),
            pytest.param("imported", "no_evidence", id="imported_evidence_missing"),
            pytest.param(
                "imported", "duplicate_evidence", id="imported_evidence_duplicate"
            ),
            pytest.param(
                "imported", "no_limitations", id="imported_limitations_missing"
            ),
            pytest.param("human", "no_evidence", id="human_evidence_missing"),
            pytest.param("human", "duplicate_evidence", id="human_evidence_duplicate"),
            pytest.param("human", "no_limitations", id="human_limitations_missing"),
            pytest.param("legacy", "no_evidence", id="legacy_evidence_missing"),
            pytest.param(
                "legacy", "duplicate_evidence", id="legacy_evidence_duplicate"
            ),
            pytest.param("legacy", "no_limitations", id="legacy_limitations_missing"),
        ],
    )
    def test_method__deserialize__rejects_producer_evidence_drift(
        self, kind: ProducerKind, mutation: EvidenceMutation
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-PROVENANCE-003

        Requirement: Nonrepresented producers retain canonical evidence and limitations.

        Method: Remove evidence/limitations or duplicate a literal evidence identity.

        Oracle: Public nonempty, unique, sorted evidence and nonempty limitation rules.

        Acceptance: Corrupt failure with no partial run or commit binding.

        Interpretation: Missing provenance cannot silently become represented lineage.

        Limitations: This verifies representation rules, not evidence authenticity.
        """
        wire = self.wire(kind)
        if mutation == "no_evidence":
            original = (
                b'"evidence_identities":[{"fields":{"value":"evidence-a"},'
                b'"type":"ResultProducerEvidenceIdentity"},{"fields":{"value":"evidence-b"},'
                b'"type":"ResultProducerEvidenceIdentity"}]'
            )
            replacement = b'"evidence_identities":[]'
        elif mutation == "duplicate_evidence":
            original, replacement = b'"value":"evidence-b"', b'"value":"evidence-a"'
        else:
            original = (
                b'"limitations":["synthetic evidence only",'
                b'"no authentic provenance claim"]'
            )
            replacement = b'"limitations":[]'
        assert original in wire
        result = self.make_serializer().deserialize(wire.replace(original, replacement))
        assert result.status == "corrupt"
        assert result.failure is not None
        assert result.run is None and result.binding is None

    @pytest.mark.parametrize(
        ("kind", "original", "replacement"),
        [
            pytest.param(
                "task",
                b'"production_identity":{"fields":{"value":"production"},"type":"ResultProductionRecordIdentity"}',
                b'"production_identity":{"fields":{"value":"production"},"type":"ResultObjectReferenceIdentity"}',
                id="task_producer_wrong_production_type",
            ),
            pytest.param(
                "decision",
                b'"producer_provenance":{"fields":{"authority_context_identity":',
                b'"producer_provenance":{"fields":{"activation_identity":{"fields":{"value":"invented"},'
                b'"type":"TaskActivationIdentity"},"authority_context_identity":',
                id="decision_producer_forbids_task_lineage",
            ),
            pytest.param(
                "task",
                b'"value":"relation-b"',
                b'"value":"relation-a"',
                id="duplicate_production_relation",
            ),
            pytest.param(
                "task",
                b'"value":"native-b"',
                b'"value":"native-a"',
                id="duplicate_admitted_entry",
            ),
            pytest.param(
                "task",
                b'"manifest_entry_identities":[{"fields":{"value":"native-a"},"type":"ArtifactManifestEntryIdentity"},{"fields":{"value":"native-b"},"type":"ArtifactManifestEntryIdentity"}]',
                b'"manifest_entry_identities":[]',
                id="admission_entries_missing",
            ),
            pytest.param(
                "task",
                b'"dispatch_envelope_identity":{"fields":{"value":"dispatch-envelope"},"type":"SimulationDispatchObservationIdentity"}',
                b'"dispatch_envelope_identity":{"fields":{"value":"dispatch-envelope"},"type":"DispatchOutcomeRecordIdentity"}',
                id="admission_envelope_wrong_nominal_type",
            ),
        ],
    )
    def test_method__deserialize__rejects_represented_provenance_drift(
        self, kind: ProducerKind, original: bytes, replacement: bytes
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-PROVENANCE-004

        Requirement: Represented provenance and admissions retain exact types.

        Method: Mutate nominal fields, relation/entry lists or no-Task field shape.

        Oracle: Public closed producer shapes and canonical production/admission rules.

        Acceptance: Corrupt failure with no partial run or binding.

        Interpretation: Native correlations and no-Task origins cannot be reconstructed
        from malformed represented state.

        Limitations: No artifact contents, history closure or replay is checked.
        """
        wire = self.wire(kind)
        assert original in wire
        result = self.make_serializer().deserialize(wire.replace(original, replacement))
        assert result.status == "corrupt"
        assert result.failure is not None
        assert result.run is None and result.binding is None
