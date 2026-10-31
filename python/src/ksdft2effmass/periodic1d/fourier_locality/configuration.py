"""Typed inputs for direct compatible rank-one Fourier-locality calculations."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction
from math import isfinite
from typing import ClassVar, Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..geometry import Periodic1DReducedCoordinateConvention


@dataclass(frozen=True, slots=True)
class Periodic1DFourierLocalityConfiguration(
    BaseTypedRecord,
    Periodic1DReducedCoordinateConvention,
):
    """Declare the exact parent and finite controls for one calculation."""

    parent_identity: str
    onsite_numerators: tuple[tuple[int, ...], ...]
    positive_hopping_numerators: tuple[tuple[int, ...], ...]
    coefficient_denominator: int
    construction_mesh_sizes: tuple[int, ...]
    production_construction_size: int
    evaluation_size: int
    evaluation_shift_numerator: int
    evaluation_shift_denominator: int
    maximum_ranges: tuple[int, ...]
    sampled_gap_threshold: float
    energy_absolute_tolerance: float
    relative_tolerance: float
    squared_energy_absolute_tolerance: float
    dimensionless_absolute_tolerance: float
    refinement_tolerance: float
    application_threshold: float

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

    def __post_init__(self) -> None:
        """Validate exact parent storage and correlated finite controls."""
        if type(self.parent_identity) is not str:
            raise TypeError("parent_identity must be a built-in string")
        for matrix, name in (
            (self.onsite_numerators, "onsite_numerators"),
            (self.positive_hopping_numerators, "positive_hopping_numerators"),
        ):
            if not isinstance(matrix, tuple) or len(matrix) != 4:
                raise TypeError(f"{name} must be a four-row tuple")
            if any(
                not isinstance(row, tuple)
                or len(row) != 4
                or any(type(entry) is not int for entry in row)
                for row in matrix
            ):
                raise TypeError(f"{name} must be a four-by-four integer matrix")
        if self.onsite_numerators != tuple(
            tuple(self.onsite_numerators[column][row] for column in range(4))
            for row in range(4)
        ):
            raise ValueError("onsite_numerators must be exactly symmetric")
        for integer_control, name in (
            (self.coefficient_denominator, "coefficient_denominator"),
            (self.production_construction_size, "production_construction_size"),
            (self.evaluation_size, "evaluation_size"),
            (self.evaluation_shift_numerator, "evaluation_shift_numerator"),
            (self.evaluation_shift_denominator, "evaluation_shift_denominator"),
        ):
            if type(integer_control) is not int:
                raise TypeError(f"{name} must be a built-in int")
        if self.coefficient_denominator <= 0:
            raise ValueError("coefficient_denominator must be positive")
        if (
            self.parent_identity != self.PARENT_IDENTITY
            or self.onsite_numerators != self.PARENT_ONSITE_NUMERATORS
            or self.positive_hopping_numerators
            != self.PARENT_POSITIVE_HOPPING_NUMERATORS
            or self.coefficient_denominator != self.PARENT_COEFFICIENT_DENOMINATOR
        ):
            raise ValueError(
                "parent identity must bind the exact controlled four-state coefficients"
            )
        if not isinstance(self.construction_mesh_sizes, tuple) or any(
            type(value) is not int for value in self.construction_mesh_sizes
        ):
            raise TypeError("construction_mesh_sizes must be a tuple of built-in ints")
        if (
            len(self.construction_mesh_sizes) < 2
            or self.construction_mesh_sizes
            != tuple(sorted(set(self.construction_mesh_sizes)))
            or self.construction_mesh_sizes[0] <= 0
        ):
            raise ValueError(
                "construction_mesh_sizes must be positive and strictly increasing"
            )
        if any(size % 2 != 0 for size in self.construction_mesh_sizes):
            raise ValueError("construction_mesh_sizes must contain even values")
        if self.production_construction_size != self.construction_mesh_sizes[-1]:
            raise ValueError("production construction size must be the largest mesh")
        if self.evaluation_size <= 0:
            raise ValueError("evaluation_size must be positive")
        if not (
            0 < self.evaluation_shift_numerator < self.evaluation_shift_denominator
        ):
            raise ValueError("evaluation shift must be a proper positive fraction")
        if not isinstance(self.maximum_ranges, tuple) or any(
            type(value) is not int for value in self.maximum_ranges
        ):
            raise TypeError("maximum_ranges must be a tuple of built-in ints")
        if (
            not self.maximum_ranges
            or self.maximum_ranges != tuple(sorted(set(self.maximum_ranges)))
            or self.maximum_ranges[0] < 0
        ):
            raise ValueError(
                "maximum_ranges must be nonnegative and strictly increasing"
            )
        if 2 * self.maximum_ranges[-1] + 1 >= self.construction_mesh_sizes[0]:
            raise ValueError(
                "ordinary supports must exclude every cyclic Nyquist point"
            )
        shift = Fraction(
            self.evaluation_shift_numerator,
            self.evaluation_shift_denominator,
        )
        evaluation = {
            (Fraction(index, 1) + shift) / self.evaluation_size
            for index in range(self.evaluation_size)
        }
        for size in self.construction_mesh_sizes:
            construction = {Fraction(index, size) for index in range(size)}
            if not construction.isdisjoint(evaluation):
                raise ValueError("construction and evaluation meshes must be disjoint")
        for numerical_control, name in (
            (self.sampled_gap_threshold, "sampled_gap_threshold"),
            (self.energy_absolute_tolerance, "energy_absolute_tolerance"),
            (self.relative_tolerance, "relative_tolerance"),
            (
                self.squared_energy_absolute_tolerance,
                "squared_energy_absolute_tolerance",
            ),
            (
                self.dimensionless_absolute_tolerance,
                "dimensionless_absolute_tolerance",
            ),
            (self.refinement_tolerance, "refinement_tolerance"),
            (self.application_threshold, "application_threshold"),
        ):
            if type(numerical_control) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not isfinite(numerical_control) or numerical_control < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")

    def evaluation_reduced_momenta(self) -> tuple[float, ...]:
        """Return the canonical exact-rational evaluation inventory in binary64."""
        shift = Fraction(
            self.evaluation_shift_numerator,
            self.evaluation_shift_denominator,
        )
        return tuple(
            float(Fraction(-1, 2) + (Fraction(index, 1) + shift) / self.evaluation_size)
            for index in range(self.evaluation_size)
        )

    def refinement_channel_names(self) -> tuple[str, ...]:
        """Return the exact ordered semantic refinement-channel inventory."""
        names = ["interpolation_maximum_error", "interpolation_rms_error"]
        for maximum_range in self.maximum_ranges:
            prefix = f"range_{maximum_range}"
            names.extend(
                (
                    f"{prefix}.truncation_maximum_error",
                    f"{prefix}.truncation_rms_error",
                    f"{prefix}.mediated_total_maximum_error",
                    f"{prefix}.mediated_total_rms_error",
                    f"{prefix}.direct_total_maximum_error",
                    f"{prefix}.direct_total_rms_error",
                    f"{prefix}.omitted_coefficient_l2_norm",
                    f"{prefix}.coefficient_l2_defect",
                    f"{prefix}.sampled_l2_defect",
                    f"{prefix}.sampled_maximum_defect",
                )
            )
        return tuple(names)

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "parent_identity": self.parent_identity,
            "onsite_numerators": self.onsite_numerators,
            "positive_hopping_numerators": self.positive_hopping_numerators,
            "coefficient_denominator": self.coefficient_denominator,
            "construction_mesh_sizes": self.construction_mesh_sizes,
            "production_construction_size": self.production_construction_size,
            "evaluation_size": self.evaluation_size,
            "evaluation_shift_numerator": self.evaluation_shift_numerator,
            "evaluation_shift_denominator": self.evaluation_shift_denominator,
            "maximum_ranges": self.maximum_ranges,
            "sampled_gap_threshold": self.sampled_gap_threshold,
            "energy_absolute_tolerance": self.energy_absolute_tolerance,
            "relative_tolerance": self.relative_tolerance,
            "squared_energy_absolute_tolerance": (
                self.squared_energy_absolute_tolerance
            ),
            "dimensionless_absolute_tolerance": (self.dimensionless_absolute_tolerance),
            "refinement_tolerance": self.refinement_tolerance,
            "application_threshold": self.application_threshold,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "parent_identity",
            "onsite_numerators",
            "positive_hopping_numerators",
            "coefficient_denominator",
            "construction_mesh_sizes",
            "production_construction_size",
            "evaluation_size",
            "evaluation_shift_numerator",
            "evaluation_shift_denominator",
            "maximum_ranges",
            "sampled_gap_threshold",
            "energy_absolute_tolerance",
            "relative_tolerance",
            "squared_energy_absolute_tolerance",
            "dimensionless_absolute_tolerance",
            "refinement_tolerance",
            "application_threshold",
        }:
            raise ValueError("Fourier-locality configuration fields do not match")
        parent_identity = values["parent_identity"]
        if type(parent_identity) is not str:
            raise TypeError("parent_identity must decode to a string")
        onsite_value = values["onsite_numerators"]
        if not isinstance(onsite_value, tuple):
            raise TypeError("onsite_numerators must decode to row tuples")
        onsite_rows: list[tuple[int, ...]] = []
        for row_value in onsite_value:
            if not isinstance(row_value, tuple):
                raise TypeError("onsite_numerators must decode to row tuples")
            row: list[int] = []
            for entry in row_value:
                if not isinstance(entry, int) or isinstance(entry, bool):
                    raise TypeError("onsite_numerators must decode to integer rows")
                row.append(entry)
            onsite_rows.append(tuple(row))
        positive_hopping_value = values["positive_hopping_numerators"]
        if not isinstance(positive_hopping_value, tuple):
            raise TypeError("positive_hopping_numerators must decode to row tuples")
        positive_hopping_rows: list[tuple[int, ...]] = []
        for row_value in positive_hopping_value:
            if not isinstance(row_value, tuple):
                raise TypeError("positive_hopping_numerators must decode to row tuples")
            row = []
            for entry in row_value:
                if not isinstance(entry, int) or isinstance(entry, bool):
                    raise TypeError(
                        "positive_hopping_numerators must decode to integer rows"
                    )
                row.append(entry)
            positive_hopping_rows.append(tuple(row))
        construction_sizes_value = values["construction_mesh_sizes"]
        if not isinstance(construction_sizes_value, tuple):
            raise TypeError("construction_mesh_sizes must decode to a tuple")
        construction_sizes: list[int] = []
        for size in construction_sizes_value:
            if not isinstance(size, int) or isinstance(size, bool):
                raise TypeError("construction_mesh_sizes must decode to ints")
            construction_sizes.append(size)
        maximum_ranges_value = values["maximum_ranges"]
        if not isinstance(maximum_ranges_value, tuple):
            raise TypeError("maximum_ranges must decode to a tuple")
        maximum_ranges: list[int] = []
        for maximum_range in maximum_ranges_value:
            if not isinstance(maximum_range, int) or isinstance(maximum_range, bool):
                raise TypeError("maximum_ranges must decode to ints")
            maximum_ranges.append(maximum_range)
        coefficient_denominator = values["coefficient_denominator"]
        production_size = values["production_construction_size"]
        evaluation_size = values["evaluation_size"]
        shift_numerator = values["evaluation_shift_numerator"]
        shift_denominator = values["evaluation_shift_denominator"]
        if not isinstance(coefficient_denominator, int) or isinstance(
            coefficient_denominator, bool
        ):
            raise TypeError("coefficient_denominator must decode to int")
        if not isinstance(production_size, int) or isinstance(production_size, bool):
            raise TypeError("production_construction_size must decode to int")
        if not isinstance(evaluation_size, int) or isinstance(evaluation_size, bool):
            raise TypeError("evaluation_size must decode to int")
        if not isinstance(shift_numerator, int) or isinstance(shift_numerator, bool):
            raise TypeError("evaluation_shift_numerator must decode to int")
        if not isinstance(shift_denominator, int) or isinstance(
            shift_denominator, bool
        ):
            raise TypeError("evaluation_shift_denominator must decode to int")
        sampled_gap_threshold = values["sampled_gap_threshold"]
        energy_absolute_tolerance = values["energy_absolute_tolerance"]
        relative_tolerance = values["relative_tolerance"]
        squared_energy_absolute_tolerance = values["squared_energy_absolute_tolerance"]
        dimensionless_absolute_tolerance = values["dimensionless_absolute_tolerance"]
        refinement_tolerance = values["refinement_tolerance"]
        application_threshold = values["application_threshold"]
        if not isinstance(sampled_gap_threshold, float):
            raise TypeError("sampled_gap_threshold must decode to float")
        if not isinstance(energy_absolute_tolerance, float):
            raise TypeError("energy_absolute_tolerance must decode to float")
        if not isinstance(relative_tolerance, float):
            raise TypeError("relative_tolerance must decode to float")
        if not isinstance(squared_energy_absolute_tolerance, float):
            raise TypeError("squared_energy_absolute_tolerance must decode to float")
        if not isinstance(dimensionless_absolute_tolerance, float):
            raise TypeError("dimensionless_absolute_tolerance must decode to float")
        if not isinstance(refinement_tolerance, float):
            raise TypeError("refinement_tolerance must decode to float")
        if not isinstance(application_threshold, float):
            raise TypeError("application_threshold must decode to float")
        return cls(
            parent_identity=parent_identity,
            onsite_numerators=tuple(onsite_rows),
            positive_hopping_numerators=tuple(positive_hopping_rows),
            coefficient_denominator=coefficient_denominator,
            construction_mesh_sizes=tuple(construction_sizes),
            production_construction_size=production_size,
            evaluation_size=evaluation_size,
            evaluation_shift_numerator=shift_numerator,
            evaluation_shift_denominator=shift_denominator,
            maximum_ranges=tuple(maximum_ranges),
            sampled_gap_threshold=sampled_gap_threshold,
            energy_absolute_tolerance=energy_absolute_tolerance,
            relative_tolerance=relative_tolerance,
            squared_energy_absolute_tolerance=squared_energy_absolute_tolerance,
            dimensionless_absolute_tolerance=dimensionless_absolute_tolerance,
            refinement_tolerance=refinement_tolerance,
            application_threshold=application_threshold,
        )


__all__ = ["Periodic1DFourierLocalityConfiguration"]
