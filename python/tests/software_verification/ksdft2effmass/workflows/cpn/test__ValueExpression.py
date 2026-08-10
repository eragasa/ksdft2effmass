r"""Software verification of ``ValueExpression``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

--------------------------------------
This module provides software-verification evidence for the public ``ValueExpression``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Intrinsic and cross-object scope

--------------------------------
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


def test_constructor__expression_union__preserves_valid_state() -> None:
    """Evidence ID: SV-CPN-006

    Requirement: ``ValueExpression`` preserves the documented exact valid-state behavior
    for its
    ``expression_union`` contract.

    Method: Construct the public SUT with the retained valid synthetic inputs and
    inspect
    exact public state.

    Oracle: The fixed inputs and documented canonical public representation provide the
    independent exact oracle.

    Acceptance: Every retained exact identity, equality, ordering, type, and
    represented-state
    assertion holds.

    Interpretation: Pass supports this valid-state mapping; failure may identify
    implementation,
    fixture, oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    assert tuple((kind.name, kind.value) for kind in ValueExpressionKind) == (
        ("LITERAL", "literal"),
        ("TOKEN_FIELD", "token_field"),
        ("BOUND_TOKEN_IDS", "bound_token_ids"),
    )


def test_constructor__expression_union__rejects_wrong_types() -> None:
    """Evidence ID: SV-CPN-135

    Requirement: ``ValueExpression`` rejects wrong semantic types for its
    ``expression_union``
    contract.

    Method: Exercise every retained synthetic wrong-type input through the public SUT
    without private mutation.

    Oracle: The documented exact-type taxonomy independently requires ``TypeError`` for
    every retained call.

    Acceptance: Every retained wrong-type call raises exactly ``TypeError``.

    Interpretation: Pass supports this type partition; failure may identify
    implementation, fixture,
    oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(TypeError, match="ValueExpressionKind"):
        ValueExpression("lambda")  # type: ignore[arg-type]


def test_constructor__expression_union__rejects_invalid_values() -> None:
    """Evidence ID: SV-CPN-111

    Requirement: ``ValueExpression`` rejects malformed values of accepted semantic
    types for its
    ``expression_union`` contract.

    Method: Exercise each preserved synthetic invalid-value input through the public SUT
    with
    no warning acceptance or private-state mutation.

    Oracle: The documented public value invariant and Python exception taxonomy
    independently require ``ValueError`` for these inputs.

    Acceptance: Every preserved partition assertion raises exactly ``ValueError``;
    retained
    exact setup and state assertions also hold.

    Interpretation: Pass supports only this named value partition; failure may identify
    implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(ValueError, match="fields"):
        ValueExpression(ValueExpressionKind.TOKEN_FIELD, variable="token")


def test_constructor__fields__every_expression_union_branch_is_constructible() -> None:
    """Evidence ID: SV-CPN-078

    Requirement: admit literal, token-field, and bound-token-ID union branches.

    Method: Exercise the primary SUT through the public construction or operation
    boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: admit literal, token-field, and
    bound-token-ID union branches. Public exact state is the method and closed grammar
    is the independent oracle. Acceptance retains each active field and repeated bound
    variables. Failure leaves a documented declarative branch unreachable. Evaluation is
    excluded.

    Oracle: The documented public rule that the SUT must admit literal, token-field, and
    bound-token-ID union branches is the contract oracle; fixed synthetic values, Python
    exact type/value semantics, and the public error taxonomy provide independently
    inspectable expected outcomes where used.

    Acceptance: Every preserved exact equality, identity, ordering, representation, and
    expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation: Pass supports only this named software contract. Failure may
    indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations: The case excludes unexercised inputs and dependencies, physical
    conclusions,
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


def test_constructor__expression_fields__rejects_wrong_types() -> None:
    """Evidence ID: SV-CPN-079

    Requirement: ``ValueExpression`` rejects wrong semantic types at the public
    constructor boundary for its
    ``expression_fields`` contract.

    Method: Exercise each preserved synthetic wrong-type input through the public SUT
    with
    no warning acceptance or private-state mutation.

    Oracle: The documented public exact-type taxonomy and Python exception taxonomy
    independently require ``TypeError`` for these inputs.

    Acceptance: Every preserved partition assertion raises exactly ``TypeError``;
    retained
    exact setup and state assertions also hold.

    Interpretation: Pass supports only this named type partition; failure may identify
    implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(TypeError):
        SUT("literal")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(ValueExpressionKind.BOUND_TOKEN_IDS, variables=["v"])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(ValueExpressionKind.BOUND_TOKEN_IDS, variables=(1,))  # type: ignore[arg-type]


def test_constructor__expression_fields__rejects_invalid_values() -> None:
    """Evidence ID: SV-CPN-112

    Requirement: ``ValueExpression`` rejects malformed values of accepted semantic
    types for its
    ``expression_fields`` contract.

    Method: Exercise each preserved synthetic invalid-value input through the public SUT
    with
    no warning acceptance or private-state mutation.

    Oracle: The documented public value invariant and Python exception taxonomy
    independently require ``ValueError`` for these inputs.

    Acceptance: Every preserved partition assertion raises exactly ``ValueError``;
    retained
    exact setup and state assertions also hold.

    Interpretation: Pass supports only this named value partition; failure may identify
    implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
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
    with pytest.raises(ValueError, match="fields"):
        malformed_shapes[0]()
    with pytest.raises(ValueError, match="fields"):
        malformed_shapes[1]()
    with pytest.raises(ValueError, match="fields"):
        malformed_shapes[2]()
    with pytest.raises(ValueError, match="fields"):
        malformed_shapes[3]()
