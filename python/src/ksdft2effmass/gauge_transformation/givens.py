"""Dimension-neutral construction of sampled finite-rank Givens circuits."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

import numpy as np
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor
from projectkoios.physkit.numerics.typing.numpy.arrays import RealArray

from .finite_rank import SampledFiniteRankGaugeTransformation


@dataclass(frozen=True, slots=True)
class FiniteRankGivensRotation:
    """Identify one ordered real Givens rotation within a finite basis."""

    first_index: int
    second_index: int

    def __post_init__(self) -> None:
        if type(self.first_index) is not int:
            raise TypeError("first_index must be a built-in integer")
        if type(self.second_index) is not int:
            raise TypeError("second_index must be a built-in integer")
        if self.first_index < 0:
            raise ValueError("first_index must be nonnegative")
        if self.second_index <= self.first_index:
            raise ValueError("second_index must be greater than first_index")


@dataclass(frozen=True, slots=True)
class FiniteRankGivensLayer:
    """Retain one ordered layer of pairwise-disjoint Givens rotations."""

    rotations: tuple[FiniteRankGivensRotation, ...]

    def __post_init__(self) -> None:
        if type(self.rotations) is not tuple:
            raise TypeError("rotations must be a tuple")
        if len(self.rotations) == 0:
            raise ValueError("rotations must be nonempty")
        occupied: set[int] = set()
        for rotation in self.rotations:
            if type(rotation) is not FiniteRankGivensRotation:
                raise TypeError(
                    "rotations must contain FiniteRankGivensRotation values"
                )
            indices = {rotation.first_index, rotation.second_index}
            if not occupied.isdisjoint(indices):
                raise ValueError("rotations within one layer must be pairwise disjoint")
            occupied.update(indices)


@dataclass(frozen=True, slots=True)
class FiniteRankGivensCircuit:
    """Retain an ordered finite-rank Givens circuit without angle policy."""

    represented_rank: int
    layers: tuple[FiniteRankGivensLayer, ...]

    def __post_init__(self) -> None:
        if type(self.represented_rank) is not int:
            raise TypeError("represented_rank must be a built-in integer")
        if self.represented_rank < 2:
            raise ValueError("represented_rank must be at least two")
        if type(self.layers) is not tuple:
            raise TypeError("layers must be a tuple")
        if len(self.layers) == 0:
            raise ValueError("layers must be nonempty")
        for layer in self.layers:
            if type(layer) is not FiniteRankGivensLayer:
                raise TypeError("layers must contain FiniteRankGivensLayer values")
            for rotation in layer.rotations:
                if rotation.second_index >= self.represented_rank:
                    raise ValueError(
                        "rotation index must be smaller than represented_rank"
                    )

    @property
    def rotation_count(self) -> int:
        """Return the total number of ordered rotations in the circuit."""
        return sum(len(layer.rotations) for layer in self.layers)


@final
class FiniteRankAlternatingNearestNeighborGivensCircuitConstructor:
    """Construct an alternating nearest-neighbor circuit of supplied depth."""

    __slots__ = ("_represented_rank", "_layer_count")

    def __init__(self, *, represented_rank: int, layer_count: int) -> None:
        if type(represented_rank) is not int:
            raise TypeError("represented_rank must be a built-in integer")
        if represented_rank < 2:
            raise ValueError("represented_rank must be at least two")
        if type(layer_count) is not int:
            raise TypeError("layer_count must be a built-in integer")
        if layer_count < 1:
            raise ValueError("layer_count must be positive")
        self._represented_rank = represented_rank
        self._layer_count = layer_count

    def execute(self) -> FiniteRankGivensCircuit:
        """Return the ordered nonempty layers of the alternating circuit."""
        rank = self._represented_rank
        layers: list[FiniteRankGivensLayer] = []
        for layer_index in range(1, self._layer_count + 1):
            first_index = 0 if layer_index % 2 == 1 else 1
            rotations = tuple(
                FiniteRankGivensRotation(left, left + 1)
                for left in range(first_index, rank - 1, 2)
            )
            if rotations:
                layers.append(FiniteRankGivensLayer(rotations=rotations))
        return FiniteRankGivensCircuit(
            represented_rank=rank,
            layers=tuple(layers),
        )


@final
class FiniteRankGivensCircuitTransformationConstructor:
    """Construct one sampled unitary field from a circuit and supplied angles."""

    __slots__ = ("_circuit", "_angle_samples")

    def __init__(
        self,
        *,
        circuit: FiniteRankGivensCircuit,
        angle_samples: RealArray,
    ) -> None:
        if type(circuit) is not FiniteRankGivensCircuit:
            raise TypeError("circuit must be FiniteRankGivensCircuit")
        admitted_angles = NumpyImmutableArrayConstructor(
            angle_samples,
            "angle_samples",
            np.dtype(np.float64),
        ).execute()
        if admitted_angles.ndim != 2 or admitted_angles.shape[0] == 0:
            raise ValueError("angle_samples must have shape (N, rotation_count)")
        if admitted_angles.shape[1] != circuit.rotation_count:
            raise ValueError("angle_samples columns must match circuit rotation order")
        self._circuit = circuit
        self._angle_samples = admitted_angles

    def execute(self) -> SampledFiniteRankGaugeTransformation:
        """Return the ordered sampled transformation represented by the circuit."""
        circuit = self._circuit
        angles = self._angle_samples
        rank = circuit.represented_rank
        values = np.broadcast_to(
            np.eye(rank, dtype=np.complex128),
            (angles.shape[0], rank, rank),
        ).copy()
        angle_index = 0
        for layer_definition in circuit.layers:
            layer = np.broadcast_to(
                np.eye(rank, dtype=np.complex128),
                (angles.shape[0], rank, rank),
            ).copy()
            for rotation in layer_definition.rotations:
                theta = angles[:, angle_index]
                angle_index += 1
                cosine = np.cos(theta)
                sine = np.sin(theta)
                first = rotation.first_index
                second = rotation.second_index
                layer[:, first, first] = cosine
                layer[:, first, second] = -sine
                layer[:, second, first] = sine
                layer[:, second, second] = cosine
            values = values @ layer
        return SampledFiniteRankGaugeTransformation(
            NumpyImmutableArrayConstructor(
                np.asarray(values, dtype=np.complex128),
                "givens_circuit_unitaries",
                np.dtype(np.complex128),
            ).execute()
        )


__all__ = [
    "FiniteRankAlternatingNearestNeighborGivensCircuitConstructor",
    "FiniteRankGivensCircuit",
    "FiniteRankGivensCircuitTransformationConstructor",
    "FiniteRankGivensLayer",
    "FiniteRankGivensRotation",
]
