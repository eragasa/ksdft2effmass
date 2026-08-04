"""Evidence class and represented meaning
--------------------------------------
This module provides software-verification evidence for the public ``TransitionBinding``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Owned contract, oracle, and scope
---------------------------------
``TransitionBinding`` is the sole primary SUT. Tests exercise its documented public
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

from ksdft2effmass.workflows.cpn import TokenBinding, TransitionBinding

SUT = TransitionBinding


def test_constructor__contract__transition_binding_is_unique_and_canonical() -> None:
    """Evidence ID
    -----------
    SV-CPN-056

    Requirement
    -----------
    require unique variables and lexical assignment order.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: require unique variables and lexical
    assignment order. Two independently valid bindings provide the oracle. Acceptance
    sorts them, rejects duplicate variables with ``ValueError``, and mutable input with
    ``TypeError``. Failure makes binding evaluation ambiguous.

    Oracle
    ------
    The documented public rule that the SUT must require unique variables and lexical
    assignment order is the contract oracle; fixed synthetic values, Python exact
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
    a, b = TokenBinding("a", "1"), TokenBinding("b", "2")
    assert SUT("t", (b, a)).assignments == (a, b)
    with pytest.raises(ValueError):
        SUT("t", (a, TokenBinding("a", "2")))
    with pytest.raises(TypeError):
        SUT("t", [a])  # type: ignore[arg-type]


pytestmark = pytest.mark.software_verification
