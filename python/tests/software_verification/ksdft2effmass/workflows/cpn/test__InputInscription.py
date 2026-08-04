"""Software verification for ``InputInscription`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

import pytest

from ksdft2effmass.workflows.cpn import InputArcMode, InputInscription, TokenPattern

SUT = InputInscription


def test_cpn_sv_p1_048_input_inscription_requires_typed_nonempty_patterns() -> None:
    """SV-CPN-048: require a mode and a nonempty immutable pattern demand.

    Public construction is the method and declared field types are the oracle.
    Acceptance preserves the pattern and distinguishes wrong types from empty
    cardinality. Failure permits an input arc with no binding demand.
    """
    pattern = TokenPattern("v", ("c",))
    assert SUT(InputArcMode.READ, (pattern,)).patterns == (pattern,)
    with pytest.raises(TypeError):
        SUT("read", (pattern,))  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT(InputArcMode.READ, ())


pytestmark = pytest.mark.software_verification
