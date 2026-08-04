"""Structured operational errors for the backend-neutral CPN contract.

Machine-readable error codes and immutable details are authoritative; messages
are explanatory only. Errors report contract validation/evaluation/firing
failures, never a physical, numerical, scientific-validation, or UQ conclusion.
"""

from dataclasses import dataclass
from enum import StrEnum


class CpnErrorCode(StrEnum):
    """Stable operational error codes for version 1.

    Attributes
    ----------
    INVALID_DEFINITION
        Fixed serialized enum value ``invalid_definition``.
    INVALID_MARKING
        Fixed serialized enum value ``invalid_marking``.
    UNKNOWN_TRANSITION
        Fixed serialized enum value ``unknown_transition``.
    INVALID_BINDING
        Fixed serialized enum value ``invalid_binding``.
    TRANSITION_NOT_ENABLED
        Fixed serialized enum value ``transition_not_enabled``.
    GUARD_EVALUATION_FAILED
        Fixed serialized enum value ``guard_evaluation_failed``.
    EXPRESSION_TYPE_MISMATCH
        Fixed serialized enum value ``expression_type_mismatch``.
    OUTPUT_ID_COUNT_MISMATCH
        Fixed serialized enum value ``output_id_count_mismatch``.
    OUTPUT_ID_COLLISION
        Fixed serialized enum value ``output_id_collision``.
    TERMINAL_TOKEN_CONSUMPTION
        Fixed serialized enum value ``terminal_token_consumption``.
    INVALID_PRODUCED_TOKEN
        Fixed serialized enum value ``invalid_produced_token``.
    REVISION_OVERFLOW
        Fixed serialized enum value ``revision_overflow`` for a firing attempted
        from the maximum nonnegative signed i64 marking revision.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    INVALID_DEFINITION = "invalid_definition"
    INVALID_MARKING = "invalid_marking"
    UNKNOWN_TRANSITION = "unknown_transition"
    INVALID_BINDING = "invalid_binding"
    TRANSITION_NOT_ENABLED = "transition_not_enabled"
    GUARD_EVALUATION_FAILED = "guard_evaluation_failed"
    EXPRESSION_TYPE_MISMATCH = "expression_type_mismatch"
    OUTPUT_ID_COUNT_MISMATCH = "output_id_count_mismatch"
    OUTPUT_ID_COLLISION = "output_id_collision"
    TERMINAL_TOKEN_CONSUMPTION = "terminal_token_consumption"
    INVALID_PRODUCED_TOKEN = "invalid_produced_token"
    REVISION_OVERFLOW = "revision_overflow"


@dataclass(frozen=True, slots=True)
class CpnErrorDetail:
    """Immutable machine-readable context retained by every contract error.

    Parameters
    ----------
    code
        Stable authoritative machine-readable enum code.
    message
        Nonempty explanatory diagnostic text; callers must not parse it as a code.
    model_id
        Nonempty stable net/model identity.
    transition_id
        Nonempty stable transition identity.
    place_id
        Nonempty stable place identity.
    token_ids
        Unique lexical nonempty token identities associated with an error.

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

    code: CpnErrorCode
    message: str
    model_id: str | None = None
    transition_id: str | None = None
    place_id: str | None = None
    token_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Validate detail fields and canonicalize token identities.

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
        if not isinstance(self.code, CpnErrorCode):
            raise TypeError("error detail code must be CpnErrorCode")
        if type(self.message) is not str:
            raise TypeError("error detail message must be a string")
        if not self.message:
            raise ValueError("error detail message must not be empty")
        for name in ("model_id", "transition_id", "place_id"):
            value = getattr(self, name)
            if value is not None and type(value) is not str:
                raise TypeError(f"{name} must be a string or None")
            if value == "":
                raise ValueError(f"{name} must not be empty")
        if not isinstance(self.token_ids, tuple) or any(
            type(value) is not str for value in self.token_ids
        ):
            raise TypeError("token_ids must be a tuple of strings")
        if any(not token_id for token_id in self.token_ids):
            raise ValueError("token_ids must not contain empty identities")
        if len(set(self.token_ids)) != len(self.token_ids):
            raise ValueError("token_ids must be unique")
        object.__setattr__(self, "token_ids", tuple(sorted(self.token_ids)))


class CpnContractError(Exception):
    """Base convenience exception retaining a structured error detail.

    Attributes
    ----------
    detail
        Immutable authoritative :class:`CpnErrorDetail` supplied at construction.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    def __init__(self, detail: CpnErrorDetail) -> None:
        """Initialize from one independently valid immutable detail.

        Parameters
        ----------
        detail
            Independently valid immutable structured operational error state.

        Raises
        ------
        TypeError
            If ``detail`` is not :class:`CpnErrorDetail`.

        Notes
        -----
        This private mechanical step owns no physical units, scientific tolerance,
        persistence, external execution, or hidden mutable state.
        """
        if not isinstance(detail, CpnErrorDetail):
            raise TypeError("detail must be CpnErrorDetail")
        self.detail = detail
        super().__init__(detail.message)


class CpnDefinitionError(CpnContractError):
    """A net definition failed executable cross-object validation.

    Attributes
    ----------
    detail
        Immutable structured error detail inherited from ``CpnContractError``.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """


class CpnMarkingError(CpnContractError):
    """A marking is incompatible with its net definition.

    Attributes
    ----------
    detail
        Immutable structured error detail inherited from ``CpnContractError``.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """


class CpnBindingError(CpnContractError):
    """A supplied transition binding is invalid or not enabled.

    Attributes
    ----------
    detail
        Immutable structured error detail inherited from ``CpnContractError``.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """


class CpnGuardEvaluationError(CpnContractError):
    """A declarative guard could not be evaluated type-safely.

    Attributes
    ----------
    detail
        Immutable structured error detail inherited from ``CpnContractError``.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """


class TransitionNotEnabledError(CpnBindingError):
    """A requested transition/binding is not enabled in the current marking.

    Attributes
    ----------
    detail
        Immutable structured error detail inherited from ``CpnContractError``.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """


class CpnFiringError(CpnContractError):
    """A firing request violates output or terminal-token policy.

    Attributes
    ----------
    detail
        Immutable structured error detail inherited from ``CpnContractError``.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """
