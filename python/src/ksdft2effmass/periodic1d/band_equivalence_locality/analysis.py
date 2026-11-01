"""Native periodic-1D band-equivalence locality analysis."""

from __future__ import annotations

import math

import numpy as np
from projectkoios.optimization.selection.harmonic import (
    PeriodicHarmonic,
    PeriodicHarmonicMaximizer,
)
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.solidstate import (
    BlockHoppingInterpolationRequest1D,
    BlockHoppingInterpolator1D,
    BlockHoppingModel1D,
    BlockHoppingTruncationRequest1D,
    BlockHoppingTruncator1D,
    CenteredEvenMeshCyclicToOrdinaryConverter1D,
    CenteredEvenMeshCyclicToOrdinaryRequest1D,
    CenteredUniformReciprocalMesh1D,
    GaugeAttack,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorFourierTransformRequest1D,
    ReciprocalOperatorSamples1D,
)

from .gauge import Periodic1DRank2SinusoidalGaugeRotation
from .request import Periodic1DBandEquivalenceLocalityRequest
from .results import (
    Periodic1DBandEquivalenceHoppingPower,
    Periodic1DBandEquivalenceLocalityAnalysis,
    Periodic1DBandEquivalencePointAnalysis,
    Periodic1DBandEquivalenceRangeAnalysis,
)


class Periodic1DBandEquivalenceLocalityAnalyzer:
    """Calculate separated finite channels for one bound smooth gauge request."""

    __slots__ = ("_harmonic_maximizer", "_request")

    def __init__(
        self,
        *,
        request: Periodic1DBandEquivalenceLocalityRequest,
        harmonic_maximizer: PeriodicHarmonicMaximizer,
    ) -> None:
        if type(request) is not Periodic1DBandEquivalenceLocalityRequest:
            raise TypeError("request must be Periodic1DBandEquivalenceLocalityRequest")
        if type(harmonic_maximizer) is not PeriodicHarmonicMaximizer:
            raise TypeError("harmonic_maximizer must be PeriodicHarmonicMaximizer")
        self._request = request
        self._harmonic_maximizer = harmonic_maximizer

    @property
    def request(self) -> Periodic1DBandEquivalenceLocalityRequest:
        """Return the immutable scientific request."""
        return self._request

    def execute(self) -> Periodic1DBandEquivalenceLocalityAnalysis:
        """Calculate exact-band, restricted-alignment, and finite-range channels."""
        request = self.request
        unit = Unitless()
        period = ScalarQuantity(1.0, unit)
        mesh = CenteredUniformReciprocalMesh1D(period, request.construction_size)
        construction_coordinates = np.asarray(
            request.construction_reduced_momenta(), dtype=np.float64
        )
        evaluation_coordinates = VectorQuantity(
            np.asarray(request.evaluation_reduced_momenta(), dtype=np.float64),
            unit,
        )
        reference_eigenvalues = np.asarray((-1.0, 1.0), dtype=np.float64)
        points: list[Periodic1DBandEquivalencePointAnalysis] = []
        for amplitude in request.amplitudes:
            construction_matrices = self._attacked_matrices(
                construction_coordinates,
                amplitude,
                request.numerical_absolute_tolerance,
            )
            construction_eigenvalues = np.linalg.eigvalsh(construction_matrices)
            band_defect = float(
                np.max(np.abs(construction_eigenvalues - reference_eigenvalues))
            )
            angles = amplitude * np.sin(2.0 * np.pi * construction_coordinates)
            correlation_cosine = float(np.mean(np.cos(2.0 * angles)))
            correlation_sine = float(np.mean(np.sin(2.0 * angles)))
            harmonic_maximum = self._harmonic_maximizer.maximize(
                PeriodicHarmonic(
                    offset=0.0,
                    cosine_coefficient=correlation_cosine,
                    sine_coefficient=correlation_sine,
                    harmonic_order=2,
                    fundamental_interval_start=-math.pi / 2.0,
                )
            )
            correlation = float(harmonic_maximum.maximum_value)
            if (
                correlation > 1.0
                and correlation - 1.0 <= request.numerical_absolute_tolerance
            ):
                correlation = 1.0
            if not -1.0 <= correlation <= 1.0:
                raise FloatingPointError("finite correlation lies outside [-1, 1]")
            alignment_angle = harmonic_maximum.canonical_maximizing_argument
            if alignment_angle is None:
                alignment_angle = 0.0
            optimal_scale = max(0.0, correlation)
            operator_squared_loss = max(0.0, 1.0 - optimal_scale**2)
            operator_threshold = math.sqrt(operator_squared_loss)
            joint_threshold = math.sqrt(max(0.0, 2.0 * (1.0 - correlation)))
            analytic_correlation = self._bessel_j0(2.0 * amplitude)

            samples = ReciprocalOperatorSamples1D(
                coordinates=mesh.coordinates,
                reciprocal_period=period,
                matrices=tuple(
                    ComplexMatrixQuantity(matrix, unit)
                    for matrix in construction_matrices
                ),
            )
            transform = ReciprocalOperatorFourierTransformer1D(
                ReciprocalOperatorFourierTransformRequest1D(
                    source=samples,
                    mesh=mesh,
                    coordinate_absolute_tolerance=request.numerical_absolute_tolerance,
                    reconstruction_absolute_tolerance=(
                        request.numerical_absolute_tolerance
                    ),
                )
            ).execute()
            conversion = CenteredEvenMeshCyclicToOrdinaryConverter1D(
                CenteredEvenMeshCyclicToOrdinaryRequest1D(transform.hopping_model)
            ).execute()
            complete_evaluation = BlockHoppingInterpolator1D(
                BlockHoppingInterpolationRequest1D(
                    conversion.ordinary,
                    evaluation_coordinates,
                )
            ).execute()
            direct_evaluation_values = self._attacked_matrices(
                evaluation_coordinates.magnitude,
                amplitude,
                request.numerical_absolute_tolerance,
            )
            complete_values = np.asarray(
                [matrix.magnitude for matrix in complete_evaluation.matrices],
                dtype=np.complex128,
            )
            interpolation_matrix, interpolation_spectral = self._errors(
                complete_values,
                direct_evaluation_values,
            )
            powers = tuple(
                Periodic1DBandEquivalenceHoppingPower(
                    displacement=representative,
                    normalized_squared_frobenius_norm=float(
                        np.linalg.norm(block.magnitude) ** 2 / 2.0
                    ),
                )
                for representative, block in zip(
                    transform.hopping_model.representatives,
                    transform.hopping_model.hopping_blocks,
                    strict=True,
                )
            )
            ranges = tuple(
                self._range_analysis(
                    conversion.ordinary,
                    maximum_range,
                    evaluation_coordinates,
                    complete_values,
                    direct_evaluation_values,
                )
                for maximum_range in request.maximum_ranges
            )
            points.append(
                Periodic1DBandEquivalencePointAnalysis(
                    amplitude=amplitude,
                    maximum_band_defect=band_defect,
                    discrete_maximum_correlation=correlation,
                    analytic_maximum_correlation=analytic_correlation,
                    correlation_quadrature_defect=abs(
                        correlation - analytic_correlation
                    ),
                    global_alignment_angle=float(alignment_angle),
                    optimal_splitting_scale=optimal_scale,
                    irreducible_operator_squared_loss=operator_squared_loss,
                    minimum_operator_threshold=operator_threshold,
                    exact_spectrum_joint_operator_threshold=joint_threshold,
                    cyclic_nyquist_power=(
                        conversion.conversion_power_per_matrix_dimension
                    ),
                    reconstruction_maximum_frobenius_error=(
                        transform.reconstruction_maximum_frobenius_error
                    ),
                    interpolation_hamiltonian_maximum_error=interpolation_matrix,
                    interpolation_spectral_maximum_error=interpolation_spectral,
                    hopping_powers=powers,
                    ranges=ranges,
                )
            )
        return Periodic1DBandEquivalenceLocalityAnalysis(request, tuple(points))

    @staticmethod
    def _attacked_matrices(
        coordinates: np.ndarray[tuple[int], np.dtype[np.float64]],
        amplitude: float,
        unitarity_absolute_tolerance: float,
    ) -> np.ndarray[tuple[int, int, int], np.dtype[np.complex128]]:
        parent = np.broadcast_to(
            np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128),
            (coordinates.size, 2, 2),
        ).copy()
        rotation = Periodic1DRank2SinusoidalGaugeRotation(amplitude)
        return GaugeAttack(
            rotation,
            unitarity_absolute_tolerance,
        ).apply(
            coordinates=coordinates,
            represented_matrices=parent,
        )

    @staticmethod
    def _errors(
        candidate: np.ndarray[tuple[int, int, int], np.dtype[np.complex128]],
        reference: np.ndarray[tuple[int, int, int], np.dtype[np.complex128]],
    ) -> tuple[float, float]:
        difference = candidate - reference
        matrix_error = float(
            np.max(np.linalg.norm(difference, axis=(1, 2))) / math.sqrt(2.0)
        )
        spectral_error = float(
            np.max(
                np.abs(np.linalg.eigvalsh(candidate) - np.linalg.eigvalsh(reference))
            )
        )
        return matrix_error, spectral_error

    def _range_analysis(
        self,
        ordinary_model: BlockHoppingModel1D,
        maximum_range: int,
        evaluation_coordinates: VectorQuantity,
        complete_values: np.ndarray[tuple[int, int, int], np.dtype[np.complex128]],
        direct_values: np.ndarray[tuple[int, int, int], np.dtype[np.complex128]],
    ) -> Periodic1DBandEquivalenceRangeAnalysis:
        if type(ordinary_model) is not BlockHoppingModel1D:
            raise TypeError("ordinary_model must be BlockHoppingModel1D")
        truncation = BlockHoppingTruncator1D(
            BlockHoppingTruncationRequest1D(ordinary_model, maximum_range)
        ).execute()
        evaluated = BlockHoppingInterpolator1D(
            BlockHoppingInterpolationRequest1D(
                truncation.truncated,
                evaluation_coordinates,
            )
        ).execute()
        truncated_values = np.asarray(
            [matrix.magnitude for matrix in evaluated.matrices],
            dtype=np.complex128,
        )
        truncation_matrix, truncation_spectral = self._errors(
            truncated_values,
            complete_values,
        )
        total_matrix, total_spectral = self._errors(
            truncated_values,
            direct_values,
        )
        return Periodic1DBandEquivalenceRangeAnalysis(
            maximum_range=maximum_range,
            ordinary_omitted_block_l2_norm=(
                truncation.omitted_block_l2_norm / math.sqrt(2.0)
            ),
            truncation_hamiltonian_maximum_error=truncation_matrix,
            total_hamiltonian_maximum_error=total_matrix,
            truncation_spectral_maximum_error=truncation_spectral,
            total_spectral_maximum_error=total_spectral,
        )

    @staticmethod
    def _bessel_j0(argument: float) -> float:
        """Evaluate ``J_0`` on the protocol interval by an alternating series."""
        if type(argument) is not float or not math.isfinite(argument):
            raise TypeError("argument must be a finite built-in float")
        if abs(argument) > math.pi / 2.0:
            raise ValueError("argument lies outside the protocol interval")
        total = 1.0
        term = 1.0
        quarter_square = argument * argument / 4.0
        for order in range(1, 65):
            term *= -quarter_square / float(order * order)
            updated = total + term
            if abs(term) <= math.ulp(1.0) * max(1.0, abs(updated)):
                return updated
            total = updated
        raise FloatingPointError("Bessel series did not converge")


__all__ = ["Periodic1DBandEquivalenceLocalityAnalyzer"]
