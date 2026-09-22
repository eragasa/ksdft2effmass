"""Effect-free preparation of simulation-dispatch observation ingress."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
from typing import final

from ..runs.aggregate import WorkflowRun
from ..runs.identities import WorkflowRunRevisionIdentity
from ..runs.records import (
    DispatchOutcomeKind,
    DispatchOutcomeRecord,
    NativeOutputAdmission,
    ObligationDisposition,
    ObligationDispositionKind,
    ResultObjectReference,
    ResultProductionRecord,
    TaskAttempt,
    TaskAttemptStatus,
    TaskFailureRecord,
    TaskInvocationOutcome,
    TaskInvocationOutcomeKind,
    TaskWorkflowTransitionRecord,
)
from ..runs.replay import (
    WorkflowRunReplayer,
    WorkflowRunReplayOutcomeKind,
    WorkflowRunReplayResult,
    WorkflowRuntimeBundle,
)
from .reconciliation import (
    SimulationDispatchReconciliationOutcomeKind,
    SimulationDispatchReconciliationResult,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationDispatchResultIngressRequest:
    """Request one replay-verified dispatch-observation WorkflowRun candidate.

    The caller supplies exact immutable records derived from one reconciliation. The
    preparer validates the closed variant, appends the records atomically to an
    immutable candidate, and requires deterministic replay equality. It performs no
    repository operation, native-file access, or external effect.
    """

    predecessor_run: WorkflowRun
    runtime_bundle: WorkflowRuntimeBundle
    reconciliation_result: SimulationDispatchReconciliationResult
    next_revision_identity: WorkflowRunRevisionIdentity
    terminal_attempt: TaskAttempt | None
    invocation_outcome: TaskInvocationOutcome | None
    dispatch_outcome: DispatchOutcomeRecord | None
    obligation_dispositions: tuple[ObligationDisposition, ...]
    result_references: tuple[ResultObjectReference, ...]
    result_productions: tuple[ResultProductionRecord, ...]
    native_output_admissions: tuple[NativeOutputAdmission, ...]
    failures: tuple[TaskFailureRecord, ...]
    transition: TaskWorkflowTransitionRecord | None

    def __post_init__(self) -> None:
        """Validate exact inputs and canonical supplied record collections."""
        expected = (
            (self.predecessor_run, WorkflowRun, "predecessor_run"),
            (self.runtime_bundle, WorkflowRuntimeBundle, "runtime_bundle"),
            (
                self.reconciliation_result,
                SimulationDispatchReconciliationResult,
                "reconciliation_result",
            ),
            (
                self.next_revision_identity,
                WorkflowRunRevisionIdentity,
                "next_revision_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if (
            self.terminal_attempt is not None
            and type(self.terminal_attempt) is not TaskAttempt
        ):
            raise TypeError("terminal_attempt must be TaskAttempt or None")
        if (
            self.invocation_outcome is not None
            and type(self.invocation_outcome) is not TaskInvocationOutcome
        ):
            raise TypeError("invocation_outcome must be TaskInvocationOutcome or None")
        if (
            self.dispatch_outcome is not None
            and type(self.dispatch_outcome) is not DispatchOutcomeRecord
        ):
            raise TypeError("dispatch_outcome must be DispatchOutcomeRecord or None")
        collections = (
            (
                self.obligation_dispositions,
                ObligationDisposition,
                "obligation_dispositions",
            ),
            (self.result_references, ResultObjectReference, "result_references"),
            (self.result_productions, ResultProductionRecord, "result_productions"),
            (
                self.native_output_admissions,
                NativeOutputAdmission,
                "native_output_admissions",
            ),
            (self.failures, TaskFailureRecord, "failures"),
        )
        for values, member_type, name in collections:
            if type(values) is not tuple or any(
                type(value) is not member_type for value in values
            ):
                raise TypeError(f"{name} must be a tuple of {member_type.__name__}")
            if values != tuple(
                sorted(values, key=lambda value: value.identity.value)
            ) or len({value.identity for value in values}) != len(values):
                raise ValueError(f"{name} must be unique and lexically sorted")
        if self.transition is not None and type(self.transition) is not (
            TaskWorkflowTransitionRecord
        ):
            raise TypeError("transition must be TaskWorkflowTransitionRecord or None")


class SimulationDispatchResultIngressOutcomeKind(StrEnum):
    """Closed outcomes of dispatch-observation ingress preparation."""

    ADMITTED = "admitted"
    ERROR = "error"


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationDispatchResultIngressResult:
    """Record one replay-verified observation candidate or fail-closed error."""

    kind: SimulationDispatchResultIngressOutcomeKind
    request: SimulationDispatchResultIngressRequest
    predecessor_replay_result: WorkflowRunReplayResult
    candidate_run: WorkflowRun | None
    candidate_replay_result: WorkflowRunReplayResult | None
    diagnostics: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate exact result types, correlations, and variants."""
        if type(self.kind) is not SimulationDispatchResultIngressOutcomeKind:
            raise TypeError("kind must be SimulationDispatchResultIngressOutcomeKind")
        if type(self.request) is not SimulationDispatchResultIngressRequest:
            raise TypeError("request must be SimulationDispatchResultIngressRequest")
        if type(self.predecessor_replay_result) is not WorkflowRunReplayResult:
            raise TypeError("predecessor_replay_result must be WorkflowRunReplayResult")
        if (
            self.candidate_run is not None
            and type(self.candidate_run) is not WorkflowRun
        ):
            raise TypeError("candidate_run must be WorkflowRun or None")
        if (
            self.candidate_replay_result is not None
            and type(self.candidate_replay_result) is not WorkflowRunReplayResult
        ):
            raise TypeError(
                "candidate_replay_result must be WorkflowRunReplayResult or None"
            )
        if type(self.diagnostics) is not tuple or any(
            type(value) is not str for value in self.diagnostics
        ):
            raise TypeError("diagnostics must be a tuple of strings")
        if any(not value for value in self.diagnostics) or len(
            set(self.diagnostics)
        ) != len(self.diagnostics):
            raise ValueError("diagnostics must be nonempty when present and unique")
        predecessor = self.request.predecessor_run
        if (
            self.predecessor_replay_result.workflow_run_identity != predecessor.identity
            or self.predecessor_replay_result.revision_identity
            != predecessor.revision_identity
            or self.predecessor_replay_result.runtime_bundle_identity
            != self.request.runtime_bundle.identity
        ):
            raise ValueError(
                "predecessor replay result must identify the requested predecessor"
            )
        if self.candidate_replay_result is not None and (
            self.candidate_replay_result.workflow_run_identity != predecessor.identity
            or self.candidate_replay_result.revision_identity
            != self.request.next_revision_identity
            or self.candidate_replay_result.runtime_bundle_identity
            != self.request.runtime_bundle.identity
        ):
            raise ValueError(
                "candidate replay result must identify the requested successor"
            )
        if self.kind is SimulationDispatchResultIngressOutcomeKind.ADMITTED:
            if (
                self.predecessor_replay_result.outcome
                is not WorkflowRunReplayOutcomeKind.EQUAL
                or self.candidate_run is None
                or self.candidate_replay_result is None
                or self.candidate_replay_result.outcome
                is not WorkflowRunReplayOutcomeKind.EQUAL
                or self.candidate_run.identity != self.request.predecessor_run.identity
                or self.candidate_run.revision_identity
                != self.request.next_revision_identity
                or self.diagnostics
            ):
                raise ValueError(
                    "admitted result requires one correlated candidate and two "
                    "equal replays"
                )
        elif (
            self.candidate_run is not None
            or self.candidate_replay_result is not None
            or not self.diagnostics
        ):
            raise ValueError(
                "error result prohibits candidate state and requires diagnostics"
            )


@dataclass(frozen=True, slots=True)
@final
class SimulationDispatchResultIngressPreparer:
    """Construct dispatch-observation candidates without persistence or effects."""

    replayer: WorkflowRunReplayer

    def __post_init__(self) -> None:
        """Validate the exact deterministic replayer."""
        if type(self.replayer) is not WorkflowRunReplayer:
            raise TypeError("replayer must be WorkflowRunReplayer")

    def execute(
        self, request: SimulationDispatchResultIngressRequest
    ) -> SimulationDispatchResultIngressResult:
        """Validate, append, and replay one observation and optional final group."""
        if type(request) is not SimulationDispatchResultIngressRequest:
            raise TypeError("request must be SimulationDispatchResultIngressRequest")
        predecessor_replay = self.replayer.execute(
            request.predecessor_run, request.runtime_bundle
        )
        if predecessor_replay.outcome is not WorkflowRunReplayOutcomeKind.EQUAL:
            return self._error(
                request,
                predecessor_replay,
                "dispatch-ingress predecessor is not replay-equal",
            )
        issue = self._precondition_issue(request)
        if issue is not None:
            return self._error(request, predecessor_replay, issue)
        run = request.predecessor_run
        transition = request.transition
        current_marking = (
            run.current_marking
            if transition is None
            else transition.firing_result.successor_marking
        )
        assert current_marking is not None
        try:
            candidate = replace(
                run,
                revision_identity=request.next_revision_identity,
                predecessor_revision_identity=run.revision_identity,
                attempts=run.attempts
                + (
                    ()
                    if request.terminal_attempt is None
                    else (request.terminal_attempt,)
                ),
                outcomes=tuple(
                    sorted(
                        run.outcomes
                        + (
                            ()
                            if request.invocation_outcome is None
                            else (request.invocation_outcome,)
                        ),
                        key=lambda value: value.identity.value,
                    )
                ),
                result_references=tuple(
                    sorted(
                        run.result_references + request.result_references,
                        key=lambda value: value.identity.value,
                    )
                ),
                result_productions=tuple(
                    sorted(
                        run.result_productions + request.result_productions,
                        key=lambda value: value.identity.value,
                    )
                ),
                native_output_admissions=tuple(
                    sorted(
                        run.native_output_admissions + request.native_output_admissions,
                        key=lambda value: value.identity.value,
                    )
                ),
                failures=tuple(
                    sorted(
                        run.failures + request.failures,
                        key=lambda value: value.identity.value,
                    )
                ),
                dispatch_observations=tuple(
                    sorted(
                        run.dispatch_observations
                        + (request.reconciliation_result.observation_record,),
                        key=lambda value: value.identity.value,
                    )
                ),
                dispatch_outcomes=tuple(
                    sorted(
                        run.dispatch_outcomes
                        + (
                            ()
                            if request.dispatch_outcome is None
                            else (request.dispatch_outcome,)
                        ),
                        key=lambda value: value.identity.value,
                    )
                ),
                obligation_dispositions=tuple(
                    sorted(
                        run.obligation_dispositions + request.obligation_dispositions,
                        key=lambda value: value.identity.value,
                    )
                ),
                current_marking=current_marking,
                transitions=(
                    run.transitions
                    if transition is None
                    else run.transitions + (transition,)
                ),
            )
        except ValueError:
            return self._error(
                request,
                predecessor_replay,
                "observation candidate construction rejected inconsistent records",
            )
        candidate_replay = self.replayer.execute(candidate, request.runtime_bundle)
        if candidate_replay.outcome is not WorkflowRunReplayOutcomeKind.EQUAL:
            return self._error(
                request,
                predecessor_replay,
                "observation candidate is not replay-equal",
            )
        return SimulationDispatchResultIngressResult(
            kind=SimulationDispatchResultIngressOutcomeKind.ADMITTED,
            request=request,
            predecessor_replay_result=predecessor_replay,
            candidate_run=candidate,
            candidate_replay_result=candidate_replay,
            diagnostics=(),
        )

    @staticmethod
    def _precondition_issue(
        request: SimulationDispatchResultIngressRequest,
    ) -> str | None:
        """Return the first deterministic observation or terminal-group mismatch."""
        run = request.predecessor_run
        reconciliation = request.reconciliation_result
        runtime_outcome = reconciliation.outcome
        observation = reconciliation.observation_record
        if request.next_revision_identity == run.revision_identity:
            return "candidate revision must differ from predecessor revision"
        if observation.identity in {
            value.identity for value in run.dispatch_observations
        }:
            return "dispatch observation identity already exists"
        dispatch_request = reconciliation.request.dispatch_request
        claim_receipt = dispatch_request.claim_commit_receipt
        entry_receipt = reconciliation.request.dispatch_entry_receipt
        if (
            dispatch_request.claimed_reservation not in run.authority_reservations
            or dispatch_request.claim_authorization_request.result_identity
            not in {value.identity for value in run.authorization_results}
            or claim_receipt.claimed_reservation_identity
            != dispatch_request.claimed_reservation.identity
            or entry_receipt.claim_commit_receipt_identity != claim_receipt.identity
            or entry_receipt.claimed_reservation_identity
            != dispatch_request.claimed_reservation.identity
        ):
            return "reconciliation does not belong to the committed dispatch entry"
        correlation = dispatch_request.execution_request.correlation
        matching_entries = tuple(
            value
            for value in run.dispatch_entries
            if value.identity == entry_receipt.dispatch_entry_identity
        )
        if len(matching_entries) != 1:
            return "dispatch-entry state is absent from the predecessor"
        entry = matching_entries[0]
        if (
            entry.workflow_run_identity != run.identity
            or entry.predecessor_revision_identity
            != entry_receipt.predecessor_revision_identity
            or entry.committed_revision_identity
            != entry_receipt.committed_revision_identity
            or entry.claimed_reservation_identity
            != entry_receipt.claimed_reservation_identity
            or entry.request_identity != correlation.request_identity
            or entry.obligation_identity != entry_receipt.obligation_identity
            or entry.receipt_identity != entry_receipt.identity
            or entry.outcome_identity != entry_receipt.outcome_identity
        ):
            return "dispatch-entry state does not match its receipt"
        prior_observations = tuple(
            value
            for value in run.dispatch_observations
            if value.obligation_identity == entry.obligation_identity
        )
        if (
            not prior_observations
            and run.revision_identity != entry.committed_revision_identity
        ):
            return "first observation must succeed the dispatch-entered revision"
        finalizable = reconciliation.kind in {
            SimulationDispatchReconciliationOutcomeKind.CONFIRMED,
            SimulationDispatchReconciliationOutcomeKind.REJECTED,
        }
        if finalizable and any(
            value.obligation_identity == observation.obligation_identity
            for value in run.dispatch_outcomes
        ):
            return "dispatch obligation already has a final outcome"
        terminal_records = (
            request.terminal_attempt,
            request.invocation_outcome,
            request.dispatch_outcome,
        )
        if not finalizable:
            if (
                runtime_outcome is not None
                or any(value is not None for value in terminal_records)
                or request.obligation_dispositions
                or request.result_references
                or request.result_productions
                or request.native_output_admissions
                or request.failures
                or request.transition is not None
            ):
                return "nonfinal observation prohibits terminal record state"
            return None
        if runtime_outcome is None or any(value is None for value in terminal_records):
            return "final reconciliation requires one complete terminal record group"
        dispatch = request.dispatch_outcome
        invocation = request.invocation_outcome
        attempt = request.terminal_attempt
        assert dispatch is not None and invocation is not None and attempt is not None
        expected_status = {
            DispatchOutcomeKind.CONFIRMED: TaskAttemptStatus.CONFIRMED,
            DispatchOutcomeKind.REJECTED: TaskAttemptStatus.REJECTED,
        }[runtime_outcome.kind]
        expected_invocation_kind = {
            DispatchOutcomeKind.CONFIRMED: TaskInvocationOutcomeKind.CONFIRMED,
            DispatchOutcomeKind.REJECTED: TaskInvocationOutcomeKind.REJECTED,
        }[runtime_outcome.kind]
        if (
            dispatch.envelope_identity != runtime_outcome.observation_identity
            or dispatch.kind is not runtime_outcome.kind
            or dispatch.workflow_run_identity != run.identity
            or dispatch.request_identity != runtime_outcome.request_identity
            or dispatch.task_instance_identity != runtime_outcome.task_instance_identity
            or dispatch.activation_identity != runtime_outcome.activation_identity
            or dispatch.operation_identity != runtime_outcome.operation_identity
            or dispatch.attempt_identity != runtime_outcome.attempt_identity
            or dispatch.executor_identity != runtime_outcome.executor_identity
            or dispatch.obligation_identity != runtime_outcome.obligation_identity
            or dispatch.grant_identity != runtime_outcome.grant_identity
            or invocation.workflow_run_identity != run.identity
            or invocation.activation_identity != correlation.activation_identity
            or invocation.operation_identity != correlation.operation_identity
            or invocation.attempt_identity != correlation.attempt_identity
            or invocation.dispatch_outcome_record_identity != dispatch.identity
            or invocation.kind is not expected_invocation_kind
            or attempt.workflow_run_identity != run.identity
            or attempt.task_instance_identity != correlation.task_instance_identity
            or attempt.activation_identity != correlation.activation_identity
            or attempt.operation_identity != correlation.operation_identity
            or attempt.attempt_identity != correlation.attempt_identity
            or attempt.status is not expected_status
            or invocation.terminal_attempt_record_identity != attempt.identity
        ):
            return "terminal records do not match the reconciled dispatch"
        started = tuple(
            value
            for value in run.attempts
            if value.attempt_identity == correlation.attempt_identity
            and value.status is TaskAttemptStatus.STARTED
        )
        if (
            len(started) != 1
            or attempt.predecessor_attempt_record_identity != started[0].identity
        ):
            return "terminal attempt must append after its exact started record"
        disposition_kinds = tuple(
            value.kind for value in request.obligation_dispositions
        )
        if runtime_outcome.kind is DispatchOutcomeKind.CONFIRMED:
            reference = (
                request.result_references[0]
                if len(request.result_references) == 1
                else None
            )
            production = (
                request.result_productions[0]
                if len(request.result_productions) == 1
                else None
            )
            admission = (
                request.native_output_admissions[0]
                if len(request.native_output_admissions) == 1
                else None
            )
            valid_shape = (
                reference is not None
                and production is not None
                and admission is not None
                and runtime_outcome.result is not None
                and reference.result == runtime_outcome.result
                and dispatch.result_reference_identity == reference.identity
                and production.result_reference_identity == reference.identity
                and admission.dispatch_outcome_record_identity == dispatch.identity
                and admission.dispatch_envelope_identity
                == runtime_outcome.observation_identity
                and admission.production_record_identity == production.identity
                and admission.result_reference_identity == reference.identity
                and admission.manifest_identity
                == runtime_outcome.native_output_manifest_identity
                and admission.manifest_entry_identities
                == runtime_outcome.native_output_manifest_entry_identities
                and not request.failures
                and request.transition is not None
                and disposition_kinds == (ObligationDispositionKind.CONFIRMED,)
            )
        else:
            failure = request.failures[0] if len(request.failures) == 1 else None
            valid_shape = (
                not request.result_references
                and not request.result_productions
                and not request.native_output_admissions
                and failure is not None
                and runtime_outcome.failure is not None
                and failure.failure == runtime_outcome.failure
                and dispatch.failure_record_identity == failure.identity
                and request.transition is None
                and disposition_kinds == (ObligationDispositionKind.REJECTED,)
            )
        if not valid_shape:
            return "terminal record group does not match the dispatch outcome variant"
        return None

    @staticmethod
    def _error(
        request: SimulationDispatchResultIngressRequest,
        predecessor_replay: WorkflowRunReplayResult,
        diagnostic: str,
    ) -> SimulationDispatchResultIngressResult:
        """Construct one fail-closed ingress-preparation error."""
        return SimulationDispatchResultIngressResult(
            kind=SimulationDispatchResultIngressOutcomeKind.ERROR,
            request=request,
            predecessor_replay_result=predecessor_replay,
            candidate_run=None,
            candidate_replay_result=None,
            diagnostics=(diagnostic,),
        )
