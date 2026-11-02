"""PhysKit-backed direct and reciprocal geometry for periodic two dimensions."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Self

import numpy as np
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    DirectLatticeMetric,
    ReciprocalLattice2D,
)
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)
from projectkoios.physkit.units import (
    ModelSystemUnitConverter,
    PhysicalUnit,
    VectorQuantity,
)


@dataclass(frozen=True, slots=True)
class Periodic2DLatticeGeometry:
    """Retain an immutable snapshot of a two-dimensional direct lattice.

    Primitive direct-lattice vectors are columns of the matrix represented by
    ``primitive_basis_rows`` and use the explicit physical length unit selected by the
    caller. Fresh PhysKit lattice objects are reconstructed from the immutable scalar
    snapshot so returned arrays cannot mutate this value.
    """

    primitive_basis_rows: tuple[tuple[float, float], tuple[float, float]]
    lattice_unit: PhysicalUnit

    def __post_init__(self) -> None:
        _primitive_basis(self.primitive_basis_rows)
        _length_unit(self.lattice_unit)
        _ = self.direct_lattice

    @classmethod
    def from_direct_lattice(
        cls,
        direct_lattice: DirectLattice2D,
        lattice_unit: PhysicalUnit,
    ) -> Self:
        """Snapshot one exact PhysKit two-dimensional direct lattice."""
        if type(direct_lattice) is not DirectLattice2D:
            raise TypeError("direct_lattice must be the exact PhysKit DirectLattice2D")
        basis = direct_lattice.A
        return cls(
            primitive_basis_rows=(
                (float(basis[0, 0]), float(basis[0, 1])),
                (float(basis[1, 0]), float(basis[1, 1])),
            ),
            lattice_unit=lattice_unit,
        )

    @property
    def direct_lattice(self) -> DirectLattice2D:
        """Return a fresh PhysKit direct lattice with column primitive vectors."""
        basis = np.asarray(self.primitive_basis_rows, dtype=np.float64)
        return DirectLattice2D(a1=basis[:, 0], a2=basis[:, 1])

    @property
    def direct_metric(self) -> DirectLatticeMetric:
        """Return the PhysKit metric derived from the exact direct lattice."""
        return DirectLatticeMetric(self.direct_lattice)

    @property
    def reciprocal_lattice(self) -> ReciprocalLattice2D:
        """Return the PhysKit reciprocal lattice satisfying ``A.T @ B = 2 pi I``."""
        return ReciprocalLattice2D.from_direct_lattice(self.direct_lattice)

    @property
    def reciprocal_lattice_unit(self) -> PhysicalUnit:
        """Return the physical inverse-length unit dual to ``lattice_unit``."""
        return PhysicalUnit(f"1 / ({self.lattice_unit.expression})")

    def direct_translation(self, displacement: LatticeDisplacement) -> VectorQuantity:
        """Return ``R_n = A n`` with the declared physical length unit."""
        if type(displacement) is not LatticeDisplacement:
            raise TypeError("displacement must be an exact LatticeDisplacement")
        if displacement.dimension is not LatticeDimension.TWO:
            raise ValueError("displacement must have lattice dimension two")
        indices = np.asarray(displacement.components, dtype=np.int64)
        return VectorQuantity(self.direct_lattice.vector(indices), self.lattice_unit)

    def bloch_wavevector(
        self,
        reduced_coordinates: tuple[float, float],
    ) -> VectorQuantity:
        """Return ``k = B q`` with the physical reciprocal-length unit."""
        coordinates = _reduced_coordinates(reduced_coordinates)
        return VectorQuantity(
            self.direct_metric.reciprocal_basis @ coordinates,
            self.reciprocal_lattice_unit,
        )

    def reduced_coordinates(
        self,
        bloch_wavevector: VectorQuantity,
    ) -> tuple[float, float]:
        """Convert a physical reciprocal-length vector to reduced coordinates."""
        vector = _converted_wavevector(
            bloch_wavevector,
            self.reciprocal_lattice_unit,
            expected_dimension=2,
        )
        coordinates = np.linalg.solve(self.direct_metric.reciprocal_basis, vector)
        return (float(coordinates[0]), float(coordinates[1]))


def _primitive_basis(
    value: tuple[tuple[float, float], tuple[float, float]],
) -> tuple[tuple[float, float], tuple[float, float]]:
    if type(value) is not tuple or len(value) != 2:
        raise TypeError("primitive_basis_rows must be a two-row tuple")
    if any(type(row) is not tuple or len(row) != 2 for row in value):
        raise TypeError("primitive_basis_rows must contain two-component tuples")
    if any(type(component) is not float for row in value for component in row):
        raise TypeError("primitive_basis_rows must contain built-in floats")
    if any(not math.isfinite(component) for row in value for component in row):
        raise ValueError("primitive_basis_rows must be finite")
    return value


def _length_unit(value: PhysicalUnit) -> PhysicalUnit:
    if type(value) is not PhysicalUnit:
        raise TypeError("lattice_unit must be PhysicalUnit")
    if not ModelSystemUnitConverter.compatible(value, PhysicalUnit("meter")):
        raise ValueError("lattice_unit must have length dimensionality")
    return value


def _reduced_coordinates(value: tuple[float, float]) -> np.ndarray:
    if type(value) is not tuple or len(value) != 2:
        raise TypeError("reduced_coordinates must be a two-component tuple")
    if any(type(component) is not float for component in value):
        raise TypeError("reduced_coordinates must contain built-in floats")
    if any(not math.isfinite(component) for component in value):
        raise ValueError("reduced_coordinates must be finite")
    return np.asarray(value, dtype=np.float64)


def _converted_wavevector(
    value: VectorQuantity,
    target_unit: PhysicalUnit,
    *,
    expected_dimension: int,
) -> np.ndarray:
    if type(value) is not VectorQuantity:
        raise TypeError("bloch_wavevector must be VectorQuantity")
    if type(value.unit) is not PhysicalUnit:
        raise TypeError("bloch_wavevector must use PhysicalUnit")
    if not ModelSystemUnitConverter.compatible(value.unit, target_unit):
        raise ValueError("bloch_wavevector must have inverse-length dimensions")
    converted = ModelSystemUnitConverter.convert_vector(value, target_unit)
    if converted.magnitude.shape != (expected_dimension,):
        raise ValueError("bloch_wavevector dimension must match the direct lattice")
    return converted.magnitude


__all__ = ["Periodic2DLatticeGeometry"]
