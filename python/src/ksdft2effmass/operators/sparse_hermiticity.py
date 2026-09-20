r"""Sparse fixed-representation Hermiticity analysis for complex matrix quantities.

For a canonical complex sparse matrix :math:`H`, the analyzer computes

.. math::

   \varepsilon_{\mathrm H}=\max_{i,j}|H_{ij}-H_{ji}^{*}|

without materializing a dense matrix. The residual and caller tolerance use the exact
unit retained by the input quantity. Passing establishes only this represented software
criterion, not physical validity or scientific validation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .quantities import ComplexSparseMatrixQuantity, ModelSystemUnit


@dataclass(frozen=True, slots=True)
class ComplexSparseHermiticityResult:
    """Record caller-toleranced sparse complex Hermiticity analysis.

    Parameters
    ----------
    matrix
        Exact immutable sparse matrix quantity analyzed.
    maximum_absolute_residual
        Entrywise maximum of ``abs(H - H.conjugate().T)`` in ``matrix.unit``.
    absolute_tolerance
        Nonnegative finite caller tolerance in ``matrix.unit``.
    """

    matrix: ComplexSparseMatrixQuantity
    maximum_absolute_residual: float
    absolute_tolerance: float

    def __post_init__(self) -> None:
        """Validate retained input and finite nonnegative result scalars."""
        if type(self.matrix) is not ComplexSparseMatrixQuantity:
            raise TypeError("matrix must be ComplexSparseMatrixQuantity")
        for value, name in (
            (self.maximum_absolute_residual, "maximum_absolute_residual"),
            (self.absolute_tolerance, "absolute_tolerance"),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")

    @property
    def is_hermitian(self) -> bool:
        """Return whether the residual satisfies the inclusive caller tolerance."""
        return self.maximum_absolute_residual <= self.absolute_tolerance

    @property
    def unit(self) -> ModelSystemUnit:
        """Return the exact unit shared by residual and tolerance."""
        return self.matrix.unit


class ComplexSparseHermiticityAnalyzer:
    """Analyze one canonical sparse complex matrix without densification."""

    __slots__ = ()

    def execute(
        self,
        matrix: ComplexSparseMatrixQuantity,
        *,
        absolute_tolerance: float,
    ) -> ComplexSparseHermiticityResult:
        """Return the entrywise maximum Hermiticity residual and tolerance.

        Raises
        ------
        TypeError
            If the matrix or tolerance has the wrong semantic type.
        ValueError
            If the matrix is nonsquare, the tolerance is negative or nonfinite, or
            sparse subtraction produces a nonfinite residual intermediate.
        """
        if type(matrix) is not ComplexSparseMatrixQuantity:
            raise TypeError("matrix must be ComplexSparseMatrixQuantity")
        if type(absolute_tolerance) is not float:
            raise TypeError("absolute_tolerance must be a built-in float")
        if not math.isfinite(absolute_tolerance) or absolute_tolerance < 0.0:
            raise ValueError("absolute_tolerance must be finite and nonnegative")
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Hermiticity analysis requires a square matrix")
        represented = matrix.to_csr()
        with np.errstate(over="ignore", invalid="ignore"):
            residual_matrix = represented - represented.conjugate().transpose()
        residual_matrix.sum_duplicates()
        residual_matrix.eliminate_zeros()
        if residual_matrix.data.size == 0:
            maximum = 0.0
        else:
            magnitudes = np.abs(residual_matrix.data)
            if not np.all(np.isfinite(magnitudes)):
                raise ValueError("Hermiticity residual must remain finite")
            maximum = float(np.max(magnitudes))
        if not math.isfinite(maximum):
            raise ValueError("Hermiticity residual must remain finite")
        return ComplexSparseHermiticityResult(matrix, maximum, absolute_tolerance)
