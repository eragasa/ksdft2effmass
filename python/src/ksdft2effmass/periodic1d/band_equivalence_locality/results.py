"""Immutable scientific results for periodic-1D band-equivalence locality."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .request import Periodic1DBandEquivalenceLocalityRequest


def _nonnegative(value: float, name: str) -> None:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DBandEquivalenceHoppingPower:
    """Retain one normalized finite-cyclic hopping-block power."""

    displacement: int
    normalized_squared_frobenius_norm: float

    def __post_init__(self) -> None:
        if type(self.displacement) is not int:
            raise TypeError("displacement must be a built-in integer")
        _nonnegative(
            self.normalized_squared_frobenius_norm,
            "normalized_squared_frobenius_norm",
        )


@dataclass(frozen=True, slots=True)
class Periodic1DBandEquivalenceRangeAnalysis:
    """Retain deliberate ordinary-lattice truncation consequences."""

    maximum_range: int
    ordinary_omitted_block_l2_norm: float
    truncation_hamiltonian_maximum_error: float
    total_hamiltonian_maximum_error: float
    truncation_spectral_maximum_error: float
    total_spectral_maximum_error: float

    def __post_init__(self) -> None:
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in integer")
        if self.maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        for value, name in (
            (
                self.ordinary_omitted_block_l2_norm,
                "ordinary_omitted_block_l2_norm",
            ),
            (
                self.truncation_hamiltonian_maximum_error,
                "truncation_hamiltonian_maximum_error",
            ),
            (
                self.total_hamiltonian_maximum_error,
                "total_hamiltonian_maximum_error",
            ),
            (
                self.truncation_spectral_maximum_error,
                "truncation_spectral_maximum_error",
            ),
            (self.total_spectral_maximum_error, "total_spectral_maximum_error"),
        ):
            _nonnegative(value, name)


@dataclass(frozen=True, slots=True)
class Periodic1DBandEquivalencePointAnalysis:
    """Retain separated band, alignment, Fourier, and truncation channels."""

    amplitude: float
    maximum_band_defect: float
    discrete_maximum_correlation: float
    analytic_maximum_correlation: float
    correlation_quadrature_defect: float
    global_alignment_angle: float
    optimal_splitting_scale: float
    irreducible_operator_squared_loss: float
    minimum_operator_threshold: float
    exact_spectrum_joint_operator_threshold: float
    cyclic_nyquist_power: float
    reconstruction_maximum_frobenius_error: float
    interpolation_hamiltonian_maximum_error: float
    interpolation_spectral_maximum_error: float
    hopping_powers: tuple[Periodic1DBandEquivalenceHoppingPower, ...]
    ranges: tuple[Periodic1DBandEquivalenceRangeAnalysis, ...]

    def __post_init__(self) -> None:
        if type(self.amplitude) is not float or not math.isfinite(self.amplitude):
            raise TypeError("amplitude must be a finite built-in float")
        for value, name in (
            (self.maximum_band_defect, "maximum_band_defect"),
            (self.correlation_quadrature_defect, "correlation_quadrature_defect"),
            (
                self.irreducible_operator_squared_loss,
                "irreducible_operator_squared_loss",
            ),
            (self.minimum_operator_threshold, "minimum_operator_threshold"),
            (
                self.exact_spectrum_joint_operator_threshold,
                "exact_spectrum_joint_operator_threshold",
            ),
            (self.cyclic_nyquist_power, "cyclic_nyquist_power"),
            (
                self.reconstruction_maximum_frobenius_error,
                "reconstruction_maximum_frobenius_error",
            ),
            (
                self.interpolation_hamiltonian_maximum_error,
                "interpolation_hamiltonian_maximum_error",
            ),
            (
                self.interpolation_spectral_maximum_error,
                "interpolation_spectral_maximum_error",
            ),
        ):
            _nonnegative(value, name)
        for value, name in (
            (self.discrete_maximum_correlation, "discrete_maximum_correlation"),
            (self.analytic_maximum_correlation, "analytic_maximum_correlation"),
            (self.global_alignment_angle, "global_alignment_angle"),
            (self.optimal_splitting_scale, "optimal_splitting_scale"),
        ):
            if type(value) is not float or not math.isfinite(value):
                raise TypeError(f"{name} must be a finite built-in float")
        if not -1.0 <= self.discrete_maximum_correlation <= 1.0:
            raise ValueError("discrete_maximum_correlation must lie in [-1, 1]")
        if not -1.0 <= self.analytic_maximum_correlation <= 1.0:
            raise ValueError("analytic_maximum_correlation must lie in [-1, 1]")
        if not 0.0 <= self.optimal_splitting_scale <= 1.0:
            raise ValueError("optimal_splitting_scale must lie in [0, 1]")
        if type(self.hopping_powers) is not tuple or not self.hopping_powers:
            raise TypeError("hopping_powers must be a nonempty tuple")
        if any(
            type(item) is not Periodic1DBandEquivalenceHoppingPower
            for item in self.hopping_powers
        ):
            raise TypeError("hopping_powers must contain typed values")
        displacements = tuple(item.displacement for item in self.hopping_powers)
        if displacements != tuple(sorted(set(displacements))) or 0 not in displacements:
            raise ValueError("hopping powers must be ordered, unique, and include zero")
        if type(self.ranges) is not tuple or any(
            type(item) is not Periodic1DBandEquivalenceRangeAnalysis
            for item in self.ranges
        ):
            raise TypeError("ranges must contain typed values")
        if tuple(item.maximum_range for item in self.ranges) != tuple(
            sorted(set(item.maximum_range for item in self.ranges))
        ):
            raise ValueError("ranges must be ordered and unique")


@dataclass(frozen=True, slots=True)
class Periodic1DBandEquivalenceLocalityAnalysis:
    """Represent one complete flat-parent finite analysis."""

    request: Periodic1DBandEquivalenceLocalityRequest
    points: tuple[Periodic1DBandEquivalencePointAnalysis, ...]

    def __post_init__(self) -> None:
        if type(self.request) is not Periodic1DBandEquivalenceLocalityRequest:
            raise TypeError("request must be Periodic1DBandEquivalenceLocalityRequest")
        if type(self.points) is not tuple or any(
            type(point) is not Periodic1DBandEquivalencePointAnalysis
            for point in self.points
        ):
            raise TypeError("points must contain typed point analyses")
        if tuple(point.amplitude for point in self.points) != self.request.amplitudes:
            raise ValueError("points must match the requested amplitudes")
        expected_ranges = self.request.maximum_ranges
        if any(
            tuple(item.maximum_range for item in point.ranges) != expected_ranges
            for point in self.points
        ):
            raise ValueError("every point must contain the requested range inventory")


__all__ = [
    "Periodic1DBandEquivalenceHoppingPower",
    "Periodic1DBandEquivalenceLocalityAnalysis",
    "Periodic1DBandEquivalencePointAnalysis",
    "Periodic1DBandEquivalenceRangeAnalysis",
]
