"""Independent direct-sum reference for periodic-1D band-equivalence locality."""

from __future__ import annotations

import math

import numpy as np

from .request import Periodic1DBandEquivalenceLocalityRequest
from .results import (
    Periodic1DBandEquivalenceHoppingPower,
    Periodic1DBandEquivalenceLocalityAnalysis,
    Periodic1DBandEquivalencePointAnalysis,
    Periodic1DBandEquivalenceRangeAnalysis,
)


class Periodic1DBandEquivalenceLocalityIndependentReferenceAnalyzer:
    """Reconstruct every retained flat-parent observation by explicit finite sums."""

    __slots__ = ("_request",)

    def __init__(self, request: Periodic1DBandEquivalenceLocalityRequest) -> None:
        if type(request) is not Periodic1DBandEquivalenceLocalityRequest:
            raise TypeError("request must be Periodic1DBandEquivalenceLocalityRequest")
        self._request = request

    def execute(self) -> Periodic1DBandEquivalenceLocalityAnalysis:
        """Return a direct-sum reference without calling production transform owners."""
        request = self._request
        construction = np.asarray(
            request.construction_reduced_momenta(), dtype=np.float64
        )
        evaluation = np.asarray(request.evaluation_reduced_momenta(), dtype=np.float64)
        representatives = np.arange(
            -(request.construction_size // 2),
            request.construction_size // 2,
            dtype=np.int64,
        )
        ordinary_mask = representatives != -(request.construction_size // 2)
        points: list[Periodic1DBandEquivalencePointAnalysis] = []
        for amplitude in request.amplitudes:
            construction_values = _flat_attacked_values(construction, amplitude)
            evaluation_values = _flat_attacked_values(evaluation, amplitude)
            blocks = _direct_fourier_blocks(
                construction, construction_values, representatives
            )
            reconstructed = _evaluate_blocks(construction, representatives, blocks)
            ordinary_representatives = representatives[ordinary_mask]
            ordinary_blocks = blocks[ordinary_mask]
            complete = _evaluate_blocks(
                evaluation, ordinary_representatives, ordinary_blocks
            )
            interpolation_matrix, interpolation_spectral = _errors(
                complete, evaluation_values
            )
            angles = amplitude * np.sin(2.0 * np.pi * construction)
            cosine = float(np.mean(np.cos(2.0 * angles)))
            sine = float(np.mean(np.sin(2.0 * angles)))
            correlation = math.hypot(cosine, sine)
            if (
                correlation > 1.0
                and correlation - 1.0 <= request.numerical_absolute_tolerance
            ):
                correlation = 1.0
            angle = 0.5 * math.atan2(sine, cosine) if correlation > 0.0 else 0.0
            optimal_scale = max(0.0, correlation)
            squared_loss = max(0.0, 1.0 - optimal_scale**2)
            ranges: list[Periodic1DBandEquivalenceRangeAnalysis] = []
            for maximum_range in request.maximum_ranges:
                retained = np.abs(ordinary_representatives) <= maximum_range
                truncated = _evaluate_blocks(
                    evaluation,
                    ordinary_representatives[retained],
                    ordinary_blocks[retained],
                )
                truncation_matrix, truncation_spectral = _errors(truncated, complete)
                total_matrix, total_spectral = _errors(truncated, evaluation_values)
                omitted = float(
                    np.sqrt(
                        np.sum(
                            np.abs(ordinary_blocks[~retained]) ** 2,
                            dtype=np.float64,
                        )
                        / 2.0
                    )
                )
                ranges.append(
                    Periodic1DBandEquivalenceRangeAnalysis(
                        maximum_range=maximum_range,
                        ordinary_omitted_block_l2_norm=omitted,
                        truncation_hamiltonian_maximum_error=truncation_matrix,
                        total_hamiltonian_maximum_error=total_matrix,
                        truncation_spectral_maximum_error=truncation_spectral,
                        total_spectral_maximum_error=total_spectral,
                    )
                )
            nyquist_block = blocks[0]
            analytic = _independent_bessel_j0(2.0 * amplitude)
            points.append(
                Periodic1DBandEquivalencePointAnalysis(
                    amplitude=amplitude,
                    maximum_band_defect=float(
                        np.max(
                            np.abs(
                                np.linalg.eigvalsh(construction_values)
                                - np.asarray((-1.0, 1.0), dtype=np.float64)
                            )
                        )
                    ),
                    discrete_maximum_correlation=correlation,
                    analytic_maximum_correlation=analytic,
                    correlation_quadrature_defect=abs(correlation - analytic),
                    global_alignment_angle=angle,
                    optimal_splitting_scale=optimal_scale,
                    irreducible_operator_squared_loss=squared_loss,
                    minimum_operator_threshold=math.sqrt(squared_loss),
                    exact_spectrum_joint_operator_threshold=math.sqrt(
                        max(0.0, 2.0 * (1.0 - correlation))
                    ),
                    cyclic_nyquist_power=float(
                        np.sum(np.abs(nyquist_block) ** 2) / 2.0
                    ),
                    reconstruction_maximum_frobenius_error=float(
                        np.max(
                            np.linalg.norm(
                                reconstructed - construction_values,
                                axis=(1, 2),
                            )
                        )
                    ),
                    interpolation_hamiltonian_maximum_error=interpolation_matrix,
                    interpolation_spectral_maximum_error=interpolation_spectral,
                    hopping_powers=tuple(
                        Periodic1DBandEquivalenceHoppingPower(
                            displacement=int(displacement),
                            normalized_squared_frobenius_norm=float(
                                np.sum(np.abs(block) ** 2) / 2.0
                            ),
                        )
                        for displacement, block in zip(
                            representatives, blocks, strict=True
                        )
                    ),
                    ranges=tuple(ranges),
                )
            )
        return Periodic1DBandEquivalenceLocalityAnalysis(request, tuple(points))


def _flat_attacked_values(
    coordinates: np.ndarray[tuple[int], np.dtype[np.float64]], amplitude: float
) -> np.ndarray[tuple[int, int, int], np.dtype[np.complex128]]:
    theta = amplitude * np.sin(2.0 * np.pi * coordinates)
    rotations = np.empty((coordinates.size, 2, 2), dtype=np.float64)
    rotations[:, 0, 0] = np.cos(theta)
    rotations[:, 0, 1] = -np.sin(theta)
    rotations[:, 1, 0] = np.sin(theta)
    rotations[:, 1, 1] = np.cos(theta)
    diagonal = np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=np.float64)
    return np.asarray(
        np.einsum(
            "nri,rs,nsj->nij",
            rotations,
            diagonal,
            rotations,
            optimize=True,
        ),
        dtype=np.complex128,
    )


def _direct_fourier_blocks(
    coordinates: np.ndarray[tuple[int], np.dtype[np.float64]],
    matrices: np.ndarray[tuple[int, int, int], np.dtype[np.complex128]],
    representatives: np.ndarray[tuple[int], np.dtype[np.int64]],
) -> np.ndarray[tuple[int, int, int], np.dtype[np.complex128]]:
    phases = np.exp(-2.0j * np.pi * np.outer(coordinates, representatives))
    return np.asarray(
        np.einsum("kr,kij->rij", phases, matrices, optimize=True)
        / float(coordinates.size),
        dtype=np.complex128,
    )


def _evaluate_blocks(
    coordinates: np.ndarray[tuple[int], np.dtype[np.float64]],
    representatives: np.ndarray[tuple[int], np.dtype[np.int64]],
    blocks: np.ndarray[tuple[int, int, int], np.dtype[np.complex128]],
) -> np.ndarray[tuple[int, int, int], np.dtype[np.complex128]]:
    phases = np.exp(2.0j * np.pi * np.outer(coordinates, representatives))
    return np.asarray(
        np.einsum("kr,rij->kij", phases, blocks, optimize=True),
        dtype=np.complex128,
    )


def _errors(
    candidate: np.ndarray[tuple[int, int, int], np.dtype[np.complex128]],
    reference: np.ndarray[tuple[int, int, int], np.dtype[np.complex128]],
) -> tuple[float, float]:
    difference = candidate - reference
    return (
        float(np.max(np.linalg.norm(difference, axis=(1, 2))) / math.sqrt(2.0)),
        float(
            np.max(
                np.abs(np.linalg.eigvalsh(candidate) - np.linalg.eigvalsh(reference))
            )
        ),
    )


def _independent_bessel_j0(argument: float) -> float:
    total = 0.0
    factorial = 1
    power = 1.0
    half = argument / 2.0
    for order in range(64):
        if order > 0:
            factorial *= order
            power *= -(half * half)
        term = power / float(factorial * factorial)
        total += term
        if abs(term) <= math.ulp(1.0) * max(1.0, abs(total)):
            return total
    raise FloatingPointError("independent Bessel series did not converge")


__all__ = ["Periodic1DBandEquivalenceLocalityIndependentReferenceAnalyzer"]
