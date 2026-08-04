"""Cross-object validators for CPN definitions and multiset markings.

DataObjects validate intrinsic state; these ActionObjects report graph reference,
binding, color, payload-reference, complete-place-set, and global token-identity
integrity as stable issue codes. Validation is deterministic and has no mutation,
I/O, engine dependency, scientific policy, numerical tolerance, or UQ meaning.
"""

from dataclasses import dataclass
from enum import StrEnum

from .expressions import GuardExpression, ValueExpression, ValueExpressionKind
from .markings import CpnMarking
from .model import ArcDirection, CpnNetDefinition


class CpnIssueCode(StrEnum):
    """Stable version-1 definition and marking validation issue codes.

    Attributes
    ----------
    DUPLICATE_IDENTIFIER
        Fixed serialized enum value ``duplicate_identifier``.
    UNKNOWN_COLOR
        Fixed serialized enum value ``unknown_color``.
    UNKNOWN_PLACE
        Fixed serialized enum value ``unknown_place``.
    UNKNOWN_TRANSITION
        Fixed serialized enum value ``unknown_transition``.
    COLOR_NOT_ALLOWED
        Fixed serialized enum value ``color_not_allowed``.
    PAYLOAD_TYPE_NOT_ALLOWED
        Fixed serialized enum value ``payload_type_not_allowed``.
    DUPLICATE_BINDING_VARIABLE
        Fixed serialized enum value ``duplicate_binding_variable``.
    UNBOUND_VARIABLE
        Fixed serialized enum value ``unbound_variable``.
    MODEL_ID_MISMATCH
        Fixed serialized enum value ``model_id_mismatch``.
    PLACE_SET_MISMATCH
        Fixed serialized enum value ``place_set_mismatch``.
    DUPLICATE_TOKEN_ID
        Fixed serialized enum value ``duplicate_token_id``.
    TOKEN_IN_MULTIPLE_PLACES
        Fixed serialized enum value ``token_in_multiple_places``.
    TOKEN_COLOR_MISMATCH
        Fixed serialized enum value ``token_color_mismatch``.
    INVALID_INITIAL_MARKING
        Fixed serialized enum value ``invalid_initial_marking``.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    DUPLICATE_IDENTIFIER = "duplicate_identifier"
    UNKNOWN_COLOR = "unknown_color"
    UNKNOWN_PLACE = "unknown_place"
    UNKNOWN_TRANSITION = "unknown_transition"
    COLOR_NOT_ALLOWED = "color_not_allowed"
    PAYLOAD_TYPE_NOT_ALLOWED = "payload_type_not_allowed"
    DUPLICATE_BINDING_VARIABLE = "duplicate_binding_variable"
    UNBOUND_VARIABLE = "unbound_variable"
    MODEL_ID_MISMATCH = "model_id_mismatch"
    PLACE_SET_MISMATCH = "place_set_mismatch"
    DUPLICATE_TOKEN_ID = "duplicate_token_id"
    TOKEN_IN_MULTIPLE_PLACES = "token_in_multiple_places"
    TOKEN_COLOR_MISMATCH = "token_color_mismatch"
    INVALID_INITIAL_MARKING = "invalid_initial_marking"


@dataclass(frozen=True, slots=True)
class CpnValidationIssue:
    """One deterministic structured validation finding.

    Parameters
    ----------
    code
        Stable authoritative machine-readable enum code.
    path
        Ordered public-field path locating an issue.
    related_ids
        Unique lexical identities related to an issue.
    message
        Nonempty explanatory diagnostic text; callers must not parse it as a code.

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

    code: CpnIssueCode
    path: tuple[str, ...]
    related_ids: tuple[str, ...]
    message: str

    def __post_init__(self) -> None:
        """Validate issue structure and canonicalize related identities.

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
        if not isinstance(self.code, CpnIssueCode):
            raise TypeError("validation issue code must be CpnIssueCode")
        for name in ("path", "related_ids"):
            value = getattr(self, name)
            if not isinstance(value, tuple) or any(
                type(item) is not str for item in value
            ):
                raise TypeError(f"{name} must be a tuple of strings")
        if any(not related_id for related_id in self.related_ids):
            raise ValueError("related_ids must not contain empty identities")
        if len(set(self.related_ids)) != len(self.related_ids):
            raise ValueError("related_ids must contain unique identities")
        if type(self.message) is not str:
            raise TypeError("validation issue message must be a string")
        if not self.message:
            raise ValueError("validation issue message must not be empty")
        object.__setattr__(self, "related_ids", tuple(sorted(self.related_ids)))


@dataclass(frozen=True, slots=True)
class CpnValidationResult:
    """Immutable ordered collection of cross-object validation issues.

    Parameters
    ----------
    issues
        Ordered immutable findings; empty means valid.

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

    issues: tuple[CpnValidationIssue, ...]

    def __post_init__(self) -> None:
        """Require an immutable issue tuple.

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
        if not isinstance(self.issues, tuple) or any(
            not isinstance(issue, CpnValidationIssue) for issue in self.issues
        ):
            raise TypeError("issues must be a tuple of CpnValidationIssue")

    @property
    def is_valid(self) -> bool:
        """Return ``True`` exactly when no issues were reported.

        Returns
        -------
        bool
            Exact derived value or new immutable contract state; no hidden state is
            retained.

        Notes
        -----
        This explicit operation owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        return not self.issues


class CpnMarkingValidator:
    """ActionObject validating one complete marking against one net.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    def execute(
        self, net: CpnNetDefinition, marking: CpnMarking
    ) -> CpnValidationResult:
        """Report deterministic model, place, identity, color, and payload issues.

        Parameters
        ----------
        net
            Immutable CPN definition whose relations are evaluated.
        marking
            Complete immutable marking associated with the operation or result.

        Returns
        -------
        CpnValidationResult
            Exact derived value or new immutable contract state; no hidden state is
            retained.

        Raises
        ------
        TypeError
            A public argument has the wrong semantic type.

        Notes
        -----
        This explicit operation owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        if not isinstance(net, CpnNetDefinition):
            raise TypeError("net must be CpnNetDefinition")
        if not isinstance(marking, CpnMarking):
            raise TypeError("marking must be CpnMarking")
        issues: list[CpnValidationIssue] = []
        if marking.model_id != net.model_id:
            issues.append(
                self._issue(
                    CpnIssueCode.MODEL_ID_MISMATCH,
                    ("model_id",),
                    (marking.model_id, net.model_id),
                    "marking model_id differs from net",
                )
            )
        # Place identity tuples expose both multiplicity and complete-set
        # compatibility without collapsing a marking to Boolean completion.
        expected_places = tuple(place.place_id for place in net.places)
        actual_places = tuple(place.place_id for place in marking.places)
        if len(set(actual_places)) != len(actual_places):
            issues.append(
                self._issue(
                    CpnIssueCode.DUPLICATE_IDENTIFIER,
                    ("places",),
                    tuple(sorted(set(actual_places))),
                    "marking place identifiers must be unique",
                )
            )
        if set(actual_places) != set(expected_places):
            issues.append(
                self._issue(
                    CpnIssueCode.PLACE_SET_MISMATCH,
                    ("places",),
                    tuple(sorted(set(actual_places))),
                    "marking must represent every and only model place",
                )
            )
        place_defs = {place.place_id: place for place in net.places}
        colors = {color.color_id: color for color in net.colors}
        # The global identity index distinguishes within-place duplication from
        # the same token identity appearing under multiple place owners.
        seen: dict[str, str] = {}
        for place in marking.places:
            definition = place_defs.get(place.place_id)
            local_ids: set[str] = set()
            for token in place.tokens:
                path = ("places", place.place_id, "tokens", token.token_id)
                if token.token_id in local_ids:
                    issues.append(
                        self._issue(
                            CpnIssueCode.DUPLICATE_TOKEN_ID,
                            path,
                            (token.token_id,),
                            "token identity is duplicated in one place",
                        )
                    )
                local_ids.add(token.token_id)
                if token.token_id in seen and seen[token.token_id] != place.place_id:
                    issues.append(
                        self._issue(
                            CpnIssueCode.TOKEN_IN_MULTIPLE_PLACES,
                            path,
                            (token.token_id,),
                            "one token identity occurs in multiple places",
                        )
                    )
                seen[token.token_id] = place.place_id
                if (
                    definition is None
                    or token.color_id not in definition.allowed_color_ids
                ):
                    issues.append(
                        self._issue(
                            CpnIssueCode.TOKEN_COLOR_MISMATCH,
                            path + ("color_id",),
                            (token.color_id,),
                            "token color is not admitted by its place",
                        )
                    )
                color = colors.get(token.color_id)
                if color is None:
                    issues.append(
                        self._issue(
                            CpnIssueCode.UNKNOWN_COLOR,
                            path + ("color_id",),
                            (token.color_id,),
                            "token references an unknown color",
                        )
                    )
                elif (
                    token.payload_type_id is not None
                    and token.payload_type_id not in color.allowed_payload_type_ids
                ):
                    issues.append(
                        self._issue(
                            CpnIssueCode.PAYLOAD_TYPE_NOT_ALLOWED,
                            path + ("payload_type_id",),
                            (token.payload_type_id,),
                            "payload reference type is not admitted by token color",
                        )
                    )
                elif token.payload_type_id is None and color.allowed_payload_type_ids:
                    # Colors may admit listed payload types without requiring one.
                    pass
        return CpnValidationResult(tuple(issues))

    @staticmethod
    def _issue(
        code: CpnIssueCode, path: tuple[str, ...], ids: tuple[str, ...], message: str
    ) -> CpnValidationIssue:
        """Construct one mechanically structured marking issue.

        Parameters
        ----------
        code
            Stable authoritative machine-readable enum code.
        path
            Ordered public-field path locating an issue.
        ids
            Identity tuple retained in a validation issue.
        message
            Nonempty explanatory diagnostic text; callers must not parse it as a code.

        Returns
        -------
        CpnValidationIssue
            Exact derived value or new immutable contract state; no hidden state is
            retained.

        Notes
        -----
        This private mechanical step owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        return CpnValidationIssue(code, path, ids, message)


class CpnDefinitionValidator:
    """ActionObject validating graph references and declarative variable use.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    def execute(self, net: CpnNetDefinition) -> CpnValidationResult:
        """Report deterministic net-definition and initial-marking issues.

        Parameters
        ----------
        net
            Immutable CPN definition whose relations are evaluated.

        Returns
        -------
        CpnValidationResult
            Exact derived value or new immutable contract state; no hidden state is
            retained.

        Raises
        ------
        TypeError
            A public argument has the wrong semantic type.

        Notes
        -----
        This explicit operation owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        if not isinstance(net, CpnNetDefinition):
            raise TypeError("net must be CpnNetDefinition")
        issues: list[CpnValidationIssue] = []
        collections = (
            ("colors", tuple(item.color_id for item in net.colors)),
            ("places", tuple(item.place_id for item in net.places)),
            ("transitions", tuple(item.transition_id for item in net.transitions)),
            ("arcs", tuple(item.arc_id for item in net.arcs)),
        )
        for name, values in collections:
            if len(set(values)) != len(values):
                issues.append(
                    CpnValidationIssue(
                        CpnIssueCode.DUPLICATE_IDENTIFIER,
                        (name,),
                        tuple(sorted(set(values))),
                        f"{name} identifiers must be unique",
                    )
                )
        colors = {item.color_id for item in net.colors}
        places = {item.place_id for item in net.places}
        place_definitions = {item.place_id: item for item in net.places}
        transitions = {item.transition_id for item in net.transitions}
        for place in net.places:
            for color_id in place.allowed_color_ids:
                if color_id not in colors:
                    issues.append(
                        CpnValidationIssue(
                            CpnIssueCode.UNKNOWN_COLOR,
                            ("places", place.place_id, "allowed_color_ids"),
                            (color_id,),
                            "place references unknown color",
                        )
                    )
        # Bound-variable ownership is transition-local. It is collected before
        # guard/template traversal so every expression reference has one owner.
        variables_by_transition: dict[str, set[str]] = {
            item.transition_id: set() for item in net.transitions
        }
        for arc in net.arcs:
            if arc.place_id not in places:
                issues.append(
                    CpnValidationIssue(
                        CpnIssueCode.UNKNOWN_PLACE,
                        ("arcs", arc.arc_id, "place_id"),
                        (arc.place_id,),
                        "arc references unknown place",
                    )
                )
            if arc.transition_id not in transitions:
                issues.append(
                    CpnValidationIssue(
                        CpnIssueCode.UNKNOWN_TRANSITION,
                        ("arcs", arc.arc_id, "transition_id"),
                        (arc.transition_id,),
                        "arc references unknown transition",
                    )
                )
            if arc.direction is ArcDirection.INPUT:
                assert arc.input_inscription is not None
                for pattern in arc.input_inscription.patterns:
                    bound = variables_by_transition.setdefault(arc.transition_id, set())
                    if pattern.variable in bound:
                        issues.append(
                            CpnValidationIssue(
                                CpnIssueCode.DUPLICATE_BINDING_VARIABLE,
                                ("arcs", arc.arc_id),
                                (pattern.variable,),
                                "input variable is bound more than once",
                            )
                        )
                    bound.add(pattern.variable)
                    for color_id in pattern.allowed_color_ids:
                        if color_id not in colors:
                            issues.append(
                                CpnValidationIssue(
                                    CpnIssueCode.UNKNOWN_COLOR,
                                    ("arcs", arc.arc_id),
                                    (color_id,),
                                    "pattern references unknown color",
                                )
                            )
                        input_place = place_definitions.get(arc.place_id)
                        if (
                            input_place is not None
                            and color_id not in input_place.allowed_color_ids
                        ):
                            issues.append(
                                CpnValidationIssue(
                                    CpnIssueCode.COLOR_NOT_ALLOWED,
                                    ("arcs", arc.arc_id),
                                    tuple(sorted({color_id, arc.place_id})),
                                    "input pattern color is not admitted by its place",
                                )
                            )
        for transition in net.transitions:
            bound = variables_by_transition.get(transition.transition_id, set())
            used = self._guard_variables(transition.guard)
            for arc in net.arcs:
                if (
                    arc.transition_id == transition.transition_id
                    and arc.direction is ArcDirection.OUTPUT
                ):
                    assert arc.output_inscription is not None
                    for template in arc.output_inscription.templates:
                        if template.color_id not in colors:
                            issues.append(
                                CpnValidationIssue(
                                    CpnIssueCode.UNKNOWN_COLOR,
                                    ("arcs", arc.arc_id),
                                    (template.color_id,),
                                    "template references unknown color",
                                )
                            )
                        output_place = place_definitions.get(arc.place_id)
                        if (
                            output_place is not None
                            and template.color_id not in output_place.allowed_color_ids
                        ):
                            issues.append(
                                CpnValidationIssue(
                                    CpnIssueCode.COLOR_NOT_ALLOWED,
                                    ("arcs", arc.arc_id),
                                    tuple(sorted({template.color_id, arc.place_id})),
                                    "output template color is not admitted "
                                    "by its place",
                                )
                            )
                        for assignment in template.assignments:
                            used.update(self._value_variables(assignment.expression))
                        if template.outcome_scope_id is not None:
                            used.update(
                                self._value_variables(template.outcome_scope_id)
                            )
            for variable in sorted(used - bound):
                issues.append(
                    CpnValidationIssue(
                        CpnIssueCode.UNBOUND_VARIABLE,
                        ("transitions", transition.transition_id),
                        (variable,),
                        "expression references an unbound variable",
                    )
                )
        marking_result = CpnMarkingValidator().execute(net, net.initial_marking)
        if marking_result.issues:
            issues.append(
                CpnValidationIssue(
                    CpnIssueCode.INVALID_INITIAL_MARKING,
                    ("initial_marking",),
                    (),
                    "initial marking is invalid",
                )
            )
            issues.extend(marking_result.issues)
        return CpnValidationResult(tuple(issues))

    def _guard_variables(self, guard: GuardExpression) -> set[str]:
        """Collect referenced variable names recursively from a pure guard.

        Parameters
        ----------
        guard
            Closed declarative guard to evaluate.

        Returns
        -------
        set[str]
            Exact derived value or new immutable contract state; no hidden state is
            retained.

        Notes
        -----
        This private mechanical step owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        values: set[str] = set()
        for operand in guard.operands:
            values.update(self._guard_variables(operand))
        if guard.left is not None:
            values.update(self._value_variables(guard.left))
        if guard.right is not None:
            values.update(self._value_variables(guard.right))
        return values

    @staticmethod
    def _value_variables(expression: ValueExpression) -> set[str]:
        """Collect variable names from one closed value expression.

        Parameters
        ----------
        expression
            Closed declarative expression to evaluate.

        Returns
        -------
        set[str]
            Exact derived value or new immutable contract state; no hidden state is
            retained.

        Notes
        -----
        This private mechanical step owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        if expression.kind is ValueExpressionKind.TOKEN_FIELD:
            assert expression.variable is not None
            return {expression.variable}
        if expression.kind is ValueExpressionKind.BOUND_TOKEN_IDS:
            return set(expression.variables)
        return set()
