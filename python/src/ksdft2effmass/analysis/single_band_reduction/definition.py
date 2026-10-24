"""Requests and tolerances for reusable one-dimensional single-band reduction."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.physkit.units import ModelSystemUnitConverter

from ksdft2effmass.analysis.periodic_bands import BandSpectrumSamples1D
from ksdft2effmass.linalg import (
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solidstate import CenteredUniformReciprocalMesh1D


@dataclass(frozen=True, slots=True)
class SingleBandHoppingReductionTolerances1D:
    """Declare numerical-consistency tolerances with explicit units.

    Parameters
    ----------
    coordinate_absolute
        Maximum accepted training-mesh coordinate defect. Its unit must be compatible
        with the request's reciprocal period.
    reconstruction_absolute, hermiticity_absolute, imaginary_absolute
        Nonnegative tolerances with the target band-energy dimension.
    parseval_absolute
        Nonnegative tolerance with squared band-energy dimensions.

    Notes
    -----
    These values control numerical consistency only. They are not scientific
    acceptance thresholds or uncertainty estimates.
    """

    coordinate_absolute: ScalarQuantity
    reconstruction_absolute: ScalarQuantity
    hermiticity_absolute: ScalarQuantity
    parseval_absolute: ScalarQuantity
    imaginary_absolute: ScalarQuantity

    def __post_init__(self) -> None:
        """Reject missing, nonfinite, or negative quantity tolerances."""
        for name, value in (
            ("coordinate_absolute", self.coordinate_absolute),
            ("reconstruction_absolute", self.reconstruction_absolute),
            ("hermiticity_absolute", self.hermiticity_absolute),
            ("parseval_absolute", self.parseval_absolute),
            ("imaginary_absolute", self.imaginary_absolute),
        ):
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if not np.isfinite(value.magnitude) or value.magnitude < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True, slots=True, eq=False)
class SingleBandHoppingReductionRequest1D:
    """Request complete Fourier reduction and finite-range route comparison.

    Parameters
    ----------
    training_target
        Exactly one real ordered band sampled on every point of ``transform_mesh``.
        These values define the complete finite Fourier representation and direct fits.
    evaluation_target
        Exactly one band on caller-selected evaluation coordinates. These values are
        evaluation-only and cannot change the transform or fitted models.
    transform_mesh
        Complete even centered half-open reciprocal mesh for the finite transform.
    hopping_ranges
        Unique increasing nonnegative symmetric cell ranges. Every range is strictly
        below half the transform-mesh extent.
    fitting_weights
        One positive unitless weight per training sample.
    tolerances
        Explicit numerical-consistency tolerances.

    Notes
    -----
    The request contains no parent-model identity, experiment identity, scientific
    acceptance policy, or evidence-retention policy. Training and evaluation
    coordinates may coincide when a caller explicitly requests in-sample evaluation;
    an experiment that requires disjoint roles must enforce that stronger contract.
    """

    training_target: BandSpectrumSamples1D
    evaluation_target: BandSpectrumSamples1D
    transform_mesh: CenteredUniformReciprocalMesh1D
    hopping_ranges: tuple[int, ...]
    fitting_weights: VectorQuantity
    tolerances: SingleBandHoppingReductionTolerances1D

    def __post_init__(self) -> None:
        """Validate band rank, meshes, ranges, units, weights, and tolerances."""
        if type(self.training_target) is not BandSpectrumSamples1D:
            raise TypeError("training_target must be BandSpectrumSamples1D")
        if type(self.evaluation_target) is not BandSpectrumSamples1D:
            raise TypeError("evaluation_target must be BandSpectrumSamples1D")
        if self.training_target.band_count != 1:
            raise ValueError("training_target must contain exactly one band")
        if self.evaluation_target.band_count != 1:
            raise ValueError("evaluation_target must contain exactly one band")
        if type(self.transform_mesh) is not CenteredUniformReciprocalMesh1D:
            raise TypeError("transform_mesh must be CenteredUniformReciprocalMesh1D")
        if not isinstance(self.hopping_ranges, tuple) or not self.hopping_ranges:
            raise TypeError("hopping_ranges must be a nonempty tuple")
        if any(type(value) is not int for value in self.hopping_ranges):
            raise TypeError("hopping_ranges must contain built-in integers")
        if tuple(sorted(set(self.hopping_ranges))) != self.hopping_ranges:
            raise ValueError("hopping_ranges must be unique and strictly increasing")
        if self.hopping_ranges[0] < 0:
            raise ValueError("hopping_ranges must be nonnegative")
        if self.hopping_ranges[-1] >= self.transform_mesh.point_count // 2:
            raise ValueError(
                "hopping_ranges must be smaller than half the transform-mesh extent"
            )
        if type(self.fitting_weights) is not VectorQuantity:
            raise TypeError("fitting_weights must be VectorQuantity")
        if not isinstance(self.fitting_weights.unit, Unitless):
            raise ValueError("fitting_weights must be unitless")
        if self.fitting_weights.magnitude.shape != (self.training_target.sample_count,):
            raise ValueError("one fitting weight is required per training sample")
        if np.any(self.fitting_weights.magnitude <= 0.0):
            raise ValueError("fitting_weights must be positive")
        if type(self.tolerances) is not SingleBandHoppingReductionTolerances1D:
            raise TypeError("tolerances must be SingleBandHoppingReductionTolerances1D")

        converter = ModelSystemUnitConverter
        training_period = self.training_target.reciprocal_period
        evaluation_period = converter.convert_scalar(
            self.evaluation_target.reciprocal_period, training_period.unit
        )
        mesh_period = converter.convert_scalar(
            self.transform_mesh.reciprocal_period, training_period.unit
        )
        if evaluation_period.magnitude != training_period.magnitude:
            raise ValueError("training and evaluation reciprocal periods must agree")
        if mesh_period.magnitude != training_period.magnitude:
            raise ValueError("training target and transform mesh periods must agree")
        if self.training_target.sample_count != self.transform_mesh.point_count:
            raise ValueError("training target must contain every transform-mesh point")

        coordinate_tolerance = converter.convert_scalar(
            self.tolerances.coordinate_absolute, training_period.unit
        )
        mesh_coordinates = converter.convert_vector(
            self.transform_mesh.coordinates, training_period.unit
        )
        coordinate_defect = float(
            np.max(
                np.abs(
                    self.training_target.coordinates.magnitude
                    - mesh_coordinates.magnitude
                )
            )
        )
        if coordinate_defect > coordinate_tolerance.magnitude:
            raise ValueError("training coordinates do not match transform_mesh")

        training_energy_unit = self.training_target.eigenvalues.unit
        if not converter.compatible(
            self.evaluation_target.eigenvalues.unit, training_energy_unit
        ):
            raise ValueError("training and evaluation energy units must be compatible")
        for name, value in (
            ("reconstruction_absolute", self.tolerances.reconstruction_absolute),
            ("hermiticity_absolute", self.tolerances.hermiticity_absolute),
            ("imaginary_absolute", self.tolerances.imaginary_absolute),
        ):
            if not converter.compatible(value.unit, training_energy_unit):
                raise ValueError(f"{name} must have band-energy dimensions")
        squared_energy_unit = (
            Unitless()
            if isinstance(training_energy_unit, Unitless)
            else PhysicalUnit(f"({training_energy_unit.expression}) ** 2")
        )
        if not converter.compatible(
            self.tolerances.parseval_absolute.unit, squared_energy_unit
        ):
            raise ValueError(
                "parseval_absolute must have squared band-energy dimensions"
            )


__all__ = [
    "SingleBandHoppingReductionRequest1D",
    "SingleBandHoppingReductionTolerances1D",
]
