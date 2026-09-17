r"""Software verification of ``WorkflowRunAtomicRepository``.

Evidence profile: claim_bearing

Bounded artifact scope: real SQLite intent/terminal commits and exact historical reads.

Facet and represented meaning

Both a new separate intent and an actual combined PENDING record survive a later
first-terminal observation, without history replacement or a second wire version.

Intrinsic and cross-object scope

Public constructors adapt an independent closed-history literal. Serialization
labels transaction inputs, not expected wire bytes. Real repository outcomes,
unchanged historical envelopes and zero rejected submissions are the oracles.

VVUQ and scientific exclusions

Synthetic child revision, replay and provenance labels do not establish child
execution, actual child replay, authority, cross-run atomicity or scientific truth.
"""

from dataclasses import replace
from pathlib import Path
from typing import Literal

import pytest
from ksdft2effmass import persistence as p
from ksdft2effmass import workflows as w
from ksdft2effmass.analysis import QuantityOfInterestResultValueSerializer
from ksdft2effmass.application import ApplicationResultValueSerializer
from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoResultValueSerializer,
)
from ksdft2effmass.workflows import WorkflowRunAtomicRepository

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunAtomicRepository

type IntentSource = Literal["separate", "combined"]
type TerminalKind = Literal["confirmed", "rejected", "indeterminate"]


class TestWorkflowRunAtomicRepositoryNestedHistory:
    """Own public two-commit v1 lifecycle evidence."""

    class CountingStore:
        """Record submissions while delegating actual SQLite operations."""

        def __init__(self, path: Path) -> None:
            self.store = p.SQLiteAtomicRevisionStore(
                path, busy_timeout_ms=1000, max_payload_bytes=1048576
            )
            self.commits: list[p.Commit] = []

        def read(self, request: p.RevisionReadRequest) -> p.RevisionReadResult:
            return self.store.read(request)

        def commit(self, commit: p.Commit) -> p.CommitResult:
            self.commits.append(commit)
            return self.store.commit(commit)

    @staticmethod
    def make_serializer() -> w.WorkflowRunSerializer:
        qe = QuantumEspressoResultValueSerializer()
        return w.WorkflowRunSerializer(
            result_codec=ApplicationResultValueSerializer(
                workflow_codec=w.WorkflowResultValueSerializer(source_codec=qe),
                quantum_espresso_codec=qe,
                quantity_of_interest_codec=QuantityOfInterestResultValueSerializer(),
            )
        )

    @classmethod
    def make_repository(
        cls, store: p.AtomicRevisionStore
    ) -> WorkflowRunAtomicRepository:
        serializer = cls.make_serializer()
        return SUT(
            store=store,
            serializer=serializer,
            validator=w.WorkflowRunTransactionValidator(serializer=serializer),
        )

    @classmethod
    def closed_history(cls) -> w.WorkflowRun:
        result = cls.make_serializer().deserialize(
            Path(__file__)
            .with_name("resources")
            .joinpath("workflow-run-closed-history-v1.json")
            .read_bytes()
        )
        assert result.run is not None, result.failure
        return result.run

    @classmethod
    def make_pending(cls, source: IntentSource) -> w.WorkflowRun:
        """Adapt literal closed invocation inputs to an explicit pending child."""
        base = cls.closed_history()
        started = replace(
            base.attempts[0], child_workflow_run_identity=w.WorkflowRunIdentity("child")
        )
        revision = w.WorkflowRunRevisionIdentity("intent")
        membership = w.NestedWorkflowMembership(
            identity=w.NestedWorkflowMembershipIdentity("child.membership"),
            parent_workflow_run_identity=base.identity,
            parent_revision_identity=revision,
            parent_task_instance_identity=started.task_instance_identity,
            child_workflow_identity=w.WorkflowIdentity("child.workflow"),
            child_workflow_run_identity=w.WorkflowRunIdentity("child"),
        )
        combined = w.NestedWorkflowInvocation(
            identity=w.NestedWorkflowInvocationIdentity("child.intent"),
            parent_workflow_run_identity=base.identity,
            parent_revision_identity=revision,
            parent_task_instance_identity=started.task_instance_identity,
            activation_identity=started.activation_identity,
            operation_identity=started.operation_identity,
            attempt_identity=started.attempt_identity,
            attempt_record_identity=started.identity,
            child_workflow_identity=membership.child_workflow_identity,
            child_workflow_run_identity=membership.child_workflow_run_identity,
            input_result_reference_identities=(),
            child_creation_idempotency_identity=w.ChildWorkflowCreationIdempotencyIdentity(
                "child.create"
            ),
            kind=w.NestedWorkflowInvocationKind.PENDING,
        )
        intent = w.NestedWorkflowInvocationIntent(
            identity=w.NestedWorkflowInvocationIntentIdentity("child.intent"),
            parent_workflow_run_identity=base.identity,
            parent_revision_identity=revision,
            parent_task_instance_identity=started.task_instance_identity,
            activation_identity=started.activation_identity,
            operation_identity=started.operation_identity,
            attempt_identity=started.attempt_identity,
            started_attempt_record_identity=started.identity,
            child_workflow_identity=membership.child_workflow_identity,
            child_workflow_run_identity=membership.child_workflow_run_identity,
            input_result_reference_identities=(),
            child_creation_idempotency_identity=combined.child_creation_idempotency_identity,
        )
        return replace(
            base,
            revision_identity=revision,
            predecessor_revision_identity=None,
            nested_memberships=(membership,),
            nested_invocations=(combined,) if source == "combined" else (),
            nested_invocation_intents=(intent,) if source == "separate" else (),
            attempts=(started,),
            outcomes=(),
            result_references=(),
            result_productions=(),
            result_dependencies=(),
            transitions=(),
            current_marking=base.initial_marking,
        )

    @classmethod
    def make_terminal(cls, pending: w.WorkflowRun, kind: TerminalKind) -> w.WorkflowRun:
        """Supply variant-specific terminal evidence without modifying intent."""
        base = cls.closed_history()
        starter = pending.attempts[0]
        attempt = replace(
            base.attempts[1],
            child_workflow_run_identity=w.WorkflowRunIdentity("child"),
            status=w.TaskAttemptStatus(kind),
        )
        source = (
            pending.nested_invocation_intents[0]
            if pending.nested_invocation_intents
            else pending.nested_invocations[0]
        )
        reference = base.result_references[0]
        producer = reference.producer_provenance
        assert isinstance(producer, w.RepresentedTaskResultProducer)
        reference = replace(
            reference,
            producer_provenance=replace(
                producer,
                workflow_identity=w.WorkflowIdentity("child.workflow"),
                workflow_run_identity=w.WorkflowRunIdentity("child"),
            ),
        )
        failure = w.TaskFailureRecord(
            identity=w.TaskFailureRecordIdentity("child.failure"),
            workflow_run_identity=pending.identity,
            task_instance_identity=starter.task_instance_identity,
            activation_identity=starter.activation_identity,
            operation_identity=starter.operation_identity,
            attempt_identity=starter.attempt_identity,
            terminal_attempt_record_identity=attempt.identity,
            child_workflow_run_identity=w.WorkflowRunIdentity("child"),
            failure=w.TaskInvocationFailure(
                identity=w.TaskInvocationFailureIdentity("failure.detail"),
                code="synthetic",
                operation_phase="child_observation",
                diagnostic="Synthetic rejection",
                retryable=False,
                claim_boundary=("synthetic only",),
            ),
        )
        outcome = replace(
            base.outcomes[0],
            kind=w.TaskInvocationOutcomeKind(kind),
            results=(reference,) if kind == "confirmed" else (),
            production_record_identities=base.outcomes[0].production_record_identities
            if kind == "confirmed"
            else (),
            failure_record_identity=failure.identity if kind == "rejected" else None,
            reconciliation_identity_values=("child.read",)
            if kind == "indeterminate"
            else (),
        )
        admission = w.ResultDependency(
            identity=w.ResultDependencyIdentity("child.admission"),
            result_reference_identity=reference.identity,
            producer_workflow_run_identity=w.WorkflowRunIdentity("child"),
            consumer_workflow_run_identity=pending.identity,
            consumer_task_instance_identity=starter.task_instance_identity,
            consumer_activation_identity=starter.activation_identity,
            input_name="export.result",
        )
        terminal_revision = w.WorkflowRunRevisionIdentity("terminal")
        observation = w.NestedWorkflowTerminalObservation(
            identity=w.NestedWorkflowObservationIdentity("child.observation"),
            intent_identity=source.identity,
            parent_workflow_run_identity=pending.identity,
            parent_revision_identity=terminal_revision,
            terminal_attempt_record_identity=attempt.identity,
            outcome_identity=outcome.identity,
            kind=w.NestedWorkflowTerminalObservationKind(kind),
            terminal_child_revision_identity=w.WorkflowRunRevisionIdentity(
                "child.terminal"
            )
            if kind == "confirmed"
            else None,
            replay_equal_child_result_identity=w.WorkflowRunReplayResultIdentity(
                "c" * 64
            )
            if kind == "confirmed"
            else None,
            exported_result_reference_identities=(reference.identity,)
            if kind == "confirmed"
            else (),
            export_admission_dependency_identities=(admission.identity,)
            if kind == "confirmed"
            else (),
            failure_record_identity=outcome.failure_record_identity,
            reconciliation_identity_values=outcome.reconciliation_identity_values,
        )
        return replace(
            pending,
            revision_identity=terminal_revision,
            predecessor_revision_identity=pending.revision_identity,
            nested_terminal_observations=(observation,),
            attempts=(starter, attempt),
            outcomes=(outcome,),
            result_references=(reference,) if kind == "confirmed" else (),
            result_productions=base.result_productions if kind == "confirmed" else (),
            result_dependencies=(admission,) if kind == "confirmed" else (),
            failures=(failure,) if kind == "rejected" else (),
            transitions=base.transitions if kind == "confirmed" else (),
            current_marking=base.current_marking
            if kind == "confirmed"
            else pending.current_marking,
        )

    @classmethod
    def transaction(cls, run: w.WorkflowRun) -> w.WorkflowRunTransaction:
        binding = w.WorkflowRunCommitBinding(
            transaction_identity=run.revision_identity.value,
            commit_idempotency_identity=run.revision_identity.value,
            persistence_implementation_identity="ksdft2effmass.workflows.WorkflowRunAtomicRepository:1",
        )
        encoded = cls.make_serializer().serialize(run, binding)
        assert encoded.encoded is not None, encoded.failure
        return w.WorkflowRunTransaction(
            binding=binding,
            run_identity=run.identity,
            expected_predecessor_revision_identity=run.predecessor_revision_identity,
            candidate=run,
            schema_identity=encoded.encoded.schema_identity,
            content_identity=encoded.encoded.content_identity,
        )

    @staticmethod
    def request(revision: str) -> p.RevisionReadRequest:
        return p.RevisionReadRequest(
            request_id="read." + revision,
            stream_id="run",
            selector=p.RevisionSelector.EXPLICIT_REVISION,
            revision_id=revision,
        )

    @pytest.mark.parametrize(
        "source,kind",
        (
            pytest.param("separate", "confirmed", id="separate_confirmed"),
            pytest.param("separate", "rejected", id="separate_rejected"),
            pytest.param("separate", "indeterminate", id="separate_indeterminate"),
            pytest.param("combined", "confirmed", id="combined_pending_confirmed"),
            pytest.param("combined", "rejected", id="combined_pending_rejected"),
            pytest.param(
                "combined", "indeterminate", id="combined_pending_indeterminate"
            ),
        ),
    )
    def test_method__commit__extends_retained_pending_intent(
        self, tmp_path: Path, source: IntentSource, kind: TerminalKind
    ) -> None:
        """Commit and reopen each v1 lifecycle without rewriting intent.

        Evidence ID: SV-WFR-REPOSITORY-NESTED-001

        Requirement: Each intent source supports one first terminal of each kind
        while preserving exact predecessor bytes, content and original binding.

        Method: Commit I to SQLite, reopen/read I, construct T from that loaded I,
        commit T, reopen/read both, then commit and reopen an unrelated extension.

        Oracle: Required committed/loaded statuses and exact retained envelopes.

        Acceptance: All commits succeed; I's envelope and both intent tuples are
        unchanged; T's complete terminal records survive reopen and later extension.

        Interpretation: Actual same-v1 parent history can advance without mutation.

        Limitations: No child stream is read and child replay labels are synthetic.
        """
        store = self.CountingStore(tmp_path / "nested.sqlite3")
        repository = self.make_repository(store)
        first = repository.commit(self.transaction(self.make_pending(source)))
        assert first.status == "committed", first.failure
        assert first.snapshot is not None
        assert first.snapshot.revision.schema_id == "ksdft2effmass.workflow-run:1"
        assert (b'"nested_invocation_intents"' in first.snapshot.revision.payload) == (
            source == "separate"
        )
        loaded = self.make_repository(store).load(self.request("intent"))
        assert loaded.snapshot is not None, loaded.failure
        terminal = self.make_terminal(loaded.snapshot.run, kind)
        second = self.make_repository(store).commit(self.transaction(terminal))
        assert second.status == "committed", second.failure
        assert second.snapshot is not None
        assert second.snapshot.revision.schema_id == "ksdft2effmass.workflow-run:1"
        assert b'"nested_terminal_observations"' in second.snapshot.revision.payload
        reopened = self.make_repository(self.CountingStore(tmp_path / "nested.sqlite3"))
        old = reopened.load(self.request("intent"))
        current = reopened.load(self.request("terminal"))
        assert old.snapshot is not None and current.snapshot is not None
        assert old.snapshot.revision == first.snapshot.revision
        assert old.snapshot.binding == first.snapshot.binding
        assert (
            current.snapshot.run.nested_invocations
            == first.snapshot.run.nested_invocations
        )
        assert (
            current.snapshot.run.nested_invocation_intents
            == first.snapshot.run.nested_invocation_intents
        )
        assert (
            current.snapshot.run.nested_terminal_observations
            == terminal.nested_terminal_observations
        )
        extended = replace(
            current.snapshot.run,
            revision_identity=w.WorkflowRunRevisionIdentity("later"),
            predecessor_revision_identity=current.snapshot.run.revision_identity,
        )
        assert reopened.commit(self.transaction(extended)).status == "committed"
        later_old = reopened.load(self.request("intent"))
        later_terminal = reopened.load(self.request("terminal"))
        assert later_old.snapshot is not None and later_terminal.snapshot is not None
        assert later_old.snapshot.revision == first.snapshot.revision
        assert later_terminal.snapshot.revision == second.snapshot.revision
        assert len(store.commits) == 2

    @pytest.mark.parametrize(
        "mutation",
        (
            pytest.param("wrong_revision", id="detached_introduction_revision"),
            pytest.param("missing_observation", id="pending_with_terminal_outcome"),
            pytest.param("wrong_intent", id="missing_nominal_source"),
            pytest.param("wrong_outcome", id="detached_generic_outcome"),
            pytest.param("wrong_attempt", id="detached_terminal_attempt"),
            pytest.param("missing_admission", id="missing_child_export_admission"),
            pytest.param("changed_intent", id="rewritten_intent_key"),
            pytest.param("removed_intent", id="deleted_intent"),
            pytest.param("wrong_started", id="terminal_record_as_original_started"),
            pytest.param("wrong_kind", id="mismatched_terminal_kind"),
            pytest.param("wrong_failure_child", id="detached_rejected_child"),
            pytest.param("wrong_reconciliation", id="mismatched_reconciliation"),
            pytest.param("absent_failure", id="absent_referenced_failure"),
            pytest.param("extra_export", id="extra_paired_export_outside_outcome"),
        ),
    )
    def test_method__commit__rejects_invalid_terminal_without_submission(
        self,
        tmp_path: Path,
        mutation: Literal[
            "wrong_revision",
            "missing_observation",
            "wrong_intent",
            "wrong_outcome",
            "wrong_attempt",
            "missing_admission",
            "changed_intent",
            "removed_intent",
            "wrong_started",
            "wrong_kind",
            "wrong_failure_child",
            "wrong_reconciliation",
            "absent_failure",
            "extra_export",
        ],
    ) -> None:
        """Reject malformed correlation and immutable-history changes before CAS.

        Evidence ID: SV-WFR-REPOSITORY-NESTED-002

        Requirement: A terminal successor must close over an unchanged retained
        intent and exact introduced terminal/outcome/export evidence.

        Method: Commit pending I and submit one named malformed T to a counting
        real SQLite store.

        Oracle: Invalid with no shared Commit, snapshot or claim receipt.

        Acceptance: Only I reaches the store and exact T is absent afterward.

        Interpretation: Domain-invalid candidates do not reach persistence.

        Limitations: These are bounded mutations, not exhaustive history verification.
        """
        store = self.CountingStore(tmp_path / "invalid.sqlite3")
        repository = self.make_repository(store)
        pending = self.make_pending("separate")
        assert repository.commit(self.transaction(pending)).status == "committed"
        terminal = self.make_terminal(
            pending,
            "rejected"
            if mutation in {"wrong_failure_child", "absent_failure"}
            else "indeterminate"
            if mutation == "wrong_reconciliation"
            else "confirmed",
        )
        observation = terminal.nested_terminal_observations[0]
        match mutation:
            case "wrong_revision":
                terminal = replace(
                    terminal,
                    nested_terminal_observations=(
                        replace(
                            observation,
                            parent_revision_identity=w.WorkflowRunRevisionIdentity(
                                "never-committed"
                            ),
                        ),
                    ),
                )
            case "missing_observation":
                terminal = replace(terminal, nested_terminal_observations=())
            case "wrong_intent":
                terminal = replace(
                    terminal,
                    nested_terminal_observations=(
                        replace(
                            observation,
                            intent_identity=w.NestedWorkflowInvocationIdentity(
                                "child.intent"
                            ),
                        ),
                    ),
                )
            case "wrong_outcome":
                terminal = replace(
                    terminal,
                    nested_terminal_observations=(
                        replace(
                            observation,
                            outcome_identity=w.TaskInvocationOutcomeIdentity("absent"),
                        ),
                    ),
                )
            case "wrong_attempt":
                terminal = replace(
                    terminal,
                    nested_terminal_observations=(
                        replace(
                            observation,
                            terminal_attempt_record_identity=pending.attempts[
                                0
                            ].identity,
                        ),
                    ),
                )
            case "missing_admission":
                terminal = replace(terminal, result_dependencies=())
            case "changed_intent":
                terminal = replace(
                    terminal,
                    nested_invocation_intents=(
                        replace(
                            terminal.nested_invocation_intents[0],
                            child_creation_idempotency_identity=w.ChildWorkflowCreationIdempotencyIdentity(
                                "changed"
                            ),
                        ),
                    ),
                )
            case "removed_intent":
                terminal = replace(terminal, nested_invocation_intents=())
            case "wrong_started":
                terminal = replace(
                    terminal,
                    nested_invocation_intents=(
                        replace(
                            terminal.nested_invocation_intents[0],
                            started_attempt_record_identity=terminal.attempts[
                                1
                            ].identity,
                        ),
                    ),
                )
            case "wrong_kind":
                terminal = replace(
                    terminal,
                    nested_terminal_observations=(
                        replace(
                            observation,
                            kind=w.NestedWorkflowTerminalObservationKind.REJECTED,
                            terminal_child_revision_identity=None,
                            replay_equal_child_result_identity=None,
                            exported_result_reference_identities=(),
                            export_admission_dependency_identities=(),
                            failure_record_identity=w.TaskFailureRecordIdentity(
                                "failure"
                            ),
                        ),
                    ),
                )
            case "wrong_failure_child":
                terminal = replace(
                    terminal,
                    failures=(
                        replace(terminal.failures[0], child_workflow_run_identity=None),
                    ),
                )
            case "wrong_reconciliation":
                terminal = replace(
                    terminal,
                    nested_terminal_observations=(
                        replace(
                            observation,
                            reconciliation_identity_values=("different.read",),
                        ),
                    ),
                )
            case "absent_failure":
                terminal = replace(terminal, failures=())
            case "extra_export":
                terminal = replace(
                    terminal,
                    nested_terminal_observations=(
                        replace(
                            observation,
                            exported_result_reference_identities=(
                                w.ResultObjectReferenceIdentity("extra"),
                            )
                            + observation.exported_result_reference_identities,
                            export_admission_dependency_identities=observation.export_admission_dependency_identities
                            + (w.ResultDependencyIdentity("extra.admission"),),
                        ),
                    ),
                )
        result = repository.commit(self.transaction(terminal))
        assert result.status == "invalid", result.failure
        assert result.snapshot is None and result.store_result is None
        assert result.claim_receipts == ()
        assert len(store.commits) == 1
        absent = repository.load(self.request("terminal"))
        assert absent.status == "absent" and absent.snapshot is None

    @pytest.mark.parametrize(
        "selected",
        (
            pytest.param("separate", id="resolve_separate_nominal_source"),
            pytest.param("combined", id="resolve_combined_nominal_source"),
        ),
    )
    def test_method__commit__resolves_coexisting_equal_string_sources(
        self, tmp_path: Path, selected: IntentSource
    ) -> None:
        """Resolve the nominal source when both same-string alternatives exist.

        Evidence ID: SV-WFR-REPOSITORY-NESTED-006

        Requirement: Terminal resolution preserves the exact nominal source, even
        when both source types share their identity string in the predecessor.

        Method: Commit two distinct child invocations with same-string nominal
        source IDs, reject a terminal naming the wrong existing alternative, then
        commit and reload the correctly linked terminal.

        Oracle: Wrong-alternative invalid/no submission, correct-alternative
        committed, and exact typed observation link retained after reload.

        Acceptance: Two successful submissions total, no wrong-alternative receipt,
        and the selected terminal targets survive while the other intent stays pending.

        Interpretation: Bare-string lookup cannot substitute for nominal resolution.

        Limitations: Indeterminate synthetic outcomes do not establish child truth.
        """
        store = self.CountingStore(tmp_path / "nominal.sqlite3")
        repository = self.make_repository(store)
        pending = self.make_pending("separate")
        instance = replace(
            pending.task_instances[0],
            identity=w.TaskInstanceIdentity("instance.second"),
        )
        activation = replace(
            pending.activations[0],
            identity=w.TaskActivationIdentity("activation.second"),
            task_instance=instance,
            operation_identity=w.OperationIdentity("operation.second"),
            attempt_identity=w.AttemptIdentity("attempt.second"),
        )
        started = replace(
            pending.attempts[0],
            identity=w.TaskAttemptRecordIdentity("started.second"),
            task_instance_identity=instance.identity,
            activation_identity=activation.identity,
            operation_identity=activation.operation_identity,
            attempt_identity=activation.attempt_identity,
            child_workflow_run_identity=w.WorkflowRunIdentity("child.second"),
        )
        combined = replace(
            self.make_pending("combined").nested_invocations[0],
            parent_task_instance_identity=instance.identity,
            activation_identity=activation.identity,
            operation_identity=activation.operation_identity,
            attempt_identity=activation.attempt_identity,
            attempt_record_identity=started.identity,
            child_workflow_run_identity=w.WorkflowRunIdentity("child.second"),
            child_creation_idempotency_identity=w.ChildWorkflowCreationIdempotencyIdentity(
                "child.create.second"
            ),
        )
        pending = replace(
            pending,
            task_instances=pending.task_instances + (instance,),
            task_memberships=pending.task_memberships
            + (
                replace(
                    pending.task_memberships[0],
                    identity=w.TaskWorkflowMembershipIdentity("membership.second"),
                    task_instance_identity=instance.identity,
                ),
            ),
            activations=pending.activations + (activation,),
            attempts=pending.attempts + (started,),
            nested_memberships=pending.nested_memberships
            + (
                replace(
                    pending.nested_memberships[0],
                    identity=w.NestedWorkflowMembershipIdentity(
                        "child.membership.second"
                    ),
                    parent_task_instance_identity=instance.identity,
                    child_workflow_run_identity=combined.child_workflow_run_identity,
                ),
            ),
            nested_invocations=(combined,),
        )
        assert repository.commit(self.transaction(pending)).status == "committed"
        terminal = self.make_terminal(pending, "indeterminate")
        attempt = terminal.attempts[-1]
        outcome = terminal.outcomes[0]
        observation = terminal.nested_terminal_observations[0]
        if selected == "combined":
            attempt = replace(
                attempt,
                identity=w.TaskAttemptRecordIdentity("terminal.second"),
                task_instance_identity=instance.identity,
                activation_identity=activation.identity,
                operation_identity=activation.operation_identity,
                attempt_identity=activation.attempt_identity,
                predecessor_attempt_record_identity=started.identity,
                child_workflow_run_identity=combined.child_workflow_run_identity,
            )
            outcome = replace(
                outcome,
                identity=w.TaskInvocationOutcomeIdentity("outcome.second"),
                activation_identity=activation.identity,
                operation_identity=activation.operation_identity,
                attempt_identity=activation.attempt_identity,
                terminal_attempt_record_identity=attempt.identity,
            )
            observation = replace(
                observation,
                intent_identity=combined.identity,
                terminal_attempt_record_identity=attempt.identity,
                outcome_identity=outcome.identity,
            )
        terminal = replace(
            terminal,
            attempts=pending.attempts + (attempt,),
            outcomes=(outcome,),
            nested_terminal_observations=(observation,),
        )
        wrong_identity = (
            pending.nested_invocation_intents[0].identity
            if selected == "combined"
            else combined.identity
        )
        wrong = replace(
            terminal,
            nested_terminal_observations=(
                replace(observation, intent_identity=wrong_identity),
            ),
        )
        rejected = repository.commit(self.transaction(wrong))
        assert rejected.status == "invalid", rejected.failure
        assert (
            rejected.snapshot is None
            and rejected.store_result is None
            and rejected.claim_receipts == ()
        )
        assert len(store.commits) == 1
        result = repository.commit(self.transaction(terminal))
        assert result.status == "committed", result.failure
        assert len(store.commits) == 2
        reloaded = self.make_repository(store).load(self.request("terminal"))
        assert reloaded.snapshot is not None
        assert reloaded.snapshot.run.nested_terminal_observations == (observation,)
        assert reloaded.snapshot.run.nested_invocations == pending.nested_invocations
        assert (
            reloaded.snapshot.run.nested_invocation_intents
            == pending.nested_invocation_intents
        )
        assert reloaded.snapshot.run.outcomes == (outcome,)

    def test_method__commit__rejects_observation_on_combined_terminal(
        self, tmp_path: Path
    ) -> None:
        """Do not reinterpret an already-terminal combined record as intent.

        Evidence ID: SV-WFR-REPOSITORY-NESTED-007

        Requirement: A retained combined terminal record cannot receive a separate
        terminal observation, regardless of that observation's new identity.

        Method: Commit an existing-form indeterminate terminal history, then submit
        a separate observation linked to that actual combined terminal source.

        Oracle: Invalid with no candidate shared Commit, snapshot or receipt.

        Acceptance: Only the original terminal history reaches the store and it
        reloads unchanged after rejection.

        Interpretation: Combined terminal evidence does not become pending intent.

        Limitations: The initial retained terminal is synthetic legacy-form history.
        """
        store = self.CountingStore(tmp_path / "combined-terminal.sqlite3")
        repository = self.make_repository(store)
        pending = self.make_pending("combined")
        terminal = self.make_terminal(pending, "indeterminate")
        observation = terminal.nested_terminal_observations[0]
        combined = replace(
            pending.nested_invocations[0],
            kind=w.NestedWorkflowInvocationKind.INDETERMINATE,
            attempt_record_identity=observation.terminal_attempt_record_identity,
            terminal_observation_identity=observation.identity,
            reconciliation_identity_values=observation.reconciliation_identity_values,
        )
        retained = replace(
            terminal,
            predecessor_revision_identity=None,
            nested_invocations=(combined,),
            nested_terminal_observations=(),
        )
        first = repository.commit(self.transaction(retained))
        assert first.status == "committed", first.failure
        candidate = replace(
            retained,
            revision_identity=w.WorkflowRunRevisionIdentity("later"),
            predecessor_revision_identity=retained.revision_identity,
            nested_terminal_observations=(
                replace(
                    observation,
                    identity=w.NestedWorkflowObservationIdentity("new.observation"),
                    parent_revision_identity=w.WorkflowRunRevisionIdentity("later"),
                ),
            ),
        )
        result = repository.commit(self.transaction(candidate))
        assert result.status == "invalid", result.failure
        assert (
            result.snapshot is None
            and result.store_result is None
            and result.claim_receipts == ()
        )
        assert len(store.commits) == 1
        reloaded = repository.load(self.request("terminal"))
        assert reloaded.snapshot is not None and first.snapshot is not None
        assert reloaded.snapshot.revision == first.snapshot.revision
        assert repository.load(self.request("later")).status == "absent"

    @pytest.mark.parametrize(
        "boundary",
        (
            pytest.param(
                "detached_revision", id="consistent_but_detached_introduction"
            ),
            pytest.param(
                "activation_started", id="reused_activation_and_started_group"
            ),
            pytest.param(
                "membership", id="replacement_source_reuses_retained_membership"
            ),
        ),
    )
    def test_method__commit__rejects_invalid_new_intent_introduction(
        self,
        tmp_path: Path,
        boundary: Literal["detached_revision", "activation_started", "membership"],
    ) -> None:
        """Reject new intent with false introduction or reused retained groups.

        Evidence ID: SV-WFR-REPOSITORY-NESTED-008

        Requirement: New intent introduces membership/activation/STARTED together
        in its actual candidate revision and cannot rewrite retained source history.

        Method: Submit consistent detached intent/membership labels at genesis, or
        attempt to repurpose an ordinary STARTED group or combined-source membership.

        Oracle: Invalid without a candidate Commit, snapshot or receipt; an optional
        valid predecessor remains exactly reloadable.

        Acceptance: Only the optional predecessor reaches the store; invalid new
        intent is absent and retained predecessor bytes are unchanged.

        Interpretation: Labels and reused records cannot fabricate a new introduction.

        Limitations: Reused-group cases also exercise immutable history: public
        closure makes reuse inseparable from changing or removing prior records.
        """
        store = self.CountingStore(tmp_path / "new-intent.sqlite3")
        repository = self.make_repository(store)
        candidate = self.make_pending("separate")
        predecessor: w.WorkflowRunWriteResult | None = None
        if boundary == "detached_revision":
            detached = w.WorkflowRunRevisionIdentity("never-committed")
            candidate = replace(
                candidate,
                nested_invocation_intents=(
                    replace(
                        candidate.nested_invocation_intents[0],
                        parent_revision_identity=detached,
                    ),
                ),
                nested_memberships=(
                    replace(
                        candidate.nested_memberships[0],
                        parent_revision_identity=detached,
                    ),
                ),
            )
        else:
            prior = self.make_pending("combined")
            if boundary == "activation_started":
                prior = replace(
                    prior,
                    nested_invocations=(),
                    nested_memberships=(),
                    attempts=(
                        replace(prior.attempts[0], child_workflow_run_identity=None),
                    ),
                )
            predecessor = repository.commit(self.transaction(prior))
            assert predecessor.status == "committed", predecessor.failure
            introduced = w.WorkflowRunRevisionIdentity("introduced")
            candidate = replace(
                candidate,
                revision_identity=introduced,
                predecessor_revision_identity=prior.revision_identity,
            )
            if boundary == "activation_started":
                candidate = replace(
                    candidate,
                    nested_invocation_intents=(
                        replace(
                            candidate.nested_invocation_intents[0],
                            parent_revision_identity=introduced,
                        ),
                    ),
                    nested_memberships=(
                        replace(
                            candidate.nested_memberships[0],
                            parent_revision_identity=introduced,
                        ),
                    ),
                )
        result = repository.commit(self.transaction(candidate))
        assert result.status == "invalid", result.failure
        assert (
            result.snapshot is None
            and result.store_result is None
            and result.claim_receipts == ()
        )
        assert len(store.commits) == (0 if predecessor is None else 1)
        if predecessor is not None:
            reloaded = repository.load(self.request("intent"))
            assert reloaded.snapshot is not None and predecessor.snapshot is not None
            assert reloaded.snapshot.revision == predecessor.snapshot.revision
        assert (
            repository.load(self.request(candidate.revision_identity.value)).status
            == "absent"
        )

    @pytest.mark.parametrize(
        "with_predecessor",
        (
            pytest.param(False, id="genesis_terminal_without_prior_intent"),
            pytest.param(True, id="same_commit_intent_and_terminal"),
        ),
    )
    def test_method__commit__requires_previously_committed_intent(
        self, tmp_path: Path, with_predecessor: bool
    ) -> None:
        """Require a retained intent before admitting any terminal observation.

        Evidence ID: SV-WFR-REPOSITORY-NESTED-005

        Requirement: Genesis terminal observations and intent-plus-terminal
        introductions in one commit are invalid.

        Method: Submit a closed candidate containing both groups either at genesis
        or against an empty predecessor which has no intent.

        Oracle: Invalid with no candidate store submission, snapshot or receipt.

        Acceptance: The store sees only the optional empty predecessor commit;
        the terminal candidate is not retained.

        Interpretation: Represented links cannot substitute for an actual prior intent.

        Limitations: Child streams and effects are absent from this synthetic case.
        """
        store = self.CountingStore(tmp_path / "introduction.sqlite3")
        repository = self.make_repository(store)
        pending = self.make_pending("separate")
        terminal = self.make_terminal(pending, "confirmed")
        empty = replace(
            pending,
            revision_identity=w.WorkflowRunRevisionIdentity("empty"),
            task_instances=(),
            task_memberships=(),
            nested_memberships=(),
            nested_invocation_intents=(),
            activations=(),
            attempts=(),
        )
        if with_predecessor:
            assert repository.commit(self.transaction(empty)).status == "committed"
        terminal = replace(
            terminal,
            predecessor_revision_identity=empty.revision_identity
            if with_predecessor
            else None,
            nested_memberships=(
                replace(
                    terminal.nested_memberships[0],
                    parent_revision_identity=terminal.revision_identity,
                ),
            ),
            nested_invocation_intents=(
                replace(
                    terminal.nested_invocation_intents[0],
                    parent_revision_identity=terminal.revision_identity,
                ),
            ),
        )
        result = repository.commit(self.transaction(terminal))
        assert result.status == "invalid", result.failure
        assert result.snapshot is None and result.claim_receipts == ()
        assert len(store.commits) == int(with_predecessor)
        assert repository.load(self.request("terminal")).status == "absent"

    def test_method__commit__rejects_second_indeterminate_terminal(
        self, tmp_path: Path
    ) -> None:
        """Retain first indeterminate evidence instead of replacing it later.

        Evidence ID: SV-WFR-REPOSITORY-NESTED-003

        Requirement: One first terminal per intent includes indeterminate; a new
        observation identity cannot replace the retained terminal observation.

        Method: Commit I and indeterminate T, then try an observation-identity
        replacement in a later revision against T.

        Oracle: Invalid without a third shared Commit and unchanged retained T.

        Acceptance: Exactly two store commits, no new snapshot or receipt, and
        original T reloads with its original observation.

        Interpretation: Indeterminate does not enable terminal-history replacement.

        Limitations: No later reconciliation, cancellation or compensation is added.
        """
        store = self.CountingStore(tmp_path / "repeat.sqlite3")
        repository = self.make_repository(store)
        pending = self.make_pending("separate")
        assert repository.commit(self.transaction(pending)).status == "committed"
        terminal = self.make_terminal(pending, "indeterminate")
        assert repository.commit(self.transaction(terminal)).status == "committed"
        changed = replace(
            terminal,
            revision_identity=w.WorkflowRunRevisionIdentity("later"),
            predecessor_revision_identity=terminal.revision_identity,
            nested_terminal_observations=(
                replace(
                    terminal.nested_terminal_observations[0],
                    identity=w.NestedWorkflowObservationIdentity("replacement"),
                    parent_revision_identity=w.WorkflowRunRevisionIdentity("later"),
                ),
            ),
        )
        result = repository.commit(self.transaction(changed))
        assert result.status == "invalid", result.failure
        assert result.snapshot is None and result.claim_receipts == ()
        assert len(store.commits) == 2
        loaded = repository.load(self.request("terminal"))
        assert loaded.snapshot is not None
        assert (
            loaded.snapshot.run.nested_terminal_observations
            == terminal.nested_terminal_observations
        )

    def test_method__commit__returns_conflict_for_valid_stale_terminal(
        self, tmp_path: Path
    ) -> None:
        """Let the shared CAS distinguish a valid stale terminal from invalid data.

        Evidence ID: SV-WFR-REPOSITORY-NESTED-004

        Requirement: A valid terminal based on historical I conflicts after a
        different successor becomes head; it does not get a receipt or retry.

        Method: Commit I, commit an unrelated extension, then submit valid T at I.

        Oracle: Conflict after one terminal submission, not structural invalidity.

        Acceptance: Three submissions total, conflict with no snapshot/receipt,
        and the losing terminal revision remains absent.

        Interpretation: Historical intent is necessary but does not bypass CAS.

        Limitations: This is a deterministic stale-head case, not a race benchmark.
        """
        store = self.CountingStore(tmp_path / "stale.sqlite3")
        repository = self.make_repository(store)
        pending = self.make_pending("combined")
        assert repository.commit(self.transaction(pending)).status == "committed"
        changed = replace(
            pending,
            revision_identity=w.WorkflowRunRevisionIdentity("other"),
            predecessor_revision_identity=pending.revision_identity,
        )
        assert repository.commit(self.transaction(changed)).status == "committed"
        result = repository.commit(
            self.transaction(self.make_terminal(pending, "rejected"))
        )
        assert result.status == "conflict", result.failure
        assert result.snapshot is None and result.claim_receipts == ()
        assert len(store.commits) == 3
        assert repository.load(self.request("terminal")).status == "absent"
