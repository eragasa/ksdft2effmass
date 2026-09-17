"""Pytest-owned shared persistence inputs and isolated claim-store lifecycles.

Synthetic genesis contains all 34 WorkflowRun fields and no history, rather than a
partial-run adapter. The fixed envelope was authored independently as record input;
the serializer's separate tests now also verify its exact genesis wire agreement.
Genesis fixtures construct records only. Claim fixtures commit literal histories to
an isolated SQLite store and reopen it for reconciliation; no scientific tool runs.
"""

import hashlib
from pathlib import Path

import pytest
from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoResultValueSerializer,
)
from ksdft2effmass.persistence import (
    Revision,
    RevisionReadRequest,
    RevisionReadResult,
    RevisionReadStatus,
    RevisionSelector,
    SQLiteAtomicRevisionStore,
)
from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetDefinitionIdentity,
    ColoredPetriNetMarking,
    ColoredPetriNetMarkingIdentity,
)
from ksdft2effmass.workflows import (
    AuthorityReservationOutcomeIdentity,
    WorkflowDefinitionReferenceIdentity,
    WorkflowIdentity,
    WorkflowPersistenceFailure,
    WorkflowPersistenceFailureCode,
    WorkflowResultValueSerializer,
    WorkflowRun,
    WorkflowRunAtomicRepository,
    WorkflowRunClaimLoadResult,
    WorkflowRunCommitBinding,
    WorkflowRunIdentity,
    WorkflowRunLoadResult,
    WorkflowRunRevisionIdentity,
    WorkflowRunSerializer,
    WorkflowRunSnapshot,
    WorkflowRuntimeBundleIdentity,
    WorkflowRunTransaction,
    WorkflowRunTransactionValidator,
    WorkflowRunWriteResult,
)


@pytest.fixture
def genesis_run() -> WorkflowRun:
    """Provide genuinely shared complete immutable genesis state through pytest."""
    marking = ColoredPetriNetMarking(
        identity=ColoredPetriNetMarkingIdentity("initial"),
        definition_identity=ColoredPetriNetDefinitionIdentity("definition"),
        places=(),
    )
    return WorkflowRun(
        identity=WorkflowRunIdentity("run"),
        revision_identity=WorkflowRunRevisionIdentity("genesis"),
        predecessor_revision_identity=None,
        workflow_identity=WorkflowIdentity("workflow"),
        definition_reference_identity=WorkflowDefinitionReferenceIdentity(
            "definition-reference"
        ),
        runtime_bundle_identity=WorkflowRuntimeBundleIdentity("runtime"),
        schema_version=1,
        adapter_implementation_identity="fixture-adapter:1",
        task_instances=(),
        task_memberships=(),
        nested_memberships=(),
        nested_invocations=(),
        activations=(),
        attempts=(),
        outcomes=(),
        result_references=(),
        result_productions=(),
        native_output_admissions=(),
        result_dependencies=(),
        failures=(),
        authorization_results=(),
        authority_references=(),
        execution_request_correlations=(),
        authority_reservations=(),
        dispatch_obligations=(),
        dispatch_entries=(),
        dispatch_observations=(),
        dispatch_outcomes=(),
        obligation_dispositions=(),
        scientific_decision_requests=(),
        scientific_decision_resolutions=(),
        initial_marking=marking,
        current_marking=marking,
        transitions=(),
    )


@pytest.fixture
def genesis_snapshot(genesis_run: WorkflowRun) -> WorkflowRunSnapshot:
    """Retain a fixed complete envelope as shared record input, not load evidence."""
    return WorkflowRunSnapshot(
        run=genesis_run,
        binding=WorkflowRunCommitBinding(
            transaction_identity="genesis-transaction",
            commit_idempotency_identity="genesis-key",
            persistence_implementation_identity="ksdft2effmass.workflows.WorkflowRunAtomicRepository:1",
        ),
        revision=Revision(
            stream_id="run",
            revision_id="genesis",
            predecessor_revision_id=None,
            schema_id="ksdft2effmass.workflow-run:1",
            content_id="ksdft2effmass.workflow-run:1:sha256:760cd93744b80ecdefd7fccb0bf0b3145dcc7cd794113154411c626fcd77f456",
            payload=(
                Path(__file__).parent / "resources/genesis-record-envelope.json"
            ).read_bytes(),
        ),
    )


@pytest.fixture
def genesis_transaction(
    genesis_snapshot: WorkflowRunSnapshot,
) -> WorkflowRunTransaction:
    """Adapt the same complete immutable inputs for shared transaction tests."""
    return WorkflowRunTransaction(
        binding=genesis_snapshot.binding,
        run_identity=WorkflowRunIdentity("run"),
        expected_predecessor_revision_identity=None,
        candidate=genesis_snapshot.run,
        schema_identity="ksdft2effmass.workflow-run:1",
        content_identity=genesis_snapshot.revision.content_id,
    )


@pytest.fixture
def persisted_claim_write(tmp_path: Path) -> WorkflowRunWriteResult:
    """Manage a genuinely shared isolated real SQLite claim for record evidence."""
    serializer = WorkflowRunSerializer(
        result_codec=WorkflowResultValueSerializer(
            source_codec=QuantumEspressoResultValueSerializer()
        )
    )
    repository = WorkflowRunAtomicRepository(
        store=SQLiteAtomicRevisionStore(
            tmp_path / "claim.sqlite3", busy_timeout_ms=1000, max_payload_bytes=1048576
        ),
        serializer=serializer,
        validator=WorkflowRunTransactionValidator(serializer=serializer),
    )
    result: WorkflowRunWriteResult | None = None
    for name in (
        "genesis-record-envelope.json",
        "prepared-run-v1.json",
        "claim-receipt-v1.json",
    ):
        payload = Path(__file__).with_name("resources").joinpath(name).read_bytes()
        decoded = serializer.deserialize(payload)
        assert decoded.run is not None and decoded.binding is not None
        result = repository.commit(
            WorkflowRunTransaction(
                binding=decoded.binding,
                run_identity=decoded.run.identity,
                expected_predecessor_revision_identity=decoded.run.predecessor_revision_identity,
                candidate=decoded.run,
                schema_identity="ksdft2effmass.workflow-run:1",
                content_identity="ksdft2effmass.workflow-run:1:sha256:"
                + hashlib.sha256(payload).hexdigest(),
            )
        )
        assert result.status == "committed", result.failure
    assert result is not None
    return result


@pytest.fixture
def persisted_claim_load(
    tmp_path: Path,
    persisted_claim_write: WorkflowRunWriteResult,
) -> WorkflowRunClaimLoadResult:
    """Reopen the shared test-managed database and confirm the historical claim."""
    snapshot = persisted_claim_write.snapshot
    assert snapshot is not None
    serializer = WorkflowRunSerializer(
        result_codec=WorkflowResultValueSerializer(
            source_codec=QuantumEspressoResultValueSerializer()
        )
    )
    repository = WorkflowRunAtomicRepository(
        store=SQLiteAtomicRevisionStore(
            tmp_path / "claim.sqlite3", busy_timeout_ms=1000, max_payload_bytes=1048576
        ),
        serializer=serializer,
        validator=WorkflowRunTransactionValidator(serializer=serializer),
    )
    result = repository.load_claim(
        RevisionReadRequest(
            request_id="record-claim-read",
            stream_id="run",
            selector=RevisionSelector.EXPLICIT_REVISION,
            revision_id="claimed",
            expected_predecessor_revision_id="prepared",
            expected_schema_id=snapshot.revision.schema_id,
            expected_content_id=snapshot.revision.content_id,
            expected_idempotency_id="claimed-key",
        ),
        AuthorityReservationOutcomeIdentity("claimed"),
    )
    assert result.status == "loaded", result.failure
    return result


@pytest.fixture
def record_failure() -> WorkflowPersistenceFailure:
    """Provide fixed sanitized domain failure evidence across variant tests."""
    return WorkflowPersistenceFailure(
        implementation_identity="fixture-persistence:1",
        phase="fixture",
        code=WorkflowPersistenceFailureCode.INVARIANT_VIOLATION,
        input_identities=("run",),
        expected="complete representation",
        observed="fixture rejection",
        diagnostic="synthetic record test",
        claim_boundary="record construction only; no stored presence or authority",
    )


@pytest.fixture
def genesis_load(genesis_snapshot: WorkflowRunSnapshot) -> WorkflowRunLoadResult:
    """Supply explicit FOUND-shaped records, not an executed repository load."""
    request = RevisionReadRequest(
        request_id="read",
        stream_id="run",
        selector=RevisionSelector.LATEST,
    )
    return WorkflowRunLoadResult(
        status="loaded",
        request=request,
        snapshot=genesis_snapshot,
        store_result=RevisionReadResult(
            result_id="read-result",
            request_id="read",
            stream_id="run",
            selector=RevisionSelector.LATEST,
            store_implementation_id="fixture-store",
            store_version_id="fixture:1",
            status=RevisionReadStatus.FOUND,
            diagnostics=(),
            claim_boundary="supplied record evidence; not a real store observation",
            revision=genesis_snapshot.revision,
        ),
    )
