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
        """Validate and canonicalize state-space metadata fields."""

        self._require_string(self.identifier, "state-space identifier")
        self._require_string(self.kind, "state-space kind")
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

    @staticmethod
    def _require_string(value: object, name: str) -> None:
        """Validate a nonempty string field owned by ``StateSpace``.

        Parameters
        ----------
        value
            Candidate metadata value; only Python strings are accepted.
        name
            Diagnostic field name.

        Raises
        ------
        TypeError
            If ``value`` is not a string.
        ValueError
            If ``value`` is empty.

        Notes
        -----
        This private method is owner-local intrinsic field validation and does
        not define cross-object compatibility policy.
        """

        if not isinstance(value, str):
            msg = f"{name} must be a string"
            raise TypeError(msg)
        if value == "":
            msg = f"{name} must not be empty"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Basis:
    """Ordered basis metadata for a finite matrix representation.

    Parameters
    ----------
    identifier
        Nonempty basis identifier. It is identity/provenance metadata and is
        ignored by compatibility analysis.
    kind
        Nonempty basis-kind label. Exact equality of this field is required for
        direct compatible-record comparison.
    ordering
        Iterable of nonempty unique string labels. ``ordering[i]`` identifies
        the represented basis state associated with row and column index ``i``
        of an :class:`OperatorRecord` matrix. The iterable is canonicalized to a
        tuple of strings.
    orthonormal
        Python ``bool`` asserting the basis convention. Schema version 1
        ``OperatorRecord`` instances require ``True``; basis vectors themselves
        are not stored or verified here.

    Raises
    ------
    TypeError
        If string fields are not strings, ``ordering`` is a string/bytes value
        or contains non-string labels, or ``orthonormal`` is not a Python bool.
    ValueError
        If string fields are empty, ordering is empty, or labels are duplicated.
    """

    identifier: str
    kind: str
    ordering: tuple[str, ...]
    orthonormal: bool

    def __post_init__(self) -> None:
        """Validate and canonicalize ordered basis metadata fields."""

        self._require_string(self.identifier, "basis identifier")
        self._require_string(self.kind, "basis kind")
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
            self._require_string(label, "basis label")
        if len(set(ordering)) != len(ordering):
            msg = "basis ordering labels must be unique"
            raise ValueError(msg)
        object.__setattr__(self, "ordering", ordering)

    @staticmethod
    def _require_string(value: object, name: str) -> None:
        """Validate a nonempty string field owned by ``Basis``.

        Parameters
        ----------
        value
            Candidate basis metadata or label value.
        name
            Diagnostic field name.

        Raises
        ------
        TypeError
            If ``value`` is not a string.
        ValueError
            If ``value`` is empty.

        Notes
        -----
        This owner-local private check prevents ambiguous module-level field
        validators and does not convert numeric values to labels.
        """

        if not isinstance(value, str):
            msg = f"{name} must be a string"
            raise TypeError(msg)
        if value == "":
            msg = f"{name} must not be empty"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Geometry:
    """Three-dimensional cell and boundary-condition metadata.

    Parameters
    ----------
    system
        Nonempty physical-system label. It is identity/provenance metadata and
        is ignored by compatibility analysis.
    cell
        Three row lattice vectors with three finite real components each.
        Components are expressed in ``length_unit`` and canonicalized to nested
        tuples of built-in ``float``.
    boundary_conditions
        Nonempty boundary-condition convention string. Exact equality is a
        compatibility rule.
    coordinate_convention
        Nonempty coordinate-convention string for interpreting cell rows. Exact
        equality is a compatibility rule.
    length_unit
        Nonempty dimensional unit for every cell component. No unit conversion
        is performed by this DataObject.

    Attributes
    ----------
    LINEAR_INDEPENDENCE_RTOL
        Relative singular-value threshold. A cell is accepted only when
        ``sigma_max > 0`` and
        ``sigma_min > LINEAR_INDEPENDENCE_RTOL * sigma_max``.

    Raises
    ------
    TypeError
        If string fields are not strings or cell rows/components are not
        accepted iterable real numeric values.
    ValueError
        If string fields are empty, the cell is not 3x3, components are
        nonfinite, or row lattice vectors are not sufficiently independent.
    """

    LINEAR_INDEPENDENCE_RTOL: ClassVar[float] = 1.0e-12

    system: str
    cell: tuple[tuple[float, float, float], ...]
    boundary_conditions: str
    coordinate_convention: str
    length_unit: str

    def __post_init__(self) -> None:
        """Validate geometry metadata and canonicalize the lattice cell."""

        self._require_string(self.system, "geometry system")
        self._require_string(self.boundary_conditions, "geometry boundary conditions")
        self._require_string(
            self.coordinate_convention, "geometry coordinate convention"
        )
        self._require_string(self.length_unit, "geometry length unit")
        object.__setattr__(self, "cell", self._canonicalize_cell(self.cell))

    @staticmethod
    def _require_string(value: object, name: str) -> None:
        """Validate a nonempty string field owned by ``Geometry``.

        Parameters
        ----------
        value
            Candidate geometry metadata value.
        name
            Diagnostic field name.

        Raises
        ------
        TypeError
            If ``value`` is not a string.
        ValueError
            If ``value`` is empty.

        Notes
        -----
        The method is private and owner-local; geometry dimensional units and
        conventions remain explicit string fields without numeric conversion.
        """

        if not isinstance(value, str):
            msg = f"{name} must be a string"
            raise TypeError(msg)
        if value == "":
            msg = f"{name} must not be empty"
            raise ValueError(msg)

    @classmethod
    def _canonicalize_cell(
        cls,
        cell: tuple[tuple[float, float, float], ...],
    ) -> tuple[tuple[float, float, float], ...]:
        """Return a validated immutable 3x3 row-vector cell.

        Parameters
        ----------
        cell
            Iterable of three row lattice vectors.  Components may be Python or
            NumPy real numeric scalars and are canonicalized to built-in floats.

        Returns
        -------
        tuple[tuple[float, float, float], ...]
            Three row lattice vectors in the documented ``length_unit``.

        Raises
        ------
        TypeError
            If the cell or a row is not iterable, or a component is not an
            accepted real numeric scalar.  Booleans, strings, bytes, and complex
            values are rejected.
        ValueError
            If the cell is not 3x3, contains nonfinite values, or is singular to
            the documented linear-independence threshold.

        Notes
        -----
        This private method is owned by ``Geometry`` because cell shape,
        canonicalization, and linear independence are intrinsic geometry
        invariants.  The singular-value check is numerical validation of row
        lattice-vector independence, not scientific validation of a structure.
        """

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
        # Represent the candidate row lattice vectors as a real 3x3 matrix for
        # a numerical rank check independent of a particular coordinate axis.
        cell_array = np.array(canonical, dtype=float)
        # Singular values quantify row-vector linear independence; the smallest
        # value is compared with the largest for a scale-aware cell check.
        singular_values = np.linalg.svd(cell_array, compute_uv=False)
        sigma_max = float(np.max(singular_values))
        sigma_min = float(np.min(singular_values))
        if sigma_max <= 0.0 or sigma_min <= cls.LINEAR_INDEPENDENCE_RTOL * sigma_max:
            msg = "cell row lattice vectors must be sufficiently linearly independent"
            raise ValueError(msg)
        return cast(tuple[tuple[float, float, float], ...], canonical)

    @staticmethod
    def _finite_real(value: object, name: str) -> float:
        """Return a canonical finite real cell component.

        Parameters
        ----------
        value
            Candidate component.  Python and NumPy integer or floating scalars
            are accepted; booleans, strings, bytes, complex values, and other
            objects are rejected.
        name
            Diagnostic field name.

        Returns
        -------
        float
            Built-in float used at the immutable Python/Rust data boundary.

        Raises
        ------
        TypeError
            If ``value`` is not an accepted real scalar.
        ValueError
            If ``value`` is nonfinite.
        """

        if (
            isinstance(value, bool)
            or isinstance(value, np.bool_)
            or not isinstance(value, int | float | np.integer | np.floating)
        ):
            msg = f"{name} must be a finite real numeric value"
            raise TypeError(msg)
        # Canonicalize accepted Python/NumPy real scalars to built-in float for
        # stable immutable Python/Rust data boundaries.
        real = float(value)
        if not np.isfinite(real):
            msg = f"{name} must be finite"
            raise ValueError(msg)
        return real


@dataclass(frozen=True, slots=True)
class EnergyReference:
    """Energy-zero metadata for a finite operator matrix.

    Parameters
    ----------
    zero
        Nonempty name of the energy-zero convention already applied to the
        stored matrix. The named reference has numerical value zero in the
        stored matrix coordinate system; no numeric offset field is stored.
    unit
        Nonempty energy unit for all operator-matrix entries and unit-bearing
        Hermiticity/comparison residuals. No unit conversion is performed here.

    Raises
    ------
    TypeError
        If ``zero`` or ``unit`` is not a string.
    ValueError
        If ``zero`` or ``unit`` is empty.
    """

    zero: str
    unit: str

    def __post_init__(self) -> None:
        """Validate energy-zero and energy-unit metadata strings."""

        self._require_string(self.zero, "energy-reference zero")
        self._require_string(self.unit, "energy-reference unit")

    @staticmethod
    def _require_string(value: object, name: str) -> None:
        """Validate a nonempty string field owned by ``EnergyReference``.

        Parameters
        ----------
        value
            Candidate energy-zero or energy-unit string.
        name
            Diagnostic field name.

        Raises
        ------
        TypeError
            If ``value`` is not a string.
        ValueError
            If ``value`` is empty.

        Notes
        -----
        This private check is intrinsic field validation only; unit conversion
        and energy alignment are intentionally outside the DataObject.
        """

        if not isinstance(value, str):
            msg = f"{name} must be a string"
            raise TypeError(msg)
        if value == "":
            msg = f"{name} must not be empty"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True, eq=False)
class OperatorRecord:
    r"""Finite square matrix representation of an operator with metadata.

    Parameters
    ----------
    identifier
        Nonempty record identifier retained as provenance and ignored by
        representation compatibility.
    operator_kind
        Nonempty operator-kind label. Exact equality is required for compatible
        direct comparison.
    matrix
        Two-dimensional square finite numeric array-like object representing
        :math:`\mathbf H \in \mathbb C^{N \times N}`. Entries are defensively
        copied, canonicalized to ``np.complex128``, and exposed as a bytes-backed
        immutable matrix so public ``setflags(write=True)`` cannot re-enable
        mutation.
    state_space
        Actual :class:`StateSpace` instance. Its ``dimension`` must equal the
        matrix dimension.
    basis
        Actual :class:`Basis` instance. Its ordering length must equal the
        state-space dimension, and schema version 1 requires ``orthonormal`` to
        be ``True``.
    geometry
        Actual :class:`Geometry` instance describing the represented cell and
        coordinate conventions.
    energy_reference
        Actual :class:`EnergyReference` instance defining the matrix energy unit
        and zero convention.
    provenance
        Mapping from nonempty strings to nonempty strings. The mapping is
        defensively copied and exposed as read-only ``MappingProxyType``.

    Raises
    ------
    TypeError
        If string fields, nested public objects, matrix scalar types, or
        provenance key/value types violate the public type boundary.
    ValueError
        If strings are empty, matrix shape/finiteness/dimension invariants fail,
        basis length or orthonormality invariants fail, or provenance entries are
        empty.

    Notes
    -----
    ``OperatorRecord`` represents data only. It does not store Hermiticity
    tolerances, analysis results, serialization policy, alignment state, or
    unit-conversion policy. Exact structural equality is implemented with
    ``np.array_equal`` for the matrix, and the object is intentionally
    unhashable because exact array hashing is not safely defined.
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
        """Validate nested objects and canonicalize owned immutable storage.

        Raises
        ------
        TypeError
            If record string fields, nested public object fields, matrix scalar
            entries, or provenance mapping types violate the public boundary.
        ValueError
            If matrix, basis, state-space, or provenance invariants fail.
        """

        self._require_string(self.identifier, "operator-record identifier")
        self._require_string(self.operator_kind, "operator kind")
        if not isinstance(self.state_space, StateSpace):
            msg = "state_space must be a StateSpace"
            raise TypeError(msg)
        if not isinstance(self.basis, Basis):
            msg = "basis must be a Basis"
            raise TypeError(msg)
        if not isinstance(self.geometry, Geometry):
            msg = "geometry must be a Geometry"
            raise TypeError(msg)
        if not isinstance(self.energy_reference, EnergyReference):
            msg = "energy_reference must be an EnergyReference"
            raise TypeError(msg)
        self._reject_forbidden_matrix_scalars(self.matrix)
        matrix = np.array(self.matrix, dtype=np.complex128, copy=True, order="C")
        self._validate_matrix(matrix)
        immutable_matrix = self._make_immutable_matrix(matrix)
        object.__setattr__(self, "matrix", immutable_matrix)
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
        """Validate represented matrix invariants owned by OperatorRecord.

        Parameters
        ----------
        matrix
            Already canonical ``np.complex128`` matrix copied from caller input.

        Raises
        ------
        ValueError
            If ``matrix`` is not two-dimensional, is not square, contains
            nonfinite entries, has dimension inconsistent with ``state_space`` or
            ``basis``, or is paired with a non-orthonormal basis under schema
            version 1.

        Notes
        -----
        This private owner-local method is mechanical DataObject validation, not
        Hermiticity analysis or scientific acceptability.
        """

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
    def _require_string(value: object, name: str) -> None:
        """Validate a nonempty string field owned by ``OperatorRecord``.

        Parameters
        ----------
        value
            Candidate record identifier or operator-kind value.
        name
            Diagnostic field name.

        Raises
        ------
        TypeError
            If ``value`` is not a string.
        ValueError
            If ``value`` is empty.

        Notes
        -----
        This private owner-local method protects record-owned string fields and
        does not implement metadata compatibility or serializer policy.
        """

        if not isinstance(value, str):
            msg = f"{name} must be a string"
            raise TypeError(msg)
        if value == "":
            msg = f"{name} must not be empty"
            raise ValueError(msg)

    @staticmethod
    def _make_immutable_matrix(matrix: ComplexMatrix) -> ComplexMatrix:
        """Return a matrix view backed by immutable owned bytes.

        Parameters
        ----------
        matrix
            Canonical finite C-contiguous ``np.complex128`` matrix.

        Returns
        -------
        ComplexMatrix
            Read-only matrix whose base chain owns an immutable ``bytes`` buffer;
            NumPy cannot mark the view writeable with ``setflags(write=True)``.

        Notes
        -----
        This private method owns the operational-immutability mechanism for the
        public ``OperatorRecord.matrix`` field.
        """

        immutable_buffer = matrix.tobytes(order="C")
        immutable_vector = np.frombuffer(immutable_buffer, dtype=np.complex128)
        immutable_matrix = immutable_vector.reshape(matrix.shape)
        return cast(ComplexMatrix, immutable_matrix)

    @staticmethod
    def _reject_forbidden_matrix_scalars(matrix: object) -> None:
        """Reject scalar types that NumPy would otherwise coerce silently.

        Parameters
        ----------
        matrix
            Caller-supplied matrix-like object before complex NumPy coercion.

        Raises
        ------
        TypeError
            If any entry is Boolean, NumPy Boolean, string, or bytes, including
            numeric strings that NumPy could otherwise convert to numbers.

        Notes
        -----
        The method is private because it protects ``OperatorRecord`` matrix
        construction at the public Python/Rust scalar boundary.
        """

        # Inspect object-dtype entries before complex coercion so forbidden
        # booleans and numeric strings cannot become numerical matrix values.
        raw = np.asarray(matrix, dtype=object)
        for value in raw.flat:
            if isinstance(value, bool | np.bool_ | str | bytes):
                msg = "operator matrix entries must be numeric, not bool or string"
                raise TypeError(msg)

    @staticmethod
    def _copy_provenance(provenance: Mapping[str, str]) -> Mapping[str, str]:
        """Return an immutable string-to-string provenance mapping.

        Parameters
        ----------
        provenance
            Candidate mapping from provenance keys to provenance values.

        Returns
        -------
        Mapping[str, str]
            Defensive copy wrapped in ``MappingProxyType`` so later caller
            mutation cannot alter the record.

        Raises
        ------
        TypeError
            If ``provenance`` is not a mapping or any key/value is not a string.
        ValueError
            If any provenance key or value is empty.

        Notes
        -----
        This private method owns the ``OperatorRecord`` provenance invariant.
        Provenance is metadata and does not affect numerical matrix entries.
        """

        if not isinstance(provenance, Mapping):
            msg = "provenance must be a mapping from strings to strings"
            raise TypeError(msg)
        # Copy caller-owned mapping data before wrapping it in a read-only proxy
        # so later caller mutation cannot alter this immutable DataObject.
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
