"""One-dimensional plane-wave bases and reciprocal sewing maps."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import numpy as np

from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)


@dataclass(frozen=True, slots=True)
class PlaneWaveBasis1D:
    """Represent the ordered reciprocal-index basis ``-P,...,P``."""

    reciprocal_vector: ScalarQuantity
    cutoff: int

    def __post_init__(self) -> None:
        """Validate a positive reciprocal vector and nonnegative integer cutoff."""
        if type(self.reciprocal_vector) is not ScalarQuantity:
            raise TypeError("reciprocal_vector must be ScalarQuantity")
        if self.reciprocal_vector.magnitude <= 0.0:
            raise ValueError("reciprocal_vector must be positive")
        if type(self.cutoff) is not int:
            raise TypeError("cutoff must be a built-in int")
        if self.cutoff < 0:
            raise ValueError("cutoff must be nonnegative")

    @property
    def reciprocal_indices(self) -> tuple[int, ...]:
        """Return ordered integer reciprocal indices."""
        return tuple(range(-self.cutoff, self.cutoff + 1))

    @property
    def wave_vectors(self) -> VectorQuantity:
        """Return represented reciprocal vectors in basis order."""
        values = self.reciprocal_vector.magnitude * np.asarray(
            self.reciprocal_indices, dtype=np.float64
        )
        return VectorQuantity(values, self.reciprocal_vector.unit)

    @property
    def dimension(self) -> int:
        """Return the represented basis dimension."""
        return 2 * self.cutoff + 1


class ReciprocalSewingDirection1D(StrEnum):
    """Supported direction of a one-dimensional reciprocal-index sewing map."""

    PLUS_RECIPROCAL_VECTOR = "plus_reciprocal_vector"


@dataclass(frozen=True, slots=True)
class PlaneWaveReciprocalSewingResult:
    r"""Retain the coefficient map representing ``k -> k + G`` at fixed cutoff.

    For ordered reciprocal indices :math:`n,m\in\{-P,\ldots,P\}`, the represented
    coefficient relation is

    .. math::

       c_n(k+G)=c_{n+1}(k), \qquad S_{nm}=\delta_{m,n+1}.

    The absent boundary coefficient is not wrapped into the finite basis. The map is
    therefore an explicit nonunitary finite-cutoff representation of reciprocal
    sewing, not the unitary sewing operator on the untruncated parent space.
    """

    basis: PlaneWaveBasis1D
    direction: ReciprocalSewingDirection1D
    coefficient_map: ComplexMatrixQuantity

    def __post_init__(self) -> None:
        """Validate exact basis, direction, unit, shape, and shift entries."""
        if type(self.basis) is not PlaneWaveBasis1D:
            raise TypeError("basis must be PlaneWaveBasis1D")
        if type(self.direction) is not ReciprocalSewingDirection1D:
            raise TypeError("direction must be ReciprocalSewingDirection1D")
        if type(self.coefficient_map) is not ComplexMatrixQuantity:
            raise TypeError("coefficient_map must be ComplexMatrixQuantity")
        if type(self.coefficient_map.unit) is not Unitless:
            raise ValueError("coefficient_map must be unitless")
        indices = self.basis.reciprocal_indices
        for target_position, target_index in enumerate(indices):
            for source_position, source_index in enumerate(indices):
                expected = 1.0 if source_index == target_index + 1 else 0.0
                if (
                    self.coefficient_map.magnitude[target_position, source_position]
                    != expected
                ):
                    raise ValueError(
                        "coefficient_map must implement the declared basis shift"
                    )


class PlaneWaveReciprocalSewingConstructor:
    """Construct the finite-cutoff coefficient map for ``k -> k + G``."""

    __slots__ = ()

    def execute(self, basis: PlaneWaveBasis1D) -> PlaneWaveReciprocalSewingResult:
        """Return the explicit nonunitary finite-cutoff shift map."""
        if type(basis) is not PlaneWaveBasis1D:
            raise TypeError("basis must be PlaneWaveBasis1D")
        coefficient_map = np.zeros(
            (basis.dimension, basis.dimension), dtype=np.complex128
        )
        positions = {
            reciprocal_index: position
            for position, reciprocal_index in enumerate(basis.reciprocal_indices)
        }
        for target_position, target_index in enumerate(basis.reciprocal_indices):
            source_position = positions.get(target_index + 1)
            if source_position is not None:
                coefficient_map[target_position, source_position] = 1.0
        return PlaneWaveReciprocalSewingResult(
            basis,
            ReciprocalSewingDirection1D.PLUS_RECIPROCAL_VECTOR,
            ComplexMatrixQuantity(coefficient_map, Unitless()),
        )
