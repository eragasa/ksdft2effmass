"""Finite dense- and sparse-matrix property verification."""

from __future__ import annotations

import math
from typing import Protocol

import numpy as np
import scipy.linalg as spl  # type: ignore[import-untyped]
import scipy.sparse as sp  # type: ignore[import-untyped]

from .quantities import (
    ComplexMatrix,
    ComplexMatrixQuantity,
    CsrComplexMatrixQuantity,
    CsrRealMatrixQuantity,
    RealMatrix,
    RealMatrixQuantity,
    Unitless,
)


class CsrSparseMatrix(Protocol):
    """Type one raw compressed-sparse-row matrix representation.

    Attributes
    ----------
    dtype
        NumPy dtype of the explicitly stored values.
    data
        One-dimensional explicitly stored values.
    indices
        One-dimensional column indices aligned with ``data``.
    indptr
        One-dimensional row offsets into ``data`` and ``indices``.
    shape
        Matrix row and column dimensions.
    """

    @property
    def dtype(self) -> np.dtype[np.generic]:
        """Return the sparse value dtype."""
        ...

    @property
    def data(self) -> np.ndarray[tuple[int], np.dtype[np.generic]]:
        """Return explicitly stored sparse values."""
        ...

    @property
    def indices(self) -> np.ndarray[tuple[int], np.dtype[np.signedinteger]]:
        """Return CSR column indices."""
        ...

    @property
    def indptr(self) -> np.ndarray[tuple[int], np.dtype[np.signedinteger]]:
        """Return CSR row offsets."""
        ...

    @property
    def shape(self) -> tuple[int, int]:
        """Return matrix dimensions."""
        ...


type VerifiedMatrix = (
    RealMatrixQuantity
    | ComplexMatrixQuantity
    | CsrRealMatrixQuantity
    | CsrComplexMatrixQuantity
)
type MatrixInput = RealMatrix | ComplexMatrix | CsrSparseMatrix | VerifiedMatrix


class VerifiedMatrixUtils:
    """Convert one verified finite matrix representation."""

    __slots__ = ("matrix",)

    matrix: VerifiedMatrix

    def __init__(self, matrix: VerifiedMatrix) -> None:
        """Retain one verified matrix representation."""
        if not isinstance(
            matrix,
            RealMatrixQuantity
            | ComplexMatrixQuantity
            | CsrRealMatrixQuantity
            | CsrComplexMatrixQuantity,
        ):
            raise TypeError("matrix must be a verified matrix quantity")
        self.matrix = matrix

    def to_dense_matrix(self) -> RealMatrixQuantity | ComplexMatrixQuantity:
        """Return an immutable dense matrix quantity with the retained unit."""
        if isinstance(self.matrix, RealMatrixQuantity | ComplexMatrixQuantity):
            return self.matrix
        return self.matrix.to_dense()


class MatrixVerifier:
    """Verify properties of one immutable finite matrix representation.

    Parameters
    ----------
    matrix
        A finite dense or sparse real or complex matrix, optionally carrying an
        explicit unit. Raw dense arrays must have exactly ``float64`` or
        ``complex128`` dtype. Raw SciPy CSR matrices and arrays must have one of
        those same dtypes. Raw inputs are copied into immutable storage so
        subsequent caller mutation cannot change verification outcomes. Units
        do not affect matrix properties and are not retained for raw inputs.

    Raises
    ------
    TypeError
        If ``matrix`` is not an accepted dense or sparse representation, or a raw
        representation does not have exactly ``float64`` or ``complex128`` dtype.
    ValueError
        If a raw dense array is not two-dimensional or any raw representation
        contains a nonfinite value.
    """

    __slots__ = ("matrix",)

    matrix: VerifiedMatrix

    def __init__(self, matrix: MatrixInput) -> None:
        """Validate ``matrix`` and retain an immutable canonical representation.

        Parameters
        ----------
        matrix
            Dense or sparse matrix representation accepted by the class contract.

        Raises
        ------
        TypeError
            If the representation or raw dtype is unsupported.
        ValueError
            If a raw representation has invalid rank or nonfinite entries.
        """
        if isinstance(
            matrix,
            RealMatrixQuantity
            | ComplexMatrixQuantity
            | CsrRealMatrixQuantity
            | CsrComplexMatrixQuantity,
        ):
            self.matrix = matrix
            return
        if isinstance(matrix, np.ndarray):
            self._require_raw_dtype(matrix.dtype)
            if matrix.ndim != 2:
                raise ValueError("raw dense matrix must be two-dimensional")
            if not np.all(np.isfinite(matrix)):
                raise ValueError("raw dense matrix must contain only finite values")
            if matrix.dtype == np.dtype(np.complex128):
                self.matrix = ComplexMatrixQuantity(
                    np.asarray(matrix, dtype=np.complex128),
                    Unitless(),
                )
            else:
                self.matrix = RealMatrixQuantity(
                    np.asarray(matrix, dtype=np.float64),
                    Unitless(),
                )
            return
        if isinstance(matrix, sp.csr_matrix | sp.csr_array):
            self._require_raw_dtype(matrix.dtype)
            if np.iscomplexobj(matrix.data):
                self.matrix = CsrComplexMatrixQuantity.from_csr(matrix, Unitless())
            else:
                self.matrix = CsrRealMatrixQuantity.from_csr(matrix, Unitless())
            return
        raise TypeError(
            "matrix must be a dense or CSR-sparse real or complex matrix representation"
        )

    def is_hermitian(
        self,
        *,
        rtol: float = 0.0,
        atol: float = 0.0,
    ) -> bool:
        r"""Return whether the matrix is Hermitian within explicit tolerances.

        Parameters
        ----------
        rtol
            Finite nonnegative built-in ``float`` interpreted as a dimensionless
            relative tolerance. The default ``0.0`` applies no relative tolerance.
        atol
            Finite nonnegative built-in ``float`` interpreted in the matrix entry
            unit when the source was a quantity. The default ``0.0`` applies no
            absolute tolerance.

        Returns
        -------
        bool
            Hermiticity decision under NumPy ``allclose`` semantics. Dense inputs
            delegate to :func:`scipy.linalg.ishermitian`. Sparse inputs evaluate
            the same elementwise criterion on the sparse difference without
            densification. With both defaults, the decision is exact for the
            retained finite representation. Rectangular matrices return ``False``.

        Raises
        ------
        TypeError
            If either tolerance is not exactly a built-in ``float``. Booleans,
            integers, NumPy scalars, and numeric strings are rejected.
        ValueError
            If either tolerance is negative or nonfinite.
        """
        self._require_tolerance(rtol, "rtol")
        self._require_tolerance(atol, "atol")
        if isinstance(self.matrix, CsrRealMatrixQuantity | CsrComplexMatrixQuantity):
            return self._sparse_is_hermitian(self.matrix, rtol=rtol, atol=atol)
        values = self.matrix.magnitude
        rows, columns = values.shape
        if rows != columns:
            return False
        return bool(
            spl.ishermitian(
                values,
                rtol=rtol,
                atol=atol,
            )
        )

    @staticmethod
    def _sparse_is_hermitian(
        matrix: CsrRealMatrixQuantity | CsrComplexMatrixQuantity,
        *,
        rtol: float,
        atol: float,
    ) -> bool:
        """Return sparse Hermiticity without materializing a dense matrix.

        Parameters
        ----------
        matrix
            Immutable canonical sparse matrix quantity.
        rtol
            Validated dimensionless relative tolerance.
        atol
            Validated absolute tolerance in the matrix entry unit.

        Returns
        -------
        bool
            Whether every structurally nonzero entry of ``A - A**H`` satisfies
            NumPy's elementwise closeness criterion. Implicit zero differences
            satisfy the criterion automatically.
        """
        rows, columns = matrix.shape
        if rows != columns:
            return False
        if rows == 0:
            return True
        represented = matrix.to_csr()
        adjoint = represented.conjugate().T.tocsr()
        difference = sp.coo_array(represented - adjoint)
        difference.sum_duplicates()
        difference.eliminate_zeros()
        if difference.nnz == 0:
            return True
        reference = np.asarray(adjoint[difference.row, difference.col]).reshape(-1)
        return bool(np.all(np.abs(difference.data) <= atol + rtol * np.abs(reference)))

    @staticmethod
    def _require_raw_dtype(dtype: np.dtype[np.generic]) -> None:
        """Require exact binary64 real or complex raw storage."""
        if dtype not in (np.dtype(np.float64), np.dtype(np.complex128)):
            raise TypeError("raw matrix dtype must be exactly float64 or complex128")

    @staticmethod
    def _require_tolerance(value: float, name: str) -> None:
        """Require one finite nonnegative built-in floating tolerance.

        Parameters
        ----------
        value
            Candidate tolerance.
        name
            Public parameter name used in diagnostics.

        Raises
        ------
        TypeError
            If ``value`` is not exactly a built-in ``float``.
        ValueError
            If ``value`` is negative or nonfinite.
        """
        if type(value) is not float:
            raise TypeError(f"{name} must be a built-in float")
        if not math.isfinite(value) or value < 0.0:
            raise ValueError(f"{name} must be finite and nonnegative")
