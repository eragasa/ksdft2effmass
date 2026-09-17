r"""Software verification of ``WorkflowPersistenceFailure``.

Bounded artifact scope: immutable closed represented failure evidence.

Evidence profile: claim_bearing

Facet and represented meaning

A failure preserves codec version, phase, nominal inputs and sanitized conditions.

Intrinsic and cross-object scope

The record validates its own fields; caller sanitization and codec logic are separate.

VVUQ and scientific exclusions

Software verification only, not scientific validation, authority or store recovery.
"""

from dataclasses import replace

import pytest
from ksdft2effmass.workflows import (
    WorkflowPersistenceFailure,
    WorkflowPersistenceFailureCode,
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowPersistenceFailure


class TestWorkflowPersistenceFailure:
    """Structured immutable evidence without exception text or partial values."""

    @staticmethod
    def make_failure() -> WorkflowPersistenceFailure:
        return WorkflowPersistenceFailure(
            implementation_identity="synthetic-codec:1",
            phase="decode",
            code=WorkflowPersistenceFailureCode.MALFORMED_REPRESENTATION,
            input_identities=("result", "schema"),
            expected="canonical record",
            observed="missing field",
            diagnostic="record shape rejected",
            claim_boundary="software only",
        )

    def test_constructor__evidence__retains_explicit_conditions(self) -> None:
        """Evidence ID: SV-WFR-FAILURE-001

        Requirement: Failure evidence preserves complete applicable input conditions.

        Method: Inspect all explicitly constructed public evidence fields.

        Oracle: Literal independent input values and closed record contract.

        Acceptance: Version, phase, code, inputs and conditions retain exact labels.

        Interpretation: Evidence records observations, not a reconstructed value.

        Limitations: Intrinsic validation cannot determine whether text is sanitized.
        """
        value = self.make_failure()
        assert value.implementation_identity == "synthetic-codec:1"
        assert value.phase == "decode"
        assert value.code is WorkflowPersistenceFailureCode.MALFORMED_REPRESENTATION
        assert value.input_identities == ("result", "schema")
        assert value.expected == "canonical record"
        assert value.observed == "missing field"
        assert value.diagnostic == "record shape rejected"
        assert value.claim_boundary == "software only"

    def test_constructor__input_identities__rejects_empty_member(self) -> None:
        """Evidence ID: SV-WFR-FAILURE-002

        Requirement: Applicable identities are nonempty labels, not fabricated defaults.

        Method: Compare explicit absent input group and a malformed member.

        Oracle: Immutable optional identity group with nonempty member contract.

        Acceptance: Empty identity members raise ValueError; no inputs is legal.

        Interpretation: Missing inputs are distinguished from empty identity labels.

        Limitations: Recorded labels do not prove provenance or authority.
        """
        assert replace(self.make_failure(), input_identities=()).input_identities == ()
        with pytest.raises(ValueError):
            replace(self.make_failure(), input_identities=("",))

    def test_constructor__code__rejects_string_substitute(self) -> None:
        """Evidence ID: SV-WFR-FAILURE-003

        Requirement: Failure categories require their closed enum semantic type.

        Method: Construct with an intentional exact-call static-contract violation.

        Oracle: Exact WorkflowPersistenceFailureCode field contract.

        Acceptance: A string matching an enum value still raises TypeError.

        Interpretation: Closed category typing is explicit rather than string coercion.

        Limitations: Code-to-operation policy belongs to each codec implementation.
        """
        with pytest.raises(TypeError):
            WorkflowPersistenceFailure(
                implementation_identity="codec:1",
                phase="decode",
                code="codec_error",  # type: ignore[arg-type]
                input_identities=(),
                expected="record",
                observed="error",
                diagnostic="failed",
                claim_boundary="software only",
            )
