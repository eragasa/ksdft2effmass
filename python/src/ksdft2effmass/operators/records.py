r"""Data objects for finite operator records.

The classes in this module are DataObjects: frozen, slotted dataclasses that own
only represented data, constructor-time validation, canonicalization of their own
fields, and exact structural equality.  Workflows such as Hermiticity analysis
and JSON-compatible serialization live in separate action objects.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, cast

import numpy as np
from numpy.typing import NDArray

ComplexMatrix = NDArray[np.complex128]
"""Owned dense complex matrix type used by :class:`OperatorRecord`."""


@dataclass(frozen=True, slots=True)
class StateSpace:
    """Finite represented state-space metadata.

    Parameters
    ----------
    identifier
        Descriptive identifier for the represented finite state space.
    kind
        Descriptive state-space category.  This is metadata, not a controlled
        vocabulary enforced by the code.
    dimension
        Positive finite represented dimension ``N``.  Ordinary Python integers
        and NumPy integral types are accepted; Boolean values and floats are
        rejected.
    domain
        Description of the represented mathematical or computational domain.
    codomain
        Description of the represented target space.

    Raises
    ------
    TypeError
        If ``dimension`` is not an integer or is Boolean.
    ValueError
        If ``dimension`` is not positive.
    """

    identifier: str
    kind: str
    dimension: int | np.integer[Any]
    domain: str
    codomain: str

    def __post_init__(self) -> None:
        if isinstance(self.dimension, bool) or not isinstance(
            self.dimension, int | np.integer
        ):
            msg = "state-space dimension must be a positive integer"
            raise TypeError(msg)
        dimension = int(self.dimension)
        if dimension <= 0:
            msg = "state-space dimension must be positive"
            raise ValueError(msg)
        object.__setattr__(self, "dimension", dimension)


@dataclass(frozen=True, slots=True)
class Basis:
    """Ordered basis metadata for a finite matrix representation.

    ``ordering[i]`` identifies the basis state associated with row and column
    index ``i`` of an :class:`OperatorRecord` matrix.  The object records the
    asserted orthonormality of the basis but does not verify basis vectors,
    because vectors are not stored.
    """

    identifier: str
    kind: str
    ordering: tuple[str, ...]
    orthonormal: bool

    def __post_init__(self) -> None:
        ordering = tuple(self.ordering)
        if not ordering:
            msg = "basis ordering must not be empty"
            raise ValueError(msg)
        object.__setattr__(self, "ordering", ordering)


@dataclass(frozen=True, slots=True)
class Geometry:
    """Three-dimensional cell and boundary-condition metadata.

    The current model represents a three-dimensional periodic cell.  Lattice
    vectors are stored as rows: ``cell[i][j]`` is Cartesian component ``j`` of
    lattice vector ``i``.  Length units must be stated in
    ``coordinate_convention`` or provenance until a project-wide unit schema is
    introduced.
    """

    system: str
    cell: tuple[tuple[float, float, float], ...]
    boundary_conditions: str
    coordinate_convention: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "cell", self._canonicalize_cell(self.cell))

    @staticmethod
    def _canonicalize_cell(
        cell: tuple[tuple[float, float, float], ...],
    ) -> tuple[tuple[float, float, float], ...]:
        try:
            canonical = tuple(
                tuple(float(component) for component in row) for row in cell
            )
        except (TypeError, ValueError) as exc:
            msg = "cell must contain finite numeric row lattice vectors"
            raise ValueError(msg) from exc
        if len(canonical) != 3 or any(len(vector) != 3 for vector in canonical):
            msg = "cell must contain three three-component row lattice vectors"
            raise ValueError(msg)
        cell_array = np.array(canonical, dtype=float)
        if not np.all(np.isfinite(cell_array)):
            msg = "cell row lattice vectors must contain only finite values"
            raise ValueError(msg)
        if np.linalg.matrix_rank(cell_array) != 3:
            msg = "cell row lattice vectors must be linearly independent"
            raise ValueError(msg)
        return cast(tuple[tuple[float, float, float], ...], canonical)


@dataclass(frozen=True, slots=True)
class EnergyReference:
    """Energy-zero metadata for a finite operator matrix.

    The stored operator matrix is already expressed relative to ``zero``.
    ``value`` records the position of that zero in ``unit`` as metadata; it is
    not an unapplied matrix shift.  Unit conversion and energy alignment are
    intentionally outside this data object.
    """

    zero: str
    unit: str
    value: float = 0.0

    def __post_init__(self) -> None:
        try:
            value = float(self.value)
        except (TypeError, ValueError) as exc:
            msg = "energy-reference value must be finite numeric metadata"
            raise ValueError(msg) from exc
        if not np.isfinite(value):
            msg = "energy-reference value must be finite"
            raise ValueError(msg)
        object.__setattr__(self, "value", value)


@dataclass(frozen=True, slots=True, eq=False)
class OperatorRecord:
    r"""Finite matrix realization of an operator with metadata.

    ``OperatorRecord`` represents data only: an owned finite matrix realization

    .. math::

       \mathbf H : \mathbb C^N \rightarrow \mathbb C^N,

    plus state-space, basis, geometry, energy-reference, and provenance
    metadata.  It does not store Hermiticity tolerances or analysis results and
    does not serialize itself.
    """

    identifier: str
    operator_kind: str
    matrix: ComplexMatrix
    state_space: StateSpace
    basis: Basis
    geometry: Geometry
    energy_reference: EnergyReference
    provenance: Mapping[str, str]

    def __post_init__(self) -> None:
        matrix = np.array(self.matrix, dtype=np.complex128, copy=True)
        self._validate_matrix(matrix)
        matrix.setflags(write=False)
        object.__setattr__(self, "matrix", matrix)
        object.__setattr__(self, "provenance", self._copy_provenance(self.provenance))

    @property
    def shape(self) -> tuple[int, int]:
        """Shape of the stored finite matrix representation."""

        return self.matrix.shape

    def __eq__(self, other: object) -> bool:
        """Return exact structural equality using ``np.array_equal`` for matrix."""

        if not isinstance(other, OperatorRecord):
            return NotImplemented
        return (
            self.identifier == other.identifier
            and self.operator_kind == other.operator_kind
            and np.array_equal(self.matrix, other.matrix)
            and self.state_space == other.state_space
            and self.basis == other.basis
            and self.geometry == other.geometry
            and self.energy_reference == other.energy_reference
            and dict(self.provenance) == dict(other.provenance)
        )

    __hash__ = None  # type: ignore[assignment]

    def _validate_matrix(self, matrix: ComplexMatrix) -> None:
        if matrix.ndim != 2:
            msg = "operator matrix must be two-dimensional"
            raise ValueError(msg)
        if matrix.shape[0] != matrix.shape[1]:
            msg = "operator matrix must be square"
            raise ValueError(msg)
        if not np.all(np.isfinite(matrix)):
            msg = "operator matrix entries must be finite"
            raise ValueError(msg)
        if matrix.shape[0] != self.state_space.dimension:
            msg = "matrix dimension must match state-space dimension"
            raise ValueError(msg)
        if len(self.basis.ordering) != self.state_space.dimension:
            msg = "basis ordering length must match state-space dimension"
            raise ValueError(msg)

    @staticmethod
    def _copy_provenance(provenance: Mapping[str, str]) -> Mapping[str, str]:
        copied = dict(provenance)
        if any(
            not isinstance(key, str) or not isinstance(value, str)
            for key, value in copied.items()
        ):
            msg = "provenance keys and values must be strings"
            raise TypeError(msg)
        return MappingProxyType(copied)
