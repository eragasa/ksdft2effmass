r"""Software verification of ``WorkflowRun``.

Evidence profile: routine

Bounded artifact scope: the public ``WorkflowRun`` contract.

Facet and represented meaning

This module verifies intrinsic represented behavior owned by ``WorkflowRun``.

Intrinsic and cross-object scope

Constructor and field invariants belong to this class. Complete cross-record replay
and package-export agreement remain with their separate owners.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import dataclass, fields, replace
from typing import Literal

import pytest

from ksdft2effmass import workflows as w
from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetDefinitionIdentity,
    ColoredPetriNetMarking,
    ColoredPetriNetMarkingIdentity,
)
from ksdft2effmass.workflows import (
    ResultObjectIdentity,
    TaskDefinitionIdentity,
    TaskInstance,
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from ksdft2effmass.workflows.runs import (
    ExternalProducerAttemptIdentity,
    ExternalResultProducer,
    ExternalResultProducerIdentity,
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectReference,
    ResultObjectReferenceIdentity,
    ResultObjectTypeIdentity,
    ResultProducerEvidenceIdentity,
    ResultProducerProvenanceIdentity,
    TaskWorkflowMembership,
    TaskWorkflowMembershipIdentity,
    WorkflowDefinitionReferenceIdentity,
    WorkflowRun,
    WorkflowRunRevisionIdentity,
    WorkflowRuntimeBundleIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowRun


@dataclass(frozen=True, slots=True)
class _SyntheticResult:
    """Provide one exact immutable ResultObject for software verification."""

    identity: ResultObjectIdentity


class TestWorkflowRun:
    """Own software evidence for ``WorkflowRun``."""

    def test_field__public_inventory__matches_exact_names(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-WORKFLOW-RUN-001

        Requirement: ``WorkflowRun`` declares exactly its documented public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "revision_identity",
            "predecessor_revision_identity",
            "workflow_identity",
            "definition_reference_identity",
            "runtime_bundle_identity",
            "schema_version",
            "adapter_implementation_identity",
            "task_instances",
            "task_memberships",
            "nested_memberships",
            "nested_invocations",
            "activations",
            "attempts",
            "outcomes",
            "result_references",
            "result_productions",
            "native_output_admissions",
            "result_dependencies",
            "failures",
            "authorization_results",
            "authority_references",
            "execution_request_correlations",
            "authority_reservations",
            "dispatch_obligations",
            "dispatch_entries",
            "dispatch_observations",
            "dispatch_outcomes",
            "obligation_dispositions",
            "scientific_decision_requests",
            "scientific_decision_resolutions",
            "initial_marking",
            "current_marking",
            "transitions",
            "nested_invocation_intents",
            "nested_terminal_observations",
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

    @pytest.mark.parametrize(
        "collision,diagnostic",
        (
            pytest.param("child", "child run identities", id="shared_child_run"),
            pytest.param(
                "key", "child creation idempotency identities", id="shared_creation_key"
            ),
            pytest.param(
                "attempt",
                "nested stable attempt identities",
                id="shared_stable_attempt",
            ),
        ),
    )
    def test_constructor__nested_sources__rejects_cross_source_collision(
        self, collision: Literal["child", "key", "attempt"], diagnostic: str
    ) -> None:
        """Enforce one child/key/attempt across old and separate intent records.

        Evidence ID: SV-WFR-AGGREGATE-NESTED-001

        Requirement: Combined and separate intent sources share child, creation-key
        and stable-attempt uniqueness, not independent uniqueness namespaces.

        Method: Supply two intrinsically valid sources, changing exactly one
        separate-source key to the combined source's key.

        Oracle: The named aggregate uniqueness invariant.

        Acceptance: Construction raises ValueError for that exact key family.

        Interpretation: An additional source cannot shadow retained child intent.

        Limitations: Constructor evidence does not resolve membership or persistence.
        """
        combined = self.make_combined()
        separate = self.make_intent("separate")
        match collision:
            case "child":
                separate = replace(
                    separate,
                    child_workflow_run_identity=combined.child_workflow_run_identity,
                )
            case "key":
                separate = replace(
                    separate,
                    child_creation_idempotency_identity=combined.child_creation_idempotency_identity,
                )
            case "attempt":
                separate = replace(separate, attempt_identity=combined.attempt_identity)
        with pytest.raises(ValueError, match=diagnostic):
            replace(
                self.make_run(()),
                nested_invocations=(combined,),
                nested_invocation_intents=(separate,),
            )

    def test_constructor__nested_identities__preserves_equal_string_nominals(
        self,
    ) -> None:
        """Permit equal label strings without merging two nominal source types.

        Evidence ID: SV-WFR-AGGREGATE-NESTED-002

        Requirement: Source record identity uniqueness preserves nominal type.

        Method: Construct distinct child/key/attempt sources sharing only their
        record identity string, one combined and one separate.

        Oracle: Independently supplied exact source records.

        Acceptance: Construction retains both sources exactly.

        Interpretation: The aggregate does not deduplicate nominally distinct links.

        Limitations: Structural terminal selection is separately repository-owned.
        """
        combined = self.make_combined()
        separate = replace(
            self.make_intent("separate"),
            identity=w.NestedWorkflowInvocationIntentIdentity(combined.identity.value),
        )
        run = replace(
            self.make_run(()),
            nested_invocations=(combined,),
            nested_invocation_intents=(separate,),
        )
        assert run.nested_invocations == (combined,)
        assert run.nested_invocation_intents == (separate,)

    @pytest.mark.parametrize(
        "collision,diagnostic",
        (
            pytest.param(
                "identity",
                "nested observation identities",
                id="repeated_observation_identity",
            ),
            pytest.param(
                "attempt",
                "nested observation terminal attempt identities",
                id="repeated_terminal_attempt",
            ),
            pytest.param(
                "outcome",
                "nested observation outcome identities",
                id="repeated_outcome_target",
            ),
        ),
    )
    def test_constructor__nested_observations__rejects_duplicate_targets(
        self, collision: Literal["identity", "attempt", "outcome"], diagnostic: str
    ) -> None:
        """Keep observation identities and terminal targets unique.

        Evidence ID: SV-WFR-AGGREGATE-NESTED-003

        Requirement: Distinct observation records cannot share an observation
        identity, terminal-attempt target or generic outcome target.

        Method: Append a second observation for a distinct nominal intent and
        duplicate only the selected target.

        Oracle: The named aggregate uniqueness invariant.

        Acceptance: Construction raises ValueError for that target family.

        Interpretation: Dictionary construction cannot silently discard evidence.

        Limitations: The synthetic observation references are not structurally resolved.
        """
        first = self.make_observation(
            "a", w.NestedWorkflowTerminalObservationKind.INDETERMINATE
        )
        second = self.make_observation(
            "b", w.NestedWorkflowTerminalObservationKind.INDETERMINATE
        )
        match collision:
            case "identity":
                second = replace(second, identity=first.identity)
            case "attempt":
                second = replace(
                    second,
                    terminal_attempt_record_identity=first.terminal_attempt_record_identity,
                )
            case "outcome":
                second = replace(second, outcome_identity=first.outcome_identity)
        with pytest.raises(ValueError, match=diagnostic):
            replace(self.make_run(()), nested_terminal_observations=(first, second))

    @pytest.mark.parametrize(
        "kind",
        (
            pytest.param(
                w.NestedWorkflowTerminalObservationKind.CONFIRMED, id="after_confirmed"
            ),
            pytest.param(
                w.NestedWorkflowTerminalObservationKind.REJECTED, id="after_rejected"
            ),
            pytest.param(
                w.NestedWorkflowTerminalObservationKind.INDETERMINATE,
                id="after_indeterminate",
            ),
        ),
    )
    def test_constructor__first_terminal__rejects_appended_second(
        self, kind: w.NestedWorkflowTerminalObservationKind
    ) -> None:
        """Retain first terminal and reject a distinct appended second observation.

        Evidence ID: SV-WFR-AGGREGATE-NESTED-004

        Requirement: Each intent has at most one first-terminal observation,
        including when the first is indeterminate.

        Method: Retain the original observation and append an intrinsically valid
        second with distinct record/attempt/outcome identities but the same intent.

        Oracle: The unique observed-intent invariant, not history-removal rejection.

        Acceptance: ValueError identifies duplicate observed intent; the original
        aggregate still contains its unchanged first observation.

        Interpretation: Append-only history does not permit a second terminal.

        Limitations: Constructor rejection occurs before any repository submission.
        """
        first = self.make_observation("a", kind)
        retained = replace(self.make_run(()), nested_terminal_observations=(first,))
        second = replace(
            self.make_observation("b", kind), intent_identity=first.intent_identity
        )
        with pytest.raises(ValueError, match="nested observed intent identities"):
            replace(retained, nested_terminal_observations=(first, second))
        assert retained.nested_terminal_observations == (first,)

    @staticmethod
    def make_intent(label: str) -> w.NestedWorkflowInvocationIntent:
        """Supply a synthetic source with independent child and invocation labels."""
        return w.NestedWorkflowInvocationIntent(
            identity=w.NestedWorkflowInvocationIntentIdentity(label),
            parent_workflow_run_identity=WorkflowRunIdentity("run.one"),
            parent_revision_identity=WorkflowRunRevisionIdentity("revision.one"),
            parent_task_instance_identity=TaskInstanceIdentity(label),
            activation_identity=w.TaskActivationIdentity(label),
            operation_identity=w.OperationIdentity(label),
            attempt_identity=w.AttemptIdentity(label),
            started_attempt_record_identity=w.TaskAttemptRecordIdentity(label),
            child_workflow_identity=WorkflowIdentity("child.workflow"),
            child_workflow_run_identity=WorkflowRunIdentity(label),
            input_result_reference_identities=(),
            child_creation_idempotency_identity=w.ChildWorkflowCreationIdempotencyIdentity(
                label
            ),
        )

    @classmethod
    def make_combined(cls) -> w.NestedWorkflowInvocation:
        """Adapt a synthetic source's fixed fields to the retained combined form."""
        source = cls.make_intent("combined")
        return w.NestedWorkflowInvocation(
            identity=w.NestedWorkflowInvocationIdentity(source.identity.value),
            parent_workflow_run_identity=source.parent_workflow_run_identity,
            parent_revision_identity=source.parent_revision_identity,
            parent_task_instance_identity=source.parent_task_instance_identity,
            activation_identity=source.activation_identity,
            operation_identity=source.operation_identity,
            attempt_identity=source.attempt_identity,
            attempt_record_identity=source.started_attempt_record_identity,
            child_workflow_identity=source.child_workflow_identity,
            child_workflow_run_identity=source.child_workflow_run_identity,
            input_result_reference_identities=(),
            child_creation_idempotency_identity=source.child_creation_idempotency_identity,
            kind=w.NestedWorkflowInvocationKind.PENDING,
        )

    @staticmethod
    def make_observation(
        label: str, kind: w.NestedWorkflowTerminalObservationKind
    ) -> w.NestedWorkflowTerminalObservation:
        """Supply explicit terminal variant fields for aggregate-only inputs."""
        return w.NestedWorkflowTerminalObservation(
            identity=w.NestedWorkflowObservationIdentity(label),
            intent_identity=w.NestedWorkflowInvocationIntentIdentity(label),
            parent_workflow_run_identity=WorkflowRunIdentity("run.one"),
            parent_revision_identity=WorkflowRunRevisionIdentity("terminal"),
            terminal_attempt_record_identity=w.TaskAttemptRecordIdentity(label),
            outcome_identity=w.TaskInvocationOutcomeIdentity(label),
            kind=kind,
            terminal_child_revision_identity=WorkflowRunRevisionIdentity(
                "child.terminal"
            )
            if kind is w.NestedWorkflowTerminalObservationKind.CONFIRMED
            else None,
            replay_equal_child_result_identity=w.WorkflowRunReplayResultIdentity(
                "c" * 64
            )
            if kind is w.NestedWorkflowTerminalObservationKind.CONFIRMED
            else None,
            exported_result_reference_identities=(ResultObjectReferenceIdentity(label),)
            if kind is w.NestedWorkflowTerminalObservationKind.CONFIRMED
            else (),
            export_admission_dependency_identities=(w.ResultDependencyIdentity(label),)
            if kind is w.NestedWorkflowTerminalObservationKind.CONFIRMED
            else (),
            failure_record_identity=w.TaskFailureRecordIdentity(label)
            if kind is w.NestedWorkflowTerminalObservationKind.REJECTED
            else None,
            reconciliation_identity_values=(label,)
            if kind is w.NestedWorkflowTerminalObservationKind.INDETERMINATE
            else (),
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
        marking = TestWorkflowRun.make_marking("marking.initial")
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
            native_output_admissions=(),
            result_dependencies=(),
            failures=(),
            authorization_results=(),
            authority_references=(),
            execution_request_correlations=(),
            authority_reservations=(),
            dispatch_obligations=(),
            dispatch_entries=(),
            dispatch_observations=(),
            dispatch_outcomes=(),
            obligation_dispositions=(),
            scientific_decision_requests=(),
            scientific_decision_resolutions=(),
            initial_marking=marking,
            current_marking=marking,
            transitions=(),
        )
