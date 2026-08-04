"""Evidence class and represented meaning
--------------------------------------
This module provides software-verification evidence for the public
``TokenFieldAssignment`` software surface and its finite, exact CPN routing
representation. It does not represent a physical observable or numerical approximation.

Owned contract, oracle, and scope
---------------------------------
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


def test_constructor__contract__assignment_requires_enum_and_expression() -> None:
    """Evidence ID
    -----------
    SV-CPN-053

    Requirement
    -----------
    constrain an assignment to public field and expression types.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: constrain an assignment to public field and
    expression types. An independently valid literal expression is the collaborator.
    Acceptance retains both objects and rejects either string substitutions with
    ``TypeError``. Failure would admit nondeclarative assignment state.

    Oracle
    ------
    The documented public rule that the SUT must constrain an assignment to public field
    and expression types is the contract oracle; fixed synthetic values, Python exact
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
    expression = ValueExpression(
        ValueExpressionKind.LITERAL,
        literal=ContractValue(ContractValueKind.STRING, "x"),
    )
    assignment = SUT(TokenField.RUN_ID, expression)
    assert assignment.field is TokenField.RUN_ID and assignment.expression is expression
    with pytest.raises(TypeError):
        SUT("run_id", expression)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(TokenField.RUN_ID, "x")  # type: ignore[arg-type]


pytestmark = pytest.mark.software_verification
