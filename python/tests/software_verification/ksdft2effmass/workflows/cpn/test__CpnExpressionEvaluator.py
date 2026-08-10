r"""Software verification of ``CpnExpressionEvaluator``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

--------------------------------------
This module provides software-verification evidence for the public
``CpnExpressionEvaluator`` software surface and its finite, exact CPN routing
representation. It does not represent a physical observable or numerical approximation.

Intrinsic and cross-object scope

--------------------------------
``CpnExpressionEvaluator`` is the sole primary SUT. Tests exercise its documented public
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

from dataclasses import replace

import pytest

from ksdft2effmass.workflows.cpn import (
    ContractValue,
    ContractValueKind,
    CpnExpressionEvaluator,
    CpnMarking,
    CpnNetDefinition,
    GuardExpression,
    GuardOperator,
    TokenBinding,
    TokenField,
    TransitionBinding,
    ValueExpression,
    ValueExpressionKind,
)

pytestmark = pytest.mark.software_verification

SUT = CpnExpressionEvaluator


def literal(kind: ContractValueKind, value: object) -> ValueExpression:
    """Evidence ID: Owns no identifier; supports SV-CPN-008, SV-CPN-009.

    Requirement: Provide explicit synthetic setup or assertion mechanics without
    creating an
    independent pass claim.

    Method: Construct or transform the public CPN test inputs required by the listed
    evidence
    owners. Prior helper description: Construct a typed literal for synthetic expression
    tests.

    Oracle: The helper has no independent oracle; each supported test owns and documents
    the
    applicable contract oracle.

    Acceptance: Return the exact public object or deterministic setup consumed by every
    listed
    evidence owner, without swallowing exceptions or asserting a separate result.

    Interpretation: A helper failure blocks or invalidates its listed evidence owners
    but is not an
    independent evidence failure.

    Limitations: The helper is synthetic, supports only the complete identifier list
    above, owns no
    independent evidence ID, and establishes no numerical verification, scientific
    validation, uncertainty quantification, physical meaning, or cross-language
    conformance."""
    return ValueExpression(
        ValueExpressionKind.LITERAL,
        literal=ContractValue(kind, value),  # type: ignore[arg-type]
    )


def test_method__evaluate_guard__exact_literals_evaluate_without_state() -> None:
    """Evidence ID: SV-CPN-008

    Requirement: exact literal ordering without token state.

    Method: Exercise the primary SUT through the public construction or operation
    boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: exact literal ordering without token state.
    Prior requirement detail: The version-1 P1 contract requires exact literal ordering
    without token state. Prior method detail: Evaluate an integer-literal ``1 < 2``
    guard with ``CpnExpressionEvaluator.evaluate_guard`` over an empty binding and
    marking. Prior independent oracle detail: Built-in exact integer ordering is an
    independent analytical oracle and requires no token lookup or tolerance. Prior
    acceptance criterion detail: The returned ``GuardEvaluationResult.value`` is exactly
    ``True``. Prior failure interpretation detail: False or an exception indicates
    incorrect literal evaluation. Prior limitations detail: No numerical tolerance, unit
    conversion, or scientific comparison is covered.

    Oracle: The documented public rule that the SUT must exact literal ordering without
    token
    state is the contract oracle; fixed synthetic values, Python exact type/value
    semantics, and the public error taxonomy provide independently inspectable expected
    outcomes where used.

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
    marking = CpnMarking(1, "model", 0, ())
    binding = TransitionBinding("transition", ())
    guard = GuardExpression(
        GuardOperator.LESS_THAN,
        left=literal(ContractValueKind.INTEGER, 1),
        right=literal(ContractValueKind.INTEGER, 2),
    )
    assert CpnExpressionEvaluator().evaluate_guard(guard, binding, marking).value


def test_method__evaluate_guard__comparison_rejects_mixed_tags() -> None:
    """Evidence ID: SV-CPN-009

    Requirement: type-strict comparison tags.

    Method: Exercise the primary SUT through the public construction or operation
    boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: type-strict comparison tags. Prior
    requirement detail: The version-1 P1 contract requires type-strict comparison tags.
    Prior method detail: Evaluate equality between integer-tagged ``1`` and real-tagged
    ``1.0`` through ``evaluate_guard``. Prior independent oracle detail: Equal Python
    magnitude does not override the contract requirement that comparison operands carry
    the same ``ContractValueKind``. Prior acceptance criterion detail: Evaluation raises
    ``TypeError`` containing ``equal ContractValue kinds``. Prior failure interpretation
    detail: Success would silently mix integer and real routing semantics. Prior
    limitations detail: This mixed-tag case excludes REAL wire canonicalization; that
    resolved contract is covered separately by the ``SV-CPN-080``--``SV-CPN-088``
    evidence.

    Oracle: The documented public rule that the SUT must type-strict comparison tags is
    the
    contract oracle; fixed synthetic values, Python exact type/value semantics, and the
    public error taxonomy provide independently inspectable expected outcomes where
    used.

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
    guard = GuardExpression(
        GuardOperator.EQUAL,
        left=literal(ContractValueKind.INTEGER, 1),
        right=literal(ContractValueKind.REAL, 1.0),
    )
    with pytest.raises(TypeError, match="equal ContractValue kinds"):
        CpnExpressionEvaluator().evaluate_guard(
            guard, TransitionBinding("transition", ()), CpnMarking(1, "model", 0, ())
        )


def make_maximum_control_context(
    executable_net: CpnNetDefinition,
) -> tuple[
    CpnExpressionEvaluator,
    TransitionBinding,
    CpnMarking,
    tuple[tuple[ValueExpression, ValueExpression], ...],
    ContractValue,
]:
    """Evidence ID: Owns no identifier; supports SV-CPN-085, SV-CPN-168.

    Requirement: Provide maximum-control expression setup without an independent
    evidence claim.

    Method: Replace both synthetic tokens' expression-visible controls and construct
    field
    reads.

    Oracle: The supported tests own exact value and comparison oracles; this helper owns
    none.

    Acceptance: Return the evaluator, binding, marking, expression pairs, and exact
    expected value.

    Interpretation: Failure invalidates supported evaluator evidence setup.

    Limitations: Synthetic setup establishes no engine behavior, numerical verification,
    science,
    or UQ.
    """
    maximum = 2**63 - 1
    places = tuple(
        replace(
            place,
            tokens=tuple(
                replace(
                    token,
                    iteration_index=maximum,
                    payload_type_id="type",
                    payload_id=f"payload-{token.token_id}",
                    payload_schema_version=maximum,
                )
                for token in place.tokens
            ),
        )
        for place in executable_net.initial_marking.places
    )
    marking = CpnMarking(1, executable_net.model_id, maximum, places)
    binding = TransitionBinding(
        "execute",
        (TokenBinding("left", "work-1"), TokenBinding("right", "authorization-1")),
    )
    fields = (TokenField.ITERATION_INDEX, TokenField.PAYLOAD_SCHEMA_VERSION)
    pairs = tuple(
        (
            ValueExpression(
                ValueExpressionKind.TOKEN_FIELD, variable="left", field=item
            ),
            ValueExpression(
                ValueExpressionKind.TOKEN_FIELD, variable="right", field=item
            ),
        )
        for item in fields
    )
    return (
        SUT(),
        binding,
        marking,
        pairs,
        ContractValue(ContractValueKind.INTEGER, maximum),
    )


def test_method__evaluate_value__routes_maximum_controls_as_integer(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID: SV-CPN-085

    Requirement: ``evaluate_value`` reads both maximum expression-visible controls as
    INTEGER values.

    Method: Evaluate explicit left/right field reads at ``2**63 - 1`` without warnings.

    Oracle: The signed-i64 maximum and identity-copy semantics fix the exact tagged
    value.

    Acceptance: Every field read equals ``ContractValue(INTEGER, 2**63 - 1)`` exactly.

    Interpretation: Failure means valid maximum routing state is not expression-visible
    as documented.

    Limitations: Synthetic routing excludes arithmetic, engine execution, numerical
    verification,
    scientific validation, UQ, persistence, and cross-language conformance.
    """
    evaluator, binding, marking, pairs, expected = make_maximum_control_context(
        executable_net
    )
    assert all(
        evaluator.evaluate_value(left, binding, marking) == expected
        and evaluator.evaluate_value(right, binding, marking) == expected
        for left, right in pairs
    )
    assert {kind.value for kind in ContractValueKind} == {
        "none",
        "boolean",
        "integer",
        "real",
        "string",
        "string_sequence",
    }


def test_method__evaluate_guard__compares_maximum_controls_exactly(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID: SV-CPN-168

    Requirement: ``evaluate_guard`` compares equal maximum expression-visible controls
    exactly.

    Method: Evaluate explicit equality guards for both maximum control-field pairs.

    Oracle: Each left/right pair is fixed to the same exact signed-i64 maximum.

    Acceptance: Every public guard result value is exactly ``True``.

    Interpretation: Failure identifies guard comparison or controlled setup drift.

    Limitations: Synthetic equality excludes arithmetic, engine execution, numerical
    verification,
    scientific validation, UQ, persistence, and cross-language conformance.
    """
    evaluator, binding, marking, pairs, _expected = make_maximum_control_context(
        executable_net
    )
    assert all(
        evaluator.evaluate_guard(
            GuardExpression(GuardOperator.EQUAL, left=left, right=right),
            binding,
            marking,
        ).value
        is True
        for left, right in pairs
    )


def test_method__evaluate_value__returns_bound_token_field(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID: SV-CPN-010

    Requirement: ``evaluate_value`` returns the exact field of a bound token.

    Method: Evaluate a public RUN_ID field expression for the synthetic ``left``
    binding.

    Oracle: The fixture fixes the bound token run identifier to the literal ``run-1``.

    Acceptance: The result equals ``ContractValue(STRING, "run-1")`` exactly.

    Interpretation: Failure identifies token lookup, field routing, fixture, or contract
    drift.

    Limitations: Other fields, missing bindings, engine execution, science, and UQ are
    excluded.
    """
    marking = executable_net.initial_marking
    binding = TransitionBinding(
        "execute", (TokenBinding("left", "work-1"), TokenBinding("right", "work-1"))
    )
    expression = ValueExpression(
        ValueExpressionKind.TOKEN_FIELD, variable="left", field=TokenField.RUN_ID
    )
    assert SUT().evaluate_value(expression, binding, marking) == ContractValue(
        ContractValueKind.STRING, "run-1"
    )


def test_method__evaluate_value__preserves_bound_token_id_sequence(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID: SV-CPN-169

    Requirement: ``evaluate_value`` preserves ordered repeated bound-token identifiers.

    Method: Evaluate a BOUND_TOKEN_IDS expression over two variables bound to one token.

    Oracle: Variable order fixes the exact repeated tuple ``("work-1", "work-1")``.

    Acceptance: The result equals the exact STRING_SEQUENCE tagged tuple.

    Interpretation: Failure identifies ordered duplicate routing or fixture drift.

    Limitations: Other sequence shapes, missing bindings, engine execution, science, and
    UQ are
    excluded.
    """
    marking = executable_net.initial_marking
    binding = TransitionBinding(
        "execute", (TokenBinding("left", "work-1"), TokenBinding("right", "work-1"))
    )
    expression = ValueExpression(
        ValueExpressionKind.BOUND_TOKEN_IDS, variables=("left", "right")
    )
    assert SUT().evaluate_value(expression, binding, marking) == ContractValue(
        ContractValueKind.STRING_SEQUENCE, ("work-1", "work-1")
    )


def test_method__evaluate_value__rejects_invalid_state(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID: SV-CPN-142

    Requirement: ``CpnExpressionEvaluator`` rejects the documented invalid state for its
    ``evaluate_value`` contract.

    Method: Exercise the retained synthetic invalid inputs through the public SUT.

    Oracle: The documented public invariant and fixed synthetic inputs provide the
    independent
    exact error-taxonomy oracle.

    Acceptance: Every retained invalid call raises the documented exact public
    exception.

    Interpretation: Pass supports only this rejection partition; failure may identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    net = executable_net
    marking = net.initial_marking
    binding = TransitionBinding(
        "execute",
        (
            TokenBinding("left", "work-1"),
            TokenBinding("right", "work-1"),
        ),
    )
    ValueExpression(
        ValueExpressionKind.TOKEN_FIELD,
        variable="left",
        field=TokenField.RUN_ID,
    )
    evaluator = CpnExpressionEvaluator()
    ValueExpression(
        ValueExpressionKind.BOUND_TOKEN_IDS,
        variables=("left", "right"),
    )
    missing_expression = ValueExpression(
        ValueExpressionKind.TOKEN_FIELD,
        variable="missing",
        field=TokenField.RUN_ID,
    )
    with pytest.raises(KeyError):
        evaluator.evaluate_value(missing_expression, binding, marking)
