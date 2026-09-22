r"""Software verification of ``WorkflowRunValidationResult``.

Bounded artifact scope: immutable transaction-bound closed validation outcomes.

Evidence profile: claim_bearing

Facet and represented meaning

The result retains the exact transaction and predecessor inputs. Valid alone carries
encoded bytes; every nonsuccess carries a structured diagnostic without partial bytes.

Intrinsic and cross-object scope

Intrinsic record invariants are the sole claim. Fixed genesis bytes provide a literal
content binding; constructing the result does not execute the validator or repository.

VVUQ and scientific exclusions

Synthetic software verification only, not replay, stored presence, authority or science.
"""

from dataclasses import FrozenInstanceError, replace
from typing import Literal

import pytest

from ksdft2effmass import workflows as w
from ksdft2effmass.workflows import WorkflowRunValidationResult

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunValidationResult


class TestWorkflowRunValidationResult:
    """Closed validation record variants, not action or storage evidence."""

    @staticmethod
    def make_encoded(snapshot: w.WorkflowRunSnapshot) -> w.WorkflowEncodedRun:
        return w.WorkflowEncodedRun(
            schema_identity=snapshot.revision.schema_id,
            content_identity=snapshot.revision.content_id,
            payload=snapshot.revision.payload,
        )

    def test_constructor__valid__retains_exact_inputs(
        self,
        genesis_transaction: w.WorkflowRunTransaction,
        genesis_snapshot: w.WorkflowRunSnapshot,
    ) -> None:
        """Evidence ID: SV-WFR-VALIDATION-RESULT-001

        Requirement: Valid records bind the exact transaction and encoded
        representation.

        Method: Construct from explicit independent genesis bytes and inspect fields.

        Oracle: Supplied exact transaction, snapshot and byte envelope identities.

        Acceptance: Inputs retained by identity with no failure and frozen fields.

        Interpretation: Intrinsic representation of successful evidence, not execution.

        Limitations: Constructor does not verify that validation actually occurred.
        """
        encoded = self.make_encoded(genesis_snapshot)
        result = SUT(
            status="valid",
            transaction=genesis_transaction,
            predecessor=genesis_snapshot,
            encoded=encoded,
        )
        assert result.transaction is genesis_transaction
        assert result.predecessor is genesis_snapshot
        assert result.encoded is encoded and result.failure is None
        with pytest.raises(FrozenInstanceError):
            result.encoded = encoded  # type: ignore[misc]

    @pytest.mark.parametrize(
        "status",
        [
            pytest.param("invalid", id="invalid_candidate"),
            pytest.param("incompatible", id="unsupported_version"),
            pytest.param("error", id="operation_error"),
        ],
    )
    def test_constructor__nonsuccess__retains_failure_only(
        self,
        genesis_transaction: w.WorkflowRunTransaction,
        record_failure: w.WorkflowPersistenceFailure,
        status: Literal["invalid", "incompatible", "error"],
    ) -> None:
        """Evidence ID: SV-WFR-VALIDATION-RESULT-002

        Requirement: Every nonsuccess records failure without encoded success bytes.

        Method: Construct each closed failure variant with an exact diagnostic.

        Oracle: Explicit valid/invalid/incompatible/error variant contract.

        Acceptance: Failure and transaction retained by identity; no encoded candidate.

        Interpretation: Failure cannot appear as a partial validated candidate.

        Limitations: Diagnostic truth and status selection belong to the validator.
        """
        result = SUT(
            status=status, transaction=genesis_transaction, failure=record_failure
        )
        assert (
            result.transaction is genesis_transaction
            and result.failure is record_failure
        )
        assert result.encoded is None and result.predecessor is None

    @pytest.mark.parametrize(
        "mutation",
        [
            pytest.param("success_without_bytes", id="valid_without_candidate_bytes"),
            pytest.param("success_with_failure", id="valid_with_failure"),
            pytest.param("failure_with_bytes", id="invalid_with_candidate_bytes"),
            pytest.param("failure_without_diagnostic", id="error_without_failure"),
            pytest.param("content", id="detached_transaction_content"),
            pytest.param("schema", id="detached_transaction_schema"),
        ],
    )
    def test_constructor__variants__rejects_inconsistent_values(
        self,
        genesis_transaction: w.WorkflowRunTransaction,
        genesis_snapshot: w.WorkflowRunSnapshot,
        record_failure: w.WorkflowPersistenceFailure,
        mutation: str,
    ) -> None:
        """Evidence ID: SV-WFR-VALIDATION-RESULT-003

        Requirement: Status closure and encoded transaction labels cannot disagree.

        Method: Replace one field on a fixed valid record or its failure counterpart.

        Oracle: Exact variant and content/schema binding rules.

        Acceptance: ValueError for each intrinsically inconsistent record.

        Interpretation: Merely supplying both data and failure cannot create success.

        Limitations: Complete candidate-byte comparison remains an ActionObject
        operation.
        """
        valid = SUT(
            status="valid",
            transaction=genesis_transaction,
            encoded=self.make_encoded(genesis_snapshot),
        )
        with pytest.raises(ValueError):
            if mutation == "success_without_bytes":
                replace(valid, encoded=None)
            elif mutation == "success_with_failure":
                replace(valid, failure=record_failure)
            elif mutation == "failure_with_bytes":
                replace(valid, status="invalid", failure=record_failure)
            elif mutation == "failure_without_diagnostic":
                replace(valid, status="error", encoded=None)
            elif mutation == "content":
                replace(
                    valid,
                    transaction=replace(genesis_transaction, content_identity="other"),
                )
            else:
                replace(
                    valid,
                    transaction=replace(genesis_transaction, schema_identity="other"),
                )

    def test_constructor__status__rejects_unknown(
        self,
        genesis_transaction: w.WorkflowRunTransaction,
    ) -> None:
        """Evidence ID: SV-WFR-VALIDATION-RESULT-005

        Requirement: Validation status has a closed string vocabulary.

        Method: Supply loaded, a read status rather than a validation status.

        Oracle: Exactly valid, invalid, incompatible and error are supported.

        Acceptance: ValueError for the unknown string.

        Interpretation: Unknown accepted-type values differ from wrong semantic types.

        Limitations: Operation status selection belongs to the validator.
        """
        with pytest.raises(ValueError):
            SUT(status="loaded", transaction=genesis_transaction)  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "field",
        [
            pytest.param("status", id="boolean_status"),
            pytest.param("transaction", id="identity_without_transaction"),
            pytest.param("predecessor", id="identity_without_snapshot"),
            pytest.param("encoded", id="payload_without_envelope"),
            pytest.param("failure", id="text_without_diagnostic_record"),
        ],
    )
    def test_constructor__types__rejects_wrong_semantic_fields(
        self,
        genesis_transaction: w.WorkflowRunTransaction,
        genesis_snapshot: w.WorkflowRunSnapshot,
        field: str,
    ) -> None:
        """Evidence ID: SV-WFR-VALIDATION-RESULT-004

        Requirement: Validation fields retain exact declared semantic record types.

        Method: Substitute one explicit wrong-type scalar at each field boundary.

        Oracle: Exact public field types, without coercion or identity-only stand-ins.

        Acceptance: TypeError at each invalid construction.

        Interpretation: Closed statuses do not erase concrete domain boundaries.

        Limitations: The finite cases do not enumerate arbitrary Python objects.
        """
        valid = SUT(
            status="valid",
            transaction=genesis_transaction,
            encoded=self.make_encoded(genesis_snapshot),
        )
        with pytest.raises(TypeError):
            if field == "status":
                replace(valid, status=True)  # type: ignore[arg-type]
            elif field == "transaction":
                replace(valid, transaction="transaction")  # type: ignore[arg-type]
            elif field == "predecessor":
                replace(valid, predecessor="predecessor")  # type: ignore[arg-type]
            elif field == "encoded":
                replace(valid, encoded=b"payload")  # type: ignore[arg-type]
            else:
                replace(valid, failure="failure")  # type: ignore[arg-type]
