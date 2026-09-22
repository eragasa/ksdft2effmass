r"""Software verification of ``SimulationDispatchControlWorkflow``.

Evidence profile: routine

Bounded artifact scope: generic persisted reservation, claim, dispatch-entry, and
one-effect lifecycle composition.

Facet and represented meaning

The Workflow composes existing replay, authorization, repository, claim, dispatch,
and effect ports without issuing authority or retrying an operation.

Intrinsic and cross-object scope

Tests cover one complete synthetic dispatch and claim-phase denial after reservation.
Calculator adaptation, result ingress, CPN result firing, and scientific interpretation
remain separately owned.

VVUQ and scientific exclusions

All state and effects are synthetic test data. No external executable is invoked, and
the tests establish no numerical verification, scientific validation, uncertainty
quantification, production authority, or human acceptance.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass.analysis import QuantityOfInterestResultValueSerializer
from ksdft2effmass.application import ApplicationResultValueSerializer
from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoResultValueSerializer,
)
from ksdft2effmass.persistence import SQLiteAtomicRevisionStore
from ksdft2effmass.workflows import (
    AuthorityReservationOutcomeIdentity,
    ScientificExecutionGrantState,
    SimulationDispatchAdapterResult,
    SimulationDispatchAdapterResultKind,
    SimulationDispatchEntryIdentity,
    SimulationDispatchOutcomeIdentity,
    SimulationExecutionAuthorizationPhase,
    SimulationExecutionAuthorizer,
    WorkflowResultValueSerializer,
    WorkflowRunAtomicRepository,
    WorkflowRunCommitBinding,
    WorkflowRunRevisionIdentity,
    WorkflowRunSerializer,
    WorkflowRunTransaction,
    WorkflowRunTransactionValidator,
)
from ksdft2effmass.workflows.control.lifecycle import (
    SimulationDispatchControlFailure,
    SimulationDispatchControlFailureStage,
    SimulationDispatchControlRequest,
    SimulationDispatchControlWorkflow,
)

from .resources.scenarios import (
    ControlScenarioFactory,
    RecordingSimulationDispatchEffect,
)
from .test__SimulationDispatchPreparer import (
    TestSimulationDispatchPreparer as PreparationEvidenceFactory,
)

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchControlWorkflow


class TestSimulationDispatchControlWorkflow:
    """Own lifecycle-composition software evidence."""

    @staticmethod
    def serializer() -> WorkflowRunSerializer:
        """Evidence ID: This helper owns no identifier.

        Requirement: Construct this module's exact serializer dependency.

        Acceptance: The serializer supports the QE ResultObject value codec.
        """
        quantum_espresso_codec = QuantumEspressoResultValueSerializer()
        return WorkflowRunSerializer(
            result_codec=ApplicationResultValueSerializer(
                workflow_codec=WorkflowResultValueSerializer(
                    source_codec=quantum_espresso_codec
                ),
                quantum_espresso_codec=quantum_espresso_codec,
                quantity_of_interest_codec=QuantityOfInterestResultValueSerializer(),
            )
        )

    @classmethod
    def repository(
        cls, path: Path
    ) -> tuple[WorkflowRunAtomicRepository, WorkflowRunSerializer]:
        """Evidence ID: This helper owns no identifier.

        Requirement: Construct an isolated exact WorkflowRun repository.

        Acceptance: Repository and validator share one serializer instance.
        """
        serializer = cls.serializer()
        return (
            WorkflowRunAtomicRepository(
                store=SQLiteAtomicRevisionStore(
                    path,
                    busy_timeout_ms=5_000,
                    max_payload_bytes=1_048_576,
                ),
                serializer=serializer,
                validator=WorkflowRunTransactionValidator(serializer=serializer),
            ),
            serializer,
        )

    @staticmethod
    def control_request() -> SimulationDispatchControlRequest:
        """Evidence ID: This helper owns no identifier.

        Requirement: Construct one exact synthetic lifecycle request.

        Acceptance: Every revision and persistence binding is distinct.
        """
        preparation = PreparationEvidenceFactory.make_request()
        return SimulationDispatchControlRequest(
            preparation_request=preparation,
            preparation_commit_binding=WorkflowRunCommitBinding(
                transaction_identity="transaction.prepared",
                commit_idempotency_identity="commit.prepared",
                persistence_implementation_identity=(
                    "ksdft2effmass.workflows.WorkflowRunAtomicRepository:1"
                ),
            ),
            claim_authorization_request=(
                ControlScenarioFactory.authorization_request(
                    phase=SimulationExecutionAuthorizationPhase.CLAIM,
                    state=ScientificExecutionGrantState.RESERVED,
                    result_identity="authorization.claim",
                    input_result_reference_identities=(),
                )
            ),
            claim_revision_identity=WorkflowRunRevisionIdentity("revision.claimed"),
            claimed_reservation_identity=AuthorityReservationOutcomeIdentity(
                "claim.one"
            ),
            claim_commit_binding=WorkflowRunCommitBinding(
                transaction_identity="transaction.claimed",
                commit_idempotency_identity="commit.claimed",
                persistence_implementation_identity=(
                    "ksdft2effmass.workflows.WorkflowRunAtomicRepository:1"
                ),
            ),
            dispatch_outcome_identity=SimulationDispatchOutcomeIdentity("outcome.one"),
            dispatch_entry_identity=SimulationDispatchEntryIdentity("entry.one"),
            dispatch_entry_revision_identity=WorkflowRunRevisionIdentity(
                "revision.dispatch-entered"
            ),
        )

    @staticmethod
    def commit_predecessor(
        repository: WorkflowRunAtomicRepository,
        serializer: WorkflowRunSerializer,
        request: SimulationDispatchControlRequest,
    ) -> None:
        """Evidence ID: This helper owns no identifier.

        Requirement: Persist the request's exact genesis predecessor.

        Acceptance: The isolated repository acknowledges the exact revision.
        """
        predecessor = request.preparation_request.predecessor_run
        binding = WorkflowRunCommitBinding(
            transaction_identity="transaction.genesis",
            commit_idempotency_identity="commit.genesis",
            persistence_implementation_identity=(
                "ksdft2effmass.workflows.WorkflowRunAtomicRepository:1"
            ),
        )
        encoded = serializer.serialize(predecessor, binding)
        assert encoded.encoded is not None
        result = repository.commit(
            WorkflowRunTransaction(
                binding=binding,
                run_identity=predecessor.identity,
                expected_predecessor_revision_identity=None,
                candidate=predecessor,
                schema_identity=encoded.encoded.schema_identity,
                content_identity=encoded.encoded.content_identity,
            )
        )
        assert result.status == "committed"

    def test_method__execute__persists_claim_and_enters_effect_once(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-WFC-DISPATCH-CONTROL-001

        Requirement: One exact authorized lifecycle must persist reservation, claim,
        and dispatch entry before entering its matching effect exactly once.

        Method: Commit a replay-equal genesis run, execute one synthetic lifecycle,
        and observe the recording effect.

        Oracle: Repository-owned claim receipt and dispatch-entry gates plus the
        recording effect's exact call count.

        Acceptance: Dispatch is confirmed and the effect observes exactly one call.

        Interpretation: Claim evidence alone does not bypass durable dispatch entry.

        Limitations: The effect is synthetic and result ingress is not exercised.
        """
        request = self.control_request()
        repository, serializer = self.repository(tmp_path / "workflow.sqlite")
        self.commit_predecessor(repository, serializer, request)
        effect = RecordingSimulationDispatchEffect(
            executor_identity=ControlScenarioFactory.outcome().executor_identity,
            outcome=ControlScenarioFactory.outcome(),
        )
        workflow = SUT(
            repository=repository,
            serializer=serializer,
            runtime_bundle=request.preparation_request.runtime_bundle,
            authorizer=SimulationExecutionAuthorizer(),
            effect=effect,
        )

        result = workflow.execute(request)

        assert type(result) is SimulationDispatchAdapterResult
        assert result.kind is SimulationDispatchAdapterResultKind.DISPATCHED
        assert result.effect_invoked is True
        assert effect.call_count == 1

    def test_method__execute__stale_claim_authority_stops_after_reservation(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-WFC-DISPATCH-CONTROL-002

        Requirement: Stale claim authority must produce no claim commit, dispatch
        entry, or effect even after reservation was committed.

        Method: Move only claim evaluation beyond the snapshot freshness bound.

        Oracle: The claim preparer's closed denial and recording effect call count.

        Acceptance: The result identifies claim-stage failure and effect count zero.

        Interpretation: A committed reservation does not confer later effect authority.

        Limitations: Conflict and persistence-fault branches remain separately owned.
        """
        request = self.control_request()
        request = replace(
            request,
            claim_authorization_request=replace(
                request.claim_authorization_request,
                evaluated_at=ControlScenarioFactory.instant(4),
            ),
        )
        repository, serializer = self.repository(tmp_path / "workflow.sqlite")
        self.commit_predecessor(repository, serializer, request)
        effect = RecordingSimulationDispatchEffect(
            executor_identity=ControlScenarioFactory.outcome().executor_identity,
            outcome=ControlScenarioFactory.outcome(),
        )
        workflow = SUT(
            repository=repository,
            serializer=serializer,
            runtime_bundle=request.preparation_request.runtime_bundle,
            authorizer=SimulationExecutionAuthorizer(),
            effect=effect,
        )

        result = workflow.execute(request)

        assert type(result) is SimulationDispatchControlFailure
        assert result.stage is SimulationDispatchControlFailureStage.CLAIM
        assert effect.call_count == 0
