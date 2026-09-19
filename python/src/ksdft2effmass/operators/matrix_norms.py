"""Public norm analysis for finite represented dense and sparse matrices."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .quantities import MatrixQuantity, ScalarQuantity, SparseMatrixQuantity, Unitless

type RepresentedRealMatrix = MatrixQuantity | SparseMatrixQuantity


@dataclass(frozen=True, slots=True)
class RepresentedMatrixNormResult:
    """Retain Frobenius, spectral, and maximum-entry norms with explicit units."""

    frobenius: ScalarQuantity
    spectral: ScalarQuantity
    maximum_entry: ScalarQuantity

    def __post_init__(self) -> None:
        for quantity, name in (
            (self.frobenius, "frobenius"),
            (self.spectral, "spectral"),
            (self.maximum_entry, "maximum_entry"),
        ):
            if not isinstance(quantity, ScalarQuantity):
                raise TypeError(f"{name} must be ScalarQuantity")
            if quantity.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if not (self.frobenius.unit == self.spectral.unit == self.maximum_entry.unit):
            raise ValueError("matrix norm units must agree exactly")

    def normalized_by(
        self, reference: RepresentedMatrixNormResult
    ) -> RepresentedMatrixNormResult:
        """Return componentwise dimensionless ratios to a nonzero reference."""
        if not isinstance(reference, RepresentedMatrixNormResult):
            raise TypeError("reference must be RepresentedMatrixNormResult")
        if self.frobenius.unit != reference.frobenius.unit:
            raise ValueError("matrix and reference norm units must agree exactly")
        denominators = (
            reference.frobenius.magnitude,
            reference.spectral.magnitude,
            reference.maximum_entry.magnitude,
        )
        if any(value <= 0.0 for value in denominators):
            raise ValueError("reference norms must be positive")
        return RepresentedMatrixNormResult(
            frobenius=ScalarQuantity(
                self.frobenius.magnitude / denominators[0], Unitless()
            ),
            spectral=ScalarQuantity(
                self.spectral.magnitude / denominators[1], Unitless()
            ),
            maximum_entry=ScalarQuantity(
                self.maximum_entry.magnitude / denominators[2], Unitless()
            ),
        )


class RepresentedMatrixNormAnalyzer:
    """Evaluate historical binary64 matrix norms at an explicit metric boundary."""

    __slots__ = ()

    def execute(self, matrix: RepresentedRealMatrix) -> RepresentedMatrixNormResult:
        """Return NumPy-compatible Frobenius, spectral, and maximum-entry norms.

        Sparse input remains sparse until this explicitly requested complete norm
        analysis. The spectral norm requires a complete metric boundary and the
        version-one monograph campaigns require bitwise agreement with their retained
        dense NumPy calculation, so this action materializes sparse input here rather
        than before eigensolution.
        """
        if not isinstance(matrix, MatrixQuantity | SparseMatrixQuantity):
            raise TypeError("matrix must be a dense or sparse matrix quantity")
        represented = (
            matrix.magnitude
            if isinstance(matrix, MatrixQuantity)
            else matrix.to_dense().magnitude
        )
        dense = np.array(represented, dtype=np.float64, order="C", copy=True)
        if dense.size == 0:
            raise ValueError("matrix must be nonempty")
        return RepresentedMatrixNormResult(
            frobenius=ScalarQuantity(
                float(np.linalg.norm(dense, ord="fro")), matrix.unit
            ),
            spectral=ScalarQuantity(float(np.linalg.norm(dense, ord=2)), matrix.unit),
            maximum_entry=ScalarQuantity(float(np.max(np.abs(dense))), matrix.unit),
        )
