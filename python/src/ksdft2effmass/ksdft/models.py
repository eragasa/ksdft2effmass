"""Representation-neutral Kohn--Sham observations.

These immutable objects represent only spectral and total-energy semantics
observed in the retained artifact.  Eigenvalues are ordered Kohn--Sham
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


@dataclass(frozen=True, slots=True)
class KohnShamSpectralObservations:
    """Ordered Kohn--Sham eigenvalues and occupations at sampled k points."""

    eigenvalues: Spectrum
    eigenvalue_unit: EnergyUnit
    occupations: Spectrum | None
    band_count: int
    spin_channel_availability: Availability
    energy_reference_availability: Availability

    def __post_init__(self) -> None:
        if type(self.band_count) is not int or self.band_count <= 0:
            raise ValueError("band_count must be a positive built-in integer")
        if type(self.eigenvalues) is not tuple or not self.eigenvalues:
            raise ValueError("eigenvalues must be a nonempty tuple")
        for row in self.eigenvalues:
            self._row(row, "eigenvalues")
            if len(row) != self.band_count:
                raise ValueError("eigenvalue rows must have band_count entries")
        if self.eigenvalue_unit is not EnergyUnit.HARTREE:
            raise ValueError("retained eigenvalue unit must be hartree")
        if self.occupations is not None:
            if type(self.occupations) is not tuple or len(self.occupations) != len(
                self.eigenvalues
            ):
                raise ValueError("occupation and eigenvalue shapes must agree")
            for occupation_row, eigenvalue_row in zip(
                self.occupations, self.eigenvalues, strict=True
            ):
                self._row(occupation_row, "occupations")
                if len(occupation_row) != len(eigenvalue_row):
                    raise ValueError("occupation and eigenvalue shapes must agree")
        if self.spin_channel_availability is not Availability.NO_SPIN_RESOLVED_ARRAYS:
            raise ValueError(
                "retained spin-channel state must be explicitly unavailable"
            )
        if self.energy_reference_availability is not Availability.NOT_REPRESENTED:
            raise ValueError("retained energy reference must be explicitly unavailable")

    @staticmethod
    def _row(row: object, name: str) -> None:
        if type(row) is not tuple or not row:
            raise ValueError(f"{name} rows must be nonempty tuples")
        if any(type(value) is not float or not math.isfinite(value) for value in row):
            raise ValueError(f"{name} values must be finite built-in floats")


@dataclass(frozen=True, slots=True)
class TotalEnergyObservation:
    """One representation-neutral observed total energy."""

    value: float
    unit: EnergyUnit
    reference_availability: Availability

    def __post_init__(self) -> None:
        if type(self.value) is not float or not math.isfinite(self.value):
            raise ValueError("total-energy value must be a finite built-in float")
        if self.unit is not EnergyUnit.HARTREE:
            raise ValueError("retained total-energy unit must be hartree")
        if self.reference_availability is not Availability.NOT_REPRESENTED:
            raise ValueError("total-energy reference must be explicitly unavailable")
