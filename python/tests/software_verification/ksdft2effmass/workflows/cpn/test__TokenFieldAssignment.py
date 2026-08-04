"""Software verification for ``TokenFieldAssignment`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

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


def test_cpn_sv_p1_053_assignment_requires_enum_and_expression() -> None:
    """SV-CPN-053: constrain an assignment to public field and expression types.

    An independently valid literal expression is the collaborator. Acceptance
    retains both objects and rejects either string substitutions with ``TypeError``.
    Failure would admit nondeclarative assignment state.
    """
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
