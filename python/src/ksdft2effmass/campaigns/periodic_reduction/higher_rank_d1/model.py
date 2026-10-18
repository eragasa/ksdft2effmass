"""Canonical analytic fields for the higher-rank D1 P0/G0 construction."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.numerics.numpy.validation import (
    immutable_complex128_array,
    immutable_float64_array,
    validate_immutable_complex128_array,
    validate_immutable_float64_array,
)

from ._validation import require_array_shape


@dataclass(frozen=True, slots=True, eq=False)
class HigherRankD1SampledFields:
    """Retain one immutable directly sampled analytic D1 field collection."""

    rank: int
    depth: int
    reduced_coordinates: Float64Array = field(repr=False)
    retained_energies: Float64Array = field(repr=False)
    exterior_energies: Float64Array = field(repr=False)
    parent_operators: Complex128Array = field(repr=False)
    reference_frames: Complex128Array = field(repr=False)
    gauges: Complex128Array = field(repr=False)
    candidate_frames: Complex128Array = field(repr=False)
    reference_operators: Complex128Array = field(repr=False)
    attacked_operators: Complex128Array = field(repr=False)

    def __post_init__(self) -> None:
        """Validate exact shapes, storage, and defining construction identities."""
        if type(self.rank) is not int or self.rank < 3:
            raise ValueError("rank must be a built-in integer at least three")
        if type(self.depth) is not int or self.depth < 1:
            raise ValueError("depth must be a positive built-in integer")
        validate_immutable_float64_array(
            self.reduced_coordinates, "reduced_coordinates"
        )
        for name, float_value in (
            ("retained_energies", self.retained_energies),
            ("exterior_energies", self.exterior_energies),
        ):
            validate_immutable_float64_array(float_value, name)
        for name, complex_value in (
            ("parent_operators", self.parent_operators),
            ("reference_frames", self.reference_frames),
            ("gauges", self.gauges),
            ("candidate_frames", self.candidate_frames),
            ("reference_operators", self.reference_operators),
            ("attacked_operators", self.attacked_operators),
        ):
            validate_immutable_complex128_array(complex_value, name)
        count = int(self.reduced_coordinates.size)
        rank = self.rank
        ambient = 2 * rank
        require_array_shape(self.retained_energies, (count, rank), "retained_energies")
        require_array_shape(self.exterior_energies, (count, rank), "exterior_energies")
        require_array_shape(
            self.parent_operators,
            (count, ambient, ambient),
            "parent_operators",
        )
        require_array_shape(
            self.reference_frames, (count, ambient, rank), "reference_frames"
        )
        require_array_shape(self.gauges, (count, rank, rank), "gauges")
        require_array_shape(
            self.candidate_frames, (count, ambient, rank), "candidate_frames"
        )
        require_array_shape(
            self.reference_operators,
            (count, rank, rank),
            "reference_operators",
        )
        require_array_shape(
            self.attacked_operators, (count, rank, rank), "attacked_operators"
        )
        expected_candidate = self.reference_frames @ self.gauges
        if not np.array_equal(self.candidate_frames, expected_candidate):
            raise ValueError("candidate_frames must equal reference_frames @ gauges")
        expected_attacked = (
            np.swapaxes(self.gauges.conjugate(), -1, -2)
            @ self.reference_operators
            @ self.gauges
        )
        if not np.array_equal(self.attacked_operators, expected_attacked):
            raise ValueError("attacked_operators must equal G^dagger D G")


class HigherRankD1ModelConstructor:
    """Construct the exact finite-rank P0/G0 model without eigensolver selection."""

    __slots__ = ()

    @staticmethod
    def construction_coordinates(mesh_size: int) -> Float64Array:
        """Return the immutable odd centered half-open reduced-coordinate mesh."""
        if type(mesh_size) is not int:
            raise TypeError("mesh_size must be a built-in int")
        if mesh_size <= 0 or mesh_size % 2 == 0:
            raise ValueError("mesh_size must be positive and odd")
        values = np.asarray(
            -0.5 + np.arange(mesh_size, dtype=np.float64) / float(mesh_size),
            dtype=np.float64,
        )
        return immutable_float64_array(values, "construction_coordinates")

    @staticmethod
    def positive_endpoint_coordinates() -> Float64Array:
        """Return the immutable singleton direct positive endpoint."""
        values = np.asarray((0.5,), dtype=np.float64)
        return immutable_float64_array(values, "positive_endpoint_coordinates")

    @staticmethod
    def evaluation_coordinates(mesh_size: int) -> Float64Array:
        """Return the immutable shifted odd withheld reduced-coordinate mesh."""
        if type(mesh_size) is not int:
            raise TypeError("mesh_size must be a built-in int")
        if mesh_size <= 0 or mesh_size % 2 == 0:
            raise ValueError("mesh_size must be positive and odd")
        values = np.asarray(
            -0.5 + (np.arange(mesh_size, dtype=np.float64) + 0.5) / float(mesh_size),
            dtype=np.float64,
        )
        return immutable_float64_array(values, "evaluation_coordinates")

    def execute(
        self,
        rank: int,
        depth: int,
        reduced_coordinates: Float64Array,
    ) -> HigherRankD1SampledFields:
        """Return all canonical analytic fields on immutable reduced coordinates."""
        if type(rank) is not int or rank < 3:
            raise ValueError("rank must be a built-in integer at least three")
        if type(depth) is not int or depth < 1:
            raise ValueError("depth must be a positive built-in integer")
        validate_immutable_float64_array(reduced_coordinates, "reduced_coordinates")
        if reduced_coordinates.ndim != 1 or reduced_coordinates.size == 0:
            raise ValueError("reduced_coordinates must be a nonempty vector")

        count = int(reduced_coordinates.size)
        phase = 2.0 * np.pi * reduced_coordinates
        orbital = np.asarray(
            tuple(
                (2.0 * float(index) - rank - 1.0) / float(rank - 1)
                for index in range(1, rank + 1)
            ),
            dtype=np.float64,
        )
        harmonic = 0.75 * np.cos(phase) + 0.25 * np.cos(2.0 * phase)
        retained = (
            0.40 * orbital[None, :]
            + 0.25 * (1.0 + 0.20 * orbital[None, :]) * harmonic[:, None]
        )
        exterior = 3.00 + 0.30 * orbital[None, :] + 0.10 * harmonic[:, None]
        reference_operators = np.zeros((count, rank, rank), dtype=np.complex128)
        diagonal = np.arange(rank)
        reference_operators[:, diagonal, diagonal] = retained
        parent = np.zeros((count, 2 * rank, 2 * rank), dtype=np.complex128)
        parent[:, diagonal, diagonal] = retained
        parent[:, rank + diagonal, rank + diagonal] = exterior
        reference_frames = np.zeros((count, 2 * rank, rank), dtype=np.complex128)
        reference_frames[:, :rank, :] = np.eye(rank, dtype=np.complex128)
        gauges = self._gauges(rank, depth, phase)
        candidate_frames = reference_frames @ gauges
        attacked = (
            np.swapaxes(gauges.conjugate(), -1, -2) @ reference_operators @ gauges
        )
        return HigherRankD1SampledFields(
            rank=rank,
            depth=depth,
            reduced_coordinates=immutable_float64_array(
                reduced_coordinates, "reduced_coordinates"
            ),
            retained_energies=immutable_float64_array(retained, "retained_energies"),
            exterior_energies=immutable_float64_array(exterior, "exterior_energies"),
            parent_operators=immutable_complex128_array(parent, "parent_operators"),
            reference_frames=immutable_complex128_array(
                reference_frames, "reference_frames"
            ),
            gauges=immutable_complex128_array(gauges, "gauges"),
            candidate_frames=immutable_complex128_array(
                candidate_frames, "candidate_frames"
            ),
            reference_operators=immutable_complex128_array(
                reference_operators, "reference_operators"
            ),
            attacked_operators=immutable_complex128_array(
                attacked, "attacked_operators"
            ),
        )

    @staticmethod
    def exact_attack_angle_bound(rank: int) -> float:
        """Return the selected rank-specific continuum angle certificate."""
        if type(rank) is not int or rank < 3:
            raise ValueError("rank must be a built-in integer at least three")
        q = (math.sqrt(41.0) - 3.0) / 8.0
        maximum_harmonic = math.sqrt(1.0 - q**2) * (0.75 + q / 2.0)
        return (
            0.35 * (1.0 + 0.15 * float(rank - 2) / float(rank - 1)) * maximum_harmonic
        )

    @staticmethod
    def sampled_attack_angle_maximum(
        rank: int,
        depth: int,
        reduced_coordinates: Float64Array,
    ) -> float:
        """Return the maximum immutable-grid angle without constructing matrices."""
        if type(rank) is not int or rank < 3:
            raise ValueError("rank must be a built-in integer at least three")
        if type(depth) is not int or depth < 1:
            raise ValueError("depth must be a positive built-in integer")
        validate_immutable_float64_array(reduced_coordinates, "reduced_coordinates")
        phase = 2.0 * np.pi * reduced_coordinates
        maximum = 0.0
        for layer in range(1, depth + 1):
            harmonic = 0.75 * np.sin(phase) + 0.25 * ((-1.0) ** layer) * np.sin(
                2.0 * phase
            )
            for first in range(1, rank):
                if first % 2 != layer % 2:
                    continue
                coordinate = (2.0 * float(first) - rank) / float(rank - 1)
                angle = (
                    0.35
                    * ((-1.0) ** (layer + first))
                    * (1.0 + 0.15 * coordinate)
                    * harmonic
                )
                maximum = max(maximum, float(np.max(np.abs(angle))))
        return maximum

    @staticmethod
    def _gauges(rank: int, depth: int, phase: Float64Array) -> Complex128Array:
        count = int(phase.size)
        gauges = np.broadcast_to(
            np.eye(rank, dtype=np.complex128), (count, rank, rank)
        ).copy()
        for layer in range(1, depth + 1):
            harmonic = 0.75 * np.sin(phase) + 0.25 * ((-1.0) ** layer) * np.sin(
                2.0 * phase
            )
            for first in range(1, rank):
                if first % 2 != layer % 2:
                    continue
                coordinate = (2.0 * float(first) - rank) / float(rank - 1)
                angle = (
                    0.35
                    * ((-1.0) ** (layer + first))
                    * (1.0 + 0.15 * coordinate)
                    * harmonic
                )
                cosine = np.cos(angle)
                sine = np.sin(angle)
                rotation = np.broadcast_to(
                    np.eye(rank, dtype=np.complex128), (count, rank, rank)
                ).copy()
                left = first - 1
                right = first
                rotation[:, left, left] = cosine
                rotation[:, left, right] = -sine
                rotation[:, right, left] = sine
                rotation[:, right, right] = cosine
                gauges = gauges @ rotation
        return np.asarray(gauges, dtype=np.complex128)


__all__ = ["HigherRankD1ModelConstructor", "HigherRankD1SampledFields"]
