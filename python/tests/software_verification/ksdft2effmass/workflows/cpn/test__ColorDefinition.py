"""Software verification for ``ColorDefinition`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

import pytest

from ksdft2effmass.workflows.cpn import ColorDefinition

SUT = ColorDefinition


def test_cpn_sv_p1_041_color_ids_are_nonempty_and_payload_ids_canonical() -> None:
    """SV-CPN-041: require identities and canonical payload-type membership.

    Public construction is the method; lexical unique tuple storage is the oracle.
    Acceptance requires sorting and exact ``TypeError``/``ValueError`` taxonomy.
    Failure makes color definitions nondeterministic or malformed.
    """
    assert SUT("c", "color", ("z", "a")).allowed_payload_type_ids == ("a", "z")
    with pytest.raises(TypeError):
        SUT(1, "color", ())  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT("", "color", ())


pytestmark = pytest.mark.software_verification
