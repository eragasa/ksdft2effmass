"""Software verification for package-wide base action patterns."""

from __future__ import annotations

import inspect

from ksdft2effmass.base import (
    DataObject,
    DataObjectActionizer,
    DataObjectActionRequest,
    DataObjectActionResult,
)
from ksdft2effmass.base.data_object import AbstractDataObject
from ksdft2effmass.base.identity import AbstractIdentity
from ksdft2effmass.base.immutable import AbstractImmutableDataObject
from ksdft2effmass.workflows.v2.runtime import (
    AbstractWorkflowEffectReconciler,
    AbstractWorkflowForegroundWorker,
    WorkflowAuthorityRejectionRecorder,
    WorkflowAuthorityRejectionRecordingRequest,
    WorkflowExecutionEvidence,
    WorkflowForegroundActionResult,
    WorkflowForegroundDispatcher,
    WorkflowForegroundDispatchRequest,
    WorkflowForegroundExecutionRequest,
    WorkflowForegroundReconciliationRecorder,
    WorkflowForegroundReconciliationRecordingRequest,
    WorkflowPlanRecorder,
    WorkflowPlanRecordingRequest,
    WorkflowReconciliationEvidence,
    WorkflowReconciliationRequest,
    WorkflowRequestRetainer,
    WorkflowRequestRetentionRequest,
    WorkflowRunStartRecorder,
    WorkflowRunStartRecordingRequest,
    WorkflowRuntimeActionResult,
    WorkflowTransitionRecorder,
    WorkflowTransitionRecordingRequest,
)


class TestWorkflowBaseActionPatterns:
    """Require one package-wide request-actionizer-result hierarchy."""

    def test__base__duplicates_ingestion_nominal_hierarchy(self) -> None:
        assert issubclass(AbstractDataObject, DataObject)
        assert issubclass(AbstractImmutableDataObject, AbstractDataObject)
        assert issubclass(AbstractIdentity, AbstractImmutableDataObject)
        assert inspect.isabstract(AbstractDataObject)
        assert inspect.isabstract(AbstractImmutableDataObject)
        assert inspect.isabstract(AbstractIdentity)

    def test__runtime_requests__inherit_action_request(self) -> None:
        request_types = (
            WorkflowRunStartRecordingRequest,
            WorkflowRequestRetentionRequest,
            WorkflowPlanRecordingRequest,
            WorkflowAuthorityRejectionRecordingRequest,
            WorkflowForegroundDispatchRequest,
            WorkflowForegroundReconciliationRecordingRequest,
            WorkflowTransitionRecordingRequest,
            WorkflowForegroundExecutionRequest,
            WorkflowReconciliationRequest,
        )
        assert all(
            issubclass(request_type, DataObjectActionRequest)
            for request_type in request_types
        )

    def test__runtime_results__inherit_action_result(self) -> None:
        result_types = (
            WorkflowRuntimeActionResult,
            WorkflowForegroundActionResult,
            WorkflowExecutionEvidence,
            WorkflowReconciliationEvidence,
        )
        assert all(
            issubclass(result_type, DataObjectActionResult)
            for result_type in result_types
        )

    def test__runtime_actionizers__inherit_actionizer(self) -> None:
        actionizer_types = (
            WorkflowRunStartRecorder,
            WorkflowRequestRetainer,
            WorkflowPlanRecorder,
            WorkflowAuthorityRejectionRecorder,
            WorkflowForegroundDispatcher,
            WorkflowForegroundReconciliationRecorder,
            WorkflowTransitionRecorder,
            AbstractWorkflowForegroundWorker,
            AbstractWorkflowEffectReconciler,
        )
        assert all(
            issubclass(actionizer_type, DataObjectActionizer)
            for actionizer_type in actionizer_types
        )

    def test__runtime_actionizers__expose_keyword_only_request(self) -> None:
        actionizer_types = (
            WorkflowRunStartRecorder,
            WorkflowRequestRetainer,
            WorkflowPlanRecorder,
            WorkflowAuthorityRejectionRecorder,
            WorkflowForegroundDispatcher,
            WorkflowForegroundReconciliationRecorder,
            WorkflowTransitionRecorder,
            AbstractWorkflowForegroundWorker,
            AbstractWorkflowEffectReconciler,
        )
        for actionizer_type in actionizer_types:
            signature = inspect.signature(actionizer_type.action)
            parameter = signature.parameters["request"]
            assert parameter.kind is inspect.Parameter.KEYWORD_ONLY
            assert signature.return_annotation is not inspect.Signature.empty
