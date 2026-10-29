"""Authenticated Mathieu1D visualization projection."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

import numpy as np
from projectkoios.physkit.units import MatrixQuantity, Unitless, VectorQuantity

from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.visualizations import BaseVisualizationData

from ..result import Mathieu1dCalculationResult


@dataclass(frozen=True, slots=True, eq=False)
class Mathieu1dVisualizationData(BaseVisualizationData):
    """Retain only independently reconstructed values required by the figures.

    Parameters
    ----------
    plane_wave_cutoffs, plane_wave_maximum_errors
        Ordered finite plane-wave refinement inventory.
    finite_difference_points, finite_difference_maximum_errors
        Ordered periodic finite-difference refinement inventory.
    parent_reduced_momenta, parent_reference_energies
        Sampled parent coordinates and ordered finite reference bands.
    training_reduced_momenta, training_selected_energies
        Construction-mesh selected-band values.
    evaluation_reduced_momenta, evaluation_selected_energies
        Withheld coordinates and selected-band values.
    evaluation_candidates
        One mediated reconstruction per range on the withheld coordinates.
    complete_representatives, complete_hopping_magnitudes
        Complete finite-transform inventory used by the hopping panel.
    hopping_ranges, training_maximum_errors, evaluation_maximum_errors
        Authenticated range inventory and sampled errors.
    omitted_block_l2_norms, route_coefficient_l2_defects
        Authenticated range-indexed locality and route diagnostics.

    Notes
    -----
    The projection contains no thresholds, fits, interpolation, or scientific decisions
    created by rendering. Every value already belongs to the verified typed result.
    """

    plane_wave_cutoffs: tuple[int, ...]
    plane_wave_maximum_errors: VectorQuantity
    finite_difference_points: tuple[int, ...]
    finite_difference_maximum_errors: VectorQuantity
    parent_reduced_momenta: VectorQuantity
    parent_reference_energies: MatrixQuantity
    training_reduced_momenta: VectorQuantity
    training_selected_energies: VectorQuantity
    evaluation_reduced_momenta: VectorQuantity
    evaluation_selected_energies: VectorQuantity
    evaluation_candidates: MatrixQuantity
    complete_representatives: tuple[int, ...]
    complete_hopping_magnitudes: VectorQuantity
    hopping_ranges: tuple[int, ...]
    training_maximum_errors: VectorQuantity
    evaluation_maximum_errors: VectorQuantity
    omitted_block_l2_norms: VectorQuantity
    route_coefficient_l2_defects: VectorQuantity

    def __post_init__(self) -> None:
        integer_fields = (
            "plane_wave_cutoffs",
            "finite_difference_points",
            "complete_representatives",
            "hopping_ranges",
        )
        for name in integer_fields:
            value = getattr(self, name)
            if not (
                isinstance(value, tuple)
                and value
                and all(type(item) is int for item in value)
            ):
                raise TypeError(f"{name} must be a nonempty tuple of ints")
        vector_fields = (
            "plane_wave_maximum_errors",
            "finite_difference_maximum_errors",
            "parent_reduced_momenta",
            "training_reduced_momenta",
            "training_selected_energies",
            "evaluation_reduced_momenta",
            "evaluation_selected_energies",
            "complete_hopping_magnitudes",
            "training_maximum_errors",
            "evaluation_maximum_errors",
            "omitted_block_l2_norms",
            "route_coefficient_l2_defects",
        )
        for name in vector_fields:
            value = getattr(self, name)
            if not isinstance(value, VectorQuantity):
                raise TypeError(f"{name} must be VectorQuantity")
            if not isinstance(value.unit, Unitless):
                raise ValueError(f"{name} must use Unitless")
        for name in ("parent_reference_energies", "evaluation_candidates"):
            value = getattr(self, name)
            if not isinstance(value, MatrixQuantity):
                raise TypeError(f"{name} must be MatrixQuantity")
            if not isinstance(value.unit, Unitless):
                raise ValueError(f"{name} must use Unitless")
        # Inventory lengths are part of authentication: a renderer must not silently
        # drop or append values while retaining a valid quantity container.
        lengths = {
            "plane_wave_maximum_errors": len(self.plane_wave_cutoffs),
            "finite_difference_maximum_errors": len(self.finite_difference_points),
            "complete_hopping_magnitudes": len(self.complete_representatives),
            "training_maximum_errors": len(self.hopping_ranges),
            "evaluation_maximum_errors": len(self.hopping_ranges),
            "omitted_block_l2_norms": len(self.hopping_ranges),
            "route_coefficient_l2_defects": len(self.hopping_ranges),
        }
        for name, size in lengths.items():
            if getattr(self, name).magnitude.shape != (size,):
                raise ValueError(f"{name} shape does not match its inventory")
        if self.parent_reference_energies.magnitude.shape[0] != (
            self.parent_reduced_momenta.magnitude.size
        ):
            raise ValueError("parent reference rows must match parent coordinates")
        evaluation_size = self.evaluation_reduced_momenta.magnitude.size
        if self.evaluation_selected_energies.magnitude.shape != (evaluation_size,):
            raise ValueError("evaluation band must match evaluation coordinates")
        if self.evaluation_candidates.magnitude.shape != (
            len(self.hopping_ranges),
            evaluation_size,
        ):
            raise ValueError("evaluation candidates must match ranges and coordinates")
        if self.training_selected_energies.magnitude.shape != (
            self.training_reduced_momenta.magnitude.size,
        ):
            raise ValueError("training band must match training coordinates")

    @classmethod
    def from_result(
        cls, result: Mathieu1dCalculationResult
    ) -> Mathieu1dVisualizationData:
        """Project one independently reconstructed result into plot data.

        Parameters
        ----------
        result
            Typed result reconstructed by an independent verifier route.

        Returns
        -------
        Mathieu1dVisualizationData
            Closed plot-data projection containing no inferred values.
        """
        if not isinstance(result, Mathieu1dCalculationResult):
            raise TypeError("result must be Mathieu1dCalculationResult")
        # Derive presentation magnitudes once at the authenticated projection boundary.
        # Figure actions below may select layout and styling but calculate no new data.
        unit = Unitless()
        return cls(
            plane_wave_cutoffs=result.refinement.plane_wave_cutoffs,
            plane_wave_maximum_errors=result.refinement.plane_wave_maximum_errors,
            finite_difference_points=result.refinement.finite_difference_points,
            finite_difference_maximum_errors=(
                result.refinement.finite_difference_maximum_errors
            ),
            parent_reduced_momenta=result.refinement.parent_reduced_momenta,
            parent_reference_energies=result.refinement.parent_reference_energies,
            training_reduced_momenta=result.bands.training_reduced_momenta,
            training_selected_energies=result.bands.training_selected_energies,
            evaluation_reduced_momenta=result.bands.evaluation_reduced_momenta,
            evaluation_selected_energies=result.bands.evaluation_selected_energies,
            evaluation_candidates=MatrixQuantity(
                np.asarray(
                    [
                        value.evaluation_candidate.magnitude.real
                        for value in result.ranges
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            complete_representatives=result.transform.representatives,
            complete_hopping_magnitudes=VectorQuantity(
                np.abs(result.transform.hopping_blocks.magnitude), unit
            ),
            hopping_ranges=tuple(value.maximum_range for value in result.ranges),
            training_maximum_errors=VectorQuantity(
                np.asarray(
                    [value.training_maximum_error.magnitude for value in result.ranges],
                    dtype=np.float64,
                ),
                unit,
            ),
            evaluation_maximum_errors=VectorQuantity(
                np.asarray(
                    [
                        value.evaluation_maximum_error.magnitude
                        for value in result.ranges
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            omitted_block_l2_norms=VectorQuantity(
                np.asarray(
                    [value.omitted_block_l2_norm.magnitude for value in result.ranges],
                    dtype=np.float64,
                ),
                unit,
            ),
            route_coefficient_l2_defects=VectorQuantity(
                np.asarray(
                    [
                        value.route_coefficient_l2_defect.magnitude
                        for value in result.ranges
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "plane_wave_cutoffs": self.plane_wave_cutoffs,
            "plane_wave_maximum_errors": self.plane_wave_maximum_errors,
            "finite_difference_points": self.finite_difference_points,
            "finite_difference_maximum_errors": (self.finite_difference_maximum_errors),
            "parent_reduced_momenta": self.parent_reduced_momenta,
            "parent_reference_energies": self.parent_reference_energies,
            "training_reduced_momenta": self.training_reduced_momenta,
            "training_selected_energies": self.training_selected_energies,
            "evaluation_reduced_momenta": self.evaluation_reduced_momenta,
            "evaluation_selected_energies": self.evaluation_selected_energies,
            "evaluation_candidates": self.evaluation_candidates,
            "complete_representatives": self.complete_representatives,
            "complete_hopping_magnitudes": self.complete_hopping_magnitudes,
            "hopping_ranges": self.hopping_ranges,
            "training_maximum_errors": self.training_maximum_errors,
            "evaluation_maximum_errors": self.evaluation_maximum_errors,
            "omitted_block_l2_norms": self.omitted_block_l2_norms,
            "route_coefficient_l2_defects": self.route_coefficient_l2_defects,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        fields = {
            "plane_wave_cutoffs",
            "plane_wave_maximum_errors",
            "finite_difference_points",
            "finite_difference_maximum_errors",
            "parent_reduced_momenta",
            "parent_reference_energies",
            "training_reduced_momenta",
            "training_selected_energies",
            "evaluation_reduced_momenta",
            "evaluation_selected_energies",
            "evaluation_candidates",
            "complete_representatives",
            "complete_hopping_magnitudes",
            "hopping_ranges",
            "training_maximum_errors",
            "evaluation_maximum_errors",
            "omitted_block_l2_norms",
            "route_coefficient_l2_defects",
        }
        if set(values) != fields:
            raise ValueError("Mathieu1D visualization-data fields do not match")
        integer_names = (
            "plane_wave_cutoffs",
            "finite_difference_points",
            "complete_representatives",
            "hopping_ranges",
        )
        integers: dict[str, tuple[int, ...]] = {}
        for name in integer_names:
            value = values[name]
            if not (
                isinstance(value, tuple) and all(type(item) is int for item in value)
            ):
                raise TypeError(f"{name} must decode to a tuple of ints")
            integers[name] = value
        vector_names = (
            fields
            - set(integer_names)
            - {
                "parent_reference_energies",
                "evaluation_candidates",
            }
        )
        vectors: dict[str, VectorQuantity] = {}
        for name in vector_names:
            value = values[name]
            if not isinstance(value, VectorQuantity):
                raise TypeError(f"{name} must decode to VectorQuantity")
            vectors[name] = value
        parent = values["parent_reference_energies"]
        candidates = values["evaluation_candidates"]
        if not isinstance(parent, MatrixQuantity) or not isinstance(
            candidates, MatrixQuantity
        ):
            raise TypeError("visualization matrices must decode to MatrixQuantity")
        return cls(
            plane_wave_cutoffs=integers["plane_wave_cutoffs"],
            plane_wave_maximum_errors=vectors["plane_wave_maximum_errors"],
            finite_difference_points=integers["finite_difference_points"],
            finite_difference_maximum_errors=vectors[
                "finite_difference_maximum_errors"
            ],
            parent_reduced_momenta=vectors["parent_reduced_momenta"],
            parent_reference_energies=parent,
            training_reduced_momenta=vectors["training_reduced_momenta"],
            training_selected_energies=vectors["training_selected_energies"],
            evaluation_reduced_momenta=vectors["evaluation_reduced_momenta"],
            evaluation_selected_energies=vectors["evaluation_selected_energies"],
            evaluation_candidates=candidates,
            complete_representatives=integers["complete_representatives"],
            complete_hopping_magnitudes=vectors["complete_hopping_magnitudes"],
            hopping_ranges=integers["hopping_ranges"],
            training_maximum_errors=vectors["training_maximum_errors"],
            evaluation_maximum_errors=vectors["evaluation_maximum_errors"],
            omitted_block_l2_norms=vectors["omitted_block_l2_norms"],
            route_coefficient_l2_defects=vectors["route_coefficient_l2_defects"],
        )
