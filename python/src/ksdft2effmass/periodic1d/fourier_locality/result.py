"""Typed results for direct compatible rank-one Fourier-locality calculations."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

import numpy as np
from projectkoios.numerics.numpy.typing import Float64Array
from projectkoios.physkit.units import (
    ComplexVectorQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .configuration import Periodic1DFourierLocalityConfiguration


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DFourierLocalityEvaluationResult(BaseTypedRecord):
    """Retain the common disjoint evaluation coordinates and two parent bands."""

    reduced_momenta: VectorQuantity
    lowest_energies: VectorQuantity
    adjacent_energies: VectorQuantity

    def __post_init__(self) -> None:
        for value, name in (
            (self.reduced_momenta, "reduced_momenta"),
            (self.lowest_energies, "lowest_energies"),
            (self.adjacent_energies, "adjacent_energies"),
        ):
            if not isinstance(value, VectorQuantity):
                raise TypeError(f"{name} must be VectorQuantity")
            if not isinstance(value.unit, Unitless):
                raise ValueError(f"{name} must use Unitless")
        size = self.reduced_momenta.magnitude.size
        if size <= 0:
            raise ValueError("evaluation samples must be nonempty")
        if self.lowest_energies.magnitude.shape != (size,):
            raise ValueError("lowest energies must match evaluation coordinates")
        if self.adjacent_energies.magnitude.shape != (size,):
            raise ValueError("adjacent energies must match evaluation coordinates")
        if np.any(self.adjacent_energies.magnitude < self.lowest_energies.magnitude):
            raise ValueError("adjacent energies must not lie below lowest energies")

    @property
    def sampled_gaps(self) -> VectorQuantity:
        """Return the sampled first-to-second parent-band gaps."""
        return VectorQuantity(
            self.adjacent_energies.magnitude - self.lowest_energies.magnitude,
            self.lowest_energies.unit,
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "reduced_momenta": self.reduced_momenta,
            "lowest_energies": self.lowest_energies,
            "adjacent_energies": self.adjacent_energies,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "reduced_momenta",
            "lowest_energies",
            "adjacent_energies",
        }:
            raise ValueError("Fourier-locality evaluation fields do not match")
        reduced_momenta = values["reduced_momenta"]
        lowest_energies = values["lowest_energies"]
        adjacent_energies = values["adjacent_energies"]
        if not isinstance(reduced_momenta, VectorQuantity):
            raise TypeError("reduced_momenta must decode to VectorQuantity")
        if not isinstance(lowest_energies, VectorQuantity):
            raise TypeError("lowest_energies must decode to VectorQuantity")
        if not isinstance(adjacent_energies, VectorQuantity):
            raise TypeError("adjacent_energies must decode to VectorQuantity")
        return cls(reduced_momenta, lowest_energies, adjacent_energies)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DFourierLocalityRangeResult(BaseTypedRecord):
    """Retain one mediated/direct ordinary-support calculation."""

    maximum_range: int
    mediated_coefficients: ComplexVectorQuantity
    direct_coefficients: ComplexVectorQuantity
    mediated_construction_candidate: VectorQuantity
    mediated_evaluation_candidate: VectorQuantity
    direct_construction_candidate: VectorQuantity
    direct_evaluation_candidate: VectorQuantity
    truncation_maximum_error: ScalarQuantity
    truncation_rms_error: ScalarQuantity
    mediated_total_maximum_error: ScalarQuantity
    mediated_total_rms_error: ScalarQuantity
    direct_total_maximum_error: ScalarQuantity
    direct_total_rms_error: ScalarQuantity
    omitted_coefficient_l2_norm: ScalarQuantity
    parseval_observed_squared_residual: ScalarQuantity
    parseval_expected_squared_residual: ScalarQuantity
    parseval_absolute_residual: ScalarQuantity
    direct_design_rank: int
    direct_design_condition_number: float
    direct_training_l2_residual: ScalarQuantity
    direct_training_maximum_residual: ScalarQuantity
    coefficient_l2_defect: ScalarQuantity
    sampled_l2_defect: ScalarQuantity
    sampled_maximum_defect: ScalarQuantity
    bandwidth: ScalarQuantity
    zone_center_curvature: ScalarQuantity
    maximum_imaginary_residual: ScalarQuantity

    def __post_init__(self) -> None:
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if self.maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        support_size = 2 * self.maximum_range + 1
        for coefficient_value, name in (
            (self.mediated_coefficients, "mediated_coefficients"),
            (self.direct_coefficients, "direct_coefficients"),
        ):
            if not isinstance(coefficient_value, ComplexVectorQuantity):
                raise TypeError(f"{name} must be ComplexVectorQuantity")
            if not isinstance(coefficient_value.unit, Unitless):
                raise ValueError(f"{name} must use Unitless")
            if coefficient_value.magnitude.shape != (support_size,):
                raise ValueError(f"{name} must match the ordinary support")
        construction_size = 0
        evaluation_size = 0
        for candidate_value, name in (
            (
                self.mediated_construction_candidate,
                "mediated_construction_candidate",
            ),
            (self.direct_construction_candidate, "direct_construction_candidate"),
            (self.mediated_evaluation_candidate, "mediated_evaluation_candidate"),
            (self.direct_evaluation_candidate, "direct_evaluation_candidate"),
        ):
            if not isinstance(candidate_value, VectorQuantity):
                raise TypeError(f"{name} must be VectorQuantity")
            if not isinstance(candidate_value.unit, Unitless):
                raise ValueError(f"{name} must use Unitless")
            if candidate_value.magnitude.size <= 0:
                raise ValueError(f"{name} must be nonempty")
            if "construction" in name:
                if construction_size == 0:
                    construction_size = candidate_value.magnitude.size
                elif candidate_value.magnitude.shape != (construction_size,):
                    raise ValueError("construction candidates must share one extent")
            elif evaluation_size == 0:
                evaluation_size = candidate_value.magnitude.size
            elif candidate_value.magnitude.shape != (evaluation_size,):
                raise ValueError("evaluation candidates must share one extent")
        signed_scalar = self.zone_center_curvature
        if not isinstance(signed_scalar, ScalarQuantity):
            raise TypeError("zone_center_curvature must be ScalarQuantity")
        if not isinstance(signed_scalar.unit, Unitless):
            raise ValueError("zone_center_curvature must use Unitless")
        for diagnostic_value, name in (
            (self.truncation_maximum_error, "truncation_maximum_error"),
            (self.truncation_rms_error, "truncation_rms_error"),
            (self.mediated_total_maximum_error, "mediated_total_maximum_error"),
            (self.mediated_total_rms_error, "mediated_total_rms_error"),
            (self.direct_total_maximum_error, "direct_total_maximum_error"),
            (self.direct_total_rms_error, "direct_total_rms_error"),
            (self.omitted_coefficient_l2_norm, "omitted_coefficient_l2_norm"),
            (
                self.parseval_observed_squared_residual,
                "parseval_observed_squared_residual",
            ),
            (
                self.parseval_expected_squared_residual,
                "parseval_expected_squared_residual",
            ),
            (self.parseval_absolute_residual, "parseval_absolute_residual"),
            (self.direct_training_l2_residual, "direct_training_l2_residual"),
            (
                self.direct_training_maximum_residual,
                "direct_training_maximum_residual",
            ),
            (self.coefficient_l2_defect, "coefficient_l2_defect"),
            (self.sampled_l2_defect, "sampled_l2_defect"),
            (self.sampled_maximum_defect, "sampled_maximum_defect"),
            (self.bandwidth, "bandwidth"),
            (self.maximum_imaginary_residual, "maximum_imaginary_residual"),
        ):
            if not isinstance(diagnostic_value, ScalarQuantity):
                raise TypeError(f"{name} must be ScalarQuantity")
            if not isinstance(diagnostic_value.unit, Unitless):
                raise ValueError(f"{name} must use Unitless")
            if diagnostic_value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if type(self.direct_design_rank) is not int:
            raise TypeError("direct_design_rank must be a built-in int")
        if not 0 <= self.direct_design_rank <= support_size:
            raise ValueError("direct_design_rank is outside the design extent")
        if type(self.direct_design_condition_number) is not float:
            raise TypeError("direct_design_condition_number must be a built-in float")
        if (
            not np.isfinite(self.direct_design_condition_number)
            or self.direct_design_condition_number < 1.0
        ):
            raise ValueError("direct condition number must be finite and at least one")

    @property
    def representatives(self) -> tuple[int, ...]:
        """Return the complete ordinary symmetric support."""
        return tuple(range(-self.maximum_range, self.maximum_range + 1))

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "maximum_range": self.maximum_range,
            "mediated_coefficients": self.mediated_coefficients,
            "direct_coefficients": self.direct_coefficients,
            "mediated_construction_candidate": self.mediated_construction_candidate,
            "mediated_evaluation_candidate": self.mediated_evaluation_candidate,
            "direct_construction_candidate": self.direct_construction_candidate,
            "direct_evaluation_candidate": self.direct_evaluation_candidate,
            "truncation_maximum_error": self.truncation_maximum_error,
            "truncation_rms_error": self.truncation_rms_error,
            "mediated_total_maximum_error": self.mediated_total_maximum_error,
            "mediated_total_rms_error": self.mediated_total_rms_error,
            "direct_total_maximum_error": self.direct_total_maximum_error,
            "direct_total_rms_error": self.direct_total_rms_error,
            "omitted_coefficient_l2_norm": self.omitted_coefficient_l2_norm,
            "parseval_observed_squared_residual": (
                self.parseval_observed_squared_residual
            ),
            "parseval_expected_squared_residual": (
                self.parseval_expected_squared_residual
            ),
            "parseval_absolute_residual": self.parseval_absolute_residual,
            "direct_design_rank": self.direct_design_rank,
            "direct_design_condition_number": self.direct_design_condition_number,
            "direct_training_l2_residual": self.direct_training_l2_residual,
            "direct_training_maximum_residual": (self.direct_training_maximum_residual),
            "coefficient_l2_defect": self.coefficient_l2_defect,
            "sampled_l2_defect": self.sampled_l2_defect,
            "sampled_maximum_defect": self.sampled_maximum_defect,
            "bandwidth": self.bandwidth,
            "zone_center_curvature": self.zone_center_curvature,
            "maximum_imaginary_residual": self.maximum_imaginary_residual,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "maximum_range",
            "mediated_coefficients",
            "direct_coefficients",
            "mediated_construction_candidate",
            "mediated_evaluation_candidate",
            "direct_construction_candidate",
            "direct_evaluation_candidate",
            "truncation_maximum_error",
            "truncation_rms_error",
            "mediated_total_maximum_error",
            "mediated_total_rms_error",
            "direct_total_maximum_error",
            "direct_total_rms_error",
            "omitted_coefficient_l2_norm",
            "parseval_observed_squared_residual",
            "parseval_expected_squared_residual",
            "parseval_absolute_residual",
            "direct_design_rank",
            "direct_design_condition_number",
            "direct_training_l2_residual",
            "direct_training_maximum_residual",
            "coefficient_l2_defect",
            "sampled_l2_defect",
            "sampled_maximum_defect",
            "bandwidth",
            "zone_center_curvature",
            "maximum_imaginary_residual",
        }:
            raise ValueError("Fourier-locality range fields do not match")
        maximum_range = values["maximum_range"]
        mediated_coefficients = values["mediated_coefficients"]
        direct_coefficients = values["direct_coefficients"]
        mediated_construction = values["mediated_construction_candidate"]
        mediated_evaluation = values["mediated_evaluation_candidate"]
        direct_construction = values["direct_construction_candidate"]
        direct_evaluation = values["direct_evaluation_candidate"]
        direct_design_rank = values["direct_design_rank"]
        direct_condition = values["direct_design_condition_number"]
        if type(maximum_range) is not int or type(direct_design_rank) is not int:
            raise TypeError("range integer fields must decode to ints")
        if type(direct_condition) is not float:
            raise TypeError("direct condition number must decode to float")
        if not isinstance(mediated_coefficients, ComplexVectorQuantity):
            raise TypeError("mediated_coefficients must decode correctly")
        if not isinstance(direct_coefficients, ComplexVectorQuantity):
            raise TypeError("direct_coefficients must decode correctly")
        if not isinstance(mediated_construction, VectorQuantity):
            raise TypeError(
                "mediated_construction_candidate must decode to VectorQuantity"
            )
        if not isinstance(mediated_evaluation, VectorQuantity):
            raise TypeError(
                "mediated_evaluation_candidate must decode to VectorQuantity"
            )
        if not isinstance(direct_construction, VectorQuantity):
            raise TypeError(
                "direct_construction_candidate must decode to VectorQuantity"
            )
        if not isinstance(direct_evaluation, VectorQuantity):
            raise TypeError("direct_evaluation_candidate must decode to VectorQuantity")
        truncation_maximum = values["truncation_maximum_error"]
        truncation_rms = values["truncation_rms_error"]
        mediated_total_maximum = values["mediated_total_maximum_error"]
        mediated_total_rms = values["mediated_total_rms_error"]
        direct_total_maximum = values["direct_total_maximum_error"]
        direct_total_rms = values["direct_total_rms_error"]
        omitted_norm = values["omitted_coefficient_l2_norm"]
        parseval_observed = values["parseval_observed_squared_residual"]
        parseval_expected = values["parseval_expected_squared_residual"]
        parseval_residual = values["parseval_absolute_residual"]
        direct_training_l2 = values["direct_training_l2_residual"]
        direct_training_maximum = values["direct_training_maximum_residual"]
        coefficient_defect = values["coefficient_l2_defect"]
        sampled_l2_defect = values["sampled_l2_defect"]
        sampled_maximum_defect = values["sampled_maximum_defect"]
        bandwidth = values["bandwidth"]
        curvature = values["zone_center_curvature"]
        imaginary_residual = values["maximum_imaginary_residual"]
        if not isinstance(truncation_maximum, ScalarQuantity):
            raise TypeError("truncation_maximum_error must decode correctly")
        if not isinstance(truncation_rms, ScalarQuantity):
            raise TypeError("truncation_rms_error must decode correctly")
        if not isinstance(mediated_total_maximum, ScalarQuantity):
            raise TypeError("mediated_total_maximum_error must decode correctly")
        if not isinstance(mediated_total_rms, ScalarQuantity):
            raise TypeError("mediated_total_rms_error must decode correctly")
        if not isinstance(direct_total_maximum, ScalarQuantity):
            raise TypeError("direct_total_maximum_error must decode correctly")
        if not isinstance(direct_total_rms, ScalarQuantity):
            raise TypeError("direct_total_rms_error must decode correctly")
        if not isinstance(omitted_norm, ScalarQuantity):
            raise TypeError("omitted_coefficient_l2_norm must decode correctly")
        if not isinstance(parseval_observed, ScalarQuantity):
            raise TypeError("parseval_observed_squared_residual must decode correctly")
        if not isinstance(parseval_expected, ScalarQuantity):
            raise TypeError("parseval_expected_squared_residual must decode correctly")
        if not isinstance(parseval_residual, ScalarQuantity):
            raise TypeError("parseval_absolute_residual must decode correctly")
        if not isinstance(direct_training_l2, ScalarQuantity):
            raise TypeError("direct_training_l2_residual must decode correctly")
        if not isinstance(direct_training_maximum, ScalarQuantity):
            raise TypeError("direct_training_maximum_residual must decode correctly")
        if not isinstance(coefficient_defect, ScalarQuantity):
            raise TypeError("coefficient_l2_defect must decode correctly")
        if not isinstance(sampled_l2_defect, ScalarQuantity):
            raise TypeError("sampled_l2_defect must decode correctly")
        if not isinstance(sampled_maximum_defect, ScalarQuantity):
            raise TypeError("sampled_maximum_defect must decode correctly")
        if not isinstance(bandwidth, ScalarQuantity):
            raise TypeError("bandwidth must decode correctly")
        if not isinstance(curvature, ScalarQuantity):
            raise TypeError("zone_center_curvature must decode correctly")
        if not isinstance(imaginary_residual, ScalarQuantity):
            raise TypeError("maximum_imaginary_residual must decode correctly")
        return cls(
            maximum_range,
            mediated_coefficients,
            direct_coefficients,
            mediated_construction,
            mediated_evaluation,
            direct_construction,
            direct_evaluation,
            truncation_maximum,
            truncation_rms,
            mediated_total_maximum,
            mediated_total_rms,
            direct_total_maximum,
            direct_total_rms,
            omitted_norm,
            parseval_observed,
            parseval_expected,
            parseval_residual,
            direct_design_rank,
            direct_condition,
            direct_training_l2,
            direct_training_maximum,
            coefficient_defect,
            sampled_l2_defect,
            sampled_maximum_defect,
            bandwidth,
            curvature,
            imaginary_residual,
        )


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DFourierLocalityMeshResult(BaseTypedRecord):
    """Retain one construction mesh, complete transform, and support table."""

    construction_size: int
    construction_reduced_momenta: VectorQuantity
    lowest_energies: VectorQuantity
    adjacent_energies: VectorQuantity
    complete_coefficients: ComplexVectorQuantity
    reconstructed_construction: VectorQuantity
    complete_evaluation_candidate: VectorQuantity
    reconstruction_maximum_error: ScalarQuantity
    hermiticity_maximum_error: ScalarQuantity
    interpolation_maximum_error: ScalarQuantity
    interpolation_rms_error: ScalarQuantity
    ranges: tuple[Periodic1DFourierLocalityRangeResult, ...]
    nondominated_mask: tuple[bool, ...]
    near_tie_mask: tuple[bool, ...]
    first_joint_pass: int | None
    sustained_after_first_pass: bool

    def __post_init__(self) -> None:
        if type(self.construction_size) is not int:
            raise TypeError("construction_size must be a built-in int")
        if self.construction_size <= 0 or self.construction_size % 2 != 0:
            raise ValueError("construction_size must be positive and even")
        for vector_value, name, size in (
            (
                self.construction_reduced_momenta,
                "construction_reduced_momenta",
                self.construction_size,
            ),
            (self.lowest_energies, "lowest_energies", self.construction_size),
            (self.adjacent_energies, "adjacent_energies", self.construction_size),
            (
                self.reconstructed_construction,
                "reconstructed_construction",
                self.construction_size,
            ),
        ):
            if not isinstance(vector_value, VectorQuantity):
                raise TypeError(f"{name} must be VectorQuantity")
            if not isinstance(vector_value.unit, Unitless):
                raise ValueError(f"{name} must use Unitless")
            if vector_value.magnitude.shape != (size,):
                raise ValueError(f"{name} must have shape ({size},)")
        if np.any(self.adjacent_energies.magnitude < self.lowest_energies.magnitude):
            raise ValueError("adjacent energies must not lie below lowest energies")
        if not isinstance(self.complete_coefficients, ComplexVectorQuantity):
            raise TypeError("complete_coefficients must be ComplexVectorQuantity")
        if not isinstance(self.complete_coefficients.unit, Unitless):
            raise ValueError("complete_coefficients must use Unitless")
        if self.complete_coefficients.magnitude.shape != (self.construction_size,):
            raise ValueError("complete_coefficients must match construction_size")
        if not isinstance(self.complete_evaluation_candidate, VectorQuantity):
            raise TypeError("complete_evaluation_candidate must be VectorQuantity")
        if not isinstance(self.complete_evaluation_candidate.unit, Unitless):
            raise ValueError("complete_evaluation_candidate must use Unitless")
        if self.complete_evaluation_candidate.magnitude.size <= 0:
            raise ValueError("complete_evaluation_candidate must be nonempty")
        for scalar_value, name in (
            (self.reconstruction_maximum_error, "reconstruction_maximum_error"),
            (self.hermiticity_maximum_error, "hermiticity_maximum_error"),
            (self.interpolation_maximum_error, "interpolation_maximum_error"),
            (self.interpolation_rms_error, "interpolation_rms_error"),
        ):
            if not isinstance(scalar_value, ScalarQuantity):
                raise TypeError(f"{name} must be ScalarQuantity")
            if not isinstance(scalar_value.unit, Unitless):
                raise ValueError(f"{name} must use Unitless")
            if scalar_value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if not (
            isinstance(self.ranges, tuple)
            and self.ranges
            and all(
                isinstance(value, Periodic1DFourierLocalityRangeResult)
                for value in self.ranges
            )
        ):
            raise TypeError("ranges must contain range results")
        for values, name in (
            (self.nondominated_mask, "nondominated_mask"),
            (self.near_tie_mask, "near_tie_mask"),
        ):
            if not (
                isinstance(values, tuple)
                and all(type(value) is bool for value in values)
            ):
                raise TypeError(f"{name} must be a tuple of bools")
            if len(values) != len(self.ranges):
                raise ValueError(f"{name} must align with ranges")
        if self.first_joint_pass is not None and type(self.first_joint_pass) is not int:
            raise TypeError("first_joint_pass must be int or None")
        if type(self.sustained_after_first_pass) is not bool:
            raise TypeError("sustained_after_first_pass must be a built-in bool")

    @property
    def complete_representatives(self) -> tuple[int, ...]:
        """Return the centered complete cyclic representative inventory."""
        return tuple(range(-(self.construction_size // 2), self.construction_size // 2))

    def refinement_vector(self) -> Float64Array:
        """Return the ordered normalized diagnostics used by refinement."""
        values = [
            self.interpolation_maximum_error.magnitude,
            self.interpolation_rms_error.magnitude,
        ]
        for result in self.ranges:
            values.extend(
                (
                    result.truncation_maximum_error.magnitude,
                    result.truncation_rms_error.magnitude,
                    result.mediated_total_maximum_error.magnitude,
                    result.mediated_total_rms_error.magnitude,
                    result.direct_total_maximum_error.magnitude,
                    result.direct_total_rms_error.magnitude,
                    result.omitted_coefficient_l2_norm.magnitude,
                    result.coefficient_l2_defect.magnitude,
                    result.sampled_l2_defect.magnitude,
                    result.sampled_maximum_defect.magnitude,
                )
            )
        return np.asarray(values, dtype=np.float64)

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "construction_size": self.construction_size,
            "construction_reduced_momenta": self.construction_reduced_momenta,
            "lowest_energies": self.lowest_energies,
            "adjacent_energies": self.adjacent_energies,
            "complete_coefficients": self.complete_coefficients,
            "reconstructed_construction": self.reconstructed_construction,
            "complete_evaluation_candidate": self.complete_evaluation_candidate,
            "reconstruction_maximum_error": self.reconstruction_maximum_error,
            "hermiticity_maximum_error": self.hermiticity_maximum_error,
            "interpolation_maximum_error": self.interpolation_maximum_error,
            "interpolation_rms_error": self.interpolation_rms_error,
            "ranges": self.ranges,
            "nondominated_mask": self.nondominated_mask,
            "near_tie_mask": self.near_tie_mask,
            "first_joint_pass": self.first_joint_pass,
            "sustained_after_first_pass": self.sustained_after_first_pass,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "construction_size",
            "construction_reduced_momenta",
            "lowest_energies",
            "adjacent_energies",
            "complete_coefficients",
            "reconstructed_construction",
            "complete_evaluation_candidate",
            "reconstruction_maximum_error",
            "hermiticity_maximum_error",
            "interpolation_maximum_error",
            "interpolation_rms_error",
            "ranges",
            "nondominated_mask",
            "near_tie_mask",
            "first_joint_pass",
            "sustained_after_first_pass",
        }:
            raise ValueError("Fourier-locality mesh fields do not match")
        construction_size = values["construction_size"]
        construction_momenta = values["construction_reduced_momenta"]
        lowest = values["lowest_energies"]
        adjacent = values["adjacent_energies"]
        coefficients = values["complete_coefficients"]
        reconstructed = values["reconstructed_construction"]
        evaluation_candidate = values["complete_evaluation_candidate"]
        reconstruction_error = values["reconstruction_maximum_error"]
        hermiticity_error = values["hermiticity_maximum_error"]
        interpolation_maximum = values["interpolation_maximum_error"]
        interpolation_rms = values["interpolation_rms_error"]
        ranges_value = values["ranges"]
        nondominated_value = values["nondominated_mask"]
        near_tie_value = values["near_tie_mask"]
        first_joint_pass = values["first_joint_pass"]
        sustained = values["sustained_after_first_pass"]
        if type(construction_size) is not int:
            raise TypeError("construction_size must decode to int")
        if not isinstance(construction_momenta, VectorQuantity):
            raise TypeError("construction_reduced_momenta must decode correctly")
        if not isinstance(lowest, VectorQuantity):
            raise TypeError("lowest_energies must decode correctly")
        if not isinstance(adjacent, VectorQuantity):
            raise TypeError("adjacent_energies must decode correctly")
        if not isinstance(reconstructed, VectorQuantity):
            raise TypeError("reconstructed_construction must decode correctly")
        if not isinstance(evaluation_candidate, VectorQuantity):
            raise TypeError("complete_evaluation_candidate must decode correctly")
        if not isinstance(coefficients, ComplexVectorQuantity):
            raise TypeError("complete_coefficients must decode correctly")
        if not isinstance(reconstruction_error, ScalarQuantity):
            raise TypeError("reconstruction_maximum_error must decode correctly")
        if not isinstance(hermiticity_error, ScalarQuantity):
            raise TypeError("hermiticity_maximum_error must decode correctly")
        if not isinstance(interpolation_maximum, ScalarQuantity):
            raise TypeError("interpolation_maximum_error must decode correctly")
        if not isinstance(interpolation_rms, ScalarQuantity):
            raise TypeError("interpolation_rms_error must decode correctly")
        if not isinstance(ranges_value, tuple):
            raise TypeError("ranges must decode to a tuple")
        range_mappings: list[Mapping[str, SerializableValue]] = []
        for range_value in ranges_value:
            if not isinstance(range_value, Mapping):
                raise TypeError("ranges must decode to mappings")
            range_mappings.append(range_value)
        nondominated: list[bool] = []
        if not isinstance(nondominated_value, tuple):
            raise TypeError("nondominated_mask must decode to a tuple")
        for value in nondominated_value:
            if type(value) is not bool:
                raise TypeError("nondominated_mask must decode to bools")
            nondominated.append(value)
        near_tie: list[bool] = []
        if not isinstance(near_tie_value, tuple):
            raise TypeError("near_tie_mask must decode to a tuple")
        for value in near_tie_value:
            if type(value) is not bool:
                raise TypeError("near_tie_mask must decode to bools")
            near_tie.append(value)
        if first_joint_pass is not None and type(first_joint_pass) is not int:
            raise TypeError("first_joint_pass must decode to int or None")
        if type(sustained) is not bool:
            raise TypeError("sustained_after_first_pass must decode to bool")
        return cls(
            construction_size,
            construction_momenta,
            lowest,
            adjacent,
            coefficients,
            reconstructed,
            evaluation_candidate,
            reconstruction_error,
            hermiticity_error,
            interpolation_maximum,
            interpolation_rms,
            tuple(
                Periodic1DFourierLocalityRangeResult.from_dict(value)
                for value in range_mappings
            ),
            tuple(nondominated),
            tuple(near_tie),
            first_joint_pass,
            sustained,
        )


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DFourierLocalityCalculationResult(BaseTypedRecord):
    """Compose one complete finite compatible rank-one calculation subject."""

    calculation_family: str
    configuration: Periodic1DFourierLocalityConfiguration
    evaluation: Periodic1DFourierLocalityEvaluationResult
    meshes: tuple[Periodic1DFourierLocalityMeshResult, ...]
    refinement_channel_names: tuple[str, ...]
    normalized_refinement_changes: MatrixQuantity
    refinement_coarse_first_passes: tuple[int | None, ...]
    refinement_fine_first_passes: tuple[int | None, ...]
    minimum_sampled_gap: ScalarQuantity
    gap_minimizing_role: str
    gap_minimizing_index: int
    gap_minimizing_reduced_momentum: ScalarQuantity

    def __post_init__(self) -> None:
        if self.calculation_family != "periodic1d-rank1-fourier-locality":
            raise ValueError("calculation_family does not identify Fourier locality")
        if not isinstance(self.configuration, Periodic1DFourierLocalityConfiguration):
            raise TypeError(
                "configuration must be Periodic1DFourierLocalityConfiguration"
            )
        if not isinstance(self.evaluation, Periodic1DFourierLocalityEvaluationResult):
            raise TypeError("evaluation has the wrong result type")
        if not (
            isinstance(self.meshes, tuple)
            and self.meshes
            and all(
                isinstance(value, Periodic1DFourierLocalityMeshResult)
                for value in self.meshes
            )
        ):
            raise TypeError("meshes must contain mesh results")
        if tuple(mesh.construction_size for mesh in self.meshes) != (
            self.configuration.construction_mesh_sizes
        ):
            raise ValueError("mesh results must match the configured inventory")
        if not (
            isinstance(self.refinement_channel_names, tuple)
            and self.refinement_channel_names
            and all(
                type(value) is str and value for value in self.refinement_channel_names
            )
        ):
            raise TypeError("refinement_channel_names must contain strings")
        if self.refinement_channel_names != (
            self.configuration.refinement_channel_names()
        ):
            raise ValueError(
                "refinement_channel_names differ from the semantic inventory"
            )
        if not isinstance(self.normalized_refinement_changes, MatrixQuantity):
            raise TypeError("normalized_refinement_changes must be MatrixQuantity")
        if not isinstance(self.normalized_refinement_changes.unit, Unitless):
            raise ValueError("normalized_refinement_changes must use Unitless")
        pair_count = len(self.meshes) - 1
        if self.normalized_refinement_changes.magnitude.shape != (
            pair_count,
            len(self.refinement_channel_names),
        ):
            raise ValueError("refinement matrix shape differs from its inventories")
        if np.any(self.normalized_refinement_changes.magnitude < 0.0):
            raise ValueError("refinement changes must be nonnegative")
        for values, name in (
            (
                self.refinement_coarse_first_passes,
                "refinement_coarse_first_passes",
            ),
            (self.refinement_fine_first_passes, "refinement_fine_first_passes"),
        ):
            if not (
                isinstance(values, tuple)
                and len(values) == pair_count
                and all(value is None or type(value) is int for value in values)
            ):
                raise TypeError(f"{name} must align with adjacent meshes")
        if not isinstance(self.minimum_sampled_gap, ScalarQuantity):
            raise TypeError("minimum_sampled_gap must be ScalarQuantity")
        if not isinstance(self.minimum_sampled_gap.unit, Unitless):
            raise ValueError("minimum_sampled_gap must use Unitless")
        if self.minimum_sampled_gap.magnitude < 0.0:
            raise ValueError("minimum_sampled_gap must be nonnegative")
        if self.gap_minimizing_role not in {"construction", "evaluation"}:
            raise ValueError("gap_minimizing_role must identify one sampled role")
        if type(self.gap_minimizing_index) is not int:
            raise TypeError("gap_minimizing_index must be a built-in int")
        if self.gap_minimizing_index < 0:
            raise ValueError("gap_minimizing_index must be nonnegative")
        if not isinstance(self.gap_minimizing_reduced_momentum, ScalarQuantity):
            raise TypeError("gap_minimizing_reduced_momentum must be ScalarQuantity")
        if not isinstance(self.gap_minimizing_reduced_momentum.unit, Unitless):
            raise ValueError("gap_minimizing_reduced_momentum must use Unitless")

        expected_evaluation_coordinates = np.asarray(
            self.configuration.evaluation_reduced_momenta(),
            dtype=np.float64,
        )
        if not np.array_equal(
            self.evaluation.reduced_momenta.magnitude,
            expected_evaluation_coordinates,
        ):
            raise ValueError("evaluation coordinates differ from configuration")

        absolute = self.configuration.energy_absolute_tolerance
        relative = self.configuration.relative_tolerance
        threshold = self.configuration.application_threshold
        expected_first_passes: list[int | None] = []
        for mesh in self.meshes:
            expected_construction_coordinates = np.asarray(
                [
                    -0.5 + float(index) / float(mesh.construction_size)
                    for index in range(mesh.construction_size)
                ],
                dtype=np.float64,
            )
            if not np.array_equal(
                mesh.construction_reduced_momenta.magnitude,
                expected_construction_coordinates,
            ):
                raise ValueError("construction coordinates differ from configuration")
            if tuple(result.maximum_range for result in mesh.ranges) != (
                self.configuration.maximum_ranges
            ):
                raise ValueError("range results differ from configuration")
            if mesh.complete_evaluation_candidate.magnitude.shape != (
                self.configuration.evaluation_size,
            ):
                raise ValueError("complete evaluation candidate has the wrong extent")
            complete_phases = np.exp(
                2j
                * np.pi
                * np.outer(
                    np.concatenate(
                        (
                            mesh.construction_reduced_momenta.magnitude,
                            self.evaluation.reduced_momenta.magnitude,
                        )
                    ),
                    np.asarray(mesh.complete_representatives, dtype=np.float64),
                )
            )
            complete_candidate = complete_phases @ mesh.complete_coefficients.magnitude
            construction_candidate = complete_candidate[: mesh.construction_size]
            evaluation_candidate = complete_candidate[mesh.construction_size :]
            for stored_candidate, expected_candidate, candidate_name in (
                (
                    mesh.reconstructed_construction.magnitude,
                    construction_candidate.real,
                    "reconstructed_construction",
                ),
                (
                    mesh.complete_evaluation_candidate.magnitude,
                    evaluation_candidate.real,
                    "complete_evaluation_candidate",
                ),
            ):
                defect = np.abs(stored_candidate - expected_candidate)
                limit = absolute + relative * np.maximum(
                    np.abs(stored_candidate), np.abs(expected_candidate)
                )
                if np.any(defect > limit):
                    raise ValueError(
                        f"{candidate_name} differs from complete coefficients"
                    )
            complete_lookup = dict(
                zip(
                    mesh.complete_representatives,
                    mesh.complete_coefficients.magnitude,
                    strict=True,
                )
            )
            expected_joint_passes: list[bool] = []
            mediated_total_errors: list[float] = []
            for result in mesh.ranges:
                expected_mediated_coefficients = np.asarray(
                    [complete_lookup[value] for value in result.representatives],
                    dtype=np.complex128,
                )
                if not np.array_equal(
                    result.mediated_coefficients.magnitude,
                    expected_mediated_coefficients,
                ):
                    raise ValueError(
                        "mediated coefficients are not complete-transform truncations"
                    )
                for coefficients, construction, evaluation, route in (
                    (
                        result.mediated_coefficients.magnitude,
                        result.mediated_construction_candidate.magnitude,
                        result.mediated_evaluation_candidate.magnitude,
                        "mediated",
                    ),
                    (
                        result.direct_coefficients.magnitude,
                        result.direct_construction_candidate.magnitude,
                        result.direct_evaluation_candidate.magnitude,
                        "direct",
                    ),
                ):
                    representatives = np.asarray(
                        result.representatives,
                        dtype=np.float64,
                    )
                    for coordinates, stored, role in (
                        (
                            mesh.construction_reduced_momenta.magnitude,
                            construction,
                            "construction",
                        ),
                        (
                            self.evaluation.reduced_momenta.magnitude,
                            evaluation,
                            "evaluation",
                        ),
                    ):
                        expected_candidate = (
                            np.exp(2j * np.pi * np.outer(coordinates, representatives))
                            @ coefficients
                        ).real
                        defect = np.abs(stored - expected_candidate)
                        limit = absolute + relative * np.maximum(
                            np.abs(stored), np.abs(expected_candidate)
                        )
                        if np.any(defect > limit):
                            raise ValueError(
                                f"{route} {role} candidate differs from "
                                "its coefficients"
                            )
                mediated_error = float(
                    np.max(
                        np.abs(
                            self.evaluation.lowest_energies.magnitude
                            - result.mediated_evaluation_candidate.magnitude
                        )
                    )
                )
                direct_error = float(
                    np.max(
                        np.abs(
                            self.evaluation.lowest_energies.magnitude
                            - result.direct_evaluation_candidate.magnitude
                        )
                    )
                )
                for stored_error, expected_error, route in (
                    (
                        result.mediated_total_maximum_error.magnitude,
                        mediated_error,
                        "mediated",
                    ),
                    (
                        result.direct_total_maximum_error.magnitude,
                        direct_error,
                        "direct",
                    ),
                ):
                    if abs(stored_error - expected_error) > absolute + relative * max(
                        abs(stored_error), abs(expected_error)
                    ):
                        raise ValueError(
                            f"{route} total maximum error differs from its candidate"
                        )
                    if (stored_error <= threshold) is not (expected_error <= threshold):
                        raise ValueError(
                            f"{route} total error reverses its threshold disposition"
                        )
                mediated_total_errors.append(mediated_error)
                expected_joint_passes.append(
                    mediated_error <= threshold and direct_error <= threshold
                )
            expected_nondominated = tuple(
                not any(
                    other_index != candidate_index
                    and mesh.ranges[other_index].maximum_range
                    <= mesh.ranges[candidate_index].maximum_range
                    and mediated_total_errors[other_index]
                    <= mediated_total_errors[candidate_index]
                    and (
                        mesh.ranges[other_index].maximum_range
                        < mesh.ranges[candidate_index].maximum_range
                        or mediated_total_errors[other_index]
                        < mediated_total_errors[candidate_index]
                    )
                    for other_index in range(len(mesh.ranges))
                )
                for candidate_index in range(len(mesh.ranges))
            )
            if mesh.nondominated_mask != expected_nondominated:
                raise ValueError("nondominated_mask differs from the attained table")
            expected_near_tie = tuple(
                expected_nondominated[candidate_index]
                and any(
                    other_index != candidate_index
                    and expected_nondominated[other_index]
                    and abs(
                        mediated_total_errors[candidate_index]
                        - mediated_total_errors[other_index]
                    )
                    <= absolute
                    + relative
                    * max(
                        abs(mediated_total_errors[candidate_index]),
                        abs(mediated_total_errors[other_index]),
                    )
                    for other_index in range(len(mesh.ranges))
                )
                for candidate_index in range(len(mesh.ranges))
            )
            if mesh.near_tie_mask != expected_near_tie:
                raise ValueError("near_tie_mask differs from the consistency rule")
            passing_ranges = tuple(
                result.maximum_range
                for result, passes in zip(
                    mesh.ranges,
                    expected_joint_passes,
                    strict=True,
                )
                if passes
            )
            expected_first = passing_ranges[0] if passing_ranges else None
            if mesh.first_joint_pass != expected_first:
                raise ValueError("first_joint_pass differs from total-error gates")
            expected_sustained = expected_first is not None and all(
                passes
                for result, passes in zip(
                    mesh.ranges,
                    expected_joint_passes,
                    strict=True,
                )
                if result.maximum_range >= expected_first
            )
            if mesh.sustained_after_first_pass is not expected_sustained:
                raise ValueError(
                    "sustained_after_first_pass differs from support table"
                )
            expected_first_passes.append(expected_first)

        expected_changes = np.vstack(
            [
                np.abs(fine.refinement_vector() - coarse.refinement_vector())
                for coarse, fine in zip(self.meshes[:-1], self.meshes[1:], strict=True)
            ]
        )
        if not np.allclose(
            self.normalized_refinement_changes.magnitude,
            expected_changes,
            rtol=0.0,
            atol=self.configuration.dimensionless_absolute_tolerance,
        ):
            raise ValueError("refinement changes differ from mesh diagnostics")
        if self.refinement_coarse_first_passes != tuple(expected_first_passes[:-1]):
            raise ValueError("coarse refinement passages differ from mesh results")
        if self.refinement_fine_first_passes != tuple(expected_first_passes[1:]):
            raise ValueError("fine refinement passages differ from mesh results")

        production = self.meshes[-1]
        production_gaps = (
            production.adjacent_energies.magnitude
            - production.lowest_energies.magnitude
        )
        evaluation_gaps = self.evaluation.sampled_gaps.magnitude
        construction_index = int(np.argmin(production_gaps))
        evaluation_index = int(np.argmin(evaluation_gaps))
        construction_gap = float(production_gaps[construction_index])
        evaluation_gap = float(evaluation_gaps[evaluation_index])
        if construction_gap <= evaluation_gap:
            expected_gap = construction_gap
            expected_role = "construction"
            expected_index = construction_index
            expected_momentum = float(
                production.construction_reduced_momenta.magnitude[construction_index]
            )
        else:
            expected_gap = evaluation_gap
            expected_role = "evaluation"
            expected_index = evaluation_index
            expected_momentum = float(
                self.evaluation.reduced_momenta.magnitude[evaluation_index]
            )
        stored_gap = self.minimum_sampled_gap.magnitude
        if abs(stored_gap - expected_gap) > absolute + relative * max(
            abs(stored_gap), abs(expected_gap)
        ):
            raise ValueError("minimum_sampled_gap differs from parent bands")
        gap_threshold = self.configuration.sampled_gap_threshold
        if (stored_gap >= gap_threshold) is not (expected_gap >= gap_threshold):
            raise ValueError("minimum sampled gap reverses its threshold disposition")
        if (
            self.gap_minimizing_role != expected_role
            or self.gap_minimizing_index != expected_index
            or self.gap_minimizing_reduced_momentum.magnitude != expected_momentum
        ):
            raise ValueError("sampled-gap minimizer differs from parent bands")

    @property
    def finite_qualification_passes(self) -> bool:
        """Return the bounded conjunction of sampled finite gates."""
        final_changes_pass = bool(
            np.all(
                self.normalized_refinement_changes.magnitude[-1]
                <= self.configuration.refinement_tolerance
            )
        )
        passage_stable = (
            self.refinement_coarse_first_passes[-1]
            == self.refinement_fine_first_passes[-1]
        )
        production = self.meshes[-1]
        return (
            self.minimum_sampled_gap.magnitude
            >= self.configuration.sampled_gap_threshold
            and final_changes_pass
            and passage_stable
            and production.first_joint_pass is not None
            and production.sustained_after_first_pass
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "calculation_family": self.calculation_family,
            "configuration": self.configuration,
            "evaluation": self.evaluation,
            "meshes": self.meshes,
            "refinement_channel_names": self.refinement_channel_names,
            "normalized_refinement_changes": self.normalized_refinement_changes,
            "refinement_coarse_first_passes": self.refinement_coarse_first_passes,
            "refinement_fine_first_passes": self.refinement_fine_first_passes,
            "minimum_sampled_gap": self.minimum_sampled_gap,
            "gap_minimizing_role": self.gap_minimizing_role,
            "gap_minimizing_index": self.gap_minimizing_index,
            "gap_minimizing_reduced_momentum": (self.gap_minimizing_reduced_momentum),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "calculation_family",
            "configuration",
            "evaluation",
            "meshes",
            "refinement_channel_names",
            "normalized_refinement_changes",
            "refinement_coarse_first_passes",
            "refinement_fine_first_passes",
            "minimum_sampled_gap",
            "gap_minimizing_role",
            "gap_minimizing_index",
            "gap_minimizing_reduced_momentum",
        }:
            raise ValueError("Fourier-locality calculation fields do not match")
        family = values["calculation_family"]
        configuration_value = values["configuration"]
        evaluation_value = values["evaluation"]
        meshes_value = values["meshes"]
        channel_names_value = values["refinement_channel_names"]
        changes = values["normalized_refinement_changes"]
        coarse_value = values["refinement_coarse_first_passes"]
        fine_value = values["refinement_fine_first_passes"]
        minimum_gap = values["minimum_sampled_gap"]
        gap_role = values["gap_minimizing_role"]
        gap_index = values["gap_minimizing_index"]
        gap_momentum = values["gap_minimizing_reduced_momentum"]
        if type(family) is not str:
            raise TypeError("calculation_family must decode to str")
        if not isinstance(configuration_value, Mapping):
            raise TypeError("configuration must decode to a mapping")
        if not isinstance(evaluation_value, Mapping):
            raise TypeError("evaluation must decode to a mapping")
        if not (
            isinstance(meshes_value, tuple)
            and all(isinstance(value, Mapping) for value in meshes_value)
        ):
            raise TypeError("meshes must decode to mappings")
        channel_names: list[str] = []
        if not isinstance(channel_names_value, tuple):
            raise TypeError("refinement_channel_names must decode to a tuple")
        for value in channel_names_value:
            if type(value) is not str:
                raise TypeError("refinement_channel_names must decode to strings")
            channel_names.append(value)
        if not isinstance(changes, MatrixQuantity):
            raise TypeError("normalized_refinement_changes must decode correctly")
        coarse: list[int | None] = []
        if not isinstance(coarse_value, tuple):
            raise TypeError("refinement_coarse_first_passes must decode to tuple")
        for value in coarse_value:
            if value is not None and type(value) is not int:
                raise TypeError("coarse first passages must decode to int or None")
            coarse.append(value)
        fine: list[int | None] = []
        if not isinstance(fine_value, tuple):
            raise TypeError("refinement_fine_first_passes must decode to tuple")
        for value in fine_value:
            if value is not None and type(value) is not int:
                raise TypeError("fine first passages must decode to int or None")
            fine.append(value)
        if not isinstance(minimum_gap, ScalarQuantity):
            raise TypeError("minimum_sampled_gap must decode correctly")
        if type(gap_role) is not str or type(gap_index) is not int:
            raise TypeError("gap minimizer labels must decode correctly")
        if not isinstance(gap_momentum, ScalarQuantity):
            raise TypeError("gap_minimizing_reduced_momentum must decode correctly")
        return cls(
            family,
            Periodic1DFourierLocalityConfiguration.from_dict(configuration_value),
            Periodic1DFourierLocalityEvaluationResult.from_dict(evaluation_value),
            tuple(
                Periodic1DFourierLocalityMeshResult.from_dict(value)
                for value in meshes_value
            ),
            tuple(channel_names),
            changes,
            tuple(coarse),
            tuple(fine),
            minimum_gap,
            gap_role,
            gap_index,
            gap_momentum,
        )


__all__ = [
    "Periodic1DFourierLocalityCalculationResult",
    "Periodic1DFourierLocalityEvaluationResult",
    "Periodic1DFourierLocalityMeshResult",
    "Periodic1DFourierLocalityRangeResult",
]
