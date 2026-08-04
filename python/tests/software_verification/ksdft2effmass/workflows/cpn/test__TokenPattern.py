"""Software verification for ``TokenPattern`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

import pytest

from ksdft2effmass.workflows.cpn import TokenPattern

SUT = TokenPattern


def test_cpn_sv_p1_054_pattern_requires_canonical_nonempty_colors() -> None:
    """SV-CPN-054: require a named variable and nonempty allowed-color set.

    Lexical tuple storage and constructor taxonomy are the oracles. Acceptance
    sorts colors, rejects empty cardinality with ``ValueError``, and mutable input
    with ``TypeError``. Failure makes input matching underspecified.
    """
    assert SUT("v", ("z", "a")).allowed_color_ids == ("a", "z")
    with pytest.raises(ValueError):
        SUT("v", ())
    with pytest.raises(TypeError):
        SUT("v", ["c"])  # type: ignore[arg-type]


pytestmark = pytest.mark.software_verification
