"""Immutable results for the maintained smooth continuum experiment."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from projectkoios.optimization.selection.harmonic import PeriodicHarmonicMaximum

from ._validation import _finite_float
from .definition import (
    SmoothBlochContinuumConvergenceDefinition,
    SmoothBlochContinuumDefinition,
)


@dataclass(frozen=True, slots=True)
class SmoothBlochContinuumHoppingBlockResult:
    """Retain one normalized Fourier-block power.

    Parameters
    ----------
    displacement
        Centered integer cell displacement.
    normalized_squared_frobenius_norm
        ``||B_R||_F^2 / (2 E_ref^2)`` for the attacked traceless field.
    """

    displacement: int
    normalized_squared_frobenius_norm: float

    def __post_init__(self) -> None:
        """Validate one finite nonnegative normalized block power."""
        if type(self.displacement) is not int:
            raise TypeError("displacement must be a built-in int")
        _finite_float(
            "normalized_squared_frobenius_norm",
            self.normalized_squared_frobenius_norm,
        )
        if self.normalized_squared_frobenius_norm < 0.0:
            raise ValueError("normalized_squared_frobenius_norm must be nonnegative")


@dataclass(frozen=True, slots=True)
class SmoothBlochContinuumPointResult:
    """Retain both Bloch-only and representation-aware channels at one amplitude.

    Parameters
    ----------
    amplitude
        Maximum sinusoidal basis-rotation amplitude in radians.
    maximum_band_defect
        Maximum normalized ordered-eigenvalue difference between reference and attacked
        matrices on the construction mesh.
    harmonic_maximum
        Owner-selected exact continuous maximum of the discrete correlation harmonic.
    discrete_maximum_correlation
        ``mu_N,max`` reconstructed from the finite reciprocal mesh.
    analytic_maximum_correlation
        Continuous comparator ``J_0(2a)``.
    correlation_quadrature_defect
        Absolute difference between discrete and analytic correlations.
    irreducible_operator_squared_loss
        Discrete continuously aligned minimum squared operator loss.
    minimum_operator_threshold
        Square root of ``irreducible_operator_squared_loss``.
    exact_spectrum_joint_operator_threshold
        Minimum operator threshold while exact spectral agreement fixes ``lambda=1``.
    analytic_minimum_operator_threshold
        Continuous Bessel comparator for the minimum operator threshold.
    analytic_exact_spectrum_joint_operator_threshold
        Continuous Bessel comparator under exact spectral agreement.
    nonzero_hopping_weight
        Sum of normalized Fourier-block powers over nonzero displacements.
    onsite_mismatch_squared
        Normalized mismatch caused by fixing the candidate splitting scale to one.
    three_way_identity_defect
        Maximum disagreement among irreducible loss, threshold squared, and nonzero
        hopping weight.
    parseval_defect
        Difference between reciprocal-sample and complete Fourier-block powers.
    hopping_blocks
        Complete centered finite-mesh Fourier-block power inventory.
    """

    amplitude: float
    maximum_band_defect: float
    harmonic_maximum: PeriodicHarmonicMaximum
    discrete_maximum_correlation: float
    analytic_maximum_correlation: float
    correlation_quadrature_defect: float
    irreducible_operator_squared_loss: float
    minimum_operator_threshold: float
    exact_spectrum_joint_operator_threshold: float
    analytic_minimum_operator_threshold: float
    analytic_exact_spectrum_joint_operator_threshold: float
    nonzero_hopping_weight: float
    onsite_mismatch_squared: float
    three_way_identity_defect: float
    parseval_defect: float
    hopping_blocks: tuple[SmoothBlochContinuumHoppingBlockResult, ...]

    def __post_init__(self) -> None:
        """Validate finite channels and a complete ordered hopping inventory."""
        for name, value in (
            ("amplitude", self.amplitude),
            ("maximum_band_defect", self.maximum_band_defect),
            ("discrete_maximum_correlation", self.discrete_maximum_correlation),
            ("analytic_maximum_correlation", self.analytic_maximum_correlation),
            ("correlation_quadrature_defect", self.correlation_quadrature_defect),
            (
                "irreducible_operator_squared_loss",
                self.irreducible_operator_squared_loss,
            ),
            ("minimum_operator_threshold", self.minimum_operator_threshold),
            (
                "exact_spectrum_joint_operator_threshold",
                self.exact_spectrum_joint_operator_threshold,
            ),
            (
                "analytic_minimum_operator_threshold",
                self.analytic_minimum_operator_threshold,
            ),
            (
                "analytic_exact_spectrum_joint_operator_threshold",
                self.analytic_exact_spectrum_joint_operator_threshold,
            ),
            ("nonzero_hopping_weight", self.nonzero_hopping_weight),
            ("onsite_mismatch_squared", self.onsite_mismatch_squared),
            ("three_way_identity_defect", self.three_way_identity_defect),
            ("parseval_defect", self.parseval_defect),
        ):
            _finite_float(name, value)
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if type(self.harmonic_maximum) is not PeriodicHarmonicMaximum:
            raise TypeError("harmonic_maximum must be PeriodicHarmonicMaximum")
        for name, value in (
            ("discrete_maximum_correlation", self.discrete_maximum_correlation),
            ("analytic_maximum_correlation", self.analytic_maximum_correlation),
        ):
            if value > 1.0:
                raise ValueError(f"{name} must not exceed one")
        if type(self.hopping_blocks) is not tuple or not self.hopping_blocks:
            raise TypeError("hopping_blocks must be a nonempty tuple")
        if any(
            type(item) is not SmoothBlochContinuumHoppingBlockResult
            for item in self.hopping_blocks
        ):
            raise TypeError("hopping_blocks must contain typed block results")
        displacements = tuple(item.displacement for item in self.hopping_blocks)
        if tuple(sorted(set(displacements))) != displacements:
            raise ValueError(
                "hopping block displacements must be unique and increasing"
            )
        if 0 not in displacements:
            raise ValueError("hopping_blocks must contain the onsite block")


@dataclass(frozen=True, slots=True)
class SmoothBlochContinuumResult:
    """Retain the complete side-by-side band and operator continuum."""

    definition: SmoothBlochContinuumDefinition
    points: tuple[SmoothBlochContinuumPointResult, ...]

    def __post_init__(self) -> None:
        """Require one result per declared amplitude and validate exact correlations."""
        if type(self.definition) is not SmoothBlochContinuumDefinition:
            raise TypeError("definition must be SmoothBlochContinuumDefinition")
        if type(self.points) is not tuple or any(
            type(point) is not SmoothBlochContinuumPointResult for point in self.points
        ):
            raise TypeError("points must be a typed tuple")
        if (
            tuple(point.amplitude for point in self.points)
            != self.definition.amplitudes
        ):
            raise ValueError("points must match the declared amplitudes")
        tolerance = self.definition.verification_absolute_tolerance
        for point in self.points:
            if (
                abs(
                    point.harmonic_maximum.maximum_value
                    - point.discrete_maximum_correlation
                )
                > tolerance
            ):
                raise ValueError("harmonic maximum must equal discrete correlation")
            expected_quadrature = abs(
                point.discrete_maximum_correlation - point.analytic_maximum_correlation
            )
            if (
                abs(point.correlation_quadrature_defect - expected_quadrature)
                > tolerance
            ):
                raise ValueError("correlation_quadrature_defect is inconsistent")
            expected_nonzero = sum(
                item.normalized_squared_frobenius_norm
                for item in point.hopping_blocks
                if item.displacement != 0
            )
            if abs(point.nonzero_hopping_weight - expected_nonzero) > tolerance:
                raise ValueError("nonzero_hopping_weight is inconsistent")


class SmoothBlochContinuumConvergenceDisposition(StrEnum):
    """Classify only demonstrated mesh stability, not scientific validity."""

    CONVERGED = "converged"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True, slots=True)
class SmoothBlochContinuumRefinementResult:
    """Retain conservative maximum changes across one nested mesh refinement."""

    coarse_mesh_size: int
    fine_mesh_size: int
    maximum_correlation_change: float
    maximum_threshold_change: float
    maximum_hopping_weight_change: float
    maximum_hopping_block_power_change: float
    maximum_angle_change: float
    maximizing_angle_dispositions_stable: bool
    maximum_fine_quadrature_defect: float
    maximum_band_defect: float
    maximum_identity_defect: float
    maximum_parseval_defect: float
    within_tolerances: bool

    def __post_init__(self) -> None:
        """Validate nested mesh identities, finite metrics, and Boolean dispositions."""
        if (
            type(self.coarse_mesh_size) is not int
            or type(self.fine_mesh_size) is not int
        ):
            raise TypeError("mesh sizes must be built-in integers")
        if self.fine_mesh_size != 2 * self.coarse_mesh_size:
            raise ValueError("refinement mesh sizes must form one doubling pair")
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
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if type(self.maximizing_angle_dispositions_stable) is not bool:
            raise TypeError(
                "maximizing_angle_dispositions_stable must be a built-in bool"
            )
        if type(self.within_tolerances) is not bool:
            raise TypeError("within_tolerances must be a built-in bool")


@dataclass(frozen=True, slots=True)
class SmoothBlochContinuumConvergenceResult:
    """Retain every mesh result and a non-overstated convergence disposition."""

    definition: SmoothBlochContinuumConvergenceDefinition
    mesh_results: tuple[SmoothBlochContinuumResult, ...]
    refinements: tuple[SmoothBlochContinuumRefinementResult, ...]
    disposition: SmoothBlochContinuumConvergenceDisposition

    def __post_init__(self) -> None:
        """Correlate mesh identities and derive the final stability disposition."""
        if type(self.definition) is not SmoothBlochContinuumConvergenceDefinition:
            raise TypeError(
                "definition must be SmoothBlochContinuumConvergenceDefinition"
            )
        if type(self.mesh_results) is not tuple or any(
            type(item) is not SmoothBlochContinuumResult for item in self.mesh_results
        ):
            raise TypeError("mesh_results must be a typed tuple")
        if (
            tuple(item.definition.reciprocal_mesh_size for item in self.mesh_results)
            != self.definition.reciprocal_mesh_sizes
        ):
            raise ValueError("mesh_results must match reciprocal_mesh_sizes")
        if type(self.refinements) is not tuple or any(
            type(item) is not SmoothBlochContinuumRefinementResult
            for item in self.refinements
        ):
            raise TypeError("refinements must be a typed tuple")
        expected_pairs = tuple(
            (coarse, fine)
            for coarse, fine in zip(
                self.definition.reciprocal_mesh_sizes[:-1],
                self.definition.reciprocal_mesh_sizes[1:],
                strict=True,
            )
        )
        actual_pairs = tuple(
            (item.coarse_mesh_size, item.fine_mesh_size) for item in self.refinements
        )
        if actual_pairs != expected_pairs:
            raise ValueError("refinements must match adjacent declared meshes")
        if type(self.disposition) is not SmoothBlochContinuumConvergenceDisposition:
            raise TypeError("disposition must be a convergence disposition")
        required = self.definition.required_stable_refinements
        expected_disposition = (
            SmoothBlochContinuumConvergenceDisposition.CONVERGED
            if all(item.within_tolerances for item in self.refinements[-required:])
            else SmoothBlochContinuumConvergenceDisposition.UNRESOLVED
        )
        if self.disposition is not expected_disposition:
            raise ValueError("disposition must match the required final refinements")


__all__ = [
    "SmoothBlochContinuumConvergenceDisposition",
    "SmoothBlochContinuumConvergenceResult",
    "SmoothBlochContinuumHoppingBlockResult",
    "SmoothBlochContinuumPointResult",
    "SmoothBlochContinuumRefinementResult",
    "SmoothBlochContinuumResult",
]
