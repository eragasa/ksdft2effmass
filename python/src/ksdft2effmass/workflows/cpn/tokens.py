"""Immutable routing-token DataObjects for the backend-neutral CPN contract.

The objects in this module carry control-plane identity, lineage, correlation,
authorization, payload references, and explicitly scoped outcomes.  They do not
contain a scientific payload, perform persistence, generate identities, inspect
external systems, or import a Petri-net engine.  Integers are dimensionless
control indices; no physical units or numerical tolerance occur here.

Construction is software-verification surface only.  It provides no numerical
verification, scientific validation, uncertainty quantification, provenance
verification, or authorization decision.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

_I64_MIN = -(2**63)
_I64_MAX = 2**63 - 1


class ContractValueKind(StrEnum):
    """Stable tags for values admitted by declarative expressions.

    Attributes
    ----------
    NONE
        Fixed serialized enum value ``none``.
    BOOLEAN
        Fixed serialized enum value ``boolean``.
    INTEGER
        Fixed serialized enum value ``integer``.
    REAL
        Fixed serialized enum value ``real``.
    STRING
        Fixed serialized enum value ``string``.
    STRING_SEQUENCE
        Fixed serialized enum value ``string_sequence``.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    NONE = "none"
    BOOLEAN = "boolean"
    INTEGER = "integer"
    REAL = "real"
    STRING = "string"
    STRING_SEQUENCE = "string_sequence"


class OutcomeStatus(StrEnum):
    """Stable workflow outcome states; none implies scientific acceptance.

    Attributes
    ----------
    ACCEPTED
        Fixed serialized enum value ``accepted``.
    REJECTED
        Fixed serialized enum value ``rejected``.
    FAILED
        Fixed serialized enum value ``failed``.
    BLOCKED
        Fixed serialized enum value ``blocked``.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    FAILED = "failed"
    BLOCKED = "blocked"


class OutcomeScope(StrEnum):
    """Level at which an outcome applies.

    Attributes
    ----------
    ATTEMPT
        Fixed serialized enum value ``attempt``.
    BRANCH
        Fixed serialized enum value ``branch``.
    GATE
        Fixed serialized enum value ``gate``.
    WORKFLOW
        Fixed serialized enum value ``workflow``.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    ATTEMPT = "attempt"
    BRANCH = "branch"
    GATE = "gate"
    WORKFLOW = "workflow"


class OutcomeTerminality(StrEnum):
    """Whether an outcome is retained terminally or may be recovered.

    Attributes
    ----------
    TERMINAL
        Fixed serialized enum value ``terminal``.
    RECOVERABLE
        Fixed serialized enum value ``recoverable``.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    TERMINAL = "terminal"
    RECOVERABLE = "recoverable"


class TokenField(StrEnum):
    """Token fields available to declarative guards and output inscriptions.

    Attributes
    ----------
    WORKFLOW_ID
        Fixed serialized enum value ``workflow_id``.
    RUN_ID
        Fixed serialized enum value ``run_id``.
    PARENT_RUN_ID
        Fixed serialized enum value ``parent_run_id``.
    ATTEMPT_ID
        Fixed serialized enum value ``attempt_id``.
    RETRY_PARENT_ATTEMPT_ID
        Fixed serialized enum value ``retry_parent_attempt_id``.
    ITERATION_INDEX
        Fixed serialized enum value ``iteration_index``.
    PAYLOAD_TYPE_ID
        Fixed serialized enum value ``payload_type_id``.
    PAYLOAD_ID
        Fixed serialized enum value ``payload_id``.
    PAYLOAD_SCHEMA_VERSION
        Fixed serialized enum value ``payload_schema_version``.
    PROVENANCE_IDS
        Fixed serialized enum value ``provenance_ids``.
    PARENT_TOKEN_IDS
        Fixed serialized enum value ``parent_token_ids``.
    CORRELATION_ID
        Fixed serialized enum value ``correlation_id``.
    AUTHORIZATION_ID
        Fixed serialized enum value ``authorization_id``.

    Notes
    -----
    This public object owns only the behavior stated above. It performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    WORKFLOW_ID = "workflow_id"
    RUN_ID = "run_id"
    PARENT_RUN_ID = "parent_run_id"
    ATTEMPT_ID = "attempt_id"
    RETRY_PARENT_ATTEMPT_ID = "retry_parent_attempt_id"
    ITERATION_INDEX = "iteration_index"
    PAYLOAD_TYPE_ID = "payload_type_id"
    PAYLOAD_ID = "payload_id"
    PAYLOAD_SCHEMA_VERSION = "payload_schema_version"
    PROVENANCE_IDS = "provenance_ids"
    PARENT_TOKEN_IDS = "parent_token_ids"
    CORRELATION_ID = "correlation_id"
    AUTHORIZATION_ID = "authorization_id"


@dataclass(frozen=True, slots=True)
class ContractValue:
    """One explicitly tagged backend-neutral expression value.

    Parameters
    ----------
    kind
        Exact enum tag selecting the active representation; enum strings are not
        coerced.
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
    ``none`` admits only ``None``; ``boolean`` only exact ``bool``; ``integer``
    only exact built-in ``int`` in signed i64 range; ``real`` only finite exact
    built-in ``int`` or ``float`` input canonicalized to built-in ``float``
    (IEEE-754 binary64); ``string`` only exact built-in ``str``; and
    ``string_sequence`` only a tuple of nonempty built-in strings while preserving
    order and duplicates. Canonicalizing a large integer-valued ``real`` may round
    it to the nearest representable binary64 value. Conversion overflow and a
    nonfinite canonical result are rejected. The intended Rust scalar mappings are
    ``i64`` for ``integer`` and ``f64`` for ``real``. This object performs no
    persistence, external execution, scientific validation, or uncertainty
    quantification.
    """

    kind: ContractValueKind
    value: None | bool | int | float | str | tuple[str, ...]

    def __post_init__(self) -> None:
        """Enforce the tagged-union invariant without implicit coercion.

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
        if not isinstance(self.kind, ContractValueKind):
            raise TypeError("contract value kind must be ContractValueKind")
        value = self.value
        valid = {
            ContractValueKind.NONE: value is None,
            ContractValueKind.BOOLEAN: type(value) is bool,
            ContractValueKind.INTEGER: type(value) is int,
            ContractValueKind.REAL: type(value) in (int, float),
            ContractValueKind.STRING: type(value) is str,
            ContractValueKind.STRING_SEQUENCE: isinstance(value, tuple)
            and all(type(item) is str for item in value),
        }[self.kind]
        if not valid:
            raise TypeError(f"value does not match {self.kind.value} kind")
        if self.kind is ContractValueKind.INTEGER:
            assert type(value) is int
            if not _I64_MIN <= value <= _I64_MAX:
                raise ValueError("integer contract value must fit signed i64")
        if self.kind is ContractValueKind.REAL:
            if type(value) is int:
                try:
                    canonical_real = float(value)
                except OverflowError as exc:
                    raise ValueError("real contract value overflows binary64") from exc
            else:
                assert type(value) is float
                canonical_real = value
            if not math.isfinite(canonical_real):
                raise ValueError("real contract value must be finite binary64")
            object.__setattr__(self, "value", canonical_real)
        if self.kind is ContractValueKind.STRING_SEQUENCE:
            assert isinstance(value, tuple)
            if any(not item for item in value):
                raise ValueError(
                    "string-sequence entries must be nonempty; ordered duplicates "
                    "are preserved"
                )


@dataclass(frozen=True, slots=True)
class TokenOutcome:
    """Explicit status, scope, identity, and terminality of an outcome.

    Parameters
    ----------
    status
        Explicit workflow-control outcome status.
    scope
        Attempt, branch, gate, or workflow scope.
    scope_id
        Nonempty identity of the affected scope.
    terminality
        Terminal or recoverable outcome classification.

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

    status: OutcomeStatus
    scope: OutcomeScope
    scope_id: str
    terminality: OutcomeTerminality

    def __post_init__(self) -> None:
        """Validate reachable status/terminality combinations.

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
        if not isinstance(self.status, OutcomeStatus):
            raise TypeError("outcome status must be OutcomeStatus")
        if not isinstance(self.scope, OutcomeScope):
            raise TypeError("outcome scope must be OutcomeScope")
        if type(self.scope_id) is not str:
            raise TypeError("outcome scope_id must be a string")
        if not self.scope_id:
            raise ValueError("outcome scope_id must not be empty")
        if not isinstance(self.terminality, OutcomeTerminality):
            raise TypeError("outcome terminality must be OutcomeTerminality")
        if (
            self.status is not OutcomeStatus.BLOCKED
            and self.terminality is not OutcomeTerminality.TERMINAL
        ):
            raise ValueError("accepted, rejected, and failed outcomes are terminal")


@dataclass(frozen=True, slots=True)
class CpnToken:
    """Immutable, engine-neutral token routing envelope.

    Parameters
    ----------
    token_id
        Nonempty caller-supplied stable token identity.
    color_id
        Nonempty token-color identity.
    workflow_id
        Nonempty workflow identity.
    run_id
        Nonempty run identity.
    parent_run_id
        Optional nonempty parent-run identity.
    attempt_id
        Nonempty attempt identity.
    retry_parent_attempt_id
        Optional prior-attempt identity for retry ancestry.
    iteration_index
        Dimensionless nonnegative control iteration index no greater than signed
        i64 maximum; Boolean is rejected. Version 1 does not advance it
        arithmetically.
    payload_type_id
        Optional payload-type reference, all-present with the other payload fields.
    payload_id
        Optional payload identity, all-present with the other payload fields.
    payload_schema_version
        Optional dimensionless nonnegative payload schema version from zero
        through signed i64 maximum. This field is expression-visible.
    provenance_ids
        Unique set-like provenance-reference tuple stored lexically.
    parent_token_ids
        Unique set-like lineage-reference tuple stored lexically.
    correlation_id
        Optional request/result correlation identity.
    authorization_id
        Optional authorization identity.
    outcome
        Optional explicit workflow outcome; it is not scientific acceptance.

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

    token_id: str
    color_id: str
    workflow_id: str
    run_id: str
    parent_run_id: str | None
    attempt_id: str
    retry_parent_attempt_id: str | None
    iteration_index: int
    payload_type_id: str | None
    payload_id: str | None
    payload_schema_version: int | None
    provenance_ids: tuple[str, ...]
    parent_token_ids: tuple[str, ...]
    correlation_id: str | None
    authorization_id: str | None
    outcome: TokenOutcome | None = None

    def __post_init__(self) -> None:
        """Validate owned fields and canonicalize set-like identity tuples.

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
        for name in ("token_id", "color_id", "workflow_id", "run_id", "attempt_id"):
            value = getattr(self, name)
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must not be empty")
        for name in (
            "parent_run_id",
            "retry_parent_attempt_id",
            "payload_type_id",
            "payload_id",
            "correlation_id",
            "authorization_id",
        ):
            value = getattr(self, name)
            if value is not None and type(value) is not str:
                raise TypeError(f"{name} must be a string or None")
            if value == "":
                raise ValueError(f"{name} must not be empty")
        if type(self.iteration_index) is not int:
            raise TypeError("iteration_index must be an integer")
        if not 0 <= self.iteration_index <= _I64_MAX:
            raise ValueError("iteration_index must be nonnegative and fit signed i64")
        present = (
            self.payload_type_id is not None,
            self.payload_id is not None,
            self.payload_schema_version is not None,
        )
        if any(present) and not all(present):
            raise ValueError(
                "payload reference fields must be all present or all absent"
            )
        if self.payload_schema_version is not None:
            if type(self.payload_schema_version) is not int:
                raise TypeError("payload_schema_version must be an integer or None")
            if not 0 <= self.payload_schema_version <= _I64_MAX:
                raise ValueError(
                    "payload_schema_version must be nonnegative and fit signed i64"
                )
        for name in ("provenance_ids", "parent_token_ids"):
            values = getattr(self, name)
            if not isinstance(values, tuple):
                raise TypeError(f"{name} must be a tuple")
            if any(type(value) is not str for value in values):
                raise TypeError(f"{name} entries must be strings")
            if any(not value for value in values):
                raise ValueError(f"{name} entries must not be empty")
            if len(set(values)) != len(values):
                raise ValueError(f"{name} entries must be unique")
            object.__setattr__(self, name, tuple(sorted(values)))
        if self.outcome is not None and not isinstance(self.outcome, TokenOutcome):
            raise TypeError("outcome must be TokenOutcome or None")
