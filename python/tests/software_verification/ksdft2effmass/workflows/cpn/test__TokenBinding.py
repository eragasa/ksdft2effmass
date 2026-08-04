"""Evidence class and represented meaning
--------------------------------------
This module provides software-verification evidence for the public ``TokenBinding``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Owned contract, oracle, and scope
---------------------------------
``TokenBinding`` is the sole primary SUT. Tests exercise its documented public contract
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

from ksdft2effmass.workflows.cpn import TokenBinding

SUT = TokenBinding


def test_constructor__contract__binding_requires_nonempty_exact_strings() -> None:
    """Evidence ID
    -----------
    SV-CPN-052

    Requirement
    -----------
    require nonempty variable and token identities.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: require nonempty variable and token
    identities. Public field equality and exact exception taxonomy are the oracle.
    Acceptance admits two strings, rejects integer input with ``TypeError``, and empty
    input with ``ValueError``. Failure permits unusable binding identities.

    Oracle
    ------
    The documented public rule that the SUT must require nonempty variable and token
    identities is the contract oracle; fixed synthetic values, Python exact type/value
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
    assert SUT("v", "token").token_id == "token"
    with pytest.raises(TypeError):
        SUT(1, "token")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT("", "token")


pytestmark = pytest.mark.software_verification
