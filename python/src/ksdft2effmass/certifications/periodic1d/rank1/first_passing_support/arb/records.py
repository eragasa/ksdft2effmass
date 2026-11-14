"""Immutable records for local Arb enclosure computations."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..records import (
    CONSTRUCTION_MESH_SIZE,
    EVALUATION_SIZE,
    SUPPORT_INVENTORY,
    ExactRational,
    NonnegativeExactInterval,
)


@dataclass(frozen=True, slots=True)
class SignedExactInterval(BaseTypedRecord):
    """Represent one signed closed interval with exact rational endpoints.

    Parameters
    ----------
    lower
        Exact inclusive lower endpoint.
    upper
        Exact inclusive upper endpoint.

    Raises
    ------
    TypeError
        An endpoint is not :class:`ExactRational`.
    ValueError
        The lower endpoint exceeds the upper endpoint.

    Notes
    -----
    Endpoints use arbitrary-precision built-in integers through `ExactRational`; there
    is no fixed-width overflow. Construction establishes ordering only, not containment.
    """

    lower: ExactRational
    upper: ExactRational

    def __post_init__(self) -> None:
        """Validate exact endpoint types and closed-interval ordering."""
        if not isinstance(self.lower, ExactRational):
            raise TypeError("lower must be ExactRational")
        if not isinstance(self.upper, ExactRational):
            raise TypeError("upper must be ExactRational")
        if self.lower.as_fraction() > self.upper.as_fraction():
            raise ValueError("interval lower endpoint must not exceed upper endpoint")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {"lower": self.lower.to_dict(), "upper": self.upper.to_dict()}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _fields(values, {"lower", "upper"}, "signed exact interval")
        return cls(
            lower=ExactRational.from_dict(_mapping_value(values, "lower")),
            upper=ExactRational.from_dict(_mapping_value(values, "upper")),
        )


@dataclass(frozen=True, slots=True)
class ControlledParentLowestEigenvalueEnclosure(BaseTypedRecord):
    """Retain one lowest-eigenvalue enclosure for the frozen four-state parent.

    Parameters
    ----------
    reduced_momentum
        Exact dimensionless reduced reciprocal coordinate.
    working_precision_bits
        Dimensionless built-in integer Arb precision, at least 64 bits.
    interval
        Signed lowest-eigenvalue interval in `E_ref`.

    Notes
    -----
    Python integers have no fixed-width overflow. Extremely large coordinate or
    precision values remain an operational resource concern.
    """

    reduced_momentum: ExactRational
    working_precision_bits: int
    interval: SignedExactInterval

    def __post_init__(self) -> None:
        """Validate exact coordinate, precision, and interval values."""
        if not isinstance(self.reduced_momentum, ExactRational):
            raise TypeError("reduced_momentum must be ExactRational")
        _require_precision(self.working_precision_bits)
        if not isinstance(self.interval, SignedExactInterval):
            raise TypeError("interval must be SignedExactInterval")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "reduced_momentum": self.reduced_momentum.to_dict(),
            "working_precision_bits": self.working_precision_bits,
            "interval": self.interval.to_dict(),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _fields(
            values,
            {"reduced_momentum", "working_precision_bits", "interval"},
            "controlled-parent eigenvalue enclosure",
        )
        return cls(
            reduced_momentum=ExactRational.from_dict(
                _mapping_value(values, "reduced_momentum")
            ),
            working_precision_bits=_int_value(values, "working_precision_bits"),
            interval=SignedExactInterval.from_dict(_mapping_value(values, "interval")),
        )


@dataclass(frozen=True, slots=True)
class MediatedMaximumErrorEnclosure(BaseTypedRecord):
    """Retain one transform-mediated maximum-error enclosure.

    Parameters
    ----------
    maximum_range
        Dimensionless ordinary support in the closed inventory `0..15`.
    working_precision_bits
        Dimensionless built-in integer Arb precision, at least 64 bits.
    interval
        Nonnegative total maximum evaluation-error interval in `E_ref`.
    lower_witness_index
        Dimensionless evaluation index attaining the exported maximum lower endpoint.
    upper_driver_index
        Dimensionless evaluation index attaining the exported maximum upper endpoint.

    Notes
    -----
    The frozen construction size is 256 and the frozen staggered evaluation size is
    1025. This record covers the mediated objective only; it is not a complete
    first-passing certificate.
    """

    maximum_range: int
    working_precision_bits: int
    interval: NonnegativeExactInterval
    lower_witness_index: int
    upper_driver_index: int

    def __post_init__(self) -> None:
        """Validate support, precision, interval, and evaluation indices."""
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int excluding bool")
        if self.maximum_range not in SUPPORT_INVENTORY:
            raise ValueError("maximum_range is outside the frozen support inventory")
        _require_precision(self.working_precision_bits)
        if not isinstance(self.interval, NonnegativeExactInterval):
            raise TypeError("interval must be NonnegativeExactInterval")
        for name, value in (
            ("lower_witness_index", self.lower_witness_index),
            ("upper_driver_index", self.upper_driver_index),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int excluding bool")
            if not 0 <= value < EVALUATION_SIZE:
                raise ValueError(f"{name} must index the frozen evaluation mesh")

    @property
    def construction_mesh_size(self) -> int:
        """Return the fixed dimensionless construction-mesh size.

        Returns
        -------
        int
            The exact value 256.
        """
        return CONSTRUCTION_MESH_SIZE

    @property
    def evaluation_mesh_size(self) -> int:
        """Return the fixed dimensionless evaluation-mesh size.

        Returns
        -------
        int
            The exact value 1025.
        """
        return EVALUATION_SIZE

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "maximum_range": self.maximum_range,
            "working_precision_bits": self.working_precision_bits,
            "interval": self.interval.to_dict(),
            "lower_witness_index": self.lower_witness_index,
            "upper_driver_index": self.upper_driver_index,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _fields(
            values,
            {
                "maximum_range",
                "working_precision_bits",
                "interval",
                "lower_witness_index",
                "upper_driver_index",
            },
            "mediated maximum-error enclosure",
        )
        return cls(
            maximum_range=_int_value(values, "maximum_range"),
            working_precision_bits=_int_value(values, "working_precision_bits"),
            interval=NonnegativeExactInterval.from_dict(
                _mapping_value(values, "interval")
            ),
            lower_witness_index=_int_value(values, "lower_witness_index"),
            upper_driver_index=_int_value(values, "upper_driver_index"),
        )


def _require_precision(value: int) -> None:
    if type(value) is not int:
        raise TypeError("working_precision_bits must be a built-in int excluding bool")
    if value < 64:
        raise ValueError("working_precision_bits must be at least 64")


def _fields(
    values: Mapping[str, SerializableValue],
    expected: set[str],
    label: str,
) -> None:
    if set(values) != expected:
        raise ValueError(f"{label} fields do not match")


def _int_value(values: Mapping[str, SerializableValue], key: str) -> int:
    value = values[key]
    if type(value) is not int:
        raise TypeError(f"{key} must decode to a built-in int excluding bool")
    return value


def _mapping_value(
    values: Mapping[str, SerializableValue],
    key: str,
) -> Mapping[str, SerializableValue]:
    value = values[key]
    if not isinstance(value, Mapping):
        raise TypeError(f"{key} must decode to a mapping")
    return value


__all__ = [
    "ControlledParentLowestEigenvalueEnclosure",
    "MediatedMaximumErrorEnclosure",
    "SignedExactInterval",
]
