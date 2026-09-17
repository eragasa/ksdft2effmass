r"""Software verification of ``WorkflowRunTransaction``.

Bounded artifact scope: immutable complete candidate and durable transaction labels.

Evidence profile: claim_bearing

Facet and represented meaning

The transaction retains a candidate, predecessor slot and one binding owner.

Intrinsic and cross-object scope

Intrinsic type/label checks only; append-only and byte correlations are validator work.

VVUQ and scientific exclusions

Software verification of synthetic genesis, not a commit, authority or science.
"""

from dataclasses import FrozenInstanceError, replace

import pytest
from ksdft2effmass.workflows import (
    WorkflowRunIdentity,
    WorkflowRunSnapshot,
    WorkflowRunTransaction,
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunTransaction


class TestWorkflowRunTransaction:
    """Intrinsic transaction boundary without hidden validation or I/O."""

    def test_constructor__fields__preserves_complete_inputs(
        self,
        genesis_transaction: WorkflowRunTransaction,
        genesis_snapshot: WorkflowRunSnapshot,
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-001

        Requirement: The transaction retains complete candidate and exact labels.

        Method: Inspect the explicit shared genesis transaction inputs.

        Oracle: Fixed complete genesis records and independent literal labels.

        Acceptance: Candidate/binding are retained and every correlation field matches.

        Interpretation: Construction establishes no successful validation or commit.

        Limitations: Nontrivial history and candidate-byte closure are not exercised.
        """
        value = genesis_transaction
        assert value.candidate is genesis_snapshot.run
        assert value.binding is genesis_snapshot.binding
        assert value.run_identity == WorkflowRunIdentity("run")
        assert value.expected_predecessor_revision_identity is None
        assert value.schema_identity == "ksdft2effmass.workflow-run:1"
        assert value.content_identity == genesis_snapshot.revision.content_id

    def test_property__binding_labels__has_one_owner(
        self, genesis_transaction: WorkflowRunTransaction
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-002

        Requirement: Operation and commit-key properties derive from the sole binding.

        Method: Replace the immutable binding with independently named labels.

        Oracle: Explicit replacement labels rather than duplicated transaction fields.

        Acceptance: Both properties expose the new binding and original is unchanged.

        Interpretation: Independent duplicate label inputs cannot silently diverge.

        Limitations: Shared-store confirmation of the key remains repository work.
        """
        value = replace(
            genesis_transaction,
            binding=replace(
                genesis_transaction.binding,
                transaction_identity="operation-two",
                commit_idempotency_identity="key-two",
            ),
        )
        assert value.transaction_identity == "operation-two"
        assert value.commit_idempotency_identity == "key-two"
        assert genesis_transaction.transaction_identity == "genesis-transaction"
        assert genesis_transaction.commit_idempotency_identity == "genesis-key"

    @pytest.mark.parametrize(
        "field",
        [
            pytest.param("binding", id="identity_without_binding"),
            pytest.param("run_identity", id="string_without_nominal_run"),
            pytest.param("predecessor", id="string_without_nominal_revision"),
            pytest.param("candidate", id="identity_without_complete_candidate"),
            pytest.param("schema", id="boolean_schema_label"),
            pytest.param("content", id="bytes_content_label"),
        ],
    )
    def test_constructor__types__rejects_wrong_fields(
        self, genesis_transaction: WorkflowRunTransaction, field: str
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-003

        Requirement: Every transaction field has its exact declared semantic type.

        Method: Replace one field with a closed explicit wrong-type value.

        Oracle: Exact nominal and complete concrete record contracts.

        Acceptance: Each wrong semantic type raises TypeError.

        Interpretation: No identity-only candidate or string coercion is accepted.

        Limitations: Arbitrary Python object types are not exhaustively enumerated.
        """
        with pytest.raises(TypeError):
            if field == "binding":
                replace(genesis_transaction, binding="binding")  # type: ignore[arg-type]
            elif field == "run_identity":
                replace(genesis_transaction, run_identity="run")  # type: ignore[arg-type]
            elif field == "predecessor":
                replace(
                    genesis_transaction,
                    expected_predecessor_revision_identity="previous",  # type: ignore[arg-type]
                )
            elif field == "candidate":
                replace(genesis_transaction, candidate=WorkflowRunIdentity("run"))  # type: ignore[arg-type]
            elif field == "schema":
                replace(genesis_transaction, schema_identity=True)  # type: ignore[arg-type]
            else:
                replace(genesis_transaction, content_identity=b"content")  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "field",
        [
            pytest.param("schema", id="empty_schema"),
            pytest.param("content", id="empty_content"),
        ],
    )
    def test_constructor__labels__rejects_empty(
        self, genesis_transaction: WorkflowRunTransaction, field: str
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-004

        Requirement: Representation labels are required nonempty strings.

        Method: Empty each label independently on an otherwise valid transaction.

        Oracle: Intrinsic schema/content nonempty-label invariant.

        Acceptance: Each empty label raises ValueError.

        Interpretation: Empty labels are not inferred from ambient state.

        Limitations: Recognizing versions and verifying content are separate actions.
        """
        with pytest.raises(ValueError):
            if field == "schema":
                replace(genesis_transaction, schema_identity="")
            else:
                replace(genesis_transaction, content_identity="")

    def test_field__candidate__is_immutable(
        self, genesis_transaction: WorkflowRunTransaction
    ) -> None:
        """Evidence ID: SV-WFR-TRANSACTION-005

        Requirement: A transaction's complete candidate is operationally immutable.

        Method: Attempt direct candidate assignment on the frozen transaction.

        Oracle: Frozen dataclass semantics and original candidate identity.

        Acceptance: Assignment raises FrozenInstanceError and candidate is retained.

        Interpretation: Commit callers cannot rewrite this transaction in place.

        Limitations: No concurrency or shared-store behavior is established.
        """
        candidate = genesis_transaction.candidate
        with pytest.raises(FrozenInstanceError):
            genesis_transaction.candidate = candidate  # type: ignore[misc]
        assert genesis_transaction.candidate is candidate
