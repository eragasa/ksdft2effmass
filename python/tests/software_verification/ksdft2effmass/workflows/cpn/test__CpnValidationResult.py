"""Software verification for ``CpnValidationResult`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

import pytest

from ksdft2effmass.workflows.cpn import (
    CpnIssueCode,
    CpnValidationIssue,
    CpnValidationResult,
)

SUT = CpnValidationResult


def test_cpn_sv_p1_046_validity_is_exactly_issue_emptiness() -> None:
    """SV-CPN-046: derive validity solely from the immutable issue tuple.

    Empty and singleton public results form the independent truth-table oracle.
    Acceptance requires exact booleans and ``TypeError`` for mutable input. Failure
    makes validation outcomes ambiguous.
    """
    issue = CpnValidationIssue(CpnIssueCode.UNKNOWN_COLOR, (), (), "unknown")
    assert SUT(()).is_valid is True and SUT((issue,)).is_valid is False
    with pytest.raises(TypeError):
        SUT([])  # type: ignore[arg-type]


pytestmark = pytest.mark.software_verification
