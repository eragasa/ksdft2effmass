"""Software verification for ``ArcDefinition`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

import pytest

from ksdft2effmass.workflows.cpn import (
    ArcDefinition,
    ArcDirection,
    InputArcMode,
    InputInscription,
    TokenPattern,
)

SUT = ArcDefinition


def test_cpn_sv_p1_040_direction_selects_exactly_one_inscription() -> None:
    """SV-CPN-040: enforce the arc direction/inscription tagged union.

    Method uses public construction; direction equality is the independent oracle.
    Acceptance requires a valid input arc and ``ValueError`` for a missing or
    opposite inscription. Failure permits ambiguous graph topology.
    """
    inscription = InputInscription(InputArcMode.CONSUME, (TokenPattern("v", ("c",)),))
    assert (
        SUT(
            "a", "p", "t", ArcDirection.INPUT, input_inscription=inscription
        ).input_inscription
        == inscription
    )
    with pytest.raises(ValueError, match="match arc direction"):
        SUT("a", "p", "t", ArcDirection.OUTPUT, input_inscription=inscription)


pytestmark = pytest.mark.software_verification
