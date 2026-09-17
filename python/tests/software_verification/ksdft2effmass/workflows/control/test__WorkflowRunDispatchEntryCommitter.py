r"""Software verification of ``WorkflowRunDispatchEntryCommitter``.

Bounded artifact scope: durable entry permission over synthetic WorkflowRun history.

Evidence profile: claim_bearing

Facet and represented meaning

Historical claim recovery, exact current-head replay and fresh one-winner entry
are separate requirements. Synthetic SQLite histories and fake effect counters
exercise the public service, including process loss before the fake effect.

Intrinsic and cross-object scope

The owner is the entry service, not the repository's receipt derivation. Existing
literal histories provide closed records; adapter and authorizer labels are
explicitly set to supported replay versions before seeding independent stores.
No serializer round trip is used as an independent receipt oracle.

VVUQ and scientific exclusions

Software verification only: no QE executable, authority authentication, scientific
validation, exactly-once completion or human acceptance is established.
"""

import subprocess
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from threading import Barrier

import pytest
from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoResultValueSerializer,
)
from ksdft2effmass.persistence import (
    RevisionReadRequest,
    RevisionSelector,
    SQLiteAtomicRevisionStore,
)
from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetBindingSelectorIdentity,
    ColoredPetriNetDefinition,
    ColoredPetriNetExpressionEvaluatorIdentity,
    ColoredPetriNetOrderingPolicyIdentity,
    ColoredPetriNetTransitionEnablerIdentity,
    ColoredPetriNetTransitionFirerIdentity,
)
from ksdft2effmass.workflows import (
    AuthorityReservationOutcomeIdentity,
    SimulationDispatchEntryIdentity,
    SimulationDispatchOutcomeIdentity,
    SimulationDispatchRequest,
    SimulationExecutionRequest,
    TaskDefinitionIdentity,
    WorkflowDefinitionReference,
    WorkflowResultValueSerializer,
    WorkflowRunAtomicRepository,
    WorkflowRunClaimCommitReceiptIdentity,
    WorkflowRunCommitBinding,
    WorkflowRunDispatchEntryCommitter,
    WorkflowRunReplayer,
    WorkflowRunRevisionIdentity,
    WorkflowRunSerializer,
    WorkflowRunSnapshot,
    WorkflowRuntimeBundle,
    WorkflowRunTransaction,
    WorkflowRunTransactionValidator,
)

from .resources.entry_ports import (
    EntryAcknowledgementMode,
    EntryReadMode,
    EntryRepositoryProbe,
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunDispatchEntryCommitter


class TestWorkflowRunDispatchEntryCommitter:
    """Own independent synthetic entry-permission contract oracles."""

    @staticmethod
    def make_repository(path: Path) -> WorkflowRunAtomicRepository:
        serializer = WorkflowRunSerializer(
            result_codec=WorkflowResultValueSerializer(
                source_codec=QuantumEspressoResultValueSerializer()
            )
        )
        return WorkflowRunAtomicRepository(
            store=SQLiteAtomicRevisionStore(
                path, busy_timeout_ms=5000, max_payload_bytes=1048576
            ),
            serializer=serializer,
            validator=WorkflowRunTransactionValidator(serializer=serializer),
        )

    @staticmethod
    def make_bundle(snapshot: WorkflowRunSnapshot) -> WorkflowRuntimeBundle:
        run = snapshot.run
        definition = ColoredPetriNetDefinition(
            run.initial_marking.definition_identity, (), (), (), (), ()
        )
        tasks = (TaskDefinitionIdentity("simulation"),)
        reference = WorkflowDefinitionReference(
            identity=run.definition_reference_identity,
            workflow_identity=run.workflow_identity,
            workflow_definition_version=1,
            colored_petri_net_definition_identity=definition.identity,
            colored_petri_net_definition_version=1,
            task_definition_identities=tasks,
            schema_version=1,
        )
        return WorkflowRuntimeBundle(
            identity=run.runtime_bundle_identity,
            definition_reference=reference,
            schema_version=1,
            workflow_identity=run.workflow_identity,
            definition=definition,
            task_definition_identities=tasks,
            adapter_implementation_identity="workflow-cpn-adapter-v1",
            expression_evaluator_identity=ColoredPetriNetExpressionEvaluatorIdentity(
                "colored-petri-net-expression-evaluator-v1"
            ),
            ordering_policy_identity=ColoredPetriNetOrderingPolicyIdentity(
                "colored-petri-net-enablement-order-v1"
            ),
            transition_enabler_identity=ColoredPetriNetTransitionEnablerIdentity(
                "colored-petri-net-transition-enabler-v1"
            ),
            binding_selector_identity=ColoredPetriNetBindingSelectorIdentity(
                "colored-petri-net-binding-selector-v1"
            ),
            transition_firer_identity=ColoredPetriNetTransitionFirerIdentity(
                "colored-petri-net-transition-firer-v1"
            ),
        )

    @classmethod
    def seed(
        cls, path: Path
    ) -> tuple[
        WorkflowRunAtomicRepository, SimulationDispatchRequest, WorkflowRuntimeBundle
    ]:
        repository = cls.make_repository(path)
        cls.append_literal_revision(repository, "genesis-record-envelope.json")
        cls.append_literal_revision(repository, "prepared-run-v1.json")
        cls.append_literal_revision(repository, "claim-receipt-v1.json")
        request, bundle = cls.recover(repository)
        return repository, request, bundle

    @staticmethod
    def append_literal_revision(
        repository: WorkflowRunAtomicRepository, name: str
    ) -> None:
        """Seed one synthetic history step with explicitly supported replay labels."""
        payload = (
            Path(__file__).parent.parent / "persistence/resources" / name
        ).read_bytes()
        decoded = repository.serializer.deserialize(payload)
        assert decoded.run is not None and decoded.binding is not None
        run = replace(
            decoded.run,
            adapter_implementation_identity="workflow-cpn-adapter-v1",
            authorization_results=tuple(
                replace(
                    authorization,
                    authorizer_implementation_identity=(
                        "ksdft2effmass.workflows.SimulationExecutionAuthorizer.v1"
                    ),
                )
                for authorization in decoded.run.authorization_results
            ),
        )
        encoded = repository.serializer.serialize(run, decoded.binding)
        assert encoded.encoded is not None
        written = repository.commit(
            WorkflowRunTransaction(
                binding=decoded.binding,
                run_identity=run.identity,
                expected_predecessor_revision_identity=run.predecessor_revision_identity,
                candidate=run,
                schema_identity=encoded.encoded.schema_identity,
                content_identity=encoded.encoded.content_identity,
            )
        )
        assert written.status == "committed", written.failure

    @classmethod
    def recover(
        cls, repository: WorkflowRunAtomicRepository
    ) -> tuple[SimulationDispatchRequest, WorkflowRuntimeBundle]:
        observed = repository.load(
            RevisionReadRequest(
                request_id="observe-claim",
                stream_id="run",
                selector=RevisionSelector.EXPLICIT_REVISION,
                revision_id="claimed",
            )
        )
        snapshot = observed.snapshot
        assert snapshot is not None
        historical = repository.load_claim(
            RevisionReadRequest(
                request_id="confirm-claim",
                stream_id="run",
                selector=RevisionSelector.EXPLICIT_REVISION,
                revision_id="claimed",
                expected_predecessor_revision_id="prepared",
                expected_schema_id=snapshot.revision.schema_id,
                expected_content_id=snapshot.revision.content_id,
                expected_idempotency_id=snapshot.binding.commit_idempotency_identity,
            ),
            AuthorityReservationOutcomeIdentity("claimed"),
        )
        assert historical.receipt is not None
        run = snapshot.run
        preparation = next(
            a
            for a in run.authorization_results
            if a.request.phase.value == "preparation"
        )
        claim = next(a for a in run.authority_reservations if a.kind.value == "claimed")
        authorization = next(
            a for a in run.authorization_results if a.request.phase.value == "claim"
        )
        return SimulationDispatchRequest(
            execution_request=SimulationExecutionRequest(
                correlation=run.execution_request_correlations[0],
                obligation=run.dispatch_obligations[0],
                preparation_authorization=preparation,
            ),
            claim_authorization_request=authorization.request,
            claimed_reservation=claim,
            claim_commit_receipt=historical.receipt,
            outcome_identity=SimulationDispatchOutcomeIdentity("outcome"),
            dispatch_entry_identity=SimulationDispatchEntryIdentity("entry"),
            dispatch_entry_revision_identity=WorkflowRunRevisionIdentity("entered"),
        ), cls.make_bundle(snapshot)

    def test_method__execute__new_winner_and_reopen(self, tmp_path: Path) -> None:
        """Only a new acknowledged candidate permits the fake effect.

        Evidence ID: SV-WFR-ENTRY-001

        Requirement: Reopening and reusing a historical claim cannot recover permission.

        Method: Enter over real SQLite, inspect durable entry, reopen and repeat.

        Oracle: One effect counter increment and the exact persisted receipt identity.

        Acceptance: First entered, second already_entered without a receipt.

        Interpretation: Durable entry prevents a later call recovering permission.

        Limitations: The counter is synthetic, not a scientific process execution.
        """
        path = tmp_path / "entry.sqlite3"
        repository, request, bundle = self.seed(path)
        result = SUT(
            repository=repository,
            serializer=repository.serializer,
            runtime_bundle=bundle,
        ).execute(request)
        assert result.kind.value == "entered", result.diagnostics
        assert result.receipt is not None
        effect_count = 1 if result.receipt is not None else 0
        reopened = self.make_repository(path)
        latest = reopened.load(
            RevisionReadRequest(
                request_id="latest", stream_id="run", selector=RevisionSelector.LATEST
            )
        )
        assert latest.snapshot is not None
        assert (
            latest.snapshot.run.dispatch_entries[0].receipt_identity
            == result.receipt.identity
        )
        assert (
            latest.snapshot.revision.content_id
            == result.receipt.workflow_run_content_identity
        )
        assert (
            WorkflowRunReplayer().execute(latest.snapshot.run, bundle).outcome.value
            == "equal"
        )
        again = SUT(
            repository=reopened, serializer=reopened.serializer, runtime_bundle=bundle
        ).execute(request)
        effect_count += int(again.kind.value == "entered")
        assert again.kind.value == "already_entered"
        assert again.receipt is None
        assert effect_count == 1

    @pytest.mark.parametrize(
        "field",
        [
            pytest.param("identity", id="receipt_identity"),
            pytest.param("persistence_operation_identity", id="operation_identity"),
            pytest.param("persistence_implementation_identity", id="historical_writer"),
            pytest.param("commit_idempotency_identity", id="stored_key"),
            pytest.param("workflow_run_content_identity", id="content_identity"),
        ],
    )
    def test_method__execute__forged_receipt(self, tmp_path: Path, field: str) -> None:
        """Compare opaque receipt labels as well as constructor correlations.

        Evidence ID: SV-WFR-ENTRY-002

        Requirement: Every supplied historical receipt field must bind actual recovery.

        Method: Substitute one independently mutable receipt label before entry.

        Oracle: Historical repository reconstruction, not supplied receipt shape.

        Acceptance: Error, no receipt, and zero candidate submissions.

        Interpretation: Receipt labels cannot substitute for historical evidence.

        Limitations: Represented identity agreement is not authentication.
        """
        repository, request, bundle = self.seed(tmp_path / "entry.sqlite3")
        receipt = request.claim_commit_receipt
        if field == "identity":
            receipt = replace(
                receipt, identity=WorkflowRunClaimCommitReceiptIdentity("forged")
            )
        elif field == "persistence_operation_identity":
            receipt = replace(receipt, persistence_operation_identity="forged")
        elif field == "persistence_implementation_identity":
            receipt = replace(receipt, persistence_implementation_identity="forged")
        elif field == "commit_idempotency_identity":
            receipt = replace(receipt, commit_idempotency_identity="forged")
        else:
            receipt = replace(receipt, workflow_run_content_identity="forged")
        probe = EntryRepositoryProbe(repository)
        result = SUT(
            repository=probe, serializer=repository.serializer, runtime_bundle=bundle
        ).execute(replace(request, claim_commit_receipt=receipt))
        assert result.kind.value == "error" and result.receipt is None
        assert probe.transactions == []

    @pytest.mark.parametrize(
        "mode",
        [
            pytest.param("historical_request_id", id="historical_request_substitution"),
            pytest.param("historical_binding", id="historical_binding_substitution"),
            pytest.param("current_request_id", id="current_request_substitution"),
            pytest.param("current_run", id="current_run_substitution"),
        ],
    )
    def test_method__execute__detached_read_evidence(
        self, tmp_path: Path, mode: EntryReadMode
    ) -> None:
        """Bind both separately observed reads before proposing any entry.

        Evidence ID: SV-WFR-ENTRY-009

        Requirement: Historical and latest snapshots must match their complete
        returned read and wire evidence, not merely the supplied receipt.

        Method: Substitute one read correlation or reconstructed snapshot field
        through an explicit typed repository port over a seeded SQLite store.

        Oracle: Detached evidence cannot establish an exact current claim head.

        Acceptance: Error, no receipt and zero entry transactions.

        Interpretation: Historical confirmation alone cannot waive current-head
        and full snapshot consistency checks.

        Limitations: Synthetic response substitutions do not authenticate storage.
        """
        repository, request, bundle = self.seed(tmp_path / "entry.sqlite3")
        probe = EntryRepositoryProbe(repository, read_mode=mode)
        result = SUT(
            repository=probe, serializer=repository.serializer, runtime_bundle=bundle
        ).execute(request)
        assert result.kind.value == "error"
        assert result.receipt is None
        assert probe.transactions == []

    def test_method__execute__later_head_is_stale(self, tmp_path: Path) -> None:
        """Historical reconciliation does not waive exact latest-head equality.

        Evidence ID: SV-WFR-ENTRY-003

        Requirement: An unrelated later head prohibits advancement from an old claim.

        Method: Append a no-effect revision then use the still-recoverable claim.

        Oracle: The declared expected predecessor of the claim differs from latest.

        Acceptance: Error and zero entry submissions.

        Interpretation: Recoverable history is not the current advancement head.

        Limitations: The unrelated successor has no external effect.
        """
        repository, request, bundle = self.seed(tmp_path / "entry.sqlite3")
        loaded = repository.load(
            RevisionReadRequest(
                request_id="head", stream_id="run", selector=RevisionSelector.LATEST
            )
        )
        assert loaded.snapshot is not None
        run = replace(
            loaded.snapshot.run,
            predecessor_revision_identity=loaded.snapshot.run.revision_identity,
            revision_identity=WorkflowRunRevisionIdentity("later"),
        )
        binding = WorkflowRunCommitBinding(
            transaction_identity="later",
            commit_idempotency_identity="later",
            persistence_implementation_identity=loaded.snapshot.binding.persistence_implementation_identity,
        )
        encoded = repository.serializer.serialize(run, binding)
        assert encoded.encoded is not None
        assert (
            repository.commit(
                WorkflowRunTransaction(
                    binding=binding,
                    run_identity=run.identity,
                    expected_predecessor_revision_identity=run.predecessor_revision_identity,
                    candidate=run,
                    schema_identity=encoded.encoded.schema_identity,
                    content_identity=encoded.encoded.content_identity,
                )
            ).status
            == "committed"
        )
        probe = EntryRepositoryProbe(repository)
        result = SUT(
            repository=probe, serializer=repository.serializer, runtime_bundle=bundle
        ).execute(request)
        assert result.kind.value == "error" and result.receipt is None
        assert probe.transactions == []

    def test_method__execute__independent_instances_race(self, tmp_path: Path) -> None:
        """Two calls share a predecessor but never share their invocation candidate.

        Evidence ID: SV-WFR-ENTRY-004

        Requirement: Identical requests yield one newly acknowledged effect permission.

        Method: Barrier both independent repositories immediately before commit.

        Oracle: Atomic CAS gives one winner; fresh keys and receipt bytes differ.

        Acceptance: One entered, one already_entered, two distinct keys and receipts.

        Interpretation: Concurrent calls cannot share one winning invocation identity.

        Limitations: This bounded race assumes collision-resistant UUID generation.
        """
        path = tmp_path / "entry.sqlite3"
        first, request, bundle = self.seed(path)
        second = self.make_repository(path)
        barrier = Barrier(2)
        probes = (
            EntryRepositoryProbe(first, barrier=barrier),
            EntryRepositoryProbe(second, barrier=barrier),
        )
        a = SUT(
            repository=probes[0], serializer=first.serializer, runtime_bundle=bundle
        )
        b = SUT(
            repository=probes[1], serializer=second.serializer, runtime_bundle=bundle
        )
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = (pool.submit(a.execute, request), pool.submit(b.execute, request))
            results = tuple(f.result(timeout=20) for f in futures)
        assert sorted(r.kind.value for r in results) == ["already_entered", "entered"]
        assert sum(r.receipt is not None for r in results) == 1
        txa, txb = probes[0].transactions[0], probes[1].transactions[0]
        assert txa.commit_idempotency_identity != txb.commit_idempotency_identity
        assert (
            txa.candidate.dispatch_entries[0].receipt_identity
            != txb.candidate.dispatch_entries[0].receipt_identity
        )

    @pytest.mark.parametrize(
        "mode",
        [
            pytest.param("lost_ack", id="lost_acknowledgement"),
            pytest.param("wrong_key", id="substituted_shared_key"),
            pytest.param("wrong_snapshot", id="substituted_snapshot_bytes"),
            pytest.param("wrong_transaction", id="substituted_transaction"),
        ],
    )
    def test_method__execute__ambiguous_or_substituted_ack(
        self, tmp_path: Path, mode: EntryAcknowledgementMode
    ) -> None:
        """Postcommit uncertainty must never produce permission or a commit retry.

        Evidence ID: SV-WFR-ENTRY-005

        Requirement: Only the exact acknowledged invocation candidate can enter.

        Method: A typed port commits once then loses or substitutes acknowledgement.

        Oracle: Durable entry exists but no local permission may be recovered.

        Acceptance: Error, one submission, no receipt; reopened repeat already entered.

        Interpretation: A durable write cannot repair lost local permission evidence.

        Limitations: Faults are synthetic port responses, not hardware-failure coverage.
        """
        path = tmp_path / "entry.sqlite3"
        repository, request, bundle = self.seed(path)
        probe = EntryRepositoryProbe(repository, mode=mode)
        result = SUT(
            repository=probe, serializer=repository.serializer, runtime_bundle=bundle
        ).execute(request)
        assert result.kind.value == "error" and result.receipt is None
        assert len(probe.transactions) == 1
        reopened = self.make_repository(path)
        again = SUT(
            repository=reopened, serializer=reopened.serializer, runtime_bundle=bundle
        ).execute(request)
        assert again.kind.value == "already_entered" and again.receipt is None

    def test_method__execute__non_equal_runtime(self, tmp_path: Path) -> None:
        """Unsupported replay versions do not permit a commit.

        Evidence ID: SV-WFR-ENTRY-006

        Requirement: Current and candidate replay must be exactly equal.

        Method: Supply an unsupported evaluator identity to the explicit bundle.

        Oracle: The owning replayer's unsupported_version outcome is not equal.

        Acceptance: No candidate submitted and no permission.

        Interpretation: Supported replay is a separate gate from receipt recovery.

        Limitations: No CPN transition computation or scientific result is validated.
        """
        repository, request, bundle = self.seed(tmp_path / "entry.sqlite3")
        bundle = replace(
            bundle,
            expression_evaluator_identity=ColoredPetriNetExpressionEvaluatorIdentity(
                "unsupported"
            ),
        )
        probe = EntryRepositoryProbe(repository)
        result = SUT(
            repository=probe, serializer=repository.serializer, runtime_bundle=bundle
        ).execute(request)
        assert result.kind.value == "error" and result.receipt is None
        assert not probe.transactions

    def test_constructor__dependencies__immutable(self, tmp_path: Path) -> None:
        """Explicit serializer and bundle dependencies remain immutable.

        Evidence ID: SV-WFR-ENTRY-007

        Requirement: The service has no mutable winner cache or ambient codec selection.

        Method: Construct through both public imports and attempt field replacement.

        Oracle: Frozen dataclass semantics and exact exported class identity.

        Acceptance: Mutation raises FrozenInstanceError; wrong request raises TypeError.

        Interpretation: Explicit dependencies do not imply mutable entry permission.

        Limitations: Immutability does not establish a repository's runtime correctness.
        """
        from ksdft2effmass.workflows.control import WorkflowRunDispatchEntryCommitter

        assert WorkflowRunDispatchEntryCommitter is SUT
        repository, _, bundle = self.seed(tmp_path / "entry.sqlite3")
        service = SUT(
            repository=repository,
            serializer=repository.serializer,
            runtime_bundle=bundle,
        )
        with pytest.raises(FrozenInstanceError):
            service.runtime_bundle = bundle  # type: ignore[misc]
        with pytest.raises(TypeError):
            service.execute("request")  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "mode",
        [
            pytest.param("race", id="independent_process_race"),
            pytest.param("crash", id="crash_before_fake_effect"),
        ],
    )
    def test_method__execute__process_boundary(self, tmp_path: Path, mode: str) -> None:
        """Independent processes cannot resurrect lost effect-entry permission.

        Evidence ID: SV-WFR-ENTRY-008

        Requirement: A process race has one winner; death after entry leaves no
        retry permission.

        Method: Run local Python fixture workers with a precommit rendezvous or
        terminate after entry.

        Oracle: Fake effect marker count is one for race and zero for crash.

        Acceptance: Reopened repeat is already_entered and never creates another marker.

        Interpretation: Crash after commitment may leave an intentionally unrun effect.

        Limitations: Local fixture-process loss is not exactly-once completion or
        scientific validation.
        """
        path = tmp_path / "entry.sqlite3"
        self.seed(path)
        worker = (
            Path(__file__).parent.parent / "persistence/resources/entry-fault-worker.py"
        )
        # Resolving the venv interpreter's symlink loses its environment.
        interpreter = str(Path(__file__).parents[5] / ".venv/bin/python")
        count = 2 if mode == "race" else 1
        with ExitStack() as stack:
            workers = [
                self.start_worker(
                    stack, [interpreter, str(worker), str(path), mode, str(i)]
                )
                for i in range(count)
            ]
            observations = [p.communicate(timeout=30) for p in workers]
        if mode == "race":
            assert [p.returncode for p in workers] == [0, 0], observations
            assert sorted(out.strip() for out, _ in observations) == [
                "already_entered",
                "entered",
            ]
            assert len(tuple(tmp_path.glob("effect-*"))) == 1
        else:
            assert workers[0].returncode == 73, observations
            assert not tuple(tmp_path.glob("effect-*"))
        reopened = self.make_repository(path)
        request, bundle = self.recover(reopened)
        result = SUT(
            repository=reopened, serializer=reopened.serializer, runtime_bundle=bundle
        ).execute(request)
        assert result.kind.value == "already_entered" and result.receipt is None

    @classmethod
    def start_worker(
        cls, stack: ExitStack, command: list[str]
    ) -> subprocess.Popen[str]:
        """Register cleanup as soon as one isolated fixture process starts."""
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stack.callback(cls.stop_worker, process)
        return process

    @staticmethod
    def stop_worker(process: subprocess.Popen[str]) -> None:
        """Reap a fixture process and close its streams even after a timeout."""
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        if process.stdout is not None:
            process.stdout.close()
        if process.stderr is not None:
            process.stderr.close()

    @classmethod
    def run_worker(cls, path: Path, mode: str, identity: str) -> None:
        """Adapt the local fixture script to the same explicit public service."""
        import os

        repository = cls.make_repository(path)
        request, bundle = cls.recover(repository)
        probe = EntryRepositoryProbe(
            repository,
            rendezvous=path.parent if mode == "race" else None,
            participant=identity,
        )
        result = SUT(
            repository=probe, serializer=repository.serializer, runtime_bundle=bundle
        ).execute(request)
        if result.kind.value == "entered":
            if mode == "crash":
                os._exit(73)
            (path.parent / f"effect-{identity}").write_text(
                "synthetic effect entered\n"
            )
        print(result.kind.value, flush=True)
