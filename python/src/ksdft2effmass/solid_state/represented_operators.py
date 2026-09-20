"""Complete scalar finite-lattice represented-operator metadata.

The record in this module composes dependency-owned complex sparse matrix quantities
with the finite geometry, boundary twist, gauge, basis, unit, energy-reference, and
provenance metadata required to interpret one scalar finite-lattice representation. It
does not construct a matrix, infer compatibility, impose Hermiticity, or authorize a
finite-domain calculation.
"""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.operators import ComplexSparseMatrixQuantity

from .boundary_phases import TwistFiber
from .geometry import FiniteLatticeShape, LatticeDimension

type ProvenanceEntry = tuple[str, str]
"""One exact nonempty provenance key/value pair."""


@dataclass(frozen=True, slots=True)
class ScalarFiniteLatticeOperator:
    """Represent one sparse scalar finite-lattice operator with interpreting metadata.

    Parameters
    ----------
    identifier
        Nonempty represented-operator identity.
    matrix
        Immutable canonical complex128 CSR values and their physical or dimensionless
        unit. The matrix must have one row and column per finite lattice cell.
    shape
        Finite periodic tensor-product geometry and site ordering.
    twist_fiber
        Correlated unreduced lift, quotient representative, and exact gauge with the
        same dimension as ``shape``.
    basis_identifier
        Nonempty identity for the scalar one-state-per-cell basis convention.
    energy_reference
        Nonempty identity for the represented energy-zero convention.
    provenance
        Sorted tuple of unique nonempty string key/value pairs. Values are retained
        exactly; construction does not verify provenance truth.

    Notes
    -----
    The scalar contract fixes exactly one basis state per lattice cell. Multi-orbital,
    spin, nonorthogonal-overlap, and atomic-to-reduced-model mappings are outside this
    record. Construction establishes represented metadata consistency only; it does not
    establish Hermiticity, gauge equivalence, physical validity, numerical
    verification, scientific validation, or uncertainty quantification.
    """

    identifier: str
    matrix: ComplexSparseMatrixQuantity
    shape: FiniteLatticeShape
    twist_fiber: TwistFiber
    basis_identifier: str
    energy_reference: str
    provenance: tuple[ProvenanceEntry, ...]

    def __post_init__(self) -> None:
        """Validate exact component types and cross-field representation invariants."""
        self._require_nonempty_string(self.identifier, "identifier")
        if type(self.matrix) is not ComplexSparseMatrixQuantity:
            raise TypeError("matrix must be ComplexSparseMatrixQuantity")
        if type(self.shape) is not FiniteLatticeShape:
            raise TypeError("shape must be FiniteLatticeShape")
        if type(self.twist_fiber) is not TwistFiber:
            raise TypeError("twist_fiber must be TwistFiber")
        self._require_nonempty_string(self.basis_identifier, "basis_identifier")
        self._require_nonempty_string(self.energy_reference, "energy_reference")
        expected_shape = (self.shape.cell_count, self.shape.cell_count)
        if self.matrix.shape != expected_shape:
            raise ValueError("matrix shape must equal scalar finite-lattice cell count")
        if self.twist_fiber.dimension is not self.shape.dimension:
            raise ValueError("twist fiber and finite-lattice dimensions must agree")
        if type(self.provenance) is not tuple:
            raise TypeError("provenance must be a tuple of key/value pairs")
        keys: list[str] = []
        for entry in self.provenance:
            if type(entry) is not tuple or len(entry) != 2:
                raise TypeError("provenance entries must be two-string tuples")
            key, value = entry
            self._require_nonempty_string(key, "provenance key")
            self._require_nonempty_string(value, "provenance value")
            keys.append(key)
        if keys != sorted(set(keys)):
            raise ValueError("provenance keys must be sorted and unique")

    @property
    def dimension(self) -> LatticeDimension:
        """Return the exact finite-lattice spatial dimension."""
        return self.shape.dimension

    @staticmethod
    def _require_nonempty_string(value: str, name: str) -> None:
        """Validate one intrinsic exact string field."""
        if type(value) is not str:
            raise TypeError(f"{name} must be a string")
        if not value:
            raise ValueError(f"{name} must be nonempty")
