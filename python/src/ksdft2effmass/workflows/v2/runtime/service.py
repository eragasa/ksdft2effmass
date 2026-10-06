"""Bounded local runtime orchestration around the pure workflow core."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar

from ksdft2effmass.base import DataObjectActionResult
from ksdft2effmass.base.immutable import AbstractImmutableDataObject
from ksdft2effmass.workflows.v2.core import (
    WorkflowOperationIdentity,
    WorkflowRunStartResult,
    WorkflowStateIdentity,
    WorkflowTransitionExecution,
    WorkflowTransitionInput,
    WorkflowTransitionPreflightInput,
    WorkflowTransitionProcessor,
    WorkflowTransitionRequestIdentity,
    WorkflowTransitionValidator,
    WorkflowValidationResult,
)

from .foreground import (
    AbstractWorkflowEffectReconciler,
    AbstractWorkflowForegroundWorker,
    WorkflowAttemptIdentity,
    WorkflowAuthorityVerification,
    WorkflowAuthorityVerificationKind,
    WorkflowEffectOutcomeKind,
    WorkflowEffectReconcilerIdentity,
    WorkflowExecutionEvidence,
    WorkflowForegroundExecutionRequest,
    WorkflowForegroundPlan,
    WorkflowReconciliationEvidence,
    WorkflowReconciliationOutcomeKind,
    WorkflowReconciliationRequest,
)
from .records import (
    WorkflowOccurrenceIdentity,
    WorkflowRuntimeEvent,
    WorkflowRuntimeEventKind,
    WorkflowRuntimeEvidenceReference,
)
from .repository import (
    WorkflowEventAppendStatus,
    WorkflowHistoryLoadStatus,
    WorkflowRuntimeHistory,
    WorkflowRuntimeRepository,
)


class WorkflowForegroundActionStatus(StrEnum):
    """Closed result of one foreground plan, dispatch, or reconciliation."""

    RECORDED = "recorded"
    IDEMPOTENT = "idempotent"
    RECONCILIATION_REQUIRED = "reconciliation_required"
    ATTEMPTS_EXHAUSTED = "attempts_exhausted"
    REJECTED = "rejected"
    CONFLICT = "conflict"
    INDETERMINATE = "indeterminate"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class WorkflowForegroundActionResult(
    AbstractImmutableDataObject,
    DataObjectActionResult,
):
    """Result of one bounded foreground runtime action."""

    CONTRACT_NAME: ClassVar[str] = "workflow-foreground-action-result"
    CONTRACT_VERSION: ClassVar[str] = "1.0"

    status: WorkflowForegroundActionStatus
    event: WorkflowRuntimeEvent | None
    diagnostics: tuple[str, ...]
    execution_evidence: WorkflowExecutionEvidence | None = None
    reconciliation_evidence: WorkflowReconciliationEvidence | None = None

    def __post_init__(self) -> None:
        if type(self.status) is not WorkflowForegroundActionStatus:
            raise TypeError("status must be WorkflowForegroundActionStatus")
        if self.event is not None and type(self.event) is not WorkflowRuntimeEvent:
            raise TypeError("event must be WorkflowRuntimeEvent or None")
        if type(self.diagnostics) is not tuple or any(
            type(value) is not str or not value for value in self.diagnostics
        ):
            raise TypeError("diagnostics must contain nonempty strings")
        if (
            self.execution_evidence is not None
            and type(self.execution_evidence) is not WorkflowExecutionEvidence
        ):
            raise TypeError(
                "execution_evidence must be WorkflowExecutionEvidence or None"
            )
        if (
            self.reconciliation_evidence is not None
            and type(self.reconciliation_evidence) is not WorkflowReconciliationEvidence
        ):
            raise TypeError(
                "reconciliation_evidence must be WorkflowReconciliationEvidence or None"
            )
        if (
            self.execution_evidence is not None
            and self.reconciliation_evidence is not None
        ):
            raise ValueError("one action result cannot contain both evidence kinds")


class WorkflowRuntimeActionStatus(StrEnum):
    """Closed result of one local runtime action."""

    RECORDED = "recorded"
    IDEMPOTENT = "idempotent"
    REJECTED = "rejected"
    CONFLICT = "conflict"
    INDETERMINATE = "indeterminate"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class WorkflowRuntimeActionResult(
    AbstractImmutableDataObject,
    DataObjectActionResult,
):
    """Represent one runtime action without hiding persistence uncertainty."""

    CONTRACT_NAME: ClassVar[str] = "workflow-runtime-action-result"
    CONTRACT_VERSION: ClassVar[str] = "1.0"

    status: WorkflowRuntimeActionStatus
    event: WorkflowRuntimeEvent | None
    diagnostics: tuple[str, ...]
    validation: WorkflowValidationResult | None = None
    transition: WorkflowTransitionExecution | None = None

    def __post_init__(self) -> None:
        if type(self.status) is not WorkflowRuntimeActionStatus:
            raise TypeError("status must be WorkflowRuntimeActionStatus")
        if self.event is not None and type(self.event) is not WorkflowRuntimeEvent:
            raise TypeError("event must be WorkflowRuntimeEvent or None")
        if type(self.diagnostics) is not tuple or any(
            type(value) is not str or not value for value in self.diagnostics
        ):
            raise TypeError("diagnostics must contain nonempty strings")
        if (
            self.validation is not None
            and type(self.validation) is not WorkflowValidationResult
        ):
            raise TypeError("validation must be WorkflowValidationResult or None")
        if (
            self.transition is not None
            and type(self.transition) is not WorkflowTransitionExecution
        ):
            raise TypeError("transition must be WorkflowTransitionExecution or None")
        if (
            self.status
            in {
                WorkflowRuntimeActionStatus.RECORDED,
                WorkflowRuntimeActionStatus.IDEMPOTENT,
                WorkflowRuntimeActionStatus.REJECTED,
            }
            and self.event is None
        ):
            raise ValueError(f"{self.status.value} requires an event")


class _LocalWorkflowRuntime:
    """Implement local runtime mechanics behind typed actionizer boundaries."""

    __slots__ = ("_processor", "_repository", "_validator")

    def __init__(self, repository: WorkflowRuntimeRepository) -> None:
        if type(repository) is not WorkflowRuntimeRepository:
            raise TypeError("repository must be WorkflowRuntimeRepository")
        self._repository = repository
        self._validator = WorkflowTransitionValidator()
        self._processor = WorkflowTransitionProcessor()

    def _start(self, started: WorkflowRunStartResult) -> WorkflowRuntimeActionResult:
        """Record one exact revision-zero run or return its retained genesis."""
        if type(started) is not WorkflowRunStartResult:
            raise TypeError("started must be WorkflowRunStartResult")
        evidence = [
            WorkflowRuntimeEvidenceReference(
                "workflow-definition",
                started.run.definition_identity.value,
            ),
            WorkflowRuntimeEvidenceReference(
                "workflow-subject",
                started.run.subject_identity.value,
            ),
        ]
        evidence.extend(
            WorkflowRuntimeEvidenceReference("artifact-reference", value.identity.value)
            for value in started.run.artifact_references
        )
        evidence.extend(
            WorkflowRuntimeEvidenceReference("decision-reference", value.identity.value)
            for value in started.run.decision_references
        )
        if started.run.parent_run_identity is not None:
            evidence.append(
                WorkflowRuntimeEvidenceReference(
                    "parent-run", started.run.parent_run_identity.value
                )
            )
        if started.run.predecessor_run_identity is not None:
            evidence.append(
                WorkflowRuntimeEvidenceReference(
                    "predecessor-run",
                    started.run.predecessor_run_identity.value,
                )
            )
        event = WorkflowRuntimeEvent.create(
            kind=WorkflowRuntimeEventKind.RUN_STARTED,
            run_identity=started.run.identity,
            ordinal=0,
            predecessor_event_identity=None,
            core_revision=started.run.revision,
            core_state_identity=started.state.identity,
            evidence_references=tuple(evidence),
        )
        loaded = self._repository.load(started.run.identity.value)
        if loaded.status is WorkflowHistoryLoadStatus.LOADED:
            assert loaded.history is not None
            genesis = loaded.history.events[0]
            if genesis == event:
                return WorkflowRuntimeActionResult(
                    WorkflowRuntimeActionStatus.IDEMPOTENT,
                    genesis,
                    (),
                )
            return WorkflowRuntimeActionResult(
                WorkflowRuntimeActionStatus.CONFLICT,
                None,
                ("run_identity_collision",),
            )
        if loaded.status is not WorkflowHistoryLoadStatus.ABSENT:
            return _load_failure_result(loaded.status, loaded.diagnostics)
        return _append_result(
            self._repository.append(
                event,
                expected_event_identity=None,
                idempotency_identity=f"runtime-start:{event.identity.value}",
            )
        )

    def _retain_request(
        self,
        preflight: WorkflowTransitionPreflightInput,
    ) -> WorkflowRuntimeActionResult:
        """Preflight and reserve one request at one exact core revision."""
        if type(preflight) is not WorkflowTransitionPreflightInput:
            raise TypeError("preflight must be WorkflowTransitionPreflightInput")
        loaded = self._repository.load(preflight.run.identity.value)
        if loaded.status is not WorkflowHistoryLoadStatus.LOADED:
            return _load_failure_result(loaded.status, loaded.diagnostics)
        assert loaded.history is not None
        history = loaded.history
        if (
            history.head.core_revision != preflight.run.revision
            or history.head.core_state_identity != preflight.prior_state.identity
        ):
            return WorkflowRuntimeActionResult(
                WorkflowRuntimeActionStatus.CONFLICT,
                None,
                ("runtime_head_core_mismatch",),
            )
        existing = _request_event(history, preflight.request.identity.value)
        if existing is not None:
            status = (
                WorkflowRuntimeActionStatus.REJECTED
                if existing.kind is WorkflowRuntimeEventKind.PREFLIGHT_REJECTED
                else WorkflowRuntimeActionStatus.CONFLICT
                if existing.kind is WorkflowRuntimeEventKind.REQUEST_CONFLICT_RECORDED
                else WorkflowRuntimeActionStatus.IDEMPOTENT
            )
            return WorkflowRuntimeActionResult(status, existing, ())
        idempotency_owner = _idempotency_owner(
            history,
            preflight.request.idempotency_identity.value,
        )
        if idempotency_owner is not None:
            assert idempotency_owner.request_identity is not None
            event = _next_event(
                history,
                kind=WorkflowRuntimeEventKind.REQUEST_CONFLICT_RECORDED,
                core_revision=preflight.run.revision,
                core_state_identity=preflight.prior_state.identity,
                occurrence_identity=WorkflowOccurrenceIdentity.create(
                    run_identity=preflight.run.identity,
                    state_identity=preflight.prior_state.identity,
                    revision=preflight.run.revision,
                    request_identity=preflight.request.identity,
                ),
                request_identity=preflight.request.identity,
                operation_identity=preflight.request.operation_identity,
                evidence_references=(
                    WorkflowRuntimeEvidenceReference(
                        "idempotency-owner-request",
                        idempotency_owner.request_identity.value,
                    ),
                    WorkflowRuntimeEvidenceReference(
                        "request-idempotency",
                        preflight.request.idempotency_identity.value,
                    ),
                ),
                reason_codes=("idempotency_collision",),
            )
            appended = self._repository.append(
                event,
                expected_event_identity=history.head.identity,
                idempotency_identity=(
                    f"runtime-idempotency-conflict:{event.identity.value}"
                ),
            )
            result = _append_result(appended)
            if result.status is WorkflowRuntimeActionStatus.RECORDED:
                return WorkflowRuntimeActionResult(
                    WorkflowRuntimeActionStatus.CONFLICT,
                    result.event,
                    result.diagnostics,
                )
            return result
        occurrence = WorkflowOccurrenceIdentity.create(
            run_identity=preflight.run.identity,
            state_identity=preflight.prior_state.identity,
            revision=preflight.run.revision,
            request_identity=preflight.request.identity,
        )
        active = _active_occurrence(history, preflight.run.revision)
        if active is not None:
            assert active.occurrence_identity is not None
            assert active.request_identity is not None
            event = _next_event(
                history,
                kind=WorkflowRuntimeEventKind.REQUEST_CONFLICT_RECORDED,
                core_revision=preflight.run.revision,
                core_state_identity=preflight.prior_state.identity,
                occurrence_identity=occurrence,
                request_identity=preflight.request.identity,
                operation_identity=preflight.request.operation_identity,
                evidence_references=(
                    WorkflowRuntimeEvidenceReference(
                        "active-occurrence", active.occurrence_identity.value
                    ),
                    WorkflowRuntimeEvidenceReference(
                        "active-request", active.request_identity.value
                    ),
                ),
                reason_codes=("revision_reserved",),
            )
            appended = self._repository.append(
                event,
                expected_event_identity=history.head.identity,
                idempotency_identity=f"runtime-conflict:{event.identity.value}",
            )
            result = _append_result(appended)
            if result.status is WorkflowRuntimeActionStatus.RECORDED:
                return WorkflowRuntimeActionResult(
                    WorkflowRuntimeActionStatus.CONFLICT,
                    result.event,
                    result.diagnostics,
                )
            return result
        validation = self._validator.execute(preflight)
        if validation.findings:
            event = _next_event(
                history,
                kind=WorkflowRuntimeEventKind.PREFLIGHT_REJECTED,
                core_revision=preflight.run.revision,
                core_state_identity=preflight.prior_state.identity,
                occurrence_identity=occurrence,
                request_identity=preflight.request.identity,
                operation_identity=preflight.request.operation_identity,
                evidence_references=(
                    WorkflowRuntimeEvidenceReference(
                        "request-idempotency",
                        preflight.request.idempotency_identity.value,
                    ),
                    WorkflowRuntimeEvidenceReference(
                        "workflow-validation", validation.identity.value
                    ),
                ),
                reason_codes=tuple(
                    finding.code.value for finding in validation.findings
                ),
            )
            appended = self._repository.append(
                event,
                expected_event_identity=history.head.identity,
                idempotency_identity=f"runtime-preflight:{event.identity.value}",
            )
            result = _append_result(appended, validation=validation)
            if result.status is WorkflowRuntimeActionStatus.RECORDED:
                return WorkflowRuntimeActionResult(
                    WorkflowRuntimeActionStatus.REJECTED,
                    result.event,
                    result.diagnostics,
                    validation,
                )
            return result
        event = _next_event(
            history,
            kind=WorkflowRuntimeEventKind.REQUEST_RETAINED,
            core_revision=preflight.run.revision,
            core_state_identity=preflight.prior_state.identity,
            occurrence_identity=occurrence,
            request_identity=preflight.request.identity,
            operation_identity=preflight.request.operation_identity,
            evidence_references=(
                WorkflowRuntimeEvidenceReference(
                    "authority-reference",
                    preflight.request.authority_reference.identity.value,
                ),
                WorkflowRuntimeEvidenceReference(
                    "request-idempotency",
                    preflight.request.idempotency_identity.value,
                ),
                WorkflowRuntimeEvidenceReference(
                    "workflow-validation", validation.identity.value
                ),
            ),
        )
        return _append_result(
            self._repository.append(
                event,
                expected_event_identity=history.head.identity,
                idempotency_identity=f"runtime-request:{event.identity.value}",
            ),
            validation=validation,
        )

    def _record_plan(
        self,
        preflight: WorkflowTransitionPreflightInput,
        plan: WorkflowForegroundPlan,
    ) -> WorkflowForegroundActionResult:
        """Retain one deterministic plan for a reserved request.

        This method performs repository I/O but no application or external
        effect.  A different plan for the same occurrence fails closed.
        """
        if type(preflight) is not WorkflowTransitionPreflightInput:
            raise TypeError("preflight must be WorkflowTransitionPreflightInput")
        if type(plan) is not WorkflowForegroundPlan:
            raise TypeError("plan must be WorkflowForegroundPlan")
        loaded = self._repository.load(preflight.run.identity.value)
        if loaded.status is not WorkflowHistoryLoadStatus.LOADED:
            return _foreground_load_failure(loaded.status, loaded.diagnostics)
        assert loaded.history is not None
        history = loaded.history
        retained = _retained_occurrence(history, preflight.request.identity.value)
        if (
            not _preflight_correlates(history, preflight, plan.occurrence_identity)
            or retained is None
            or retained.occurrence_identity != plan.occurrence_identity
            or plan.definition_identity != preflight.definition.identity
        ):
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.CONFLICT,
                None,
                ("plan_occurrence_not_reserved",),
            )
        existing = _event_with_reference(
            history,
            WorkflowRuntimeEventKind.PLAN_RECORDED,
            "foreground-plan",
            plan.identity.value,
        )
        if existing is not None:
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.IDEMPOTENT,
                existing,
                (),
            )
        active = _active_occurrence(history, preflight.run.revision)
        if (
            active is None
            or active.identity != retained.identity
            or history.head.core_revision != preflight.run.revision
            or history.head.core_state_identity != preflight.prior_state.identity
        ):
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.CONFLICT,
                None,
                ("plan_occurrence_not_active",),
            )
        other = next(
            (
                event
                for event in history.events
                if event.kind is WorkflowRuntimeEventKind.PLAN_RECORDED
                and event.occurrence_identity == plan.occurrence_identity
            ),
            None,
        )
        if other is not None:
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.CONFLICT,
                None,
                ("occurrence_plan_collision",),
            )
        event = _next_event(
            history,
            kind=WorkflowRuntimeEventKind.PLAN_RECORDED,
            core_revision=preflight.run.revision,
            core_state_identity=preflight.prior_state.identity,
            occurrence_identity=plan.occurrence_identity,
            request_identity=preflight.request.identity,
            operation_identity=preflight.request.operation_identity,
            evidence_references=(
                WorkflowRuntimeEvidenceReference(
                    "adapter", plan.adapter_identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "adapter-configuration",
                    plan.adapter_configuration_identity.value,
                ),
                WorkflowRuntimeEvidenceReference(
                    "final-effect-intent",
                    plan.effect_intents[-1].identity.value,
                ),
                WorkflowRuntimeEvidenceReference(
                    "foreground-plan", plan.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "workflow-definition", plan.definition_identity.value
                ),
                *tuple(
                    WorkflowRuntimeEvidenceReference(
                        "effect-intent", intent.identity.value
                    )
                    for intent in plan.effect_intents
                ),
            ),
        )
        return _foreground_append_result(
            self._repository.append(
                event,
                expected_event_identity=history.head.identity,
                idempotency_identity=f"runtime-plan:{event.identity.value}",
            )
        )

    def _record_authority_rejection(
        self,
        preflight: WorkflowTransitionPreflightInput,
        plan: WorkflowForegroundPlan,
        verification: WorkflowAuthorityVerification,
    ) -> WorkflowForegroundActionResult:
        """Retain an application-policy rejection without calling a worker."""
        if type(preflight) is not WorkflowTransitionPreflightInput:
            raise TypeError("preflight must be WorkflowTransitionPreflightInput")
        if type(plan) is not WorkflowForegroundPlan:
            raise TypeError("plan must be WorkflowForegroundPlan")
        if type(verification) is not WorkflowAuthorityVerification:
            raise TypeError("verification must be WorkflowAuthorityVerification")
        if (
            verification.kind is not WorkflowAuthorityVerificationKind.REJECTED
            or verification.occurrence_identity != plan.occurrence_identity
            or verification.plan_identity != plan.identity
            or verification.authority_reference_identity
            != preflight.request.authority_reference.identity
            or verification.authority_version
            != preflight.request.authority_reference.authority_version
            or verification.effect_intent_identity
            not in {intent.identity for intent in plan.effect_intents}
            or verification.attempt_identity
            != WorkflowAttemptIdentity.create(
                occurrence_identity=plan.occurrence_identity,
                effect_intent_identity=verification.effect_intent_identity,
                attempt_ordinal=1,
            )
        ):
            raise ValueError("authority rejection is not correlated")
        loaded = self._repository.load(preflight.run.identity.value)
        if loaded.status is not WorkflowHistoryLoadStatus.LOADED:
            return _foreground_load_failure(loaded.status, loaded.diagnostics)
        assert loaded.history is not None
        history = loaded.history
        if not _preflight_correlates(
            history,
            preflight,
            plan.occurrence_identity,
            plan=plan,
        ):
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.CONFLICT,
                None,
                ("preflight_occurrence_mismatch",),
            )
        plan_event = _event_with_reference(
            history,
            WorkflowRuntimeEventKind.PLAN_RECORDED,
            "foreground-plan",
            plan.identity.value,
        )
        existing = _event_with_reference(
            history,
            WorkflowRuntimeEventKind.AUTHORITY_REJECTED,
            "authority-verification",
            verification.identity.value,
        )
        if existing is not None:
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.IDEMPOTENT,
                existing,
                (),
            )
        active = _active_occurrence(history, preflight.run.revision)
        dispatch_began = any(
            event.occurrence_identity == plan.occurrence_identity
            and event.kind
            in {
                WorkflowRuntimeEventKind.DISPATCH_AUTHORIZED,
                WorkflowRuntimeEventKind.EXECUTION_RECORDED,
            }
            for event in history.events
        )
        if dispatch_began:
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.CONFLICT,
                None,
                ("authority_rejection_after_dispatch",),
            )
        if (
            plan_event is None
            or active is None
            or active.occurrence_identity != plan.occurrence_identity
        ):
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.CONFLICT,
                None,
                ("plan_not_retained",),
            )
        event = _next_event(
            history,
            kind=WorkflowRuntimeEventKind.AUTHORITY_REJECTED,
            core_revision=preflight.run.revision,
            core_state_identity=preflight.prior_state.identity,
            occurrence_identity=plan.occurrence_identity,
            request_identity=preflight.request.identity,
            operation_identity=preflight.request.operation_identity,
            evidence_references=(
                WorkflowRuntimeEvidenceReference(
                    "authority-verification", verification.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "foreground-plan", plan.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "effect-intent",
                    verification.effect_intent_identity.value,
                ),
                WorkflowRuntimeEvidenceReference(
                    "workflow-attempt",
                    verification.attempt_identity.value,
                ),
            ),
            reason_codes=verification.reason_codes,
        )
        appended = _foreground_append_result(
            self._repository.append(
                event,
                expected_event_identity=history.head.identity,
                idempotency_identity=(
                    f"runtime-authority-rejection:{event.identity.value}"
                ),
            )
        )
        if appended.status is WorkflowForegroundActionStatus.RECORDED:
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.REJECTED,
                appended.event,
                appended.diagnostics,
            )
        return appended

    def _dispatch_foreground(
        self,
        preflight: WorkflowTransitionPreflightInput,
        request: WorkflowForegroundExecutionRequest,
        authority_verification: WorkflowAuthorityVerification,
        worker: AbstractWorkflowForegroundWorker,
    ) -> WorkflowForegroundActionResult:
        """Retain authorization, invoke one worker, and retain its evidence.

        The method performs application-owned external I/O only through
        ``worker``.  It never calls a worker when authorization was previously
        retained without conclusive execution evidence; that boundary requires
        reconciliation.
        """
        if type(preflight) is not WorkflowTransitionPreflightInput:
            raise TypeError("preflight must be WorkflowTransitionPreflightInput")
        if type(request) is not WorkflowForegroundExecutionRequest:
            raise TypeError("request must be WorkflowForegroundExecutionRequest")
        if type(authority_verification) is not WorkflowAuthorityVerification:
            raise TypeError(
                "authority_verification must be WorkflowAuthorityVerification"
            )
        if not isinstance(worker, AbstractWorkflowForegroundWorker):
            raise TypeError("worker must be AbstractWorkflowForegroundWorker")
        authorization = request.authorization
        if (
            authority_verification.kind
            is not WorkflowAuthorityVerificationKind.ACCEPTED
            or authority_verification.identity
            != authorization.authority_verification_identity
            or authority_verification.occurrence_identity
            != request.plan.occurrence_identity
            or authority_verification.plan_identity != request.plan.identity
            or authority_verification.effect_intent_identity
            != request.effect_intent.identity
            or authority_verification.attempt_identity != authorization.attempt_identity
            or authority_verification.authority_reference_identity
            != preflight.request.authority_reference.identity
            or authority_verification.authority_version
            != preflight.request.authority_reference.authority_version
        ):
            raise ValueError("dispatch authority or worker is not correlated")
        loaded = self._repository.load(preflight.run.identity.value)
        if loaded.status is not WorkflowHistoryLoadStatus.LOADED:
            return _foreground_load_failure(loaded.status, loaded.diagnostics)
        assert loaded.history is not None
        history = loaded.history
        if not _preflight_correlates(
            history,
            preflight,
            request.plan.occurrence_identity,
            plan=request.plan,
        ):
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.CONFLICT,
                None,
                ("preflight_occurrence_mismatch",),
            )
        if not _plan_is_retained(history, request.plan):
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.CONFLICT,
                None,
                ("plan_not_retained",),
            )
        existing_execution = _event_with_reference(
            history,
            WorkflowRuntimeEventKind.EXECUTION_RECORDED,
            "dispatch-authorization",
            authorization.identity.value,
        )
        if existing_execution is not None:
            retained_evidence = _execution_evidence_from_event(
                existing_execution, request
            )
            if retained_evidence is None:
                return WorkflowForegroundActionResult(
                    WorkflowForegroundActionStatus.INDETERMINATE,
                    existing_execution,
                    ("retained_execution_evidence_not_reconstructible",),
                )
            exhausted = _event_with_reference(
                history,
                WorkflowRuntimeEventKind.TERMINAL_FAILURE_RECORDED,
                "execution-evidence",
                retained_evidence.identity.value,
            )
            if exhausted is not None:
                return WorkflowForegroundActionResult(
                    WorkflowForegroundActionStatus.ATTEMPTS_EXHAUSTED,
                    exhausted,
                    (),
                    retained_evidence,
                )
            if (
                retained_evidence.outcome
                in {
                    WorkflowEffectOutcomeKind.KNOWN_NOT_APPLIED,
                    WorkflowEffectOutcomeKind.REJECTED_BEFORE_EFFECT,
                }
                and request.attempt_ordinal == request.plan.maximum_attempts_per_intent
            ):
                return _record_attempt_exhaustion(
                    self._repository,
                    preflight,
                    request,
                    retained_evidence,
                    reconciliation_evidence=None,
                )
            status = (
                WorkflowForegroundActionStatus.RECONCILIATION_REQUIRED
                if retained_evidence.outcome is WorkflowEffectOutcomeKind.AMBIGUOUS
                else WorkflowForegroundActionStatus.IDEMPOTENT
            )
            return WorkflowForegroundActionResult(
                status,
                existing_execution,
                (),
                retained_evidence,
            )
        existing_authorization = _event_with_reference(
            history,
            WorkflowRuntimeEventKind.DISPATCH_AUTHORIZED,
            "dispatch-authorization",
            authorization.identity.value,
        )
        if existing_authorization is not None:
            recovered_evidence = WorkflowExecutionEvidence.create(
                request=request,
                outcome=WorkflowEffectOutcomeKind.AMBIGUOUS,
                evidence_references=(),
                reason_codes=("authorization_without_worker_report",),
            )
            recovery_event = _next_event(
                history,
                kind=WorkflowRuntimeEventKind.EXECUTION_RECORDED,
                core_revision=preflight.run.revision,
                core_state_identity=preflight.prior_state.identity,
                occurrence_identity=request.plan.occurrence_identity,
                request_identity=preflight.request.identity,
                operation_identity=preflight.request.operation_identity,
                evidence_references=(
                    WorkflowRuntimeEvidenceReference(
                        "dispatch-authorization",
                        authorization.identity.value,
                    ),
                    WorkflowRuntimeEvidenceReference(
                        "effect-intent",
                        request.effect_intent.identity.value,
                    ),
                    WorkflowRuntimeEvidenceReference(
                        "execution-evidence",
                        recovered_evidence.identity.value,
                    ),
                    WorkflowRuntimeEvidenceReference(
                        "foreground-plan", request.plan.identity.value
                    ),
                    WorkflowRuntimeEvidenceReference(
                        "workflow-attempt",
                        authorization.attempt_identity.value,
                    ),
                ),
                reason_codes=(
                    recovered_evidence.outcome.value,
                    *recovered_evidence.reason_codes,
                ),
            )
            recovered_append = _foreground_append_result(
                self._repository.append(
                    recovery_event,
                    expected_event_identity=history.head.identity,
                    idempotency_identity=(
                        f"runtime-execution:{recovery_event.identity.value}"
                    ),
                ),
                execution_evidence=recovered_evidence,
            )
            if recovered_append.status in {
                WorkflowForegroundActionStatus.RECORDED,
                WorkflowForegroundActionStatus.IDEMPOTENT,
            }:
                return WorkflowForegroundActionResult(
                    WorkflowForegroundActionStatus.RECONCILIATION_REQUIRED,
                    recovered_append.event,
                    ("authorized_attempt_requires_reconciliation",),
                    recovered_evidence,
                )
            return recovered_append
        active = _active_occurrence(history, preflight.run.revision)
        if (
            active is None
            or active.occurrence_identity != request.plan.occurrence_identity
            or history.head.core_revision != preflight.run.revision
            or history.head.core_state_identity != preflight.prior_state.identity
        ):
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.CONFLICT,
                None,
                ("occurrence_not_active",),
            )
        if worker.identity != authorization.worker_identity:
            raise ValueError("dispatch worker is not correlated")
        if not _predecessor_intents_are_applied(history, request):
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.CONFLICT,
                None,
                ("predecessor_effect_not_applied",),
            )
        if not _attempt_is_allowed(history, request):
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.CONFLICT,
                None,
                ("attempt_not_allowed",),
            )
        authorization_event = _next_event(
            history,
            kind=WorkflowRuntimeEventKind.DISPATCH_AUTHORIZED,
            core_revision=preflight.run.revision,
            core_state_identity=preflight.prior_state.identity,
            occurrence_identity=request.plan.occurrence_identity,
            request_identity=preflight.request.identity,
            operation_identity=preflight.request.operation_identity,
            evidence_references=(
                WorkflowRuntimeEvidenceReference(
                    "authority-verification",
                    authority_verification.identity.value,
                ),
                WorkflowRuntimeEvidenceReference(
                    "dispatch-authorization", authorization.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "effect-intent", request.effect_intent.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "foreground-plan", request.plan.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "workflow-attempt", authorization.attempt_identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "workflow-worker", authorization.worker_identity.value
                ),
            ),
        )
        authorization_append = _foreground_append_result(
            self._repository.append(
                authorization_event,
                expected_event_identity=history.head.identity,
                idempotency_identity=(
                    f"runtime-dispatch-authorization:"
                    f"{authorization_event.identity.value}"
                ),
            )
        )
        if authorization_append.status is not (WorkflowForegroundActionStatus.RECORDED):
            return authorization_append
        try:
            evidence = worker.action(request=request)
        except Exception:  # worker exceptions cross an ambiguous effect boundary
            evidence = WorkflowExecutionEvidence.create(
                request=request,
                outcome=WorkflowEffectOutcomeKind.AMBIGUOUS,
                evidence_references=(),
                reason_codes=("worker_exception",),
            )
        if not _execution_evidence_matches(evidence, request):
            evidence = WorkflowExecutionEvidence.create(
                request=request,
                outcome=WorkflowEffectOutcomeKind.AMBIGUOUS,
                evidence_references=(),
                reason_codes=("worker_evidence_invalid",),
            )
        reloaded = self._repository.load(preflight.run.identity.value)
        if (
            reloaded.status is not WorkflowHistoryLoadStatus.LOADED
            or reloaded.history is None
            or reloaded.history.head.identity != authorization_event.identity
        ):
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.INDETERMINATE,
                authorization_event,
                ("authorization_head_changed_after_worker",),
                evidence,
            )
        execution_event = _next_event(
            reloaded.history,
            kind=WorkflowRuntimeEventKind.EXECUTION_RECORDED,
            core_revision=preflight.run.revision,
            core_state_identity=preflight.prior_state.identity,
            occurrence_identity=request.plan.occurrence_identity,
            request_identity=preflight.request.identity,
            operation_identity=preflight.request.operation_identity,
            evidence_references=(
                WorkflowRuntimeEvidenceReference(
                    "dispatch-authorization", authorization.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "effect-intent", request.effect_intent.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "execution-evidence", evidence.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "foreground-plan", request.plan.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "workflow-attempt", authorization.attempt_identity.value
                ),
                *evidence.evidence_references,
            ),
            reason_codes=(evidence.outcome.value, *evidence.reason_codes),
        )
        execution_append = _foreground_append_result(
            self._repository.append(
                execution_event,
                expected_event_identity=authorization_event.identity,
                idempotency_identity=(
                    f"runtime-execution:{execution_event.identity.value}"
                ),
            ),
            execution_evidence=evidence,
        )
        if execution_append.status not in {
            WorkflowForegroundActionStatus.RECORDED,
            WorkflowForegroundActionStatus.IDEMPOTENT,
        }:
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.INDETERMINATE,
                authorization_event,
                (
                    *execution_append.diagnostics,
                    "worker_evidence_not_retained",
                ),
                evidence,
            )
        if (
            execution_append.status
            in {
                WorkflowForegroundActionStatus.RECORDED,
                WorkflowForegroundActionStatus.IDEMPOTENT,
            }
            and evidence.outcome
            in {
                WorkflowEffectOutcomeKind.KNOWN_NOT_APPLIED,
                WorkflowEffectOutcomeKind.REJECTED_BEFORE_EFFECT,
            }
            and request.attempt_ordinal == request.plan.maximum_attempts_per_intent
        ):
            return _record_attempt_exhaustion(
                self._repository,
                preflight,
                request,
                evidence,
                reconciliation_evidence=None,
            )
        if (
            execution_append.status
            in {
                WorkflowForegroundActionStatus.RECORDED,
                WorkflowForegroundActionStatus.IDEMPOTENT,
            }
            and evidence.outcome is WorkflowEffectOutcomeKind.AMBIGUOUS
        ):
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.RECONCILIATION_REQUIRED,
                execution_append.event,
                execution_append.diagnostics,
                evidence,
            )
        return execution_append

    def _reconcile_foreground(
        self,
        preflight: WorkflowTransitionPreflightInput,
        request: WorkflowReconciliationRequest,
        reconciler: AbstractWorkflowEffectReconciler,
    ) -> WorkflowForegroundActionResult:
        """Invoke one query-only reconciler and retain bounded evidence."""
        if type(preflight) is not WorkflowTransitionPreflightInput:
            raise TypeError("preflight must be WorkflowTransitionPreflightInput")
        if type(request) is not WorkflowReconciliationRequest:
            raise TypeError("request must be WorkflowReconciliationRequest")
        if not isinstance(reconciler, AbstractWorkflowEffectReconciler):
            raise TypeError("reconciler must be AbstractWorkflowEffectReconciler")
        loaded = self._repository.load(preflight.run.identity.value)
        if loaded.status is not WorkflowHistoryLoadStatus.LOADED:
            return _foreground_load_failure(loaded.status, loaded.diagnostics)
        assert loaded.history is not None
        history = loaded.history
        if not _preflight_correlates(
            history,
            preflight,
            request.execution_request.plan.occurrence_identity,
            plan=request.execution_request.plan,
        ):
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.CONFLICT,
                None,
                ("preflight_occurrence_mismatch",),
            )
        execution = request.execution_evidence
        retained_execution = _event_with_reference(
            history,
            WorkflowRuntimeEventKind.EXECUTION_RECORDED,
            "execution-evidence",
            execution.identity.value,
        )
        if retained_execution is None:
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.CONFLICT,
                None,
                ("ambiguous_execution_not_retained",),
            )
        existing = _event_with_reference(
            history,
            WorkflowRuntimeEventKind.RECONCILIATION_RECORDED,
            "execution-evidence",
            execution.identity.value,
        )
        if existing is not None:
            retained_reconciliation = _reconciliation_evidence_from_event(
                existing, request
            )
            if retained_reconciliation is None:
                return WorkflowForegroundActionResult(
                    WorkflowForegroundActionStatus.INDETERMINATE,
                    existing,
                    ("retained_reconciliation_not_reconstructible",),
                )
            if (
                retained_reconciliation.outcome
                is WorkflowReconciliationOutcomeKind.CONFIRMED_NOT_APPLIED
                and request.execution_request.attempt_ordinal
                == request.execution_request.plan.maximum_attempts_per_intent
            ):
                return _record_attempt_exhaustion(
                    self._repository,
                    preflight,
                    request.execution_request,
                    request.execution_evidence,
                    reconciliation_evidence=retained_reconciliation,
                )
            unresolved = {
                WorkflowReconciliationOutcomeKind.STILL_AMBIGUOUS,
                WorkflowReconciliationOutcomeKind.CONFIRMED_PARTIAL,
                WorkflowReconciliationOutcomeKind.EVIDENCE_INVALID,
            }
            status = (
                WorkflowForegroundActionStatus.RECONCILIATION_REQUIRED
                if retained_reconciliation.outcome in unresolved
                else WorkflowForegroundActionStatus.IDEMPOTENT
            )
            return WorkflowForegroundActionResult(
                status,
                existing,
                (),
                reconciliation_evidence=retained_reconciliation,
            )
        active = _active_occurrence(history, preflight.run.revision)
        if (
            active is None
            or active.occurrence_identity
            != request.execution_request.plan.occurrence_identity
            or history.head.core_revision != preflight.run.revision
            or history.head.core_state_identity != preflight.prior_state.identity
        ):
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.CONFLICT,
                None,
                ("occurrence_not_active",),
            )
        try:
            evidence = reconciler.action(request=request)
        except Exception:  # reconciliation remains ambiguous on query failure
            evidence = WorkflowReconciliationEvidence.create(
                request=request,
                reconciler_identity=reconciler.identity,
                outcome=WorkflowReconciliationOutcomeKind.STILL_AMBIGUOUS,
                evidence_references=(),
                reason_codes=("reconciler_exception",),
            )
        if not _reconciliation_evidence_matches(
            evidence,
            request,
            reconciler.identity,
        ):
            evidence = WorkflowReconciliationEvidence.create(
                request=request,
                reconciler_identity=reconciler.identity,
                outcome=WorkflowReconciliationOutcomeKind.EVIDENCE_INVALID,
                evidence_references=(),
                reason_codes=("reconciler_evidence_invalid",),
            )
        reloaded = self._repository.load(preflight.run.identity.value)
        if (
            reloaded.status is not WorkflowHistoryLoadStatus.LOADED
            or reloaded.history is None
            or reloaded.history.head.identity != history.head.identity
        ):
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.INDETERMINATE,
                retained_execution,
                ("runtime_head_changed_during_reconciliation",),
                reconciliation_evidence=evidence,
            )
        event = _next_event(
            reloaded.history,
            kind=WorkflowRuntimeEventKind.RECONCILIATION_RECORDED,
            core_revision=preflight.run.revision,
            core_state_identity=preflight.prior_state.identity,
            occurrence_identity=(request.execution_request.plan.occurrence_identity),
            request_identity=preflight.request.identity,
            operation_identity=preflight.request.operation_identity,
            evidence_references=(
                WorkflowRuntimeEvidenceReference(
                    "execution-evidence", execution.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "reconciliation-evidence", evidence.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "workflow-reconciler",
                    evidence.reconciler_identity.value,
                ),
                *evidence.evidence_references,
            ),
            reason_codes=(evidence.outcome.value, *evidence.reason_codes),
        )
        appended = _foreground_append_result(
            self._repository.append(
                event,
                expected_event_identity=reloaded.history.head.identity,
                idempotency_identity=(f"runtime-reconciliation:{event.identity.value}"),
            ),
            reconciliation_evidence=evidence,
        )
        if (
            appended.status
            in {
                WorkflowForegroundActionStatus.RECORDED,
                WorkflowForegroundActionStatus.IDEMPOTENT,
            }
            and evidence.outcome
            is WorkflowReconciliationOutcomeKind.CONFIRMED_NOT_APPLIED
            and request.execution_request.attempt_ordinal
            == request.execution_request.plan.maximum_attempts_per_intent
        ):
            return _record_attempt_exhaustion(
                self._repository,
                preflight,
                request.execution_request,
                request.execution_evidence,
                reconciliation_evidence=evidence,
            )
        if appended.status in {
            WorkflowForegroundActionStatus.RECORDED,
            WorkflowForegroundActionStatus.IDEMPOTENT,
        } and evidence.outcome in {
            WorkflowReconciliationOutcomeKind.STILL_AMBIGUOUS,
            WorkflowReconciliationOutcomeKind.CONFIRMED_PARTIAL,
            WorkflowReconciliationOutcomeKind.EVIDENCE_INVALID,
        }:
            return WorkflowForegroundActionResult(
                WorkflowForegroundActionStatus.RECONCILIATION_REQUIRED,
                appended.event,
                appended.diagnostics,
                reconciliation_evidence=evidence,
            )
        return appended

    def _record_transition(
        self,
        transition_input: WorkflowTransitionInput,
    ) -> WorkflowRuntimeActionResult:
        """Process and retain one pure adapter result for a reserved request."""
        if type(transition_input) is not WorkflowTransitionInput:
            raise TypeError("transition_input must be WorkflowTransitionInput")
        loaded = self._repository.load(transition_input.run.identity.value)
        if loaded.status is not WorkflowHistoryLoadStatus.LOADED:
            return _load_failure_result(loaded.status, loaded.diagnostics)
        assert loaded.history is not None
        history = loaded.history
        request = transition_input.request
        prior = transition_input.prior_state
        retained = _retained_occurrence(history, request.identity.value)
        if retained is None:
            return WorkflowRuntimeActionResult(
                WorkflowRuntimeActionStatus.CONFLICT,
                None,
                ("request_not_reserved",),
            )
        existing = _transition_event(history, request.identity.value)
        if existing is not None:
            return WorkflowRuntimeActionResult(
                WorkflowRuntimeActionStatus.IDEMPOTENT,
                existing,
                (),
            )
        if (
            history.head.core_revision != transition_input.run.revision
            or history.head.core_state_identity != prior.identity
        ):
            return WorkflowRuntimeActionResult(
                WorkflowRuntimeActionStatus.CONFLICT,
                None,
                ("runtime_head_core_mismatch",),
            )
        assert retained.occurrence_identity is not None
        if transition_input.adapter_evidence is not None:
            final_evidence_reference = WorkflowRuntimeEvidenceReference(
                "adapter-evidence",
                transition_input.adapter_evidence.identity.value,
            )
        else:
            assert transition_input.infrastructure_failure is not None
            final_evidence_reference = WorkflowRuntimeEvidenceReference(
                "infrastructure-failure",
                transition_input.infrastructure_failure.identity.value,
            )
        readiness = _foreground_transition_diagnostic(
            history,
            retained.occurrence_identity,
            final_evidence_reference,
        )
        if readiness is not None:
            return WorkflowRuntimeActionResult(
                WorkflowRuntimeActionStatus.CONFLICT,
                None,
                (readiness,),
            )
        transition = self._processor.execute(transition_input)
        successor = transition.outcome.successor_run
        successor_state = transition.outcome.successor_state
        core_revision = (
            transition_input.run.revision if successor is None else successor.revision
        )
        core_state = (
            prior.identity if successor_state is None else successor_state.identity
        )
        evidence = [
            WorkflowRuntimeEvidenceReference(
                "transition-outcome", transition.outcome.identity.value
            ),
            WorkflowRuntimeEvidenceReference(
                "transition-audit", transition.audit_event.identity.value
            ),
            WorkflowRuntimeEvidenceReference(
                "workflow-validation",
                transition.outcome.validation.identity.value,
            ),
        ]
        if transition.outcome.adapter_evidence_identity is not None:
            evidence.append(
                WorkflowRuntimeEvidenceReference(
                    "adapter-evidence",
                    transition.outcome.adapter_evidence_identity.value,
                )
            )
        if transition.outcome.infrastructure_failure_identity is not None:
            evidence.append(
                WorkflowRuntimeEvidenceReference(
                    "infrastructure-failure",
                    transition.outcome.infrastructure_failure_identity.value,
                )
            )
        event = _next_event(
            history,
            kind=WorkflowRuntimeEventKind.TRANSITION_RECORDED,
            core_revision=core_revision,
            core_state_identity=core_state,
            occurrence_identity=retained.occurrence_identity,
            request_identity=request.identity,
            operation_identity=request.operation_identity,
            evidence_references=tuple(evidence),
            reason_codes=(transition.outcome.kind.value,),
        )
        return _append_result(
            self._repository.append(
                event,
                expected_event_identity=history.head.identity,
                idempotency_identity=f"runtime-transition:{event.identity.value}",
            ),
            validation=transition.outcome.validation,
            transition=transition,
        )


def _next_event(
    history: WorkflowRuntimeHistory,
    *,
    kind: WorkflowRuntimeEventKind,
    core_revision: int,
    core_state_identity: WorkflowStateIdentity,
    occurrence_identity: WorkflowOccurrenceIdentity | None,
    request_identity: WorkflowTransitionRequestIdentity | None,
    operation_identity: WorkflowOperationIdentity | None,
    evidence_references: tuple[WorkflowRuntimeEvidenceReference, ...],
    reason_codes: tuple[str, ...] = (),
) -> WorkflowRuntimeEvent:
    return WorkflowRuntimeEvent.create(
        kind=kind,
        run_identity=history.head.run_identity,
        ordinal=history.head.ordinal + 1,
        predecessor_event_identity=history.head.identity,
        core_revision=core_revision,
        core_state_identity=core_state_identity,
        occurrence_identity=occurrence_identity,
        request_identity=request_identity,
        operation_identity=operation_identity,
        evidence_references=evidence_references,
        reason_codes=reason_codes,
    )


def _request_event(
    history: WorkflowRuntimeHistory,
    request_identity: str,
) -> WorkflowRuntimeEvent | None:
    return next(
        (
            event
            for event in history.events
            if event.request_identity is not None
            and event.request_identity.value == request_identity
            and event.kind
            in {
                WorkflowRuntimeEventKind.REQUEST_RETAINED,
                WorkflowRuntimeEventKind.REQUEST_CONFLICT_RECORDED,
                WorkflowRuntimeEventKind.PREFLIGHT_REJECTED,
            }
        ),
        None,
    )


def _idempotency_owner(
    history: WorkflowRuntimeHistory,
    idempotency_identity: str,
) -> WorkflowRuntimeEvent | None:
    return next(
        (
            event
            for event in history.events
            if event.kind
            in {
                WorkflowRuntimeEventKind.REQUEST_RETAINED,
                WorkflowRuntimeEventKind.PREFLIGHT_REJECTED,
            }
            and any(
                reference.reference_kind == "request-idempotency"
                and reference.reference_identity == idempotency_identity
                for reference in event.evidence_references
            )
        ),
        None,
    )


def _active_occurrence(
    history: WorkflowRuntimeHistory,
    revision: int,
) -> WorkflowRuntimeEvent | None:
    retained = [
        event
        for event in history.events
        if event.kind is WorkflowRuntimeEventKind.REQUEST_RETAINED
        and event.core_revision == revision
    ]
    for event in reversed(retained):
        assert event.occurrence_identity is not None
        completed = any(
            later.kind
            in {
                WorkflowRuntimeEventKind.AUTHORITY_REJECTED,
                WorkflowRuntimeEventKind.PLAN_REJECTED,
                WorkflowRuntimeEventKind.TERMINAL_FAILURE_RECORDED,
                WorkflowRuntimeEventKind.TRANSITION_RECORDED,
            }
            and later.occurrence_identity == event.occurrence_identity
            for later in history.events[event.ordinal + 1 :]
        )
        if not completed:
            return event
    return None


def _retained_occurrence(
    history: WorkflowRuntimeHistory,
    request_identity: str,
) -> WorkflowRuntimeEvent | None:
    return next(
        (
            event
            for event in history.events
            if event.kind is WorkflowRuntimeEventKind.REQUEST_RETAINED
            and event.request_identity is not None
            and event.request_identity.value == request_identity
        ),
        None,
    )


def _transition_event(
    history: WorkflowRuntimeHistory,
    request_identity: str,
) -> WorkflowRuntimeEvent | None:
    return next(
        (
            event
            for event in history.events
            if event.kind is WorkflowRuntimeEventKind.TRANSITION_RECORDED
            and event.request_identity is not None
            and event.request_identity.value == request_identity
        ),
        None,
    )


def _preflight_correlates(
    history: WorkflowRuntimeHistory,
    preflight: WorkflowTransitionPreflightInput,
    occurrence_identity: WorkflowOccurrenceIdentity,
    *,
    plan: WorkflowForegroundPlan | None = None,
) -> bool:
    expected_occurrence = WorkflowOccurrenceIdentity.create(
        run_identity=preflight.run.identity,
        state_identity=preflight.prior_state.identity,
        revision=preflight.run.revision,
        request_identity=preflight.request.identity,
    )
    retained = _retained_occurrence(history, preflight.request.identity.value)
    if (
        expected_occurrence != occurrence_identity
        or retained is None
        or retained.occurrence_identity != occurrence_identity
        or retained.request_identity != preflight.request.identity
        or retained.operation_identity != preflight.request.operation_identity
    ):
        return False
    if plan is None:
        return True
    plan_event = _event_with_reference(
        history,
        WorkflowRuntimeEventKind.PLAN_RECORDED,
        "foreground-plan",
        plan.identity.value,
    )
    return (
        plan.definition_identity == preflight.definition.identity
        and plan_event is not None
        and plan_event.occurrence_identity == occurrence_identity
        and plan_event.request_identity == preflight.request.identity
        and plan_event.operation_identity == preflight.request.operation_identity
    )


def _event_with_reference(
    history: WorkflowRuntimeHistory,
    kind: WorkflowRuntimeEventKind,
    reference_kind: str,
    reference_identity: str,
) -> WorkflowRuntimeEvent | None:
    return next(
        (
            event
            for event in history.events
            if event.kind is kind
            and any(
                reference.reference_kind == reference_kind
                and reference.reference_identity == reference_identity
                for reference in event.evidence_references
            )
        ),
        None,
    )


def _plan_is_retained(
    history: WorkflowRuntimeHistory,
    plan: WorkflowForegroundPlan,
) -> bool:
    event = _event_with_reference(
        history,
        WorkflowRuntimeEventKind.PLAN_RECORDED,
        "foreground-plan",
        plan.identity.value,
    )
    return event is not None and event.occurrence_identity == (plan.occurrence_identity)


def _predecessor_intents_are_applied(
    history: WorkflowRuntimeHistory,
    request: WorkflowForegroundExecutionRequest,
) -> bool:
    predecessors = request.plan.effect_intents[: request.effect_intent.ordinal]
    return all(
        _effect_intent_is_applied(history, intent.identity.value)
        for intent in predecessors
    )


def _execution_outcome(
    event: WorkflowRuntimeEvent,
) -> WorkflowEffectOutcomeKind | None:
    matches = tuple(
        candidate
        for candidate in (
            *WorkflowEffectOutcomeKind,
            *WorkflowReconciliationOutcomeKind,
        )
        if candidate.value in event.reason_codes
    )
    if len(matches) != 1 or type(matches[0]) is not WorkflowEffectOutcomeKind:
        return None
    return matches[0]


def _reconciliation_outcome(
    event: WorkflowRuntimeEvent,
) -> WorkflowReconciliationOutcomeKind | None:
    matches = tuple(
        candidate
        for candidate in (
            *WorkflowEffectOutcomeKind,
            *WorkflowReconciliationOutcomeKind,
        )
        if candidate.value in event.reason_codes
    )
    if len(matches) != 1 or type(matches[0]) is not WorkflowReconciliationOutcomeKind:
        return None
    return matches[0]


def _effect_intent_is_applied(
    history: WorkflowRuntimeHistory,
    intent_identity: str,
) -> bool:
    return _conclusive_effect_event(history, intent_identity) is not None


def _conclusive_effect_event(
    history: WorkflowRuntimeHistory,
    intent_identity: str,
) -> WorkflowRuntimeEvent | None:
    executions = tuple(
        event
        for event in history.events
        if event.kind is WorkflowRuntimeEventKind.EXECUTION_RECORDED
        and any(
            reference.reference_kind == "effect-intent"
            and reference.reference_identity == intent_identity
            for reference in event.evidence_references
        )
    )
    if not executions:
        return None
    latest = executions[-1]
    outcome = _execution_outcome(latest)
    if outcome in {
        WorkflowEffectOutcomeKind.SUCCEEDED,
        WorkflowEffectOutcomeKind.KNOWN_APPLIED_WITH_FAILURE,
    }:
        return latest
    if outcome is not WorkflowEffectOutcomeKind.AMBIGUOUS:
        return None
    execution_reference = next(
        (
            reference.reference_identity
            for reference in latest.evidence_references
            if reference.reference_kind == "execution-evidence"
        ),
        None,
    )
    if execution_reference is None:
        return None
    reconciliation = _event_with_reference(
        history,
        WorkflowRuntimeEventKind.RECONCILIATION_RECORDED,
        "execution-evidence",
        execution_reference,
    )
    if reconciliation is None:
        return None
    if (
        _reconciliation_outcome(reconciliation)
        is not WorkflowReconciliationOutcomeKind.CONFIRMED_APPLIED
    ):
        return None
    return reconciliation


def _foreground_transition_diagnostic(
    history: WorkflowRuntimeHistory,
    occurrence_identity: WorkflowOccurrenceIdentity,
    final_evidence_reference: WorkflowRuntimeEvidenceReference,
) -> str | None:
    plan_event = next(
        (
            event
            for event in history.events
            if event.kind is WorkflowRuntimeEventKind.PLAN_RECORDED
            and event.occurrence_identity == occurrence_identity
            and any(
                reference.reference_kind == "foreground-plan"
                for reference in event.evidence_references
            )
        ),
        None,
    )
    if plan_event is None:
        return None
    intent_identities = tuple(
        reference.reference_identity
        for reference in plan_event.evidence_references
        if reference.reference_kind == "effect-intent"
    )
    if not intent_identities:
        return "foreground_plan_has_no_effect_intents"
    if not all(
        _effect_intent_is_applied(history, identity) for identity in intent_identities
    ):
        return "foreground_effects_not_conclusively_applied"
    final_intent_identity = next(
        (
            reference.reference_identity
            for reference in plan_event.evidence_references
            if reference.reference_kind == "final-effect-intent"
        ),
        None,
    )
    if final_intent_identity is None:
        return "foreground_plan_has_no_final_effect_intent"
    conclusive_event = _conclusive_effect_event(history, final_intent_identity)
    if (
        conclusive_event is None
        or conclusive_event.occurrence_identity != occurrence_identity
        or final_evidence_reference not in conclusive_event.evidence_references
    ):
        return "foreground_final_evidence_not_bound"
    return None


def _attempt_is_allowed(
    history: WorkflowRuntimeHistory,
    request: WorkflowForegroundExecutionRequest,
) -> bool:
    intent_identity = request.effect_intent.identity.value
    executions = tuple(
        event
        for event in history.events
        if event.kind is WorkflowRuntimeEventKind.EXECUTION_RECORDED
        and any(
            reference.reference_kind == "effect-intent"
            and reference.reference_identity == intent_identity
            for reference in event.evidence_references
        )
    )
    if len(executions) != request.attempt_ordinal - 1:
        return False
    authorizations = tuple(
        event
        for event in history.events
        if event.kind is WorkflowRuntimeEventKind.DISPATCH_AUTHORIZED
        and any(
            reference.reference_kind == "effect-intent"
            and reference.reference_identity == intent_identity
            for reference in event.evidence_references
        )
    )
    if len(authorizations) != len(executions):
        return False
    if not executions:
        return request.attempt_ordinal == 1
    last = executions[-1]
    outcome = _execution_outcome(last)
    retryable = {
        WorkflowEffectOutcomeKind.KNOWN_NOT_APPLIED,
        WorkflowEffectOutcomeKind.REJECTED_BEFORE_EFFECT,
    }
    if outcome in retryable:
        return True
    if outcome is not WorkflowEffectOutcomeKind.AMBIGUOUS:
        return False
    execution_reference = next(
        (
            reference.reference_identity
            for reference in last.evidence_references
            if reference.reference_kind == "execution-evidence"
        ),
        None,
    )
    if execution_reference is None:
        return False
    reconciliation = _event_with_reference(
        history,
        WorkflowRuntimeEventKind.RECONCILIATION_RECORDED,
        "execution-evidence",
        execution_reference,
    )
    return reconciliation is not None and (
        _reconciliation_outcome(reconciliation)
        is WorkflowReconciliationOutcomeKind.CONFIRMED_NOT_APPLIED
    )


def _execution_evidence_from_event(
    event: WorkflowRuntimeEvent,
    request: WorkflowForegroundExecutionRequest,
) -> WorkflowExecutionEvidence | None:
    outcome = _execution_outcome(event)
    identity = next(
        (
            reference.reference_identity
            for reference in event.evidence_references
            if reference.reference_kind == "execution-evidence"
        ),
        None,
    )
    if outcome is None or identity is None:
        return None
    runtime_reference_kinds = {
        "dispatch-authorization",
        "effect-intent",
        "execution-evidence",
        "foreground-plan",
        "workflow-attempt",
    }
    evidence_references = tuple(
        reference
        for reference in event.evidence_references
        if reference.reference_kind not in runtime_reference_kinds
    )
    reason_codes = tuple(
        reason for reason in event.reason_codes if reason != outcome.value
    )
    try:
        evidence = WorkflowExecutionEvidence.create(
            request=request,
            outcome=outcome,
            evidence_references=evidence_references,
            reason_codes=reason_codes,
        )
    except TypeError, ValueError:
        return None
    if evidence.identity.value != identity:
        return None
    return evidence


def _execution_evidence_matches(
    evidence: WorkflowExecutionEvidence,
    request: WorkflowForegroundExecutionRequest,
) -> bool:
    return type(evidence) is WorkflowExecutionEvidence and (
        evidence.occurrence_identity == request.plan.occurrence_identity
        and evidence.plan_identity == request.plan.identity
        and evidence.effect_intent_identity == request.effect_intent.identity
        and evidence.attempt_identity == request.authorization.attempt_identity
        and evidence.dispatch_authorization_identity == request.authorization.identity
        and evidence.worker_identity == request.authorization.worker_identity
    )


def _reconciliation_evidence_from_event(
    event: WorkflowRuntimeEvent,
    request: WorkflowReconciliationRequest,
) -> WorkflowReconciliationEvidence | None:
    outcome = _reconciliation_outcome(event)
    identity = next(
        (
            reference.reference_identity
            for reference in event.evidence_references
            if reference.reference_kind == "reconciliation-evidence"
        ),
        None,
    )
    reconciler_identity = next(
        (
            reference.reference_identity
            for reference in event.evidence_references
            if reference.reference_kind == "workflow-reconciler"
        ),
        None,
    )
    if outcome is None or identity is None or reconciler_identity is None:
        return None
    runtime_reference_kinds = {
        "execution-evidence",
        "reconciliation-evidence",
        "workflow-reconciler",
    }
    evidence_references = tuple(
        reference
        for reference in event.evidence_references
        if reference.reference_kind not in runtime_reference_kinds
    )
    reason_codes = tuple(
        reason for reason in event.reason_codes if reason != outcome.value
    )
    try:
        evidence = WorkflowReconciliationEvidence.create(
            request=request,
            reconciler_identity=WorkflowEffectReconcilerIdentity(reconciler_identity),
            outcome=outcome,
            evidence_references=evidence_references,
            reason_codes=reason_codes,
        )
    except TypeError, ValueError:
        return None
    if evidence.identity.value != identity:
        return None
    return evidence


def _reconciliation_evidence_matches(
    evidence: WorkflowReconciliationEvidence,
    request: WorkflowReconciliationRequest,
    reconciler_identity: WorkflowEffectReconcilerIdentity,
) -> bool:
    return type(evidence) is WorkflowReconciliationEvidence and (
        evidence.execution_evidence_identity == request.execution_evidence.identity
        and evidence.reconciler_identity == reconciler_identity
    )


def _record_attempt_exhaustion(
    repository: WorkflowRuntimeRepository,
    preflight: WorkflowTransitionPreflightInput,
    request: WorkflowForegroundExecutionRequest,
    execution_evidence: WorkflowExecutionEvidence,
    *,
    reconciliation_evidence: WorkflowReconciliationEvidence | None,
) -> WorkflowForegroundActionResult:
    loaded = repository.load(preflight.run.identity.value)
    if loaded.status is not WorkflowHistoryLoadStatus.LOADED:
        return _foreground_load_failure(loaded.status, loaded.diagnostics)
    assert loaded.history is not None
    history = loaded.history
    existing = _event_with_reference(
        history,
        WorkflowRuntimeEventKind.TERMINAL_FAILURE_RECORDED,
        "execution-evidence",
        execution_evidence.identity.value,
    )
    if existing is not None:
        return WorkflowForegroundActionResult(
            WorkflowForegroundActionStatus.ATTEMPTS_EXHAUSTED,
            existing,
            (),
            execution_evidence,
        )
    active = _active_occurrence(history, preflight.run.revision)
    if (
        active is None
        or active.occurrence_identity != request.plan.occurrence_identity
        or history.head.core_revision != preflight.run.revision
        or history.head.core_state_identity != preflight.prior_state.identity
    ):
        return WorkflowForegroundActionResult(
            WorkflowForegroundActionStatus.CONFLICT,
            None,
            ("occurrence_not_active_at_attempt_exhaustion",),
            execution_evidence,
        )
    references = [
        WorkflowRuntimeEvidenceReference(
            "effect-intent", request.effect_intent.identity.value
        ),
        WorkflowRuntimeEvidenceReference(
            "execution-evidence", execution_evidence.identity.value
        ),
        WorkflowRuntimeEvidenceReference(
            "workflow-attempt", request.authorization.attempt_identity.value
        ),
    ]
    if reconciliation_evidence is not None:
        references.append(
            WorkflowRuntimeEvidenceReference(
                "reconciliation-evidence",
                reconciliation_evidence.identity.value,
            )
        )
    event = _next_event(
        history,
        kind=WorkflowRuntimeEventKind.TERMINAL_FAILURE_RECORDED,
        core_revision=preflight.run.revision,
        core_state_identity=preflight.prior_state.identity,
        occurrence_identity=request.plan.occurrence_identity,
        request_identity=preflight.request.identity,
        operation_identity=preflight.request.operation_identity,
        evidence_references=tuple(references),
        reason_codes=("attempts_exhausted",),
    )
    appended = _foreground_append_result(
        repository.append(
            event,
            expected_event_identity=history.head.identity,
            idempotency_identity=(f"runtime-attempt-exhaustion:{event.identity.value}"),
        ),
        execution_evidence=execution_evidence,
    )
    if appended.status in {
        WorkflowForegroundActionStatus.RECORDED,
        WorkflowForegroundActionStatus.IDEMPOTENT,
    }:
        return WorkflowForegroundActionResult(
            WorkflowForegroundActionStatus.ATTEMPTS_EXHAUSTED,
            appended.event,
            appended.diagnostics,
            execution_evidence,
        )
    return appended


def _foreground_append_result(
    result: object,
    *,
    execution_evidence: WorkflowExecutionEvidence | None = None,
    reconciliation_evidence: WorkflowReconciliationEvidence | None = None,
) -> WorkflowForegroundActionResult:
    from .repository import WorkflowEventAppendResult

    if type(result) is not WorkflowEventAppendResult:
        raise TypeError("result must be WorkflowEventAppendResult")
    status = {
        WorkflowEventAppendStatus.APPENDED: (WorkflowForegroundActionStatus.RECORDED),
        WorkflowEventAppendStatus.IDEMPOTENT: (
            WorkflowForegroundActionStatus.IDEMPOTENT
        ),
        WorkflowEventAppendStatus.CONFLICT: (WorkflowForegroundActionStatus.CONFLICT),
        WorkflowEventAppendStatus.INDETERMINATE: (
            WorkflowForegroundActionStatus.INDETERMINATE
        ),
        WorkflowEventAppendStatus.ERROR: WorkflowForegroundActionStatus.ERROR,
    }[result.status]
    event = (
        result.event
        if result.status
        in {
            WorkflowEventAppendStatus.APPENDED,
            WorkflowEventAppendStatus.IDEMPOTENT,
        }
        else None
    )
    return WorkflowForegroundActionResult(
        status,
        event,
        result.diagnostics,
        execution_evidence,
        reconciliation_evidence,
    )


def _foreground_load_failure(
    status: WorkflowHistoryLoadStatus,
    diagnostics: tuple[str, ...],
) -> WorkflowForegroundActionResult:
    mapped = {
        WorkflowHistoryLoadStatus.ABSENT: (WorkflowForegroundActionStatus.CONFLICT),
        WorkflowHistoryLoadStatus.INCOMPATIBLE: (WorkflowForegroundActionStatus.ERROR),
        WorkflowHistoryLoadStatus.CORRUPT: (WorkflowForegroundActionStatus.ERROR),
        WorkflowHistoryLoadStatus.INDETERMINATE: (
            WorkflowForegroundActionStatus.INDETERMINATE
        ),
        WorkflowHistoryLoadStatus.ERROR: WorkflowForegroundActionStatus.ERROR,
    }
    if status is WorkflowHistoryLoadStatus.LOADED:
        raise ValueError("loaded is not a failure")
    return WorkflowForegroundActionResult(
        mapped[status],
        None,
        diagnostics or ("runtime_history_unavailable",),
    )


def _append_result(
    result: object,
    *,
    validation: WorkflowValidationResult | None = None,
    transition: WorkflowTransitionExecution | None = None,
) -> WorkflowRuntimeActionResult:
    from .repository import WorkflowEventAppendResult

    if type(result) is not WorkflowEventAppendResult:
        raise TypeError("result must be WorkflowEventAppendResult")
    status = {
        WorkflowEventAppendStatus.APPENDED: (WorkflowRuntimeActionStatus.RECORDED),
        WorkflowEventAppendStatus.IDEMPOTENT: (WorkflowRuntimeActionStatus.IDEMPOTENT),
        WorkflowEventAppendStatus.CONFLICT: (WorkflowRuntimeActionStatus.CONFLICT),
        WorkflowEventAppendStatus.INDETERMINATE: (
            WorkflowRuntimeActionStatus.INDETERMINATE
        ),
        WorkflowEventAppendStatus.ERROR: WorkflowRuntimeActionStatus.ERROR,
    }[result.status]
    event = (
        result.event
        if result.status
        in {
            WorkflowEventAppendStatus.APPENDED,
            WorkflowEventAppendStatus.IDEMPOTENT,
        }
        else None
    )
    return WorkflowRuntimeActionResult(
        status,
        event,
        result.diagnostics,
        validation,
        transition,
    )


def _load_failure_result(
    status: WorkflowHistoryLoadStatus,
    diagnostics: tuple[str, ...],
) -> WorkflowRuntimeActionResult:
    mapped = {
        WorkflowHistoryLoadStatus.ABSENT: WorkflowRuntimeActionStatus.CONFLICT,
        WorkflowHistoryLoadStatus.INCOMPATIBLE: (WorkflowRuntimeActionStatus.ERROR),
        WorkflowHistoryLoadStatus.CORRUPT: WorkflowRuntimeActionStatus.ERROR,
        WorkflowHistoryLoadStatus.INDETERMINATE: (
            WorkflowRuntimeActionStatus.INDETERMINATE
        ),
        WorkflowHistoryLoadStatus.ERROR: WorkflowRuntimeActionStatus.ERROR,
    }
    if status is WorkflowHistoryLoadStatus.LOADED:
        raise ValueError("loaded is not a failure")
    return WorkflowRuntimeActionResult(
        mapped[status],
        None,
        diagnostics or ("runtime_history_unavailable",),
    )
