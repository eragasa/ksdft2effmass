"""Software verification for ``CpnNetDefinition`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

import pytest

from ksdft2effmass.workflows.cpn import CpnMarking, CpnNetDefinition

SUT = CpnNetDefinition


def test_cpn_sv_p1_044_net_requires_v1_and_canonicalizes_collections(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-044: enforce version-1 container ownership and lexical order.

    The public executable fixture supplies valid collaborators; sorted identities
    and the fixed version are the oracle. Acceptance requires canonical order and
    exact type/value rejection. Failure makes the net wire surface unstable.
    """
    net = executable_net
    assert tuple(x.place_id for x in net.places) == tuple(
        sorted(x.place_id for x in net.places)
    )
    with pytest.raises(TypeError):
        SUT(True, "m", (), (), (), (), CpnMarking(1, "m", 0, ()))
    with pytest.raises(ValueError):
        SUT(2, "m", (), (), (), (), CpnMarking(1, "m", 0, ()))


pytestmark = pytest.mark.software_verification
