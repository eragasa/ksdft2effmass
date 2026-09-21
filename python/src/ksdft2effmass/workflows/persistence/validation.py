"""Structural validation for complete WorkflowRun persistence transactions."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

from ksdft2effmass.workflows.runs.identities import (
    SimulationDispatchEntryIdentity,
)
from ksdft2effmass.workflows.runs.records import (
    NestedWorkflowInvocation,
    NestedWorkflowInvocationIntent,
    NestedWorkflowInvocationKind,
)

from ..runs.aggregate import WorkflowRun
from ..runs.replay import _WorkflowRunStructureValidator
from .records import (
    WorkflowPersistenceFailure,
    WorkflowPersistenceFailureCode,
    WorkflowRunSnapshot,
    WorkflowRunTransaction,
    WorkflowRunValidationResult,
)
from .serialization.run import WorkflowRunSerializer


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunTransactionValidator:
    """Validate exact candidate binding, retained closure and immutable extension.

    Parameters
    ----------
    serializer
        Exact immutable WorkflowRunSerializer with an explicit outward result codec.
        Wire mechanics and complete result-value equality remain serializer-owned.

    Notes
    -----
    Validation checks the same transaction/candidate, its schema/content labels,
    predecessor address and complete snapshot bytes, run-level correlations,
    contiguous zero-based transition order and retained predecessor-marking links.
    Collections extend by nominal identity; attempts and transitions retain sequence
    prefixes. Historical records and initial marking, Workflow/definition/runtime/
    schema/adapter identities remain byte-equivalent under the codec. This operation
    does not use NumPy-backed dataclass equality for historical comparison.
    Newly introduced dispatch entries must name this transaction's non-null
    predecessor and candidate revision; genesis entries are invalid. Historical
    entries retain their original introduction labels rather than being rebound
    to the current successor. A new nested intent introduces its membership,
    activation and STARTED group in this candidate revision. A new terminal
    observation requires its exact intent source in the actual predecessor and
    introduces its terminal attempt/outcome group atomically in this revision.
    Genesis observations and same-commit intent/terminal introduction are invalid.
    Historical intent and observations retain their original bytes and labels.

    Retained structural closure is distinct from computed replay equality. The
    current marking may remain replay-unequal. No transitions or authorization
    requests are evaluated, and no repository, native file or external effect is
    accessed. A supplied predecessor is an explicit input, not proof of storage.

    Raises
    ------
    TypeError
        The serializer is not its exact declared type.
    """

    serializer: WorkflowRunSerializer

    def __post_init__(self) -> None:
        """Require the explicit domain serializer dependency."""
        if type(self.serializer) is not WorkflowRunSerializer:
            raise TypeError("serializer must be WorkflowRunSerializer")

    def execute(
        self,
        transaction: WorkflowRunTransaction,
        predecessor: WorkflowRunSnapshot | None = None,
    ) -> WorkflowRunValidationResult:
        """Check a complete candidate against its explicitly addressed predecessor.

        Parameters
        ----------
        transaction
            Exact complete proposed transaction; its labels are never inferred.
        predecessor
            Exact historical snapshot for the expected predecessor, not latest.
            Required for a non-genesis transaction and prohibited for genesis.

        Returns
        -------
        WorkflowRunValidationResult
            Bound validated bytes on valid only. Invalid, incompatible and error
            preserve structured failures without a partial successful candidate.

        Raises
        ------
        TypeError
            A direct argument has the wrong exact semantic type.
        """
        if type(transaction) is not WorkflowRunTransaction:
            raise TypeError("transaction must be WorkflowRunTransaction")
        if predecessor is not None and type(predecessor) is not WorkflowRunSnapshot:
            raise TypeError("predecessor must be WorkflowRunSnapshot or None")
        try:
            return self._validate(transaction, predecessor)
        except MemoryError, RecursionError:
            code = WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT
        except Exception:
            code = WorkflowPersistenceFailureCode.CODEC_ERROR
        return self._reject(
            transaction, predecessor, "error", code, "validation did not complete"
        )

    def _validate(
        self,
        transaction: WorkflowRunTransaction,
        predecessor: WorkflowRunSnapshot | None,
    ) -> WorkflowRunValidationResult:
        run = transaction.candidate
        expected = transaction.expected_predecessor_revision_identity
        if transaction.schema_identity != "ksdft2effmass.workflow-run:1":
            return self._reject(
                transaction,
                predecessor,
                "incompatible",
                WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION,
                "transaction schema is not supported",
            )
        if (
            run.identity != transaction.run_identity
            or run.predecessor_revision_identity != expected
            or (expected is None) != (predecessor is None)
        ):
            return self._reject(
                transaction,
                predecessor,
                "invalid",
                WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                "candidate/run/predecessor slots do not agree",
            )
        encoded_result = self.serializer.serialize(run, transaction.binding)
        if encoded_result.status != "encoded":
            assert encoded_result.failure is not None
            return WorkflowRunValidationResult(
                status=encoded_result.status,
                transaction=transaction,
                predecessor=predecessor,
                failure=encoded_result.failure,
            )
        encoded = encoded_result.encoded
        assert encoded is not None
        if (
            transaction.schema_identity != encoded.schema_identity
            or transaction.content_identity != encoded.content_identity
        ):
            return self._reject(
                transaction,
                predecessor,
                "invalid",
                WorkflowPersistenceFailureCode.CONTENT_MISMATCH,
                "transaction labels do not bind the exact candidate bytes",
            )
        # Check structural links on the exact reconstructed candidate. Complete
        # equal-identity result content is bound by the codec, not NumPy dataclass
        # equality or a protocol-identity stand-in.
        decoded = self.serializer.deserialize(encoded.payload)
        if decoded.status != "decoded":
            assert decoded.failure is not None
            return WorkflowRunValidationResult(
                status="invalid" if decoded.status == "corrupt" else decoded.status,
                transaction=transaction,
                predecessor=predecessor,
                failure=decoded.failure,
            )
        assert decoded.run is not None
        issue = _WorkflowRunStructureValidator().execute(decoded.run)
        if issue is not None:
            return self._reject(
                transaction,
                predecessor,
                "invalid",
                WorkflowPersistenceFailureCode.INVARIANT_VIOLATION,
                issue.code.value + ": " + issue.diagnostic,
            )
        if predecessor is not None:
            old = predecessor.run
            revision = predecessor.revision
            if (
                old.identity != run.identity
                or old.revision_identity != expected
                or revision.stream_id != old.identity.value
                or revision.revision_id != old.revision_identity.value
                or revision.predecessor_revision_id
                != (
                    None
                    if old.predecessor_revision_identity is None
                    else old.predecessor_revision_identity.value
                )
            ):
                return self._reject(
                    transaction,
                    predecessor,
                    "invalid",
                    WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                    "predecessor snapshot does not name the exact expected revision",
                )
            old_encoded_result = self.serializer.serialize(old, predecessor.binding)
            if old_encoded_result.status != "encoded":
                assert old_encoded_result.failure is not None
                return WorkflowRunValidationResult(
                    status=old_encoded_result.status,
                    transaction=transaction,
                    predecessor=predecessor,
                    failure=old_encoded_result.failure,
                )
            old_encoded = old_encoded_result.encoded
            assert old_encoded is not None
            if (
                old_encoded.schema_identity != revision.schema_id
                or old_encoded.content_identity != revision.content_id
                or old_encoded.payload != revision.payload
            ):
                return self._reject(
                    transaction,
                    predecessor,
                    "invalid",
                    WorkflowPersistenceFailureCode.CONTENT_MISMATCH,
                    "predecessor snapshot differs from its exact revision bytes",
                )
            old_issue = _WorkflowRunStructureValidator().execute(old)
            if old_issue is not None:
                return self._reject(
                    transaction,
                    predecessor,
                    "invalid",
                    WorkflowPersistenceFailureCode.INVARIANT_VIOLATION,
                    "predecessor: "
                    + old_issue.code.value
                    + ": "
                    + old_issue.diagnostic,
                )
            projection = self._historical_projection(run, old)
            projection_result = self.serializer.serialize(
                projection, predecessor.binding
            )
            if projection_result.status != "encoded":
                assert projection_result.failure is not None
                return WorkflowRunValidationResult(
                    status=projection_result.status,
                    transaction=transaction,
                    predecessor=predecessor,
                    failure=projection_result.failure,
                )
            assert projection_result.encoded is not None
            if projection_result.encoded.payload != old_encoded.payload:
                return self._reject(
                    transaction,
                    predecessor,
                    "invalid",
                    WorkflowPersistenceFailureCode.INVARIANT_VIOLATION,
                    "candidate rewrites or removes immutable predecessor state",
                )
        historical_entry_ids: set[SimulationDispatchEntryIdentity] = (
            set()
            if predecessor is None
            else {entry.identity for entry in predecessor.run.dispatch_entries}
        )
        if any(
            entry.identity not in historical_entry_ids
            and (
                expected is None
                or entry.predecessor_revision_identity != expected
                or entry.committed_revision_identity != run.revision_identity
            )
            for entry in run.dispatch_entries
        ):
            return self._reject(
                transaction,
                predecessor,
                "invalid",
                WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                "new dispatch entry must name its committing predecessor and revision",
            )
        introduction_issue = self._nested_introduction_issue(
            run, None if predecessor is None else predecessor.run
        )
        if introduction_issue is not None:
            return self._reject(
                transaction,
                predecessor,
                "invalid",
                WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                introduction_issue,
            )
        return WorkflowRunValidationResult(
            status="valid",
            transaction=transaction,
            predecessor=predecessor,
            encoded=encoded,
        )

    @staticmethod
    def _nested_introduction_issue(
        run: WorkflowRun, old: WorkflowRun | None
    ) -> str | None:
        """Bind new intent and terminal groups to actual transaction history."""
        old_sources = {
            v.identity: v
            for v in (
                ()
                if old is None
                else old.nested_invocations + old.nested_invocation_intents
            )
        }
        old_attempts = {v.identity for v in (() if old is None else old.attempts)}
        old_activations = {v.identity for v in (() if old is None else old.activations)}
        old_memberships = {
            v.identity for v in (() if old is None else old.nested_memberships)
        }
        old_observations = {
            v.identity
            for v in (() if old is None else old.nested_terminal_observations)
        }
        old_outcomes = {v.identity for v in (() if old is None else old.outcomes)}
        memberships = {v.child_workflow_run_identity: v for v in run.nested_memberships}
        intent_sources = run.nested_invocation_intents + tuple(
            v
            for v in run.nested_invocations
            if v.kind is NestedWorkflowInvocationKind.PENDING
        )
        for source in intent_sources:
            if source.identity in old_sources:
                continue
            started_identity = (
                source.started_attempt_record_identity
                if isinstance(source, NestedWorkflowInvocationIntent)
                else source.attempt_record_identity
            )
            membership = memberships.get(source.child_workflow_run_identity)
            if (
                source.parent_revision_identity != run.revision_identity
                or source.activation_identity in old_activations
                or started_identity in old_attempts
                or membership is None
                or membership.identity in old_memberships
            ):
                return (
                    "new nested intent must introduce its membership, activation "
                    "and STARTED group in the candidate revision"
                )
        for observation in run.nested_terminal_observations:
            if observation.identity in old_observations:
                continue
            predecessor_source = old_sources.get(observation.intent_identity)
            if (
                predecessor_source is None
                or (
                    isinstance(predecessor_source, NestedWorkflowInvocation)
                    and predecessor_source.kind
                    is not NestedWorkflowInvocationKind.PENDING
                )
                or observation.parent_revision_identity != run.revision_identity
                or observation.terminal_attempt_record_identity in old_attempts
                or observation.outcome_identity in old_outcomes
            ):
                return (
                    "new nested observation requires an actual predecessor intent "
                    "and a new terminal group in the candidate revision"
                )
        return None

    @staticmethod
    def _historical_projection(run: WorkflowRun, old: WorkflowRun) -> WorkflowRun:
        """Select old identities from the candidate; serializer owns byte comparison."""
        return replace(
            run,
            revision_identity=old.revision_identity,
            predecessor_revision_identity=old.predecessor_revision_identity,
            current_marking=old.current_marking,
            attempts=run.attempts[: len(old.attempts)],
            transitions=run.transitions[: len(old.transitions)],
            task_instances=tuple(
                v
                for v in run.task_instances
                if v.identity in {o.identity for o in old.task_instances}
            ),
            task_memberships=tuple(
                v
                for v in run.task_memberships
                if v.identity in {o.identity for o in old.task_memberships}
            ),
            nested_memberships=tuple(
                v
                for v in run.nested_memberships
                if v.identity in {o.identity for o in old.nested_memberships}
            ),
            nested_invocations=tuple(
                v
                for v in run.nested_invocations
                if v.identity in {o.identity for o in old.nested_invocations}
            ),
            nested_invocation_intents=tuple(
                v
                for v in run.nested_invocation_intents
                if v.identity in {o.identity for o in old.nested_invocation_intents}
            ),
            nested_terminal_observations=tuple(
                v
                for v in run.nested_terminal_observations
                if v.identity in {o.identity for o in old.nested_terminal_observations}
            ),
            activations=tuple(
                v
                for v in run.activations
                if v.identity in {o.identity for o in old.activations}
            ),
            outcomes=tuple(
                v
                for v in run.outcomes
                if v.identity in {o.identity for o in old.outcomes}
            ),
            result_references=tuple(
                v
                for v in run.result_references
                if v.identity in {o.identity for o in old.result_references}
            ),
            result_productions=tuple(
                v
                for v in run.result_productions
                if v.identity in {o.identity for o in old.result_productions}
            ),
            native_output_admissions=tuple(
                v
                for v in run.native_output_admissions
                if v.identity in {o.identity for o in old.native_output_admissions}
            ),
            result_dependencies=tuple(
                v
                for v in run.result_dependencies
                if v.identity in {o.identity for o in old.result_dependencies}
            ),
            failures=tuple(
                v
                for v in run.failures
                if v.identity in {o.identity for o in old.failures}
            ),
            authorization_results=tuple(
                v
                for v in run.authorization_results
                if v.identity in {o.identity for o in old.authorization_results}
            ),
            authority_references=tuple(
                v
                for v in run.authority_references
                if v.grant_identity
                in {o.grant_identity for o in old.authority_references}
            ),
            execution_request_correlations=tuple(
                v
                for v in run.execution_request_correlations
                if v.identity
                in {o.identity for o in old.execution_request_correlations}
            ),
            authority_reservations=tuple(
                v
                for v in run.authority_reservations
                if v.identity in {o.identity for o in old.authority_reservations}
            ),
            dispatch_obligations=tuple(
                v
                for v in run.dispatch_obligations
                if v.identity in {o.identity for o in old.dispatch_obligations}
            ),
            dispatch_entries=tuple(
                v
                for v in run.dispatch_entries
                if v.identity in {o.identity for o in old.dispatch_entries}
            ),
            dispatch_observations=tuple(
                v
                for v in run.dispatch_observations
                if v.identity in {o.identity for o in old.dispatch_observations}
            ),
            dispatch_outcomes=tuple(
                v
                for v in run.dispatch_outcomes
                if v.identity in {o.identity for o in old.dispatch_outcomes}
            ),
            obligation_dispositions=tuple(
                v
                for v in run.obligation_dispositions
                if v.identity in {o.identity for o in old.obligation_dispositions}
            ),
            scientific_decision_requests=tuple(
                v
                for v in run.scientific_decision_requests
                if v.identity in {o.identity for o in old.scientific_decision_requests}
            ),
            scientific_decision_resolutions=tuple(
                v
                for v in run.scientific_decision_resolutions
                if v.identity
                in {o.identity for o in old.scientific_decision_resolutions}
            ),
        )

    @staticmethod
    def _reject(
        transaction: WorkflowRunTransaction,
        predecessor: WorkflowRunSnapshot | None,
        status: Literal["invalid", "incompatible", "error"],
        code: WorkflowPersistenceFailureCode,
        diagnostic: str,
    ) -> WorkflowRunValidationResult:
        return WorkflowRunValidationResult(
            status=status,
            transaction=transaction,
            predecessor=predecessor,
            failure=WorkflowPersistenceFailure(
                implementation_identity="ksdft2effmass.workflows.WorkflowRunTransactionValidator:1",
                phase="transaction_validation",
                code=code,
                input_identities=(
                    transaction.transaction_identity,
                    transaction.run_identity.value,
                    transaction.candidate.revision_identity.value,
                ),
                expected=(
                    "exact candidate binding and immutable closed predecessor extension"
                ),
                observed=code.value,
                diagnostic=diagnostic,
                claim_boundary=(
                    "structural software validation only; "
                    "no replay, stored presence or authority"
                ),
            ),
        )
