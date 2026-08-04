"""Software verification for ``PlaceMarking`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

from collections.abc import Callable

import pytest

from ksdft2effmass.workflows.cpn import CpnToken, PlaceMarking

SUT = PlaceMarking


def test_cpn_sv_p1_051_place_marking_canonicalizes_token_order(
    token_factory: Callable[..., CpnToken],
) -> None:
    """SV-CPN-051: retain multiplicity while ordering tokens by identity.

    Two public synthetic tokens are the fixture; lexical identity order is the
    oracle. Acceptance also requires empty identity ``ValueError`` and mutable
    token collection ``TypeError``. Failure destabilizes marking representation.
    """
    a, b = token_factory("a"), token_factory("b")
    assert SUT("p", (b, a)).tokens == (a, b)
    with pytest.raises(ValueError):
        SUT("", ())
    with pytest.raises(TypeError):
        SUT("p", [a])  # type: ignore[arg-type]


pytestmark = pytest.mark.software_verification
