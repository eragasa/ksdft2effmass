r"""Software verification of ``GuardExpression``.

Facet and represented meaning

--------------------------------------
This module provides software-verification evidence for the public ``GuardExpression``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Intrinsic and cross-object scope

--------------------------------
``GuardExpression`` is the sole primary SUT. Tests exercise its documented public
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
    GuardExpression,
    GuardOperator,
    ValueExpression,
    ValueExpressionKind,
)

pytestmark = pytest.mark.software_verification

SUT = GuardExpression


def test_constructor__fields__guard_arity_is_enforced() -> None:
    """Evidence ID: SV-CPN-007

    Requirement: operator-specific guard arity.

    Method: Exercise the primary SUT through the public construction or operation
    boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: operator-specific guard arity. Prior
    requirement detail: The version-1 P1 contract requires operator-specific guard
    arity. Prior method detail: Construct ``GuardExpression`` for ``NOT`` and ``ALL``
    without required operands. Prior independent oracle detail: The closed grammar
    requires exactly one operand for NOT and at least one for ALL. Prior acceptance
    criterion detail: Both public constructions raise ``ValueError`` containing
    ``arity``. Prior failure interpretation detail: Failure means malformed guards
    became independently valid. Prior limitations detail: Comparison value typing is
    owned by separate evidence.

    Oracle: The documented public rule that the SUT must operator-specific guard arity
    is the
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
    with pytest.raises(ValueError, match="arity"):
        GuardExpression(GuardOperator.NOT)
    with pytest.raises(ValueError, match="arity"):
        GuardExpression(GuardOperator.ALL)


def test_constructor__fields__every_guard_shape_is_publicly_constructible() -> None:
    """Evidence ID: SV-CPN-074

    Requirement: ``GuardExpression`` preserves the exact accepted state for its
    ``fields`` contract.

    Method: Construct the public SUT and inspect retained exact public outcomes.

    Oracle: The documented public invariant and fixed synthetic inputs provide the
    independent
    exact state oracle.

    Acceptance: Every retained exact state assertion holds.

    Interpretation: Pass supports only this accepted-state partition; failure may
    identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
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


def test_constructor__fields__rejects_invalid_state() -> None:
    """Evidence ID: SV-CPN-147

    Requirement: ``GuardExpression`` rejects the documented invalid state for its
    ``fields`` contract.

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
    true = SUT(GuardOperator.TRUE)
    literal = ValueExpression(
        ValueExpressionKind.LITERAL,
        literal=ContractValue(ContractValueKind.INTEGER, 1),
    )
    (
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


def test_constructor__fields__guard_fields_reject_wrong_semantic_types() -> None:
    """Evidence ID: SV-CPN-075

    Requirement: reject non-enum operators and non-guard operand tuples.

    Method: Exercise the primary SUT through the public construction or operation
    boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: reject non-enum operators and non-guard
    operand tuples. Controlled-invalid public construction exercises the error boundary;
    exact documented field types are the oracle. Acceptance requires ``TypeError``
    rather than arity ``ValueError``. Failure permits nondeclarative guard state. No
    collaborator behavior is validated.

    Oracle: The documented public rule that the SUT must reject non-enum operators and
    non-guard
    operand tuples is the contract oracle; fixed synthetic values, Python exact
    type/value semantics, and the public error taxonomy provide independently
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
    with pytest.raises(TypeError, match="operator"):
        SUT("true")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="operands"):
        SUT(GuardOperator.ALL, [SUT(GuardOperator.TRUE)])  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="operands"):
        SUT(GuardOperator.ALL, (True,))  # type: ignore[arg-type]
