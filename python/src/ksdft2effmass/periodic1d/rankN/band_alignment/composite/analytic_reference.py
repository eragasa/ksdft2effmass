"""Independent analytic model used by bounded rank-N reference actions."""

from __future__ import annotations

from typing import final

import numpy as np
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray, RealArray


@final
class _Periodic1DRankNAnalyticReferenceModel:
    """Evaluate the frozen analytic family without producer model actions."""

    __slots__ = ("_retained_rank", "_circuit_depth")

    def __init__(self, retained_rank: int, circuit_depth: int) -> None:
        if type(retained_rank) is not int or retained_rank <= 1:
            raise ValueError(
                "retained_rank must be a built-in integer greater than one"
            )
        if type(circuit_depth) is not int or circuit_depth <= 0:
            raise ValueError("circuit_depth must be a positive built-in integer")
        self._retained_rank = retained_rank
        self._circuit_depth = circuit_depth

    @property
    def retained_rank(self) -> int:
        """Return the represented retained-space dimension."""
        return self._retained_rank

    @property
    def circuit_depth(self) -> int:
        """Return the analytic nearest-neighbor circuit depth."""
        return self._circuit_depth

    def energy_parameters(self) -> tuple[RealArray, RealArray, RealArray]:
        """Return orbital offsets and first- and second-harmonic amplitudes."""
        orbital = np.arange(self._retained_rank, dtype=np.float64)
        normalized = (2.0 * orbital - self._retained_rank + 1.0) / (
            self._retained_rank - 1.0
        )
        amplitude = 0.25 * (1.0 + 0.2 * normalized)
        return (
            np.asarray(0.4 * normalized, dtype=np.float64),
            np.asarray(0.75 * amplitude, dtype=np.float64),
            np.asarray(0.25 * amplitude, dtype=np.float64),
        )

    def exact_field(self, coordinates: RealArray) -> ComplexArray:
        """Return the exact diagonal retained Hamiltonian field."""
        offsets, first, second = self.energy_parameters()
        k = 2.0 * np.pi * coordinates
        energies = (
            offsets[None, :]
            + first[None, :] * np.cos(k)[:, None]
            + second[None, :] * np.cos(2.0 * k)[:, None]
        )
        identity = np.eye(self._retained_rank, dtype=np.complex128)
        return np.asarray(
            np.einsum("qi,ij->qij", energies, identity, optimize=True),
            dtype=np.complex128,
        )

    def gauge_unitaries(self, coordinates: RealArray) -> ComplexArray:
        """Return the analytic retained-space right-action gauge field."""
        rank = self._retained_rank
        k = 2.0 * np.pi * coordinates
        gauges = np.broadcast_to(
            np.eye(rank, dtype=np.complex128),
            (coordinates.size, rank, rank),
        ).copy()
        for layer_index in range(1, self._circuit_depth + 1):
            harmonic = 0.75 * np.sin(k) + 0.25 * ((-1.0) ** layer_index) * np.sin(
                2.0 * k
            )
            layer = np.broadcast_to(
                np.eye(rank, dtype=np.complex128),
                (coordinates.size, rank, rank),
            ).copy()
            first_index = 0 if layer_index % 2 == 1 else 1
            for left in range(first_index, rank - 1, 2):
                pair_index = left + 1
                normalized_pair = (2.0 * pair_index - rank) / (rank - 1.0)
                angle = (
                    0.35
                    * (-1.0) ** (layer_index + pair_index)
                    * (1.0 + 0.15 * normalized_pair)
                    * harmonic
                )
                cosine = np.cos(angle)
                sine = np.sin(angle)
                layer[:, left, left] = cosine
                layer[:, left, left + 1] = -sine
                layer[:, left + 1, left] = sine
                layer[:, left + 1, left + 1] = cosine
            gauges = gauges @ layer
        return np.asarray(gauges, dtype=np.complex128)


def _reduced_coordinates(mesh_size: int) -> RealArray:
    """Return the unshifted centered reduced-coordinate mesh."""
    if type(mesh_size) is not int or mesh_size <= 0:
        raise ValueError("mesh_size must be a positive built-in integer")
    return np.asarray(
        -0.5 + np.arange(mesh_size, dtype=np.float64) / mesh_size,
        dtype=np.float64,
    )
