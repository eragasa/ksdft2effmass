"""Software verification for ``PlaceDefinition`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

import pytest

from ksdft2effmass.workflows.cpn import PlaceDefinition

SUT = PlaceDefinition


def test_cpn_sv_p1_050_place_requires_colors_and_canonicalizes_them() -> None:
    """SV-CPN-050: require a nonempty canonical allowed-color set.

    Lexical unique storage is the oracle. Acceptance sorts public input, rejects an
    empty set with ``ValueError``, and rejects a list with ``TypeError``. Failure
    leaves place admission undefined or nondeterministic.
    """
    assert SUT("p", "place", ("z", "a")).allowed_color_ids == ("a", "z")
    with pytest.raises(ValueError):
        SUT("p", "place", ())
    with pytest.raises(TypeError):
        SUT("p", "place", ["c"])  # type: ignore[arg-type]


pytestmark = pytest.mark.software_verification
