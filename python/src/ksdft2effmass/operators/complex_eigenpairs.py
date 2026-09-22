"""Retained complex-Hermitian eigenpairs and sparse algebraic residual analysis."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

import numpy as np

from .quantities import (
    ComplexMatrixQuantity,
    ComplexSparseMatrixQuantity,
    PhysicalUnit,
    Unitless,
    VectorQuantity,
)
from .sparse_hermiticity import ComplexSparseHermiticityResult

type EigenpairResidualUnit = PhysicalUnit | Unitless


class HermitianEigenpairSelection(StrEnum):
    """Supported ordering contract for retained Hermitian eigenpairs."""

    LOWEST = "lowest"


@dataclass(frozen=True, slots=True, eq=False)
class ComplexHermitianEigenpairResult:
    """Retain ascending selected eigenpairs of one complex sparse Hermitian matrix."""

    operator: ComplexSparseMatrixQuantity
    hermiticity: ComplexSparseHermiticityResult
    eigenvalues: VectorQuantity
    eigenvectors: ComplexMatrixQuantity
    selection: HermitianEigenpairSelection

    def __post_init__(self) -> None:
        """Validate dimensions, units, ordering, and binary64 orthonormality."""
        if type(self.operator) is not ComplexSparseMatrixQuantity:
            raise TypeError("operator must be ComplexSparseMatrixQuantity")
        if type(self.hermiticity) is not ComplexSparseHermiticityResult:
            raise TypeError("hermiticity must be ComplexSparseHermiticityResult")
        if self.hermiticity.matrix is not self.operator:
            raise ValueError("hermiticity result must correlate the exact operator")
        if not self.hermiticity.is_hermitian:
            raise ValueError("hermiticity result must pass")
        if type(self.eigenvalues) is not VectorQuantity:
            raise TypeError("eigenvalues must be VectorQuantity")
        if type(self.eigenvectors) is not ComplexMatrixQuantity:
            raise TypeError("eigenvectors must be ComplexMatrixQuantity")
        if type(self.selection) is not HermitianEigenpairSelection:
            raise TypeError("selection must be HermitianEigenpairSelection")
        rows, columns = self.operator.shape
        if rows != columns or rows <= 0:
            raise ValueError("operator must be nonempty and square")
        selected = self.eigenvalues.magnitude.size
        if selected <= 0 or selected > rows:
            raise ValueError("eigenvalues must select between one and all states")
        if self.eigenvectors.magnitude.shape != (rows, selected):
            raise ValueError("eigenvectors must match operator and selected dimensions")
        if self.eigenvalues.unit != self.operator.unit:
            raise ValueError("eigenvalue and operator units must agree")
        if type(self.eigenvectors.unit) is not Unitless:
            raise ValueError("eigenvectors must be unitless")
        if np.any(self.eigenvalues.magnitude[1:] < self.eigenvalues.magnitude[:-1]):
            raise ValueError("eigenvalues must be ordered nondecreasingly")
        vectors = self.eigenvectors.magnitude
        gram = vectors.conjugate().T @ vectors
        tolerance = 128.0 * np.finfo(np.float64).eps * float(max(rows, selected))
        if not np.allclose(
            gram,
            np.eye(selected, dtype=np.complex128),
            rtol=0.0,
            atol=tolerance,
        ):
            raise ValueError(
                "eigenvectors must be orthonormal within binary64 tolerance"
            )

    @property
    def full_dimension(self) -> int:
        """Return the represented operator dimension."""
        return self.operator.shape[0]

    @property
    def selected_count(self) -> int:
        """Return the retained lowest-eigenpair count."""
        return int(self.eigenvalues.magnitude.size)


@dataclass(frozen=True, slots=True)
class ComplexHermitianEigenpairResidualResult:
    """Retain algebraic residual norms for selected complex Hermitian eigenpairs."""

    eigenpairs: ComplexHermitianEigenpairResult
    residuals: tuple[float, ...]
    maximum_residual: float
    absolute_tolerance: float
    unit: EigenpairResidualUnit

    def __post_init__(self) -> None:
        """Validate exact count, unit, finite metrics, and retained maximum."""
        if type(self.eigenpairs) is not ComplexHermitianEigenpairResult:
            raise TypeError("eigenpairs must be ComplexHermitianEigenpairResult")
        if type(self.residuals) is not tuple or any(
            type(value) is not float for value in self.residuals
        ):
            raise TypeError("residuals must be a tuple of built-in floats")
        if len(self.residuals) != self.eigenpairs.selected_count:
            raise ValueError("residual count must equal selected eigenpair count")
        if any(not math.isfinite(value) or value < 0.0 for value in self.residuals):
            raise ValueError("eigenpair residuals must be finite and nonnegative")
        if type(self.maximum_residual) is not float:
            raise TypeError("maximum_residual must be a built-in float")
        if not math.isfinite(self.maximum_residual) or self.maximum_residual < 0.0:
            raise ValueError("maximum_residual must be finite and nonnegative")
        if self.maximum_residual != max(self.residuals):
            raise ValueError(
                "maximum_residual must equal the retained residual maximum"
            )
        if type(self.absolute_tolerance) is not float:
            raise TypeError("absolute_tolerance must be a built-in float")
        if not math.isfinite(self.absolute_tolerance) or self.absolute_tolerance < 0.0:
            raise ValueError("absolute_tolerance must be finite and nonnegative")
        if not isinstance(self.unit, PhysicalUnit | Unitless):
            raise TypeError("unit must be PhysicalUnit or Unitless")
        if self.unit != self.eigenpairs.operator.unit:
            raise ValueError("residual and operator units must agree")

    @property
    def passes(self) -> bool:
        """Return whether every retained eigenpair satisfies the caller tolerance."""
        return self.maximum_residual <= self.absolute_tolerance


class ComplexHermitianEigenpairResidualAnalyzer:
    """Evaluate ``||H v - lambda v||_2`` with sparse matrix multiplication."""

    __slots__ = ()

    def execute(
        self,
        eigenpairs: ComplexHermitianEigenpairResult,
        *,
        absolute_tolerance: float,
    ) -> ComplexHermitianEigenpairResidualResult:
        """Return one algebraic residual per retained eigenpair."""
        if type(eigenpairs) is not ComplexHermitianEigenpairResult:
            raise TypeError("eigenpairs must be ComplexHermitianEigenpairResult")
        if type(absolute_tolerance) is not float:
            raise TypeError("absolute_tolerance must be a built-in float")
        if not math.isfinite(absolute_tolerance) or absolute_tolerance < 0.0:
            raise ValueError("absolute_tolerance must be finite and nonnegative")
        vectors = eigenpairs.eigenvectors.magnitude
        values = eigenpairs.eigenvalues.magnitude
        residual_matrix = eigenpairs.operator.to_csr() @ vectors - vectors * values
        residuals = tuple(
            float(np.linalg.norm(residual_matrix[:, column], ord=2))
            for column in range(eigenpairs.selected_count)
        )
        return ComplexHermitianEigenpairResidualResult(
            eigenpairs,
            residuals,
            max(residuals),
            absolute_tolerance,
            eigenpairs.operator.unit,
        )
