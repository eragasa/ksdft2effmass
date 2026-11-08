"""Calculation-owned analytic Givens transformation composition."""

from __future__ import annotations

import math

import numpy as np

from ksdft2effmass.gauge_transformation import (
    FiniteRankAlternatingNearestNeighborGivensCircuitConstructor,
)
from ksdft2effmass.periodic1d.gauge_transformation import (
    Periodic1DFourierGivensGaugeTransformation,
)


class AnalyticGaugeTransformationConstructor:
    """Construct the explicitly selected analytic angle field from generic mechanics."""

    __slots__ = ("_retained_rank", "_circuit_depth")

    def __init__(self, *, retained_rank: int, circuit_depth: int) -> None:
        if type(retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if retained_rank < 3:
            raise ValueError(
                "retained_rank must be at least three for this calculation"
            )
        if type(circuit_depth) is not int:
            raise TypeError("circuit_depth must be a built-in integer")
        if circuit_depth < 1:
            raise ValueError("circuit_depth must be positive")
        self._retained_rank = retained_rank
        self._circuit_depth = circuit_depth

    def execute(self) -> Periodic1DFourierGivensGaugeTransformation:
        """Return the analytic transformation with explicit ordered Fourier coefficients."""
        rank = self._retained_rank
        depth = self._circuit_depth
        circuit = FiniteRankAlternatingNearestNeighborGivensCircuitConstructor(
            represented_rank=rank,
            layer_count=depth,
        ).execute()
        sine_rows: list[tuple[float, float]] = []
        for layer_index in range(1, depth + 1):
            first_index = 0 if layer_index % 2 == 1 else 1
            for left in range(first_index, rank - 1, 2):
                pair_index = left + 1
                normalized_pair = (2.0 * pair_index - rank) / (rank - 1.0)
                amplitude = (
                    0.35
                    * (-1.0) ** (layer_index + pair_index)
                    * (1.0 + 0.15 * normalized_pair)
                )
                sine_rows.append(
                    (
                        0.75 * amplitude,
                        0.25 * ((-1.0) ** layer_index) * amplitude,
                    )
                )
        q = (math.sqrt(41.0) - 3.0) / 8.0
        harmonic_maximum = math.sqrt(1.0 - q**2) * (0.75 + 0.5 * q)
        angle_maximum = (
            0.35 * (1.0 + 0.15 * (rank - 2.0) / (rank - 1.0)) * harmonic_maximum
        )
        rotation_count = circuit.rotation_count
        return Periodic1DFourierGivensGaugeTransformation(
            transformation_identifier=(
                "periodic1d-rankN-analytic-fourier-givens-transformation.v1:"
                f"r{rank:02d}-L{depth:02d}"
            ),
            circuit=circuit,
            continuum_angle_maximum_bound=float(angle_maximum),
            constant_angles=np.zeros(rotation_count, dtype=np.float64),
            cosine_coefficients=np.zeros((rotation_count, 2), dtype=np.float64),
            sine_coefficients=np.asarray(sine_rows, dtype=np.float64),
        )


__all__ = ["AnalyticGaugeTransformationConstructor"]
