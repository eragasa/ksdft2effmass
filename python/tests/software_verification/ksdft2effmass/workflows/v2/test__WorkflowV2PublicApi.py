"""Public API verification for provisional workflow v2."""

from __future__ import annotations

from importlib.util import find_spec

import ksdft2effmass.workflows.v2.persistence as persistence
import ksdft2effmass.workflows.v2.runtime as runtime


class TestWorkflowV2PublicApi:
    """Require explicit v2 package surfaces without compatibility aliases."""

    def test__persistence__exports_exact_revision_surface(self) -> None:
        assert persistence.__all__ == [
            "AtomicRevisionStore",
            "Revision",
            "RevisionCommit",
            "RevisionCommitResult",
            "RevisionCommitStatus",
            "RevisionReadRequest",
            "RevisionReadResult",
            "RevisionReadStatus",
            "RevisionSelector",
            "SQLiteAtomicRevisionStore",
        ]

    def test__runtime__exports_exact_foreground_surface(self) -> None:
        expected = {
            "AbstractWorkflowEffectReconciler",
            "AbstractWorkflowForegroundWorker",
            "WORKFLOW_RUNTIME_CONTRACT_VERSION",
            "WORKFLOW_RUNTIME_IMPLEMENTATION_IDENTITY",
            "WorkflowAdapterConfigurationIdentity",
            "WorkflowAttemptIdentity",
            "WorkflowAuthorityRejectionRecorder",
            "WorkflowAuthorityRejectionRecordingRequest",
            "WorkflowAuthorityVerification",
            "WorkflowAuthorityVerificationIdentity",
            "WorkflowAuthorityVerificationKind",
            "WorkflowDispatchAuthorization",
            "WorkflowDispatchAuthorizationIdentity",
            "WorkflowEffectCapability",
            "WorkflowEffectIntent",
            "WorkflowEffectIntentIdentity",
            "WorkflowEffectOutcomeKind",
            "WorkflowEffectReconcilerIdentity",
            "WorkflowEventAppendResult",
            "WorkflowEventAppendStatus",
            "WorkflowExecutionEvidence",
            "WorkflowExecutionEvidenceIdentity",
            "WorkflowForegroundActionResult",
            "WorkflowForegroundActionStatus",
            "WorkflowForegroundDispatcher",
            "WorkflowForegroundDispatchRequest",
            "WorkflowForegroundExecutionRequest",
            "WorkflowForegroundPlan",
            "WorkflowForegroundReconciliationRecorder",
            "WorkflowForegroundReconciliationRecordingRequest",
            "WorkflowForegroundWorkerIdentity",
            "WorkflowHistoryLoadResult",
            "WorkflowHistoryLoadStatus",
            "WorkflowOccurrenceIdentity",
            "WorkflowPlanIdentity",
            "WorkflowPlanRecorder",
            "WorkflowPlanRecordingRequest",
            "WorkflowReconciliationEvidence",
            "WorkflowReconciliationEvidenceIdentity",
            "WorkflowReconciliationOutcomeKind",
            "WorkflowReconciliationRequest",
            "WorkflowRequestRetainer",
            "WorkflowRequestRetentionRequest",
            "WorkflowRunStartRecorder",
            "WorkflowRunStartRecordingRequest",
            "WorkflowRuntimeActionResult",
            "WorkflowRuntimeActionStatus",
            "WorkflowRuntimeEvent",
            "WorkflowRuntimeEventIdentity",
            "WorkflowRuntimeEventKind",
            "WorkflowRuntimeEventSerializer",
            "WorkflowRuntimeEvidenceReference",
            "WorkflowRuntimeHistory",
            "WorkflowRuntimeRepository",
            "WorkflowTransitionRecorder",
            "WorkflowTransitionRecordingRequest",
        }
        assert len(runtime.__all__) == len(expected)
        assert set(runtime.__all__) == expected

    def test__v2__does_not_restore_workflow_local_base_package(self) -> None:
        assert find_spec("ksdft2effmass.workflows.v2.base") is None
