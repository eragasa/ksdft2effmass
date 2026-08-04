"""Evidence class and represented meaning
--------------------------------------
This module provides software-verification evidence for the public ``TokenTemplate``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Owned contract, oracle, and scope
---------------------------------
``TokenTemplate`` is the sole primary SUT. Tests exercise its documented public contract
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
    ContractValue,
    ContractValueKind,
    TokenField,
    TokenFieldAssignment,
    TokenTemplate,
    ValueExpression,
    ValueExpressionKind,
)

SUT = TokenTemplate


def _assign(field: TokenField, value: ContractValue) -> TokenFieldAssignment:
    """Evidence ID
    -----------
    This helper supports exactly SV-CPN-055 and owns no independent evidence ID.

    Requirement
    -----------
    Provide explicit synthetic setup or assertion mechanics without creating an
    independent pass claim.

    Method
    ------
    Construct or transform the public CPN test inputs required by the listed evidence
    owners. Prior helper description: local synthetic setup only.

    Oracle
    ------
    The helper has no independent oracle; each supported test owns and documents the
    applicable contract oracle.

    Acceptance
    ----------
    Return the exact public object or deterministic setup consumed by every listed
    evidence owner, without swallowing exceptions or asserting a separate result.

    Interpretation
    --------------
    A helper failure blocks or invalidates its listed evidence owners but is not an
    independent evidence failure.

    Limitations
    -----------
    The helper is synthetic, supports only the complete identifier list above, owns no
    independent evidence ID, and establishes no numerical verification, scientific
    validation, uncertainty quantification, physical meaning, or cross-language
    conformance."""
    return TokenFieldAssignment(
        field, ValueExpression(ValueExpressionKind.LITERAL, literal=value)
    )


def test_constructor__contract__template_requires_unique_complete_assignments() -> None:
    """Evidence ID
    -----------
    SV-CPN-055

    Requirement
    -----------
    enforce complete unique output routing assignments.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: enforce complete unique output routing
    assignments. Six required public fields form the independent oracle. Acceptance
    constructs that template and rejects a missing field and duplicate field with
    ``ValueError``. Failure permits produced tokens lacking contract routing state.

    Oracle
    ------
    The documented public rule that the SUT must enforce complete unique output routing
    assignments is the contract oracle; fixed synthetic values, Python exact type/value
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
    assignments = (
        _assign(TokenField.WORKFLOW_ID, ContractValue(ContractValueKind.STRING, "w")),
        _assign(TokenField.RUN_ID, ContractValue(ContractValueKind.STRING, "r")),
        _assign(TokenField.ATTEMPT_ID, ContractValue(ContractValueKind.STRING, "a")),
        _assign(
            TokenField.ITERATION_INDEX, ContractValue(ContractValueKind.INTEGER, 0)
        ),
        _assign(
            TokenField.PROVENANCE_IDS,
            ContractValue(ContractValueKind.STRING_SEQUENCE, ()),
        ),
        _assign(
            TokenField.PARENT_TOKEN_IDS,
            ContractValue(ContractValueKind.STRING_SEQUENCE, ()),
        ),
    )
    assert SUT("c", assignments).assignments == assignments
    with pytest.raises(ValueError, match="missing required"):
        SUT("c", assignments[:-1])
    with pytest.raises(ValueError, match="unique"):
        SUT("c", assignments + (assignments[0],))


pytestmark = pytest.mark.software_verification
