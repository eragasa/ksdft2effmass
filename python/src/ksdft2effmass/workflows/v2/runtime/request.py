"""Immutable requests for fixed local workflow-runtime actions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from ksdft2effmass.base import DataObjectActionRequest
from ksdft2effmass.base.immutable import AbstractImmutableDataObject
from ksdft2effmass.workflows.v2.core import (
    WorkflowRunStartResult,
    WorkflowTransitionInput,
    WorkflowTransitionPreflightInput,
)
from ksdft2effmass.workflows.v2.core.identities import stable_identity
from ksdft2effmass.workflows.v2.runtime.foreground import (
    WorkflowAuthorityVerification,
    WorkflowForegroundExecutionRequest,
    WorkflowForegroundPlan,
    WorkflowReconciliationRequest,
)

_CONTRACT_VERSION = "1.0"


def _preflight_parts(
    preflight: WorkflowTransitionPreflightInput,
) -> tuple[str, str, str, str]:
    return (
        preflight.definition.identity.value,
        preflight.run.identity.value,
        preflight.prior_state.identity.value,
        preflight.request.identity.value,
    )


@dataclass(frozen=True, slots=True)
class WorkflowRunStartRecordingRequest(
    AbstractImmutableDataObject,
    DataObjectActionRequest,
):
    """Request append-only retention of one exact started workflow run."""

    CONTRACT_NAME: ClassVar[str] = "workflow-run-start-recording-request"
    CONTRACT_VERSION: ClassVar[str] = _CONTRACT_VERSION

    request_id: str
    started: WorkflowRunStartResult
    contract_version: str = CONTRACT_VERSION

    @classmethod
    def create(
        cls, *, started: WorkflowRunStartResult
    ) -> WorkflowRunStartRecordingRequest:
        if type(started) is not WorkflowRunStartResult:
            raise TypeError("started must be WorkflowRunStartResult")
        return cls(
            stable_identity(
                cls.CONTRACT_NAME,
                cls.CONTRACT_VERSION,
                started.run.identity.value,
                started.state.identity.value,
            ),
            started,
        )

    def __post_init__(self) -> None:
        if type(self.started) is not WorkflowRunStartResult:
            raise TypeError("started must be WorkflowRunStartResult")
        expected = stable_identity(
            self.CONTRACT_NAME,
            self.CONTRACT_VERSION,
            self.started.run.identity.value,
            self.started.state.identity.value,
        )
        if (
            self.contract_version != self.CONTRACT_VERSION
            or self.request_id != expected
        ):
            raise ValueError("run-start recording request is inconsistent")


@dataclass(frozen=True, slots=True)
class WorkflowRequestRetentionRequest(
    AbstractImmutableDataObject,
    DataObjectActionRequest,
):
    """Request preflight and reservation of one transition request."""

    CONTRACT_NAME: ClassVar[str] = "workflow-request-retention-request"
    CONTRACT_VERSION: ClassVar[str] = _CONTRACT_VERSION

    request_id: str
    preflight: WorkflowTransitionPreflightInput
    contract_version: str = CONTRACT_VERSION

    @classmethod
    def create(
        cls, *, preflight: WorkflowTransitionPreflightInput
    ) -> WorkflowRequestRetentionRequest:
        if type(preflight) is not WorkflowTransitionPreflightInput:
            raise TypeError("preflight must be WorkflowTransitionPreflightInput")
        return cls(
            stable_identity(
                cls.CONTRACT_NAME,
                cls.CONTRACT_VERSION,
                *_preflight_parts(preflight),
            ),
            preflight,
        )

    def __post_init__(self) -> None:
        if type(self.preflight) is not WorkflowTransitionPreflightInput:
            raise TypeError("preflight must be WorkflowTransitionPreflightInput")
        expected = stable_identity(
            self.CONTRACT_NAME,
            self.CONTRACT_VERSION,
            *_preflight_parts(self.preflight),
        )
        if (
            self.contract_version != self.CONTRACT_VERSION
            or self.request_id != expected
        ):
            raise ValueError("request-retention request is inconsistent")


@dataclass(frozen=True, slots=True)
class WorkflowPlanRecordingRequest(
    AbstractImmutableDataObject,
    DataObjectActionRequest,
):
    """Request retention of one deterministic foreground plan."""

    CONTRACT_NAME: ClassVar[str] = "workflow-plan-recording-request"
    CONTRACT_VERSION: ClassVar[str] = _CONTRACT_VERSION

    request_id: str
    preflight: WorkflowTransitionPreflightInput
    plan: WorkflowForegroundPlan
    contract_version: str = CONTRACT_VERSION

    @classmethod
    def create(
        cls,
        *,
        preflight: WorkflowTransitionPreflightInput,
        plan: WorkflowForegroundPlan,
    ) -> WorkflowPlanRecordingRequest:
        if type(preflight) is not WorkflowTransitionPreflightInput:
            raise TypeError("preflight must be WorkflowTransitionPreflightInput")
        if type(plan) is not WorkflowForegroundPlan:
            raise TypeError("plan must be WorkflowForegroundPlan")
        return cls(
            stable_identity(
                cls.CONTRACT_NAME,
                cls.CONTRACT_VERSION,
                *_preflight_parts(preflight),
                plan.identity.value,
            ),
            preflight,
            plan,
        )

    def __post_init__(self) -> None:
        if type(self.preflight) is not WorkflowTransitionPreflightInput:
            raise TypeError("preflight must be WorkflowTransitionPreflightInput")
        if type(self.plan) is not WorkflowForegroundPlan:
            raise TypeError("plan must be WorkflowForegroundPlan")
        expected = stable_identity(
            self.CONTRACT_NAME,
            self.CONTRACT_VERSION,
            *_preflight_parts(self.preflight),
            self.plan.identity.value,
        )
        if (
            self.contract_version != self.CONTRACT_VERSION
            or self.request_id != expected
        ):
            raise ValueError("plan-recording request is inconsistent")


@dataclass(frozen=True, slots=True)
class WorkflowAuthorityRejectionRecordingRequest(
    AbstractImmutableDataObject,
    DataObjectActionRequest,
):
    """Request retention of one application-owned authority rejection."""

    CONTRACT_NAME: ClassVar[str] = "workflow-authority-rejection-recording-request"
    CONTRACT_VERSION: ClassVar[str] = _CONTRACT_VERSION

    request_id: str
    preflight: WorkflowTransitionPreflightInput
    plan: WorkflowForegroundPlan
    verification: WorkflowAuthorityVerification
    contract_version: str = CONTRACT_VERSION

    @classmethod
    def create(
        cls,
        *,
        preflight: WorkflowTransitionPreflightInput,
        plan: WorkflowForegroundPlan,
        verification: WorkflowAuthorityVerification,
    ) -> WorkflowAuthorityRejectionRecordingRequest:
        if type(preflight) is not WorkflowTransitionPreflightInput:
            raise TypeError("preflight must be WorkflowTransitionPreflightInput")
        if type(plan) is not WorkflowForegroundPlan:
            raise TypeError("plan must be WorkflowForegroundPlan")
        if type(verification) is not WorkflowAuthorityVerification:
            raise TypeError("verification must be WorkflowAuthorityVerification")
        return cls(
            stable_identity(
                cls.CONTRACT_NAME,
                cls.CONTRACT_VERSION,
                *_preflight_parts(preflight),
                plan.identity.value,
                verification.identity.value,
            ),
            preflight,
            plan,
            verification,
        )

    def __post_init__(self) -> None:
        if type(self.preflight) is not WorkflowTransitionPreflightInput:
            raise TypeError("preflight must be WorkflowTransitionPreflightInput")
        if type(self.plan) is not WorkflowForegroundPlan:
            raise TypeError("plan must be WorkflowForegroundPlan")
        if type(self.verification) is not WorkflowAuthorityVerification:
            raise TypeError("verification must be WorkflowAuthorityVerification")
        expected = stable_identity(
            self.CONTRACT_NAME,
            self.CONTRACT_VERSION,
            *_preflight_parts(self.preflight),
            self.plan.identity.value,
            self.verification.identity.value,
        )
        if (
            self.contract_version != self.CONTRACT_VERSION
            or self.request_id != expected
        ):
            raise ValueError("authority-rejection recording request is inconsistent")


@dataclass(frozen=True, slots=True)
class WorkflowForegroundDispatchRequest(
    AbstractImmutableDataObject,
    DataObjectActionRequest,
):
    """Request one exact authorized foreground worker handoff."""

    CONTRACT_NAME: ClassVar[str] = "workflow-foreground-dispatch-request"
    CONTRACT_VERSION: ClassVar[str] = _CONTRACT_VERSION

    request_id: str
    preflight: WorkflowTransitionPreflightInput
    execution: WorkflowForegroundExecutionRequest
    verification: WorkflowAuthorityVerification
    contract_version: str = CONTRACT_VERSION

    @classmethod
    def create(
        cls,
        *,
        preflight: WorkflowTransitionPreflightInput,
        execution: WorkflowForegroundExecutionRequest,
        verification: WorkflowAuthorityVerification,
    ) -> WorkflowForegroundDispatchRequest:
        if type(preflight) is not WorkflowTransitionPreflightInput:
            raise TypeError("preflight must be WorkflowTransitionPreflightInput")
        if type(execution) is not WorkflowForegroundExecutionRequest:
            raise TypeError("execution must be WorkflowForegroundExecutionRequest")
        if type(verification) is not WorkflowAuthorityVerification:
            raise TypeError("verification must be WorkflowAuthorityVerification")
        return cls(
            stable_identity(
                cls.CONTRACT_NAME,
                cls.CONTRACT_VERSION,
                *_preflight_parts(preflight),
                execution.authorization.identity.value,
                verification.identity.value,
            ),
            preflight,
            execution,
            verification,
        )

    def __post_init__(self) -> None:
        if type(self.preflight) is not WorkflowTransitionPreflightInput:
            raise TypeError("preflight must be WorkflowTransitionPreflightInput")
        if type(self.execution) is not WorkflowForegroundExecutionRequest:
            raise TypeError("execution must be WorkflowForegroundExecutionRequest")
        if type(self.verification) is not WorkflowAuthorityVerification:
            raise TypeError("verification must be WorkflowAuthorityVerification")
        expected = stable_identity(
            self.CONTRACT_NAME,
            self.CONTRACT_VERSION,
            *_preflight_parts(self.preflight),
            self.execution.authorization.identity.value,
            self.verification.identity.value,
        )
        if (
            self.contract_version != self.CONTRACT_VERSION
            or self.request_id != expected
        ):
            raise ValueError("foreground-dispatch request is inconsistent")


@dataclass(frozen=True, slots=True)
class WorkflowForegroundReconciliationRecordingRequest(
    AbstractImmutableDataObject,
    DataObjectActionRequest,
):
    """Request one query-only foreground reconciliation observation."""

    CONTRACT_NAME: ClassVar[str] = (
        "workflow-foreground-reconciliation-recording-request"
    )
    CONTRACT_VERSION: ClassVar[str] = _CONTRACT_VERSION

    request_id: str
    preflight: WorkflowTransitionPreflightInput
    reconciliation: WorkflowReconciliationRequest
    contract_version: str = CONTRACT_VERSION

    @classmethod
    def create(
        cls,
        *,
        preflight: WorkflowTransitionPreflightInput,
        reconciliation: WorkflowReconciliationRequest,
    ) -> WorkflowForegroundReconciliationRecordingRequest:
        if type(preflight) is not WorkflowTransitionPreflightInput:
            raise TypeError("preflight must be WorkflowTransitionPreflightInput")
        if type(reconciliation) is not WorkflowReconciliationRequest:
            raise TypeError("reconciliation must be WorkflowReconciliationRequest")
        return cls(
            stable_identity(
                cls.CONTRACT_NAME,
                cls.CONTRACT_VERSION,
                *_preflight_parts(preflight),
                reconciliation.execution_evidence.identity.value,
            ),
            preflight,
            reconciliation,
        )

    def __post_init__(self) -> None:
        if type(self.preflight) is not WorkflowTransitionPreflightInput:
            raise TypeError("preflight must be WorkflowTransitionPreflightInput")
        if type(self.reconciliation) is not WorkflowReconciliationRequest:
            raise TypeError("reconciliation must be WorkflowReconciliationRequest")
        expected = stable_identity(
            self.CONTRACT_NAME,
            self.CONTRACT_VERSION,
            *_preflight_parts(self.preflight),
            self.reconciliation.execution_evidence.identity.value,
        )
        if (
            self.contract_version != self.CONTRACT_VERSION
            or self.request_id != expected
        ):
            raise ValueError(
                "foreground-reconciliation recording request is inconsistent"
            )


@dataclass(frozen=True, slots=True)
class WorkflowTransitionRecordingRequest(
    AbstractImmutableDataObject,
    DataObjectActionRequest,
):
    """Request final append-only retention of one core transition."""

    CONTRACT_NAME: ClassVar[str] = "workflow-transition-recording-request"
    CONTRACT_VERSION: ClassVar[str] = _CONTRACT_VERSION

    request_id: str
    transition: WorkflowTransitionInput
    contract_version: str = CONTRACT_VERSION

    @classmethod
    def create(
        cls, *, transition: WorkflowTransitionInput
    ) -> WorkflowTransitionRecordingRequest:
        if type(transition) is not WorkflowTransitionInput:
            raise TypeError("transition must be WorkflowTransitionInput")
        evidence_identity = (
            transition.adapter_evidence.identity.value
            if transition.adapter_evidence is not None
            else transition.infrastructure_failure.identity.value
            if transition.infrastructure_failure is not None
            else "missing-evidence"
        )
        return cls(
            stable_identity(
                cls.CONTRACT_NAME,
                cls.CONTRACT_VERSION,
                transition.definition.identity.value,
                transition.run.identity.value,
                transition.prior_state.identity.value,
                transition.request.identity.value,
                evidence_identity,
            ),
            transition,
        )

    def __post_init__(self) -> None:
        if type(self.transition) is not WorkflowTransitionInput:
            raise TypeError("transition must be WorkflowTransitionInput")
        evidence_identity = (
            self.transition.adapter_evidence.identity.value
            if self.transition.adapter_evidence is not None
            else self.transition.infrastructure_failure.identity.value
            if self.transition.infrastructure_failure is not None
            else "missing-evidence"
        )
        expected = stable_identity(
            self.CONTRACT_NAME,
            self.CONTRACT_VERSION,
            self.transition.definition.identity.value,
            self.transition.run.identity.value,
            self.transition.prior_state.identity.value,
            self.transition.request.identity.value,
            evidence_identity,
        )
        if (
            self.contract_version != self.CONTRACT_VERSION
            or self.request_id != expected
        ):
            raise ValueError("transition-recording request is inconsistent")
