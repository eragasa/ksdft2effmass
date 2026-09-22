r"""Software verification of ``WorkflowRunSerializer``.

Bounded artifact scope: dispatch runtime observations, final records and dispositions.

Evidence profile: claim_bearing

Facet and represented meaning

An independent synthetic literal retains three runtime outcome variants, all five
observation kinds (including empty indeterminate evidence), three final outcome
kinds and four disposition kinds. Nested scalar values and structured failures
remain complete; ordered repeated observations are not deduplicated.

Intrinsic and cross-object scope

Public record construction and aggregate wire preservation only. The synthetic
aggregate deliberately omits the Task history needed for structural closure.

VVUQ and scientific exclusions

Software verification only, not scientific results, computed firing, replay equality,
authority authentication, artifact admission or exactly-once effect completion.
"""

from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass import analysis as q
from ksdft2effmass import workflows as w
from ksdft2effmass.workflows import WorkflowRunSerializer

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunSerializer


class TestWorkflowRunSerializer:
    """Own literal dispatch representation evidence, not execution evidence."""

    @staticmethod
    def wire(retryable: bool | None = None) -> bytes:
        wire = (
            Path(__file__)
            .with_name("resources")
            .joinpath("workflow-run-dispatch-variants-v1.json")
            .read_bytes()
        )
        if retryable is None:
            return wire
        return wire.replace(
            b'"retryable":null',
            b'"retryable":true' if retryable else b'"retryable":false',
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

    def make_runtime(
        self, kind: w.DispatchOutcomeKind, retryable: bool | None
    ) -> w.SimulationDispatchOutcome:
        return w.SimulationDispatchOutcome(
            identity=w.SimulationDispatchOutcomeIdentity("outcome"),
            observation_identity=w.SimulationDispatchObservationIdentity(
                f"envelope-{kind.value}"
            ),
            request_identity=w.SimulationExecutionRequestIdentity("request"),
            workflow_run_identity=w.WorkflowRunIdentity("run"),
            task_instance_identity=w.TaskInstanceIdentity("task-instance"),
            activation_identity=w.TaskActivationIdentity("activation"),
            operation_identity=w.OperationIdentity("operation"),
            attempt_identity=w.AttemptIdentity("attempt"),
            executor_identity=w.ScientificExecutorIdentity("executor"),
            obligation_identity=w.ObligationIdentity("obligation"),
            grant_identity=w.ExecutionGrantIdentity("grant"),
            kind=kind,
            result=self.make_scalar()
            if kind is w.DispatchOutcomeKind.CONFIRMED
            else None,
            native_output_manifest_identity=(
                w.ArtifactManifestIdentity("manifest")
                if kind is w.DispatchOutcomeKind.CONFIRMED
                else None
            ),
            native_output_manifest_entry_identities=(
                (
                    w.ArtifactManifestEntryIdentity("native-a"),
                    w.ArtifactManifestEntryIdentity("native-b"),
                )
                if kind is w.DispatchOutcomeKind.CONFIRMED
                else ()
            ),
            failure=(
                w.TaskInvocationFailure(
                    identity=w.TaskInvocationFailureIdentity("failure"),
                    code="synthetic-rejection",
                    operation_phase="synthetic-dispatch",
                    diagnostic="synthetic failure only",
                    retryable=retryable,
                    claim_boundary=(
                        "no effect completion evidence",
                        "no successful firing",
                    ),
                )
                if kind is w.DispatchOutcomeKind.REJECTED
                else None
            ),
            reconciliation_identity_values=("read-runtime",)
            if kind is w.DispatchOutcomeKind.INDETERMINATE
            else (),
        )

    @staticmethod
    def make_observation(
        identity: str,
        kind: w.DispatchObservationKind,
        outcomes: tuple[w.SimulationDispatchOutcome, ...],
    ) -> w.DispatchObservationRecord:
        return w.DispatchObservationRecord(
            identity=w.DispatchObservationRecordIdentity(identity),
            workflow_run_identity=w.WorkflowRunIdentity("run"),
            request_identity=w.SimulationExecutionRequestIdentity("request"),
            obligation_identity=w.ObligationIdentity("obligation"),
            dispatch_entry_identity=w.SimulationDispatchEntryIdentity("entry"),
            dispatch_entry_receipt_identity=w.SimulationDispatchEntryReceiptIdentity(
                "entry-receipt"
            ),
            outcome_identity=w.SimulationDispatchOutcomeIdentity("outcome"),
            kind=kind,
            observed_outcomes=outcomes,
            reconciliation_identity_values=("read-observation-a", "read-observation-b"),
        )

    @staticmethod
    def make_outcome(kind: w.DispatchOutcomeKind) -> w.DispatchOutcomeRecord:
        return w.DispatchOutcomeRecord(
            identity=w.DispatchOutcomeRecordIdentity(f"final-{kind.value}"),
            envelope_identity=w.SimulationDispatchObservationIdentity(
                f"envelope-{kind.value}"
            ),
            workflow_run_identity=w.WorkflowRunIdentity("run"),
            request_identity=w.SimulationExecutionRequestIdentity("request"),
            task_instance_identity=w.TaskInstanceIdentity("task-instance"),
            activation_identity=w.TaskActivationIdentity("activation"),
            operation_identity=w.OperationIdentity("operation"),
            attempt_identity=w.AttemptIdentity("attempt"),
            executor_identity=w.ScientificExecutorIdentity("executor"),
            obligation_identity=w.ObligationIdentity("obligation"),
            grant_identity=w.ExecutionGrantIdentity("grant"),
            kind=kind,
            result_reference_identity=(
                w.ResultObjectReferenceIdentity("result-reference")
                if kind is w.DispatchOutcomeKind.CONFIRMED
                else None
            ),
            failure_record_identity=(
                w.TaskFailureRecordIdentity("failure-record")
                if kind is w.DispatchOutcomeKind.REJECTED
                else None
            ),
            reconciliation_identity_values=("read-outcome",)
            if kind is w.DispatchOutcomeKind.INDETERMINATE
            else (),
        )

    @staticmethod
    def make_disposition(kind: w.ObligationDispositionKind) -> w.ObligationDisposition:
        final = (
            "confirmed" if kind is w.ObligationDispositionKind.COMPLETED else kind.value
        )
        return w.ObligationDisposition(
            identity=w.ObligationDispositionIdentity(f"disposition-{kind.value}"),
            obligation_identity=w.ObligationIdentity("obligation"),
            request_identity=w.SimulationExecutionRequestIdentity("request"),
            dispatch_outcome_record_identity=w.DispatchOutcomeRecordIdentity(
                f"final-{final}"
            ),
            attempt_record_identity=w.TaskAttemptRecordIdentity("attempt-record"),
            kind=kind,
            predecessor_disposition_identity=(
                w.ObligationDispositionIdentity("disposition-confirmed")
                if kind is w.ObligationDispositionKind.COMPLETED
                else None
            ),
            reconciliation_identity_values=("read-disposition",)
            if kind is w.ObligationDispositionKind.INDETERMINATE
            else (),
        )

    def make_run(self, genesis: w.WorkflowRun, retryable: bool | None) -> w.WorkflowRun:
        confirmed = self.make_runtime(w.DispatchOutcomeKind.CONFIRMED, retryable)
        rejected = self.make_runtime(w.DispatchOutcomeKind.REJECTED, retryable)
        indeterminate = self.make_runtime(
            w.DispatchOutcomeKind.INDETERMINATE, retryable
        )
        return replace(
            genesis,
            dispatch_observations=(
                self.make_observation(
                    "confirmed",
                    w.DispatchObservationKind.CONFIRMED,
                    (confirmed, confirmed),
                ),
                self.make_observation(
                    "conflict",
                    w.DispatchObservationKind.CONFLICT,
                    (rejected, confirmed),
                ),
                self.make_observation(
                    "empty", w.DispatchObservationKind.INDETERMINATE, ()
                ),
                self.make_observation(
                    "error",
                    w.DispatchObservationKind.ERROR,
                    (
                        replace(
                            rejected,
                            identity=w.SimulationDispatchOutcomeIdentity(
                                "foreign-outcome"
                            ),
                        ),
                    ),
                ),
                self.make_observation(
                    "indeterminate",
                    w.DispatchObservationKind.INDETERMINATE,
                    (indeterminate,),
                ),
                self.make_observation(
                    "rejected", w.DispatchObservationKind.REJECTED, (rejected,)
                ),
            ),
            dispatch_outcomes=(
                self.make_outcome(w.DispatchOutcomeKind.CONFIRMED),
                self.make_outcome(w.DispatchOutcomeKind.INDETERMINATE),
                self.make_outcome(w.DispatchOutcomeKind.REJECTED),
            ),
            obligation_dispositions=(
                self.make_disposition(w.ObligationDispositionKind.COMPLETED),
                self.make_disposition(w.ObligationDispositionKind.CONFIRMED),
                self.make_disposition(w.ObligationDispositionKind.INDETERMINATE),
                self.make_disposition(w.ObligationDispositionKind.REJECTED),
            ),
        )

    @pytest.mark.parametrize(
        "retryable",
        [
            pytest.param(None, id="retryability_unknown"),
            pytest.param(False, id="not_retryable"),
            pytest.param(True, id="retryable"),
        ],
    )
    def test_method__serialize__matches_dispatch_literal(
        self, genesis_snapshot: w.WorkflowRunSnapshot, retryable: bool | None
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-DISPATCH-001

        Requirement: Dispatch records preserve full nested values and variant fields.

        Method: Encode a separately constructed aggregate with all dispatch kinds.

        Oracle: Literal wire authored without production serialization, retaining
        repeated observations, ordered conflict evidence and scalar signed-zero bytes.

        Acceptance: Complete canonical payload equals the independent literal.

        Interpretation: Structured diagnostics and reconciliation evidence survive.

        Limitations: No dispatch occurs; represented references are not closed history.
        """
        result = SUT(
            result_codec=q.QuantityOfInterestResultValueSerializer()
        ).serialize(
            self.make_run(genesis_snapshot.run, retryable), genesis_snapshot.binding
        )
        assert result.status == "encoded", result.failure
        assert result.encoded is not None
        assert result.encoded.payload == self.wire(retryable)

    @pytest.mark.parametrize(
        "retryable",
        [
            pytest.param(None, id="retryability_unknown"),
            pytest.param(False, id="not_retryable"),
            pytest.param(True, id="retryable"),
        ],
    )
    def test_method__deserialize__restores_dispatch_literal(
        self, genesis_snapshot: w.WorkflowRunSnapshot, retryable: bool | None
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-DISPATCH-002

        Requirement: Dispatch decoding reconstructs complete concrete domain records.

        Method: Decode independent literal bytes and compare public constructors.

        Oracle: Full independently constructed aggregate and commit binding.

        Acceptance: Run and binding compare equal, including ordered multiplicity.

        Interpretation: Values are concrete records, not identity-only stand-ins.

        Limitations: Equality does not establish scientific meaning or valid execution.
        """
        result = SUT(
            result_codec=q.QuantityOfInterestResultValueSerializer()
        ).deserialize(self.wire(retryable))
        assert result.status == "decoded", result.failure
        assert result.run == self.make_run(genesis_snapshot.run, retryable)
        assert result.binding == genesis_snapshot.binding

    @pytest.mark.parametrize(
        ("original", "replacement"),
        [
            pytest.param(
                b'"native_output_manifest_identity":{"fields":{"value":"manifest"},"type":"ArtifactManifestIdentity"}',
                b'"native_output_manifest_identity":null',
                id="confirmed_manifest_missing",
            ),
            pytest.param(
                b'"value":"native-b"',
                b'"value":"native-a"',
                id="duplicate_native_entry",
            ),
            pytest.param(
                b'"retryable":null',
                b'"retryable":"true"',
                id="failure_retryability_string",
            ),
            pytest.param(
                b'"kind":{"fields":{"value":"conflict"},"type":"DispatchObservationKind"}',
                b'"kind":{"fields":{"value":"confirmed"},"type":"DispatchObservationKind"}',
                id="mixed_confirmed_observation",
            ),
            pytest.param(
                b'"kind":{"fields":{"value":"indeterminate"},"type":"DispatchObservationKind"},'
                b'"obligation_identity":{"fields":{"value":"obligation"},"type":"ObligationIdentity"},'
                b'"observed_outcomes":[]',
                b'"kind":{"fields":{"value":"error"},"type":"DispatchObservationKind"},'
                b'"obligation_identity":{"fields":{"value":"obligation"},"type":"ObligationIdentity"},'
                b'"observed_outcomes":[]',
                id="empty_error_observation",
            ),
            pytest.param(
                b'"reconciliation_identity_values":["read-runtime"]',
                b'"reconciliation_identity_values":[]',
                id="indeterminate_runtime_evidence_missing",
            ),
            pytest.param(
                b'"reconciliation_identity_values":["read-outcome"]',
                b'"reconciliation_identity_values":[]',
                id="indeterminate_final_evidence_missing",
            ),
            pytest.param(
                b'"reconciliation_identity_values":["read-disposition"]',
                b'"reconciliation_identity_values":[]',
                id="indeterminate_disposition_evidence_missing",
            ),
            pytest.param(
                b'"predecessor_disposition_identity":{"fields":{"value":"disposition-confirmed"},"type":"ObligationDispositionIdentity"}',
                b'"predecessor_disposition_identity":null',
                id="completed_predecessor_missing",
            ),
            pytest.param(
                b'"failure_record_identity":{"fields":{"value":"failure-record"},"type":"TaskFailureRecordIdentity"}',
                b'"failure_record_identity":null',
                id="rejected_final_failure_missing",
            ),
        ],
    )
    def test_method__deserialize__rejects_dispatch_variant_drift(
        self, original: bytes, replacement: bytes
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-DISPATCH-003

        Requirement: Nested dispatch payloads must satisfy their public closed variants.

        Method: Change one named field pattern in the independent canonical literal.

        Oracle: Public manifest, typed-failure, observation-kind and disposition rules.

        Acceptance: Corrupt failure with no partial reconstructed run or binding.

        Interpretation: Valid JSON cannot bypass dispatch record invariants.

        Limitations: Does not establish history closure, replay or artifact validity.
        """
        wire = self.wire()
        assert original in wire
        result = SUT(
            result_codec=q.QuantityOfInterestResultValueSerializer()
        ).deserialize(wire.replace(original, replacement))
        assert result.status == "corrupt"
        assert result.failure is not None
        assert result.run is None and result.binding is None
