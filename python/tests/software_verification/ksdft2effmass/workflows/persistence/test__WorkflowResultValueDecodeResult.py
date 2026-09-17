r"""Software verification of ``WorkflowResultValueDecodeResult``.

Bounded artifact scope: decoded/incompatible/corrupt/error result field closure.

Evidence profile: claim_bearing

Facet and represented meaning

Success contains a concrete result, while failed reconstruction contains no value.

Intrinsic and cross-object scope

The result container owns shape, not concrete codec coverage or domain validation.

VVUQ and scientific exclusions

Software verification only; no numerical verification, science, authority or effects.
"""

from dataclasses import dataclass
from typing import Literal

import pytest
from ksdft2effmass.workflows import (
    ResultObjectIdentity,
    WorkflowPersistenceFailure,
    WorkflowPersistenceFailureCode,
    WorkflowResultValueDecodeResult,
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowResultValueDecodeResult


class TestWorkflowResultValueDecodeResult:
    """Protocol-shaped values establish only container typing, never codec support."""

    @staticmethod
    def make_failure() -> WorkflowPersistenceFailure:
        return WorkflowPersistenceFailure(
            implementation_identity="codec:1",
            phase="decode",
            code=WorkflowPersistenceFailureCode.CODEC_ERROR,
            input_identities=(),
            expected="complete result",
            observed="failure",
            diagnostic="failed",
            claim_boundary="software only",
        )

    def test_constructor__decoded__requires_only_value(self) -> None:
        """Evidence ID: SV-WFR-DECODE-RESULT-001

        Requirement: Only decoded contains a concrete result with no failure.

        Method: Exercise one populated result and two invalid success shapes.

        Oracle: Closed decoded result variant contract, not an encode round trip.

        Acceptance: Decoded requires a value and prohibits failure evidence.

        Interpretation: Container protocol typing does not confer serializability.

        Limitations: This identity-only synthetic value is not supported by a codec.
        """

        @dataclass(frozen=True)
        class SyntheticResult:
            identity: ResultObjectIdentity

        value = SyntheticResult(ResultObjectIdentity("synthetic"))
        result = WorkflowResultValueDecodeResult(status="decoded", value=value)
        assert result.value is value and result.failure is None
        with pytest.raises(ValueError):
            WorkflowResultValueDecodeResult(status="decoded")
        with pytest.raises(ValueError):
            WorkflowResultValueDecodeResult(
                status="decoded", value=value, failure=self.make_failure()
            )

    @pytest.mark.parametrize(
        "status",
        [
            pytest.param("incompatible", id="incompatible"),
            pytest.param("corrupt", id="corrupt"),
            pytest.param("error", id="error"),
        ],
    )
    def test_constructor__failure__requires_evidence(
        self, status: Literal["incompatible", "corrupt", "error"]
    ) -> None:
        """Evidence ID: SV-WFR-DECODE-RESULT-002

        Requirement: Every failed decode must retain structured failure evidence.

        Method: Exercise valid and evidence-free failure variants.

        Oracle: Closed failure shape contract.

        Acceptance: Each failure requires evidence and retains no value.

        Interpretation: Failure outcomes cannot be interpreted as empty success.

        Limitations: Correct classification belongs to each owning operation.
        """
        failure = self.make_failure()
        result = WorkflowResultValueDecodeResult(status=status, failure=failure)
        assert result.failure is failure and result.value is None
        with pytest.raises(ValueError):
            WorkflowResultValueDecodeResult(status=status)

    def test_constructor__status__rejects_unknown(self) -> None:
        """Evidence ID: SV-WFR-DECODE-RESULT-003

        Requirement: Decode outcomes are a closed vocabulary.

        Method: Supply one intentional invalid status at the exact call boundary.

        Oracle: The four supported decode statuses.

        Acceptance: Unknown exact string status raises ValueError.

        Interpretation: The container cannot silently introduce another outcome.

        Limitations: This checks vocabulary, not versioned payload reconstruction.
        """
        with pytest.raises(ValueError):
            WorkflowResultValueDecodeResult(status="future")  # type: ignore[arg-type]
