"""Model-class fitting tools for finite represented operators."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import MatrixQuantity, ScalarQuantity


@dataclass(frozen=True, slots=True, eq=False)
class RetainedModelClassFitResult:
    """Retain one best-fit model, residual, and Frobenius norm."""

    name: str
    best_fit: MatrixQuantity
    unexplained_residual: MatrixQuantity
    unexplained_frobenius_norm: ScalarQuantity

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name:
            raise TypeError("name must be a nonempty string")
        if not isinstance(self.best_fit, MatrixQuantity):
            raise TypeError("best_fit must be MatrixQuantity")
        if not isinstance(self.unexplained_residual, MatrixQuantity):
            raise TypeError("unexplained_residual must be MatrixQuantity")
        if not isinstance(self.unexplained_frobenius_norm, ScalarQuantity):
            raise TypeError("unexplained_frobenius_norm must be ScalarQuantity")


class RetainedModelClassFitter:
    """Fit the four declared retained real-symmetric model classes."""

    __slots__ = ()

    def execute(
        self, target: MatrixQuantity
    ) -> tuple[RetainedModelClassFitResult, ...]:
        """Return ordered least-Frobenius fits for the declared nested classes."""
        if not isinstance(target, MatrixQuantity):
            raise TypeError("target must be MatrixQuantity")
        matrix = target.magnitude
        dimension = matrix.shape[0]
        if matrix.shape != (dimension, dimension):
            raise ValueError("target must be square")
        rows, columns = np.indices(matrix.shape)
        candidates = (
            (
                "scalar_identity",
                np.eye(dimension) * float(np.trace(matrix) / dimension),
            ),
            ("diagonal_in_retained_basis", np.diag(np.diag(matrix))),
            (
                "real_symmetric_tridiagonal",
                np.where(np.abs(rows - columns) <= 1, matrix, 0.0),
            ),
            ("arbitrary_real_symmetric", matrix.copy()),
        )
        return tuple(
            RetainedModelClassFitResult(
                name=name,
                best_fit=MatrixQuantity(candidate, target.unit),
                unexplained_residual=MatrixQuantity(matrix - candidate, target.unit),
                unexplained_frobenius_norm=ScalarQuantity(
                    float(np.linalg.norm(matrix - candidate, ord="fro")), target.unit
                ),
            )
            for name, candidate in candidates
        )
