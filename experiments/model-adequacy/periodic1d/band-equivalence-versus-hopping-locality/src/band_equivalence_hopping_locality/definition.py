"""Definitions for the maintained smooth continuum experiment."""

from __future__ import annotations

import math
from dataclasses import dataclass

EXPERIMENT_FAMILY_ID = (
    "ksdft2effmass.campaign.model-adequacy.periodic1d."
    "band-equivalence-versus-hopping-locality"
)
SMOOTH_CONTINUUM_METHOD_ID = "flat-rank-two-smooth-sinusoidal-gauge-continuum.v1"
CONTINUOUS_ALIGNMENT_METHOD_ID = "continuous-global-real-rotation-harmonic.v1"
FOURIER_CONVENTION_ID = "forward-negative-exponent-inverse-positive-exponent.v1"
FOURIER_NORMALIZATION_ID = "forward-one-over-n-inverse-unit.v1"
SMOOTH_CONTINUUM_INPUT_SCHEMA_ID = f"{EXPERIMENT_FAMILY_ID}.smooth-continuum.input.v1"
SMOOTH_CONTINUUM_RESULT_SCHEMA_ID = f"{EXPERIMENT_FAMILY_ID}.smooth-continuum.result.v1"
SMOOTH_CONTINUUM_VERIFICATION_SCHEMA_ID = (
    f"{EXPERIMENT_FAMILY_ID}.smooth-continuum.verification.v1"
)


def _finite_float(name: str, value: float) -> None:
    """Reject booleans, numeric strings, non-built-in scalars, and nonfinite values."""
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


@dataclass(frozen=True, slots=True)
class SmoothBlochContinuumDefinition:
    """Define the smooth band-equivalent continuum calculation.

    Parameters
    ----------
    reciprocal_mesh_size
        Even number of samples in the half-open reduced-wavenumber period.
    amplitudes
        Strictly increasing rotation amplitudes in radians. The first value must be
        zero and every value must lie in ``[0, pi/4]``.
    harmonic_absolute_degeneracy_tolerance
        Absolute unit-free cutoff delegated to the periodic-harmonic owner.
    harmonic_relative_degeneracy_tolerance
        Relative unit-free cutoff delegated to the periodic-harmonic owner.
    verification_absolute_tolerance
        Unit-free absolute tolerance for independent reconstruction defects.

    Notes
    -----
    The analytic parent is normalized by ``E_G``: its traceless block is
    ``diag(1, -1)``. Consequently, all retained losses and hopping powers are
    dimensionless. The definition describes one reciprocal-space calculation sampled
    at several gauge amplitudes, not several independently fitted parent models.
    """

    reciprocal_mesh_size: int
    amplitudes: tuple[float, ...]
    harmonic_absolute_degeneracy_tolerance: float
    harmonic_relative_degeneracy_tolerance: float
    verification_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Reject incomplete meshes, ambiguous amplitudes, and invalid tolerances."""
        if type(self.reciprocal_mesh_size) is not int:
            raise TypeError("reciprocal_mesh_size must be a built-in int")
        if self.reciprocal_mesh_size < 8:
            raise ValueError("reciprocal_mesh_size must be at least eight")
        if self.reciprocal_mesh_size % 2 != 0:
            raise ValueError("reciprocal_mesh_size must be even")
        if type(self.amplitudes) is not tuple or len(self.amplitudes) < 2:
            raise TypeError("amplitudes must contain at least two built-in floats")
        for index, amplitude in enumerate(self.amplitudes):
            _finite_float(f"amplitudes[{index}]", amplitude)
            if amplitude < 0.0 or amplitude > math.pi / 4.0:
                raise ValueError("amplitudes must lie in [0, pi/4]")
        if self.amplitudes[0] != 0.0:
            raise ValueError("amplitudes must begin at zero")
        if tuple(sorted(set(self.amplitudes))) != self.amplitudes:
            raise ValueError("amplitudes must be unique and strictly increasing")
        for name, value in (
            (
                "harmonic_absolute_degeneracy_tolerance",
                self.harmonic_absolute_degeneracy_tolerance,
            ),
            (
                "harmonic_relative_degeneracy_tolerance",
                self.harmonic_relative_degeneracy_tolerance,
            ),
            ("verification_absolute_tolerance", self.verification_absolute_tolerance),
        ):
            _finite_float(name, value)
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if (
            self.harmonic_absolute_degeneracy_tolerance == 0.0
            and self.harmonic_relative_degeneracy_tolerance == 0.0
        ):
            raise ValueError(
                "at least one harmonic degeneracy tolerance must be positive"
            )
        if self.verification_absolute_tolerance == 0.0:
            raise ValueError("verification_absolute_tolerance must be positive")


@dataclass(frozen=True, slots=True)
class SmoothBlochContinuumConvergenceThresholds:
    """Declare caller-selected unit-free mesh-convergence tolerances."""

    maximum_correlation_change: float
    maximum_threshold_change: float
    maximum_hopping_weight_change: float
    maximum_hopping_block_power_change: float
    maximum_angle_change: float
    maximum_fine_quadrature_defect: float
    maximum_band_defect: float
    maximum_identity_defect: float
    maximum_parseval_defect: float

    def __post_init__(self) -> None:
        """Require strictly positive finite tolerances without freezing their values."""
        for name, value in (
            ("maximum_correlation_change", self.maximum_correlation_change),
            ("maximum_threshold_change", self.maximum_threshold_change),
            ("maximum_hopping_weight_change", self.maximum_hopping_weight_change),
            (
                "maximum_hopping_block_power_change",
                self.maximum_hopping_block_power_change,
            ),
            ("maximum_angle_change", self.maximum_angle_change),
            (
                "maximum_fine_quadrature_defect",
                self.maximum_fine_quadrature_defect,
            ),
            ("maximum_band_defect", self.maximum_band_defect),
            ("maximum_identity_defect", self.maximum_identity_defect),
            ("maximum_parseval_defect", self.maximum_parseval_defect),
        ):
            _finite_float(name, value)
            if value <= 0.0:
                raise ValueError(f"{name} must be positive")


@dataclass(frozen=True, slots=True)
class SmoothBlochContinuumConvergenceDefinition:
    """Define nested meshes with caller controls and a conservative error margin.

    The verification absolute tolerance is added to every observed convergence metric
    before threshold comparison. Cases lacking that complete margin remain unresolved.
    """

    reciprocal_mesh_sizes: tuple[int, ...]
    amplitudes: tuple[float, ...]
    harmonic_absolute_degeneracy_tolerance: float
    harmonic_relative_degeneracy_tolerance: float
    verification_absolute_tolerance: float
    thresholds: SmoothBlochContinuumConvergenceThresholds
    required_stable_refinements: int

    def __post_init__(self) -> None:
        """Require nested doubling meshes and a valid single-mesh definition."""
        if (
            type(self.reciprocal_mesh_sizes) is not tuple
            or len(self.reciprocal_mesh_sizes) < 2
        ):
            raise TypeError("reciprocal_mesh_sizes must contain at least two integers")
        for index, size in enumerate(self.reciprocal_mesh_sizes):
            if type(size) is not int:
                raise TypeError(
                    f"reciprocal_mesh_sizes[{index}] must be a built-in int"
                )
        if any(
            fine != 2 * coarse
            for coarse, fine in zip(
                self.reciprocal_mesh_sizes[:-1],
                self.reciprocal_mesh_sizes[1:],
                strict=True,
            )
        ):
            raise ValueError("reciprocal_mesh_sizes must be nested doubling meshes")
        self.mesh_definition(self.reciprocal_mesh_sizes[0])
        if type(self.thresholds) is not SmoothBlochContinuumConvergenceThresholds:
            raise TypeError(
                "thresholds must be SmoothBlochContinuumConvergenceThresholds"
            )
        if type(self.required_stable_refinements) is not int:
            raise TypeError("required_stable_refinements must be a built-in int")
        if not 1 <= self.required_stable_refinements < len(self.reciprocal_mesh_sizes):
            raise ValueError("required_stable_refinements exceeds available mesh pairs")

    def mesh_definition(
        self, reciprocal_mesh_size: int
    ) -> SmoothBlochContinuumDefinition:
        """Return one immutable single-mesh definition from shared study controls."""
        return SmoothBlochContinuumDefinition(
            reciprocal_mesh_size=reciprocal_mesh_size,
            amplitudes=self.amplitudes,
            harmonic_absolute_degeneracy_tolerance=(
                self.harmonic_absolute_degeneracy_tolerance
            ),
            harmonic_relative_degeneracy_tolerance=(
                self.harmonic_relative_degeneracy_tolerance
            ),
            verification_absolute_tolerance=self.verification_absolute_tolerance,
        )


__all__ = [
    "CONTINUOUS_ALIGNMENT_METHOD_ID",
    "EXPERIMENT_FAMILY_ID",
    "FOURIER_CONVENTION_ID",
    "FOURIER_NORMALIZATION_ID",
    "SMOOTH_CONTINUUM_INPUT_SCHEMA_ID",
    "SMOOTH_CONTINUUM_METHOD_ID",
    "SMOOTH_CONTINUUM_RESULT_SCHEMA_ID",
    "SMOOTH_CONTINUUM_VERIFICATION_SCHEMA_ID",
    "SmoothBlochContinuumConvergenceDefinition",
    "SmoothBlochContinuumConvergenceThresholds",
    "SmoothBlochContinuumDefinition",
]
