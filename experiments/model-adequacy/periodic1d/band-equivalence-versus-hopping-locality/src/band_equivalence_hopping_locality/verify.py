"""Independent reconstruction for the maintained smooth continuum."""

from __future__ import annotations

import math
from dataclasses import dataclass

from projectkoios.optimization.selection.harmonic import (
    PeriodicHarmonicMaximumStatus,
)

from .definition import (
    SmoothBlochContinuumConvergenceDefinition,
    SmoothBlochContinuumDefinition,
    _finite_float,
)
from .results import (
    SmoothBlochContinuumConvergenceDisposition,
    SmoothBlochContinuumConvergenceResult,
    SmoothBlochContinuumPointResult,
    SmoothBlochContinuumRefinementResult,
    SmoothBlochContinuumResult,
)


@dataclass(frozen=True, slots=True)
class SmoothBlochContinuumVerificationResult:
    """Retain the maximum independent continuum-reconstruction defect."""

    experiment_result: SmoothBlochContinuumResult
    maximum_absolute_defect: float
    absolute_tolerance: float
    passes: bool

    def __post_init__(self) -> None:
        """Validate the defect and its derived pass disposition."""
        if type(self.experiment_result) is not SmoothBlochContinuumResult:
            raise TypeError("experiment_result must be SmoothBlochContinuumResult")
        for name, value in (
            ("maximum_absolute_defect", self.maximum_absolute_defect),
            ("absolute_tolerance", self.absolute_tolerance),
        ):
            _finite_float(name, value)
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        expected = self.maximum_absolute_defect <= self.absolute_tolerance
        if self.passes is not expected:
            raise ValueError("passes must match the defect and tolerance")


class SmoothBlochContinuumVerifier:
    """Independently reconstruct the smooth continuum without calling its producer."""

    __slots__ = ()

    def execute(
        self, result: SmoothBlochContinuumResult
    ) -> SmoothBlochContinuumVerificationResult:
        """Return the maximum defect across every retained continuum channel."""
        if type(result) is not SmoothBlochContinuumResult:
            raise TypeError("result must be SmoothBlochContinuumResult")
        definition = result.definition
        count = definition.reciprocal_mesh_size
        coordinates = tuple(-0.5 + index / float(count) for index in range(count))
        displacements = tuple(range(-(count // 2), count // 2))
        defects: list[float] = []
        for retained in result.points:
            self._point_defects(
                retained,
                definition,
                coordinates,
                displacements,
                defects,
            )
        maximum = max(defects, default=0.0)
        tolerance = definition.verification_absolute_tolerance
        return SmoothBlochContinuumVerificationResult(
            result,
            float(maximum),
            tolerance,
            maximum <= tolerance,
        )

    @staticmethod
    def _point_defects(
        retained: SmoothBlochContinuumPointResult,
        definition: SmoothBlochContinuumDefinition,
        coordinates: tuple[float, ...],
        displacements: tuple[int, ...],
        defects: list[float],
    ) -> None:
        """Append independently reconstructed defects at one amplitude."""
        amplitude = retained.amplitude
        cosine_samples = tuple(
            math.cos(2.0 * amplitude * math.sin(math.tau * coordinate))
            for coordinate in coordinates
        )
        sine_samples = tuple(
            math.sin(2.0 * amplitude * math.sin(math.tau * coordinate))
            for coordinate in coordinates
        )
        cosine_coefficient = math.fsum(cosine_samples) / float(len(coordinates))
        sine_coefficient = math.fsum(sine_samples) / float(len(coordinates))
        harmonic_amplitude = math.hypot(cosine_coefficient, sine_coefficient)
        maximum = harmonic_amplitude
        scale = max(1.0, harmonic_amplitude)
        cutoff = definition.harmonic_absolute_degeneracy_tolerance + (
            definition.harmonic_relative_degeneracy_tolerance * scale
        )
        is_degenerate = harmonic_amplitude <= cutoff
        expected_status = (
            PeriodicHarmonicMaximumStatus.NUMERICALLY_CONSTANT
            if is_degenerate
            else PeriodicHarmonicMaximumStatus.UNIQUE
        )
        expected_argument = (
            None
            if is_degenerate
            else _verification_canonical_angle(
                math.atan2(sine_coefficient, cosine_coefficient) / 2.0
            )
        )
        owner = retained.harmonic_maximum
        defects.extend(
            (
                abs(owner.harmonic.offset),
                abs(owner.harmonic.cosine_coefficient - cosine_coefficient),
                abs(owner.harmonic.sine_coefficient - sine_coefficient),
                0.0 if owner.harmonic.harmonic_order == 2 else 1.0,
                abs(owner.harmonic.fundamental_interval_start + math.pi / 2.0),
                abs(owner.amplitude - harmonic_amplitude),
                abs(owner.maximum_value - maximum),
                abs(owner.applied_degeneracy_cutoff - cutoff),
                0.0 if owner.status is expected_status else 1.0,
                _optional_float_defect(
                    owner.canonical_maximizing_argument,
                    expected_argument,
                ),
            )
        )

        analytic = _verification_bessel_j0(2.0 * amplitude)
        operator_squared = max(0.0, 1.0 - maximum**2)
        operator_threshold = math.sqrt(operator_squared)
        onsite_mismatch = (1.0 - maximum) ** 2
        joint_threshold = math.sqrt(operator_squared + onsite_mismatch)
        analytic_operator = math.sqrt(max(0.0, 1.0 - analytic**2))
        analytic_joint = math.sqrt(max(0.0, 2.0 * (1.0 - analytic)))

        block_powers = tuple(
            _verification_block_power(
                displacement,
                coordinates,
                cosine_samples,
                sine_samples,
            )
            for displacement in displacements
        )
        nonzero_weight = math.fsum(
            power
            for displacement, power in zip(displacements, block_powers, strict=True)
            if displacement != 0
        )
        coefficient_power = math.fsum(block_powers)
        sample_power = math.fsum(
            cosine * cosine + sine * sine
            for cosine, sine in zip(cosine_samples, sine_samples, strict=True)
        ) / float(len(coordinates))
        identity_defect = max(
            abs(operator_squared - operator_threshold**2),
            abs(operator_squared - nonzero_weight),
            abs(joint_threshold**2 - (nonzero_weight + onsite_mismatch)),
        )
        expected_band_defect = max(
            abs(math.hypot(cosine, sine) - 1.0)
            for cosine, sine in zip(cosine_samples, sine_samples, strict=True)
        )
        defects.extend(
            (
                abs(retained.maximum_band_defect - expected_band_defect),
                abs(retained.discrete_maximum_correlation - maximum),
                abs(retained.analytic_maximum_correlation - analytic),
                abs(retained.correlation_quadrature_defect - abs(maximum - analytic)),
                abs(retained.irreducible_operator_squared_loss - operator_squared),
                abs(retained.minimum_operator_threshold - operator_threshold),
                abs(retained.exact_spectrum_joint_operator_threshold - joint_threshold),
                abs(retained.analytic_minimum_operator_threshold - analytic_operator),
                abs(
                    retained.analytic_exact_spectrum_joint_operator_threshold
                    - analytic_joint
                ),
                abs(retained.nonzero_hopping_weight - nonzero_weight),
                abs(retained.onsite_mismatch_squared - onsite_mismatch),
                abs(retained.three_way_identity_defect - identity_defect),
                abs(retained.parseval_defect - abs(sample_power - coefficient_power)),
            )
        )
        if len(retained.hopping_blocks) != len(displacements):
            defects.append(1.0)
        else:
            for item, displacement, power in zip(
                retained.hopping_blocks,
                displacements,
                block_powers,
                strict=True,
            ):
                defects.append(0.0 if item.displacement == displacement else 1.0)
                defects.append(abs(item.normalized_squared_frobenius_norm - power))


def _verification_block_power(
    displacement: int,
    coordinates: tuple[float, ...],
    cosine_samples: tuple[float, ...],
    sine_samples: tuple[float, ...],
) -> float:
    """Return one direct finite-Fourier normalized squared block norm."""
    real_cosine = 0.0
    imaginary_cosine = 0.0
    real_sine = 0.0
    imaginary_sine = 0.0
    for coordinate, cosine, sine in zip(
        coordinates, cosine_samples, sine_samples, strict=True
    ):
        phase = -math.tau * coordinate * float(displacement)
        phase_cosine = math.cos(phase)
        phase_sine = math.sin(phase)
        real_cosine += phase_cosine * cosine
        imaginary_cosine += phase_sine * cosine
        real_sine += phase_cosine * sine
        imaginary_sine += phase_sine * sine
    count = float(len(coordinates))
    cosine_power = (real_cosine / count) ** 2 + (imaginary_cosine / count) ** 2
    sine_power = (real_sine / count) ** 2 + (imaginary_sine / count) ** 2
    return cosine_power + sine_power


def _verification_bessel_j0(argument: float) -> float:
    """Independently evaluate the protocol Bessel comparator by recurrence."""
    quarter_square = argument * argument / 4.0
    total = 1.0
    term = 1.0
    for order in range(1, 65):
        term = -term * quarter_square / float(order * order)
        updated = total + term
        if abs(term) <= math.ulp(1.0) * max(1.0, abs(updated)):
            return updated
        total = updated
    raise FloatingPointError("verification Bessel series did not converge")


def _verification_canonical_angle(argument: float) -> float:
    """Reduce one maximizing angle into ``[-pi/2, pi/2)``."""
    return -math.pi / 2.0 + ((argument + math.pi / 2.0) % math.pi)


def _optional_float_defect(left: float | None, right: float | None) -> float:
    """Return an exact-presence-aware optional scalar defect."""
    if left is None or right is None:
        return 0.0 if left is right else 1.0
    return abs(left - right)


@dataclass(frozen=True, slots=True)
class SmoothBlochContinuumConvergenceVerificationResult:
    """Retain independent mesh and refinement reconstruction evidence."""

    experiment_result: SmoothBlochContinuumConvergenceResult
    mesh_verifications: tuple[SmoothBlochContinuumVerificationResult, ...]
    maximum_refinement_absolute_defect: float
    disposition_matches: bool
    passes: bool

    def __post_init__(self) -> None:
        """Validate correlated mesh verifications and derived pass state."""
        if type(self.experiment_result) is not SmoothBlochContinuumConvergenceResult:
            raise TypeError(
                "experiment_result must be SmoothBlochContinuumConvergenceResult"
            )
        if type(self.mesh_verifications) is not tuple or any(
            type(item) is not SmoothBlochContinuumVerificationResult
            for item in self.mesh_verifications
        ):
            raise TypeError("mesh_verifications must be a typed tuple")
        if tuple(item.experiment_result for item in self.mesh_verifications) != (
            self.experiment_result.mesh_results
        ):
            raise ValueError("mesh_verifications must bind every mesh result")
        _finite_float(
            "maximum_refinement_absolute_defect",
            self.maximum_refinement_absolute_defect,
        )
        if self.maximum_refinement_absolute_defect < 0.0:
            raise ValueError("maximum_refinement_absolute_defect must be nonnegative")
        if type(self.disposition_matches) is not bool or type(self.passes) is not bool:
            raise TypeError("verification dispositions must be built-in booleans")
        expected = (
            all(item.passes for item in self.mesh_verifications)
            and self.maximum_refinement_absolute_defect
            <= self.experiment_result.definition.verification_absolute_tolerance
            and self.disposition_matches
        )
        if self.passes is not expected:
            raise ValueError("passes must match reconstructed evidence")


class SmoothBlochContinuumConvergenceVerifier:
    """Independently reconstruct mesh calculations and refinement dispositions."""

    __slots__ = ()

    def execute(
        self, result: SmoothBlochContinuumConvergenceResult
    ) -> SmoothBlochContinuumConvergenceVerificationResult:
        """Verify every mesh, refinement metric, and final disposition."""
        if type(result) is not SmoothBlochContinuumConvergenceResult:
            raise TypeError("result must be SmoothBlochContinuumConvergenceResult")
        mesh_verifications = tuple(
            SmoothBlochContinuumVerifier().execute(item) for item in result.mesh_results
        )
        defects: list[float] = []
        expected_within: list[bool] = []
        for retained, coarse, fine in zip(
            result.refinements,
            result.mesh_results[:-1],
            result.mesh_results[1:],
            strict=True,
        ):
            expected = _verification_refinement(coarse, fine, result.definition)
            defects.extend(
                (
                    abs(
                        retained.maximum_correlation_change
                        - expected.maximum_correlation_change
                    ),
                    abs(
                        retained.maximum_threshold_change
                        - expected.maximum_threshold_change
                    ),
                    abs(
                        retained.maximum_hopping_weight_change
                        - expected.maximum_hopping_weight_change
                    ),
                    abs(
                        retained.maximum_hopping_block_power_change
                        - expected.maximum_hopping_block_power_change
                    ),
                    abs(retained.maximum_angle_change - expected.maximum_angle_change),
                    abs(
                        retained.maximum_fine_quadrature_defect
                        - expected.maximum_fine_quadrature_defect
                    ),
                    abs(retained.maximum_band_defect - expected.maximum_band_defect),
                    abs(
                        retained.maximum_identity_defect
                        - expected.maximum_identity_defect
                    ),
                    abs(
                        retained.maximum_parseval_defect
                        - expected.maximum_parseval_defect
                    ),
                    0.0
                    if retained.maximizing_angle_dispositions_stable
                    is expected.maximizing_angle_dispositions_stable
                    else 1.0,
                    0.0
                    if retained.within_tolerances is expected.within_tolerances
                    else 1.0,
                )
            )
            expected_within.append(expected.within_tolerances)
        required = result.definition.required_stable_refinements
        expected_disposition = (
            SmoothBlochContinuumConvergenceDisposition.CONVERGED
            if all(expected_within[-required:])
            else SmoothBlochContinuumConvergenceDisposition.UNRESOLVED
        )
        disposition_matches = result.disposition is expected_disposition
        maximum = max(defects, default=0.0)
        passes = (
            all(item.passes for item in mesh_verifications)
            and maximum <= result.definition.verification_absolute_tolerance
            and disposition_matches
        )
        return SmoothBlochContinuumConvergenceVerificationResult(
            result,
            mesh_verifications,
            maximum,
            disposition_matches,
            passes,
        )


def _verification_refinement(
    coarse: SmoothBlochContinuumResult,
    fine: SmoothBlochContinuumResult,
    definition: SmoothBlochContinuumConvergenceDefinition,
) -> SmoothBlochContinuumRefinementResult:
    """Reconstruct one adjacent refinement without calling the producer."""
    correlation_change = 0.0
    threshold_change = 0.0
    hopping_weight_change = 0.0
    hopping_block_change = 0.0
    angle_change = 0.0
    angle_dispositions_stable = True
    for coarse_point, fine_point in zip(coarse.points, fine.points, strict=True):
        correlation_change = max(
            correlation_change,
            abs(
                fine_point.discrete_maximum_correlation
                - coarse_point.discrete_maximum_correlation
            ),
        )
        threshold_change = max(
            threshold_change,
            abs(
                fine_point.minimum_operator_threshold
                - coarse_point.minimum_operator_threshold
            ),
            abs(
                fine_point.exact_spectrum_joint_operator_threshold
                - coarse_point.exact_spectrum_joint_operator_threshold
            ),
        )
        hopping_weight_change = max(
            hopping_weight_change,
            abs(
                fine_point.nonzero_hopping_weight - coarse_point.nonzero_hopping_weight
            ),
        )
        coarse_blocks = {
            item.displacement: item.normalized_squared_frobenius_norm
            for item in coarse_point.hopping_blocks
        }
        fine_blocks = {
            item.displacement: item.normalized_squared_frobenius_norm
            for item in fine_point.hopping_blocks
        }
        hopping_block_change = max(
            hopping_block_change,
            *(
                abs(fine_blocks[key] - coarse_blocks[key])
                for key in coarse_blocks.keys() & fine_blocks.keys()
            ),
        )
        coarse_angle = coarse_point.harmonic_maximum.canonical_maximizing_argument
        fine_angle = fine_point.harmonic_maximum.canonical_maximizing_argument
        if coarse_angle is None and fine_angle is None:
            current_angle_change = 0.0
        elif coarse_angle is None or fine_angle is None:
            angle_dispositions_stable = False
            current_angle_change = 0.0
        else:
            difference = abs(fine_angle - coarse_angle) % math.pi
            current_angle_change = min(difference, math.pi - difference)
        angle_change = max(angle_change, current_angle_change)
    fine_quadrature = max(point.correlation_quadrature_defect for point in fine.points)
    band_defect = max(point.maximum_band_defect for point in fine.points)
    identity_defect = max(point.three_way_identity_defect for point in fine.points)
    parseval_defect = max(point.parseval_defect for point in fine.points)
    thresholds = definition.thresholds
    margin = definition.verification_absolute_tolerance
    within = (
        angle_dispositions_stable
        and correlation_change + margin <= thresholds.maximum_correlation_change
        and threshold_change + margin <= thresholds.maximum_threshold_change
        and hopping_weight_change + margin <= thresholds.maximum_hopping_weight_change
        and hopping_block_change + margin
        <= thresholds.maximum_hopping_block_power_change
        and angle_change + margin <= thresholds.maximum_angle_change
        and fine_quadrature + margin <= thresholds.maximum_fine_quadrature_defect
        and band_defect + margin <= thresholds.maximum_band_defect
        and identity_defect + margin <= thresholds.maximum_identity_defect
        and parseval_defect + margin <= thresholds.maximum_parseval_defect
    )
    return SmoothBlochContinuumRefinementResult(
        coarse.definition.reciprocal_mesh_size,
        fine.definition.reciprocal_mesh_size,
        correlation_change,
        threshold_change,
        hopping_weight_change,
        hopping_block_change,
        angle_change,
        angle_dispositions_stable,
        fine_quadrature,
        band_defect,
        identity_defect,
        parseval_defect,
        within,
    )


__all__ = [
    "SmoothBlochContinuumConvergenceVerificationResult",
    "SmoothBlochContinuumConvergenceVerifier",
    "SmoothBlochContinuumVerificationResult",
    "SmoothBlochContinuumVerifier",
]
