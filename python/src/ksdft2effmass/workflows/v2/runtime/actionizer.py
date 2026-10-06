"""Fixed actionizers for append-only local workflow runtime operations."""

from __future__ import annotations

from ksdft2effmass.base import DataObjectActionizer
from ksdft2effmass.workflows.v2.runtime.foreground import (
    AbstractWorkflowEffectReconciler,
    AbstractWorkflowForegroundWorker,
    WorkflowEffectReconcilerIdentity,
)
from ksdft2effmass.workflows.v2.runtime.repository import WorkflowRuntimeRepository
from ksdft2effmass.workflows.v2.runtime.request import (
    WorkflowAuthorityRejectionRecordingRequest,
    WorkflowForegroundDispatchRequest,
    WorkflowForegroundReconciliationRecordingRequest,
    WorkflowPlanRecordingRequest,
    WorkflowRequestRetentionRequest,
    WorkflowRunStartRecordingRequest,
    WorkflowTransitionRecordingRequest,
)
from ksdft2effmass.workflows.v2.runtime.service import (
    WorkflowForegroundActionResult,
    WorkflowRuntimeActionResult,
    _LocalWorkflowRuntime,
)


class _LocalRuntimeActionizer(_LocalWorkflowRuntime):
    """Share private runtime mechanics across exact actionizers."""

    __slots__ = ()


class WorkflowRunStartRecorder(
    _LocalRuntimeActionizer,
    DataObjectActionizer[
        WorkflowRunStartRecordingRequest,
        WorkflowRuntimeActionResult,
    ],
):
    """Retain one exact revision-zero workflow run."""

    __slots__ = ()

    def action(
        self, *, request: WorkflowRunStartRecordingRequest
    ) -> WorkflowRuntimeActionResult:
        if type(request) is not WorkflowRunStartRecordingRequest:
            raise TypeError("request must be WorkflowRunStartRecordingRequest")
        return self._start(request.started)


class WorkflowRequestRetainer(
    _LocalRuntimeActionizer,
    DataObjectActionizer[
        WorkflowRequestRetentionRequest,
        WorkflowRuntimeActionResult,
    ],
):
    """Preflight and reserve one exact workflow request."""

    __slots__ = ()

    def action(
        self, *, request: WorkflowRequestRetentionRequest
    ) -> WorkflowRuntimeActionResult:
        if type(request) is not WorkflowRequestRetentionRequest:
            raise TypeError("request must be WorkflowRequestRetentionRequest")
        return self._retain_request(request.preflight)


class WorkflowPlanRecorder(
    _LocalRuntimeActionizer,
    DataObjectActionizer[
        WorkflowPlanRecordingRequest,
        WorkflowForegroundActionResult,
    ],
):
    """Retain one deterministic foreground plan."""

    __slots__ = ()

    def action(
        self, *, request: WorkflowPlanRecordingRequest
    ) -> WorkflowForegroundActionResult:
        if type(request) is not WorkflowPlanRecordingRequest:
            raise TypeError("request must be WorkflowPlanRecordingRequest")
        return self._record_plan(request.preflight, request.plan)


class WorkflowAuthorityRejectionRecorder(
    _LocalRuntimeActionizer,
    DataObjectActionizer[
        WorkflowAuthorityRejectionRecordingRequest,
        WorkflowForegroundActionResult,
    ],
):
    """Retain one application-owned authority rejection."""

    __slots__ = ()

    def action(
        self,
        *,
        request: WorkflowAuthorityRejectionRecordingRequest,
    ) -> WorkflowForegroundActionResult:
        if type(request) is not WorkflowAuthorityRejectionRecordingRequest:
            raise TypeError(
                "request must be WorkflowAuthorityRejectionRecordingRequest"
            )
        return self._record_authority_rejection(
            request.preflight,
            request.plan,
            request.verification,
        )


class WorkflowForegroundDispatcher(
    _LocalRuntimeActionizer,
    DataObjectActionizer[
        WorkflowForegroundDispatchRequest,
        WorkflowForegroundActionResult,
    ],
):
    """Authorize and hand one foreground attempt to an exact worker."""

    __slots__ = ("_worker",)

    def __init__(
        self,
        repository: WorkflowRuntimeRepository,
        worker: AbstractWorkflowForegroundWorker,
    ) -> None:
        super().__init__(repository)
        if not isinstance(worker, AbstractWorkflowForegroundWorker):
            raise TypeError("worker must be AbstractWorkflowForegroundWorker")
        self._worker = worker

    def action(
        self, *, request: WorkflowForegroundDispatchRequest
    ) -> WorkflowForegroundActionResult:
        if type(request) is not WorkflowForegroundDispatchRequest:
            raise TypeError("request must be WorkflowForegroundDispatchRequest")
        return self._dispatch_foreground(
            request.preflight,
            request.execution,
            request.verification,
            self._worker,
        )


class WorkflowForegroundReconciliationRecorder(
    _LocalRuntimeActionizer,
    DataObjectActionizer[
        WorkflowForegroundReconciliationRecordingRequest,
        WorkflowForegroundActionResult,
    ],
):
    """Query and retain one foreground reconciliation observation."""

    __slots__ = ("_reconciler",)

    def __init__(
        self,
        repository: WorkflowRuntimeRepository,
        reconciler: AbstractWorkflowEffectReconciler,
    ) -> None:
        super().__init__(repository)
        if not isinstance(reconciler, AbstractWorkflowEffectReconciler):
            raise TypeError("reconciler must be AbstractWorkflowEffectReconciler")
        if type(reconciler.identity) is not WorkflowEffectReconcilerIdentity:
            raise TypeError(
                "reconciler identity must be WorkflowEffectReconcilerIdentity"
            )
        self._reconciler = reconciler

    def action(
        self,
        *,
        request: WorkflowForegroundReconciliationRecordingRequest,
    ) -> WorkflowForegroundActionResult:
        if type(request) is not WorkflowForegroundReconciliationRecordingRequest:
            raise TypeError(
                "request must be WorkflowForegroundReconciliationRecordingRequest"
            )
        return self._reconcile_foreground(
            request.preflight,
            request.reconciliation,
            self._reconciler,
        )


class WorkflowTransitionRecorder(
    _LocalRuntimeActionizer,
    DataObjectActionizer[
        WorkflowTransitionRecordingRequest,
        WorkflowRuntimeActionResult,
    ],
):
    """Process and retain one final core transition."""

    __slots__ = ()

    def action(
        self, *, request: WorkflowTransitionRecordingRequest
    ) -> WorkflowRuntimeActionResult:
        if type(request) is not WorkflowTransitionRecordingRequest:
            raise TypeError("request must be WorkflowTransitionRecordingRequest")
        return self._record_transition(request.transition)
