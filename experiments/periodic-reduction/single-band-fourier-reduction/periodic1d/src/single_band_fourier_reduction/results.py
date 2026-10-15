"""Typed outputs of the single-band Fourier-reduction experiment."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from ksdft2effmass.analysis.periodic_bands import (
    BandGapResult1D,
    BandSpectrumSamples1D,
)
from ksdft2effmass.analysis.single_band_reduction import (
    SingleBandHoppingReductionResult1D,
)
from ksdft2effmass.operators import ScalarQuantity

from .definition import SingleBandFourierReductionExperimentDefinition


@dataclass(frozen=True, slots=True)
class PlaneWaveRefinementObservation:
    """Retain one cutoff error against the finite represented reference."""

    cutoff: int
    maximum_absolute_error: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate one positive cutoff and nonnegative error quantity."""
        if type(self.cutoff) is not int:
            raise TypeError("cutoff must be a built-in int")
        if self.cutoff <= 0:
            raise ValueError("cutoff must be positive")
        if type(self.maximum_absolute_error) is not ScalarQuantity:
            raise TypeError("maximum_absolute_error must be ScalarQuantity")
        if self.maximum_absolute_error.magnitude < 0.0:
            raise ValueError("maximum_absolute_error must be nonnegative")


@dataclass(frozen=True, slots=True)
class FiniteDifferenceRefinementObservation:
    """Retain one grid error against the same finite represented reference."""

    point_count: int
    maximum_absolute_error: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate one finite grid extent and nonnegative error quantity."""
        if type(self.point_count) is not int:
            raise TypeError("point_count must be a built-in int")
        if self.point_count < 3:
            raise ValueError("point_count must be at least three")
        if type(self.maximum_absolute_error) is not ScalarQuantity:
            raise TypeError("maximum_absolute_error must be ScalarQuantity")
        if self.maximum_absolute_error.magnitude < 0.0:
            raise ValueError("maximum_absolute_error must be nonnegative")


@dataclass(frozen=True, slots=True, eq=False)
class SingleBandFourierReductionExperimentResult:
    """Correlate parent refinement, sampled gaps, and reusable reduction output."""

    definition: SingleBandFourierReductionExperimentDefinition
    parent_reference: BandSpectrumSamples1D
    plane_wave_refinement: tuple[PlaneWaveRefinementObservation, ...]
    finite_difference_refinement: tuple[FiniteDifferenceRefinementObservation, ...]
    training_gap: BandGapResult1D
    evaluation_gap: BandGapResult1D
    reduction: SingleBandHoppingReductionResult1D

    def __post_init__(self) -> None:
        """Validate exact experiment inventories and cross-layer correlations."""
        if type(self.definition) is not SingleBandFourierReductionExperimentDefinition:
            raise TypeError(
                "definition must be SingleBandFourierReductionExperimentDefinition"
            )
        if type(self.parent_reference) is not BandSpectrumSamples1D:
            raise TypeError("parent_reference must be BandSpectrumSamples1D")
        if not isinstance(self.plane_wave_refinement, tuple) or any(
            type(item) is not PlaneWaveRefinementObservation
            for item in self.plane_wave_refinement
        ):
            raise TypeError("plane_wave_refinement must be a typed tuple")
        if not isinstance(self.finite_difference_refinement, tuple) or any(
            type(item) is not FiniteDifferenceRefinementObservation
            for item in self.finite_difference_refinement
        ):
            raise TypeError("finite_difference_refinement must be a typed tuple")
        if tuple(item.cutoff for item in self.plane_wave_refinement) != (
            self.definition.plane_wave_cutoffs
        ):
            raise ValueError("plane-wave observations must match declared cutoffs")
        if tuple(item.point_count for item in self.finite_difference_refinement) != (
            self.definition.finite_difference_points
        ):
            raise ValueError("finite-difference observations must match declared grids")
        if self.parent_reference.band_count != self.definition.compared_band_count:
            raise ValueError("parent reference must contain the compared bands")
        expected_parent_coordinates = (
            self.definition.parent_model.reciprocal_vector.magnitude
            * np.asarray(
                self.definition.parent_sample_reduced_momenta,
                dtype=np.float64,
            )
        )
        if not np.array_equal(
            self.parent_reference.coordinates.magnitude,
            expected_parent_coordinates,
        ):
            raise ValueError("parent reference must use the declared coordinates")
        if type(self.training_gap) is not BandGapResult1D:
            raise TypeError("training_gap must be BandGapResult1D")
        if type(self.evaluation_gap) is not BandGapResult1D:
            raise TypeError("evaluation_gap must be BandGapResult1D")
        if type(self.reduction) is not SingleBandHoppingReductionResult1D:
            raise TypeError("reduction must be SingleBandHoppingReductionResult1D")
        selection = self.definition.selected_band_index
        if (
            self.training_gap.selection.lower_index != selection
            or self.training_gap.selection.upper_index != selection
        ):
            raise ValueError("training gap must use the selected band")
        if (
            self.evaluation_gap.selection.lower_index != selection
            or self.evaluation_gap.selection.upper_index != selection
        ):
            raise ValueError("evaluation gap must use the selected band")
        if self.training_gap.external_minimum_gap is None:
            raise ValueError("training gap must retain an external neighbor")
        if self.evaluation_gap.external_minimum_gap is None:
            raise ValueError("evaluation gap must retain an external neighbor")
        request = self.reduction.request
        if (
            request.training_target.coordinates.unit
            != self.training_gap.spectrum.coordinates.unit
            or not np.array_equal(
                request.training_target.coordinates.magnitude,
                self.training_gap.spectrum.coordinates.magnitude,
            )
        ):
            raise ValueError(
                "training reduction and sampled gap coordinates must agree"
            )
        if (
            request.evaluation_target.coordinates.unit
            != self.evaluation_gap.spectrum.coordinates.unit
            or not np.array_equal(
                request.evaluation_target.coordinates.magnitude,
                self.evaluation_gap.spectrum.coordinates.magnitude,
            )
        ):
            raise ValueError(
                "evaluation reduction and sampled gap coordinates must agree"
            )
        if not np.array_equal(
            request.training_target.eigenvalues.magnitude[:, 0],
            self.training_gap.spectrum.eigenvalues.magnitude[:, selection],
        ):
            raise ValueError("training target must contain the selected band")
        if not np.array_equal(
            request.evaluation_target.eigenvalues.magnitude[:, 0],
            self.evaluation_gap.spectrum.eigenvalues.magnitude[:, selection],
        ):
            raise ValueError("evaluation target must contain the selected band")


__all__ = [
    "FiniteDifferenceRefinementObservation",
    "PlaneWaveRefinementObservation",
    "SingleBandFourierReductionExperimentResult",
]
