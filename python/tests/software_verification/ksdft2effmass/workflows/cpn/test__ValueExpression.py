"""Software verification for ``ValueExpression`` as the sole primary SUT.

Evidence class: software verification. Requirement and strategy are stated per
case; public construction/execution supplies the method and exact state or the
documented exception taxonomy supplies the independent oracle. Passing verifies
only the named class contract. It does not provide numerical verification,
scientific validation, uncertainty quantification, persistence, SNAKES-adapter,
Rust-conformance, or scientific-execution evidence. Collaborators are synthetic
setup only.
"""

import pytest

from ksdft2effmass.workflows.cpn import (
    ContractValue,
    ContractValueKind,
    TokenField,
    ValueExpression,
    ValueExpressionKind,
)

pytestmark = pytest.mark.software_verification

SUT = ValueExpression


def test_cpn_sv_p1_006_expression_union_rejects_lambda_like_state() -> None:
    """SV-CPN-006: exact closed, nonarithmetic value-expression vocabulary.

    Requirement
    -----------
    The version-1 P1 contract admits exactly literal, token-field, and bound-token-ID
    value expressions. It has no addition, subtraction, increment, or other
    arithmetic expression kind.

    Method
    ------
    Enumerate ``ValueExpressionKind`` and compare its ordered names and serialized
    values with the exact public vocabulary. Then invoke ``ValueExpression`` with a
    string ``'lambda'`` and with an incomplete token-field alternative.

    Independent oracle
    ------------------
    The documented closed grammar is exactly ``LITERAL = 'literal'``,
    ``TOKEN_FIELD = 'token_field'``, and
    ``BOUND_TOKEN_IDS = 'bound_token_ids'``. No callable, source-text, addition,
    subtraction, increment, or general arithmetic alternative exists.

    Acceptance criterion
    --------------------
    Enum names and values match that exact three-entry vocabulary; the string tag
    raises ``TypeError`` and the incomplete branch raises ``ValueError``.

    Failure interpretation
    ----------------------
    A missing or additional enum entry changes the version-1 expression language.
    Acceptance of either malformed construction would expose a nondeclarative or
    ambiguous expression state.

    Limitations
    -----------
    This constructor case does not evaluate a guard and does not prove future
    expression-language compatibility. In particular, it asserts absence rather
    than implementing arithmetic or automatic ``iteration_index`` advancement.
    """
    assert tuple((kind.name, kind.value) for kind in ValueExpressionKind) == (
        ("LITERAL", "literal"),
        ("TOKEN_FIELD", "token_field"),
        ("BOUND_TOKEN_IDS", "bound_token_ids"),
    )
    with pytest.raises(TypeError, match="ValueExpressionKind"):
        ValueExpression("lambda")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="fields"):
        ValueExpression(ValueExpressionKind.TOKEN_FIELD, variable="token")


def test_cpn_sv_p1_078_every_expression_union_branch_is_constructible() -> None:
    """SV-CPN-078: admit literal, token-field, and bound-token-ID union branches.

    Public exact state is the method and closed grammar is the independent oracle.
    Acceptance retains each active field and repeated bound variables. Failure leaves
    a documented declarative branch unreachable. Evaluation is excluded.
    """
    literal = ContractValue(ContractValueKind.STRING, "x")
    assert SUT(ValueExpressionKind.LITERAL, literal=literal).literal is literal
    assert (
        SUT(
            ValueExpressionKind.TOKEN_FIELD, variable="v", field=TokenField.RUN_ID
        ).variable
        == "v"
    )
    assert SUT(ValueExpressionKind.BOUND_TOKEN_IDS, variables=("v", "v")).variables == (
        "v",
        "v",
    )


def test_cpn_sv_p1_079_expression_fields_enforce_exact_semantic_types() -> None:
    """SV-CPN-079: reject non-enum tags and malformed variable containers.

    Controlled-invalid public construction reliably exercises the error boundary;
    exact declared types are the oracle. Acceptance requires ``TypeError`` for tag,
    collection, and entry mismatches, and ``ValueError`` for empty identity. Failure
    permits non-portable expression state.
    """
    with pytest.raises(TypeError):
        SUT("literal")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(ValueExpressionKind.BOUND_TOKEN_IDS, variables=["v"])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(ValueExpressionKind.BOUND_TOKEN_IDS, variables=(1,))  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT(ValueExpressionKind.BOUND_TOKEN_IDS, variables=("",))

    literal = ContractValue(ContractValueKind.STRING, "x")
    malformed_shapes = (
        lambda: SUT(ValueExpressionKind.LITERAL),
        lambda: SUT(ValueExpressionKind.LITERAL, literal=literal, variable="v"),
        lambda: SUT(
            ValueExpressionKind.TOKEN_FIELD,
            variable=1,  # type: ignore[arg-type]
            field=TokenField.RUN_ID,
        ),
        lambda: SUT(
            ValueExpressionKind.TOKEN_FIELD, variable="", field=TokenField.RUN_ID
        ),
        lambda: SUT(
            ValueExpressionKind.TOKEN_FIELD,
            variable="v",
            field="run_id",  # type: ignore[arg-type]
        ),
        lambda: SUT(
            ValueExpressionKind.TOKEN_FIELD,
            literal=literal,
            variable="v",
            field=TokenField.RUN_ID,
        ),
        lambda: SUT(ValueExpressionKind.BOUND_TOKEN_IDS),
        lambda: SUT(
            ValueExpressionKind.BOUND_TOKEN_IDS,
            variable="v",
            variables=("v",),
        ),
    )
    for construct in malformed_shapes:
        with pytest.raises(ValueError, match="fields"):
            construct()
