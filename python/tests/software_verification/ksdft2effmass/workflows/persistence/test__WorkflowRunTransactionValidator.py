r"""Software verification of ``WorkflowRunTransactionValidator``.

Bounded artifact scope: exact candidate binding and immutable structural extension.

Evidence profile: claim_bearing

Facet and represented meaning

An independently authored one-invocation history supplies closed Task, membership,
attempt, production, outcome and transition links. Named mutations challenge closure
and byte-equivalent predecessor extension without reconstructing the validation rules.

Intrinsic and cross-object scope

The validator is the public owner under test. Fixed wire and explicit record changes
are inputs; contract-required statuses, preserved transaction and bytes are the oracle.
Serialization used for mutated input labels is setup, never an expected-wire oracle.

VVUQ and scientific exclusions

Synthetic software verification only. No stored presence, computed replay equality,
scientific validation, execution authority or recovered claim receipt is established.
"""

from dataclasses import replace
from pathlib import Path
from typing import Literal

import pytest
from ksdft2effmass import workflows as w
from ksdft2effmass.analysis import (
    QuantityOfInterestResultValueSerializer,
    ScalarQuantityOfInterestValue,
)
from ksdft2effmass.application import ApplicationResultValueSerializer
from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoResultValueSerializer,
)
from ksdft2effmass.persistence import Revision
from ksdft2effmass.petrinet import colored as c
from ksdft2effmass.workflows import WorkflowRunTransactionValidator

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunTransactionValidator


class TestWorkflowRunTransactionValidator:
    """Contract-driven structural and extension oracles, not repository evidence."""

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

    @staticmethod
    def wire(name: str = "workflow-run-closed-history-v1.json") -> bytes:
        return Path(__file__).with_name("resources").joinpath(name).read_bytes()

    @classmethod
    def make_history(cls) -> w.WorkflowRunSnapshot:
        wire = cls.wire()
        decoded = cls.make_serializer().deserialize(wire)
        assert decoded.status == "decoded", decoded.failure
        assert decoded.run is not None and decoded.binding is not None
        return w.WorkflowRunSnapshot(
            run=decoded.run,
            binding=decoded.binding,
            revision=Revision(
                stream_id="run",
                revision_id="history",
                predecessor_revision_id="genesis",
                schema_id="ksdft2effmass.workflow-run:1",
                content_id="ksdft2effmass.workflow-run:1:sha256:151c4567b6bb7567c85b213e5c87456303c9345c410dfa0740fc87e785328623",
                payload=wire,
            ),
        )

    @classmethod
    def make_transaction(
        cls, run: w.WorkflowRun, binding: w.WorkflowRunCommitBinding
    ) -> w.WorkflowRunTransaction:
        """Encode mutated input metadata only; statuses remain independent oracles."""
        encoded = cls.make_serializer().serialize(run, binding)
        assert encoded.status == "encoded", encoded.failure
        assert encoded.encoded is not None
        return w.WorkflowRunTransaction(
            binding=binding,
            run_identity=run.identity,
            expected_predecessor_revision_identity=run.predecessor_revision_identity,
            candidate=run,
            schema_identity=encoded.encoded.schema_identity,
            content_identity=encoded.encoded.content_identity,
        )

    @classmethod
    def make_snapshot(
        cls, run: w.WorkflowRun, binding: w.WorkflowRunCommitBinding
    ) -> w.WorkflowRunSnapshot:
        """Supply exact input bytes for nonliteral predecessor variants, not load."""
        encoded = cls.make_serializer().serialize(run, binding)
        assert encoded.status == "encoded", encoded.failure
        assert encoded.encoded is not None
        return w.WorkflowRunSnapshot(
            run=run,
            binding=binding,
            revision=Revision(
                stream_id=run.identity.value,
                revision_id=run.revision_identity.value,
                predecessor_revision_id=(
                    None
                    if run.predecessor_revision_identity is None
                    else run.predecessor_revision_identity.value
                ),
                schema_id=encoded.encoded.schema_identity,
                content_id=encoded.encoded.content_identity,
                payload=encoded.encoded.payload,
            ),
        )

    @staticmethod
    def make_extension(old: w.WorkflowRun) -> w.WorkflowRun:
        """Append a pending invocation with a lexically earlier Task identity."""
        instance = w.TaskInstance(
            w.TaskInstanceIdentity("a-instance"),
            w.TaskDefinitionIdentity("other-task"),
            None,
        )
        activation = w.TaskActivation(
            w.TaskActivationIdentity("a-activation"),
            old.workflow_identity,
            old.identity,
            instance,
            w.OperationIdentity("a-operation"),
            w.AttemptIdentity("a-attempt"),
            (),
            w.DirectTaskActivationSelection(
                c.ColoredPetriNetSelectionResultIdentity("c" * 64)
            ),
        )
        attempt = w.TaskAttempt(
            identity=w.TaskAttemptRecordIdentity("a-started"),
            workflow_run_identity=old.identity,
            task_instance_identity=instance.identity,
            activation_identity=activation.identity,
            operation_identity=activation.operation_identity,
            attempt_identity=activation.attempt_identity,
            status=w.TaskAttemptStatus.STARTED,
        )
        membership = w.TaskWorkflowMembership(
            identity=w.TaskWorkflowMembershipIdentity("a-member"),
            workflow_run_identity=old.identity,
            workflow_identity=old.workflow_identity,
            task_instance_identity=instance.identity,
        )
        return replace(
            old,
            revision_identity=w.WorkflowRunRevisionIdentity("extension"),
            predecessor_revision_identity=old.revision_identity,
            task_instances=(instance, *old.task_instances),
            task_memberships=(membership, *old.task_memberships),
            activations=(activation, *old.activations),
            attempts=(*old.attempts, attempt),
        )

    @classmethod
    def make_claimed_snapshot(cls) -> w.WorkflowRunSnapshot:
        """Decode the retained claim as byte-bound input, not stored presence."""
        decoded = cls.make_serializer().deserialize(cls.wire("claim-receipt-v1.json"))
        assert decoded.run is not None and decoded.binding is not None
        return cls.make_snapshot(decoded.run, decoded.binding)

    @staticmethod
    def make_entry_run(old: w.WorkflowRun) -> w.WorkflowRun:
        """Append explicit entry state to the independently retained claim history."""
        return replace(
            old,
            revision_identity=w.WorkflowRunRevisionIdentity("entered"),
            predecessor_revision_identity=old.revision_identity,
            dispatch_entries=(
                w.SimulationDispatchEntry(
                    identity=w.SimulationDispatchEntryIdentity("entry"),
                    workflow_run_identity=old.identity,
                    predecessor_revision_identity=w.WorkflowRunRevisionIdentity(
                        "claimed"
                    ),
                    committed_revision_identity=w.WorkflowRunRevisionIdentity(
                        "entered"
                    ),
                    claimed_reservation_identity=w.AuthorityReservationOutcomeIdentity(
                        "claimed"
                    ),
                    request_identity=w.SimulationExecutionRequestIdentity("request"),
                    obligation_identity=w.ObligationIdentity("obligation"),
                    receipt_identity=w.SimulationDispatchEntryReceiptIdentity(
                        "entry-receipt"
                    ),
                    outcome_identity=w.SimulationDispatchOutcomeIdentity("outcome"),
                ),
            ),
        )

    @pytest.mark.parametrize(
        "variant",
        [
            pytest.param("committed_revision", id="never_committed_entry_revision"),
            pytest.param("stale_predecessor", id="old_claim_in_later_predecessor"),
            pytest.param("genesis", id="entry_without_predecessor"),
        ],
    )
    def test_method__execute__binds_new_entry_to_transaction(
        self, variant: Literal["committed_revision", "stale_predecessor", "genesis"]
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-VALIDATOR-015

        Requirement: A new entry names the actual non-genesis committing revisions.

        Method: Submit exact byte-bound candidates with one detached entry boundary.

        Oracle: The entry consumes the transaction predecessor and names its successor.

        Acceptance: Invalid with no encoded candidate and retained transaction.

        Interpretation: Claim correlation alone does not establish entry introduction.

        Limitations: Synthetic validation, not stored presence or effect permission.
        """
        old = self.make_claimed_snapshot()
        if variant == "stale_predecessor":
            old = self.make_snapshot(
                replace(
                    old.run,
                    revision_identity=w.WorkflowRunRevisionIdentity("later"),
                    predecessor_revision_identity=old.run.revision_identity,
                ),
                old.binding,
            )
        run = self.make_entry_run(old.run)
        if variant == "committed_revision":
            run = replace(
                run,
                dispatch_entries=(
                    replace(
                        run.dispatch_entries[0],
                        committed_revision_identity=w.WorkflowRunRevisionIdentity(
                            "never-committed"
                        ),
                    ),
                ),
            )
        elif variant == "genesis":
            run = replace(run, predecessor_revision_identity=None)
        transaction = self.make_transaction(run, old.binding)
        result = SUT(serializer=self.make_serializer()).execute(
            transaction, None if variant == "genesis" else old
        )
        assert result.status == "invalid", result.failure
        assert result.transaction is transaction and result.encoded is None
        assert result.failure is not None

    def test_method__execute__accepts_exact_entry_introduction(self) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-VALIDATOR-016

        Requirement: Correctly bound new entry state is valid against its predecessor.

        Method: Append one explicit entry to the retained claimed revision.

        Oracle: Claimed predecessor and entered successor are the exact entry labels.

        Acceptance: Valid with encoded candidate and unchanged supplied transaction.

        Interpretation: Introduction checks permit the documented entry transition.

        Limitations: No store, acknowledgement, replay or execution is established.
        """
        old = self.make_claimed_snapshot()
        transaction = self.make_transaction(self.make_entry_run(old.run), old.binding)
        result = SUT(serializer=self.make_serializer()).execute(transaction, old)
        assert result.status == "valid", result.failure
        assert result.transaction is transaction and result.encoded is not None

    @pytest.mark.parametrize(
        "rewrite",
        [
            pytest.param(False, id="retain_original_entry_revision"),
            pytest.param(True, id="reject_historical_entry_rewrite"),
        ],
    )
    def test_method__execute__preserves_historical_entry_labels(
        self, rewrite: bool
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-VALIDATOR-017

        Requirement: Historical entries keep their original introduction revisions.

        Method: Extend entered state, optionally rewriting its existing entry label.

        Oracle: Immutable predecessor bytes, not the new transaction's revision labels.

        Acceptance: Unchanged history is valid; changed historical entry is invalid.

        Interpretation: The new-entry rule must not rebind existing entry records.

        Limitations: Synthetic exact-byte extension, not historical store evidence.
        """
        claimed = self.make_claimed_snapshot()
        old = self.make_snapshot(self.make_entry_run(claimed.run), claimed.binding)
        run = replace(
            old.run,
            revision_identity=w.WorkflowRunRevisionIdentity("after-entry"),
            predecessor_revision_identity=old.run.revision_identity,
        )
        if rewrite:
            run = replace(
                run,
                dispatch_entries=(
                    replace(
                        run.dispatch_entries[0],
                        committed_revision_identity=run.revision_identity,
                    ),
                ),
            )
        result = SUT(serializer=self.make_serializer()).execute(
            self.make_transaction(run, old.binding), old
        )
        assert result.status == ("invalid" if rewrite else "valid"), result.failure

    def test_method__execute__accepts_independent_closed_history(
        self, genesis_snapshot: w.WorkflowRunSnapshot
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-VALIDATOR-001

        Requirement: A complete byte-bound closed history extends its exact genesis.

        Method: Validate fixed independent wire against the fixed genesis snapshot.

        Oracle: Literal closed invocation links, content digest and exact payload.

        Acceptance: Valid retains the exact transaction/predecessor and literal bytes.

        Interpretation: Structural history validation, not computed replay equality.

        Limitations: One scalar-producing Task, without dispatch or authority history.
        """
        snapshot = self.make_history()
        transaction = w.WorkflowRunTransaction(
            binding=snapshot.binding,
            run_identity=w.WorkflowRunIdentity("run"),
            expected_predecessor_revision_identity=w.WorkflowRunRevisionIdentity(
                "genesis"
            ),
            candidate=snapshot.run,
            schema_identity=snapshot.revision.schema_id,
            content_identity=snapshot.revision.content_id,
        )
        result = SUT(serializer=self.make_serializer()).execute(
            transaction, genesis_snapshot
        )
        assert result.status == "valid", result.failure
        assert (
            result.transaction is transaction and result.predecessor is genesis_snapshot
        )
        assert result.encoded is not None and result.encoded.payload == self.wire()
        assert tuple(a.identity.value for a in transaction.candidate.attempts) == (
            "started",
            "terminal",
        )
        assert transaction.candidate.transitions[0].sequence_index == 0

    @pytest.mark.parametrize(
        "mutation, code",
        [
            pytest.param(
                "membership",
                "membership_correlation_error",
                id="missing_task_membership",
            ),
            pytest.param(
                "started", "attempt_correlation_error", id="missing_started_record"
            ),
            pytest.param(
                "outcome", "outcome_correlation_error", id="missing_terminal_outcome"
            ),
            pytest.param(
                "production", "result_correlation_error", id="missing_result_production"
            ),
            pytest.param(
                "reference", "result_correlation_error", id="missing_result_reference"
            ),
            pytest.param(
                "transition_attempt",
                "attempt_correlation_error",
                id="dangling_transition_attempt",
            ),
            pytest.param(
                "transition_activation",
                "activation_correlation_error",
                id="dangling_transition_activation",
            ),
            pytest.param(
                "selection",
                "outcome_correlation_error",
                id="detached_activation_selection",
            ),
            pytest.param(
                "sequence",
                "noncanonical_transition_order",
                id="noncontiguous_transition_sequence",
            ),
            pytest.param(
                "marking",
                "predecessor_marking_mismatch",
                id="broken_retained_marking_link",
            ),
        ],
    )
    def test_method__execute__rejects_broken_history_links(
        self, genesis_snapshot: w.WorkflowRunSnapshot, mutation: str, code: str
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-VALIDATOR-002

        Requirement: Retained invocation and ordered marking links must close exactly.

        Method: Change one named link of the independently closed history.

        Oracle: The missing endpoint or sequence violation and existing replay issue
        code.

        Acceptance: Invalid carries the expected issue code and no encoded success.

        Interpretation: Serialized records alone cannot establish structural closure.

        Limitations: This finite link partition is not all authority or nested variants.
        """
        snapshot = self.make_history()
        run = snapshot.run
        transition = run.transitions[0]
        assert type(transition) is w.TaskWorkflowTransitionRecord
        if mutation == "membership":
            run = replace(run, task_memberships=())
        elif mutation == "started":
            run = replace(run, attempts=run.attempts[1:])
        elif mutation == "outcome":
            run = replace(run, outcomes=())
        elif mutation == "production":
            run = replace(run, result_productions=())
        elif mutation == "reference":
            run = replace(run, result_references=())
        elif mutation == "transition_attempt":
            run = replace(
                run,
                transitions=(
                    replace(
                        transition,
                        terminal_attempt_record_identity=w.TaskAttemptRecordIdentity(
                            "missing"
                        ),
                    ),
                ),
            )
        elif mutation == "transition_activation":
            run = replace(
                run,
                transitions=(
                    replace(
                        transition,
                        activation_identity=w.TaskActivationIdentity("missing"),
                    ),
                ),
            )
        elif mutation == "selection":
            run = replace(
                run,
                activations=(
                    replace(
                        run.activations[0],
                        selection=w.DirectTaskActivationSelection(
                            c.ColoredPetriNetSelectionResultIdentity("d" * 64)
                        ),
                    ),
                ),
            )
        elif mutation == "sequence":
            run = replace(run, transitions=(replace(transition, sequence_index=1),))
        else:
            firing = transition.firing_result
            run = replace(
                run,
                transitions=(
                    replace(
                        transition,
                        firing_result=replace(
                            firing,
                            firing_input=replace(
                                firing.firing_input,
                                predecessor_marking=replace(
                                    run.initial_marking,
                                    identity=c.ColoredPetriNetMarkingIdentity(
                                        "detached"
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            )
        result = SUT(serializer=self.make_serializer()).execute(
            self.make_transaction(run, snapshot.binding), genesis_snapshot
        )
        assert result.status == "invalid", result.failure
        assert result.encoded is None and result.failure is not None
        assert (
            result.failure.code is w.WorkflowPersistenceFailureCode.INVARIANT_VIOLATION
        )
        assert result.failure.diagnostic.startswith(code + ":")

    @pytest.mark.parametrize(
        "mutation, status",
        [
            pytest.param("run", "invalid", id="transaction_run_substitution"),
            pytest.param("expected", "invalid", id="predecessor_slot_substitution"),
            pytest.param("content", "invalid", id="detached_content_label"),
            pytest.param("schema", "incompatible", id="unsupported_transaction_schema"),
            pytest.param("binding", "invalid", id="changed_transaction_binding"),
            pytest.param("writer", "incompatible", id="unsupported_historical_writer"),
            pytest.param("run_schema", "incompatible", id="unsupported_run_schema"),
        ],
    )
    def test_method__execute__binds_same_transaction_candidate(
        self, genesis_transaction: w.WorkflowRunTransaction, mutation: str, status: str
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-VALIDATOR-003

        Requirement: Validation binds exact labels, candidate and supported versions.

        Method: Substitute one transaction correlation without inferring new metadata.

        Oracle: Exact genesis bytes and supported schema/writer contract.

        Acceptance: Expected invalid/incompatible status retains input and no success.

        Interpretation: Validating another candidate cannot validate this transaction.

        Limitations: No shared Commit or store acknowledgement is exercised.
        """
        transaction = genesis_transaction
        if mutation == "run":
            transaction = replace(
                transaction, run_identity=w.WorkflowRunIdentity("other")
            )
        elif mutation == "expected":
            transaction = replace(
                transaction,
                expected_predecessor_revision_identity=w.WorkflowRunRevisionIdentity(
                    "other"
                ),
            )
        elif mutation == "content":
            transaction = replace(transaction, content_identity="detached")
        elif mutation == "schema":
            transaction = replace(
                transaction, schema_identity="ksdft2effmass.workflow-run:2"
            )
        elif mutation == "binding":
            transaction = replace(
                transaction,
                binding=replace(transaction.binding, transaction_identity="other"),
            )
        elif mutation == "writer":
            transaction = replace(
                transaction,
                binding=replace(
                    transaction.binding, persistence_implementation_identity="writer:2"
                ),
            )
        else:
            transaction = replace(
                transaction, candidate=replace(transaction.candidate, schema_version=2)
            )
        result = SUT(serializer=self.make_serializer()).execute(transaction)
        assert result.status == status and result.transaction is transaction
        assert result.encoded is None and result.failure is not None

    @pytest.mark.parametrize(
        "mutation",
        [
            pytest.param("missing", id="non_genesis_without_predecessor"),
            pytest.param("extra", id="genesis_with_predecessor"),
            pytest.param("address", id="wrong_snapshot_address"),
            pytest.param("payload", id="wrong_snapshot_payload"),
            pytest.param("binding", id="wrong_snapshot_binding"),
            pytest.param("run", id="wrong_snapshot_run"),
        ],
    )
    def test_method__execute__requires_exact_predecessor_snapshot(
        self,
        genesis_snapshot: w.WorkflowRunSnapshot,
        genesis_transaction: w.WorkflowRunTransaction,
        mutation: str,
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-VALIDATOR-004

        Requirement: Genesis and extension require exact and distinct predecessor
        inputs.

        Method: Supply absent, extra, substituted-address or detached-byte snapshots.

        Oracle: Explicit historical genesis envelope and candidate predecessor identity.

        Acceptance: Invalid contains failure without encoded candidate.

        Interpretation: Snapshot construction alone is not validated predecessor
        evidence.

        Limitations: The repository's exact historical read remains separate work.
        """
        history = self.make_history()
        transaction = self.make_transaction(history.run, history.binding)
        predecessor: w.WorkflowRunSnapshot | None = genesis_snapshot
        if mutation == "missing":
            predecessor = None
        elif mutation == "extra":
            transaction = genesis_transaction
        elif mutation == "address":
            predecessor = replace(
                genesis_snapshot,
                revision=replace(genesis_snapshot.revision, stream_id="other"),
            )
        elif mutation == "payload":
            predecessor = replace(
                genesis_snapshot,
                revision=replace(genesis_snapshot.revision, payload=b"detached"),
            )
        elif mutation == "binding":
            predecessor = replace(genesis_snapshot, binding=history.binding)
        else:
            predecessor = replace(genesis_snapshot, run=history.run)
        result = SUT(serializer=self.make_serializer()).execute(
            transaction, predecessor
        )
        assert result.status == "invalid" and result.encoded is None
        assert result.failure is not None

    def test_method__execute__extends_collections_by_identity(self) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-VALIDATOR-005

        Requirement: Unordered-by-history collections may insert earlier lexical
        identities.

        Method: Append one pending invocation whose canonical identity sorts before old
        data.

        Oracle: Retained original history and explicit new pending invocation.

        Acceptance: Valid exact transaction retains new sorted member and old attempt
        prefix.

        Interpretation: Append-only is identity extension, not tuple prefix for every
        field.

        Limitations: No authority, dispatch or nested pending invocation is represented.
        """
        old = self.make_history()
        run = self.make_extension(old.run)
        transaction = self.make_transaction(run, old.binding)
        result = SUT(serializer=self.make_serializer()).execute(transaction, old)
        assert result.status == "valid", result.failure
        assert result.transaction is transaction
        assert run.task_instances[0].identity.value == "a-instance"
        assert tuple(a.identity.value for a in run.attempts) == (
            "started",
            "terminal",
            "a-started",
        )

    @pytest.mark.parametrize(
        "mutation",
        [
            pytest.param("attempt_order", id="rewritten_attempt_prefix"),
            pytest.param("transition", id="replaced_transition_prefix"),
            pytest.param("member", id="removed_historical_member_identity"),
            pytest.param("instance", id="rewritten_same_identity_instance"),
        ],
    )
    def test_method__execute__rejects_structurally_closed_history_rewrite(
        self, mutation: str
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-VALIDATOR-006

        Requirement: Structural closure cannot excuse rewriting predecessor records.

        Method: Modify a still-closed extension in one sequence or identity collection.

        Oracle: The literal predecessor records must remain byte-equivalent.

        Acceptance: Invalid identifies immutable predecessor rewrite, not a link
        failure.

        Interpretation: Structural validity and immutable extension are distinct gates.

        Limitations: The fixture does not cover every stored record variant.
        """
        old = self.make_history()
        run = self.make_extension(old.run)
        if mutation == "attempt_order":
            run = replace(run, attempts=(run.attempts[-1], *run.attempts[:-1]))
        elif mutation == "transition":
            transition = run.transitions[0]
            assert type(transition) is w.TaskWorkflowTransitionRecord
            run = replace(
                run,
                transitions=(
                    replace(
                        transition,
                        identity=w.TaskWorkflowTransitionRecordIdentity("replaced"),
                    ),
                ),
            )
        elif mutation == "member":
            run = replace(
                run,
                task_memberships=(
                    run.task_memberships[0],
                    replace(
                        run.task_memberships[1],
                        identity=w.TaskWorkflowMembershipIdentity("replacement"),
                    ),
                ),
            )
        else:
            instance = replace(
                run.task_instances[1],
                definition_identity=w.TaskDefinitionIdentity("changed-definition"),
            )
            run = replace(
                run,
                task_instances=(run.task_instances[0], instance),
                activations=(
                    run.activations[0],
                    replace(run.activations[1], task_instance=instance),
                ),
            )
        result = SUT(serializer=self.make_serializer()).execute(
            self.make_transaction(run, old.binding), old
        )
        assert result.status == "invalid" and result.failure is not None
        assert (
            result.failure.diagnostic
            == "candidate rewrites or removes immutable predecessor state"
        )

    @pytest.mark.parametrize(
        "mutation",
        [
            pytest.param("workflow", id="workflow_identity_drift"),
            pytest.param("runtime", id="runtime_identity_drift"),
            pytest.param("definition", id="definition_reference_drift"),
            pytest.param("adapter", id="adapter_identity_drift"),
            pytest.param("initial", id="initial_marking_drift"),
        ],
    )
    def test_method__execute__preserves_immutable_run_foundations(
        self, genesis_snapshot: w.WorkflowRunSnapshot, mutation: str
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-VALIDATOR-007

        Requirement: Initial marking and exact Workflow/runtime/definition/adapter
        cannot drift.

        Method: Change one immutable foundation in an otherwise empty extension.

        Oracle: Independently fixed genesis values, preserved under byte equivalence.

        Acceptance: Invalid explicitly identifies immutable predecessor rewrite.

        Interpretation: New revision identity does not permit a replacement run model.

        Limitations: No mathematical or scientific interpretation is compared.
        """
        old = genesis_snapshot.run
        run = replace(
            old,
            revision_identity=w.WorkflowRunRevisionIdentity("next"),
            predecessor_revision_identity=old.revision_identity,
        )
        if mutation == "workflow":
            run = replace(run, workflow_identity=w.WorkflowIdentity("other"))
        elif mutation == "runtime":
            run = replace(
                run, runtime_bundle_identity=w.WorkflowRuntimeBundleIdentity("other")
            )
        elif mutation == "definition":
            run = replace(
                run,
                definition_reference_identity=w.WorkflowDefinitionReferenceIdentity(
                    "other"
                ),
            )
        elif mutation == "adapter":
            run = replace(run, adapter_implementation_identity="other")
        else:
            run = replace(
                run,
                initial_marking=replace(
                    run.initial_marking,
                    identity=c.ColoredPetriNetMarkingIdentity("other"),
                ),
            )
        result = SUT(serializer=self.make_serializer()).execute(
            self.make_transaction(run, genesis_snapshot.binding), genesis_snapshot
        )
        assert result.status == "invalid" and result.failure is not None
        assert (
            result.failure.diagnostic
            == "candidate rewrites or removes immutable predecessor state"
        )

    def test_method__execute__does_not_compute_replay_or_authorization(
        self, genesis_snapshot: w.WorkflowRunSnapshot, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-VALIDATOR-008

        Requirement: Structural validation neither fires nor authorizes nor proves final
        equality.

        Method: Forbid replay/firing/authorization and retain a different current
        marking.

        Oracle: Closed retained history can coexist with a replay-unequal current
        marking.

        Acceptance: Valid result without invoking any forbidden operation.

        Interpretation: Persistence structural closure cannot authorize advancement.

        Limitations: A final external replay gate remains required by the entry service.
        """
        snapshot = self.make_history()
        run = replace(
            snapshot.run,
            current_marking=replace(
                snapshot.run.current_marking,
                identity=c.ColoredPetriNetMarkingIdentity("unequal-current"),
            ),
        )
        transaction = self.make_transaction(run, snapshot.binding)
        with monkeypatch.context() as patch:
            patch.delattr(c.ColoredPetriNetTransitionFirer, "execute")
            patch.delattr(w.WorkflowRunReplayer, "execute")
            patch.delattr(w.SimulationExecutionAuthorizationResult, "evaluate")
            result = SUT(serializer=self.make_serializer()).execute(
                transaction, genesis_snapshot
            )
        assert result.status == "valid", result.failure

    @pytest.mark.parametrize(
        "placement",
        [
            pytest.param("reference", id="retained_array_reference"),
            pytest.param("confirmed", id="repeated_array_in_confirmed_history"),
        ],
    )
    def test_method__execute__compares_numpy_history_by_codec_bytes(
        self,
        placement: str,
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-VALIDATOR-009

        Requirement: Historical complete scientific values use exact codec bytes, not
        array equality.

        Method: Independently decode two array-backed observation graphs and extend one.

        Oracle: Unchanged complete observation bytes must preserve the old reference
        identity.

        Acceptance: Valid extension across distinct concrete result instances.

        Interpretation: Complete array-bearing values are retained without a dataclass
        truth test.

        Limitations: Synthetic observation data establishes no physical adequacy.
        """
        serializer = self.make_serializer()
        first = serializer.deserialize(self.wire("workflow-run-observation-v1.json"))
        second = serializer.deserialize(self.wire("workflow-run-observation-v1.json"))
        assert (
            first.run is not None
            and first.binding is not None
            and second.run is not None
        )
        if placement == "confirmed":
            history = self.make_history()
            reference = replace(
                first.run.result_references[0],
                producer_provenance=history.run.result_references[
                    0
                ].producer_provenance,
            )
            old = self.make_snapshot(
                replace(
                    history.run,
                    result_references=(reference,),
                    outcomes=(replace(history.run.outcomes[0], results=(reference,)),),
                ),
                history.binding,
            )
            second = serializer.deserialize(old.revision.payload)
        else:
            old = self.make_snapshot(replace(first.run, outcomes=()), first.binding)
        assert second.run is not None
        run = replace(
            second.run,
            outcomes=() if placement == "reference" else second.run.outcomes,
            revision_identity=w.WorkflowRunRevisionIdentity("next"),
            predecessor_revision_identity=old.run.revision_identity,
        )
        assert (
            run.result_references[0].result is not old.run.result_references[0].result
        )
        result = SUT(serializer=serializer).execute(
            self.make_transaction(run, old.binding), old
        )
        assert result.status == "valid", result.failure

    def test_method__execute__propagates_codec_failure(
        self, genesis_snapshot: w.WorkflowRunSnapshot
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-VALIDATOR-010

        Requirement: Unsupported concrete values remain incompatible, never valid empty
        results.

        Method: Supply observation input to the explicitly scalar-only codec.

        Oracle: Exact scalar codec support excludes QE observations.

        Acceptance: Incompatible retains the owning codec failure and no encoded
        success.

        Interpretation: Structural closure cannot expand outward result support.

        Limitations: Operational codec error propagation is covered by the fault case
        separately.
        """
        decoded = self.make_serializer().deserialize(
            self.wire("workflow-run-observation-v1.json")
        )
        assert decoded.run is not None and decoded.binding is not None
        transaction = self.make_transaction(
            replace(decoded.run, outcomes=()), decoded.binding
        )
        result = SUT(
            serializer=w.WorkflowRunSerializer(
                result_codec=QuantityOfInterestResultValueSerializer()
            )
        ).execute(transaction)
        assert result.status == "incompatible" and result.failure is not None
        assert result.failure.code is w.WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE
        assert (
            result.failure.implementation_identity
            == "ksdft2effmass.analysis.QuantityOfInterestResultValueSerializer:1"
        )

    @pytest.mark.parametrize(
        "operation",
        [
            pytest.param("serialize", id="encode_boundary_exception"),
            pytest.param("deserialize", id="decode_boundary_exception"),
        ],
    )
    def test_method__execute__sanitizes_operational_exception(
        self,
        genesis_transaction: w.WorkflowRunTransaction,
        operation: str,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-VALIDATOR-011

        Requirement: Unexpected operation failure returns error without leaking
        exception text.

        Method: Remove one serializer operation after constructing the explicit
        validator.

        Oracle: Missing operation is not a successful validation or domain invariant
        failure.

        Acceptance: Error, codec_error and no encoded candidate with sanitized
        diagnostic.

        Interpretation: Infrastructure uncertainty cannot become structural success.

        Limitations: Synthetic local operation fault, not a runtime infrastructure
        failure.
        """
        validator = SUT(serializer=self.make_serializer())
        with monkeypatch.context() as patch:
            patch.delattr(w.WorkflowRunSerializer, operation)
            result = validator.execute(genesis_transaction)
        assert result.status == "error" and result.encoded is None
        assert (
            result.failure is not None
            and result.failure.code is w.WorkflowPersistenceFailureCode.CODEC_ERROR
        )
        assert result.failure.diagnostic == "validation did not complete"

    def test_method__execute__rejects_equal_identity_changed_result_content(
        self,
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-VALIDATOR-013

        Requirement: Historical value equality requires bytes, not just identity.

        Method: Replace scalar content consistently at all candidate occurrences.

        Oracle: The predecessor retains signed zero, not the newly supplied scalar one.

        Acceptance: Invalid identifies immutable predecessor rewrite.

        Interpretation: Internal candidate agreement cannot replace historical content.

        Limitations: Exact representation, not a numerical tolerance comparison.
        """
        old = self.make_history()
        reference = old.run.result_references[0]
        value = reference.result
        assert type(value) is ScalarQuantityOfInterestValue
        changed = replace(value, value=1.0)
        envelope = QuantityOfInterestResultValueSerializer().encode(changed)
        assert envelope.encoded is not None
        reference = replace(
            reference,
            result=changed,
            content_identity=envelope.encoded.content_identity,
        )
        run = replace(
            old.run,
            revision_identity=w.WorkflowRunRevisionIdentity("next"),
            predecessor_revision_identity=old.run.revision_identity,
            result_references=(reference,),
            outcomes=(replace(old.run.outcomes[0], results=(reference,)),),
        )
        result = SUT(serializer=self.make_serializer()).execute(
            self.make_transaction(run, old.binding),
            old,
        )
        assert result.status == "invalid" and result.failure is not None
        assert result.failure.diagnostic == (
            "candidate rewrites or removes immutable predecessor state"
        )

    def test_method__execute__rejects_unclosed_predecessor(self) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-VALIDATOR-014

        Requirement: An exact predecessor snapshot must itself have closed history.

        Method: Supply byte-bound missing-membership history and a closed successor.

        Oracle: The old Task instance lacks membership despite successor repair.

        Acceptance: Invalid explicitly reports predecessor membership correlation.

        Interpretation: Candidate closure cannot retrospectively validate old state.

        Limitations: No repository read or historical presence is established.
        """
        history = self.make_history()
        old = self.make_snapshot(
            replace(history.run, task_memberships=()), history.binding
        )
        run = replace(
            history.run,
            revision_identity=w.WorkflowRunRevisionIdentity("next"),
            predecessor_revision_identity=old.run.revision_identity,
        )
        result = SUT(serializer=self.make_serializer()).execute(
            self.make_transaction(run, history.binding),
            old,
        )
        assert result.status == "invalid" and result.failure is not None
        assert result.failure.diagnostic.startswith(
            "predecessor: membership_correlation_error:"
        )

    @pytest.mark.parametrize(
        "boundary",
        [
            pytest.param("serializer", id="wrong_serializer_dependency"),
            pytest.param("transaction", id="wrong_direct_transaction"),
            pytest.param("predecessor", id="wrong_direct_predecessor"),
        ],
    )
    def test_method__types__rejects_wrong_direct_semantic_types(
        self,
        genesis_transaction: w.WorkflowRunTransaction,
        boundary: Literal["serializer", "transaction", "predecessor"],
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-VALIDATOR-012

        Requirement: Direct API wrong semantic types raise TypeError rather than
        represented error.

        Method: Supply one exact string at each concrete API boundary.

        Oracle: Explicit serializer, transaction and snapshot types in the public
        contract.

        Acceptance: TypeError at the exact invalid call.

        Interpretation: Wire error vocabulary does not weaken Python input typing.

        Limitations: All Python objects are not enumerated as invalid inputs.
        """
        with pytest.raises(TypeError):
            if boundary == "serializer":
                SUT(serializer="serializer")  # type: ignore[arg-type]
            elif boundary == "transaction":
                SUT(serializer=self.make_serializer()).execute("transaction")  # type: ignore[arg-type]
            else:
                SUT(serializer=self.make_serializer()).execute(
                    genesis_transaction,
                    "predecessor",  # type: ignore[arg-type]
                )
