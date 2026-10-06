"""Software verification for bounded foreground workflow dispatch."""

from __future__ import annotations

from pathlib import Path
from typing import cast

import pytest
from _runtime_fixtures import (
    LocalWorkflowRuntimeHarness,
    runtime_fixture,
    transition_input,
)

from ksdft2effmass.workflows.v2.core import (
    WorkflowAdapterIdentity,
    WorkflowTransitionPreflightInput,
)
from ksdft2effmass.workflows.v2.persistence import SQLiteAtomicRevisionStore
from ksdft2effmass.workflows.v2.runtime import (
    AbstractWorkflowEffectReconciler,
    AbstractWorkflowForegroundWorker,
    WorkflowAdapterConfigurationIdentity,
    WorkflowAttemptIdentity,
    WorkflowAuthorityVerification,
    WorkflowAuthorityVerificationKind,
    WorkflowDispatchAuthorization,
    WorkflowEffectCapability,
    WorkflowEffectIntent,
    WorkflowEffectOutcomeKind,
    WorkflowEffectReconcilerIdentity,
    WorkflowEventAppendResult,
    WorkflowExecutionEvidence,
    WorkflowForegroundActionStatus,
    WorkflowForegroundExecutionRequest,
    WorkflowForegroundPlan,
    WorkflowForegroundWorkerIdentity,
    WorkflowReconciliationEvidence,
    WorkflowReconciliationOutcomeKind,
    WorkflowReconciliationRequest,
    WorkflowRuntimeEvent,
    WorkflowRuntimeEventIdentity,
    WorkflowRuntimeEventKind,
    WorkflowRuntimeEvidenceReference,
    WorkflowRuntimeRepository,
)


class TestLocalWorkflowForegroundRuntime:
    """Exercise retained authorization and ambiguity boundaries."""

    class Worker(AbstractWorkflowForegroundWorker):
        """Synthetic worker with one selected bounded outcome."""

        def __init__(
            self,
            outcome: WorkflowEffectOutcomeKind,
            *,
            evidence_references: tuple[WorkflowRuntimeEvidenceReference, ...] = (),
        ) -> None:
            self._outcome = outcome
            self._evidence_references = evidence_references
            self.calls = 0

        @property
        def identity(self) -> WorkflowForegroundWorkerIdentity:
            return WorkflowForegroundWorkerIdentity("synthetic-worker:1")

        def execute(
            self, *, request: WorkflowForegroundExecutionRequest
        ) -> WorkflowExecutionEvidence:
            self.calls += 1
            evidence = (
                WorkflowRuntimeEvidenceReference(
                    "synthetic-receipt", f"receipt:{self.calls}"
                ),
                *self._evidence_references,
            )
            return WorkflowExecutionEvidence.create(
                request=request,
                outcome=self._outcome,
                evidence_references=tuple(
                    sorted(
                        evidence,
                        key=lambda value: (
                            value.reference_kind,
                            value.reference_identity,
                        ),
                    )
                ),
                reason_codes=("synthetic_worker_report",),
            )

    class RaisingWorker(AbstractWorkflowForegroundWorker):
        """Synthetic worker whose exception leaves effect status unknown."""

        def __init__(self) -> None:
            self.calls = 0

        @property
        def identity(self) -> WorkflowForegroundWorkerIdentity:
            return WorkflowForegroundWorkerIdentity("synthetic-worker:1")

        def execute(
            self, *, request: WorkflowForegroundExecutionRequest
        ) -> WorkflowExecutionEvidence:
            self.calls += 1
            raise RuntimeError("private worker detail must not be retained")

    class IdentityTrackingWorker(AbstractWorkflowForegroundWorker):
        """Worker proving identity is not read before runtime correlation."""

        def __init__(self) -> None:
            self.identity_reads = 0
            self.calls = 0

        @property
        def identity(self) -> WorkflowForegroundWorkerIdentity:
            self.identity_reads += 1
            return WorkflowForegroundWorkerIdentity("synthetic-worker:1")

        def execute(
            self, *, request: WorkflowForegroundExecutionRequest
        ) -> WorkflowExecutionEvidence:
            self.calls += 1
            raise AssertionError("uncorrelated worker must not execute")

    class MalformedWorker(AbstractWorkflowForegroundWorker):
        """Synthetic worker returning an invalid application boundary value."""

        @property
        def identity(self) -> WorkflowForegroundWorkerIdentity:
            return WorkflowForegroundWorkerIdentity("synthetic-worker:1")

        def execute(
            self, *, request: WorkflowForegroundExecutionRequest
        ) -> WorkflowExecutionEvidence:
            return cast(WorkflowExecutionEvidence, "invalid-worker-report")

    class Reconciler(AbstractWorkflowEffectReconciler):
        """Synthetic query-only reconciler."""

        def __init__(self, outcome: WorkflowReconciliationOutcomeKind) -> None:
            self._outcome = outcome
            self.calls = 0

        @property
        def identity(self) -> WorkflowEffectReconcilerIdentity:
            return WorkflowEffectReconcilerIdentity("synthetic-reconciler:1")

        def reconcile(
            self, *, request: WorkflowReconciliationRequest
        ) -> WorkflowReconciliationEvidence:
            self.calls += 1
            return WorkflowReconciliationEvidence.create(
                request=request,
                reconciler_identity=self.identity,
                outcome=self._outcome,
                evidence_references=(
                    WorkflowRuntimeEvidenceReference(
                        "synthetic-query", f"query:{self.calls}"
                    ),
                ),
                reason_codes=("synthetic_reconciliation",),
            )

    class MalformedReconciler(AbstractWorkflowEffectReconciler):
        """Synthetic reconciler returning an invalid boundary value."""

        @property
        def identity(self) -> WorkflowEffectReconcilerIdentity:
            return WorkflowEffectReconcilerIdentity("synthetic-reconciler:1")

        def reconcile(
            self, *, request: WorkflowReconciliationRequest
        ) -> WorkflowReconciliationEvidence:
            return cast(
                WorkflowReconciliationEvidence,
                "invalid-reconciliation-report",
            )

    @staticmethod
    def prepared(
        tmp_path: Path,
        *,
        effect_count: int = 1,
        maximum_attempts_per_intent: int = 2,
    ) -> tuple[
        LocalWorkflowRuntimeHarness,
        WorkflowRuntimeRepository,
        WorkflowTransitionPreflightInput,
        WorkflowForegroundPlan,
    ]:
        repository = WorkflowRuntimeRepository(
            SQLiteAtomicRevisionStore(tmp_path / "private" / "foreground.sqlite3")
        )
        runtime = LocalWorkflowRuntimeHarness(repository)
        fixture = runtime_fixture()
        candidate = transition_input(fixture)
        preflight = WorkflowTransitionPreflightInput(
            candidate.definition,
            candidate.run,
            candidate.prior_state,
            candidate.request,
        )
        runtime.start(fixture.started)
        retained = runtime.retain_request(preflight)
        assert retained.event is not None
        assert retained.event.occurrence_identity is not None
        occurrence = retained.event.occurrence_identity
        adapter_identity = WorkflowAdapterIdentity("synthetic-adapter")
        adapter_configuration_identity = WorkflowAdapterConfigurationIdentity(
            "synthetic-adapter-configuration:1"
        )
        intents = tuple(
            WorkflowEffectIntent.create(
                occurrence_identity=occurrence,
                ordinal=ordinal,
                operation_kind=f"synthetic-effect-{ordinal}",
                adapter_identity=adapter_identity,
                adapter_configuration_identity=adapter_configuration_identity,
                input_references=(
                    WorkflowRuntimeEvidenceReference(
                        "synthetic-input", f"input:fixture:{ordinal}"
                    ),
                ),
                expected_output_contract="synthetic-output:1",
                capability=(WorkflowEffectCapability.IDEMPOTENT_EXECUTION_AND_LOOKUP),
            )
            for ordinal in range(effect_count)
        )
        plan = WorkflowForegroundPlan.create(
            occurrence_identity=occurrence,
            definition_identity=preflight.definition.identity,
            adapter_identity=adapter_identity,
            adapter_configuration_identity=adapter_configuration_identity,
            effect_intents=intents,
            maximum_attempts_per_intent=maximum_attempts_per_intent,
        )
        planned = runtime.record_plan(preflight, plan)
        assert planned.status is WorkflowForegroundActionStatus.RECORDED
        return runtime, repository, preflight, plan

    @staticmethod
    def execution_request(
        preflight: WorkflowTransitionPreflightInput,
        plan: WorkflowForegroundPlan,
        *,
        effect_ordinal: int = 0,
        attempt_ordinal: int = 1,
    ) -> tuple[
        WorkflowForegroundExecutionRequest,
        WorkflowAuthorityVerification,
    ]:
        intent = plan.effect_intents[effect_ordinal]
        attempt_identity = WorkflowAttemptIdentity.create(
            occurrence_identity=plan.occurrence_identity,
            effect_intent_identity=intent.identity,
            attempt_ordinal=attempt_ordinal,
        )
        verification = WorkflowAuthorityVerification.create(
            occurrence_identity=plan.occurrence_identity,
            plan_identity=plan.identity,
            effect_intent_identity=intent.identity,
            attempt_identity=attempt_identity,
            authority_reference_identity=(
                preflight.request.authority_reference.identity
            ),
            authority_version=(preflight.request.authority_reference.authority_version),
            policy_decision_identity=(f"policy-decision:attempt-{attempt_ordinal}"),
            validity_observation_identity=(
                f"validity-observation:attempt-{attempt_ordinal}"
            ),
            kind=WorkflowAuthorityVerificationKind.ACCEPTED,
            reason_codes=("authorized",),
        )
        authorization = WorkflowDispatchAuthorization.create(
            plan=plan,
            effect_intent=intent,
            attempt_ordinal=attempt_ordinal,
            worker_identity=WorkflowForegroundWorkerIdentity("synthetic-worker:1"),
            authority_verification=verification,
            limit_references=(
                WorkflowRuntimeEvidenceReference("synthetic-limit", "limit:one-call"),
            ),
        )
        return (
            WorkflowForegroundExecutionRequest(
                plan,
                intent,
                attempt_ordinal,
                authorization,
            ),
            verification,
        )

    def test__dispatch__retains_authorization_before_success(
        self, tmp_path: Path
    ) -> None:
        runtime, repository, preflight, plan = self.prepared(tmp_path)
        request, verification = self.execution_request(preflight, plan)
        worker = self.Worker(WorkflowEffectOutcomeKind.SUCCEEDED)

        result = runtime.dispatch_foreground(preflight, request, verification, worker)
        loaded = repository.load(preflight.run.identity.value)

        assert result.status is WorkflowForegroundActionStatus.RECORDED
        assert result.execution_evidence is not None
        assert worker.calls == 1
        assert loaded.history is not None
        assert tuple(event.kind for event in loaded.history.events)[-2:] == (
            WorkflowRuntimeEventKind.DISPATCH_AUTHORIZED,
            WorkflowRuntimeEventKind.EXECUTION_RECORDED,
        )

    def test__dispatch__rejects_different_same_run_preflight(
        self, tmp_path: Path
    ) -> None:
        runtime, _, preflight, plan = self.prepared(tmp_path)
        request, verification = self.execution_request(preflight, plan)
        fixture = runtime_fixture()
        other = transition_input(
            fixture,
            request_key="candidate:other",
            proposal_identity="proposal-set:sha256:other",
        )
        wrong_preflight = WorkflowTransitionPreflightInput(
            other.definition,
            other.run,
            other.prior_state,
            other.request,
        )
        worker = self.IdentityTrackingWorker()

        result = runtime.dispatch_foreground(
            wrong_preflight, request, verification, worker
        )

        assert result.status is WorkflowForegroundActionStatus.CONFLICT
        assert result.diagnostics == ("preflight_occurrence_mismatch",)
        assert worker.identity_reads == 0
        assert worker.calls == 0

    def test__authority_rejection__records_without_worker_call(
        self, tmp_path: Path
    ) -> None:
        runtime, repository, preflight, plan = self.prepared(tmp_path)
        intent = plan.effect_intents[0]
        rejection = WorkflowAuthorityVerification.create(
            occurrence_identity=plan.occurrence_identity,
            plan_identity=plan.identity,
            effect_intent_identity=intent.identity,
            attempt_identity=WorkflowAttemptIdentity.create(
                occurrence_identity=plan.occurrence_identity,
                effect_intent_identity=intent.identity,
                attempt_ordinal=1,
            ),
            authority_reference_identity=(
                preflight.request.authority_reference.identity
            ),
            authority_version=(preflight.request.authority_reference.authority_version),
            policy_decision_identity="policy-decision:rejected",
            validity_observation_identity="validity-observation:revoked",
            kind=WorkflowAuthorityVerificationKind.REJECTED,
            reason_codes=("authority_revoked",),
        )

        result = runtime.record_authority_rejection(preflight, plan, rejection)
        loaded = repository.load(preflight.run.identity.value)

        assert result.status is WorkflowForegroundActionStatus.REJECTED
        assert loaded.history is not None
        assert loaded.history.head.kind is (WorkflowRuntimeEventKind.AUTHORITY_REJECTED)

    def test__authority_rejection__cannot_erase_started_dispatch(
        self, tmp_path: Path
    ) -> None:
        runtime, _, preflight, plan = self.prepared(tmp_path)
        request, verification = self.execution_request(preflight, plan)
        dispatched = runtime.dispatch_foreground(
            preflight,
            request,
            verification,
            self.Worker(WorkflowEffectOutcomeKind.SUCCEEDED),
        )
        intent = plan.effect_intents[0]
        rejection = WorkflowAuthorityVerification.create(
            occurrence_identity=plan.occurrence_identity,
            plan_identity=plan.identity,
            effect_intent_identity=intent.identity,
            attempt_identity=WorkflowAttemptIdentity.create(
                occurrence_identity=plan.occurrence_identity,
                effect_intent_identity=intent.identity,
                attempt_ordinal=1,
            ),
            authority_reference_identity=(
                preflight.request.authority_reference.identity
            ),
            authority_version=(preflight.request.authority_reference.authority_version),
            policy_decision_identity="policy-decision:late-rejection",
            validity_observation_identity="validity-observation:late",
            kind=WorkflowAuthorityVerificationKind.REJECTED,
            reason_codes=("authority_revoked",),
        )

        result = runtime.record_authority_rejection(preflight, plan, rejection)

        assert dispatched.status is WorkflowForegroundActionStatus.RECORDED
        assert result.status is WorkflowForegroundActionStatus.CONFLICT
        assert result.diagnostics == ("authority_rejection_after_dispatch",)

    def test__dispatch__malformed_worker_report_becomes_ambiguity(
        self, tmp_path: Path
    ) -> None:
        runtime, _, preflight, plan = self.prepared(tmp_path)
        request, verification = self.execution_request(preflight, plan)

        result = runtime.dispatch_foreground(
            preflight,
            request,
            verification,
            self.MalformedWorker(),
        )

        assert result.status is (WorkflowForegroundActionStatus.RECONCILIATION_REQUIRED)
        assert result.execution_evidence is not None
        assert result.execution_evidence.reason_codes == ("worker_evidence_invalid",)

    def test__dispatch__append_race_after_worker_fails_indeterminate(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        runtime, repository, preflight, plan = self.prepared(tmp_path)
        request, verification = self.execution_request(preflight, plan)
        worker = self.Worker(WorkflowEffectOutcomeKind.SUCCEEDED)
        original_append = repository.append
        raced = False

        def append_with_race(
            event: WorkflowRuntimeEvent,
            *,
            expected_event_identity: WorkflowRuntimeEventIdentity | None,
            idempotency_identity: str,
        ) -> WorkflowEventAppendResult:
            nonlocal raced
            if event.kind is WorkflowRuntimeEventKind.EXECUTION_RECORDED and not raced:
                raced = True
                loaded = repository.load(preflight.run.identity.value)
                assert loaded.history is not None
                competing = WorkflowRuntimeEvent.create(
                    kind=WorkflowRuntimeEventKind.REQUEST_CONFLICT_RECORDED,
                    run_identity=preflight.run.identity,
                    ordinal=loaded.history.head.ordinal + 1,
                    predecessor_event_identity=loaded.history.head.identity,
                    core_revision=preflight.run.revision,
                    core_state_identity=preflight.prior_state.identity,
                    occurrence_identity=plan.occurrence_identity,
                    request_identity=preflight.request.identity,
                    operation_identity=preflight.request.operation_identity,
                    evidence_references=(
                        WorkflowRuntimeEvidenceReference(
                            "conflict-request", "synthetic-racing-request"
                        ),
                    ),
                    reason_codes=("synthetic_race",),
                )
                appended = original_append(
                    competing,
                    expected_event_identity=loaded.history.head.identity,
                    idempotency_identity="synthetic-racing-request",
                )
                assert appended.event == competing
            return original_append(
                event,
                expected_event_identity=expected_event_identity,
                idempotency_identity=idempotency_identity,
            )

        monkeypatch.setattr(repository, "append", append_with_race)

        result = runtime.dispatch_foreground(preflight, request, verification, worker)

        assert result.status is WorkflowForegroundActionStatus.INDETERMINATE
        assert "worker_evidence_not_retained" in result.diagnostics
        assert worker.calls == 1

        recovered = runtime.dispatch_foreground(
            preflight, request, verification, worker
        )

        assert recovered.status is (
            WorkflowForegroundActionStatus.RECONCILIATION_REQUIRED
        )
        assert recovered.execution_evidence is not None
        assert recovered.execution_evidence.outcome is (
            WorkflowEffectOutcomeKind.AMBIGUOUS
        )
        assert worker.calls == 1

    def test__dispatch__worker_exception_requires_reconciliation_and_no_retry(
        self, tmp_path: Path
    ) -> None:
        runtime, _, preflight, plan = self.prepared(tmp_path)
        request, verification = self.execution_request(preflight, plan)
        worker = self.RaisingWorker()

        first = runtime.dispatch_foreground(preflight, request, verification, worker)
        repeated = runtime.dispatch_foreground(preflight, request, verification, worker)

        assert first.status is (WorkflowForegroundActionStatus.RECONCILIATION_REQUIRED)
        assert first.execution_evidence is not None
        assert first.execution_evidence.outcome is (WorkflowEffectOutcomeKind.AMBIGUOUS)
        assert first.execution_evidence.reason_codes == ("worker_exception",)
        assert repeated.status is (
            WorkflowForegroundActionStatus.RECONCILIATION_REQUIRED
        )
        assert worker.calls == 1
        assert all(
            "private worker detail" not in diagnostic
            for diagnostic in first.diagnostics
        )

    def test__reconciliation__malformed_report_remains_unresolved(
        self, tmp_path: Path
    ) -> None:
        runtime, _, preflight, plan = self.prepared(tmp_path)
        request, verification = self.execution_request(preflight, plan)
        dispatched = runtime.dispatch_foreground(
            preflight, request, verification, self.RaisingWorker()
        )
        assert dispatched.execution_evidence is not None

        result = runtime.reconcile_foreground(
            preflight,
            WorkflowReconciliationRequest(request, dispatched.execution_evidence),
            self.MalformedReconciler(),
        )

        assert result.status is (WorkflowForegroundActionStatus.RECONCILIATION_REQUIRED)
        assert result.reconciliation_evidence is not None
        assert result.reconciliation_evidence.outcome is (
            WorkflowReconciliationOutcomeKind.EVIDENCE_INVALID
        )

    @pytest.mark.parametrize(
        "outcome",
        (
            WorkflowReconciliationOutcomeKind.STILL_AMBIGUOUS,
            WorkflowReconciliationOutcomeKind.CONFIRMED_PARTIAL,
            WorkflowReconciliationOutcomeKind.EVIDENCE_INVALID,
        ),
    )
    def test__reconciliation__unresolved_replay_remains_required(
        self,
        tmp_path: Path,
        outcome: WorkflowReconciliationOutcomeKind,
    ) -> None:
        runtime, _, preflight, plan = self.prepared(tmp_path)
        request, verification = self.execution_request(preflight, plan)
        dispatched = runtime.dispatch_foreground(
            preflight, request, verification, self.RaisingWorker()
        )
        assert dispatched.execution_evidence is not None
        reconciliation_request = WorkflowReconciliationRequest(
            request, dispatched.execution_evidence
        )
        reconciler = self.Reconciler(outcome)

        first = runtime.reconcile_foreground(
            preflight, reconciliation_request, reconciler
        )
        repeated = runtime.reconcile_foreground(
            preflight, reconciliation_request, reconciler
        )

        assert first.status is (WorkflowForegroundActionStatus.RECONCILIATION_REQUIRED)
        assert repeated.status is (
            WorkflowForegroundActionStatus.RECONCILIATION_REQUIRED
        )
        assert reconciler.calls == 1

    def test__reconciliation__confirmed_not_applied_permits_fresh_attempt(
        self, tmp_path: Path
    ) -> None:
        runtime, _, preflight, plan = self.prepared(tmp_path)
        first_request, first_verification = self.execution_request(preflight, plan)
        first_worker = self.RaisingWorker()
        first = runtime.dispatch_foreground(
            preflight,
            first_request,
            first_verification,
            first_worker,
        )
        assert first.execution_evidence is not None
        reconciliation_request = WorkflowReconciliationRequest(
            first_request, first.execution_evidence
        )
        reconciler = self.Reconciler(
            WorkflowReconciliationOutcomeKind.CONFIRMED_NOT_APPLIED
        )

        reconciled = runtime.reconcile_foreground(
            preflight, reconciliation_request, reconciler
        )
        second_request, second_verification = self.execution_request(
            preflight, plan, attempt_ordinal=2
        )
        second_worker = self.Worker(WorkflowEffectOutcomeKind.SUCCEEDED)
        second = runtime.dispatch_foreground(
            preflight,
            second_request,
            second_verification,
            second_worker,
        )

        assert reconciled.status is WorkflowForegroundActionStatus.RECORDED
        assert second.status is WorkflowForegroundActionStatus.RECORDED
        assert second_worker.calls == 1
        assert reconciler.calls == 1

    def test__dispatch_authorization__rejects_prior_attempt_verification(
        self, tmp_path: Path
    ) -> None:
        runtime, _, preflight, plan = self.prepared(tmp_path)
        first_request, first_verification = self.execution_request(preflight, plan)
        first = runtime.dispatch_foreground(
            preflight,
            first_request,
            first_verification,
            self.Worker(WorkflowEffectOutcomeKind.KNOWN_NOT_APPLIED),
        )

        assert first.status is WorkflowForegroundActionStatus.RECORDED
        with pytest.raises(
            ValueError,
            match="authority verification does not authorize this intent",
        ):
            WorkflowDispatchAuthorization.create(
                plan=plan,
                effect_intent=plan.effect_intents[0],
                attempt_ordinal=2,
                worker_identity=WorkflowForegroundWorkerIdentity("synthetic-worker:1"),
                authority_verification=first_verification,
                limit_references=(),
            )

    def test__record_plan__maximum_intents_fit_event_envelope(
        self, tmp_path: Path
    ) -> None:
        _, repository, preflight, plan = self.prepared(tmp_path, effect_count=251)
        loaded = repository.load(preflight.run.identity.value)

        assert len(plan.effect_intents) == 251
        assert loaded.history is not None
        assert loaded.history.head.kind is WorkflowRuntimeEventKind.PLAN_RECORDED
        assert len(loaded.history.head.evidence_references) == 256

    def test__dispatch__maximum_worker_evidence_fits_event_envelope(
        self, tmp_path: Path
    ) -> None:
        runtime, repository, preflight, plan = self.prepared(tmp_path)
        request, verification = self.execution_request(preflight, plan)
        extra = tuple(
            WorkflowRuntimeEvidenceReference(
                "synthetic-evidence", f"evidence:{ordinal:03d}"
            )
            for ordinal in range(250)
        )
        worker = self.Worker(
            WorkflowEffectOutcomeKind.SUCCEEDED,
            evidence_references=extra,
        )

        result = runtime.dispatch_foreground(preflight, request, verification, worker)
        loaded = repository.load(preflight.run.identity.value)

        assert result.status is WorkflowForegroundActionStatus.RECORDED
        assert loaded.history is not None
        assert len(loaded.history.head.evidence_references) == 256

    def test__worker_evidence__rejects_execution_outcome_reason_code(
        self, tmp_path: Path
    ) -> None:
        _, _, preflight, plan = self.prepared(tmp_path)
        request, _ = self.execution_request(preflight, plan)

        for reserved_code in (
            WorkflowEffectOutcomeKind.SUCCEEDED.value,
            WorkflowReconciliationOutcomeKind.CONFIRMED_APPLIED.value,
        ):
            with pytest.raises(
                ValueError,
                match="runtime-reserved outcome code",
            ):
                WorkflowExecutionEvidence.create(
                    request=request,
                    outcome=WorkflowEffectOutcomeKind.KNOWN_NOT_APPLIED,
                    evidence_references=(),
                    reason_codes=(reserved_code,),
                )

    def test__reconciliation_evidence__rejects_outcome_reason_code(
        self, tmp_path: Path
    ) -> None:
        runtime, _, preflight, plan = self.prepared(tmp_path)
        execution_request, verification = self.execution_request(preflight, plan)
        dispatched = runtime.dispatch_foreground(
            preflight,
            execution_request,
            verification,
            self.RaisingWorker(),
        )
        assert dispatched.execution_evidence is not None
        request = WorkflowReconciliationRequest(
            execution_request, dispatched.execution_evidence
        )

        for reserved_code in (
            WorkflowReconciliationOutcomeKind.CONFIRMED_APPLIED.value,
            WorkflowEffectOutcomeKind.SUCCEEDED.value,
        ):
            with pytest.raises(
                ValueError,
                match="runtime-reserved outcome code",
            ):
                WorkflowReconciliationEvidence.create(
                    request=request,
                    reconciler_identity=self.Reconciler(
                        WorkflowReconciliationOutcomeKind.STILL_AMBIGUOUS
                    ).identity,
                    outcome=(WorkflowReconciliationOutcomeKind.CONFIRMED_NOT_APPLIED),
                    evidence_references=(),
                    reason_codes=(reserved_code,),
                )

    def test__authority_evidence__rejects_outcome_reason_code(
        self, tmp_path: Path
    ) -> None:
        _, _, preflight, plan = self.prepared(tmp_path)
        _, verification = self.execution_request(preflight, plan)

        with pytest.raises(
            ValueError,
            match="runtime-reserved outcome code",
        ):
            WorkflowAuthorityVerification.create(
                occurrence_identity=verification.occurrence_identity,
                plan_identity=verification.plan_identity,
                effect_intent_identity=verification.effect_intent_identity,
                attempt_identity=verification.attempt_identity,
                authority_reference_identity=(
                    verification.authority_reference_identity
                ),
                authority_version=verification.authority_version,
                policy_decision_identity=(verification.policy_decision_identity),
                validity_observation_identity=(
                    verification.validity_observation_identity
                ),
                kind=verification.kind,
                reason_codes=(WorkflowEffectOutcomeKind.SUCCEEDED.value,),
            )

    def test__dispatch_replay__rejects_mixed_outcome_vocabularies(
        self, tmp_path: Path
    ) -> None:
        runtime, repository, preflight, plan = self.prepared(tmp_path)
        request, verification = self.execution_request(preflight, plan)
        loaded = repository.load(preflight.run.identity.value)
        assert loaded.history is not None
        authorization = request.authorization
        authorization_event = WorkflowRuntimeEvent.create(
            kind=WorkflowRuntimeEventKind.DISPATCH_AUTHORIZED,
            run_identity=preflight.run.identity,
            ordinal=loaded.history.head.ordinal + 1,
            predecessor_event_identity=loaded.history.head.identity,
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
                    "dispatch-authorization", authorization.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "effect-intent", request.effect_intent.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "foreground-plan", plan.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "workflow-attempt", authorization.attempt_identity.value
                ),
            ),
        )
        first_append = repository.append(
            authorization_event,
            expected_event_identity=loaded.history.head.identity,
            idempotency_identity="synthetic-mixed-authorization",
        )
        assert first_append.event == authorization_event
        execution_event = WorkflowRuntimeEvent.create(
            kind=WorkflowRuntimeEventKind.EXECUTION_RECORDED,
            run_identity=preflight.run.identity,
            ordinal=authorization_event.ordinal + 1,
            predecessor_event_identity=authorization_event.identity,
            core_revision=preflight.run.revision,
            core_state_identity=preflight.prior_state.identity,
            occurrence_identity=plan.occurrence_identity,
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
                    "execution-evidence", "synthetic-mixed-evidence"
                ),
                WorkflowRuntimeEvidenceReference(
                    "foreground-plan", plan.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "workflow-attempt", authorization.attempt_identity.value
                ),
            ),
            reason_codes=(
                WorkflowEffectOutcomeKind.SUCCEEDED.value,
                WorkflowReconciliationOutcomeKind.CONFIRMED_APPLIED.value,
            ),
        )
        second_append = repository.append(
            execution_event,
            expected_event_identity=authorization_event.identity,
            idempotency_identity="synthetic-mixed-execution",
        )
        assert second_append.event == execution_event
        worker = self.IdentityTrackingWorker()

        result = runtime.dispatch_foreground(preflight, request, verification, worker)

        assert result.status is WorkflowForegroundActionStatus.INDETERMINATE
        assert "retained_execution_evidence_not_reconstructible" in result.diagnostics
        assert worker.identity_reads == 0
        assert worker.calls == 0

    def test__dispatch_authorization__derives_bounded_attempt_identity(
        self, tmp_path: Path
    ) -> None:
        _, _, preflight, plan = self.prepared(tmp_path)
        _, verification = self.execution_request(preflight, plan)

        with pytest.raises(ValueError, match="exceeds the plan bound"):
            WorkflowDispatchAuthorization.create(
                plan=plan,
                effect_intent=plan.effect_intents[0],
                attempt_ordinal=3,
                worker_identity=WorkflowForegroundWorkerIdentity("synthetic-worker:1"),
                authority_verification=verification,
                limit_references=(),
            )

    def test__worker_evidence__rejects_runtime_reference_kinds(
        self, tmp_path: Path
    ) -> None:
        _, _, preflight, plan = self.prepared(tmp_path)
        request, _ = self.execution_request(preflight, plan)

        with pytest.raises(
            ValueError,
            match="runtime-reserved reference kind",
        ):
            WorkflowExecutionEvidence.create(
                request=request,
                outcome=WorkflowEffectOutcomeKind.SUCCEEDED,
                evidence_references=(
                    WorkflowRuntimeEvidenceReference(
                        "effect-intent", "application-collision"
                    ),
                ),
                reason_codes=("synthetic_report",),
            )

    def test__dispatch__records_terminal_exhaustion_at_attempt_bound(
        self, tmp_path: Path
    ) -> None:
        runtime, repository, preflight, plan = self.prepared(tmp_path)
        first_request, first_verification = self.execution_request(preflight, plan)
        first = runtime.dispatch_foreground(
            preflight,
            first_request,
            first_verification,
            self.Worker(WorkflowEffectOutcomeKind.KNOWN_NOT_APPLIED),
        )
        second_request, second_verification = self.execution_request(
            preflight, plan, attempt_ordinal=2
        )

        exhausted = runtime.dispatch_foreground(
            preflight,
            second_request,
            second_verification,
            self.Worker(WorkflowEffectOutcomeKind.KNOWN_NOT_APPLIED),
        )
        loaded = repository.load(preflight.run.identity.value)

        assert first.status is WorkflowForegroundActionStatus.RECORDED
        assert exhausted.status is (WorkflowForegroundActionStatus.ATTEMPTS_EXHAUSTED)
        assert exhausted.event is not None
        assert exhausted.event.kind is (
            WorkflowRuntimeEventKind.TERMINAL_FAILURE_RECORDED
        )
        assert loaded.history is not None
        assert loaded.history.head == exhausted.event

    def test__dispatch__requires_ordered_predecessor_effects(
        self, tmp_path: Path
    ) -> None:
        runtime, _, preflight, plan = self.prepared(tmp_path, effect_count=2)
        second_request, second_verification = self.execution_request(
            preflight, plan, effect_ordinal=1
        )
        second_worker = self.Worker(WorkflowEffectOutcomeKind.SUCCEEDED)

        premature = runtime.dispatch_foreground(
            preflight,
            second_request,
            second_verification,
            second_worker,
        )
        first_request, first_verification = self.execution_request(preflight, plan)
        first_worker = self.Worker(WorkflowEffectOutcomeKind.SUCCEEDED)
        first = runtime.dispatch_foreground(
            preflight,
            first_request,
            first_verification,
            first_worker,
        )
        second = runtime.dispatch_foreground(
            preflight,
            second_request,
            second_verification,
            second_worker,
        )

        assert premature.status is WorkflowForegroundActionStatus.CONFLICT
        assert premature.diagnostics == ("predecessor_effect_not_applied",)
        assert first.status is WorkflowForegroundActionStatus.RECORDED
        assert second.status is WorkflowForegroundActionStatus.RECORDED
        assert second_worker.calls == 1

    def test__transition__requires_all_foreground_effects_applied(
        self, tmp_path: Path
    ) -> None:
        runtime, _, preflight, plan = self.prepared(tmp_path)
        transition = transition_input(runtime_fixture())
        assert transition.adapter_evidence is not None

        premature = runtime.record_transition(transition)
        request, verification = self.execution_request(preflight, plan)
        worker = self.Worker(
            WorkflowEffectOutcomeKind.SUCCEEDED,
            evidence_references=(
                WorkflowRuntimeEvidenceReference(
                    "adapter-evidence",
                    transition.adapter_evidence.identity.value,
                ),
            ),
        )
        dispatched = runtime.dispatch_foreground(
            preflight, request, verification, worker
        )
        completed = runtime.record_transition(transition)

        assert premature.diagnostics == ("foreground_effects_not_conclusively_applied",)
        assert dispatched.status is WorkflowForegroundActionStatus.RECORDED
        assert completed.event is not None
        assert completed.event.kind is (WorkflowRuntimeEventKind.TRANSITION_RECORDED)

    def test__transition__rejects_unbound_final_adapter_evidence(
        self, tmp_path: Path
    ) -> None:
        runtime, _, preflight, plan = self.prepared(tmp_path)
        request, verification = self.execution_request(preflight, plan)
        worker = self.Worker(WorkflowEffectOutcomeKind.SUCCEEDED)
        dispatched = runtime.dispatch_foreground(
            preflight, request, verification, worker
        )

        result = runtime.record_transition(transition_input(runtime_fixture()))

        assert dispatched.status is WorkflowForegroundActionStatus.RECORDED
        assert result.diagnostics == ("foreground_final_evidence_not_bound",)

    def test__transition__rejects_final_evidence_from_failed_attempt(
        self, tmp_path: Path
    ) -> None:
        runtime, _, preflight, plan = self.prepared(tmp_path)
        transition = transition_input(runtime_fixture())
        assert transition.adapter_evidence is not None
        first_request, first_verification = self.execution_request(preflight, plan)
        failed = self.Worker(
            WorkflowEffectOutcomeKind.KNOWN_NOT_APPLIED,
            evidence_references=(
                WorkflowRuntimeEvidenceReference(
                    "adapter-evidence",
                    transition.adapter_evidence.identity.value,
                ),
            ),
        )
        first = runtime.dispatch_foreground(
            preflight, first_request, first_verification, failed
        )
        second_request, second_verification = self.execution_request(
            preflight, plan, attempt_ordinal=2
        )
        second = runtime.dispatch_foreground(
            preflight,
            second_request,
            second_verification,
            self.Worker(WorkflowEffectOutcomeKind.SUCCEEDED),
        )

        completed = runtime.record_transition(transition)

        assert first.status is WorkflowForegroundActionStatus.RECORDED
        assert second.status is WorkflowForegroundActionStatus.RECORDED
        assert completed.diagnostics == ("foreground_final_evidence_not_bound",)

    def test__reconciliation_replay__repairs_missing_terminal_exhaustion(
        self, tmp_path: Path
    ) -> None:
        runtime, repository, preflight, plan = self.prepared(
            tmp_path, maximum_attempts_per_intent=1
        )
        execution_request, verification = self.execution_request(preflight, plan)
        dispatched = runtime.dispatch_foreground(
            preflight,
            execution_request,
            verification,
            self.RaisingWorker(),
        )
        assert dispatched.execution_evidence is not None
        reconciliation_request = WorkflowReconciliationRequest(
            execution_request, dispatched.execution_evidence
        )
        evidence = WorkflowReconciliationEvidence.create(
            request=reconciliation_request,
            reconciler_identity=self.Reconciler(
                WorkflowReconciliationOutcomeKind.CONFIRMED_NOT_APPLIED
            ).identity,
            outcome=(WorkflowReconciliationOutcomeKind.CONFIRMED_NOT_APPLIED),
            evidence_references=(),
            reason_codes=("synthetic_not_applied",),
        )
        loaded = repository.load(preflight.run.identity.value)
        assert loaded.history is not None
        event = WorkflowRuntimeEvent.create(
            kind=WorkflowRuntimeEventKind.RECONCILIATION_RECORDED,
            run_identity=preflight.run.identity,
            ordinal=loaded.history.head.ordinal + 1,
            predecessor_event_identity=loaded.history.head.identity,
            core_revision=preflight.run.revision,
            core_state_identity=preflight.prior_state.identity,
            occurrence_identity=plan.occurrence_identity,
            request_identity=preflight.request.identity,
            operation_identity=preflight.request.operation_identity,
            evidence_references=(
                WorkflowRuntimeEvidenceReference(
                    "execution-evidence",
                    dispatched.execution_evidence.identity.value,
                ),
                WorkflowRuntimeEvidenceReference(
                    "reconciliation-evidence", evidence.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "workflow-reconciler",
                    evidence.reconciler_identity.value,
                ),
            ),
            reason_codes=(evidence.outcome.value, *evidence.reason_codes),
        )
        appended = repository.append(
            event,
            expected_event_identity=loaded.history.head.identity,
            idempotency_identity="synthetic-final-reconciliation",
        )
        assert appended.event == event
        reconciler = self.Reconciler(WorkflowReconciliationOutcomeKind.STILL_AMBIGUOUS)

        result = runtime.reconcile_foreground(
            preflight, reconciliation_request, reconciler
        )

        assert result.status is (WorkflowForegroundActionStatus.ATTEMPTS_EXHAUSTED)
        assert result.event is not None
        assert result.event.kind is (WorkflowRuntimeEventKind.TERMINAL_FAILURE_RECORDED)
        assert reconciler.calls == 0

    def test__dispatch_replay__repairs_missing_terminal_exhaustion(
        self, tmp_path: Path
    ) -> None:
        runtime, repository, preflight, plan = self.prepared(
            tmp_path, maximum_attempts_per_intent=1
        )
        request, verification = self.execution_request(preflight, plan)
        loaded = repository.load(preflight.run.identity.value)
        assert loaded.history is not None
        authorization = request.authorization
        authorization_event = WorkflowRuntimeEvent.create(
            kind=WorkflowRuntimeEventKind.DISPATCH_AUTHORIZED,
            run_identity=preflight.run.identity,
            ordinal=loaded.history.head.ordinal + 1,
            predecessor_event_identity=loaded.history.head.identity,
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
                    "dispatch-authorization", authorization.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "effect-intent", request.effect_intent.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "foreground-plan", plan.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "workflow-attempt", authorization.attempt_identity.value
                ),
            ),
        )
        first_append = repository.append(
            authorization_event,
            expected_event_identity=loaded.history.head.identity,
            idempotency_identity="synthetic-final-authorization",
        )
        assert first_append.event == authorization_event
        evidence = WorkflowExecutionEvidence.create(
            request=request,
            outcome=WorkflowEffectOutcomeKind.KNOWN_NOT_APPLIED,
            evidence_references=(),
            reason_codes=("synthetic_not_applied",),
        )
        execution_event = WorkflowRuntimeEvent.create(
            kind=WorkflowRuntimeEventKind.EXECUTION_RECORDED,
            run_identity=preflight.run.identity,
            ordinal=authorization_event.ordinal + 1,
            predecessor_event_identity=authorization_event.identity,
            core_revision=preflight.run.revision,
            core_state_identity=preflight.prior_state.identity,
            occurrence_identity=plan.occurrence_identity,
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
                    "foreground-plan", plan.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "workflow-attempt", authorization.attempt_identity.value
                ),
            ),
            reason_codes=(evidence.outcome.value, *evidence.reason_codes),
        )
        second_append = repository.append(
            execution_event,
            expected_event_identity=authorization_event.identity,
            idempotency_identity="synthetic-final-execution",
        )
        assert second_append.event == execution_event
        worker = self.IdentityTrackingWorker()

        result = runtime.dispatch_foreground(preflight, request, verification, worker)

        assert result.status is (WorkflowForegroundActionStatus.ATTEMPTS_EXHAUSTED)
        assert result.event is not None
        assert result.event.kind is (WorkflowRuntimeEventKind.TERMINAL_FAILURE_RECORDED)
        assert worker.identity_reads == 0
        assert worker.calls == 0

    def test__dispatch__retained_authorization_without_report_never_retries(
        self, tmp_path: Path
    ) -> None:
        runtime, repository, preflight, plan = self.prepared(tmp_path)
        request, verification = self.execution_request(preflight, plan)
        loaded = repository.load(preflight.run.identity.value)
        assert loaded.history is not None
        history = loaded.history
        authorization = request.authorization
        authorization_event = WorkflowRuntimeEvent.create(
            kind=WorkflowRuntimeEventKind.DISPATCH_AUTHORIZED,
            run_identity=preflight.run.identity,
            ordinal=history.head.ordinal + 1,
            predecessor_event_identity=history.head.identity,
            core_revision=preflight.run.revision,
            core_state_identity=preflight.prior_state.identity,
            occurrence_identity=plan.occurrence_identity,
            request_identity=preflight.request.identity,
            operation_identity=preflight.request.operation_identity,
            evidence_references=(
                WorkflowRuntimeEvidenceReference(
                    "dispatch-authorization", authorization.identity.value
                ),
                WorkflowRuntimeEvidenceReference(
                    "effect-intent", request.effect_intent.identity.value
                ),
            ),
        )
        appended = repository.append(
            authorization_event,
            expected_event_identity=history.head.identity,
            idempotency_identity="synthetic-crash-boundary",
        )
        assert appended.event == authorization_event
        worker = self.Worker(WorkflowEffectOutcomeKind.SUCCEEDED)

        result = runtime.dispatch_foreground(preflight, request, verification, worker)

        assert result.status is (WorkflowForegroundActionStatus.RECONCILIATION_REQUIRED)
        assert result.diagnostics == ("authorized_attempt_requires_reconciliation",)
        assert result.execution_evidence is not None
        assert result.event is not None
        assert result.event.kind is WorkflowRuntimeEventKind.EXECUTION_RECORDED
        assert result.execution_evidence.reason_codes == (
            "authorization_without_worker_report",
        )
        assert worker.calls == 0

        reconciler = self.Reconciler(
            WorkflowReconciliationOutcomeKind.CONFIRMED_NOT_APPLIED
        )
        reconciled = runtime.reconcile_foreground(
            preflight,
            WorkflowReconciliationRequest(request, result.execution_evidence),
            reconciler,
        )
        assert reconciled.status is WorkflowForegroundActionStatus.RECORDED
