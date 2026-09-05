r"""Software verification of WorkflowRun public package integration.

Evidence profile: routine

Bounded artifact scope: supported ``ksdft2effmass.workflows`` package-root exports
for the complete in-memory WorkflowRun and replay contract.

Facet and represented meaning

The artifact verifies the selected private rollout has reached its public integration
gate: complete WorkflowRun records and replay behavior are supported package imports.

Intrinsic and cross-object scope

Tests verify the exact package export inventory and retirement of the provisional
generic transition alias. Record invariants and replay behavior belong to separate
owners.

VVUQ and scientific exclusions

This is structural software verification only. Export presence establishes no
execution, persistence, scientific validation, uncertainty quantification, authority,
or human acceptance.
"""

from importlib.util import find_spec

import pytest

import ksdft2effmass.workflows as api
import ksdft2effmass.workflows.runs as runs_api

pytestmark = pytest.mark.software_verification


class TestWorkflowRunPublicApi:
    """Own package-boundary evidence for the complete WorkflowRun contract."""

    def test_public_api__package__exports_complete_workflow_run_contract(
        self,
    ) -> None:
        """Export every complete WorkflowRun name from the package root.

        Evidence ID: SV-WFR-PUBLIC-001

        Requirement: Selected rollout Option 1A publishes the cohesive WorkflowRun
        records and replayer only after complete aggregate and replay closure.

        Acceptance: The root and ``workflows.runs`` ``__all__`` values equal their
        exact approved inventories, every listed name is present, and both the
        withdrawn transition alias and superseded ``workflow_run`` module are absent.
        """
        approved_names = {
            "AuthorityContextIdentity",
            "AuthorityReservationOutcome",
            "AuthorityReservationOutcomeIdentity",
            "AuthorityReservationOutcomeKind",
            "BoundaryReceiptIdentity",
            "ChildWorkflowCreationIdempotencyIdentity",
            "DispatchCreationIdempotencyIdentity",
            "DispatchDestinationIdentity",
            "DispatchOutcomeKind",
            "DispatchOutcomeRecord",
            "DispatchOutcomeRecordIdentity",
            "DispatchResourceScopeIdentity",
            "ExecutionGrantIdentity",
            "ExecutionGrantRevisionIdentity",
            "ExternalProducerAttemptIdentity",
            "ExternalResultProducer",
            "ExternalResultProducerIdentity",
            "HumanAuthoredResultProducer",
            "HumanResultAuthorIdentity",
            "ImportedRetainedResultProducer",
            "NestedWorkflowInvocation",
            "NestedWorkflowInvocationIdentity",
            "NestedWorkflowInvocationKind",
            "NestedWorkflowMembership",
            "NestedWorkflowMembershipIdentity",
            "NestedWorkflowObservationIdentity",
            "ObligationDisposition",
            "ObligationDispositionIdentity",
            "ObligationDispositionKind",
            "ObligationIdentity",
            "RepresentedScientificDecisionIngressProducer",
            "ResponseSourceIdentity",
            "ScientificDecisionOption",
            "ScientificDecisionOptionIdentity",
            "ScientificDecisionRecorderIdentity",
            "ScientificDecisionRequest",
            "ScientificDecisionRequestIdentity",
            "ScientificDecisionResolution",
            "ScientificDecisionTransitionRecordIdentity",
            "ScientificDecisionWorkflowTransitionRecord",
            "ScientificExecutionAuthorityReference",
            "ScientificExecutionAuthoritySnapshotIdentity",
            "ScientificExecutionAuthorityStateIdentity",
            "ScientificExecutorIdentity",
            "SimulationDispatchObligation",
            "SimulationDispatchOutcomeIdentity",
            "SimulationExecutionAuthorizationResultIdentity",
            "SimulationExecutionRequestCorrelation",
            "SimulationExecutionRequestCorrelationIdentity",
            "SimulationExecutionRequestIdentity",
            "RetainedResultSourceIdentity",
            "TaskAttempt",
            "TaskAttemptRecordIdentity",
            "TaskAttemptStatus",
            "TaskFailureRecord",
            "TaskFailureRecordIdentity",
            "TaskInvocationFailure",
            "TaskInvocationFailureIdentity",
            "TaskInvocationOutcome",
            "TaskInvocationOutcomeIdentity",
            "TaskInvocationOutcomeKind",
            "TaskWorkflowMembership",
            "TaskWorkflowMembershipIdentity",
            "TaskWorkflowTransitionRecord",
            "TaskWorkflowTransitionRecordIdentity",
            "RepresentedTaskResultProducer",
            "ResultDependency",
            "ResultDependencyIdentity",
            "ResultObjectContentIdentity",
            "ResultObjectDomainIdentity",
            "ResultObjectReference",
            "ResultObjectReferenceIdentity",
            "ResultObjectTypeIdentity",
            "ResultProducerEvidenceIdentity",
            "ResultProducerProvenanceIdentity",
            "ResultProductionRecord",
            "ResultProductionRecordIdentity",
            "UnknownLegacyResultProducer",
            "WorkflowDefinitionReference",
            "WorkflowDefinitionReferenceIdentity",
            "WorkflowRun",
            "WorkflowRunReplayIssue",
            "WorkflowRunReplayIssueCode",
            "WorkflowRunReplayOutcomeKind",
            "WorkflowRunReplayResult",
            "WorkflowRunReplayResultIdentity",
            "WorkflowRunReplayer",
            "WorkflowRunRevisionIdentity",
            "WorkflowRuntimeBundle",
            "WorkflowRuntimeBundleIdentity",
            "WorkflowTransitionSequenceIdentity",
        }

        preexisting_names = {
            "AllOfTaskActivationSelection",
            "AnyOfTaskActivationSelection",
            "ArtifactContentIdentity",
            "ArtifactIdentity",
            "ArtifactLineageKind",
            "ArtifactLineageRelation",
            "ArtifactLineageRelationIdentity",
            "ArtifactLineageSourceIdentity",
            "ArtifactManifest",
            "ArtifactManifestEntry",
            "ArtifactManifestEntryIdentity",
            "ArtifactManifestIdentity",
            "ArtifactManifestSupersessionIdentity",
            "ArtifactProducerKind",
            "ArtifactProducerProvenance",
            "ArtifactProducerProvenanceIdentity",
            "AttemptIdentity",
            "ColoredPetriNetWorkflowActivationFailureCode",
            "ColoredPetriNetWorkflowActivationMode",
            "ColoredPetriNetWorkflowActivationOutcomeKind",
            "ColoredPetriNetWorkflowActivationRequest",
            "ColoredPetriNetWorkflowActivationResult",
            "ColoredPetriNetWorkflowActivationResultIdentity",
            "ColoredPetriNetWorkflowAdapter",
            "ColoredPetriNetWorkflowMapping",
            "ColoredPetriNetWorkflowSelectionPolicy",
            "DirectTaskActivationSelection",
            "ExternalSourceObservation",
            "HumanAuthoredCompactInput",
            "ImportedRetainedFixture",
            "OperationIdentity",
            "RepresentedWorkflowProducer",
            "ResultArtifactRelationIdentity",
            "ResultObject",
            "ResultObjectIdentity",
            "Task",
            "TaskActivation",
            "TaskActivationIdentity",
            "TaskActivationSelection",
            "TaskDefinitionIdentity",
            "TaskExecutionContext",
            "TaskGateSelection",
            "TaskInputBinding",
            "TaskInstance",
            "TaskInstanceIdentity",
            "TaskStartGate",
            "TaskStartGateIdentity",
            "TaskStartGateSet",
            "TaskStartGateSetIdentity",
            "TaskStartGateSetMode",
            "UnknownLegacyProducer",
            "Workflow",
            "WorkflowComposition",
            "WorkflowIdentity",
            "WorkflowResultTokenMapping",
            "WorkflowRunIdentity",
        }
        expected_names = preexisting_names | approved_names

        assert api.__all__ == sorted(expected_names)
        assert all(hasattr(api, name) for name in expected_names)
        assert runs_api.__all__ == sorted(approved_names)
        assert all(hasattr(runs_api, name) for name in approved_names)
        assert "WorkflowTransitionRecord" not in api.__all__
        assert not hasattr(api, "WorkflowTransitionRecord")
        assert find_spec("ksdft2effmass.workflows.workflow_run") is None
