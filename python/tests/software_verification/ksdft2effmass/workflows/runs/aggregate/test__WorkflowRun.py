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

import pytest

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

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
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
            "result_dependencies",
            "failures",
            "authority_references",
            "execution_request_correlations",
            "authority_reservations",
            "dispatch_obligations",
            "dispatch_outcomes",
            "obligation_dispositions",
            "scientific_decision_requests",
            "scientific_decision_resolutions",
            "initial_marking",
            "current_marking",
            "transitions",
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
