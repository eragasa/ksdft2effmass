"""Declarative guard and output-inscription expressions for the CPN contract.

The expression language is a closed, backend-neutral data model. It has no
source-text, callable, lambda, attribute-traversal, import, ``eval``, file, or
external-operation surface. Evaluation is exact routing logic over immutable
bound tokens; it owns no physical units, scientific tolerances, or convergence
policy. Behavior here is software verification, not scientific validation or
uncertainty quantification.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, cast

from .markings import CpnMarking, TransitionBinding
from .tokens import (
    ContractValue,
    ContractValueKind,
    CpnToken,
    OutcomeScope,
    OutcomeStatus,
    OutcomeTerminality,
    TokenField,
)


class ValueExpressionKind(StrEnum):
    """Closed alternatives for obtaining a value.

    Attributes
    ----------
    LITERAL
        Fixed serialized enum value ``literal``.
    TOKEN_FIELD
        Fixed serialized enum value ``token_field``.
    BOUND_TOKEN_IDS
        Fixed serialized enum value ``bound_token_ids``.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    LITERAL = "literal"
    TOKEN_FIELD = "token_field"
    BOUND_TOKEN_IDS = "bound_token_ids"


class GuardOperator(StrEnum):
    """Closed Boolean and exact-comparison guard operators.

    Attributes
    ----------
    TRUE
        Fixed serialized enum value ``true``.
    FALSE
        Fixed serialized enum value ``false``.
    ALL
        Fixed serialized enum value ``all``.
    ANY
        Fixed serialized enum value ``any``.
    NOT
        Fixed serialized enum value ``not``.
    EQUAL
        Fixed serialized enum value ``equal``.
    NOT_EQUAL
        Fixed serialized enum value ``not_equal``.
    LESS_THAN
        Fixed serialized enum value ``less_than``.
    LESS_THAN_OR_EQUAL
        Fixed serialized enum value ``less_than_or_equal``.
    GREATER_THAN
        Fixed serialized enum value ``greater_than``.
    GREATER_THAN_OR_EQUAL
        Fixed serialized enum value ``greater_than_or_equal``.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    TRUE = "true"
    FALSE = "false"
    ALL = "all"
    ANY = "any"
    NOT = "not"
    EQUAL = "equal"
    NOT_EQUAL = "not_equal"
    LESS_THAN = "less_than"
    LESS_THAN_OR_EQUAL = "less_than_or_equal"
    GREATER_THAN = "greater_than"
    GREATER_THAN_OR_EQUAL = "greater_than_or_equal"


@dataclass(frozen=True, slots=True)
class ValueExpression:
    """One invariant-checked declarative value expression.

    Parameters
    ----------
    kind
        Exact enum tag selecting the active representation; enum strings are not
        coerced.
    literal
        Tagged literal active only for a literal expression.
    variable
        Nonempty declarative binding-variable identity.
    field
        Enumerated token field active only for a token-field expression.
    variables
        Ordered variables active only for bound-token identities; resulting token
        identities may repeat.

    Raises
    ------
    TypeError
        A field has the wrong semantic type; enum strings and mutable collections
        are not coerced.
    ValueError
        A correctly typed field violates an intrinsic invariant.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    kind: ValueExpressionKind
    literal: ContractValue | None = None
    variable: str | None = None
    field: TokenField | None = None
    variables: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Enforce exactly one expression representation.

        Raises
        ------
        TypeError
            An owned field has the wrong semantic type.
        ValueError
            A correctly typed owned field violates an intrinsic invariant.

        Notes
        -----
        This private mechanical step owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        if not isinstance(self.kind, ValueExpressionKind):
            raise TypeError("value expression kind must be ValueExpressionKind")
        if not isinstance(self.variables, tuple) or any(
            type(value) is not str for value in self.variables
        ):
            raise TypeError("value expression variables must be a tuple of strings")
        if any(not value for value in self.variables):
            raise ValueError("value expression variables must not be empty")
        if self.kind is ValueExpressionKind.LITERAL:
            valid = (
                isinstance(self.literal, ContractValue)
                and self.variable is None
                and self.field is None
                and not self.variables
            )
        elif self.kind is ValueExpressionKind.TOKEN_FIELD:
            valid = (
                self.literal is None
                and type(self.variable) is str
                and bool(self.variable)
                and isinstance(self.field, TokenField)
                and not self.variables
            )
        else:
            valid = (
                self.literal is None
                and self.variable is None
                and self.field is None
                and bool(self.variables)
            )
        if not valid:
            raise ValueError("value expression fields do not match its kind")


@dataclass(frozen=True, slots=True)
class GuardExpression:
    """Pure Boolean expression with operator-specific arity.

    Parameters
    ----------
    operator
        Closed declarative Boolean or comparison operator.
    operands
        Ordered nested guards with operator-specific arity.
    left
        Left comparison value expression.
    right
        Right comparison value expression.

    Raises
    ------
    TypeError
        A field has the wrong semantic type; enum strings and mutable collections
        are not coerced.
    ValueError
        A correctly typed field violates an intrinsic invariant.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    operator: GuardOperator
    operands: tuple[GuardExpression, ...] = ()
    left: ValueExpression | None = None
    right: ValueExpression | None = None

    def __post_init__(self) -> None:
        """Validate guard arity and reject nondeclarative values.

        Raises
        ------
        TypeError
            An owned field has the wrong semantic type.
        ValueError
            A correctly typed owned field violates an intrinsic invariant.

        Notes
        -----
        This private mechanical step owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        if not isinstance(self.operator, GuardOperator):
            raise TypeError("guard operator must be GuardOperator")
        if not isinstance(self.operands, tuple) or any(
            not isinstance(value, GuardExpression) for value in self.operands
        ):
            raise TypeError("guard operands must be a tuple of GuardExpression")
        constants = {GuardOperator.TRUE, GuardOperator.FALSE}
        composites = {GuardOperator.ALL, GuardOperator.ANY}
        comparisons = set(GuardOperator) - constants - composites - {GuardOperator.NOT}
        if self.operator in constants:
            valid = not self.operands and self.left is None and self.right is None
        elif self.operator in composites:
            valid = bool(self.operands) and self.left is None and self.right is None
        elif self.operator is GuardOperator.NOT:
            valid = len(self.operands) == 1 and self.left is None and self.right is None
        elif self.operator in comparisons:
            valid = (
                not self.operands
                and isinstance(self.left, ValueExpression)
                and isinstance(self.right, ValueExpression)
            )
        else:  # pragma: no cover - exhaustive enum defense
            valid = False
        if not valid:
            raise ValueError("guard fields do not match operator arity")


@dataclass(frozen=True, slots=True)
class TokenFieldAssignment:
    """Assignment of one output-token field from a declarative expression.

    Parameters
    ----------
    field
        Enumerated token field active only for a token-field expression.
    expression
        Closed declarative expression to evaluate.

    Raises
    ------
    TypeError
        A field has the wrong semantic type; enum strings and mutable collections
        are not coerced.
    ValueError
        A correctly typed field violates an intrinsic invariant.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    field: TokenField
    expression: ValueExpression

    def __post_init__(self) -> None:
        """Validate assignment-owned enum and expression types.

        Raises
        ------
        TypeError
            An owned field has the wrong semantic type.
        ValueError
            A correctly typed owned field violates an intrinsic invariant.

        Notes
        -----
        This private mechanical step owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        if not isinstance(self.field, TokenField):
            raise TypeError("assignment field must be TokenField")
        if not isinstance(self.expression, ValueExpression):
            raise TypeError("assignment expression must be ValueExpression")


@dataclass(frozen=True, slots=True)
class TokenTemplate:
    """Declarative template for one produced routing token.

    Parameters
    ----------
    color_id
        Nonempty token-color identity.
    assignments
        Immutable assignments ordered according to the owning contract.
    outcome_status
        Optional status, all-present with the other outcome-template fields.
    outcome_scope
        Optional scope, all-present with the other outcome-template fields.
    outcome_scope_id
        Optional declarative scope-identity expression.
    outcome_terminality
        Optional terminality, all-present with the other outcome-template fields.

    Raises
    ------
    TypeError
        A field has the wrong semantic type; enum strings and mutable collections
        are not coerced.
    ValueError
        A correctly typed field violates an intrinsic invariant.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    color_id: str
    assignments: tuple[TokenFieldAssignment, ...]
    outcome_status: OutcomeStatus | None = None
    outcome_scope: OutcomeScope | None = None
    outcome_scope_id: ValueExpression | None = None
    outcome_terminality: OutcomeTerminality | None = None

    def __post_init__(self) -> None:
        """Validate template structure; model validation checks bound variables.

        Raises
        ------
        TypeError
            An owned field has the wrong semantic type.
        ValueError
            A correctly typed owned field violates an intrinsic invariant.

        Notes
        -----
        This private mechanical step owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """

        if type(self.color_id) is not str:
            raise TypeError("template color_id must be a string")
        if not self.color_id:
            raise ValueError("template color_id must not be empty")
        if not isinstance(self.assignments, tuple) or any(
            not isinstance(value, TokenFieldAssignment) for value in self.assignments
        ):
            raise TypeError("template assignments must be a tuple")
        fields = tuple(value.field for value in self.assignments)
        if len(set(fields)) != len(fields):
            raise ValueError("template assignment fields must be unique")
        required = {
            TokenField.WORKFLOW_ID,
            TokenField.RUN_ID,
            TokenField.ATTEMPT_ID,
            TokenField.ITERATION_INDEX,
            TokenField.PROVENANCE_IDS,
            TokenField.PARENT_TOKEN_IDS,
        }
        if not required.issubset(fields):
            raise ValueError("template is missing required token field assignments")
        outcome_values = (
            self.outcome_status,
            self.outcome_scope,
            self.outcome_scope_id,
            self.outcome_terminality,
        )
        if any(value is not None for value in outcome_values):
            if not (
                isinstance(self.outcome_status, OutcomeStatus)
                and isinstance(self.outcome_scope, OutcomeScope)
                and isinstance(self.outcome_scope_id, ValueExpression)
                and isinstance(self.outcome_terminality, OutcomeTerminality)
            ):
                raise ValueError("outcome template fields must be all present")
            if (
                self.outcome_status is not OutcomeStatus.BLOCKED
                and self.outcome_terminality is not OutcomeTerminality.TERMINAL
            ):
                raise ValueError(
                    "accepted, rejected, and failed template outcomes are terminal"
                )


@dataclass(frozen=True, slots=True)
class GuardEvaluationResult:
    """Immutable result of one pure guard evaluation.

    Parameters
    ----------
    value
        Tagged immutable value whose built-in Python type is determined by ``kind``.

    Raises
    ------
    TypeError
        A field has the wrong semantic type; enum strings and mutable collections
        are not coerced.
    ValueError
        A correctly typed field violates an intrinsic invariant.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    value: bool

    def __post_init__(self) -> None:
        """Require an exact built-in Boolean result.

        Raises
        ------
        TypeError
            An owned field has the wrong semantic type.
        ValueError
            A correctly typed owned field violates an intrinsic invariant.

        Notes
        -----
        This private mechanical step owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        if type(self.value) is not bool:
            raise TypeError("guard result value must be bool")


class CpnExpressionEvaluator:
    """ActionObject for deterministic evaluation over bound immutable tokens.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    def evaluate_value(
        self,
        expression: ValueExpression,
        binding: TransitionBinding,
        marking: CpnMarking,
    ) -> ContractValue:
        """Evaluate one value expression.

        Parameters
        ----------
        expression
            Closed declarative expression to evaluate.
        binding
            Explicit immutable transition binding.
        marking
            Complete immutable marking associated with the operation or result.

        Returns
        -------
        ContractValue
            Exact derived value or new immutable contract state; no hidden state is
            retained.

        Raises
        ------
        TypeError
            The expression or public argument has the wrong semantic type.
        KeyError
            A requested bound variable or token identity is absent, where applicable.

        Notes
        -----
        This explicit operation owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        if not isinstance(expression, ValueExpression):
            raise TypeError("expression must be ValueExpression")
        if not isinstance(binding, TransitionBinding):
            raise TypeError("binding must be TransitionBinding")
        if not isinstance(marking, CpnMarking):
            raise TypeError("marking must be CpnMarking")
        if expression.kind is ValueExpressionKind.LITERAL:
            assert expression.literal is not None
            return expression.literal
        assignments = {item.variable: item.token_id for item in binding.assignments}
        if expression.kind is ValueExpressionKind.BOUND_TOKEN_IDS:
            return ContractValue(
                ContractValueKind.STRING_SEQUENCE,
                tuple(assignments[variable] for variable in expression.variables),
            )
        assert expression.variable is not None and expression.field is not None
        token = self._token_by_id(marking, assignments[expression.variable])
        return self._field_value(token, expression.field)

    def evaluate_guard(
        self,
        guard: GuardExpression,
        binding: TransitionBinding,
        marking: CpnMarking,
    ) -> GuardEvaluationResult:
        """Evaluate a pure guard with exact type-strict comparison semantics.

        Parameters
        ----------
        guard
            Closed declarative guard to evaluate.
        binding
            Explicit immutable transition binding.
        marking
            Complete immutable marking associated with the operation or result.

        Returns
        -------
        GuardEvaluationResult
            Exact derived value or new immutable contract state; no hidden state is
            retained.

        Raises
        ------
        TypeError
            The expression or public argument has the wrong semantic type.
        KeyError
            A requested bound variable or token identity is absent, where applicable.

        Notes
        -----
        This explicit operation owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        if not isinstance(guard, GuardExpression):
            raise TypeError("guard must be GuardExpression")
        operator = guard.operator
        if operator is GuardOperator.TRUE:
            return GuardEvaluationResult(True)
        if operator is GuardOperator.FALSE:
            return GuardEvaluationResult(False)
        if operator is GuardOperator.ALL:
            return GuardEvaluationResult(
                all(
                    self.evaluate_guard(item, binding, marking).value
                    for item in guard.operands
                )
            )
        if operator is GuardOperator.ANY:
            return GuardEvaluationResult(
                any(
                    self.evaluate_guard(item, binding, marking).value
                    for item in guard.operands
                )
            )
        if operator is GuardOperator.NOT:
            return GuardEvaluationResult(
                not self.evaluate_guard(guard.operands[0], binding, marking).value
            )
        assert guard.left is not None and guard.right is not None
        left = self.evaluate_value(guard.left, binding, marking)
        right = self.evaluate_value(guard.right, binding, marking)
        if left.kind is not right.kind:
            raise TypeError("guard comparison requires equal ContractValue kinds")
        if operator is GuardOperator.EQUAL:
            return GuardEvaluationResult(left.value == right.value)
        if operator is GuardOperator.NOT_EQUAL:
            return GuardEvaluationResult(left.value != right.value)
        if left.kind not in {
            ContractValueKind.INTEGER,
            ContractValueKind.REAL,
            ContractValueKind.STRING,
        }:
            raise TypeError("ordering guard requires integer, real, or string values")
        # The equal tag check above establishes a homogeneous ordered pair;
        # this cast expresses that tagged-union refinement to the type checker.
        left_ordered = cast(Any, left.value)
        right_ordered = cast(Any, right.value)
        if operator is GuardOperator.LESS_THAN:
            value = left_ordered < right_ordered
        elif operator is GuardOperator.LESS_THAN_OR_EQUAL:
            value = left_ordered <= right_ordered
        elif operator is GuardOperator.GREATER_THAN:
            value = left_ordered > right_ordered
        else:
            value = left_ordered >= right_ordered
        return GuardEvaluationResult(value)

    @staticmethod
    def _token_by_id(marking: CpnMarking, token_id: str) -> CpnToken:
        """Return one token by stable identity from an immutable marking.

        Parameters
        ----------
        marking
            Complete immutable marking associated with the operation or result.
        token_id
            Nonempty caller-supplied stable token identity.

        Returns
        -------
        CpnToken
            The uniquely identified token borrowed from ``marking``.

        Raises
        ------
        KeyError
            If ``token_id`` is absent from the complete marking.

        Notes
        -----
        This private mechanical step owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        for place in marking.places:
            for token in place.tokens:
                if token.token_id == token_id:
                    return token
        raise KeyError(token_id)

    @staticmethod
    def _field_value(token: CpnToken, field: TokenField) -> ContractValue:
        """Map one public token field to its exact tagged contract value.

        Parameters
        ----------
        token
            Explicit immutable ``token`` contract value used by this owner.
        field
            Enumerated token field active only for a token-field expression.

        Returns
        -------
        ContractValue
            Exact tagged representation of the enumerated token field.

        Raises
        ------
        TypeError
            If an internal token field has no version-1 contract-value mapping.

        Notes
        -----
        This private mechanical step owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        value = getattr(token, field.value)
        if value is None:
            return ContractValue(ContractValueKind.NONE, None)
        if type(value) is int:
            return ContractValue(ContractValueKind.INTEGER, value)
        if type(value) is str:
            return ContractValue(ContractValueKind.STRING, value)
        if isinstance(value, tuple):
            return ContractValue(ContractValueKind.STRING_SEQUENCE, value)
        raise TypeError(f"unsupported token field value for {field.value}")
