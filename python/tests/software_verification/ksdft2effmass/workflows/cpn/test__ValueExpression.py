"""Evidence class and represented meaning
--------------------------------------
This module provides software-verification evidence for the public ``ValueExpression``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Owned contract, oracle, and scope
---------------------------------
``ValueExpression`` is the sole primary SUT. Tests exercise its documented public
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
    ValueExpression,
    ValueExpressionKind,
)

pytestmark = pytest.mark.software_verification

SUT = ValueExpression


def test_constructor__contract__expression_union_rejects_lambda_like_state() -> None:
    """Evidence ID
    -----------
    SV-CPN-006

    Requirement
    -----------
    exact closed three-member value-expression tagged union with no arithmetic
    expression kind.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: exact closed, nonarithmetic
    value-expression vocabulary. Prior requirement detail: The version-1 P1 contract
    admits exactly literal, token-field, and bound-token-ID value expressions. It has no
    addition, subtraction, increment, or other arithmetic expression kind. Prior method
    detail: Enumerate ``ValueExpressionKind`` and compare its ordered names and
    serialized values with the exact public vocabulary. Then invoke ``ValueExpression``
    with a string ``'lambda'`` and with an incomplete token-field alternative. Prior
    independent oracle detail: The documented closed grammar is exactly ``LITERAL =
    'literal'``, ``TOKEN_FIELD = 'token_field'``, and ``BOUND_TOKEN_IDS =
    'bound_token_ids'``. No callable, source-text, addition, subtraction, increment, or
    general arithmetic alternative exists. Prior acceptance criterion detail: Enum names
    and values match that exact three-entry vocabulary; the string tag raises
    ``TypeError`` and the incomplete branch raises ``ValueError``. Prior failure
    interpretation detail: A missing or additional enum entry changes the version-1
    expression language. Acceptance of either malformed construction would expose a
    nondeclarative or ambiguous expression state. Prior limitations detail: This
    constructor case does not evaluate a guard and does not prove future
    expression-language compatibility. In particular, it asserts absence rather than
    implementing arithmetic or automatic ``iteration_index`` advancement.

    Oracle
    ------
    The documented public rule that the SUT must exact closed three-member
    value-expression tagged union with no arithmetic expression kind is the contract
    oracle; fixed synthetic values, Python exact type/value semantics, and the public
    error taxonomy provide independently inspectable expected outcomes where used.

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
    assert tuple((kind.name, kind.value) for kind in ValueExpressionKind) == (
        ("LITERAL", "literal"),
        ("TOKEN_FIELD", "token_field"),
        ("BOUND_TOKEN_IDS", "bound_token_ids"),
    )
    with pytest.raises(TypeError, match="ValueExpressionKind"):
        ValueExpression("lambda")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="fields"):
        ValueExpression(ValueExpressionKind.TOKEN_FIELD, variable="token")


def test_constructor__contract__every_expression_union_branch_is_constructible() -> (
    None
):
    """Evidence ID
    -----------
    SV-CPN-078

    Requirement
    -----------
    admit literal, token-field, and bound-token-ID union branches.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: admit literal, token-field, and
    bound-token-ID union branches. Public exact state is the method and closed grammar
    is the independent oracle. Acceptance retains each active field and repeated bound
    variables. Failure leaves a documented declarative branch unreachable. Evaluation is
    excluded.

    Oracle
    ------
    The documented public rule that the SUT must admit literal, token-field, and
    bound-token-ID union branches is the contract oracle; fixed synthetic values, Python
    exact type/value semantics, and the public error taxonomy provide independently
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


def test_constructor__contract__expression_fields_enforce_exact_semantic_types() -> (
    None
):
    """Evidence ID
    -----------
    SV-CPN-079

    Requirement
    -----------
    reject non-enum tags and malformed variable containers.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: reject non-enum tags and malformed variable
    containers. Controlled-invalid public construction reliably exercises the error
    boundary; exact declared types are the oracle. Acceptance requires ``TypeError`` for
    tag, collection, and entry mismatches, and ``ValueError`` for empty identity.
    Failure permits non-portable expression state.

    Oracle
    ------
    The documented public rule that the SUT must reject non-enum tags and malformed
    variable containers is the contract oracle; fixed synthetic values, Python exact
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
