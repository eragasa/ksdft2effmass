"""Evidence class and represented meaning
--------------------------------------
This module provides software-verification evidence for the public ``CpnNetDefinition``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Owned contract, oracle, and scope
---------------------------------
``CpnNetDefinition`` is the sole primary SUT. Tests exercise its documented public
contract with synthetic routing inputs; exact constructor, language, enum, ordering, and
error-taxonomy rules provide the independent oracles. Collaborators only construct
inputs or expose public outcomes.

VVUQ and scientific exclusions
------------------------------
Passing means the named software contracts hold; failure may identify an implementation,
fixture, oracle transcription, environment, or public-contract inconsistency. This
module excludes numerical verification, scientific validation, uncertainty
quantification, physical correctness, persistence and engine-adapter behavior, and
cross-language conformance."""

import pytest

from ksdft2effmass.workflows.cpn import CpnMarking, CpnNetDefinition

SUT = CpnNetDefinition


def test_constructor__contract__net_requires_v1_and_canonicalizes_collections(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-044

    Requirement
    -----------
    enforce version-1 container ownership and lexical order.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: enforce version-1 container ownership and
    lexical order. The public executable fixture supplies valid collaborators; sorted
    identities and the fixed version are the oracle. Acceptance requires canonical order
    and exact type/value rejection. Failure makes the net wire surface unstable.

    Oracle
    ------
    The documented public rule that the SUT must enforce version-1 container ownership
    and lexical order is the contract oracle; fixed synthetic values, Python exact
    type/value semantics, and the public error taxonomy provide independently
    inspectable expected outcomes where used.

    Acceptance
    ----------
    Every preserved exact equality, identity, ordering, representation, and expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation
    --------------
    Pass supports only this named software contract. Failure may indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations
    -----------
    The case excludes unexercised inputs and dependencies, physical conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
    net = executable_net
    assert tuple(x.place_id for x in net.places) == tuple(
        sorted(x.place_id for x in net.places)
    )
    with pytest.raises(TypeError):
        SUT(True, "m", (), (), (), (), CpnMarking(1, "m", 0, ()))
    with pytest.raises(ValueError):
        SUT(2, "m", (), (), (), (), CpnMarking(1, "m", 0, ()))


pytestmark = pytest.mark.software_verification
