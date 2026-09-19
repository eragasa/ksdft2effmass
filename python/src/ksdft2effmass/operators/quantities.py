"""Immutable typed quantities for public represented operators and analyses.

Pint owns unit parsing, dimensional compatibility, and conversion. Project records own
strict scalar and array types, operational immutability, and the distinction between a
physical unit and the first-class :class:`Unitless` unit.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
import pint
from scipy import sparse  # type: ignore[import-untyped]

type RealVector = npt.NDArray[np.float64]
type RealMatrix = npt.NDArray[np.float64]
type IntegerVector = npt.NDArray[np.int64]

MODEL_SYSTEM_PINT_REGISTRY = pint.UnitRegistry()
"""Fixed Pint registry used by public model-system unit records and actions."""


@dataclass(frozen=True, slots=True)
class PhysicalUnit:
    """Identify one non-dimensionless Pint unit expression.

    Parameters
    ----------
    expression
        Nonempty Pint unit expression. Dimensional validity is checked by
        :class:`PintUnitConverter` at the conversion boundary.
    """

    expression: str

    def __post_init__(self) -> None:
        if not isinstance(self.expression, str):
            raise TypeError("expression must be a string")
        if not self.expression:
            raise ValueError("expression must be nonempty")
        try:
            parsed = MODEL_SYSTEM_PINT_REGISTRY.Unit(self.expression)
        except (
            pint.errors.DefinitionSyntaxError,
            pint.errors.UndefinedUnitError,
        ) as error:
            raise ValueError("expression must identify a valid Pint unit") from error
        if parsed.dimensionless:
            raise ValueError("dimensionless values require Unitless")


@dataclass(frozen=True, slots=True)
class Unitless:
    """Represent the first-class unit of a genuinely dimensionless quantity."""

    @property
    def expression(self) -> str:
        """Return Pint's canonical dimensionless unit expression."""
        return "dimensionless"


type ModelSystemUnit = PhysicalUnit | Unitless


@dataclass(frozen=True, slots=True)
class ScalarQuantity:
    """Represent one finite binary64 scalar and its explicit unit."""

    magnitude: float
    unit: ModelSystemUnit

    def __post_init__(self) -> None:
        if type(self.magnitude) is not float:
            raise TypeError("magnitude must be a built-in float")
        if not np.isfinite(self.magnitude):
            raise ValueError("magnitude must be finite")
        if not isinstance(self.unit, PhysicalUnit | Unitless):
            raise TypeError("unit must be PhysicalUnit or Unitless")


@dataclass(frozen=True, slots=True, eq=False)
class VectorQuantity:
    """Represent one immutable finite binary64 vector and its explicit unit."""

    magnitude: RealVector
    unit: ModelSystemUnit

    def __post_init__(self) -> None:
        if not isinstance(self.magnitude, np.ndarray):
            raise TypeError("magnitude must be a numpy.ndarray")
        values = np.asarray(self.magnitude, dtype=np.float64)
        if values.ndim != 1 or not np.all(np.isfinite(values)):
            raise ValueError("magnitude must be a finite vector")
        if not isinstance(self.unit, PhysicalUnit | Unitless):
            raise TypeError("unit must be PhysicalUnit or Unitless")
        immutable = np.frombuffer(values.astype("<f8").tobytes(), dtype="<f8")
        object.__setattr__(self, "magnitude", immutable)


@dataclass(frozen=True, slots=True, eq=False)
class MatrixQuantity:
    """Represent one immutable finite binary64 matrix and its explicit unit."""

    magnitude: RealMatrix
    unit: ModelSystemUnit

    def __post_init__(self) -> None:
        if not isinstance(self.magnitude, np.ndarray):
            raise TypeError("magnitude must be a numpy.ndarray")
        values = np.asarray(self.magnitude, dtype=np.float64)
        if values.ndim != 2 or not np.all(np.isfinite(values)):
            raise ValueError("magnitude must be a finite matrix")
        if not isinstance(self.unit, PhysicalUnit | Unitless):
            raise TypeError("unit must be PhysicalUnit or Unitless")
        immutable = np.frombuffer(values.astype("<f8").tobytes(), dtype="<f8")
        object.__setattr__(self, "magnitude", immutable.reshape(values.shape))


@dataclass(frozen=True, slots=True, eq=False)
class SparseMatrixQuantity:
    """Represent one immutable finite binary64 matrix in canonical CSR storage.

    The three CSR component arrays are copied into immutable byte-backed NumPy
    arrays. :meth:`to_csr` returns a fresh SciPy sparse array, so callers cannot
    mutate the maintained quantity through the returned representation.
    """

    data: RealVector
    column_indices: IntegerVector
    row_offsets: IntegerVector
    shape: tuple[int, int]
    unit: ModelSystemUnit

    def __post_init__(self) -> None:
        if not isinstance(self.data, np.ndarray):
            raise TypeError("data must be a numpy.ndarray")
        if not isinstance(self.column_indices, np.ndarray):
            raise TypeError("column_indices must be a numpy.ndarray")
        if not isinstance(self.row_offsets, np.ndarray):
            raise TypeError("row_offsets must be a numpy.ndarray")
        if self.data.dtype.kind not in "iuf":
            raise TypeError("data must contain real numeric values excluding booleans")
        if self.column_indices.dtype.kind not in "iu":
            raise TypeError("column_indices must contain integers excluding booleans")
        if self.row_offsets.dtype.kind not in "iu":
            raise TypeError("row_offsets must contain integers excluding booleans")
        data = np.asarray(self.data, dtype=np.float64)
        columns = np.asarray(self.column_indices, dtype=np.int64)
        offsets = np.asarray(self.row_offsets, dtype=np.int64)
        if data.ndim != 1 or not np.all(np.isfinite(data)):
            raise ValueError("data must be a finite vector")
        if columns.ndim != 1 or offsets.ndim != 1:
            raise ValueError("CSR indices and offsets must be vectors")
        if not (
            isinstance(self.shape, tuple)
            and len(self.shape) == 2
            and all(type(dimension) is int for dimension in self.shape)
        ):
            raise TypeError("shape must be a pair of built-in integers")
        rows, columns_count = self.shape
        if rows < 0 or columns_count < 0:
            raise ValueError("shape dimensions must be nonnegative")
        if offsets.shape != (rows + 1,):
            raise ValueError("row_offsets length must equal rows plus one")
        if columns.shape != data.shape:
            raise ValueError("column_indices and data must have equal lengths")
        if np.any(data == 0.0):
            raise ValueError("canonical CSR data must not store explicit zeros")
        if offsets[0] != 0 or offsets[-1] != data.size:
            raise ValueError("row_offsets must span all stored entries")
        if np.any(offsets[1:] < offsets[:-1]):
            raise ValueError("row_offsets must be nondecreasing")
        if np.any(columns < 0) or np.any(columns >= columns_count):
            raise ValueError("column indices must lie within the matrix shape")
        for row in range(rows):
            row_columns = columns[offsets[row] : offsets[row + 1]]
            if np.any(row_columns[1:] <= row_columns[:-1]):
                raise ValueError(
                    "canonical CSR column indices must increase within each row"
                )
        if not isinstance(self.unit, PhysicalUnit | Unitless):
            raise TypeError("unit must be PhysicalUnit or Unitless")
        immutable_data = np.frombuffer(data.astype("<f8").tobytes(), dtype="<f8")
        immutable_columns = np.frombuffer(columns.astype("<i8").tobytes(), dtype="<i8")
        immutable_offsets = np.frombuffer(offsets.astype("<i8").tobytes(), dtype="<i8")
        object.__setattr__(self, "data", immutable_data)
        object.__setattr__(self, "column_indices", immutable_columns)
        object.__setattr__(self, "row_offsets", immutable_offsets)

    @classmethod
    def from_csr(
        cls,
        magnitude: sparse.spmatrix | sparse.sparray,
        unit: ModelSystemUnit,
    ) -> SparseMatrixQuantity:
        """Canonicalize one SciPy sparse matrix as an immutable CSR quantity."""
        if not isinstance(magnitude, sparse.spmatrix | sparse.sparray):
            raise TypeError("magnitude must be a SciPy sparse matrix or sparse array")
        if magnitude.dtype.kind not in "iuf":
            raise TypeError(
                "magnitude must contain real numeric values excluding booleans"
            )
        canonical = sparse.csr_array(magnitude, dtype=np.float64)
        canonical.sum_duplicates()
        canonical.eliminate_zeros()
        canonical.sort_indices()
        return cls(
            data=np.asarray(canonical.data, dtype=np.float64),
            column_indices=np.asarray(canonical.indices, dtype=np.int64),
            row_offsets=np.asarray(canonical.indptr, dtype=np.int64),
            shape=(int(canonical.shape[0]), int(canonical.shape[1])),
            unit=unit,
        )

    @property
    def nonzero_count(self) -> int:
        """Return the number of explicitly stored nonzero entries."""
        return int(self.data.size)

    def to_csr(self) -> sparse.csr_array:
        """Return a fresh SciPy CSR array with the represented values."""
        return sparse.csr_array(
            (
                self.data.copy(),
                self.column_indices.copy(),
                self.row_offsets.copy(),
            ),
            shape=self.shape,
            dtype=np.float64,
        )

    def to_dense(self) -> MatrixQuantity:
        """Materialize the represented matrix at an explicit dense boundary."""
        return MatrixQuantity(np.asarray(self.to_csr().toarray()), self.unit)


class PintUnitConverter:
    """Own Pint-backed validation, dimensional compatibility, and conversion."""

    __slots__ = ("registry",)

    registry: pint.UnitRegistry

    def __init__(self) -> None:
        """Construct an isolated registry using Pint's maintained definitions."""
        self.registry = MODEL_SYSTEM_PINT_REGISTRY

    def validate(self, unit: ModelSystemUnit) -> None:
        """Validate that one project unit is a parseable Pint unit."""
        if not isinstance(unit, PhysicalUnit | Unitless):
            raise TypeError("unit must be PhysicalUnit or Unitless")
        parsed = self.registry.Unit(unit.expression)
        if isinstance(unit, Unitless) and not parsed.dimensionless:
            raise ValueError("Unitless must be dimensionless")
        if isinstance(unit, PhysicalUnit) and parsed.dimensionless:
            raise ValueError("PhysicalUnit must not be dimensionless")

    def compatible(self, left: ModelSystemUnit, right: ModelSystemUnit) -> bool:
        """Return whether two validated units have equal dimensionality."""
        self.validate(left)
        self.validate(right)
        left_unit = self.registry.Unit(left.expression)
        right_unit = self.registry.Unit(right.expression)
        return bool(left_unit.is_compatible_with(right_unit))

    def conversion_factor(
        self, source: ModelSystemUnit, target: ModelSystemUnit
    ) -> float:
        """Return the multiplicative factor from ``source`` to ``target``.

        Raises
        ------
        ValueError
            If the units have incompatible dimensionality.
        """
        self.validate(source)
        self.validate(target)
        if not self.compatible(source, target):
            raise ValueError("source and target units are dimensionally incompatible")
        quantity = self.registry.Quantity(1.0, source.expression)
        return float(quantity.to(target.expression).magnitude)

    def convert_scalar(
        self, quantity: ScalarQuantity, target: ModelSystemUnit
    ) -> ScalarQuantity:
        """Convert one scalar quantity to a compatible target unit."""
        if not isinstance(quantity, ScalarQuantity):
            raise TypeError("quantity must be ScalarQuantity")
        factor = self.conversion_factor(quantity.unit, target)
        return ScalarQuantity(quantity.magnitude * factor, target)

    def convert_vector(
        self, quantity: VectorQuantity, target: ModelSystemUnit
    ) -> VectorQuantity:
        """Convert one vector quantity to a compatible target unit."""
        if not isinstance(quantity, VectorQuantity):
            raise TypeError("quantity must be VectorQuantity")
        factor = self.conversion_factor(quantity.unit, target)
        return VectorQuantity(quantity.magnitude * factor, target)

    def convert_matrix(
        self, quantity: MatrixQuantity, target: ModelSystemUnit
    ) -> MatrixQuantity:
        """Convert one dense matrix quantity to a compatible target unit."""
        if not isinstance(quantity, MatrixQuantity):
            raise TypeError("quantity must be MatrixQuantity")
        factor = self.conversion_factor(quantity.unit, target)
        return MatrixQuantity(quantity.magnitude * factor, target)

    def convert_sparse_matrix(
        self, quantity: SparseMatrixQuantity, target: ModelSystemUnit
    ) -> SparseMatrixQuantity:
        """Convert one sparse matrix quantity to a compatible target unit."""
        if not isinstance(quantity, SparseMatrixQuantity):
            raise TypeError("quantity must be SparseMatrixQuantity")
        factor = self.conversion_factor(quantity.unit, target)
        return SparseMatrixQuantity.from_csr(quantity.to_csr() * factor, target)


MODEL_SYSTEM_UNIT_CONVERTER = PintUnitConverter()
"""Shared converter using one fixed Pint registry for model-system operations."""
