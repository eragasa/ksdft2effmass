"""Analytic periodic-1D higher-rank model owned by the calculation producer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, final

import numpy as np
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray, RealArray

from ksdft2effmass.periodic import Periodic1DModel, PeriodicModelRole

from .configuration import Periodic1DHigherRankAlignmentConfiguration


def _finite_reduced_coordinates(value: RealArray, name: str) -> RealArray:
    normalized = NumpyImmutableArrayConstructor(
        value,
        name,
        np.dtype(np.float64),
    ).execute()
    if normalized.ndim != 1 or normalized.size == 0:
        raise ValueError(f"{name} must be a nonempty one-dimensional array")
    return normalized


@final
@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DHigherRankAnalyticCase(Periodic1DModel):
    """Represent one exact analytic parent family and synthetic frame attack.

    Reduced coordinates lie in one reciprocal period. The ambient basis is the
    ordered direct sum of ``retained_rank`` retained orbitals followed by the same
    number of exterior orbitals. Energies are dimensionless and use the fixed zero
    declared by the calculation request.
    """

    MODEL_FAMILY_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic1d.higher-rank-analytic-givens-family.v1"
    )

    retained_rank: int
    circuit_depth: int
    reference_frame: ComplexArray = field(repr=False)
    endpoint_sewing_map: ComplexArray = field(repr=False)

    def __post_init__(self) -> None:
        """Validate the frozen case inventory and exact analytic geometry."""
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if (
            self.retained_rank
            not in Periodic1DHigherRankAlignmentConfiguration.RETAINED_RANKS
        ):
            raise ValueError("retained_rank is not in the frozen inventory")
        if type(self.circuit_depth) is not int:
            raise TypeError("circuit_depth must be a built-in integer")
        if (
            self.circuit_depth
            not in Periodic1DHigherRankAlignmentConfiguration.CIRCUIT_DEPTHS
        ):
            raise ValueError("circuit_depth is not in the frozen inventory")
        reference = NumpyImmutableArrayConstructor(
            self.reference_frame,
            "reference_frame",
            np.dtype(np.complex128),
        ).execute()
        sewing = NumpyImmutableArrayConstructor(
            self.endpoint_sewing_map,
            "endpoint_sewing_map",
            np.dtype(np.complex128),
        ).execute()
        ambient = 2 * self.retained_rank
        if reference.shape != (ambient, self.retained_rank):
            raise ValueError("reference_frame must have shape (2r, r)")
        if sewing.shape != (ambient, ambient):
            raise ValueError("endpoint_sewing_map must have shape (2r, 2r)")
        expected_reference = np.zeros(
            (ambient, self.retained_rank), dtype=np.complex128
        )
        expected_reference[: self.retained_rank] = np.eye(
            self.retained_rank, dtype=np.complex128
        )
        if not np.array_equal(reference, expected_reference):
            raise ValueError(
                "reference_frame must be the frozen retained-coordinate embedding"
            )
        if not np.array_equal(sewing, np.eye(ambient, dtype=np.complex128)):
            raise ValueError(
                "endpoint_sewing_map must be the identity for the analytic family"
            )
        object.__setattr__(self, "reference_frame", reference)
        object.__setattr__(self, "endpoint_sewing_map", sewing)

    @property
    def model_id(self) -> str:
        """Return the stable analytic-family and rank/depth case identity."""
        return (
            f"{self.MODEL_FAMILY_IDENTITY}:"
            f"r{self.retained_rank:02d}-L{self.circuit_depth:02d}"
        )

    @property
    def model_role(self) -> PeriodicModelRole:
        """Classify the analytic family as a controlled toy model."""
        return PeriodicModelRole.TOY

    @property
    def ambient_dimension(self) -> int:
        """Return the parent-space dimension ``2r``."""
        return 2 * self.retained_rank

    def retained_energies(self, reduced_coordinates: RealArray) -> RealArray:
        """Return the ordered retained energies on supplied reduced coordinates."""
        coordinates = _finite_reduced_coordinates(
            reduced_coordinates, "reduced_coordinates"
        )
        k = 2.0 * np.pi * coordinates
        c = 0.75 * np.cos(k) + 0.25 * np.cos(2.0 * k)
        orbital = np.arange(self.retained_rank, dtype=np.float64)
        normalized_orbital = (2.0 * orbital - self.retained_rank + 1.0) / (
            self.retained_rank - 1.0
        )
        values = (
            0.4 * normalized_orbital[None, :]
            + 0.25 * (1.0 + 0.2 * normalized_orbital[None, :]) * c[:, None]
        )
        return np.asarray(values, dtype=np.float64)

    def exterior_energies(self, reduced_coordinates: RealArray) -> RealArray:
        """Return the ordered exterior energies on supplied reduced coordinates."""
        coordinates = _finite_reduced_coordinates(
            reduced_coordinates, "reduced_coordinates"
        )
        k = 2.0 * np.pi * coordinates
        c = 0.75 * np.cos(k) + 0.25 * np.cos(2.0 * k)
        orbital = np.arange(self.retained_rank, dtype=np.float64)
        normalized_orbital = (2.0 * orbital - self.retained_rank + 1.0) / (
            self.retained_rank - 1.0
        )
        values = 3.0 + 0.3 * normalized_orbital[None, :] + 0.1 * c[:, None]
        return np.asarray(values, dtype=np.float64)

    def parent_hamiltonians(self, reduced_coordinates: RealArray) -> ComplexArray:
        """Return parent Hamiltonian matrices in the ordered ambient basis."""
        retained = self.retained_energies(reduced_coordinates)
        exterior = self.exterior_energies(reduced_coordinates)
        diagonal = np.concatenate((retained, exterior), axis=1)
        identity = np.eye(self.ambient_dimension, dtype=np.complex128)
        return np.asarray(
            diagonal[:, :, None] * identity[None, :, :], dtype=np.complex128
        )

    def reference_frames(self, reduced_coordinates: RealArray) -> ComplexArray:
        """Return the constant analytic retained frame on supplied coordinates."""
        coordinates = _finite_reduced_coordinates(
            reduced_coordinates, "reduced_coordinates"
        )
        return np.asarray(
            np.broadcast_to(
                self.reference_frame,
                (coordinates.size,) + self.reference_frame.shape,
            ),
            dtype=np.complex128,
        ).copy()

    def exact_reduced_hamiltonians(
        self,
        reduced_coordinates: RealArray,
    ) -> ComplexArray:
        """Return the exact retained operator in the analytic reference frame."""
        energies = self.retained_energies(reduced_coordinates)
        identity = np.eye(self.retained_rank, dtype=np.complex128)
        return np.asarray(
            energies[:, :, None] * identity[None, :, :], dtype=np.complex128
        )

    @property
    def exact_attack_angle_maximum(self) -> float:
        """Return the protocol's analytic continuum maximum Givens angle."""
        q = (np.sqrt(41.0) - 3.0) / 8.0
        harmonic_maximum = np.sqrt(1.0 - q**2) * (0.75 + 0.5 * q)
        return float(
            0.35
            * (1.0 + 0.15 * (self.retained_rank - 2.0) / (self.retained_rank - 1.0))
            * harmonic_maximum
        )

    def sampled_attack_angle_maximum(self, reduced_coordinates: RealArray) -> float:
        """Return the sampled maximum absolute Givens angle on one mesh."""
        coordinates = _finite_reduced_coordinates(
            reduced_coordinates, "reduced_coordinates"
        )
        k = 2.0 * np.pi * coordinates
        maximum = 0.0
        for layer_index in range(1, self.circuit_depth + 1):
            layer_harmonic = 0.75 * np.sin(k) + 0.25 * ((-1.0) ** layer_index) * np.sin(
                2.0 * k
            )
            for pair_index in range(1, self.retained_rank):
                normalized_pair = (2.0 * pair_index - self.retained_rank) / (
                    self.retained_rank - 1.0
                )
                angles = (
                    0.35
                    * (-1.0) ** (layer_index + pair_index)
                    * (1.0 + 0.15 * normalized_pair)
                    * layer_harmonic
                )
                maximum = max(maximum, float(np.max(np.abs(angles))))
        return maximum

    def gauge_unitaries(self, reduced_coordinates: RealArray) -> ComplexArray:
        """Return the frozen depth-``L`` nearest-neighbor gauge circuit."""
        coordinates = _finite_reduced_coordinates(
            reduced_coordinates, "reduced_coordinates"
        )
        k = 2.0 * np.pi * coordinates
        rank = self.retained_rank
        gauges = np.broadcast_to(
            np.eye(rank, dtype=np.complex128),
            (coordinates.size, rank, rank),
        ).copy()
        for layer_index in range(1, self.circuit_depth + 1):
            layer_harmonic = 0.75 * np.sin(k) + 0.25 * ((-1.0) ** layer_index) * np.sin(
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
                theta = (
                    0.35
                    * (-1.0) ** (layer_index + pair_index)
                    * (1.0 + 0.15 * normalized_pair)
                    * layer_harmonic
                )
                cosine = np.cos(theta)
                sine = np.sin(theta)
                layer[:, left, left] = cosine
                layer[:, left, left + 1] = -sine
                layer[:, left + 1, left] = sine
                layer[:, left + 1, left + 1] = cosine
            gauges = gauges @ layer
        return np.asarray(gauges, dtype=np.complex128)

    def attacked_frames(self, reduced_coordinates: RealArray) -> ComplexArray:
        """Return analytic retained frames after the right-acting gauge attack."""
        return np.asarray(
            self.reference_frames(reduced_coordinates)
            @ self.gauge_unitaries(reduced_coordinates),
            dtype=np.complex128,
        )

    def attacked_reduced_hamiltonians(
        self,
        reduced_coordinates: RealArray,
    ) -> ComplexArray:
        """Return reduced Hamiltonians represented in the attacked frame."""
        gauge = self.gauge_unitaries(reduced_coordinates)
        exact = self.exact_reduced_hamiltonians(reduced_coordinates)
        return np.asarray(
            np.swapaxes(gauge.conjugate(), -1, -2) @ exact @ gauge,
            dtype=np.complex128,
        )


@final
class Periodic1DHigherRankAnalyticCaseConstructor:
    """Construct one frozen analytic rank/depth case without hidden collaborators."""

    __slots__ = ("_retained_rank", "_circuit_depth")

    def __init__(self, *, retained_rank: int, circuit_depth: int) -> None:
        """Bind the exact case selected by a calculation request."""
        self._retained_rank = retained_rank
        self._circuit_depth = circuit_depth

    def execute(self) -> Periodic1DHigherRankAnalyticCase:
        """Return the immutable analytic case definition."""
        rank = self._retained_rank
        if type(rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        ambient = 2 * rank
        frame = np.zeros((ambient, rank), dtype=np.complex128)
        frame[:rank] = np.eye(rank, dtype=np.complex128)
        return Periodic1DHigherRankAnalyticCase(
            retained_rank=rank,
            circuit_depth=self._circuit_depth,
            reference_frame=frame,
            endpoint_sewing_map=np.eye(ambient, dtype=np.complex128),
        )


__all__ = [
    "Periodic1DHigherRankAnalyticCase",
    "Periodic1DHigherRankAnalyticCaseConstructor",
]
