"""Software verification for ``CpnExpressionEvaluator`` as the sole primary SUT.

Evidence class: software verification. Requirement and strategy are stated per
case; public construction/execution supplies the method and exact state or the
documented exception taxonomy supplies the independent oracle. Passing verifies
only the named class contract. It does not provide numerical verification,
scientific validation, uncertainty quantification, persistence, SNAKES-adapter,
Rust-conformance, or scientific-execution evidence. Collaborators are synthetic
setup only.
"""

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
    """Construct a typed literal for synthetic expression tests."""
    return ValueExpression(
        ValueExpressionKind.LITERAL,
        literal=ContractValue(kind, value),  # type: ignore[arg-type]
    )


def test_cpn_sv_p1_008_exact_literals_evaluate_without_state() -> None:
    """SV-CPN-008: exact literal ordering without token state.

    Requirement
    -----------
    The version-1 P1 contract requires exact literal ordering without token state.

    Method
    ------
    Evaluate an integer-literal ``1 < 2`` guard with
    ``CpnExpressionEvaluator.evaluate_guard`` over an empty binding and marking.

    Independent oracle
    ------------------
    Built-in exact integer ordering is an independent analytical oracle and requires
    no token lookup or tolerance.

    Acceptance criterion
    --------------------
    The returned ``GuardEvaluationResult.value`` is exactly ``True``.

    Failure interpretation
    ----------------------
    False or an exception indicates incorrect literal evaluation.

    Limitations
    -----------
    No numerical tolerance, unit conversion, or scientific comparison is covered.
    """
    marking = CpnMarking(1, "model", 0, ())
    binding = TransitionBinding("transition", ())
    guard = GuardExpression(
        GuardOperator.LESS_THAN,
        left=literal(ContractValueKind.INTEGER, 1),
        right=literal(ContractValueKind.INTEGER, 2),
    )
    assert CpnExpressionEvaluator().evaluate_guard(guard, binding, marking).value


def test_cpn_sv_p1_009_comparison_rejects_mixed_tags() -> None:
    """SV-CPN-009: type-strict comparison tags.

    Requirement
    -----------
    The version-1 P1 contract requires type-strict comparison tags.

    Method
    ------
    Evaluate equality between integer-tagged ``1`` and real-tagged ``1.0`` through
    ``evaluate_guard``.

    Independent oracle
    ------------------
    Equal Python magnitude does not override the contract requirement that
    comparison operands carry the same ``ContractValueKind``.

    Acceptance criterion
    --------------------
    Evaluation raises ``TypeError`` containing ``equal ContractValue kinds``.

    Failure interpretation
    ----------------------
    Success would silently mix integer and real routing semantics.

    Limitations
    -----------
    This mixed-tag case excludes REAL wire canonicalization; that resolved contract
    is covered separately by the ``SV-CPN-080``--``SV-CPN-088`` evidence.
    """
    guard = GuardExpression(
        GuardOperator.EQUAL,
        left=literal(ContractValueKind.INTEGER, 1),
        right=literal(ContractValueKind.REAL, 1.0),
    )
    with pytest.raises(TypeError, match="equal ContractValue kinds"):
        CpnExpressionEvaluator().evaluate_guard(
            guard, TransitionBinding("transition", ()), CpnMarking(1, "model", 0, ())
        )


def test_cpn_sv_p1_085_maximum_controls_read_copy_and_compare_as_integer(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-085: route maximum control values through INTEGER expressions.

    Requirement: expression evaluation can read, copy, and compare every valid
    expression-visible control at ``2**63 - 1`` without an unsigned value kind or
    arithmetic advancement. Method: replace both independently valid input tokens'
    iteration and payload-version controls, evaluate field reads and equality, and
    inspect the copied public tagged values. Oracle: exact signed-i64 endpoint and
    identity-copy semantics. Acceptance returns INTEGER-tagged maxima and ``True``.
    Failure means valid routing state is not expression-visible. Repeating the value
    is deliberate nonarithmetic routing, not scientific iteration evidence.
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
    evaluator = SUT()

    def field(variable: str, token_field: TokenField) -> ValueExpression:
        """Construct one public field read over synthetic maximum controls."""
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


def test_cpn_sv_p1_010_bound_token_fields_and_id_sequences(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-010: positive token-field and repeated bound-token-ID evaluation.

    Requirement
    -----------
    The version-1 P1 contract requires positive token-field and repeated
    bound-token-ID evaluation.

    Method
    ------
    Call ``evaluate_value`` for ``RUN_ID`` and ``BOUND_TOKEN_IDS`` using two
    variables bound to ``work-1``, then request an unbound variable.

    Independent oracle
    ------------------
    The synthetic marking fixes run ID ``run-1``; variable order fixes the repeated
    ID tuple ``('work-1', 'work-1')``.

    Acceptance criterion
    --------------------
    Exact tagged values match those oracles and the absent variable raises
    ``KeyError``.

    Failure interpretation
    ----------------------
    Failure breaks field routing, ordered duplicate reads, or documented lookup
    errors.

    Limitations
    -----------
    This does not validate a scientific payload or persistence format.
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
