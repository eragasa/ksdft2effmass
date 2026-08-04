"""Deterministic enablement and firing ActionObjects for the neutral CPN contract.

Enablement enumerates all multiset bindings in canonical arc/token order and
evaluates only closed declarative guards. Firing returns a new revision, consumes
``consume`` inputs, retains ``read`` inputs, and creates caller-identified output
tokens from declarative templates. ActionObjects retain no state and perform no
I/O, persistence, identity generation, external execution, scientific
calculation, numerical validation, or uncertainty quantification.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from .errors import (
    CpnBindingError,
    CpnDefinitionError,
    CpnErrorCode,
    CpnErrorDetail,
    CpnFiringError,
    CpnGuardEvaluationError,
    CpnMarkingError,
    TransitionNotEnabledError,
)
from .expressions import CpnExpressionEvaluator, TokenTemplate
from .markings import CpnMarking, PlaceMarking, TokenBinding, TransitionBinding
from .model import ArcDirection, CpnNetDefinition, InputArcMode, TokenPattern
from .tokens import (
    ContractValue,
    ContractValueKind,
    CpnToken,
    OutcomeScope,
    OutcomeStatus,
    OutcomeTerminality,
    TokenField,
    TokenOutcome,
)
from .validation import CpnDefinitionValidator, CpnMarkingValidator

_I64_MAX = 2**63 - 1


@dataclass(frozen=True, slots=True)
class TransitionEnablementResult:
    """All enabled bindings for one transition in deterministic order.

    Parameters
    ----------
    transition_id
        Nonempty stable transition identity.
    bindings
        Unique enabled bindings in deterministic token-signature order; every
        binding carries the same ``transition_id`` as this result.

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

    transition_id: str
    bindings: tuple[TransitionBinding, ...]

    def __post_init__(self) -> None:
        """Validate immutable result structure.

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
        if type(self.transition_id) is not str:
            raise TypeError("transition_id must be a string")
        if not self.transition_id:
            raise ValueError("transition_id must not be empty")
        if not isinstance(self.bindings, tuple) or any(
            not isinstance(item, TransitionBinding) for item in self.bindings
        ):
            raise TypeError("bindings must be a tuple of TransitionBinding")
        if any(item.transition_id != self.transition_id for item in self.bindings):
            raise ValueError(
                "every enablement binding must match the result transition_id"
            )
        if len(set(self.bindings)) != len(self.bindings):
            raise ValueError("enablement bindings must be unique")


@dataclass(frozen=True, slots=True)
class FiringRequest:
    """Explicit request to fire one current binding with supplied output IDs.

    Parameters
    ----------
    transition_id
        Nonempty stable transition identity.
    binding
        Explicit immutable transition binding.
    output_token_ids
        Unique nonempty caller-supplied output identities in output-template order.

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

    transition_id: str
    binding: TransitionBinding
    output_token_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate request structure without consulting mutable state.

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
        if type(self.transition_id) is not str:
            raise TypeError("transition_id must be a string")
        if not self.transition_id:
            raise ValueError("transition_id must not be empty")
        if not isinstance(self.binding, TransitionBinding):
            raise TypeError("binding must be TransitionBinding")
        if not isinstance(self.output_token_ids, tuple) or any(
            type(item) is not str for item in self.output_token_ids
        ):
            raise TypeError("output_token_ids must be a tuple of strings")
        if any(not item for item in self.output_token_ids):
            raise ValueError("output_token_ids must not contain empty identities")
        if len(set(self.output_token_ids)) != len(self.output_token_ids):
            raise ValueError("output_token_ids must contain unique identities")


@dataclass(frozen=True, slots=True)
class FiringResult:
    """Immutable audit result and complete successor marking.

    Parameters
    ----------
    transition_id
        Nonempty stable transition identity.
    binding
        Explicit immutable binding whose transition identity matches
        ``transition_id``.
    previous_revision
        Nonnegative revision of the input marking no greater than signed i64
        maximum.
    marking
        Complete immutable successor marking whose revision is exactly
        ``previous_revision + 1``.
    consumed_token_ids
        Unique nonempty consumed identities in canonical order.
    read_token_ids
        Unique nonempty retained identities in canonical order.
    produced_tokens
        New immutable tokens with unique identities in deterministic template order.

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

    transition_id: str
    binding: TransitionBinding
    previous_revision: int
    marking: CpnMarking
    consumed_token_ids: tuple[str, ...]
    read_token_ids: tuple[str, ...]
    produced_tokens: tuple[CpnToken, ...]

    def __post_init__(self) -> None:
        """Validate result-owned structural invariants.

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
        if type(self.transition_id) is not str:
            raise TypeError("transition_id must be a string")
        if not self.transition_id:
            raise ValueError("transition_id must not be empty")
        if not isinstance(self.binding, TransitionBinding):
            raise TypeError("binding must be TransitionBinding")
        if self.binding.transition_id != self.transition_id:
            raise ValueError("firing-result binding must match transition_id")
        if type(self.previous_revision) is not int:
            raise TypeError("previous_revision must be an integer")
        if not 0 <= self.previous_revision <= _I64_MAX:
            raise ValueError("previous_revision must be nonnegative and fit signed i64")
        if not isinstance(self.marking, CpnMarking):
            raise TypeError("marking must be CpnMarking")
        if self.marking.revision != self.previous_revision + 1:
            raise ValueError(
                "firing-result marking revision must equal previous_revision + 1"
            )
        for name in ("consumed_token_ids", "read_token_ids"):
            values = getattr(self, name)
            if not isinstance(values, tuple) or any(
                type(value) is not str for value in values
            ):
                raise TypeError(f"{name} must be a tuple of strings")
            if any(not value for value in values):
                raise ValueError(f"{name} must not contain empty identities")
            if len(set(values)) != len(values):
                raise ValueError(f"{name} must contain unique identities")
        if not isinstance(self.produced_tokens, tuple) or any(
            not isinstance(value, CpnToken) for value in self.produced_tokens
        ):
            raise TypeError("produced_tokens must be a tuple of CpnToken")
        produced_ids = tuple(token.token_id for token in self.produced_tokens)
        if len(set(produced_ids)) != len(produced_ids):
            raise ValueError("produced token identities must be unique")


class TransitionEnabler:
    """ActionObject enumerating every enabled binding deterministically.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    def execute(
        self, net: CpnNetDefinition, marking: CpnMarking, transition_id: str
    ) -> TransitionEnablementResult:
        """Validate state and enumerate all type-correct guard-satisfying bindings.

        Parameters
        ----------
        net
            Immutable CPN definition whose relations are evaluated.
        marking
            Complete immutable marking associated with the operation or result.
        transition_id
            Nonempty stable transition identity.

        Returns
        -------
        TransitionEnablementResult
            Exact derived value or new immutable contract state; no hidden state is
            retained.

        Raises
        ------
        TypeError
            A public argument has the wrong semantic type.
        CpnContractError
            Definition, marking, binding, guard, or firing policy fails as documented by
            structured detail.

        Notes
        -----
        This explicit operation owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        self._validate_inputs(net, marking)
        if type(transition_id) is not str:
            raise TypeError("transition_id must be a string")
        transition = next(
            (item for item in net.transitions if item.transition_id == transition_id),
            None,
        )
        if transition is None:
            raise CpnBindingError(
                self._detail(
                    CpnErrorCode.UNKNOWN_TRANSITION,
                    net,
                    transition_id,
                    "transition is not defined",
                )
            )
        # The complete marking is indexed without mutation so candidate discovery
        # retains place ownership while avoiding order-dependent repeated scans.
        by_place = {item.place_id: item.tokens for item in marking.places}
        # Demands retain canonical arc order and declared pattern order; this is
        # the deterministic multiset-binding coordinate system.
        demands: list[tuple[str, InputArcMode, TokenPattern]] = []
        for arc in sorted(
            (
                item
                for item in net.arcs
                if item.transition_id == transition_id
                and item.direction is ArcDirection.INPUT
            ),
            key=lambda item: item.arc_id,
        ):
            assert arc.input_inscription is not None
            for pattern in arc.input_inscription.patterns:
                demands.append((arc.place_id, arc.input_inscription.mode, pattern))
        # Each tuple preserves canonical token-id order inherited from the
        # PlaceMarking DataObject and excludes terminal tokens from consumption.
        candidate_lists: list[tuple[CpnToken, ...]] = []
        for place_id, mode, pattern in demands:
            candidates = tuple(
                token
                for token in by_place[place_id]
                if token.color_id in pattern.allowed_color_ids
                and not (
                    mode is InputArcMode.CONSUME
                    and token.outcome is not None
                    and token.outcome.terminality is OutcomeTerminality.TERMINAL
                )
            )
            candidate_lists.append(candidates)
        bindings: list[TransitionBinding] = []
        # Cartesian enumeration realizes every multiset choice. An input-free
        # transition has exactly one empty candidate combination.
        choices = product(*candidate_lists) if candidate_lists else [()]
        for selected in choices:
            consumed = [
                token.token_id
                for (_, mode, _), token in zip(demands, selected, strict=True)
                if mode is InputArcMode.CONSUME
            ]
            if len(set(consumed)) != len(consumed):
                continue
            assignment = TransitionBinding(
                transition_id,
                tuple(
                    TokenBinding(pattern.variable, token.token_id)
                    for (_, _, pattern), token in zip(demands, selected, strict=True)
                ),
            )
            try:
                enabled = (
                    CpnExpressionEvaluator()
                    .evaluate_guard(transition.guard, assignment, marking)
                    .value
                )
            except TypeError as exc:
                raise CpnGuardEvaluationError(
                    self._detail(
                        CpnErrorCode.EXPRESSION_TYPE_MISMATCH,
                        net,
                        transition_id,
                        f"guard expression type mismatch: {exc}",
                    )
                ) from exc
            except (KeyError, ValueError) as exc:
                raise CpnGuardEvaluationError(
                    self._detail(
                        CpnErrorCode.GUARD_EVALUATION_FAILED,
                        net,
                        transition_id,
                        f"guard evaluation failed: {exc}",
                    )
                ) from exc
            if enabled:
                bindings.append(assignment)
        bindings.sort(
            key=lambda binding: tuple(
                (item.variable, item.token_id) for item in binding.assignments
            )
        )
        return TransitionEnablementResult(transition_id, tuple(bindings))

    @staticmethod
    def _validate_inputs(net: CpnNetDefinition, marking: CpnMarking) -> None:
        """Translate invalid cross-object state to structured operational errors.

        Parameters
        ----------
        net
            Immutable CPN definition whose relations are evaluated.
        marking
            Complete immutable marking associated with the operation or result.

        Raises
        ------
        CpnDefinitionError
            If cross-object definition validation reports any issue.
        CpnMarkingError
            If the supplied marking is incompatible with the valid definition.

        Notes
        -----
        This private mechanical step owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        definition = CpnDefinitionValidator().execute(net)
        if not definition.is_valid:
            raise CpnDefinitionError(
                CpnErrorDetail(
                    CpnErrorCode.INVALID_DEFINITION,
                    "CPN definition is invalid",
                    model_id=net.model_id,
                )
            )
        marking_result = CpnMarkingValidator().execute(net, marking)
        if not marking_result.is_valid:
            raise CpnMarkingError(
                CpnErrorDetail(
                    CpnErrorCode.INVALID_MARKING,
                    "CPN marking is invalid",
                    model_id=net.model_id,
                )
            )

    @staticmethod
    def _detail(
        code: CpnErrorCode, net: CpnNetDefinition, transition_id: str, message: str
    ) -> CpnErrorDetail:
        """Create deterministic transition-scoped operational detail.

        Parameters
        ----------
        code
            Stable authoritative machine-readable enum code.
        net
            Immutable CPN definition whose relations are evaluated.
        transition_id
            Nonempty stable transition identity.
        message
            Nonempty explanatory diagnostic text; callers must not parse it as a code.

        Returns
        -------
        CpnErrorDetail
            Exact derived value or new immutable contract state; no hidden state is
            retained.

        Notes
        -----
        This private mechanical step owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        return CpnErrorDetail(
            code, message, model_id=net.model_id, transition_id=transition_id
        )


class TransitionFirer:
    """ActionObject producing one immutable successor marking.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    def execute(
        self, net: CpnNetDefinition, marking: CpnMarking, request: FiringRequest
    ) -> FiringResult:
        """Fire one currently enabled binding under deterministic output ordering.

        Parameters
        ----------
        net
            Immutable CPN definition whose relations are evaluated.
        marking
            Complete immutable marking associated with the operation or result.
        request
            Explicit immutable firing request.

        Returns
        -------
        FiringResult
            Exact derived value or new immutable contract state; no hidden state is
            retained.

        Raises
        ------
        TypeError
            A public argument has the wrong semantic type.
        CpnContractError
            Definition, marking, binding, guard, or firing policy fails as documented by
            structured detail.

        Notes
        -----
        This explicit operation owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        # Validate every public semantic type before dereferencing any argument so
        # wrong-type calls follow the documented exception taxonomy.
        if not isinstance(net, CpnNetDefinition):
            raise TypeError("net must be CpnNetDefinition")
        if not isinstance(marking, CpnMarking):
            raise TypeError("marking must be CpnMarking")
        if not isinstance(request, FiringRequest):
            raise TypeError("request must be FiringRequest")
        if request.transition_id != request.binding.transition_id:
            raise CpnBindingError(
                CpnErrorDetail(
                    CpnErrorCode.INVALID_BINDING,
                    "request and binding transition identities differ",
                    model_id=net.model_id,
                    transition_id=request.transition_id,
                )
            )
        input_arcs = sorted(
            (
                arc
                for arc in net.arcs
                if arc.transition_id == request.transition_id
                and arc.direction is ArcDirection.INPUT
            ),
            key=lambda arc: arc.arc_id,
        )
        # Binding and marking identity indexes are derived audit state only; no
        # mutable workflow state is retained by the ActionObject.
        assignments = {
            item.variable: item.token_id for item in request.binding.assignments
        }
        token_lookup = {
            token.token_id: token for place in marking.places for token in place.tokens
        }
        consumed: list[str] = []
        read: list[str] = []
        for arc in input_arcs:
            assert arc.input_inscription is not None
            target = (
                consumed if arc.input_inscription.mode is InputArcMode.CONSUME else read
            )
            for pattern in arc.input_inscription.patterns:
                token_id = assignments.get(pattern.variable)
                if token_id is None:
                    continue
                token = token_lookup.get(token_id)
                if (
                    target is consumed
                    and token is not None
                    and token.outcome is not None
                    and token.outcome.terminality is OutcomeTerminality.TERMINAL
                ):
                    raise CpnFiringError(
                        CpnErrorDetail(
                            CpnErrorCode.TERMINAL_TOKEN_CONSUMPTION,
                            "terminal outcome token cannot be consumed",
                            model_id=net.model_id,
                            transition_id=request.transition_id,
                            token_ids=(token_id,),
                        )
                    )
                target.append(token_id)
        enablement = TransitionEnabler().execute(net, marking, request.transition_id)
        if request.binding not in enablement.bindings:
            raise TransitionNotEnabledError(
                CpnErrorDetail(
                    CpnErrorCode.TRANSITION_NOT_ENABLED,
                    "binding is not enabled in current marking",
                    model_id=net.model_id,
                    transition_id=request.transition_id,
                )
            )
        # A valid maximum-revision marking has no successor representable by the
        # signed INTEGER expression contract. Report this through the established
        # structured firing taxonomy before evaluating outputs or constructing any
        # successor state.
        if marking.revision == _I64_MAX:
            raise CpnFiringError(
                CpnErrorDetail(
                    CpnErrorCode.REVISION_OVERFLOW,
                    "marking revision has no nonnegative signed i64 successor",
                    model_id=net.model_id,
                    transition_id=request.transition_id,
                )
            )
        output_arcs = sorted(
            (
                arc
                for arc in net.arcs
                if arc.transition_id == request.transition_id
                and arc.direction is ArcDirection.OUTPUT
            ),
            key=lambda arc: arc.arc_id,
        )
        # This flattened order is the public positional contract for caller-
        # supplied output identities: lexical arc ID, then template index.
        flattened = tuple(
            (arc, template)
            for arc in output_arcs
            for template in arc.output_inscription.templates  # type: ignore[union-attr]
        )
        if len(request.output_token_ids) != len(flattened):
            raise CpnFiringError(
                CpnErrorDetail(
                    CpnErrorCode.OUTPUT_ID_COUNT_MISMATCH,
                    "output identity count must equal output template count",
                    model_id=net.model_id,
                    transition_id=request.transition_id,
                )
            )
        existing = set(token_lookup)
        requested = request.output_token_ids
        if len(set(requested)) != len(requested) or existing.intersection(requested):
            raise CpnFiringError(
                CpnErrorDetail(
                    CpnErrorCode.OUTPUT_ID_COLLISION,
                    "output identities must be new and unique",
                    model_id=net.model_id,
                    transition_id=request.transition_id,
                    token_ids=requested,
                )
            )
        produced_by_place: dict[str, list[CpnToken]] = {}
        produced: list[CpnToken] = []
        for token_id, (arc, template) in zip(requested, flattened, strict=True):
            try:
                token = self._produce_token(
                    token_id, template, request.binding, marking, net
                )
            except CpnFiringError:
                raise
            except (KeyError, TypeError, ValueError) as exc:
                raise CpnFiringError(
                    CpnErrorDetail(
                        CpnErrorCode.INVALID_PRODUCED_TOKEN,
                        f"output expression produced invalid token state: {exc}",
                        model_id=net.model_id,
                        transition_id=request.transition_id,
                        token_ids=(token_id,),
                    )
                ) from exc
            produced.append(token)
            produced_by_place.setdefault(arc.place_id, []).append(token)
        consumed_set = set(consumed)
        # Consumption and production are applied compositionally to every place,
        # including empty places, so the successor remains a complete marking.
        successor_places = tuple(
            PlaceMarking(
                place.place_id,
                tuple(
                    token
                    for token in place.tokens
                    if token.token_id not in consumed_set
                )
                + tuple(produced_by_place.get(place.place_id, ())),
            )
            for place in marking.places
        )
        successor = CpnMarking(
            1, marking.model_id, marking.revision + 1, successor_places
        )
        if not CpnMarkingValidator().execute(net, successor).is_valid:
            raise CpnFiringError(
                CpnErrorDetail(
                    CpnErrorCode.INVALID_PRODUCED_TOKEN,
                    "produced token is incompatible with output place or color",
                    model_id=net.model_id,
                    transition_id=request.transition_id,
                    token_ids=requested,
                )
            )
        return FiringResult(
            request.transition_id,
            request.binding,
            marking.revision,
            successor,
            tuple(sorted(set(consumed))),
            tuple(sorted(set(read))),
            tuple(produced),
        )

    @staticmethod
    def _produce_token(
        token_id: str,
        template: TokenTemplate,
        binding: TransitionBinding,
        marking: CpnMarking,
        net: CpnNetDefinition,
    ) -> CpnToken:
        """Evaluate one template and construct one immutable routing envelope.

        Parameters
        ----------
        token_id
            Nonempty caller-supplied stable token identity.
        template
            Explicit immutable ``template`` contract value used by this owner.
        binding
            Explicit immutable transition binding.
        marking
            Complete immutable marking associated with the operation or result.
        net
            Immutable CPN definition whose relations are evaluated.

        Returns
        -------
        CpnToken
            New immutable caller-identified routing envelope.

        Raises
        ------
        KeyError
            If a template references an absent binding or token.
        TypeError
            If a template value has the wrong tagged kind.
        CpnFiringError
            If evaluated fields violate a produced-token invariant.

        Notes
        -----
        This private mechanical step owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        evaluator = CpnExpressionEvaluator()
        fields: dict[TokenField, ContractValue] = {
            assignment.field: evaluator.evaluate_value(
                assignment.expression, binding, marking
            )
            for assignment in template.assignments
        }

        def value(
            field: TokenField, kind: ContractValueKind, default: object
        ) -> object:
            """Extract a template value with one exact expected contract tag.

            Parameters
            ----------
            field
                Enumerated token field active only for a token-field expression.
            kind
                Exact enum tag selecting the active representation; enum strings are not
                coerced.
            default
                Documented empty value for an optional unassigned token field.

            Returns
            -------
            object
                Exact derived value or new immutable contract state; no hidden state is
                retained.

            Raises
            ------
            TypeError
                The expression or public argument has the wrong semantic type.
            KeyError
                A requested bound variable or token identity is absent, where
                applicable.

            Notes
            -----
            This explicit operation owns no physical units, scientific tolerance,
            persistence, external execution, or hidden mutable state.
            """
            result = fields.get(field)
            if result is None:
                return default
            if result.kind is not kind:
                raise TypeError(f"{field.value} requires {kind.value}")
            return result.value

        payload_schema_value = fields.get(TokenField.PAYLOAD_SCHEMA_VERSION)
        if (
            payload_schema_value is None
            or payload_schema_value.kind is ContractValueKind.NONE
        ):
            payload_schema: int | None = None
        elif payload_schema_value.kind is ContractValueKind.INTEGER:
            assert type(payload_schema_value.value) is int
            payload_schema = payload_schema_value.value
        else:
            raise TypeError("payload_schema_version requires integer or none")
        optional_strings: dict[TokenField, str | None] = {}
        for field in (
            TokenField.PARENT_RUN_ID,
            TokenField.RETRY_PARENT_ATTEMPT_ID,
            TokenField.PAYLOAD_TYPE_ID,
            TokenField.PAYLOAD_ID,
            TokenField.CORRELATION_ID,
            TokenField.AUTHORIZATION_ID,
        ):
            result = fields.get(field)
            if result is None or result.kind is ContractValueKind.NONE:
                optional_strings[field] = None
            elif result.kind is ContractValueKind.STRING:
                assert type(result.value) is str
                optional_strings[field] = result.value
            else:
                raise TypeError(f"{field.value} requires string or none")
        outcome = None
        if template.outcome_status is not None:
            assert isinstance(template.outcome_status, OutcomeStatus)
            assert isinstance(template.outcome_scope, OutcomeScope)
            assert isinstance(template.outcome_terminality, OutcomeTerminality)
            assert template.outcome_scope_id is not None
            scope_value = evaluator.evaluate_value(
                template.outcome_scope_id, binding, marking
            )
            if scope_value.kind is not ContractValueKind.STRING:
                raise TypeError("outcome scope identity requires string")
            assert type(scope_value.value) is str
            outcome = TokenOutcome(
                template.outcome_status,
                template.outcome_scope,
                scope_value.value,
                template.outcome_terminality,
            )
        try:
            return CpnToken(
                token_id=token_id,
                color_id=template.color_id,
                workflow_id=value(TokenField.WORKFLOW_ID, ContractValueKind.STRING, ""),  # type: ignore[arg-type]
                run_id=value(TokenField.RUN_ID, ContractValueKind.STRING, ""),  # type: ignore[arg-type]
                parent_run_id=optional_strings[TokenField.PARENT_RUN_ID],
                attempt_id=value(TokenField.ATTEMPT_ID, ContractValueKind.STRING, ""),  # type: ignore[arg-type]
                retry_parent_attempt_id=optional_strings[
                    TokenField.RETRY_PARENT_ATTEMPT_ID
                ],
                iteration_index=value(
                    TokenField.ITERATION_INDEX, ContractValueKind.INTEGER, 0
                ),  # type: ignore[arg-type]
                payload_type_id=optional_strings[TokenField.PAYLOAD_TYPE_ID],
                payload_id=optional_strings[TokenField.PAYLOAD_ID],
                payload_schema_version=payload_schema,
                provenance_ids=value(
                    TokenField.PROVENANCE_IDS, ContractValueKind.STRING_SEQUENCE, ()
                ),  # type: ignore[arg-type]
                parent_token_ids=value(
                    TokenField.PARENT_TOKEN_IDS, ContractValueKind.STRING_SEQUENCE, ()
                ),  # type: ignore[arg-type]
                correlation_id=optional_strings[TokenField.CORRELATION_ID],
                authorization_id=optional_strings[TokenField.AUTHORIZATION_ID],
                outcome=outcome,
            )
        except (TypeError, ValueError) as exc:
            raise CpnFiringError(
                CpnErrorDetail(
                    CpnErrorCode.INVALID_PRODUCED_TOKEN,
                    f"output template produced invalid token: {exc}",
                    model_id=net.model_id,
                    token_ids=(token_id,),
                )
            ) from exc
