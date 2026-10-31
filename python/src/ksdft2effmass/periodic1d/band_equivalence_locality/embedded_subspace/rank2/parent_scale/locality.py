"""Analyze cyclic hopping power for one represented matrix field."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.physkit.units import ComplexMatrixQuantity, ScalarQuantity, Unitless

from ksdft2effmass.solidstate import (
    CenteredUniformReciprocalMesh1D,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorFourierTransformRequest1D,
    ReciprocalOperatorSamples1D,
)


@dataclass(frozen=True, slots=True)
class _Periodic1DCyclicHoppingPower:
    displacement: int
    normalized_squared_frobenius_norm: float


class _Periodic1DCyclicHoppingPowerAnalyzer:
    """Return one semantic single-channel power inventory."""

    __slots__ = (
        "_coordinate_absolute_tolerance",
        "_coordinates",
        "_matrices",
        "_reconstruction_absolute_tolerance",
    )

    def __init__(
        self,
        *,
        coordinates: Float64Array,
        matrices: Complex128Array,
        coordinate_absolute_tolerance: float,
        reconstruction_absolute_tolerance: float,
    ) -> None:
        if not isinstance(coordinates, np.ndarray):
            raise TypeError("coordinates must be a numpy array")
        if not isinstance(matrices, np.ndarray):
            raise TypeError("matrices must be a numpy array")
        for name, value in (
            ("coordinate_absolute_tolerance", coordinate_absolute_tolerance),
            ("reconstruction_absolute_tolerance", reconstruction_absolute_tolerance),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
        coordinates_copy = np.array(coordinates, dtype=np.float64, copy=True)
        matrices_copy = np.array(matrices, dtype=np.complex128, copy=True)
        if coordinates_copy.shape != (coordinates_copy.size,):
            raise ValueError("coordinates must be one-dimensional")
        if matrices_copy.shape != (coordinates_copy.size, 2, 2):
            raise ValueError("matrices must have shape (N, 2, 2)")
        coordinates_copy.setflags(write=False)
        matrices_copy.setflags(write=False)
        self._coordinates = coordinates_copy
        self._matrices = matrices_copy
        self._coordinate_absolute_tolerance = coordinate_absolute_tolerance
        self._reconstruction_absolute_tolerance = reconstruction_absolute_tolerance

    def execute(self) -> tuple[_Periodic1DCyclicHoppingPower, ...]:
        """Transform the field and report normalized block powers."""
        unit = Unitless()
        period = ScalarQuantity(1.0, unit)
        mesh = CenteredUniformReciprocalMesh1D(period, self._coordinates.size)
        if not np.allclose(
            mesh.coordinates.magnitude,
            self._coordinates,
            rtol=0.0,
            atol=self._coordinate_absolute_tolerance,
        ):
            raise ValueError("Fourier mesh differs from the qualified parent mesh")
        transform = ReciprocalOperatorFourierTransformer1D(
            ReciprocalOperatorFourierTransformRequest1D(
                source=ReciprocalOperatorSamples1D(
                    coordinates=mesh.coordinates,
                    reciprocal_period=period,
                    matrices=tuple(
                        ComplexMatrixQuantity(matrix, unit) for matrix in self._matrices
                    ),
                ),
                mesh=mesh,
                coordinate_absolute_tolerance=self._coordinate_absolute_tolerance,
                reconstruction_absolute_tolerance=(
                    self._reconstruction_absolute_tolerance
                ),
            )
        ).execute()
        return tuple(
            _Periodic1DCyclicHoppingPower(
                displacement=displacement,
                normalized_squared_frobenius_norm=float(
                    np.linalg.norm(block.magnitude) ** 2 / 2.0
                ),
            )
            for displacement, block in zip(
                transform.hopping_model.representatives,
                transform.hopping_model.hopping_blocks,
                strict=True,
            )
        )


__all__: list[str] = []
