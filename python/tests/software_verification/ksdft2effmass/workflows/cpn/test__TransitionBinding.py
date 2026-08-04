"""Software verification for ``TransitionBinding`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

import pytest

from ksdft2effmass.workflows.cpn import TokenBinding, TransitionBinding

SUT = TransitionBinding


def test_cpn_sv_p1_056_transition_binding_is_unique_and_canonical() -> None:
    """SV-CPN-056: require unique variables and lexical assignment order.

    Two independently valid bindings provide the oracle. Acceptance sorts them,
    rejects duplicate variables with ``ValueError``, and mutable input with
    ``TypeError``. Failure makes binding evaluation ambiguous.
    """
    a, b = TokenBinding("a", "1"), TokenBinding("b", "2")
    assert SUT("t", (b, a)).assignments == (a, b)
    with pytest.raises(ValueError):
        SUT("t", (a, TokenBinding("a", "2")))
    with pytest.raises(TypeError):
        SUT("t", [a])  # type: ignore[arg-type]


pytestmark = pytest.mark.software_verification
