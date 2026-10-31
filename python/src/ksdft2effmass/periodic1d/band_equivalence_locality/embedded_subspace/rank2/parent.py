"""Exact installed embedded-subspace/rank2 parent construction."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array

from .request import Periodic1DEmbeddedSubspaceRank2Request


def _immutable_complex(values: Complex128Array) -> Complex128Array:
    result = np.array(values, dtype=np.complex128, copy=True)
    result.setflags(write=False)
    return result


def _immutable_real(values: Float64Array) -> Float64Array:
    result = np.array(values, dtype=np.float64, copy=True)
    result.setflags(write=False)
    return result


@dataclass(frozen=True, slots=True, eq=False)
class _Periodic1DEmbeddedSubspaceRank2Parent:
    """Bind exact parent matrices, spectrum, and raw retained frames."""

    coordinates: Float64Array
    matrices: Complex128Array
    eigenvalues: Float64Array
    raw_retained_frames: Complex128Array
    minimum_external_gap: float

    def __post_init__(self) -> None:
        size = self.coordinates.size
        if self.coordinates.shape != (size,):
            raise ValueError("coordinates must be one-dimensional")
        if self.matrices.shape != (size, 4, 4):
            raise ValueError("parent matrices must have shape (N, 4, 4)")
        if self.eigenvalues.shape != (size, 4):
            raise ValueError("parent eigenvalues must have shape (N, 4)")
        if self.raw_retained_frames.shape != (size, 4, 2):
            raise ValueError("raw retained frames must have shape (N, 4, 2)")
        for array in (
            self.coordinates,
            self.matrices,
            self.eigenvalues,
            self.raw_retained_frames,
        ):
            if array.flags.writeable:
                raise ValueError("parent arrays must be read-only")
        if type(self.minimum_external_gap) is not float:
            raise TypeError("minimum_external_gap must be a built-in float")
        if not math.isfinite(self.minimum_external_gap):
            raise ValueError("minimum_external_gap must be finite")
        expected_gap = float(np.min(self.eigenvalues[:, 2] - self.eigenvalues[:, 1]))
        if self.minimum_external_gap != expected_gap:
            raise ValueError("minimum_external_gap must match the parent spectrum")


class _Periodic1DEmbeddedSubspaceRank2ParentConstructor:
    """Construct the fixed parent for one constructor-bound request."""

    __slots__ = ("_request",)

    def __init__(self, request: Periodic1DEmbeddedSubspaceRank2Request) -> None:
        if type(request) is not Periodic1DEmbeddedSubspaceRank2Request:
            raise TypeError("request must be Periodic1DEmbeddedSubspaceRank2Request")
        self._request = request

    def execute(self) -> _Periodic1DEmbeddedSubspaceRank2Parent:
        """Construct the exact normalized finite-range parent."""
        coordinates = np.asarray(
            self._request.construction_reduced_momenta(), dtype=np.float64
        )
        matrices = self._matrices(
            coordinates,
            self._request.parent_hopping_scale,
        )
        eigenvalues, eigenvectors = np.linalg.eigh(matrices)
        external_gap = float(np.min(eigenvalues[:, 2] - eigenvalues[:, 1]))
        return _Periodic1DEmbeddedSubspaceRank2Parent(
            coordinates=_immutable_real(coordinates),
            matrices=_immutable_complex(matrices),
            eigenvalues=_immutable_real(eigenvalues),
            raw_retained_frames=_immutable_complex(eigenvectors[:, :, :2]),
            minimum_external_gap=external_gap,
        )

    @staticmethod
    def _matrices(
        coordinates: Float64Array,
        parent_hopping_scale: float,
    ) -> Complex128Array:
        lower_onsite = np.asarray([[-1.20, 0.06], [0.06, -0.35]], dtype=np.complex128)
        upper_onsite = np.asarray([[1.00, 0.04], [0.04, 1.75]], dtype=np.complex128)
        lower_hopping = np.diag(np.asarray([0.15, -0.10])).astype(np.complex128)
        upper_hopping = np.diag(np.asarray([0.05, -0.04])).astype(np.complex128)
        coupling = np.diag(np.asarray([0.12, 0.10])).astype(np.complex128)
        matrices = np.empty((coordinates.size, 4, 4), dtype=np.complex128)
        for index, coordinate in enumerate(coordinates):
            phase = np.exp(2.0j * np.pi * coordinate)
            scaled_phase = parent_hopping_scale * phase
            matrices[index] = np.block(
                [
                    [
                        lower_onsite
                        + scaled_phase * lower_hopping
                        + scaled_phase.conjugate() * lower_hopping.conj().T,
                        scaled_phase * coupling,
                    ],
                    [
                        scaled_phase.conjugate() * coupling.conj().T,
                        upper_onsite
                        + scaled_phase * upper_hopping
                        + scaled_phase.conjugate() * upper_hopping.conj().T,
                    ],
                ]
            )
        return matrices


__all__: list[str] = []
