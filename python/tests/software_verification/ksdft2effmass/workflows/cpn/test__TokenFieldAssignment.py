r"""Software verification of ``TokenFieldAssignment``.

Facet and represented meaning
--------------------------------------
This module provides software-verification evidence for the public
``TokenFieldAssignment`` software surface and its finite, exact CPN routing
representation. It does not represent a physical observable or numerical approximation.

Intrinsic and cross-object scope
--------------------------------
``TokenFieldAssignment`` is the sole primary SUT. Tests exercise its documented public
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
    ContractValue,
    ContractValueKind,
    TokenField,
    TokenFieldAssignment,
    ValueExpression,
    ValueExpressionKind,
)

SUT = TokenFieldAssignment


def test_constructor__fields__assignment_requires_enum_and_expression() -> None:
    """Evidence ID
    -----------
    SV-CPN-053

    Requirement
    -----------
    ``TokenFieldAssignment`` preserves the exact accepted state for its
    ``fields`` contract.

    Method
    ------
    Construct the public SUT and inspect retained exact public outcomes.

    Oracle
    ------
    The documented public invariant and fixed synthetic inputs provide the independent
    exact state oracle.

    Acceptance
    ----------
    Every retained exact state assertion holds.

    Interpretation
    --------------
    Pass supports only this accepted-state partition; failure may identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    expression = ValueExpression(
        ValueExpressionKind.LITERAL,
        literal=ContractValue(ContractValueKind.STRING, "x"),
    )
    assignment = SUT(TokenField.RUN_ID, expression)
    assert assignment.field is TokenField.RUN_ID and assignment.expression is expression


def test_constructor__fields__rejects_invalid_state() -> None:
    """Evidence ID
    -----------
    SV-CPN-148

    Requirement
    -----------
    ``TokenFieldAssignment`` rejects the documented invalid state for its
    ``fields`` contract.

    Method
    ------
    Exercise the retained synthetic invalid inputs through the public SUT.

    Oracle
    ------
    The documented public invariant and fixed synthetic inputs provide the independent
    exact error-taxonomy oracle.

    Acceptance
    ----------
    Every retained invalid call raises the documented exact public exception.

    Interpretation
    --------------
    Pass supports only this rejection partition; failure may identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    expression = ValueExpression(
        ValueExpressionKind.LITERAL,
        literal=ContractValue(ContractValueKind.STRING, "x"),
    )
    SUT(TokenField.RUN_ID, expression)
    with pytest.raises(TypeError):
        SUT("run_id", expression)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(TokenField.RUN_ID, "x")  # type: ignore[arg-type]


pytestmark = pytest.mark.software_verification
