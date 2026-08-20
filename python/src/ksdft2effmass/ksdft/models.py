"""Representation-neutral Kohn--Sham observations.

These immutable objects represent only spectral and total-energy semantics
observed in the retained artifact. Numeric fields accept built-in Python scalar
and tuple types only; booleans, numeric strings, NumPy scalars, and nonfinite
values are rejected rather than converted. Eigenvalues are ordered Kohn--Sham
observations, not a complete many-body spectrum or a uniquely identified
basis-independent operator.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

type Spectrum = tuple[tuple[float, ...], ...]


class EnergyUnit(StrEnum):
    """Concrete energy units demonstrated by retained observations."""

    HARTREE = "hartree"


class Availability(StrEnum):
    """Availability states needed by the retained Kohn--Sham artifact."""

    AVAILABLE = "available"
    NOT_REPRESENTED = "not_represented"
    NO_SPIN_RESOLVED_ARRAYS = "no_spin_resolved_arrays"


def _require_enum(value: object, enum_type: type[StrEnum], name: str) -> None:
    if type(value) is not enum_type:
        raise TypeError(f"{name} must be {enum_type.__name__}")


@dataclass(frozen=True, slots=True)
class KohnShamSpectralObservations:
    """Ordered Kohn--Sham eigenvalues and occupations at sampled k points.

    Attributes
    ----------
    eigenvalues
        Nonempty tuple of nonempty finite built-in-float rows in sampled-point
        order. Every row contains ``band_count`` values.
    eigenvalue_unit
        Must be :attr:`EnergyUnit.HARTREE`.
    occupations
        ``None`` or finite built-in-float rows with the eigenvalue shape.
    band_count
        Positive built-in integer; booleans are rejected.
    spin_channel_availability
        Must be :attr:`Availability.NO_SPIN_RESOLVED_ARRAYS` for the retained
        representation.
    energy_reference_availability
        Must be :attr:`Availability.NOT_REPRESENTED`.
    """

    eigenvalues: Spectrum
    eigenvalue_unit: EnergyUnit
    occupations: Spectrum | None
    band_count: int
    spin_channel_availability: Availability
    energy_reference_availability: Availability

    def __post_init__(self) -> None:
        if type(self.band_count) is not int:
            raise TypeError("band_count must be a built-in integer")
        if self.band_count <= 0:
            raise ValueError("band_count must be positive")
        if type(self.eigenvalues) is not tuple:
            raise TypeError("eigenvalues must be a tuple")
        if not self.eigenvalues:
            raise ValueError("eigenvalues must be nonempty")
        for row in self.eigenvalues:
            self._row(row, "eigenvalues")
            if len(row) != self.band_count:
                raise ValueError("eigenvalue rows must have band_count entries")
        _require_enum(self.eigenvalue_unit, EnergyUnit, "eigenvalue_unit")
        if self.eigenvalue_unit is not EnergyUnit.HARTREE:
            raise ValueError("retained eigenvalue unit must be hartree")
        if self.occupations is not None:
            if type(self.occupations) is not tuple:
                raise TypeError("occupations must be a tuple or None")
            if len(self.occupations) != len(self.eigenvalues):
                raise ValueError("occupation and eigenvalue shapes must agree")
            for occupation_row, eigenvalue_row in zip(
                self.occupations, self.eigenvalues, strict=True
            ):
                self._row(occupation_row, "occupations")
                if len(occupation_row) != len(eigenvalue_row):
                    raise ValueError("occupation and eigenvalue shapes must agree")
        _require_enum(
            self.spin_channel_availability,
            Availability,
            "spin_channel_availability",
        )
        _require_enum(
            self.energy_reference_availability,
            Availability,
            "energy_reference_availability",
        )
        if self.spin_channel_availability is not Availability.NO_SPIN_RESOLVED_ARRAYS:
            raise ValueError(
                "retained spin-channel state must be explicitly unavailable"
            )
        if self.energy_reference_availability is not Availability.NOT_REPRESENTED:
            raise ValueError("retained energy reference must be explicitly unavailable")

    @staticmethod
    def _row(row: object, name: str) -> None:
        if type(row) is not tuple:
            raise TypeError(f"{name} rows must be tuples")
        if not row:
            raise ValueError(f"{name} rows must be nonempty")
        if any(type(value) is not float for value in row):
            raise TypeError(f"{name} values must be built-in floats")
        if any(not math.isfinite(value) for value in row):
            raise ValueError(f"{name} values must be finite")


@dataclass(frozen=True, slots=True)
class TotalEnergyObservation:
    """One representation-neutral observed total energy.

    Attributes
    ----------
    value
        Finite built-in float in ``unit``; no overflow conversion is performed.
    unit
        Must be :attr:`EnergyUnit.HARTREE`.
    reference_availability
        Must be :attr:`Availability.NOT_REPRESENTED`.
    """

    value: float
    unit: EnergyUnit
    reference_availability: Availability

    def __post_init__(self) -> None:
        if type(self.value) is not float:
            raise TypeError("total-energy value must be a built-in float")
        if not math.isfinite(self.value):
            raise ValueError("total-energy value must be finite")
        _require_enum(self.unit, EnergyUnit, "total-energy unit")
        if self.unit is not EnergyUnit.HARTREE:
            raise ValueError("retained total-energy unit must be hartree")
        _require_enum(
            self.reference_availability,
            Availability,
            "total-energy reference_availability",
        )
        if self.reference_availability is not Availability.NOT_REPRESENTED:
            raise ValueError("total-energy reference must be explicitly unavailable")
