"""Explicit sparse eigensolver boundary for complex Hermitian operators."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.sparse import linalg as sparse_linalg  # type: ignore[import-untyped]

from .complex_eigenpairs import (
    ComplexHermitianEigenpairResidualAnalyzer,
    ComplexHermitianEigenpairResidualResult,
    ComplexHermitianEigenpairResult,
    HermitianEigenpairSelection,
)
from .quantities import (
    ComplexMatrixQuantity,
    ComplexSparseMatrixQuantity,
    Unitless,
    VectorQuantity,
)
from .sparse_hermiticity import ComplexSparseHermiticityResult


@dataclass(frozen=True, slots=True)
class ComplexHermitianEigensolverRequest:
    """Declare one iterative lowest-eigenpair solve and its acceptance tolerance."""

    selected_count: int
    solver_tolerance: float
    maximum_iterations: int | None
    initial_vector_seed: int
    residual_tolerance: float

    def __post_init__(self) -> None:
        """Validate counts and finite nonnegative tolerances."""
        if type(self.selected_count) is not int:
            raise TypeError("selected_count must be a built-in int")
        if self.selected_count <= 0:
            raise ValueError("selected_count must be positive")
        if type(self.solver_tolerance) is not float:
            raise TypeError("solver_tolerance must be a built-in float")
        if not math.isfinite(self.solver_tolerance) or self.solver_tolerance < 0.0:
            raise ValueError("solver_tolerance must be finite and nonnegative")
        if self.maximum_iterations is not None:
            if type(self.maximum_iterations) is not int:
                raise TypeError("maximum_iterations must be a built-in int or None")
            if self.maximum_iterations <= 0:
                raise ValueError("maximum_iterations must be positive when provided")
        if type(self.initial_vector_seed) is not int:
            raise TypeError("initial_vector_seed must be a built-in int")
        if not 0 <= self.initial_vector_seed < 2**64:
            raise ValueError("initial_vector_seed must lie in [0, 2**64)")
        if type(self.residual_tolerance) is not float:
            raise TypeError("residual_tolerance must be a built-in float")
        if not math.isfinite(self.residual_tolerance) or self.residual_tolerance < 0.0:
            raise ValueError("residual_tolerance must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class ComplexHermitianEigensolverResult:
    """Retain one sparse solve request and its independently evaluated residuals."""

    request: ComplexHermitianEigensolverRequest
    eigenpair_residuals: ComplexHermitianEigenpairResidualResult

    def __post_init__(self) -> None:
        """Correlate the request, selected count, and residual tolerance."""
        if type(self.request) is not ComplexHermitianEigensolverRequest:
            raise TypeError("request must be ComplexHermitianEigensolverRequest")
        if (
            type(self.eigenpair_residuals)
            is not ComplexHermitianEigenpairResidualResult
        ):
            raise TypeError(
                "eigenpair_residuals must be ComplexHermitianEigenpairResidualResult"
            )
        if (
            self.eigenpair_residuals.eigenpairs.selected_count
            != self.request.selected_count
        ):
            raise ValueError("selected eigenpair count must match the solve request")
        if (
            self.eigenpair_residuals.absolute_tolerance
            != self.request.residual_tolerance
        ):
            raise ValueError("residual tolerance must match the solve request")

    @property
    def eigenpairs(self) -> ComplexHermitianEigenpairResult:
        """Return the selected eigenpairs covered by residual analysis."""
        return self.eigenpair_residuals.eigenpairs

    @property
    def passes(self) -> bool:
        """Return whether the independently evaluated residuals pass."""
        return self.eigenpair_residuals.passes


class ComplexHermitianSparseEigenpairSolver:
    """Solve a proper lowest subset of a canonical sparse Hermitian operator."""

    __slots__ = ()

    def execute(
        self,
        operator: ComplexSparseMatrixQuantity,
        hermiticity: ComplexSparseHermiticityResult,
        request: ComplexHermitianEigensolverRequest,
    ) -> ComplexHermitianEigensolverResult:
        """Run sparse ``eigsh`` without materializing the represented operator."""
        if type(operator) is not ComplexSparseMatrixQuantity:
            raise TypeError("operator must be ComplexSparseMatrixQuantity")
        if type(hermiticity) is not ComplexSparseHermiticityResult:
            raise TypeError("hermiticity must be ComplexSparseHermiticityResult")
        if hermiticity.matrix is not operator:
            raise ValueError("hermiticity result must correlate the exact operator")
        if not hermiticity.is_hermitian:
            raise ValueError("hermiticity result must pass")
        if type(request) is not ComplexHermitianEigensolverRequest:
            raise TypeError("request must be ComplexHermitianEigensolverRequest")
        dimension = operator.shape[0]
        if request.selected_count >= dimension:
            raise ValueError(
                "sparse eigensolver requires a proper spectral subset; use an explicit "
                "dense boundary for a complete eigensystem"
            )
        generator = np.random.default_rng(request.initial_vector_seed)
        initial_vector = generator.standard_normal(
            dimension
        ) + 1.0j * generator.standard_normal(dimension)
        initial_vector /= np.linalg.norm(initial_vector)
        try:
            values, vectors = sparse_linalg.eigsh(
                operator.to_csr(),
                k=request.selected_count,
                which="SA",
                v0=initial_vector,
                tol=request.solver_tolerance,
                maxiter=request.maximum_iterations,
                return_eigenvectors=True,
            )
        except sparse_linalg.ArpackNoConvergence as error:
            raise RuntimeError(
                "complex Hermitian sparse eigensolver did not converge"
            ) from error
        order = np.argsort(values, kind="stable")
        ordered_values = np.asarray(values[order], dtype=np.float64)
        ordered_vectors = self.canonicalize_phases(
            np.asarray(vectors[:, order], dtype=np.complex128)
        )
        eigenpairs = ComplexHermitianEigenpairResult(
            operator,
            hermiticity,
            VectorQuantity(ordered_values, operator.unit),
            ComplexMatrixQuantity(ordered_vectors, Unitless()),
            HermitianEigenpairSelection.LOWEST,
        )
        residuals = ComplexHermitianEigenpairResidualAnalyzer().execute(
            eigenpairs,
            absolute_tolerance=request.residual_tolerance,
        )
        return ComplexHermitianEigensolverResult(request, residuals)

    @staticmethod
    def canonicalize_phases(
        eigenvectors: np.ndarray[tuple[int, int], np.dtype[np.complex128]],
    ) -> np.ndarray[tuple[int, int], np.dtype[np.complex128]]:
        """Choose one representative phase using each column's largest entry."""
        canonical = eigenvectors.copy()
        for column in range(canonical.shape[1]):
            vector = canonical[:, column]
            pivot = int(np.argmax(np.abs(vector)))
            pivot_value = vector[pivot]
            if abs(pivot_value) > 0.0:
                canonical[:, column] *= np.exp(-1.0j * np.angle(pivot_value))
        return canonical
