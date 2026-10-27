"""Results for finite-range consequences of the non-flat realization."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .._validation import _finite_float
from .definition import SmoothFourStateTruncationDefinition


def _nonnegative(name: str, value: float) -> None:
    _finite_float(name, value)
    if value < 0.0:
        raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True)
class SmoothFourStateTruncationRangeResult:
    """Report errors caused by one conjugate-closed ordinary-lattice cutoff.

    Powers are squared Frobenius norms divided by the retained rank two and by
    ``E_ref**2``. Hamiltonian errors are Frobenius norms divided by
    ``sqrt(2) * E_ref``; band errors are normalized by ``E_ref``. ``total`` means
    interpolation plus deliberate truncation relative to the direct ordinary-lattice
    field; it does not assign an
    off-node spectrum to the removed cyclic Nyquist term.
    """

    maximum_range: int
    reference_ordinary_omitted_power: float
    comparison_ordinary_omitted_power: float
    reference_total_omitted_power: float
    comparison_total_omitted_power: float
    reference_maximum_truncation_hamiltonian_error: float
    reference_rms_truncation_hamiltonian_error: float
    reference_maximum_band_error: float
    reference_rms_band_error: float
    comparison_maximum_truncation_hamiltonian_error: float
    comparison_rms_truncation_hamiltonian_error: float
    comparison_maximum_truncation_band_error: float
    comparison_rms_truncation_band_error: float
    comparison_maximum_total_hamiltonian_error: float
    comparison_rms_total_hamiltonian_error: float
    comparison_maximum_total_band_error: float
    comparison_rms_total_band_error: float

    def __post_init__(self) -> None:
        """Require finite nonnegative errors and one ordinary-lattice cutoff."""
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if self.maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        for name in (
            "reference_ordinary_omitted_power",
            "comparison_ordinary_omitted_power",
            "reference_total_omitted_power",
            "comparison_total_omitted_power",
            "reference_maximum_truncation_hamiltonian_error",
            "reference_rms_truncation_hamiltonian_error",
            "reference_maximum_band_error",
            "reference_rms_band_error",
            "comparison_maximum_truncation_hamiltonian_error",
            "comparison_rms_truncation_hamiltonian_error",
            "comparison_maximum_truncation_band_error",
            "comparison_rms_truncation_band_error",
            "comparison_maximum_total_hamiltonian_error",
            "comparison_rms_total_hamiltonian_error",
            "comparison_maximum_total_band_error",
            "comparison_rms_total_band_error",
        ):
            _nonnegative(name, getattr(self, name))
        if self.reference_total_omitted_power < self.reference_ordinary_omitted_power:
            raise ValueError("reference total omitted power must include Nyquist power")
        if self.comparison_total_omitted_power < self.comparison_ordinary_omitted_power:
            raise ValueError(
                "comparison total omitted power must include Nyquist power"
            )


@dataclass(frozen=True, slots=True)
class SmoothFourStateTruncationPointResult:
    """Report ordinary conversion, interpolation, and cutoff errors at one amplitude."""

    amplitude: float
    reference_nyquist_power: float
    comparison_nyquist_power: float
    reference_maximum_ordinary_hermiticity_defect: float
    comparison_maximum_ordinary_hermiticity_defect: float
    maximum_direct_band_defect: float
    comparison_maximum_interpolation_hamiltonian_error: float
    comparison_rms_interpolation_hamiltonian_error: float
    comparison_maximum_interpolation_band_error: float
    comparison_rms_interpolation_band_error: float
    ranges: tuple[SmoothFourStateTruncationRangeResult, ...]

    def __post_init__(self) -> None:
        """Validate one amplitude and its ordered cutoff inventory."""
        _nonnegative("amplitude", self.amplitude)
        for name in (
            "reference_nyquist_power",
            "comparison_nyquist_power",
            "reference_maximum_ordinary_hermiticity_defect",
            "comparison_maximum_ordinary_hermiticity_defect",
            "maximum_direct_band_defect",
            "comparison_maximum_interpolation_hamiltonian_error",
            "comparison_rms_interpolation_hamiltonian_error",
            "comparison_maximum_interpolation_band_error",
            "comparison_rms_interpolation_band_error",
        ):
            _nonnegative(name, getattr(self, name))
        if type(self.ranges) is not tuple or not self.ranges:
            raise TypeError("ranges must be a nonempty tuple")
        if any(
            type(item) is not SmoothFourStateTruncationRangeResult
            for item in self.ranges
        ):
            raise TypeError("ranges must contain truncation range results")
        cutoffs = tuple(item.maximum_range for item in self.ranges)
        if cutoffs != tuple(sorted(set(cutoffs))):
            raise ValueError("range results must be unique and strictly increasing")


@dataclass(frozen=True, slots=True)
class SmoothFourStateTruncationResult:
    """Retain one pointwise finite-range consequence study."""

    definition: SmoothFourStateTruncationDefinition
    minimum_external_gap: float
    minimum_transport_singular_value: float
    maximum_transport_procrustes_residual: float
    maximum_transport_unitarity_defect: float
    maximum_transport_rank_cutoff: float
    closure_holonomy_phases: tuple[float, ...]
    closure_holonomy_unitarity_defect: float
    maximum_frame_orthonormality_defect: float
    periodic_closure_defect: float
    maximum_reference_hermiticity_defect: float
    evaluation_coordinate_offset: float
    minimum_construction_evaluation_separation: float
    points: tuple[SmoothFourStateTruncationPointResult, ...]

    def __post_init__(self) -> None:
        """Correlate the result with its definition and disjoint sample roles."""
        if type(self.definition) is not SmoothFourStateTruncationDefinition:
            raise TypeError("definition must be SmoothFourStateTruncationDefinition")
        for name in (
            "minimum_external_gap",
            "minimum_transport_singular_value",
            "maximum_transport_procrustes_residual",
            "maximum_transport_unitarity_defect",
            "maximum_transport_rank_cutoff",
            "closure_holonomy_unitarity_defect",
            "maximum_frame_orthonormality_defect",
            "periodic_closure_defect",
            "maximum_reference_hermiticity_defect",
        ):
            _nonnegative(name, getattr(self, name))
        if (
            type(self.closure_holonomy_phases) is not tuple
            or len(self.closure_holonomy_phases) != 2
        ):
            raise TypeError(
                "closure_holonomy_phases must contain the rank-two phase set"
            )
        for phase in self.closure_holonomy_phases:
            _finite_float("closure_holonomy_phase", phase)
            if not -math.pi <= phase <= math.pi:
                raise ValueError("closure holonomy phases must lie in [-pi, pi]")
        if self.closure_holonomy_phases != tuple(sorted(self.closure_holonomy_phases)):
            raise ValueError("closure holonomy phases must be ordered")
        if self.minimum_external_gap < self.definition.model.minimum_external_gap:
            raise ValueError("minimum_external_gap fails its declared lower bound")
        if (
            self.minimum_transport_singular_value
            <= self.definition.model.minimum_transport_singular_value
        ):
            raise ValueError("minimum_transport_singular_value fails its lower bound")
        _nonnegative("evaluation_coordinate_offset", self.evaluation_coordinate_offset)
        _nonnegative(
            "minimum_construction_evaluation_separation",
            self.minimum_construction_evaluation_separation,
        )
        if self.evaluation_coordinate_offset == 0.0:
            raise ValueError("evaluation_coordinate_offset must be positive")
        if self.minimum_construction_evaluation_separation == 0.0:
            raise ValueError("construction and evaluation meshes must be disjoint")
        if type(self.points) is not tuple or any(
            type(point) is not SmoothFourStateTruncationPointResult
            for point in self.points
        ):
            raise TypeError("points must contain truncation point results")
        if (
            tuple(point.amplitude for point in self.points)
            != self.definition.model.amplitudes
        ):
            raise ValueError("point amplitudes must match the definition")
        expected_ranges = self.definition.maximum_ranges
        if any(
            tuple(item.maximum_range for item in point.ranges) != expected_ranges
            for point in self.points
        ):
            raise ValueError("every point must report every declared cutoff")
        if not math.isfinite(self.minimum_construction_evaluation_separation):
            raise ValueError("mesh separation must be finite")
