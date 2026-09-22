r"""Software verification of ``WorkflowRunEncodeResult``.

Bounded artifact scope: closed aggregate encoding-result variants.

Evidence profile: claim_bearing

Facet and represented meaning

Success alone retains a complete immutable encoded run; failures retain evidence.

Intrinsic and cross-object scope

Constructor closure only, without invoking a serializer or repository.

VVUQ and scientific exclusions

Software verification only; no scientific validity or stored presence is claimed.
"""

from dataclasses import FrozenInstanceError, replace
from typing import Literal

import pytest

from ksdft2effmass.workflows import (
    WorkflowEncodedRun,
    WorkflowPersistenceFailure,
    WorkflowRunEncodeResult,
    WorkflowRunSnapshot,
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunEncodeResult


class TestWorkflowRunEncodeResult:
    """Complete bytes or complete failure, never both."""

    @staticmethod
    def make_encoded(snapshot: WorkflowRunSnapshot) -> WorkflowEncodedRun:
        return WorkflowEncodedRun(
            schema_identity=snapshot.revision.schema_id,
            content_identity=snapshot.revision.content_id,
            payload=snapshot.revision.payload,
        )

    def test_constructor__encoded__retains_envelope(
        self, genesis_snapshot: WorkflowRunSnapshot
    ) -> None:
        """Evidence ID: SV-WFR-RUN-ENCODE-001

        Requirement: Encoded success retains the complete supplied envelope.

        Method: Construct success from the fixed complete genesis byte fixture.

        Oracle: Exact input envelope and closed encoded-result field contract.

        Acceptance: Encoded field is the input and failure is None.

        Interpretation: This is variant construction, not serialization execution.

        Limitations: No run traversal or domain closure is claimed.
        """
        envelope = self.make_encoded(genesis_snapshot)
        value = WorkflowRunEncodeResult(status="encoded", encoded=envelope)
        assert value.status == "encoded"
        assert value.encoded is envelope
        assert value.failure is None

    @pytest.mark.parametrize(
        "status",
        [
            pytest.param("incompatible", id="unsupported_representation"),
            pytest.param("invalid", id="invalid_candidate"),
            pytest.param("error", id="operation_failure"),
        ],
    )
    def test_constructor__nonsuccess__preserves_failure(
        self,
        status: Literal["incompatible", "invalid", "error"],
        record_failure: WorkflowPersistenceFailure,
    ) -> None:
        """Evidence ID: SV-WFR-RUN-ENCODE-002

        Requirement: Every encode nonsuccess retains evidence and no bytes.

        Method: Construct each named nonsuccess with exact supplied failure.

        Oracle: Reviewed closed encode status vocabulary and field closure.

        Acceptance: Status and complete failure are retained; encoded is None.

        Interpretation: Distinct failure statuses are not collapsed into success.

        Limitations: Codec failure classification is outside the result record.
        """
        value = WorkflowRunEncodeResult(status=status, failure=record_failure)
        assert value.status == status
        assert value.failure is record_failure
        assert value.encoded is None

    @pytest.mark.parametrize(
        "variant",
        [
            pytest.param("missing_bytes", id="success_without_bytes"),
            pytest.param("success_failure", id="success_with_failure"),
            pytest.param("missing_failure", id="failure_without_evidence"),
            pytest.param("failure_bytes", id="failure_with_bytes"),
        ],
    )
    def test_constructor__variant__rejects_mixed_or_missing_fields(
        self,
        variant: str,
        genesis_snapshot: WorkflowRunSnapshot,
        record_failure: WorkflowPersistenceFailure,
    ) -> None:
        """Evidence ID: SV-WFR-RUN-ENCODE-003

        Requirement: Unknown, mixed and incomplete variants are invalid.

        Method: Construct independent invalid success and failure partitions.

        Oracle: Exact mutually exclusive success/failure field invariant.

        Acceptance: Every invalid variant raises ValueError.

        Interpretation: No partial encoded success can be constructed ordinarily.

        Limitations: Malformed wire input belongs to future serializer tests.
        """
        envelope = self.make_encoded(genesis_snapshot)
        with pytest.raises(ValueError):
            if variant == "missing_bytes":
                WorkflowRunEncodeResult(status="encoded")
            elif variant == "success_failure":
                WorkflowRunEncodeResult(
                    status="encoded", encoded=envelope, failure=record_failure
                )
            elif variant == "missing_failure":
                WorkflowRunEncodeResult(status="error")
            else:
                WorkflowRunEncodeResult(
                    status="invalid", encoded=envelope, failure=record_failure
                )

    @pytest.mark.parametrize(
        "field",
        [
            pytest.param("status", id="nonstring_status"),
            pytest.param("encoded", id="bytes_without_envelope"),
            pytest.param("failure", id="text_without_failure_record"),
        ],
    )
    def test_constructor__types__rejects_wrong_semantic_fields(
        self, field: str, record_failure: WorkflowPersistenceFailure
    ) -> None:
        """Evidence ID: SV-WFR-RUN-ENCODE-004

        Requirement: Exact concrete field types are mandatory.

        Method: Replace one field of a valid failure with a wrong semantic type.

        Oracle: Declared exact status/envelope/failure types.

        Acceptance: Each replacement raises TypeError.

        Interpretation: A string diagnostic is not structured failure evidence.

        Limitations: Inputs are closed representative wrong-type partitions.
        """
        value = WorkflowRunEncodeResult(status="error", failure=record_failure)
        with pytest.raises(TypeError):
            if field == "status":
                replace(value, status=True)  # type: ignore[arg-type]
            elif field == "encoded":
                replace(value, encoded=b"bytes")  # type: ignore[arg-type]
            else:
                replace(value, failure="failure")  # type: ignore[arg-type]

    def test_constructor__status__rejects_unknown(self) -> None:
        """Evidence ID: SV-WFR-RUN-ENCODE-006

        Requirement: The aggregate encode status vocabulary is closed.

        Method: Supply an unknown exact string at the constructor boundary.

        Oracle: Exactly encoded, incompatible, invalid and error are accepted.

        Acceptance: The unknown status raises ValueError.

        Interpretation: Unknown string values differ from wrong semantic types.

        Limitations: This record does not classify codec operation failures.
        """
        with pytest.raises(ValueError):
            WorkflowRunEncodeResult(status="unknown")  # type: ignore[arg-type]

    def test_field__status__is_immutable(
        self, record_failure: WorkflowPersistenceFailure
    ) -> None:
        """Evidence ID: SV-WFR-RUN-ENCODE-005

        Requirement: A completed outcome cannot be relabeled in place.

        Method: Attempt status assignment on a represented error.

        Oracle: Frozen dataclass semantics and original error status.

        Acceptance: Assignment raises FrozenInstanceError and status stays error.

        Interpretation: Ordinary mutation cannot manufacture encoded success.

        Limitations: No hostile-memory protection is claimed.
        """
        value = WorkflowRunEncodeResult(status="error", failure=record_failure)
        with pytest.raises(FrozenInstanceError):
            value.status = "encoded"  # type: ignore[misc]
        assert value.status == "error"
