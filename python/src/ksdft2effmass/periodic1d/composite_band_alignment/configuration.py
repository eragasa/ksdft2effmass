"""Typed configuration for direct rank-two composite-band alignment."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction
from math import isfinite
from typing import ClassVar, Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeBandAlignmentConfiguration(BaseTypedRecord):
    """Declare the exact parent and finite controls for the rank-two calculation."""

    parent_identity: str
    onsite_numerators: tuple[tuple[int, ...], ...]
    positive_hopping_numerators: tuple[tuple[int, ...], ...]
    coefficient_denominator: int
    retained_rank: int
    construction_size: int
    evaluation_size: int
    evaluation_shift_numerator: int
    evaluation_shift_denominator: int
    hopping_ranges: tuple[int, ...]
    attack_constant_angle: float
    attack_sine_coefficients: tuple[float, ...]
    sampled_gap_threshold: float
    overlap_singular_value_threshold: float
    procrustes_rank_absolute_tolerance: float
    procrustes_rank_relative_tolerance: float
    energy_absolute_tolerance: float
    dimensionless_absolute_tolerance: float

    PARENT_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic1d.controlled-four-state-parent.v1"
    )
    PARENT_ONSITE_NUMERATORS: ClassVar[tuple[tuple[int, ...], ...]] = (
        (-120, 6, 0, 0),
        (6, -35, 0, 0),
        (0, 0, 100, 4),
        (0, 0, 4, 175),
    )
    PARENT_POSITIVE_HOPPING_NUMERATORS: ClassVar[tuple[tuple[int, ...], ...]] = (
        (15, 0, 12, 0),
        (0, -10, 0, 10),
        (0, 0, 5, 0),
        (0, 0, 0, -4),
    )
    PARENT_COEFFICIENT_DENOMINATOR: ClassVar[int] = 100
    HOPPING_RANGES: ClassVar[tuple[int, ...]] = (0, 1, 2, 3, 4, 6, 8)

    def __post_init__(self) -> None:
        """Reject alternate parents, sample sets, attacks, and numerical controls."""
        if type(self.parent_identity) is not str:
            raise TypeError("parent_identity must be a built-in string")
        for matrix, name in (
            (self.onsite_numerators, "onsite_numerators"),
            (self.positive_hopping_numerators, "positive_hopping_numerators"),
        ):
            if (
                not isinstance(matrix, tuple)
                or len(matrix) != 4
                or any(
                    not isinstance(row, tuple)
                    or len(row) != 4
                    or any(type(entry) is not int for entry in row)
                    for row in matrix
                )
            ):
                raise TypeError(f"{name} must be a four-by-four integer tuple")
        for value, name in (
            (self.coefficient_denominator, "coefficient_denominator"),
            (self.retained_rank, "retained_rank"),
            (self.construction_size, "construction_size"),
            (self.evaluation_size, "evaluation_size"),
            (self.evaluation_shift_numerator, "evaluation_shift_numerator"),
            (self.evaluation_shift_denominator, "evaluation_shift_denominator"),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
        if (
            self.parent_identity != self.PARENT_IDENTITY
            or self.onsite_numerators != self.PARENT_ONSITE_NUMERATORS
            or self.positive_hopping_numerators
            != self.PARENT_POSITIVE_HOPPING_NUMERATORS
            or self.coefficient_denominator != self.PARENT_COEFFICIENT_DENOMINATOR
        ):
            raise ValueError(
                "parent identity must bind the exact four-state coefficients"
            )
        if self.retained_rank != 2:
            raise ValueError("retained_rank must equal two")
        if self.construction_size != 64 or self.construction_size % 2 != 0:
            raise ValueError("construction_size must equal the frozen even extent 64")
        if self.evaluation_size != 257:
            raise ValueError("evaluation_size must equal the frozen extent 257")
        if (
            self.evaluation_shift_numerator != 1
            or self.evaluation_shift_denominator != 65
        ):
            raise ValueError("evaluation shift must equal the frozen rational 1/65")
        if not isinstance(self.hopping_ranges, tuple) or any(
            type(value) is not int for value in self.hopping_ranges
        ):
            raise TypeError("hopping_ranges must be a tuple of built-in integers")
        if self.hopping_ranges != self.HOPPING_RANGES:
            raise ValueError("hopping_ranges must match the frozen range inventory")
        if 2 * self.hopping_ranges[-1] + 1 >= self.construction_size:
            raise ValueError("hopping ranges must exclude the cyclic Nyquist point")
        if not isinstance(self.attack_sine_coefficients, tuple) or any(
            type(value) is not float for value in self.attack_sine_coefficients
        ):
            raise TypeError("attack_sine_coefficients must contain built-in floats")
        for scalar, name in (
            (self.attack_constant_angle, "attack_constant_angle"),
            (self.sampled_gap_threshold, "sampled_gap_threshold"),
            (
                self.overlap_singular_value_threshold,
                "overlap_singular_value_threshold",
            ),
            (
                self.procrustes_rank_absolute_tolerance,
                "procrustes_rank_absolute_tolerance",
            ),
            (
                self.procrustes_rank_relative_tolerance,
                "procrustes_rank_relative_tolerance",
            ),
            (self.energy_absolute_tolerance, "energy_absolute_tolerance"),
            (
                self.dimensionless_absolute_tolerance,
                "dimensionless_absolute_tolerance",
            ),
        ):
            if type(scalar) is not float or not isfinite(scalar):
                raise TypeError(f"{name} must be a finite built-in float")
            if scalar < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if any(not isfinite(value) for value in self.attack_sine_coefficients):
            raise ValueError("attack_sine_coefficients must be finite")
        if self.attack_constant_angle != 0.30 or self.attack_sine_coefficients != (
            0.65,
            0.30,
        ):
            raise ValueError(
                "attack coefficients must match the frozen rank-two attack"
            )
        if self.sampled_gap_threshold != 0.5:
            raise ValueError("sampled_gap_threshold must equal 0.5")
        if self.overlap_singular_value_threshold != 0.8:
            raise ValueError("overlap_singular_value_threshold must equal 0.8")
        if self.overlap_singular_value_threshold >= 1.0:
            raise ValueError("overlap_singular_value_threshold must be below one")
        if self.procrustes_rank_absolute_tolerance != 1.0e-14:
            raise ValueError("absolute rank cutoff must equal 1e-14")
        if self.procrustes_rank_relative_tolerance != 1.0e-12:
            raise ValueError("relative rank cutoff must equal 1e-12")
        if self.energy_absolute_tolerance != 1.0e-11:
            raise ValueError("energy_absolute_tolerance must equal 1e-11")
        if self.dimensionless_absolute_tolerance != 1.0e-12:
            raise ValueError("dimensionless_absolute_tolerance must equal 1e-12")
        evaluation = set(self.evaluation_reduced_momenta_fractional())
        construction = {
            Fraction(-1, 2) + Fraction(index, self.construction_size)
            for index in range(self.construction_size)
        }
        if not construction.isdisjoint(evaluation):
            raise ValueError("construction and evaluation coordinates must be disjoint")

    def construction_reduced_momenta(self) -> tuple[float, ...]:
        """Return the frozen centered half-open construction coordinates."""
        return tuple(
            float(Fraction(-1, 2) + Fraction(index, self.construction_size))
            for index in range(self.construction_size)
        )

    def evaluation_reduced_momenta_fractional(self) -> tuple[Fraction, ...]:
        """Return the exact staggered evaluation coordinates."""
        shift = Fraction(
            self.evaluation_shift_numerator,
            self.evaluation_shift_denominator,
        )
        return tuple(
            Fraction(-1, 2) + (Fraction(index, 1) + shift) / self.evaluation_size
            for index in range(self.evaluation_size)
        )

    def evaluation_reduced_momenta(self) -> tuple[float, ...]:
        """Return the exact-rational evaluation inventory in binary64."""
        return tuple(
            float(value) for value in self.evaluation_reduced_momenta_fractional()
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "parent_identity": self.parent_identity,
            "onsite_numerators": self.onsite_numerators,
            "positive_hopping_numerators": self.positive_hopping_numerators,
            "coefficient_denominator": self.coefficient_denominator,
            "retained_rank": self.retained_rank,
            "construction_size": self.construction_size,
            "evaluation_size": self.evaluation_size,
            "evaluation_shift_numerator": self.evaluation_shift_numerator,
            "evaluation_shift_denominator": self.evaluation_shift_denominator,
            "hopping_ranges": self.hopping_ranges,
            "attack_constant_angle": self.attack_constant_angle,
            "attack_sine_coefficients": self.attack_sine_coefficients,
            "sampled_gap_threshold": self.sampled_gap_threshold,
            "overlap_singular_value_threshold": self.overlap_singular_value_threshold,
            "procrustes_rank_absolute_tolerance": (
                self.procrustes_rank_absolute_tolerance
            ),
            "procrustes_rank_relative_tolerance": (
                self.procrustes_rank_relative_tolerance
            ),
            "energy_absolute_tolerance": self.energy_absolute_tolerance,
            "dimensionless_absolute_tolerance": (self.dimensionless_absolute_tolerance),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "parent_identity",
            "onsite_numerators",
            "positive_hopping_numerators",
            "coefficient_denominator",
            "retained_rank",
            "construction_size",
            "evaluation_size",
            "evaluation_shift_numerator",
            "evaluation_shift_denominator",
            "hopping_ranges",
            "attack_constant_angle",
            "attack_sine_coefficients",
            "sampled_gap_threshold",
            "overlap_singular_value_threshold",
            "procrustes_rank_absolute_tolerance",
            "procrustes_rank_relative_tolerance",
            "energy_absolute_tolerance",
            "dimensionless_absolute_tolerance",
        }
        if set(values) != required:
            raise ValueError("composite-band configuration fields do not match")
        parent_identity = values["parent_identity"]
        onsite = values["onsite_numerators"]
        positive = values["positive_hopping_numerators"]
        ranges = values["hopping_ranges"]
        attack = values["attack_sine_coefficients"]
        if type(parent_identity) is not str:
            raise TypeError("parent_identity must decode to a string")
        if not isinstance(onsite, tuple) or not isinstance(positive, tuple):
            raise TypeError("parent coefficient matrices must decode to tuples")
        if not isinstance(ranges, tuple) or not isinstance(attack, tuple):
            raise TypeError("range and attack inventories must decode to tuples")
        integer_names = (
            "coefficient_denominator",
            "retained_rank",
            "construction_size",
            "evaluation_size",
            "evaluation_shift_numerator",
            "evaluation_shift_denominator",
        )
        integer_values: dict[str, int] = {}
        for name in integer_names:
            value = values[name]
            if type(value) is not int:
                raise TypeError(f"{name} must decode to a built-in integer")
            integer_values[name] = value
        float_names = (
            "attack_constant_angle",
            "sampled_gap_threshold",
            "overlap_singular_value_threshold",
            "procrustes_rank_absolute_tolerance",
            "procrustes_rank_relative_tolerance",
            "energy_absolute_tolerance",
            "dimensionless_absolute_tolerance",
        )
        float_values: dict[str, float] = {}
        for name in float_names:
            value = values[name]
            if type(value) is not float:
                raise TypeError(f"{name} must decode to a built-in float")
            float_values[name] = value
        return cls(
            parent_identity=parent_identity,
            onsite_numerators=tuple(tuple(row) for row in onsite),
            positive_hopping_numerators=tuple(tuple(row) for row in positive),
            coefficient_denominator=integer_values["coefficient_denominator"],
            retained_rank=integer_values["retained_rank"],
            construction_size=integer_values["construction_size"],
            evaluation_size=integer_values["evaluation_size"],
            evaluation_shift_numerator=integer_values["evaluation_shift_numerator"],
            evaluation_shift_denominator=integer_values["evaluation_shift_denominator"],
            hopping_ranges=tuple(ranges),
            attack_constant_angle=float_values["attack_constant_angle"],
            attack_sine_coefficients=tuple(attack),
            sampled_gap_threshold=float_values["sampled_gap_threshold"],
            overlap_singular_value_threshold=float_values[
                "overlap_singular_value_threshold"
            ],
            procrustes_rank_absolute_tolerance=float_values[
                "procrustes_rank_absolute_tolerance"
            ],
            procrustes_rank_relative_tolerance=float_values[
                "procrustes_rank_relative_tolerance"
            ],
            energy_absolute_tolerance=float_values["energy_absolute_tolerance"],
            dimensionless_absolute_tolerance=float_values[
                "dimensionless_absolute_tolerance"
            ],
        )


__all__ = ["Periodic1DCompositeBandAlignmentConfiguration"]
