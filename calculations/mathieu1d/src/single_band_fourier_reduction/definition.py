"""Scientific controls for the periodic one-dimensional single-band experiment."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from ksdft2effmass.analysis.single_band_reduction import (
    SingleBandHoppingReductionTolerances1D,
)
from ksdft2effmass.linalg import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    VectorQuantity,
)
from ksdft2effmass.periodic1d.model import Periodic1DFourierHamiltonianToyModel

EXPERIMENT_FAMILY_ID = (
    "ksdft2effmass.campaign.periodic-reduction.periodic1d.single-band-fourier-reduction"
)
EXPERIMENT_VERSION_ID = f"{EXPERIMENT_FAMILY_ID}.v1"
INPUT_SCHEMA_ID = f"{EXPERIMENT_VERSION_ID}.input.v1"
RESULT_SCHEMA_ID = f"{EXPERIMENT_VERSION_ID}.result.v1"
VERIFICATION_SCHEMA_ID = f"{EXPERIMENT_VERSION_ID}.verification.v1"
ENERGY_REFERENCE_ID = "parent-model-fixed-zero-no-post-fit-shift.v1"
FOURIER_CONVENTION_ID = "forward-negative-exponent-inverse-positive-exponent.v1"
FOURIER_NORMALIZATION_ID = "forward-one-over-n-inverse-unit.v1"
OBJECTIVE_CONSTRUCTION_ROLE_ID = "complete-centered-training-mesh.v1"
OBJECTIVE_EVALUATION_ROLE_ID = "disjoint-staggered-evaluation-mesh.v1"


@dataclass(frozen=True, slots=True)
class SingleBandFourierReductionExperimentIdentity:
    """Immutable identity and convention contract for retained version one."""

    family_id: str = EXPERIMENT_FAMILY_ID
    version_id: str = EXPERIMENT_VERSION_ID
    input_schema_id: str = INPUT_SCHEMA_ID
    result_schema_id: str = RESULT_SCHEMA_ID
    verification_schema_id: str = VERIFICATION_SCHEMA_ID
    energy_reference_id: str = ENERGY_REFERENCE_ID
    fourier_convention_id: str = FOURIER_CONVENTION_ID
    fourier_normalization_id: str = FOURIER_NORMALIZATION_ID
    objective_construction_role_id: str = OBJECTIVE_CONSTRUCTION_ROLE_ID
    objective_evaluation_role_id: str = OBJECTIVE_EVALUATION_ROLE_ID

    def __post_init__(self) -> None:
        """Reject mutation-by-construction of the frozen version contract."""
        expected = (
            EXPERIMENT_FAMILY_ID,
            EXPERIMENT_VERSION_ID,
            INPUT_SCHEMA_ID,
            RESULT_SCHEMA_ID,
            VERIFICATION_SCHEMA_ID,
            ENERGY_REFERENCE_ID,
            FOURIER_CONVENTION_ID,
            FOURIER_NORMALIZATION_ID,
            OBJECTIVE_CONSTRUCTION_ROLE_ID,
            OBJECTIVE_EVALUATION_ROLE_ID,
        )
        actual = (
            self.family_id,
            self.version_id,
            self.input_schema_id,
            self.result_schema_id,
            self.verification_schema_id,
            self.energy_reference_id,
            self.fourier_convention_id,
            self.fourier_normalization_id,
            self.objective_construction_role_id,
            self.objective_evaluation_role_id,
        )
        if actual != expected:
            raise ValueError("version-one identity and conventions are immutable")


EXPERIMENT_IDENTITY = SingleBandFourierReductionExperimentIdentity()


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
class SingleBandFourierReductionExperimentDefinition:
    """Freeze one parent-refinement and single-band reduction experiment.

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
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.tolerances.coordinate_absolute.unit, reciprocal_unit
        ):
            raise ValueError(
                "coordinate tolerance must have reciprocal-coordinate dimensions"
            )
        self._validate_disjoint_sample_roles()

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
        tolerance = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            self.tolerances.coordinate_absolute, reciprocal.unit
        ).magnitude
        reduced_tolerance = tolerance / reciprocal.magnitude
        minimum_defect = float(np.min(np.abs(training[:, None] - evaluation[None, :])))
        if minimum_defect <= reduced_tolerance:
            raise ValueError("training and evaluation coordinates must be disjoint")


__all__ = [
    "ENERGY_REFERENCE_ID",
    "EXPERIMENT_FAMILY_ID",
    "EXPERIMENT_IDENTITY",
    "EXPERIMENT_VERSION_ID",
    "FOURIER_CONVENTION_ID",
    "FOURIER_NORMALIZATION_ID",
    "INPUT_SCHEMA_ID",
    "OBJECTIVE_CONSTRUCTION_ROLE_ID",
    "OBJECTIVE_EVALUATION_ROLE_ID",
    "RESULT_SCHEMA_ID",
    "SingleBandFourierReductionExperimentDefinition",
    "SingleBandFourierReductionExperimentIdentity",
    "VERIFICATION_SCHEMA_ID",
]
