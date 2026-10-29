"""Authenticated rank-one Fourier-locality projection."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.visualizations import BaseVisualizationData


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DFourierLocalityVisualizationData(BaseVisualizationData):
    """Retain exactly the verifier-authenticated values used by both figures."""

    evaluation_reduced_momenta: VectorQuantity
    evaluation_lowest_energies: VectorQuantity
    evaluation_adjacent_energies: VectorQuantity
    evaluation_sampled_gaps: VectorQuantity
    production_reduced_momenta: VectorQuantity
    production_sampled_gaps: VectorQuantity
    construction_sizes: tuple[int, ...]
    maximum_ranges: tuple[int, ...]
    interpolation_maximum_errors: VectorQuantity
    refinement_maximum_changes: VectorQuantity
    truncation_maximum_errors: MatrixQuantity
    mediated_total_maximum_errors: MatrixQuantity
    direct_total_maximum_errors: MatrixQuantity
    omitted_coefficient_l2_norms: MatrixQuantity
    coefficient_l2_defects: MatrixQuantity
    sampled_maximum_defects: MatrixQuantity
    production_complete_representatives: tuple[int, ...]
    production_complete_coefficient_magnitudes: VectorQuantity
    nondominated_masks: tuple[tuple[bool, ...], ...]
    near_tie_masks: tuple[tuple[bool, ...], ...]
    first_joint_passes: tuple[int | None, ...]
    sustained_after_first_passes: tuple[bool, ...]
    minimum_sampled_gap: ScalarQuantity
    sampled_gap_threshold: ScalarQuantity
    application_threshold: ScalarQuantity

    def __post_init__(self) -> None:
        for value, name in (
            (self.evaluation_reduced_momenta, "evaluation_reduced_momenta"),
            (self.evaluation_lowest_energies, "evaluation_lowest_energies"),
            (self.evaluation_adjacent_energies, "evaluation_adjacent_energies"),
            (self.evaluation_sampled_gaps, "evaluation_sampled_gaps"),
            (self.production_reduced_momenta, "production_reduced_momenta"),
            (self.production_sampled_gaps, "production_sampled_gaps"),
            (self.interpolation_maximum_errors, "interpolation_maximum_errors"),
            (self.refinement_maximum_changes, "refinement_maximum_changes"),
            (
                self.production_complete_coefficient_magnitudes,
                "production_complete_coefficient_magnitudes",
            ),
        ):
            if not isinstance(value, VectorQuantity):
                raise TypeError(f"{name} must be VectorQuantity")
            if not isinstance(value.unit, Unitless):
                raise ValueError(f"{name} must use Unitless")
        evaluation_size = self.evaluation_reduced_momenta.magnitude.size
        if evaluation_size <= 0 or any(
            value.magnitude.shape != (evaluation_size,)
            for value in (
                self.evaluation_lowest_energies,
                self.evaluation_adjacent_energies,
                self.evaluation_sampled_gaps,
            )
        ):
            raise ValueError("evaluation vectors must share one nonempty extent")
        for values, name in (
            (self.construction_sizes, "construction_sizes"),
            (self.maximum_ranges, "maximum_ranges"),
            (
                self.production_complete_representatives,
                "production_complete_representatives",
            ),
        ):
            if not (
                isinstance(values, tuple)
                and values
                and all(type(value) is int for value in values)
            ):
                raise TypeError(f"{name} must contain built-in integers")
        if self.construction_sizes != tuple(sorted(set(self.construction_sizes))):
            raise ValueError("construction_sizes must be strictly increasing")
        if self.maximum_ranges != tuple(sorted(set(self.maximum_ranges))):
            raise ValueError("maximum_ranges must be strictly increasing")
        mesh_count = len(self.construction_sizes)
        range_count = len(self.maximum_ranges)
        if self.interpolation_maximum_errors.magnitude.shape != (mesh_count,):
            raise ValueError("interpolation errors must align with meshes")
        production_size = self.production_reduced_momenta.magnitude.size
        if production_size <= 0 or self.production_sampled_gaps.magnitude.shape != (
            production_size,
        ):
            raise ValueError("production gap samples must align with coordinates")
        if self.refinement_maximum_changes.magnitude.shape != (mesh_count - 1,):
            raise ValueError("refinement maxima must align with adjacent meshes")
        for matrix_value, name in (
            (self.truncation_maximum_errors, "truncation_maximum_errors"),
            (self.mediated_total_maximum_errors, "mediated_total_maximum_errors"),
            (self.direct_total_maximum_errors, "direct_total_maximum_errors"),
            (self.omitted_coefficient_l2_norms, "omitted_coefficient_l2_norms"),
            (self.coefficient_l2_defects, "coefficient_l2_defects"),
            (self.sampled_maximum_defects, "sampled_maximum_defects"),
        ):
            if not isinstance(matrix_value, MatrixQuantity):
                raise TypeError(f"{name} must be MatrixQuantity")
            if not isinstance(matrix_value.unit, Unitless):
                raise ValueError(f"{name} must use Unitless")
            if matrix_value.magnitude.shape != (mesh_count, range_count):
                raise ValueError(f"{name} must align with meshes and ranges")
        if len(self.production_complete_representatives) != (
            self.production_complete_coefficient_magnitudes.magnitude.size
        ):
            raise ValueError("production coefficient inventory must align")
        for masks, name in (
            (self.nondominated_masks, "nondominated_masks"),
            (self.near_tie_masks, "near_tie_masks"),
        ):
            if not (
                isinstance(masks, tuple)
                and len(masks) == mesh_count
                and all(
                    isinstance(mask, tuple)
                    and len(mask) == range_count
                    and all(type(value) is bool for value in mask)
                    for mask in masks
                )
            ):
                raise TypeError(f"{name} must align with meshes and ranges")
        if not (
            isinstance(self.sustained_after_first_passes, tuple)
            and len(self.sustained_after_first_passes) == mesh_count
            and all(type(value) is bool for value in self.sustained_after_first_passes)
        ):
            raise TypeError("sustained passage flags must align with meshes")
        if not (
            isinstance(self.first_joint_passes, tuple)
            and len(self.first_joint_passes) == mesh_count
            and all(
                value is None or type(value) is int for value in self.first_joint_passes
            )
        ):
            raise TypeError("first_joint_passes must align with meshes")
        for scalar_value, name in (
            (self.minimum_sampled_gap, "minimum_sampled_gap"),
            (self.sampled_gap_threshold, "sampled_gap_threshold"),
            (self.application_threshold, "application_threshold"),
        ):
            if not isinstance(scalar_value, ScalarQuantity):
                raise TypeError(f"{name} must be ScalarQuantity")
            if not isinstance(scalar_value.unit, Unitless):
                raise ValueError(f"{name} must use Unitless")
            if scalar_value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "evaluation_reduced_momenta": self.evaluation_reduced_momenta,
            "evaluation_lowest_energies": self.evaluation_lowest_energies,
            "evaluation_adjacent_energies": self.evaluation_adjacent_energies,
            "evaluation_sampled_gaps": self.evaluation_sampled_gaps,
            "production_reduced_momenta": self.production_reduced_momenta,
            "production_sampled_gaps": self.production_sampled_gaps,
            "construction_sizes": self.construction_sizes,
            "maximum_ranges": self.maximum_ranges,
            "interpolation_maximum_errors": self.interpolation_maximum_errors,
            "refinement_maximum_changes": self.refinement_maximum_changes,
            "truncation_maximum_errors": self.truncation_maximum_errors,
            "mediated_total_maximum_errors": self.mediated_total_maximum_errors,
            "direct_total_maximum_errors": self.direct_total_maximum_errors,
            "omitted_coefficient_l2_norms": self.omitted_coefficient_l2_norms,
            "coefficient_l2_defects": self.coefficient_l2_defects,
            "sampled_maximum_defects": self.sampled_maximum_defects,
            "production_complete_representatives": (
                self.production_complete_representatives
            ),
            "production_complete_coefficient_magnitudes": (
                self.production_complete_coefficient_magnitudes
            ),
            "nondominated_masks": self.nondominated_masks,
            "near_tie_masks": self.near_tie_masks,
            "first_joint_passes": self.first_joint_passes,
            "sustained_after_first_passes": self.sustained_after_first_passes,
            "minimum_sampled_gap": self.minimum_sampled_gap,
            "sampled_gap_threshold": self.sampled_gap_threshold,
            "application_threshold": self.application_threshold,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        expected = {
            "evaluation_reduced_momenta",
            "evaluation_lowest_energies",
            "evaluation_adjacent_energies",
            "evaluation_sampled_gaps",
            "production_reduced_momenta",
            "production_sampled_gaps",
            "construction_sizes",
            "maximum_ranges",
            "interpolation_maximum_errors",
            "refinement_maximum_changes",
            "truncation_maximum_errors",
            "mediated_total_maximum_errors",
            "direct_total_maximum_errors",
            "omitted_coefficient_l2_norms",
            "coefficient_l2_defects",
            "sampled_maximum_defects",
            "production_complete_representatives",
            "production_complete_coefficient_magnitudes",
            "nondominated_masks",
            "near_tie_masks",
            "first_joint_passes",
            "sustained_after_first_passes",
            "minimum_sampled_gap",
            "sampled_gap_threshold",
            "application_threshold",
        }
        if set(values) != expected:
            raise ValueError("visualization-data fields do not match")
        evaluation_momenta = values["evaluation_reduced_momenta"]
        evaluation_lowest = values["evaluation_lowest_energies"]
        evaluation_adjacent = values["evaluation_adjacent_energies"]
        evaluation_gaps = values["evaluation_sampled_gaps"]
        production_momenta = values["production_reduced_momenta"]
        production_gaps = values["production_sampled_gaps"]
        interpolation = values["interpolation_maximum_errors"]
        refinement_maxima = values["refinement_maximum_changes"]
        coefficient_magnitudes = values["production_complete_coefficient_magnitudes"]
        for vector_value in (
            evaluation_momenta,
            evaluation_lowest,
            evaluation_adjacent,
            evaluation_gaps,
            production_momenta,
            production_gaps,
            interpolation,
            refinement_maxima,
            coefficient_magnitudes,
        ):
            if not isinstance(vector_value, VectorQuantity):
                raise TypeError("visualization vectors must decode correctly")
        truncation = values["truncation_maximum_errors"]
        mediated = values["mediated_total_maximum_errors"]
        direct = values["direct_total_maximum_errors"]
        omitted = values["omitted_coefficient_l2_norms"]
        coefficient_defects = values["coefficient_l2_defects"]
        sampled_defects = values["sampled_maximum_defects"]
        for matrix_value in (
            truncation,
            mediated,
            direct,
            omitted,
            coefficient_defects,
            sampled_defects,
        ):
            if not isinstance(matrix_value, MatrixQuantity):
                raise TypeError("visualization matrices must decode correctly")
        minimum_gap = values["minimum_sampled_gap"]
        gap_threshold = values["sampled_gap_threshold"]
        application_threshold = values["application_threshold"]
        for scalar_value in (minimum_gap, gap_threshold, application_threshold):
            if not isinstance(scalar_value, ScalarQuantity):
                raise TypeError("visualization scalars must decode correctly")
        if not isinstance(evaluation_momenta, VectorQuantity):
            raise TypeError("evaluation_reduced_momenta must decode correctly")
        if not isinstance(evaluation_lowest, VectorQuantity):
            raise TypeError("evaluation_lowest_energies must decode correctly")
        if not isinstance(evaluation_adjacent, VectorQuantity):
            raise TypeError("evaluation_adjacent_energies must decode correctly")
        if not isinstance(evaluation_gaps, VectorQuantity):
            raise TypeError("evaluation gaps must decode correctly")
        if not isinstance(production_momenta, VectorQuantity):
            raise TypeError("production momenta must decode correctly")
        if not isinstance(production_gaps, VectorQuantity):
            raise TypeError("production gaps must decode correctly")
        if not isinstance(interpolation, VectorQuantity):
            raise TypeError("interpolation errors must decode correctly")
        if not isinstance(refinement_maxima, VectorQuantity):
            raise TypeError("refinement maxima must decode correctly")
        if not isinstance(coefficient_magnitudes, VectorQuantity):
            raise TypeError("coefficient magnitudes must decode correctly")
        if not isinstance(truncation, MatrixQuantity):
            raise TypeError("truncation errors must decode correctly")
        if not isinstance(mediated, MatrixQuantity):
            raise TypeError("mediated errors must decode correctly")
        if not isinstance(direct, MatrixQuantity):
            raise TypeError("direct errors must decode correctly")
        if not isinstance(omitted, MatrixQuantity):
            raise TypeError("omitted norms must decode correctly")
        if not isinstance(coefficient_defects, MatrixQuantity):
            raise TypeError("coefficient defects must decode correctly")
        if not isinstance(sampled_defects, MatrixQuantity):
            raise TypeError("sampled defects must decode correctly")
        if not isinstance(minimum_gap, ScalarQuantity):
            raise TypeError("minimum gap must decode correctly")
        if not isinstance(gap_threshold, ScalarQuantity):
            raise TypeError("gap threshold must decode correctly")
        if not isinstance(application_threshold, ScalarQuantity):
            raise TypeError("application threshold must decode correctly")
        construction_sizes_value = values["construction_sizes"]
        maximum_ranges_value = values["maximum_ranges"]
        representatives_value = values["production_complete_representatives"]
        masks_value = values["nondominated_masks"]
        near_ties_value = values["near_tie_masks"]
        passages_value = values["first_joint_passes"]
        sustained_value = values["sustained_after_first_passes"]
        if not isinstance(construction_sizes_value, tuple):
            raise TypeError("construction_sizes must decode to a tuple")
        construction_sizes: list[int] = []
        for value in construction_sizes_value:
            if type(value) is not int:
                raise TypeError("construction_sizes must decode to integers")
            construction_sizes.append(value)
        if not isinstance(maximum_ranges_value, tuple):
            raise TypeError("maximum_ranges must decode to a tuple")
        maximum_ranges: list[int] = []
        for value in maximum_ranges_value:
            if type(value) is not int:
                raise TypeError("maximum_ranges must decode to integers")
            maximum_ranges.append(value)
        if not isinstance(representatives_value, tuple):
            raise TypeError("representatives must decode to a tuple")
        representatives: list[int] = []
        for value in representatives_value:
            if type(value) is not int:
                raise TypeError("representatives must decode to integers")
            representatives.append(value)
        if not isinstance(masks_value, tuple):
            raise TypeError("nondominated_masks must decode to a tuple")
        masks: list[tuple[bool, ...]] = []
        for mask_value in masks_value:
            if not isinstance(mask_value, tuple):
                raise TypeError("nondominated masks must decode to tuples")
            mask: list[bool] = []
            for value in mask_value:
                if type(value) is not bool:
                    raise TypeError("nondominated masks must decode to booleans")
                mask.append(value)
            masks.append(tuple(mask))
        if not isinstance(near_ties_value, tuple):
            raise TypeError("near_tie_masks must decode to a tuple")
        near_ties: list[tuple[bool, ...]] = []
        for mask_value in near_ties_value:
            if not isinstance(mask_value, tuple):
                raise TypeError("near-tie masks must decode to tuples")
            mask = []
            for value in mask_value:
                if type(value) is not bool:
                    raise TypeError("near-tie masks must decode to booleans")
                mask.append(value)
            near_ties.append(tuple(mask))
        if not isinstance(passages_value, tuple):
            raise TypeError("first_joint_passes must decode to a tuple")
        passages: list[int | None] = []
        for value in passages_value:
            if value is not None and type(value) is not int:
                raise TypeError("first passages must decode to integers or None")
            passages.append(value)
        if not isinstance(sustained_value, tuple):
            raise TypeError("sustained flags must decode to a tuple")
        sustained: list[bool] = []
        for value in sustained_value:
            if type(value) is not bool:
                raise TypeError("sustained flags must decode to booleans")
            sustained.append(value)
        return cls(
            evaluation_reduced_momenta=evaluation_momenta,
            evaluation_lowest_energies=evaluation_lowest,
            evaluation_adjacent_energies=evaluation_adjacent,
            evaluation_sampled_gaps=evaluation_gaps,
            production_reduced_momenta=production_momenta,
            production_sampled_gaps=production_gaps,
            construction_sizes=tuple(construction_sizes),
            maximum_ranges=tuple(maximum_ranges),
            interpolation_maximum_errors=interpolation,
            refinement_maximum_changes=refinement_maxima,
            truncation_maximum_errors=truncation,
            mediated_total_maximum_errors=mediated,
            direct_total_maximum_errors=direct,
            omitted_coefficient_l2_norms=omitted,
            coefficient_l2_defects=coefficient_defects,
            sampled_maximum_defects=sampled_defects,
            production_complete_representatives=tuple(representatives),
            production_complete_coefficient_magnitudes=coefficient_magnitudes,
            nondominated_masks=tuple(masks),
            near_tie_masks=tuple(near_ties),
            first_joint_passes=tuple(passages),
            sustained_after_first_passes=tuple(sustained),
            minimum_sampled_gap=minimum_gap,
            sampled_gap_threshold=gap_threshold,
            application_threshold=application_threshold,
        )
