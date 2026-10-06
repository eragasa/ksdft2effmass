"""Synthetic payload-free fixtures for the local workflow runtime."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.workflows.v2.core import (
    WorkflowActorIdentity,
    WorkflowAdapterDisposition,
    WorkflowAdapterEvidence,
    WorkflowAdapterIdentity,
    WorkflowAuthorityReference,
    WorkflowDefinitionReference,
    WorkflowExternalReferenceIdentity,
    WorkflowIdempotencyIdentity,
    WorkflowOperationIdentity,
    WorkflowRunStarter,
    WorkflowRunStartResult,
    WorkflowSubjectIdentity,
    WorkflowTransitionInput,
    WorkflowTransitionPreflightInput,
    WorkflowTransitionRequest,
    WorkflowTypedReference,
)
from ksdft2effmass.workflows.v2.runtime import (
    AbstractWorkflowEffectReconciler,
    AbstractWorkflowForegroundWorker,
    WorkflowAuthorityRejectionRecorder,
    WorkflowAuthorityRejectionRecordingRequest,
    WorkflowAuthorityVerification,
    WorkflowForegroundActionResult,
    WorkflowForegroundDispatcher,
    WorkflowForegroundDispatchRequest,
    WorkflowForegroundExecutionRequest,
    WorkflowForegroundPlan,
    WorkflowForegroundReconciliationRecorder,
    WorkflowForegroundReconciliationRecordingRequest,
    WorkflowPlanRecorder,
    WorkflowPlanRecordingRequest,
    WorkflowReconciliationRequest,
    WorkflowRequestRetainer,
    WorkflowRequestRetentionRequest,
    WorkflowRunStartRecorder,
    WorkflowRunStartRecordingRequest,
    WorkflowRuntimeActionResult,
    WorkflowRuntimeRepository,
    WorkflowTransitionRecorder,
    WorkflowTransitionRecordingRequest,
)


class LocalWorkflowRuntimeHarness:
    """Test-only façade over exact production actionizer boundaries."""

    def __init__(self, repository: WorkflowRuntimeRepository) -> None:
        self.repository = repository

    def start(self, started: WorkflowRunStartResult) -> WorkflowRuntimeActionResult:
        actionizer = WorkflowRunStartRecorder(self.repository)
        request = WorkflowRunStartRecordingRequest.create(started=started)
        return actionizer.action(request=request)

    def retain_request(
        self, preflight: WorkflowTransitionPreflightInput
    ) -> WorkflowRuntimeActionResult:
        actionizer = WorkflowRequestRetainer(self.repository)
        request = WorkflowRequestRetentionRequest.create(preflight=preflight)
        return actionizer.action(request=request)

    def record_plan(
        self,
        preflight: WorkflowTransitionPreflightInput,
        plan: WorkflowForegroundPlan,
    ) -> WorkflowForegroundActionResult:
        actionizer = WorkflowPlanRecorder(self.repository)
        request = WorkflowPlanRecordingRequest.create(
            preflight=preflight,
            plan=plan,
        )
        return actionizer.action(request=request)

    def record_authority_rejection(
        self,
        preflight: WorkflowTransitionPreflightInput,
        plan: WorkflowForegroundPlan,
        verification: WorkflowAuthorityVerification,
    ) -> WorkflowForegroundActionResult:
        actionizer = WorkflowAuthorityRejectionRecorder(self.repository)
        request = WorkflowAuthorityRejectionRecordingRequest.create(
            preflight=preflight,
            plan=plan,
            verification=verification,
        )
        return actionizer.action(request=request)

    def dispatch_foreground(
        self,
        preflight: WorkflowTransitionPreflightInput,
        execution: WorkflowForegroundExecutionRequest,
        verification: WorkflowAuthorityVerification,
        worker: AbstractWorkflowForegroundWorker,
    ) -> WorkflowForegroundActionResult:
        actionizer = WorkflowForegroundDispatcher(self.repository, worker)
        request = WorkflowForegroundDispatchRequest.create(
            preflight=preflight,
            execution=execution,
            verification=verification,
        )
        return actionizer.action(request=request)

    def reconcile_foreground(
        self,
        preflight: WorkflowTransitionPreflightInput,
        reconciliation: WorkflowReconciliationRequest,
        reconciler: AbstractWorkflowEffectReconciler,
    ) -> WorkflowForegroundActionResult:
        actionizer = WorkflowForegroundReconciliationRecorder(
            self.repository,
            reconciler,
        )
        request = WorkflowForegroundReconciliationRecordingRequest.create(
            preflight=preflight,
            reconciliation=reconciliation,
        )
        return actionizer.action(request=request)

    def record_transition(
        self, transition: WorkflowTransitionInput
    ) -> WorkflowRuntimeActionResult:
        actionizer = WorkflowTransitionRecorder(self.repository)
        request = WorkflowTransitionRecordingRequest.create(transition=transition)
        return actionizer.action(request=request)


@dataclass(frozen=True, slots=True)
class RuntimeFixture:
    definition: WorkflowDefinitionReference
    operation: WorkflowOperationIdentity
    authority: WorkflowAuthorityReference
    started: WorkflowRunStartResult


def runtime_fixture() -> RuntimeFixture:
    operation = WorkflowOperationIdentity("record-course-candidate")
    definition = WorkflowDefinitionReference.create(
        contract_id="ksdft2effmass.workflows.v2.test-course-review",
        definition_version="1",
        definition_digest_sha256="a" * 64,
        operation_identities=(operation,),
    )
    subject = WorkflowSubjectIdentity("course:pacific_ENGR219")
    started = WorkflowRunStarter().execute(
        definition=definition,
        subject_identity=subject,
        run_key="course-review:pacific_ENGR219",
        initial_state_references=(
            WorkflowTypedReference(
                "course-review-status",
                WorkflowExternalReferenceIdentity("inventory-only"),
            ),
        ),
    )
    authority = WorkflowAuthorityReference.create(
        authority_kind="local-course-review-policy",
        subject_identity=subject,
        operation_identities=(operation,),
        evidence_identity=WorkflowExternalReferenceIdentity("policy:course-review:1"),
        authority_version="1",
    )
    return RuntimeFixture(definition, operation, authority, started)


def transition_input(
    fixture: RuntimeFixture,
    *,
    request_key: str = "candidate:1",
    expected_revision: int = 0,
    proposal_identity: str = "proposal-set:sha256:fixture",
) -> WorkflowTransitionInput:
    request = WorkflowTransitionRequest.create(
        run_identity=fixture.started.run.identity,
        expected_prior_state_identity=fixture.started.state.identity,
        expected_revision=expected_revision,
        operation_identity=fixture.operation,
        input_references=(
            WorkflowTypedReference(
                "organizer-proposal-set",
                WorkflowExternalReferenceIdentity(proposal_identity),
                "b" * 64,
            ),
        ),
        artifact_references=(),
        decision_references=(),
        actor_identity=WorkflowActorIdentity("agent:organizer"),
        authority_reference=fixture.authority,
        idempotency_identity=WorkflowIdempotencyIdentity(request_key),
    )
    evidence = WorkflowAdapterEvidence.create(
        adapter_identity=WorkflowAdapterIdentity("course-review-baseline:1"),
        definition_identity=fixture.definition.identity,
        request_identity=request.identity,
        prior_state_identity=fixture.started.state.identity,
        disposition=WorkflowAdapterDisposition.ENABLED,
        successor_state_references=(
            WorkflowTypedReference(
                "course-review-status",
                WorkflowExternalReferenceIdentity("manual-review-required"),
            ),
        ),
        successor_run_status=fixture.started.run.status,
        reasons=("metadata candidate requires manual review",),
    )
    return WorkflowTransitionInput(
        fixture.definition,
        fixture.started.run,
        fixture.started.state,
        request,
        evidence,
    )
