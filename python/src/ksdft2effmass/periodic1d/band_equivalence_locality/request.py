"""Scientific requests for periodic-1D band-equivalence locality analysis."""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

FLAT_PARENT_MODEL_IDENTIFIER = "flat-two-level-parent.v1"
FLAT_REPRESENTED_BASIS_IDENTIFIER = "fixed-real-rank-two-basis.v1"
FLAT_ENERGY_REFERENCE_IDENTIFIER = "positive-reference-energy-E_ref.v1"
FLAT_RECIPROCAL_COORDINATE_CONVENTION = "centered-half-open-reduced-coordinate.v1"
FLAT_GAUGE_ATTACK_IDENTIFIER = "real-sinusoidal-rotation.v1"


@dataclass(frozen=True, slots=True)
class Periodic1DBandEquivalenceLocalityRequest:
    """Bind the finite flat-parent construction and evaluation controls.

    All reported values are dimensionless relative to the positive reference energy
    ``E_ref``.  The construction mesh is centered and half open.  The evaluation mesh
    is shifted by an exact rational fraction and is required to be disjoint from it.
    """

    parent_model_identifier: str
    represented_basis_identifier: str
    energy_reference_identifier: str
    reciprocal_coordinate_convention: str
    gauge_attack_identifier: str
    construction_size: int
    evaluation_size: int
    evaluation_shift_numerator: int
    evaluation_shift_denominator: int
    amplitudes: tuple[float, ...]
    maximum_ranges: tuple[int, ...]
    harmonic_absolute_degeneracy_tolerance: float
    harmonic_relative_degeneracy_tolerance: float
    numerical_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Reject ambiguous scalars and correlated invalid mesh controls."""
        for identifier, identifier_name in (
            (self.parent_model_identifier, "parent_model_identifier"),
            (self.represented_basis_identifier, "represented_basis_identifier"),
            (self.energy_reference_identifier, "energy_reference_identifier"),
            (
                self.reciprocal_coordinate_convention,
                "reciprocal_coordinate_convention",
            ),
            (self.gauge_attack_identifier, "gauge_attack_identifier"),
        ):
            if type(identifier) is not str or not identifier:
                raise TypeError(f"{identifier_name} must be a nonempty built-in string")
        expected_identifiers = {
            "parent_model_identifier": FLAT_PARENT_MODEL_IDENTIFIER,
            "represented_basis_identifier": FLAT_REPRESENTED_BASIS_IDENTIFIER,
            "energy_reference_identifier": FLAT_ENERGY_REFERENCE_IDENTIFIER,
            "reciprocal_coordinate_convention": (FLAT_RECIPROCAL_COORDINATE_CONVENTION),
            "gauge_attack_identifier": FLAT_GAUGE_ATTACK_IDENTIFIER,
        }
        for identifier_name, expected_identifier in expected_identifiers.items():
            if getattr(self, identifier_name) != expected_identifier:
                raise ValueError(
                    f"{identifier_name} must identify the installed flat control"
                )
        for value, name in (
            (self.construction_size, "construction_size"),
            (self.evaluation_size, "evaluation_size"),
            (self.evaluation_shift_numerator, "evaluation_shift_numerator"),
            (self.evaluation_shift_denominator, "evaluation_shift_denominator"),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
        if self.construction_size < 8 or self.construction_size % 2 != 0:
            raise ValueError("construction_size must be an even integer of at least 8")
        if self.evaluation_size < 2 * self.construction_size + 1:
            raise ValueError("evaluation_size must be at least 2*N+1")
        if not (
            0 < self.evaluation_shift_numerator < self.evaluation_shift_denominator
        ):
            raise ValueError("evaluation shift must be a proper positive fraction")
        if type(self.amplitudes) is not tuple or len(self.amplitudes) < 2:
            raise TypeError("amplitudes must contain at least two built-in floats")
        for index, amplitude in enumerate(self.amplitudes):
            if type(amplitude) is not float:
                raise TypeError(f"amplitudes[{index}] must be a built-in float")
            if not math.isfinite(amplitude):
                raise ValueError(f"amplitudes[{index}] must be finite")
            if not 0.0 <= amplitude <= math.pi / 4.0:
                raise ValueError("amplitudes must lie in [0, pi/4]")
        if self.amplitudes[0] != 0.0:
            raise ValueError("amplitudes must begin at zero")
        if tuple(sorted(set(self.amplitudes))) != self.amplitudes:
            raise ValueError("amplitudes must be unique and strictly increasing")
        if type(self.maximum_ranges) is not tuple or not self.maximum_ranges:
            raise TypeError("maximum_ranges must be a nonempty tuple")
        if any(type(value) is not int for value in self.maximum_ranges):
            raise TypeError("maximum_ranges must contain built-in integers")
        if (
            self.maximum_ranges != tuple(sorted(set(self.maximum_ranges)))
            or self.maximum_ranges[0] < 0
        ):
            raise ValueError("maximum_ranges must be nonnegative and increasing")
        if self.maximum_ranges[-1] >= self.construction_size // 2:
            raise ValueError("maximum_ranges must exclude the cyclic Nyquist class")
        for tolerance, tolerance_name in (
            (
                self.harmonic_absolute_degeneracy_tolerance,
                "harmonic_absolute_degeneracy_tolerance",
            ),
            (
                self.harmonic_relative_degeneracy_tolerance,
                "harmonic_relative_degeneracy_tolerance",
            ),
            (self.numerical_absolute_tolerance, "numerical_absolute_tolerance"),
        ):
            if type(tolerance) is not float:
                raise TypeError(f"{tolerance_name} must be a built-in float")
            if not math.isfinite(tolerance) or tolerance < 0.0:
                raise ValueError(f"{tolerance_name} must be finite and nonnegative")
        if (
            self.harmonic_absolute_degeneracy_tolerance == 0.0
            and self.harmonic_relative_degeneracy_tolerance == 0.0
        ):
            raise ValueError("at least one harmonic tolerance must be positive")
        if self.numerical_absolute_tolerance == 0.0:
            raise ValueError("numerical_absolute_tolerance must be positive")
        construction = {
            Fraction(-1, 2) + Fraction(index, self.construction_size)
            for index in range(self.construction_size)
        }
        if construction.intersection(self.evaluation_reduced_momenta_fractional()):
            raise ValueError("construction and evaluation meshes must be disjoint")

    def construction_reduced_momenta(self) -> tuple[float, ...]:
        """Return centered half-open construction coordinates."""
        return tuple(
            float(Fraction(-1, 2) + Fraction(index, self.construction_size))
            for index in range(self.construction_size)
        )

    def evaluation_reduced_momenta_fractional(self) -> tuple[Fraction, ...]:
        """Return the exact shifted evaluation inventory."""
        shift = Fraction(
            self.evaluation_shift_numerator,
            self.evaluation_shift_denominator,
        )
        return tuple(
            Fraction(-1, 2) + (Fraction(index, 1) + shift) / self.evaluation_size
            for index in range(self.evaluation_size)
        )

    def evaluation_reduced_momenta(self) -> tuple[float, ...]:
        """Return the shifted evaluation inventory as binary64 values."""
        return tuple(
            float(value) for value in self.evaluation_reduced_momenta_fractional()
        )


__all__ = [
    "FLAT_ENERGY_REFERENCE_IDENTIFIER",
    "FLAT_GAUGE_ATTACK_IDENTIFIER",
    "FLAT_PARENT_MODEL_IDENTIFIER",
    "FLAT_RECIPROCAL_COORDINATE_CONVENTION",
    "FLAT_REPRESENTED_BASIS_IDENTIFIER",
    "Periodic1DBandEquivalenceLocalityRequest",
]
