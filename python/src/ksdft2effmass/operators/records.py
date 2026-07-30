r"""Data objects for finite represented operator records.

The classes in this module are DataObjects: frozen, slotted dataclasses that own
only represented data, intrinsic constructor validation, canonicalization of
their own fields, and exact structural equality. Numerical analyses such as
Hermiticity checks and external representations such as JSON-compatible payloads
live in action objects outside this module.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, ClassVar, cast

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
        Descriptive state-space category. This is metadata, not a controlled
        vocabulary enforced by the code.
    dimension
        Positive finite represented dimension ``N``. Ordinary Python integers
        and NumPy integral types are accepted; Boolean values and floats are
        rejected.

    Raises
    ------
    TypeError
        If ``identifier`` or ``kind`` is not a string, or if ``dimension`` is
        not an integer or is Boolean.
    ValueError
        If ``dimension`` is not positive.
    """

    identifier: str
    kind: str
    dimension: int | np.integer[Any]

    def __post_init__(self) -> None:
        _require_string(self.identifier, "state-space identifier")
        _require_string(self.kind, "state-space kind")
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
    index ``i`` of an :class:`OperatorRecord` matrix. Labels must be nonempty
    strings and must be unique. The object records the asserted orthonormality
    of the basis but does not verify basis vectors, because vectors are not
    stored.

    Schema version 1 operator records require ``orthonormal is True``; that
    representation-level invariant is enforced by :class:`OperatorRecord`.
    """

    identifier: str
    kind: str
    ordering: tuple[str, ...]
    orthonormal: bool

    def __post_init__(self) -> None:
        _require_string(self.identifier, "basis identifier")
        _require_string(self.kind, "basis kind")
        if type(self.orthonormal) is not bool:
            msg = "basis orthonormal flag must be a Python bool"
            raise TypeError(msg)
        if isinstance(self.ordering, str | bytes):
            msg = "basis ordering must be an iterable of labels, not a string"
            raise TypeError(msg)
        ordering = tuple(self.ordering)
        if not ordering:
            msg = "basis ordering must not be empty"
            raise ValueError(msg)
        for label in ordering:
            _require_string(label, "basis label")
        if len(set(ordering)) != len(ordering):
            msg = "basis ordering labels must be unique"
            raise ValueError(msg)
        object.__setattr__(self, "ordering", ordering)


@dataclass(frozen=True, slots=True)
class Geometry:
    """Three-dimensional cell and boundary-condition metadata.

    Lattice vectors are stored as rows: ``cell[i][j]`` is Cartesian component
    ``j`` of lattice vector ``i``. Every cell component is expressed in
    ``length_unit``. A cell is accepted only when its singular values satisfy
    ``sigma_max > 0`` and
    ``sigma_min > LINEAR_INDEPENDENCE_RTOL * sigma_max``.
    """

    LINEAR_INDEPENDENCE_RTOL: ClassVar[float] = 1.0e-12

    system: str
    cell: tuple[tuple[float, float, float], ...]
    boundary_conditions: str
    coordinate_convention: str
    length_unit: str

    def __post_init__(self) -> None:
        _require_string(self.system, "geometry system")
        _require_string(self.boundary_conditions, "geometry boundary conditions")
        _require_string(self.coordinate_convention, "geometry coordinate convention")
        _require_string(self.length_unit, "geometry length unit")
        object.__setattr__(self, "cell", self._canonicalize_cell(self.cell))

    @classmethod
    def _canonicalize_cell(
        cls,
        cell: tuple[tuple[float, float, float], ...],
    ) -> tuple[tuple[float, float, float], ...]:
        if isinstance(cell, str | bytes):
            msg = "cell must be an iterable of row lattice vectors"
            raise TypeError(msg)
        try:
            iterator = iter(cell)
        except TypeError as exc:
            msg = "cell must be an iterable of row lattice vectors"
            raise TypeError(msg) from exc
        canonical_rows: list[tuple[float, ...]] = []
        for row in iterator:
            if isinstance(row, str | bytes):
                msg = "cell rows must be iterables of numeric components"
                raise TypeError(msg)
            try:
                row_iterator = iter(row)
            except TypeError as exc:
                msg = "cell rows must be iterables of numeric components"
                raise TypeError(msg) from exc
            canonical_rows.append(
                tuple(
                    cls._finite_real(component, "cell component")
                    for component in row_iterator
                )
            )
        canonical = tuple(canonical_rows)
        if len(canonical) != 3 or any(len(vector) != 3 for vector in canonical):
            msg = "cell must contain three three-component row lattice vectors"
            raise ValueError(msg)
        cell_array = np.array(canonical, dtype=float)
        singular_values = np.linalg.svd(cell_array, compute_uv=False)
        sigma_max = float(np.max(singular_values))
        sigma_min = float(np.min(singular_values))
        if sigma_max <= 0.0 or sigma_min <= cls.LINEAR_INDEPENDENCE_RTOL * sigma_max:
            msg = "cell row lattice vectors must be sufficiently linearly independent"
            raise ValueError(msg)
        return cast(tuple[tuple[float, float, float], ...], canonical)

    @staticmethod
    def _finite_real(value: Any, name: str) -> float:
        if (
            isinstance(value, bool)
            or isinstance(value, np.bool_)
            or not isinstance(value, int | float | np.integer | np.floating)
        ):
            msg = f"{name} must be a finite real numeric value"
            raise ValueError(msg)
        real = float(value)
        if not np.isfinite(real):
            msg = f"{name} must be finite"
            raise ValueError(msg)
        return real


@dataclass(frozen=True, slots=True)
class EnergyReference:
    """Energy-zero metadata for a finite operator matrix.

    The stored operator matrix is already expressed relative to ``zero``. The
    named reference has numerical value zero in the stored matrix coordinate
    system, and no unapplied offset is stored. Unit conversion and energy
    alignment are intentionally outside this data object.
    """

    zero: str
    unit: str

    def __post_init__(self) -> None:
        _require_string(self.zero, "energy-reference zero")
        _require_string(self.unit, "energy-reference unit")


@dataclass(frozen=True, slots=True, eq=False)
class OperatorRecord:
    r"""Finite square matrix representation of an operator with metadata.

    ``OperatorRecord`` represents data only: an owned finite matrix
    representation

    .. math::

       \mathbf H \in \mathbb C^{N \times N},

    plus state-space, orthonormal basis, geometry, energy-reference, and
    provenance metadata. It does not store Hermiticity tolerances, analysis
    results, serialization policy, alignment state, or unit-conversion policy.

    The matrix is copied into owned C-contiguous row-major ``np.complex128``
    storage and marked non-writeable through the public API. This is API-level
    immutability for represented data; it is not a claim about NumPy internals
    outside the public object contract. ``OperatorRecord`` is explicitly
    unhashable because it owns an array.
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
        _require_string(self.identifier, "operator-record identifier")
        _require_string(self.operator_kind, "operator kind")
        self._reject_forbidden_matrix_scalars(self.matrix)
        matrix = np.array(self.matrix, dtype=np.complex128, copy=True, order="C")
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
        if self.basis.orthonormal is not True:
            msg = "operator records require an orthonormal basis in schema version 1"
            raise ValueError(msg)

    @staticmethod
    def _reject_forbidden_matrix_scalars(matrix: object) -> None:
        raw = np.asarray(matrix, dtype=object)
        for value in raw.flat:
            if isinstance(value, bool | np.bool_ | str | bytes):
                msg = "operator matrix entries must be numeric, not bool or string"
                raise TypeError(msg)

    @staticmethod
    def _copy_provenance(provenance: Mapping[str, str]) -> Mapping[str, str]:
        if not isinstance(provenance, Mapping):
            msg = "provenance must be a mapping from strings to strings"
            raise TypeError(msg)
        copied = dict(provenance)
        if any(
            not isinstance(key, str) or not isinstance(value, str)
            for key, value in copied.items()
        ):
            msg = "provenance keys and values must be strings"
            raise TypeError(msg)
        if any(key == "" or value == "" for key, value in copied.items()):
            msg = "provenance keys and values must not be empty"
            raise ValueError(msg)
        return MappingProxyType(copied)


def _require_string(value: object, name: str) -> None:
    if not isinstance(value, str):
        msg = f"{name} must be a string"
        raise TypeError(msg)
    if value == "":
        msg = f"{name} must not be empty"
        raise ValueError(msg)
