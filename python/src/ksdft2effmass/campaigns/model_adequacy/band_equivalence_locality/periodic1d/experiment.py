"""Calculation actions for the maintained smooth continuum experiment."""

from __future__ import annotations

import math

import numpy as np
import numpy.typing as npt
from projectkoios.optimization.selection.harmonic import (
    PeriodicHarmonic,
    PeriodicHarmonicMaximizer,
)

from .definition import (
    SmoothBlochContinuumConvergenceDefinition,
    SmoothBlochContinuumDefinition,
)
from .results import (
    SmoothBlochContinuumConvergenceDisposition,
    SmoothBlochContinuumConvergenceResult,
    SmoothBlochContinuumHoppingBlockResult,
    SmoothBlochContinuumPointResult,
    SmoothBlochContinuumRefinementResult,
    SmoothBlochContinuumResult,
)


class SmoothBlochContinuumExperiment:
    """Compare Bloch-only and representation-aware channels across a smooth gauge.

    Notes
    -----
    The normalized analytic parent is ``sigma_z``. For amplitude ``a`` the attacked
    field is ``R(a*sin(2*pi*q))^T sigma_z R(a*sin(2*pi*q))``. The action calls the
    Optimization owner only for exact continuous maximization of the reconstructed
    second harmonic. KSD owns the reciprocal mesh, analytic comparator, Fourier
    convention, locality channels, and scientific interpretation.
    """

    __slots__ = ()

    def execute(
        self, definition: SmoothBlochContinuumDefinition
    ) -> SmoothBlochContinuumResult:
        """Calculate the complete smooth continuum on one uniform reciprocal mesh."""
        if type(definition) is not SmoothBlochContinuumDefinition:
            raise TypeError("definition must be SmoothBlochContinuumDefinition")
        sample_count = definition.reciprocal_mesh_size
        coordinates = -0.5 + np.arange(sample_count, dtype=np.float64) / float(
            sample_count
        )
        reference = np.broadcast_to(
            np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128),
            (sample_count, 2, 2),
        ).copy()
        reference_eigenvalues = np.linalg.eigvalsh(reference)
        displacements = tuple(range(-(sample_count // 2), sample_count // 2))
        maximizer = PeriodicHarmonicMaximizer(
            absolute_degeneracy_tolerance=(
                definition.harmonic_absolute_degeneracy_tolerance
            ),
            relative_degeneracy_tolerance=(
                definition.harmonic_relative_degeneracy_tolerance
            ),
        )
        points = tuple(
            self._point(
                amplitude,
                coordinates,
                reference_eigenvalues,
                displacements,
                maximizer,
            )
            for amplitude in definition.amplitudes
        )
        return SmoothBlochContinuumResult(definition, points)

    @staticmethod
    def _point(
        amplitude: float,
        coordinates: npt.NDArray[np.float64],
        reference_eigenvalues: npt.NDArray[np.float64],
        displacements: tuple[int, ...],
        maximizer: PeriodicHarmonicMaximizer,
    ) -> SmoothBlochContinuumPointResult:
        """Calculate all channels at one continuum amplitude."""
        theta = amplitude * np.sin(2.0 * np.pi * coordinates)
        cosine = np.cos(2.0 * theta)
        sine = np.sin(2.0 * theta)
        attacked = np.empty((coordinates.size, 2, 2), dtype=np.complex128)
        attacked[:, 0, 0] = cosine
        attacked[:, 0, 1] = -sine
        attacked[:, 1, 0] = -sine
        attacked[:, 1, 1] = -cosine
        band_defect = float(
            np.max(np.abs(np.linalg.eigvalsh(attacked) - reference_eigenvalues))
        )

        correlation_cosine = float(np.mean(cosine))
        correlation_sine = float(np.mean(sine))
        harmonic_maximum = maximizer.maximize(
            PeriodicHarmonic(
                offset=0.0,
                cosine_coefficient=correlation_cosine,
                sine_coefficient=correlation_sine,
                harmonic_order=2,
                fundamental_interval_start=-math.pi / 2.0,
            )
        )
        discrete_correlation = harmonic_maximum.maximum_value
        analytic_correlation = _protocol_bessel_j0(2.0 * amplitude)
        correlation_defect = abs(discrete_correlation - analytic_correlation)

        block_matrices = SmoothBlochContinuumExperiment._fourier_blocks(
            coordinates,
            attacked,
            displacements,
        )
        block_results = tuple(
            SmoothBlochContinuumHoppingBlockResult(
                displacement,
                float(np.linalg.norm(block) ** 2 / 2.0),
            )
            for displacement, block in zip(displacements, block_matrices, strict=True)
        )
        nonzero_weight = float(
            sum(
                item.normalized_squared_frobenius_norm
                for item in block_results
                if item.displacement != 0
            )
        )
        sample_power = float(np.mean(np.sum(np.abs(attacked) ** 2, axis=(1, 2)) / 2.0))
        coefficient_power = float(
            sum(item.normalized_squared_frobenius_norm for item in block_results)
        )
        parseval_defect = abs(sample_power - coefficient_power)

        operator_squared_loss = max(0.0, 1.0 - discrete_correlation**2)
        operator_threshold = math.sqrt(operator_squared_loss)
        onsite_mismatch = (1.0 - discrete_correlation) ** 2
        joint_threshold = math.sqrt(operator_squared_loss + onsite_mismatch)
        analytic_operator_squared = max(0.0, 1.0 - analytic_correlation**2)
        analytic_operator_threshold = math.sqrt(analytic_operator_squared)
        analytic_joint_threshold = math.sqrt(
            max(0.0, 2.0 * (1.0 - analytic_correlation))
        )
        identity_defect = max(
            abs(operator_squared_loss - operator_threshold**2),
            abs(operator_squared_loss - nonzero_weight),
            abs(joint_threshold**2 - (nonzero_weight + onsite_mismatch)),
        )
        return SmoothBlochContinuumPointResult(
            amplitude=amplitude,
            maximum_band_defect=band_defect,
            harmonic_maximum=harmonic_maximum,
            discrete_maximum_correlation=discrete_correlation,
            analytic_maximum_correlation=analytic_correlation,
            correlation_quadrature_defect=correlation_defect,
            irreducible_operator_squared_loss=operator_squared_loss,
            minimum_operator_threshold=operator_threshold,
            exact_spectrum_joint_operator_threshold=joint_threshold,
            analytic_minimum_operator_threshold=analytic_operator_threshold,
            analytic_exact_spectrum_joint_operator_threshold=(analytic_joint_threshold),
            nonzero_hopping_weight=nonzero_weight,
            onsite_mismatch_squared=onsite_mismatch,
            three_way_identity_defect=identity_defect,
            parseval_defect=parseval_defect,
            hopping_blocks=block_results,
        )

    @staticmethod
    def _fourier_blocks(
        coordinates: npt.NDArray[np.float64],
        matrices: npt.NDArray[np.complex128],
        displacements: tuple[int, ...],
    ) -> npt.NDArray[np.complex128]:
        """Return complete negative-exponent, one-over-N Fourier coefficients."""
        phases = np.exp(
            -2.0j
            * np.pi
            * np.outer(np.asarray(displacements, dtype=np.float64), coordinates)
        )
        return np.asarray(
            np.einsum("rn,nij->rij", phases, matrices, optimize=True)
            / float(coordinates.size),
            dtype=np.complex128,
        )


def _protocol_bessel_j0(argument: float) -> float:
    """Evaluate ``J_0`` on the protocol interval by its alternating power series."""
    if not math.isfinite(argument):
        raise ValueError("Bessel argument must be finite")
    if abs(argument) > math.pi / 2.0:
        raise ValueError("Bessel argument lies outside the protocol interval")
    terms = [1.0]
    term = 1.0
    quarter_square = argument * argument / 4.0
    for order in range(1, 65):
        term *= -quarter_square / float(order * order)
        terms.append(term)
        total = math.fsum(terms)
        if abs(term) <= math.ulp(1.0) * max(1.0, abs(total)):
            return total
    raise FloatingPointError("Bessel series did not converge on the protocol interval")


class SmoothBlochContinuumConvergenceExperiment:
    """Evaluate caller-selected nested meshes and classify demonstrated stability."""

    __slots__ = ()

    def execute(
        self, definition: SmoothBlochContinuumConvergenceDefinition
    ) -> SmoothBlochContinuumConvergenceResult:
        """Calculate every mesh and compare adjacent refinements conservatively."""
        if type(definition) is not SmoothBlochContinuumConvergenceDefinition:
            raise TypeError(
                "definition must be SmoothBlochContinuumConvergenceDefinition"
            )
        action = SmoothBlochContinuumExperiment()
        mesh_results = tuple(
            action.execute(definition.mesh_definition(size))
            for size in definition.reciprocal_mesh_sizes
        )
        refinements = tuple(
            self._refinement(coarse, fine, definition)
            for coarse, fine in zip(mesh_results[:-1], mesh_results[1:], strict=True)
        )
        required = definition.required_stable_refinements
        disposition = (
            SmoothBlochContinuumConvergenceDisposition.CONVERGED
            if all(item.within_tolerances for item in refinements[-required:])
            else SmoothBlochContinuumConvergenceDisposition.UNRESOLVED
        )
        return SmoothBlochContinuumConvergenceResult(
            definition, mesh_results, refinements, disposition
        )

    @staticmethod
    def _refinement(
        coarse: SmoothBlochContinuumResult,
        fine: SmoothBlochContinuumResult,
        definition: SmoothBlochContinuumConvergenceDefinition,
    ) -> SmoothBlochContinuumRefinementResult:
        """Compare one adjacent nested pair without analytic-value substitution."""
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
                    fine_point.nonzero_hopping_weight
                    - coarse_point.nonzero_hopping_weight
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
            common_displacements = coarse_blocks.keys() & fine_blocks.keys()
            hopping_block_change = max(
                hopping_block_change,
                *(
                    abs(fine_blocks[key] - coarse_blocks[key])
                    for key in common_displacements
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

        fine_quadrature = max(
            point.correlation_quadrature_defect for point in fine.points
        )
        band_defect = max(point.maximum_band_defect for point in fine.points)
        identity_defect = max(point.three_way_identity_defect for point in fine.points)
        parseval_defect = max(point.parseval_defect for point in fine.points)
        thresholds = definition.thresholds
        margin = definition.verification_absolute_tolerance
        within_tolerances = (
            angle_dispositions_stable
            and correlation_change + margin <= thresholds.maximum_correlation_change
            and threshold_change + margin <= thresholds.maximum_threshold_change
            and hopping_weight_change + margin
            <= thresholds.maximum_hopping_weight_change
            and hopping_block_change + margin
            <= thresholds.maximum_hopping_block_power_change
            and angle_change + margin <= thresholds.maximum_angle_change
            and fine_quadrature + margin <= thresholds.maximum_fine_quadrature_defect
            and band_defect + margin <= thresholds.maximum_band_defect
            and identity_defect + margin <= thresholds.maximum_identity_defect
            and parseval_defect + margin <= thresholds.maximum_parseval_defect
        )
        return SmoothBlochContinuumRefinementResult(
            coarse_mesh_size=coarse.definition.reciprocal_mesh_size,
            fine_mesh_size=fine.definition.reciprocal_mesh_size,
            maximum_correlation_change=correlation_change,
            maximum_threshold_change=threshold_change,
            maximum_hopping_weight_change=hopping_weight_change,
            maximum_hopping_block_power_change=hopping_block_change,
            maximum_angle_change=angle_change,
            maximizing_angle_dispositions_stable=angle_dispositions_stable,
            maximum_fine_quadrature_defect=fine_quadrature,
            maximum_band_defect=band_defect,
            maximum_identity_defect=identity_defect,
            maximum_parseval_defect=parseval_defect,
            within_tolerances=within_tolerances,
        )


__all__ = [
    "SmoothBlochContinuumConvergenceExperiment",
    "SmoothBlochContinuumExperiment",
]
