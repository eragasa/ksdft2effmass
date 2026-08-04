"""Evidence class and represented meaning
--------------------------------------
This module provides software-verification evidence for the public ``ArcDefinition``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Owned contract, oracle, and scope
---------------------------------
``ArcDefinition`` is the sole primary SUT. Tests exercise its documented public contract
with synthetic routing inputs; exact constructor, language, enum, ordering, and
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

from ksdft2effmass.workflows.cpn import (
    ArcDefinition,
    ArcDirection,
    InputArcMode,
    InputInscription,
    TokenPattern,
)

SUT = ArcDefinition


def test_constructor__contract__direction_selects_exactly_one_inscription() -> None:
    """Evidence ID
    -----------
    SV-CPN-040

    Requirement
    -----------
    enforce the arc direction/inscription tagged union.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: enforce the arc direction/inscription
    tagged union. Method uses public construction; direction equality is the independent
    oracle. Acceptance requires a valid input arc and ``ValueError`` for a missing or
    opposite inscription. Failure permits ambiguous graph topology.

    Oracle
    ------
    The documented public rule that the SUT must enforce the arc direction/inscription
    tagged union is the contract oracle; fixed synthetic values, Python exact type/value
    semantics, and the public error taxonomy provide independently inspectable expected
    outcomes where used.

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
