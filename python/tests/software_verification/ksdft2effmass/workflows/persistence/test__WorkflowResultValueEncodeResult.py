r"""Software verification of ``WorkflowResultValueEncodeResult``.

Bounded artifact scope: closed encoded/incompatible/invalid/error variant shape.

Evidence profile: claim_bearing

Facet and represented meaning

Success carries exactly an envelope; every failure carries only structured evidence.

Intrinsic and cross-object scope

These are result-shape invariants, not a claim of codec or aggregate correctness.

VVUQ and scientific exclusions

Software verification only; no scientific validity, persistence or execution permission.
"""

from typing import Literal

import pytest

from ksdft2effmass.workflows import (
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectIdentity,
    ResultObjectTypeIdentity,
    WorkflowEncodedResultValue,
    WorkflowPersistenceFailure,
    WorkflowPersistenceFailureCode,
    WorkflowResultValueEncodeResult,
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowResultValueEncodeResult


class TestWorkflowResultValueEncodeResult:
    """Closed encode variants cannot disguise missing or partial outputs."""

    @staticmethod
    def make_failure() -> WorkflowPersistenceFailure:
        return WorkflowPersistenceFailure(
            implementation_identity="codec:1",
            phase="encode",
            code=WorkflowPersistenceFailureCode.CODEC_ERROR,
            input_identities=(),
            expected="complete value",
            observed="failure",
            diagnostic="failed",
            claim_boundary="software only",
        )

    @staticmethod
    def make_envelope() -> WorkflowEncodedResultValue:
        return WorkflowEncodedResultValue(
            result_identity=ResultObjectIdentity("result"),
            concrete_type_identity=ResultObjectTypeIdentity("synthetic:1"),
            owning_domain_identity=ResultObjectDomainIdentity("synthetic"),
            schema_identity="synthetic:1",
            content_identity=ResultObjectContentIdentity("opaque"),
            payload=b"",
            payload_digest="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        )

    def test_constructor__encoded__requires_only_envelope(self) -> None:
        """Evidence ID: SV-WFR-ENCODE-RESULT-001

        Requirement: Encoded alone contains an envelope and no failure evidence.

        Method: Exercise the valid and two invalid success field combinations.

        Oracle: Closed encoded result variant contract.

        Acceptance: Only a complete envelope without failure permits encoded status.

        Interpretation: Empty success and mixed success/failure are impossible.

        Limitations: Envelope schema support belongs to the selected codec.
        """
        envelope = self.make_envelope()
        assert (
            WorkflowResultValueEncodeResult(status="encoded", encoded=envelope).encoded
            is envelope
        )
        with pytest.raises(ValueError):
            WorkflowResultValueEncodeResult(status="encoded")
        with pytest.raises(ValueError):
            WorkflowResultValueEncodeResult(
                status="encoded", encoded=envelope, failure=self.make_failure()
            )

    @pytest.mark.parametrize(
        "status",
        [
            pytest.param("incompatible", id="incompatible"),
            pytest.param("invalid", id="invalid"),
            pytest.param("error", id="error"),
        ],
    )
    def test_constructor__failure__excludes_envelope(
        self, status: Literal["incompatible", "invalid", "error"]
    ) -> None:
        """Evidence ID: SV-WFR-ENCODE-RESULT-002

        Requirement: Every failed encode contains evidence and no encoded envelope.

        Method: Test all three explicit failure statuses and invalid field mixes.

        Oracle: Closed failure variant invariant.

        Acceptance: Each failure requires evidence and prohibits an envelope.

        Interpretation: A nonencoded status cannot carry a partial success value.

        Limitations: Failure semantics are classified by the operation owner.
        """
        failure = self.make_failure()
        result = WorkflowResultValueEncodeResult(status=status, failure=failure)
        assert result.failure is failure and result.encoded is None
        with pytest.raises(ValueError):
            WorkflowResultValueEncodeResult(status=status)
        with pytest.raises(ValueError):
            WorkflowResultValueEncodeResult(
                status=status, encoded=self.make_envelope(), failure=failure
            )

    def test_constructor__status__rejects_unknown(self) -> None:
        """Evidence ID: SV-WFR-ENCODE-RESULT-003

        Requirement: Encode outcome vocabulary is closed.

        Method: Pass one explicit unknown status at the intentional invalid call.

        Oracle: The four permitted encode statuses.

        Acceptance: An unknown exact string status raises ValueError.

        Interpretation: Unrecognized variants cannot masquerade as success or failure.

        Limitations: Wire version support is a separate codec responsibility.
        """
        with pytest.raises(ValueError):
            WorkflowResultValueEncodeResult(status="future")  # type: ignore[arg-type]
