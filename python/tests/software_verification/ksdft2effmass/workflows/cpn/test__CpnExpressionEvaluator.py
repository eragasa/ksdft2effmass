"""Evidence class and represented meaning
--------------------------------------
This module provides software-verification evidence for the public
``CpnExpressionEvaluator`` software surface and its finite, exact CPN routing
representation. It does not represent a physical observable or numerical approximation.

Owned contract, oracle, and scope
---------------------------------
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
    """Evidence ID
    -----------
    This helper supports exactly SV-CPN-008, SV-CPN-009 and owns no independent evidence
    ID.

    Requirement
    -----------
    Provide explicit synthetic setup or assertion mechanics without creating an
    independent pass claim.

    Method
    ------
    Construct or transform the public CPN test inputs required by the listed evidence
    owners. Prior helper description: Construct a typed literal for synthetic expression
    tests.

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
    return ValueExpression(
        ValueExpressionKind.LITERAL,
        literal=ContractValue(kind, value),  # type: ignore[arg-type]
    )


def test_method__contract__exact_literals_evaluate_without_state() -> None:
    """Evidence ID
    -----------
    SV-CPN-008

    Requirement
    -----------
    exact literal ordering without token state.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
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

    Oracle
    ------
    The documented public rule that the SUT must exact literal ordering without token
    state is the contract oracle; fixed synthetic values, Python exact type/value
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
    marking = CpnMarking(1, "model", 0, ())
    binding = TransitionBinding("transition", ())
    guard = GuardExpression(
        GuardOperator.LESS_THAN,
        left=literal(ContractValueKind.INTEGER, 1),
        right=literal(ContractValueKind.INTEGER, 2),
    )
    assert CpnExpressionEvaluator().evaluate_guard(guard, binding, marking).value


def test_method__contract__comparison_rejects_mixed_tags() -> None:
    """Evidence ID
    -----------
    SV-CPN-009

    Requirement
    -----------
    type-strict comparison tags.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
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

    Oracle
    ------
    The documented public rule that the SUT must type-strict comparison tags is the
    contract oracle; fixed synthetic values, Python exact type/value semantics, and the
    public error taxonomy provide independently inspectable expected outcomes where
    used.

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
    guard = GuardExpression(
        GuardOperator.EQUAL,
        left=literal(ContractValueKind.INTEGER, 1),
        right=literal(ContractValueKind.REAL, 1.0),
    )
    with pytest.raises(TypeError, match="equal ContractValue kinds"):
        CpnExpressionEvaluator().evaluate_guard(
            guard, TransitionBinding("transition", ()), CpnMarking(1, "model", 0, ())
        )


def test_method__contract__maximum_controls_read_copy_and_compare_as_integer(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-085

    Requirement
    -----------
    maximum expression-visible controls read and copy through INTEGER.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: route maximum control values through
    INTEGER expressions. Requirement: expression evaluation can read, copy, and compare
    every valid expression-visible control at ``2**63 - 1`` without an unsigned value
    kind or arithmetic advancement. Method: replace both independently valid input
    tokens' iteration and payload-version controls, evaluate field reads and equality,
    and inspect the copied public tagged values. Oracle: exact signed-i64 endpoint and
    identity-copy semantics. Acceptance returns INTEGER-tagged maxima and ``True``.
    Failure means valid routing state is not expression-visible. Repeating the value is
    deliberate nonarithmetic routing, not scientific iteration evidence.

    Oracle
    ------
    The documented public rule that the SUT must maximum expression-visible controls
    read and copy through INTEGER is the contract oracle; fixed synthetic values, Python
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
    evaluator = SUT()

    def field(variable: str, token_field: TokenField) -> ValueExpression:
        """Evidence ID
        -----------
        This helper supports exactly SV-CPN-085 and owns no independent evidence ID.

        Requirement
        -----------
        Provide explicit synthetic setup or assertion mechanics without creating an
        independent pass claim.

        Method
        ------
        Construct or transform the public CPN test inputs required by the listed
        evidence owners. Prior helper description: Construct one public field read over
        synthetic maximum controls.

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
        The helper is synthetic, supports only the complete identifier list above, owns
        no independent evidence ID, and establishes no numerical verification,
        scientific validation, uncertainty quantification, physical meaning, or
        cross-language conformance."""
        return ValueExpression(
            ValueExpressionKind.TOKEN_FIELD,
            variable=variable,
            field=token_field,
        )

    for token_field in (TokenField.ITERATION_INDEX, TokenField.PAYLOAD_SCHEMA_VERSION):
        left = field("left", token_field)
        right = field("right", token_field)
        expected = ContractValue(ContractValueKind.INTEGER, maximum)
        assert evaluator.evaluate_value(left, binding, marking) == expected
        assert evaluator.evaluate_value(right, binding, marking) == expected
        comparison = GuardExpression(GuardOperator.EQUAL, left=left, right=right)
        assert evaluator.evaluate_guard(comparison, binding, marking).value is True
    assert {kind.value for kind in ContractValueKind} == {
        "none",
        "boolean",
        "integer",
        "real",
        "string",
        "string_sequence",
    }


def test_method__contract__bound_token_fields_and_id_sequences(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-010

    Requirement
    -----------
    positive token-field and repeated bound-token-ID evaluation.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: positive token-field and repeated
    bound-token-ID evaluation. Prior requirement detail: The version-1 P1 contract
    requires positive token-field and repeated bound-token-ID evaluation. Prior method
    detail: Call ``evaluate_value`` for ``RUN_ID`` and ``BOUND_TOKEN_IDS`` using two
    variables bound to ``work-1``, then request an unbound variable. Prior independent
    oracle detail: The synthetic marking fixes run ID ``run-1``; variable order fixes
    the repeated ID tuple ``('work-1', 'work-1')``. Prior acceptance criterion detail:
    Exact tagged values match those oracles and the absent variable raises ``KeyError``.
    Prior failure interpretation detail: Failure breaks field routing, ordered duplicate
    reads, or documented lookup errors. Prior limitations detail: This does not validate
    a scientific payload or persistence format.

    Oracle
    ------
    The documented public rule that the SUT must positive token-field and repeated
    bound-token-ID evaluation is the contract oracle; fixed synthetic values, Python
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
    net = executable_net
    marking = net.initial_marking
    binding = TransitionBinding(
        "execute",
        (
            TokenBinding("left", "work-1"),
            TokenBinding("right", "work-1"),
        ),
    )
    field_expression = ValueExpression(
        ValueExpressionKind.TOKEN_FIELD,
        variable="left",
        field=TokenField.RUN_ID,
    )
    evaluator = CpnExpressionEvaluator()
    assert evaluator.evaluate_value(
        field_expression, binding, marking
    ) == ContractValue(ContractValueKind.STRING, "run-1")
    ids_expression = ValueExpression(
        ValueExpressionKind.BOUND_TOKEN_IDS,
        variables=("left", "right"),
    )
    assert evaluator.evaluate_value(ids_expression, binding, marking) == ContractValue(
        ContractValueKind.STRING_SEQUENCE,
        ("work-1", "work-1"),
    )
    missing_expression = ValueExpression(
        ValueExpressionKind.TOKEN_FIELD,
        variable="missing",
        field=TokenField.RUN_ID,
    )
    with pytest.raises(KeyError):
        evaluator.evaluate_value(missing_expression, binding, marking)
