"""Evidence class and represented meaning
--------------------------------------
This module provides software-verification evidence for the public ``InputInscription``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Owned contract, oracle, and scope
---------------------------------
``InputInscription`` is the sole primary SUT. Tests exercise its documented public
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

from ksdft2effmass.workflows.cpn import InputArcMode, InputInscription, TokenPattern

SUT = InputInscription


def test_constructor__contract__input_inscription_requires_typed_nonempty_patterns\
() -> None:
    """Evidence ID
    -----------
    SV-CPN-048

    Requirement
    -----------
    require a mode and a nonempty immutable pattern demand.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: require a mode and a nonempty immutable
    pattern demand. Public construction is the method and declared field types are the
    oracle. Acceptance preserves the pattern and distinguishes wrong types from empty
    cardinality. Failure permits an input arc with no binding demand.

    Oracle
    ------
    The documented public rule that the SUT must require a mode and a nonempty immutable
    pattern demand is the contract oracle; fixed synthetic values, Python exact
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
    pattern = TokenPattern("v", ("c",))
    assert SUT(InputArcMode.READ, (pattern,)).patterns == (pattern,)
    with pytest.raises(TypeError):
        SUT("read", (pattern,))  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT(InputArcMode.READ, ())


pytestmark = pytest.mark.software_verification
