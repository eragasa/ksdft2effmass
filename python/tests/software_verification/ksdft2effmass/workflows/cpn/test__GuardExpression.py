"""Software verification for ``GuardExpression`` as the sole primary SUT.

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
    GuardExpression,
    GuardOperator,
    ValueExpression,
    ValueExpressionKind,
)

pytestmark = pytest.mark.software_verification

SUT = GuardExpression


def test_cpn_sv_p1_007_guard_arity_is_enforced() -> None:
    """SV-CPN-007: operator-specific guard arity.

    Requirement
    -----------
    The version-1 P1 contract requires operator-specific guard arity.

    Method
    ------
    Construct ``GuardExpression`` for ``NOT`` and ``ALL`` without required operands.

    Independent oracle
    ------------------
    The closed grammar requires exactly one operand for NOT and at least one for
    ALL.

    Acceptance criterion
    --------------------
    Both public constructions raise ``ValueError`` containing ``arity``.

    Failure interpretation
    ----------------------
    Failure means malformed guards became independently valid.

    Limitations
    -----------
    Comparison value typing is owned by separate evidence.
    """
    with pytest.raises(ValueError, match="arity"):
        GuardExpression(GuardOperator.NOT)
    with pytest.raises(ValueError, match="arity"):
        GuardExpression(GuardOperator.ALL)


def test_cpn_sv_p1_074_every_guard_shape_is_publicly_constructible() -> None:
    """SV-CPN-074: admit every constant, composite, unary, and comparison shape.

    Method constructs the closed public forms; the operator arity table is the
    independent oracle. Acceptance retains exact operands for all operator groups.
    Failure leaves a documented declarative branch unreachable. Evaluation and
    scientific meaning are excluded.
    """
    true = SUT(GuardOperator.TRUE)
    literal = ValueExpression(
        ValueExpressionKind.LITERAL,
        literal=ContractValue(ContractValueKind.INTEGER, 1),
    )
    guards = (
        SUT(GuardOperator.FALSE),
        SUT(GuardOperator.ALL, (true,)),
        SUT(GuardOperator.ANY, (true,)),
        SUT(GuardOperator.NOT, (true,)),
    ) + tuple(
        SUT(operator, left=literal, right=literal)
        for operator in set(GuardOperator)
        - {
            GuardOperator.TRUE,
            GuardOperator.FALSE,
            GuardOperator.ALL,
            GuardOperator.ANY,
            GuardOperator.NOT,
        }
    )
    assert {guard.operator for guard in guards} == set(GuardOperator) - {
        GuardOperator.TRUE
    }
    with pytest.raises(ValueError, match="arity"):
        SUT(GuardOperator.TRUE, left=literal)
    with pytest.raises(ValueError, match="arity"):
        SUT(GuardOperator.ALL, (true,), left=literal)
    with pytest.raises(ValueError, match="arity"):
        SUT(GuardOperator.NOT, (true, true))
    with pytest.raises(ValueError, match="arity"):
        SUT(GuardOperator.EQUAL, left=literal)
    with pytest.raises(ValueError, match="arity"):
        SUT(GuardOperator.EQUAL, left=True, right=literal)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="arity"):
        SUT(GuardOperator.EQUAL, left=literal, right=True)  # type: ignore[arg-type]


def test_cpn_sv_p1_075_guard_fields_reject_wrong_semantic_types() -> None:
    """SV-CPN-075: reject non-enum operators and non-guard operand tuples.

    Controlled-invalid public construction exercises the error boundary; exact
    documented field types are the oracle. Acceptance requires ``TypeError``
    rather than arity ``ValueError``. Failure permits nondeclarative guard state.
    No collaborator behavior is validated.
    """
    with pytest.raises(TypeError, match="operator"):
        SUT("true")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="operands"):
        SUT(GuardOperator.ALL, [SUT(GuardOperator.TRUE)])  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="operands"):
        SUT(GuardOperator.ALL, (True,))  # type: ignore[arg-type]
