"""Software verification for ``TokenBinding`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

import pytest

from ksdft2effmass.workflows.cpn import TokenBinding

SUT = TokenBinding


def test_cpn_sv_p1_052_binding_requires_nonempty_exact_strings() -> None:
    """SV-CPN-052: require nonempty variable and token identities.

    Public field equality and exact exception taxonomy are the oracle. Acceptance
    admits two strings, rejects integer input with ``TypeError``, and empty input
    with ``ValueError``. Failure permits unusable binding identities.
    """
    assert SUT("v", "token").token_id == "token"
    with pytest.raises(TypeError):
        SUT(1, "token")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT("", "token")


pytestmark = pytest.mark.software_verification
