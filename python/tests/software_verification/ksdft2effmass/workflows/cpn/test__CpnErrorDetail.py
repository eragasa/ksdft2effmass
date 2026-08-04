"""Software verification for ``CpnErrorDetail`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

import pytest

from ksdft2effmass.workflows.cpn import CpnErrorCode, CpnErrorDetail

SUT = CpnErrorDetail


def test_cpn_sv_p1_043_detail_validates_and_canonicalizes_context() -> None:
    """SV-CPN-043: require structured codes/messages and canonical token IDs.

    Public construction is compared with lexical tuple order. Acceptance also
    requires wrong code type to raise ``TypeError`` and empty message ``ValueError``.
    Failure weakens deterministic operational diagnostics.
    """
    assert SUT(CpnErrorCode.INVALID_MARKING, "bad", token_ids=("z", "a")).token_ids == (
        "a",
        "z",
    )
    with pytest.raises(TypeError):
        SUT("invalid_marking", "bad")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT(CpnErrorCode.INVALID_MARKING, "")


pytestmark = pytest.mark.software_verification
