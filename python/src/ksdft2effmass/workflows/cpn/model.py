"""Immutable project-owned definition of a Colored Petri Net.

``CpnNetDefinition`` represents
``N = (P, T, A, Sigma, C, G, E, I)``: places, transitions, directed arcs,
colors, place color assignments, pure guards, arc inscriptions, and an initial
multiset marking. Objects define backend-neutral control flow only. They do not
own persistence, external execution, scientific payloads, or SNAKES objects.
Cross-object graph integrity belongs to ``CpnDefinitionValidator``.

The contract is software-verification surface and supplies no numerical
verification, scientific validation, uncertainty quantification, or calculation.
"""

from dataclasses import dataclass
from enum import StrEnum

from .expressions import GuardExpression, TokenTemplate
from .markings import CpnMarking


class ArcDirection(StrEnum):
    """Direction of an arc relative to its transition.

    Attributes
    ----------
    INPUT
        Fixed serialized enum value ``input``.
    OUTPUT
        Fixed serialized enum value ``output``.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    INPUT = "input"
    OUTPUT = "output"


class InputArcMode(StrEnum):
    """Whether input tokens are consumed or retained when firing.

    Attributes
    ----------
    CONSUME
        Fixed serialized enum value ``consume``.
    READ
        Fixed serialized enum value ``read``.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    CONSUME = "consume"
    READ = "read"


@dataclass(frozen=True, slots=True)
class ColorDefinition:
    """One token color and its allowed later-task payload reference types.

    Parameters
    ----------
    color_id
        Nonempty token-color identity.
    description
        Nonempty explanatory text with no machine-readable authority.
    allowed_payload_type_ids
        Unique lexical admitted payload-type identities; empty means no payload.

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
    description: str
    allowed_payload_type_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate strings and canonicalize set-like payload type identities.

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
        _validate_text(self.color_id, "color_id", nonempty=True)
        _validate_text(self.description, "color description", nonempty=True)
        object.__setattr__(
            self,
            "allowed_payload_type_ids",
            _canonical_ids(self.allowed_payload_type_ids, "allowed_payload_type_ids"),
        )


@dataclass(frozen=True, slots=True)
class PlaceDefinition:
    """One place and the nonempty set of colors admissible there.

    Parameters
    ----------
    place_id
        Nonempty stable place identity.
    description
        Nonempty explanatory text with no machine-readable authority.
    allowed_color_ids
        Nonempty unique lexical admitted color identities.

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

    place_id: str
    description: str
    allowed_color_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate intrinsic place fields and canonicalize colors.

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
        _validate_text(self.place_id, "place_id", nonempty=True)
        _validate_text(self.description, "place description", nonempty=True)
        colors = _canonical_ids(self.allowed_color_ids, "allowed_color_ids")
        if not colors:
            raise ValueError("allowed_color_ids must not be empty")
        object.__setattr__(self, "allowed_color_ids", colors)


@dataclass(frozen=True, slots=True)
class TokenPattern:
    """One input variable and its nonempty allowed-color set.

    Parameters
    ----------
    variable
        Nonempty declarative binding-variable identity.
    allowed_color_ids
        Nonempty unique lexical admitted color identities.

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

    variable: str
    allowed_color_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate intrinsic pattern state.

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
        _validate_text(self.variable, "pattern variable", nonempty=True)
        colors = _canonical_ids(self.allowed_color_ids, "allowed_color_ids")
        if not colors:
            raise ValueError("pattern allowed_color_ids must not be empty")
        object.__setattr__(self, "allowed_color_ids", colors)


@dataclass(frozen=True, slots=True)
class InputInscription:
    """Ordered multiset demand on one input arc.

    Parameters
    ----------
    mode
        Read or consume input behavior.
    patterns
        Nonempty ordered multiset demand.

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

    mode: InputArcMode
    patterns: tuple[TokenPattern, ...]

    def __post_init__(self) -> None:
        """Require a mode and at least one declarative token pattern.

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
        if not isinstance(self.mode, InputArcMode):
            raise TypeError("input inscription mode must be InputArcMode")
        if not isinstance(self.patterns, tuple) or any(
            not isinstance(pattern, TokenPattern) for pattern in self.patterns
        ):
            raise TypeError("input patterns must be a tuple of TokenPattern")
        if not self.patterns:
            raise ValueError("input patterns must not be empty")


@dataclass(frozen=True, slots=True)
class OutputInscription:
    """Ordered templates produced on one output arc.

    Parameters
    ----------
    templates
        Nonempty ordered output templates.

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

    templates: tuple[TokenTemplate, ...]

    def __post_init__(self) -> None:
        """Require at least one immutable token template.

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
        if not isinstance(self.templates, tuple) or any(
            not isinstance(template, TokenTemplate) for template in self.templates
        ):
            raise TypeError("output templates must be a tuple of TokenTemplate")
        if not self.templates:
            raise ValueError("output templates must not be empty")


@dataclass(frozen=True, slots=True)
class TransitionDefinition:
    """One transition with a pure declarative guard.

    Parameters
    ----------
    transition_id
        Nonempty stable transition identity.
    description
        Nonempty explanatory text with no machine-readable authority.
    guard
        Closed declarative guard to evaluate.

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
    description: str
    guard: GuardExpression

    def __post_init__(self) -> None:
        """Validate transition-owned fields.

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
        _validate_text(self.transition_id, "transition_id", nonempty=True)
        _validate_text(self.description, "transition description", nonempty=True)
        if not isinstance(self.guard, GuardExpression):
            raise TypeError("transition guard must be GuardExpression")


@dataclass(frozen=True, slots=True)
class ArcDefinition:
    """Directed place/transition arc carrying exactly one inscription kind.

    Parameters
    ----------
    arc_id
        Nonempty stable arc identity.
    place_id
        Nonempty stable place identity.
    transition_id
        Nonempty stable transition identity.
    direction
        Input or output direction relative to the transition.
    input_inscription
        Input inscription exactly for an input arc; otherwise ``None``.
    output_inscription
        Output inscription exactly for an output arc; otherwise ``None``.

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

    arc_id: str
    place_id: str
    transition_id: str
    direction: ArcDirection
    input_inscription: InputInscription | None = None
    output_inscription: OutputInscription | None = None

    def __post_init__(self) -> None:
        """Validate intrinsic direction/inscription consistency.

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
        for name in ("arc_id", "place_id", "transition_id"):
            _validate_text(getattr(self, name), name, nonempty=True)
        if not isinstance(self.direction, ArcDirection):
            raise TypeError("arc direction must be ArcDirection")
        if self.direction is ArcDirection.INPUT:
            valid = (
                isinstance(self.input_inscription, InputInscription)
                and self.output_inscription is None
            )
        else:
            valid = (
                isinstance(self.output_inscription, OutputInscription)
                and self.input_inscription is None
            )
        if not valid:
            raise ValueError("arc inscription must match arc direction")


@dataclass(frozen=True, slots=True)
class CpnNetDefinition:
    """Complete immutable version-1 project CPN definition.

    Parameters
    ----------
    schema_version
        Fixed language-neutral contract version ``1``.
    model_id
        Nonempty stable net/model identity.
    colors
        Canonical immutable color definitions representing Sigma.
    places
        Complete immutable place collection, including empty places, ordered
        lexically.
    transitions
        Canonical immutable transition definitions representing T.
    arcs
        Canonical immutable directed arcs and inscriptions.
    initial_marking
        Complete initial marking for the same model.

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

    schema_version: int
    model_id: str
    colors: tuple[ColorDefinition, ...]
    places: tuple[PlaceDefinition, ...]
    transitions: tuple[TransitionDefinition, ...]
    arcs: tuple[ArcDefinition, ...]
    initial_marking: CpnMarking

    def __post_init__(self) -> None:
        """Validate intrinsic container types and canonicalize stable ordering.

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
        if type(self.schema_version) is not int:
            raise TypeError("net schema_version must be an integer")
        if self.schema_version != 1:
            raise ValueError("net schema_version must equal 1")
        _validate_text(self.model_id, "model_id", nonempty=True)
        collections = (
            ("colors", ColorDefinition, "color_id"),
            ("places", PlaceDefinition, "place_id"),
            ("transitions", TransitionDefinition, "transition_id"),
            ("arcs", ArcDefinition, "arc_id"),
        )
        for name, item_type, identity in collections:
            values = getattr(self, name)
            if not isinstance(values, tuple) or any(
                not isinstance(item, item_type) for item in values
            ):
                raise TypeError(f"{name} must be a tuple of {item_type.__name__}")
            object.__setattr__(
                self, name, tuple(sorted(values, key=lambda x: getattr(x, identity)))
            )
        if not isinstance(self.initial_marking, CpnMarking):
            raise TypeError("initial_marking must be CpnMarking")


def _validate_text(value: object, name: str, *, nonempty: bool) -> None:
    """Mechanically validate a model-owned built-in string field.

    Parameters
    ----------
    value
        Candidate field value; only an exact built-in string is accepted.
    name
        Diagnostic field name used only for deterministic messages.
    nonempty
        Whether the otherwise valid string must contain at least one character.

    Raises
    ------
    TypeError
        If ``value`` is not an exact built-in string.
    ValueError
        If ``nonempty`` is true and ``value`` is empty.

    Notes
    -----
    This private mechanical step owns no physical units, scientific tolerance,
    persistence, external execution, or hidden mutable state.
    """
    if type(value) is not str:
        raise TypeError(f"{name} must be a string")
    if nonempty and not value:
        raise ValueError(f"{name} must not be empty")


def _canonical_ids(values: object, name: str) -> tuple[str, ...]:
    """Validate and lexical-canonicalize a model-owned set-like identity tuple.

    Parameters
    ----------
    values
        Candidate set-like identity tuple.
    name
        Diagnostic field name used only for deterministic messages.

    Returns
    -------
    tuple[str, ...]
        Unique nonempty identifiers in Unicode lexical order.

    Raises
    ------
    TypeError
        If ``values`` is not a tuple of exact built-in strings.
    ValueError
        If an entry is empty or duplicated.

    Notes
    -----
    This private mechanical step owns no physical units, scientific tolerance,
    persistence, external execution, or hidden mutable state.
    """
    if not isinstance(values, tuple) or any(type(value) is not str for value in values):
        raise TypeError(f"{name} must be a tuple of strings")
    if any(not value for value in values):
        raise ValueError(f"{name} entries must not be empty")
    if len(set(values)) != len(values):
        raise ValueError(f"{name} entries must be unique")
    return tuple(sorted(values))
