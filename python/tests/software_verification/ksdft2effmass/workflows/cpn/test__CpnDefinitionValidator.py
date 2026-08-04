"""Evidence class and represented meaning
--------------------------------------
This module provides software-verification evidence for the public
``CpnDefinitionValidator`` software surface and its finite, exact CPN routing
representation. It does not represent a physical observable or numerical approximation.

Owned contract, oracle, and scope
---------------------------------
``CpnDefinitionValidator`` is the sole primary SUT. Tests exercise its documented public
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

from ksdft2effmass.workflows.cpn import (
    CpnDefinitionValidator,
    CpnNetDefinition,
)

pytestmark = pytest.mark.software_verification

SUT = CpnDefinitionValidator


def test_method__contract__complete_net_mapping_validates(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-011

    Requirement
    -----------
    complete executable representation of the CPN tuple.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: complete executable representation of the
    CPN tuple. Prior requirement detail: The version-1 P1 contract requires complete
    executable representation of the CPN tuple. Prior method detail: Run
    ``CpnDefinitionValidator.execute`` on the complete ``executable_net``. Prior
    independent oracle detail: The synthetic fixture explicitly supplies every member of
    N=(P,T,A,Sigma,C,G,E,I) with consistent references. Prior acceptance criterion
    detail: The validator-owned ``is_valid`` result is true and carries no issue. Prior
    failure interpretation detail: Any issue means a known-consistent public net is
    rejected or incomplete. Prior limitations detail: This establishes contract
    structure, not scientific-workflow adequacy.

    Oracle
    ------
    The documented public rule that the SUT must complete executable representation of
    the CPN tuple is the contract oracle; fixed synthetic values, Python exact
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
    result = CpnDefinitionValidator().execute(executable_net)
    assert result.is_valid
