"""Scientific controls for the periodic one-dimensional single-band experiment."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from projectkoios.physkit.units import ModelSystemUnitConverter

from ksdft2effmass.analysis.periodic_bands import (
    BandGapResult1D,
    BandSpectrumSamples1D,
)
from ksdft2effmass.analysis.single_band_reduction import (
    SingleBandHoppingReductionResult1D,
    SingleBandHoppingReductionTolerances1D,
)
from ksdft2effmass.linalg import (
    ScalarQuantity,
    VectorQuantity,
)
from ksdft2effmass.periodic1d.model import Periodic1DFourierHamiltonianToyModel

from ...study import (
    ModelId,
    ModelSystemStudyBase,
    ModelSystemStudyIdentity,
    ModelSystemStudySchemaId,
)


def _increasing_integers(
    name: str, values: tuple[int, ...], *, allow_zero: bool
) -> None:
    """Validate one exact increasing built-in integer inventory."""
    if not isinstance(values, tuple) or not values:
        raise TypeError(f"{name} must be a nonempty tuple")
    if any(type(value) is not int for value in values):
        raise TypeError(f"{name} must contain built-in integers")
    if tuple(sorted(set(values))) != values:
        raise ValueError(f"{name} must be unique and strictly increasing")
    lower = 0 if allow_zero else 1
    if values[0] < lower:
        qualifier = "nonnegative" if allow_zero else "positive"
        raise ValueError(f"{name} must contain {qualifier} values")


@dataclass(frozen=True, slots=True)
class Mathieu1dStudyDefinition(ModelSystemStudyBase):
    """Freeze one parent-refinement and single-band reduction study.

    The experiment selects a finite Fourier parent, parent-representation sweeps, one
    retained band, disjoint reciprocal sample roles, fitting weights, hopping ranges,
    and numerical-consistency tolerances. It does not select a scientifically adequate
    range or interpret the observed sampled gap as a continuum isolation certificate.
    """

    parent_model: Periodic1DFourierHamiltonianToyModel
    plane_wave_cutoffs: tuple[int, ...]
    plane_wave_reference_cutoff: int
    production_plane_wave_cutoff: int
    finite_difference_points: tuple[int, ...]
    parent_sample_reduced_momenta: tuple[float, ...]
    compared_band_count: int
    selected_band_index: int
    reciprocal_training_mesh_size: int
    evaluation_reduced_momenta: tuple[float, ...]
    hopping_ranges: tuple[int, ...]
    fitting_weights: tuple[float, ...]
    tolerances: SingleBandHoppingReductionTolerances1D
    model_id: ModelId = field(default=ModelId.mathieu1d, init=False)
    schema_id: ModelSystemStudySchemaId = field(
        default=ModelSystemStudySchemaId.mathieu1d_v1,
        init=False,
    )

    def __post_init__(self) -> None:
        """Reject ambiguous model, inventory, sample-role, and tolerance controls."""
        if type(self.parent_model) is not Periodic1DFourierHamiltonianToyModel:
            raise TypeError("parent_model must be Periodic1DFourierHamiltonianToyModel")
        _increasing_integers(
            "plane_wave_cutoffs", self.plane_wave_cutoffs, allow_zero=False
        )
        _increasing_integers(
            "finite_difference_points",
            self.finite_difference_points,
            allow_zero=False,
        )
        _increasing_integers("hopping_ranges", self.hopping_ranges, allow_zero=True)
        for name, value in (
            ("plane_wave_reference_cutoff", self.plane_wave_reference_cutoff),
            ("production_plane_wave_cutoff", self.production_plane_wave_cutoff),
            ("compared_band_count", self.compared_band_count),
            ("reciprocal_training_mesh_size", self.reciprocal_training_mesh_size),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        if type(self.selected_band_index) is not int:
            raise TypeError("selected_band_index must be a built-in int")
        if self.selected_band_index < 0:
            raise ValueError("selected_band_index must be nonnegative")
        if self.plane_wave_reference_cutoff <= self.plane_wave_cutoffs[-1]:
            raise ValueError(
                "plane_wave_reference_cutoff must exceed every sweep cutoff"
            )
        if self.production_plane_wave_cutoff not in self.plane_wave_cutoffs:
            raise ValueError(
                "production_plane_wave_cutoff must be one declared sweep cutoff"
            )
        smallest_basis = 2 * self.plane_wave_cutoffs[0] + 1
        if self.compared_band_count > smallest_basis:
            raise ValueError("compared bands must fit every plane-wave basis")
        if self.selected_band_index + 2 > (2 * self.production_plane_wave_cutoff + 1):
            raise ValueError(
                "production basis must contain the selected band and an upper neighbor"
            )
        if any(
            points <= self.compared_band_count
            for points in self.finite_difference_points
        ):
            raise ValueError(
                "finite-difference grids must exceed the compared band count"
            )
        if (
            self.reciprocal_training_mesh_size < 2
            or self.reciprocal_training_mesh_size % 2 != 0
        ):
            raise ValueError(
                "reciprocal_training_mesh_size must be an even integer of at least two"
            )
        if self.hopping_ranges[-1] >= self.reciprocal_training_mesh_size // 2:
            raise ValueError(
                "hopping_ranges must be smaller than half the training-mesh extent"
            )
        self._validate_reduced_coordinates(
            "parent_sample_reduced_momenta",
            self.parent_sample_reduced_momenta,
            upper_closed=True,
        )
        self._validate_reduced_coordinates(
            "evaluation_reduced_momenta",
            self.evaluation_reduced_momenta,
            upper_closed=False,
        )
        if not isinstance(self.fitting_weights, tuple):
            raise TypeError("fitting_weights must be a tuple")
        if len(self.fitting_weights) != self.reciprocal_training_mesh_size:
            raise ValueError("one fitting weight is required per training sample")
        if any(type(value) is not float for value in self.fitting_weights):
            raise TypeError("fitting_weights must contain built-in floats")
        if any(
            not np.isfinite(value) or value <= 0.0 for value in self.fitting_weights
        ):
            raise ValueError("fitting_weights must contain finite positive values")
        if type(self.tolerances) is not SingleBandHoppingReductionTolerances1D:
            raise TypeError("tolerances must be SingleBandHoppingReductionTolerances1D")
        reciprocal_unit = self.parent_model.reciprocal_vector.unit
        if not ModelSystemUnitConverter.compatible(
            self.tolerances.coordinate_absolute.unit, reciprocal_unit
        ):
            raise ValueError(
                "coordinate tolerance must have reciprocal-coordinate dimensions"
            )
        self._validate_disjoint_sample_roles()

    def study_identity(self) -> ModelSystemStudyIdentity:
        """Return the fixed model and schema identity."""
        return ModelSystemStudyIdentity(self.model_id, self.schema_id)

    @staticmethod
    def _validate_reduced_coordinates(
        name: str,
        values: tuple[float, ...],
        *,
        upper_closed: bool,
    ) -> None:
        """Validate one ordered finite tuple in the first reciprocal period."""
        if not isinstance(values, tuple) or not values:
            raise TypeError(f"{name} must be a nonempty tuple")
        if any(type(value) is not float for value in values):
            raise TypeError(f"{name} must contain built-in floats")
        if any(not np.isfinite(value) for value in values):
            raise ValueError(f"{name} must contain finite values")
        outside = (
            any(value < -0.5 or value > 0.5 for value in values)
            if upper_closed
            else any(value < -0.5 or value >= 0.5 for value in values)
        )
        if outside:
            interval = "[-0.5, 0.5]" if upper_closed else "[-0.5, 0.5)"
            raise ValueError(f"{name} must lie in {interval}")
        if tuple(sorted(set(values))) != values:
            raise ValueError(f"{name} must be unique and strictly increasing")

    @property
    def training_reduced_momenta(self) -> tuple[float, ...]:
        """Return the complete centered half-open training coordinates."""
        size = self.reciprocal_training_mesh_size
        return tuple(float(-0.5 + float(index) / float(size)) for index in range(size))

    @property
    def evaluation_coordinates(self) -> VectorQuantity:
        """Return physical evaluation coordinates in the model reciprocal unit."""
        reciprocal = self.parent_model.reciprocal_vector
        return VectorQuantity(
            reciprocal.magnitude
            * np.asarray(self.evaluation_reduced_momenta, dtype=np.float64),
            reciprocal.unit,
        )

    def _validate_disjoint_sample_roles(self) -> None:
        """Require evaluation coordinates to be separated from the training mesh."""
        training = np.asarray(self.training_reduced_momenta, dtype=np.float64)
        evaluation = np.asarray(self.evaluation_reduced_momenta, dtype=np.float64)
        reciprocal = self.parent_model.reciprocal_vector
        tolerance = ModelSystemUnitConverter.convert_scalar(
            self.tolerances.coordinate_absolute, reciprocal.unit
        ).magnitude
        reduced_tolerance = tolerance / reciprocal.magnitude
        minimum_defect = float(np.min(np.abs(training[:, None] - evaluation[None, :])))
        if minimum_defect <= reduced_tolerance:
            raise ValueError("training and evaluation coordinates must be disjoint")


@dataclass(frozen=True, slots=True)
class Mathieu1dPlaneWaveRefinementObservation:
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
class Mathieu1dFiniteDifferenceRefinementObservation:
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
class Mathieu1dStudyResult:
    """Correlate parent refinement, sampled gaps, and reusable reduction output."""

    definition: Mathieu1dStudyDefinition
    parent_reference: BandSpectrumSamples1D
    plane_wave_refinement: tuple[Mathieu1dPlaneWaveRefinementObservation, ...]
    finite_difference_refinement: tuple[
        Mathieu1dFiniteDifferenceRefinementObservation, ...
    ]
    training_gap: BandGapResult1D
    evaluation_gap: BandGapResult1D
    reduction: SingleBandHoppingReductionResult1D

    def __post_init__(self) -> None:
        """Validate exact experiment inventories and cross-layer correlations."""
        if type(self.definition) is not Mathieu1dStudyDefinition:
            raise TypeError("definition must be Mathieu1dStudyDefinition")
        if type(self.parent_reference) is not BandSpectrumSamples1D:
            raise TypeError("parent_reference must be BandSpectrumSamples1D")
        if not isinstance(self.plane_wave_refinement, tuple) or any(
            type(item) is not Mathieu1dPlaneWaveRefinementObservation
            for item in self.plane_wave_refinement
        ):
            raise TypeError("plane_wave_refinement must be a typed tuple")
        if not isinstance(self.finite_difference_refinement, tuple) or any(
            type(item) is not Mathieu1dFiniteDifferenceRefinementObservation
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
    "Mathieu1dFiniteDifferenceRefinementObservation",
    "Mathieu1dPlaneWaveRefinementObservation",
    "Mathieu1dStudyDefinition",
    "Mathieu1dStudyResult",
]
