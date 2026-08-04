"""Immutable multiset markings and transition bindings for project CPNs.

A marking assigns a tuple-backed multiset of independently identified colored
routing tokens to every place. Canonical lexical order makes representation and
future serialization deterministic without collapsing multiplicity to Boolean
completion. No persistence or engine state is implemented. These are
software-contract objects, not numerical, scientific-validation, or UQ results.
"""

from dataclasses import dataclass

from .tokens import CpnToken

_I64_MAX = 2**63 - 1


@dataclass(frozen=True, slots=True)
class PlaceMarking:
    """Immutable token multiset at one place.

    Parameters
    ----------
    place_id
        Nonempty stable place identity.
    tokens
        Immutable token multiset ordered by token identity without Boolean collapse.

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
    tokens: tuple[CpnToken, ...]

    def __post_init__(self) -> None:
        """Validate intrinsic fields and canonicalize token order.

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
        if type(self.place_id) is not str:
            raise TypeError("place_id must be a string")
        if not self.place_id:
            raise ValueError("place_id must not be empty")
        if not isinstance(self.tokens, tuple) or any(
            not isinstance(token, CpnToken) for token in self.tokens
        ):
            raise TypeError("tokens must be a tuple of CpnToken")
        object.__setattr__(
            self, "tokens", tuple(sorted(self.tokens, key=lambda x: x.token_id))
        )


@dataclass(frozen=True, slots=True)
class CpnMarking:
    """Complete immutable marking for one model revision.

    Parameters
    ----------
    schema_version
        Fixed language-neutral contract version ``1``.
    model_id
        Nonempty stable net/model identity.
    revision
        Dimensionless nonnegative marking revision no greater than signed i64
        maximum.
    places
        Complete immutable place collection, including empty places, ordered
        lexically.

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
    revision: int
    places: tuple[PlaceMarking, ...]

    def __post_init__(self) -> None:
        """Validate intrinsic marking structure and canonicalize place order.

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
            raise TypeError("marking schema_version must be an integer")
        if self.schema_version != 1:
            raise ValueError("marking schema_version must equal 1")
        if type(self.model_id) is not str:
            raise TypeError("marking model_id must be a string")
        if not self.model_id:
            raise ValueError("marking model_id must not be empty")
        if type(self.revision) is not int:
            raise TypeError("marking revision must be an integer")
        if not 0 <= self.revision <= _I64_MAX:
            raise ValueError("marking revision must be nonnegative and fit signed i64")
        if not isinstance(self.places, tuple) or any(
            not isinstance(place, PlaceMarking) for place in self.places
        ):
            raise TypeError("marking places must be a tuple of PlaceMarking")
        object.__setattr__(
            self, "places", tuple(sorted(self.places, key=lambda x: x.place_id))
        )


@dataclass(frozen=True, slots=True)
class TokenBinding:
    """Association between one inscription variable and one token identity.

    Parameters
    ----------
    variable
        Nonempty declarative binding-variable identity.
    token_id
        Nonempty caller-supplied stable token identity.

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
    token_id: str

    def __post_init__(self) -> None:
        """Require nonempty built-in string identities.

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
        for name in ("variable", "token_id"):
            value = getattr(self, name)
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True, slots=True)
class TransitionBinding:
    """Deterministically ordered complete binding for one transition.

    Parameters
    ----------
    transition_id
        Nonempty stable transition identity.
    assignments
        Immutable assignments ordered according to the owning contract.

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
    assignments: tuple[TokenBinding, ...]

    def __post_init__(self) -> None:
        """Validate unique variables and canonicalize assignment order.

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
        if not isinstance(self.assignments, tuple) or any(
            not isinstance(item, TokenBinding) for item in self.assignments
        ):
            raise TypeError("binding assignments must be a tuple of TokenBinding")
        variables = tuple(item.variable for item in self.assignments)
        if len(set(variables)) != len(variables):
            raise ValueError("binding variables must be unique")
        object.__setattr__(
            self,
            "assignments",
            tuple(sorted(self.assignments, key=lambda x: x.variable)),
        )
