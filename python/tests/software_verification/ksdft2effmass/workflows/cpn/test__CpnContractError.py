"""Software verification for ``CpnContractError`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

import pytest

from ksdft2effmass.workflows.cpn import CpnContractError, CpnErrorCode, CpnErrorDetail

SUT = CpnContractError


def test_cpn_sv_p1_042_error_retains_authoritative_detail() -> None:
    """SV-CPN-042: retain structured detail and expose its message as exception text.

    An independently valid detail is the fixture and oracle. Acceptance requires
    identity retention and ``TypeError`` for a non-detail. Failure loses stable
    machine-readable error context.
    """
    detail = CpnErrorDetail(CpnErrorCode.INVALID_BINDING, "invalid binding")
    error = SUT(detail)
    assert error.detail is detail and str(error) == detail.message
    with pytest.raises(TypeError):
        SUT("bad")  # type: ignore[arg-type]


pytestmark = pytest.mark.software_verification
