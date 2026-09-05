r"""Software verification of WorkflowRun task-origin and nested-run records.

Evidence profile: routine

Bounded artifact scope: immutable task-origin, membership, and nested-run records.

Facet and represented meaning

The artifact records one represented run revision, bounded Task attempts, ordinary
membership, distinct child-run correlation, closed invocation outcomes, successful
transition history, and exact marking snapshots.

Intrinsic and cross-object scope

Tests cover exact public constructor discrimination, retry locality, immutable
collection shape, identity uniqueness, distinct parent/child runs, and closed nested
observations. Replay correlation belongs to ``WorkflowRunReplayer`` and is tested
separately.

VVUQ and scientific exclusions

This is software verification only. It establishes no Task execution, persistence,
scientific calculation, validation, uncertainty quantification, authority, or human
acceptance.
"""

from dataclasses import dataclass, replace

import pytest

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetDefinitionIdentity,
    ColoredPetriNetMarking,
    ColoredPetriNetMarkingIdentity,
)
from ksdft2effmass.workflows import (
    AttemptIdentity,
    OperationIdentity,
    ResultObjectIdentity,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskInstance,
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from ksdft2effmass.workflows.runs import (
    ChildWorkflowCreationIdempotencyIdentity,
    ExternalProducerAttemptIdentity,
    ExternalResultProducer,
    ExternalResultProducerIdentity,
    HumanAuthoredResultProducer,
    HumanResultAuthorIdentity,
    ImportedRetainedResultProducer,
    NestedWorkflowInvocation,
    NestedWorkflowInvocationIdentity,
    NestedWorkflowInvocationKind,
    NestedWorkflowMembership,
    NestedWorkflowMembershipIdentity,
    NestedWorkflowObservationIdentity,
    RepresentedTaskResultProducer,
    ResultDependencyIdentity,
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectReference,
    ResultObjectReferenceIdentity,
    ResultObjectTypeIdentity,
    ResultProducerEvidenceIdentity,
    ResultProducerProvenanceIdentity,
    ResultProductionRecordIdentity,
    RetainedResultSourceIdentity,
    TaskAttempt,
    TaskAttemptRecordIdentity,
    TaskAttemptStatus,
    TaskFailureRecordIdentity,
    TaskInvocationFailure,
    TaskInvocationFailureIdentity,
    TaskInvocationOutcome,
    TaskInvocationOutcomeIdentity,
    TaskInvocationOutcomeKind,
    TaskWorkflowMembership,
    TaskWorkflowMembershipIdentity,
    UnknownLegacyResultProducer,
    WorkflowDefinitionReference,
    WorkflowDefinitionReferenceIdentity,
    WorkflowRun,
    WorkflowRunReplayResultIdentity,
    WorkflowRunRevisionIdentity,
    WorkflowRuntimeBundleIdentity,
)

pytestmark = pytest.mark.software_verification


@dataclass(frozen=True, slots=True)
class _SyntheticResult:
    """Provide one exact immutable ResultObject for software verification."""

    identity: ResultObjectIdentity


class TestWorkflowRunRecords:
    """Own software evidence for the cohesive WorkflowRun record artifact."""

    @staticmethod
    def make_failure() -> TaskInvocationFailure:
        """Construct one bounded synthetic Task-domain failure."""
        return TaskInvocationFailure(
            identity=TaskInvocationFailureIdentity("failure.one"),
            code="synthetic_failure",
            operation_phase="test_operation",
            diagnostic="synthetic software-verification failure",
            retryable=False,
            claim_boundary=("synthetic software-verification input",),
        )

    @staticmethod
    def make_marking(identity: str) -> ColoredPetriNetMarking:
        """Construct one empty semantic marking for record tests."""
        return ColoredPetriNetMarking(
            ColoredPetriNetMarkingIdentity(identity),
            ColoredPetriNetDefinitionIdentity("definition.one"),
            (),
        )

    @staticmethod
    def make_run(task_instances: tuple[TaskInstance, ...]) -> WorkflowRun:
        """Construct one transition-free WorkflowRun revision."""
        marking = TestWorkflowRunRecords.make_marking("marking.initial")
        return WorkflowRun(
            identity=WorkflowRunIdentity("run.one"),
            revision_identity=WorkflowRunRevisionIdentity("revision.one"),
            predecessor_revision_identity=None,
            workflow_identity=WorkflowIdentity("workflow.one"),
            definition_reference_identity=WorkflowDefinitionReferenceIdentity(
                "definition-reference.one"
            ),
            runtime_bundle_identity=WorkflowRuntimeBundleIdentity("bundle.one"),
            schema_version=1,
            adapter_implementation_identity="adapter.one",
            task_instances=task_instances,
            task_memberships=tuple(
                TaskWorkflowMembership(
                    identity=TaskWorkflowMembershipIdentity(
                        f"membership.{instance.identity.value}"
                    ),
                    workflow_run_identity=WorkflowRunIdentity("run.one"),
                    workflow_identity=WorkflowIdentity("workflow.one"),
                    task_instance_identity=instance.identity,
                )
                for instance in task_instances
            ),
            nested_memberships=(),
            nested_invocations=(),
            activations=(),
            attempts=(),
            outcomes=(),
            result_references=(),
            result_productions=(),
            result_dependencies=(),
            failures=(),
            authority_references=(),
            execution_request_correlations=(),
            authority_reservations=(),
            dispatch_obligations=(),
            dispatch_outcomes=(),
            obligation_dispositions=(),
            scientific_decision_requests=(),
            scientific_decision_resolutions=(),
            initial_marking=marking,
            current_marking=marking,
            transitions=(),
        )

    def test_constructor__invocation_outcome__enforces_closed_variants(self) -> None:
        """Reject fields that do not match the represented invocation outcome.

        Evidence ID: SV-WFR-RECORDS-001

        Requirement: Confirmed contains results only, rejected contains one failure
        only, and indeterminate contains reconciliation identities only.

        Acceptance: Each valid variant constructs and a confirmed outcome without a
        result raises ``ValueError``.
        """
        activation_identity = self.make_activation_identity()
        operation_identity = OperationIdentity("operation.one")
        attempt_identity = AttemptIdentity("attempt.one")
        terminal_record_identity = TaskAttemptRecordIdentity("attempt.one.confirmed")
        production_identity = ResultProductionRecordIdentity("production.one")
        producer = RepresentedTaskResultProducer(
            identity=ResultProducerProvenanceIdentity("producer.one"),
            workflow_identity=WorkflowIdentity("workflow.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            task_instance_identity=TaskInstanceIdentity("instance.one"),
            activation_identity=activation_identity,
            operation_identity=operation_identity,
            attempt_identity=attempt_identity,
            terminal_attempt_record_identity=terminal_record_identity,
            outcome_identity=TaskInvocationOutcomeIdentity("outcome.confirmed"),
            production_identity=production_identity,
        )
        result = ResultObjectReference(
            identity=ResultObjectReferenceIdentity("reference.one"),
            result=_SyntheticResult(ResultObjectIdentity("result.one")),
            concrete_type_identity=ResultObjectTypeIdentity("synthetic-result.v1"),
            owning_domain_identity=ResultObjectDomainIdentity("test.synthetic"),
            content_identity=ResultObjectContentIdentity("content.one"),
            producer_provenance=producer,
        )
        confirmed = TaskInvocationOutcome(
            identity=TaskInvocationOutcomeIdentity("outcome.confirmed"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            activation_identity=activation_identity,
            operation_identity=operation_identity,
            attempt_identity=attempt_identity,
            terminal_attempt_record_identity=terminal_record_identity,
            kind=TaskInvocationOutcomeKind.CONFIRMED,
            results=(result,),
            production_record_identities=(production_identity,),
        )
        rejected = TaskInvocationOutcome(
            identity=TaskInvocationOutcomeIdentity("outcome.rejected"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            activation_identity=activation_identity,
            operation_identity=operation_identity,
            attempt_identity=attempt_identity,
            terminal_attempt_record_identity=terminal_record_identity,
            kind=TaskInvocationOutcomeKind.REJECTED,
            failure_record_identity=TaskFailureRecordIdentity("failure-record.one"),
        )
        indeterminate = TaskInvocationOutcome(
            identity=TaskInvocationOutcomeIdentity("outcome.indeterminate"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            activation_identity=activation_identity,
            operation_identity=operation_identity,
            attempt_identity=attempt_identity,
            terminal_attempt_record_identity=terminal_record_identity,
            kind=TaskInvocationOutcomeKind.INDETERMINATE,
            reconciliation_identity_values=("reconciliation.one",),
        )

        assert confirmed.results == (result,)
        assert rejected.failure_record_identity == TaskFailureRecordIdentity(
            "failure-record.one"
        )
        assert indeterminate.reconciliation_identity_values == ("reconciliation.one",)
        with pytest.raises(ValueError):
            TaskInvocationOutcome(
                identity=TaskInvocationOutcomeIdentity("outcome.invalid"),
                workflow_run_identity=WorkflowRunIdentity("run.one"),
                activation_identity=activation_identity,
                operation_identity=operation_identity,
                attempt_identity=attempt_identity,
                terminal_attempt_record_identity=terminal_record_identity,
                kind=TaskInvocationOutcomeKind.CONFIRMED,
            )

    def test_constructor__task_attempt__rejects_self_record_predecessor(self) -> None:
        """Reject a terminal state record that names itself as predecessor.

        Evidence ID: SV-WFR-RECORDS-002

        Requirement: Attempt state is append-only and a terminal state record names
        an earlier distinct record for the same stable attempt.

        Acceptance: Equal state-record and predecessor identities raise ``ValueError``.
        """
        record_identity = TaskAttemptRecordIdentity("attempt.one.confirmed")
        with pytest.raises(ValueError):
            TaskAttempt(
                identity=record_identity,
                workflow_run_identity=WorkflowRunIdentity("run.one"),
                task_instance_identity=TaskInstanceIdentity("instance.one"),
                activation_identity=self.make_activation_identity(),
                operation_identity=OperationIdentity("operation.one"),
                attempt_identity=AttemptIdentity("attempt.one"),
                status=TaskAttemptStatus.CONFIRMED,
                predecessor_attempt_record_identity=record_identity,
            )

    def test_constructor__workflow_run__requires_unique_record_identities(self) -> None:
        """Reject duplicate identities in aggregate-owned collections.

        Evidence ID: SV-WFR-RECORDS-003

        Requirement: A WorkflowRun revision contains each run-scoped Task instance at
        most once.

        Acceptance: Repeating one exact Task instance raises ``ValueError``.
        """
        task_instance = TaskInstance(
            TaskInstanceIdentity("instance.one"),
            TaskDefinitionIdentity("task.one"),
            None,
        )

        with pytest.raises(ValueError):
            self.make_run((task_instance, task_instance))

    def test_constructor__nested_membership__requires_distinct_child_run(self) -> None:
        """Reject parent/child membership that reuses the parent run identity.

        Evidence ID: SV-WFR-RECORDS-004

        Requirement: A nested Workflow always owns a distinct child WorkflowRun.

        Acceptance: Equal parent and child run identities raise ``ValueError``.
        """
        with pytest.raises(ValueError):
            NestedWorkflowMembership(
                identity=NestedWorkflowMembershipIdentity("membership.nested.one"),
                parent_workflow_run_identity=WorkflowRunIdentity("run.one"),
                parent_revision_identity=WorkflowRunRevisionIdentity("revision.one"),
                parent_task_instance_identity=TaskInstanceIdentity("instance.one"),
                child_workflow_identity=WorkflowIdentity("workflow.child"),
                child_workflow_run_identity=WorkflowRunIdentity("run.one"),
            )

    def test_constructor__nested_invocation__enforces_closed_observations(self) -> None:
        """Admit only variant-appropriate nested terminal observation fields.

        Evidence ID: SV-WFR-RECORDS-005

        Requirement: Confirmed alone carries a replay-equal terminal child revision
        and paired exports/admissions; indeterminate carries reconciliation identities
        and exports nothing.

        Acceptance: Valid confirmed and indeterminate records construct, while a
        pending record containing a terminal observation raises ``ValueError``.
        """
        confirmed = self.make_nested_invocation(
            identity="invocation.one",
            kind=NestedWorkflowInvocationKind.CONFIRMED,
            terminal_observation_identity=NestedWorkflowObservationIdentity(
                "observation.one"
            ),
            terminal_child_revision_identity=WorkflowRunRevisionIdentity(
                "revision.child.terminal"
            ),
            replay_equal_child_result_identity=(self.make_replay_result_identity()),
            exported_result_reference_identities=(
                ResultObjectReferenceIdentity("reference.child"),
            ),
            export_admission_dependency_identities=(
                ResultDependencyIdentity("dependency.admission"),
            ),
        )
        indeterminate = self.make_nested_invocation(
            identity="invocation.two",
            kind=NestedWorkflowInvocationKind.INDETERMINATE,
            terminal_observation_identity=NestedWorkflowObservationIdentity(
                "observation.two"
            ),
            reconciliation_identity_values=("child-read.one",),
        )

        assert confirmed.child_workflow_run_identity == WorkflowRunIdentity("run.child")
        assert indeterminate.exported_result_reference_identities == ()
        with pytest.raises(ValueError):
            self.make_nested_invocation(
                identity="invocation.invalid",
                kind=NestedWorkflowInvocationKind.PENDING,
                terminal_observation_identity=NestedWorkflowObservationIdentity(
                    "observation.invalid"
                ),
            )

    def test_constructor__workflow_definition_reference__binds_exact_versions(
        self,
    ) -> None:
        """Bind Workflow, CPN, Task-definition, and schema versions explicitly.

        Evidence ID: SV-WFR-RECORDS-007

        Requirement: Replay input names one immutable definition reference with exact
        positive built-in integer versions and canonical Task-definition identities.

        Acceptance: The exact reference constructs and Boolean Workflow version raises
        ``TypeError``.
        """
        reference = WorkflowDefinitionReference(
            identity=WorkflowDefinitionReferenceIdentity("definition-reference.one"),
            workflow_identity=WorkflowIdentity("workflow.one"),
            workflow_definition_version=1,
            colored_petri_net_definition_identity=ColoredPetriNetDefinitionIdentity(
                "definition.one"
            ),
            colored_petri_net_definition_version=1,
            task_definition_identities=(TaskDefinitionIdentity("task.one"),),
            schema_version=1,
        )

        assert reference.workflow_definition_version == 1
        with pytest.raises(TypeError):
            replace(reference, workflow_definition_version=True)

    def test_constructor__result_producer_variants__retain_actual_evidence(
        self,
    ) -> None:
        """Require non-Workflow provenance to retain evidence and limitations.

        Evidence ID: SV-WFR-RECORDS-006

        Requirement: External, imported-retained, human-authored, and unknown-legacy
        producers are distinct closed variants with actual evidence and limitations,
        not fabricated Workflow lineage.

        Acceptance: Every variant constructs with canonical evidence; empty evidence
        raises ``ValueError``.
        """
        evidence = (ResultProducerEvidenceIdentity("evidence.one"),)
        limitations = ("synthetic software-verification provenance only",)
        external = ExternalResultProducer(
            identity=ResultProducerProvenanceIdentity("producer.external"),
            external_producer_identity=ExternalResultProducerIdentity("external.one"),
            producer_attempt_identity=ExternalProducerAttemptIdentity("attempt.one"),
            evidence_identities=evidence,
            limitations=limitations,
        )
        imported = ImportedRetainedResultProducer(
            identity=ResultProducerProvenanceIdentity("producer.imported"),
            source_identity=RetainedResultSourceIdentity("source.imported"),
            evidence_identities=evidence,
            limitations=limitations,
        )
        authored = HumanAuthoredResultProducer(
            identity=ResultProducerProvenanceIdentity("producer.authored"),
            author_identity=HumanResultAuthorIdentity("author.one"),
            source_identity=RetainedResultSourceIdentity("source.authored"),
            evidence_identities=evidence,
            limitations=limitations,
        )
        legacy = UnknownLegacyResultProducer(
            identity=ResultProducerProvenanceIdentity("producer.legacy"),
            source_identity=RetainedResultSourceIdentity("source.legacy"),
            evidence_identities=evidence,
            limitations=limitations,
        )

        assert tuple(
            type(producer) for producer in (external, imported, authored, legacy)
        ) == (
            ExternalResultProducer,
            ImportedRetainedResultProducer,
            HumanAuthoredResultProducer,
            UnknownLegacyResultProducer,
        )
        with pytest.raises(ValueError):
            replace(external, evidence_identities=())

    def test_constructor__workflow_run__rejects_provenance_collision_and_order(
        self,
    ) -> None:
        """Reject conflicting producer identities and noncanonical references.

        Evidence ID: SV-WFR-RECORDS-008

        Requirement: One provenance identity cannot name conflicting producer records,
        and aggregate collections use deterministic lexical identity ordering.

        Acceptance: Conflicting producer attempts and reversed distinct references
        each raise ``ValueError``.
        """
        run = self.make_run(())
        evidence = (ResultProducerEvidenceIdentity("evidence.one"),)
        limitations = ("synthetic software-verification provenance only",)
        first_producer = ExternalResultProducer(
            identity=ResultProducerProvenanceIdentity("producer.shared"),
            external_producer_identity=ExternalResultProducerIdentity("external.one"),
            producer_attempt_identity=ExternalProducerAttemptIdentity("attempt.one"),
            evidence_identities=evidence,
            limitations=limitations,
        )
        second_producer = replace(
            first_producer,
            producer_attempt_identity=ExternalProducerAttemptIdentity("attempt.two"),
        )
        first_reference = ResultObjectReference(
            identity=ResultObjectReferenceIdentity("reference.a"),
            result=_SyntheticResult(ResultObjectIdentity("result.a")),
            concrete_type_identity=ResultObjectTypeIdentity("synthetic-result.v1"),
            owning_domain_identity=ResultObjectDomainIdentity("test.external"),
            content_identity=ResultObjectContentIdentity("content.a"),
            producer_provenance=first_producer,
        )
        second_reference = ResultObjectReference(
            identity=ResultObjectReferenceIdentity("reference.b"),
            result=_SyntheticResult(ResultObjectIdentity("result.b")),
            concrete_type_identity=ResultObjectTypeIdentity("synthetic-result.v1"),
            owning_domain_identity=ResultObjectDomainIdentity("test.external"),
            content_identity=ResultObjectContentIdentity("content.b"),
            producer_provenance=second_producer,
        )

        with pytest.raises(ValueError, match="conflicting"):
            replace(run, result_references=(first_reference, second_reference))
        with pytest.raises(ValueError, match="lexical identity order"):
            replace(
                run,
                result_references=(
                    replace(
                        second_reference,
                        producer_provenance=replace(
                            second_producer,
                            identity=ResultProducerProvenanceIdentity("producer.two"),
                        ),
                    ),
                    first_reference,
                ),
            )

    @staticmethod
    def make_nested_invocation(
        *,
        identity: str,
        kind: NestedWorkflowInvocationKind,
        terminal_observation_identity: NestedWorkflowObservationIdentity | None = None,
        terminal_child_revision_identity: WorkflowRunRevisionIdentity | None = None,
        replay_equal_child_result_identity: WorkflowRunReplayResultIdentity
        | None = None,
        exported_result_reference_identities: tuple[
            ResultObjectReferenceIdentity, ...
        ] = (),
        export_admission_dependency_identities: tuple[
            ResultDependencyIdentity, ...
        ] = (),
        reconciliation_identity_values: tuple[str, ...] = (),
    ) -> NestedWorkflowInvocation:
        """Construct one nested invocation for closed-variant evidence."""
        return NestedWorkflowInvocation(
            identity=NestedWorkflowInvocationIdentity(identity),
            parent_workflow_run_identity=WorkflowRunIdentity("run.one"),
            parent_revision_identity=WorkflowRunRevisionIdentity("revision.one"),
            parent_task_instance_identity=TaskInstanceIdentity("instance.one"),
            activation_identity=TaskActivationIdentity("activation.one"),
            operation_identity=OperationIdentity("operation.one"),
            attempt_identity=AttemptIdentity("attempt.one"),
            attempt_record_identity=TaskAttemptRecordIdentity("attempt.one.confirmed"),
            child_workflow_identity=WorkflowIdentity("workflow.child"),
            child_workflow_run_identity=WorkflowRunIdentity("run.child"),
            input_result_reference_identities=(),
            child_creation_idempotency_identity=(
                ChildWorkflowCreationIdempotencyIdentity("child-create.one")
            ),
            kind=kind,
            terminal_observation_identity=terminal_observation_identity,
            terminal_child_revision_identity=terminal_child_revision_identity,
            replay_equal_child_result_identity=replay_equal_child_result_identity,
            exported_result_reference_identities=(exported_result_reference_identities),
            export_admission_dependency_identities=(
                export_admission_dependency_identities
            ),
            reconciliation_identity_values=reconciliation_identity_values,
        )

    @staticmethod
    def make_replay_result_identity() -> WorkflowRunReplayResultIdentity:
        """Construct one syntactically exact child replay-result identity."""
        return WorkflowRunReplayResultIdentity("a" * 64)

    @staticmethod
    def make_activation_identity() -> TaskActivationIdentity:
        """Construct the exact activation identity used by record tests."""
        return TaskActivationIdentity("activation.one")
