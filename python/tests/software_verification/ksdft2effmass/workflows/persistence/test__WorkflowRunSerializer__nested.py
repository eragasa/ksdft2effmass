r"""Software verification of ``WorkflowRunSerializer``.

Bounded artifact scope: nested variants, memberships and dependency endpoints.

Evidence profile: claim_bearing

Facet and represented meaning

A literal aggregate and separate public constructors retain all four nested invocation
kinds, ordinary/nested memberships and all nullable dependency endpoint combinations.

Intrinsic and cross-object scope

The fixture contains supplied identities, not embedded child state. It deliberately
omits the activation, result and child histories required for structural closure.
The serializer neither creates children nor reads or replays their streams.

VVUQ and scientific exclusions

Synthetic software representation only; replay-result labels are not proof of replay
equality, cross-run atomicity, successful execution or scientific validity.
"""

from dataclasses import replace
from pathlib import Path

import pytest
from ksdft2effmass import workflows as w
from ksdft2effmass.analysis import QuantityOfInterestResultValueSerializer
from ksdft2effmass.workflows import WorkflowRunSerializer

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunSerializer


class TestWorkflowRunSerializer:
    """Own independent nested-record wires, not child execution evidence."""

    @staticmethod
    def wire() -> bytes:
        return (
            Path(__file__)
            .with_name("resources")
            .joinpath("workflow-run-nested-variants-v1.json")
            .read_bytes()
        )

    @staticmethod
    def make_invocation(
        kind: w.NestedWorkflowInvocationKind,
    ) -> w.NestedWorkflowInvocation:
        label = kind.value
        return w.NestedWorkflowInvocation(
            identity=w.NestedWorkflowInvocationIdentity(f"invocation-{label}"),
            parent_workflow_run_identity=w.WorkflowRunIdentity("run"),
            parent_revision_identity=w.WorkflowRunRevisionIdentity("genesis"),
            parent_task_instance_identity=w.TaskInstanceIdentity("task"),
            activation_identity=w.TaskActivationIdentity(f"activation-{label}"),
            operation_identity=w.OperationIdentity(f"operation-{label}"),
            attempt_identity=w.AttemptIdentity(f"attempt-{label}"),
            attempt_record_identity=w.TaskAttemptRecordIdentity(
                f"attempt-record-{label}"
            ),
            child_workflow_identity=w.WorkflowIdentity(f"child-definition-{label}"),
            child_workflow_run_identity=w.WorkflowRunIdentity(f"child-{label}"),
            input_result_reference_identities=(
                w.ResultObjectReferenceIdentity("input-a"),
                w.ResultObjectReferenceIdentity("input-b"),
            ),
            child_creation_idempotency_identity=w.ChildWorkflowCreationIdempotencyIdentity(
                f"creation-{label}"
            ),
            kind=kind,
            terminal_observation_identity=(
                w.NestedWorkflowObservationIdentity(f"observation-{label}")
                if kind is not w.NestedWorkflowInvocationKind.PENDING
                else None
            ),
            terminal_child_revision_identity=(
                w.WorkflowRunRevisionIdentity("child-terminal")
                if kind is w.NestedWorkflowInvocationKind.CONFIRMED
                else None
            ),
            replay_equal_child_result_identity=(
                w.WorkflowRunReplayResultIdentity("c" * 64)
                if kind is w.NestedWorkflowInvocationKind.CONFIRMED
                else None
            ),
            exported_result_reference_identities=(
                (
                    w.ResultObjectReferenceIdentity("export-a"),
                    w.ResultObjectReferenceIdentity("export-b"),
                )
                if kind is w.NestedWorkflowInvocationKind.CONFIRMED
                else ()
            ),
            export_admission_dependency_identities=(
                (
                    w.ResultDependencyIdentity("admit-a"),
                    w.ResultDependencyIdentity("admit-b"),
                )
                if kind is w.NestedWorkflowInvocationKind.CONFIRMED
                else ()
            ),
            failure_record_identity=(
                w.TaskFailureRecordIdentity("child-failure")
                if kind is w.NestedWorkflowInvocationKind.REJECTED
                else None
            ),
            reconciliation_identity_values=("child-read-a", "child-read-b")
            if kind is w.NestedWorkflowInvocationKind.INDETERMINATE
            else (),
        )

    @staticmethod
    def make_dependency(
        identity: str, represented: bool, activated: bool
    ) -> w.ResultDependency:
        return w.ResultDependency(
            identity=w.ResultDependencyIdentity(identity),
            result_reference_identity=w.ResultObjectReferenceIdentity(
                f"result-{identity}"
            ),
            producer_workflow_run_identity=w.WorkflowRunIdentity("producer-run")
            if represented
            else None,
            consumer_workflow_run_identity=w.WorkflowRunIdentity("run"),
            consumer_task_instance_identity=w.TaskInstanceIdentity("task"),
            consumer_activation_identity=w.TaskActivationIdentity("consumer-activation")
            if activated
            else None,
            input_name=f"input-{identity}",
        )

    def make_run(self, genesis: w.WorkflowRun) -> w.WorkflowRun:
        return replace(
            genesis,
            task_memberships=(
                w.TaskWorkflowMembership(
                    identity=w.TaskWorkflowMembershipIdentity("membership"),
                    workflow_run_identity=genesis.identity,
                    workflow_identity=genesis.workflow_identity,
                    task_instance_identity=w.TaskInstanceIdentity("task"),
                ),
            ),
            nested_memberships=(
                w.NestedWorkflowMembership(
                    identity=w.NestedWorkflowMembershipIdentity("nested-membership"),
                    parent_workflow_run_identity=genesis.identity,
                    parent_revision_identity=genesis.revision_identity,
                    parent_task_instance_identity=w.TaskInstanceIdentity("member-task"),
                    child_workflow_identity=w.WorkflowIdentity(
                        "member-child-definition"
                    ),
                    child_workflow_run_identity=w.WorkflowRunIdentity("member-child"),
                ),
            ),
            nested_invocations=(
                self.make_invocation(w.NestedWorkflowInvocationKind.CONFIRMED),
                self.make_invocation(w.NestedWorkflowInvocationKind.INDETERMINATE),
                self.make_invocation(w.NestedWorkflowInvocationKind.PENDING),
                self.make_invocation(w.NestedWorkflowInvocationKind.REJECTED),
            ),
            result_dependencies=(
                self.make_dependency("activated-external", False, True),
                self.make_dependency("activated-represented", True, True),
                self.make_dependency("pending-external", False, False),
                self.make_dependency("pending-represented", True, False),
            ),
        )

    def test_method__serialize__matches_nested_literal(
        self, genesis_snapshot: w.WorkflowRunSnapshot
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-NESTED-001

        Requirement: Nested kinds, memberships and nullable endpoints retain all fields.

        Method: Serialize a separately constructed public aggregate.

        Oracle: Independently authored canonical literal, not serializer output.

        Acceptance: The entire encoded payload equals the literal bytes.

        Interpretation: Scope, ordered exports and observation identities survive.

        Limitations: No child state, replay proof or closed history is supplied.
        """
        result = SUT(result_codec=QuantityOfInterestResultValueSerializer()).serialize(
            self.make_run(genesis_snapshot.run), genesis_snapshot.binding
        )
        assert result.status == "encoded", result.failure
        assert result.encoded is not None and result.encoded.payload == self.wire()

    def test_method__deserialize__restores_nested_literal(
        self, genesis_snapshot: w.WorkflowRunSnapshot
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-NESTED-002

        Requirement: Decode exact nested records without inferring child state.

        Method: Decode the independent literal and compare public constructor values.

        Oracle: Complete expected run and binding, including every optional field.

        Acceptance: Full run and binding compare equal.

        Interpretation: Pending, confirmed, rejected and indeterminate remain distinct.

        Limitations: Identities do not verify dependency or child histories.
        """
        result = SUT(
            result_codec=QuantityOfInterestResultValueSerializer()
        ).deserialize(self.wire())
        assert result.status == "decoded", result.failure
        assert result.run == self.make_run(genesis_snapshot.run)
        assert result.binding == genesis_snapshot.binding

    @pytest.mark.parametrize(
        ("original", "replacement"),
        [
            pytest.param(
                b'"value":"member-child"', b'"value":"run"', id="membership_self_child"
            ),
            pytest.param(
                b'"value":"child-confirmed"',
                b'"value":"run"',
                id="invocation_self_child",
            ),
            pytest.param(
                b'"kind":{"fields":{"value":"pending"},"type":"NestedWorkflowInvocationKind"}',
                b'"kind":{"fields":{"value":"confirmed"},"type":"NestedWorkflowInvocationKind"}',
                id="pending_fields_as_confirmed",
            ),
            pytest.param(
                b'"replay_equal_child_result_identity":{"fields":{"value":"'
                b"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
                b'"},"type":"WorkflowRunReplayResultIdentity"}',
                b'"replay_equal_child_result_identity":null',
                id="confirmed_replay_reference_missing",
            ),
            pytest.param(
                b'"terminal_child_revision_identity":{"fields":{"value":"child-terminal"},"type":"WorkflowRunRevisionIdentity"}',
                b'"terminal_child_revision_identity":null',
                id="confirmed_child_revision_missing",
            ),
            pytest.param(
                b'"export_admission_dependency_identities":[{"fields":{"value":"admit-a"},"type":"ResultDependencyIdentity"},{"fields":{"value":"admit-b"},"type":"ResultDependencyIdentity"}]',
                b'"export_admission_dependency_identities":[{"fields":{"value":"admit-a"},"type":"ResultDependencyIdentity"}]',
                id="exports_and_admissions_unpaired",
            ),
            pytest.param(
                b'"value":"export-b"',
                b'"value":"export-a"',
                id="duplicate_export_reference",
            ),
            pytest.param(
                b'"value":"input-b"', b'"value":"input-a"', id="duplicate_child_input"
            ),
            pytest.param(
                b'"failure_record_identity":{"fields":{"value":"child-failure"},"type":"TaskFailureRecordIdentity"}',
                b'"failure_record_identity":null',
                id="rejected_failure_missing",
            ),
            pytest.param(
                b'"reconciliation_identity_values":["child-read-a","child-read-b"]',
                b'"reconciliation_identity_values":[]',
                id="indeterminate_evidence_missing",
            ),
            pytest.param(
                b'"input_name":"input-activated-external"',
                b'"input_name":""',
                id="empty_dependency_input_name",
            ),
            pytest.param(
                b'"consumer_activation_identity":{"fields":{"value":"consumer-activation"},"type":"TaskActivationIdentity"}',
                b'"consumer_activation_identity":{"fields":{"value":"consumer-activation"},"type":"OperationIdentity"}',
                id="dependency_activation_wrong_nominal_type",
            ),
        ],
    )
    def test_method__deserialize__rejects_nested_record_drift(
        self, original: bytes, replacement: bytes
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-NESTED-003

        Requirement: Nested and dependency records obey their intrinsic contracts.

        Method: Alter explicit field patterns in the independent literal.

        Oracle: Distinct runs, closed variants, paired exports, canonical collections
        and typed nonempty dependency endpoints.

        Acceptance: Corrupt failure with no partial run or commit binding.

        Interpretation: Valid JSON cannot bypass local record invariants.

        Limitations: No child execution or cross-run validation occurs.
        """
        wire = self.wire()
        assert original in wire
        result = SUT(
            result_codec=QuantityOfInterestResultValueSerializer()
        ).deserialize(wire.replace(original, replacement))
        assert result.status == "corrupt"
        assert result.failure is not None
        assert result.run is None and result.binding is None
