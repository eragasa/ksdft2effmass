"""Independent verification of PIAB1D residual-norm sweeps."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

import numpy as np
from projectkoios.physkit.linalg.matrix.norm import MatrixNorm
from projectkoios.physkit.units import MatrixQuantity, ScalarQuantity, Unitless

from ksdft2effmass.verification import MaximumAbsoluteErrorComparison

from ..residual_norms import Piab1dResidualNormSweepResult


@dataclass(frozen=True, slots=True)
class Piab1dResidualNormSweepReference:
    """Retain independent comparisons for residual-norm observations."""

    comparisons: Mapping[str, MaximumAbsoluteErrorComparison]

    def __post_init__(self) -> None:
        if not self.comparisons:
            raise ValueError("residual-norm comparisons must be nonempty")
        object.__setattr__(
            self, "comparisons", MappingProxyType(dict(self.comparisons))
        )


@dataclass(frozen=True, slots=True, eq=False)
class Piab1dResidualNormSweepReferenceRequest:
    """Bind one admitted residual-norm sweep for independent reconstruction."""

    result: Piab1dResidualNormSweepResult

    def __post_init__(self) -> None:
        """Admit the complete typed residual-norm reference request."""
        if type(self.result) is not Piab1dResidualNormSweepResult:
            raise TypeError("result must be Piab1dResidualNormSweepResult")


class Piab1dResidualNormSweepReferenceAnalyzer:
    """Reconstruct one bound PIAB1D operator-norm sweep analytically."""

    __slots__ = ("_request",)

    def __init__(self, request: Piab1dResidualNormSweepReferenceRequest) -> None:
        if type(request) is not Piab1dResidualNormSweepReferenceRequest:
            raise TypeError("request must be Piab1dResidualNormSweepReferenceRequest")
        self._request = request

    @property
    def request(self) -> Piab1dResidualNormSweepReferenceRequest:
        """Return the complete immutable residual-norm reference request."""
        return self._request

    def execute(self) -> Piab1dResidualNormSweepReference:
        """Reconstruct grid-indexed operator and residual norms.

        Returns
        -------
        Piab1dResidualNormSweepReference
            Independent comparisons for raw Hamiltonian, boundary, unmatched,
            consistent, and eigensolver residual norms and their normalized ratios.

        Raises
        ------
        ValueError
            A represented grid or comparison violates the residual-norm contract.

        Notes
        -----
        The method reconstructs dense reference matrices analytically and evaluates
        norms through the canonical PhysKit matrix-norm owner.
        """
        result = self.request.result
        expected_hamiltonian: list[tuple[float, ...]] = []
        expected_boundary: list[tuple[float, ...]] = []
        expected_unmatched: list[tuple[float, ...]] = []
        definition = result.definition
        for dimension in definition.interior_points:
            spacing = definition.length / (dimension + 1.0)
            prefactor = 1.0 / (2.0 * definition.mass * spacing**2)
            hamiltonian = np.diag(np.full(dimension, 2.0 * prefactor))
            hamiltonian += np.diag(np.full(dimension - 1, -prefactor), 1)
            hamiltonian += np.diag(np.full(dimension - 1, -prefactor), -1)
            nodes = np.arange(1, dimension + 1, dtype=np.float64)
            modes = np.arange(1, definition.retained_dimension + 1, dtype=np.float64)
            retained = np.sqrt(2.0 / (dimension + 1.0)) * np.sin(
                np.pi * nodes[:, None] * modes[None, :] / (dimension + 1.0)
            )
            projector = retained @ retained.T
            unmatched = projector @ hamiltonian @ projector - hamiltonian
            cyclic = hamiltonian.copy()
            cyclic[0, -1] = hamiltonian[0, 1]
            cyclic[-1, 0] = hamiltonian[1, 0]
            boundary = hamiltonian - cyclic
            expected = []
            for matrix in (hamiltonian, boundary, unmatched):
                quantity = MatrixQuantity(matrix, Unitless())
                expected.append(
                    tuple(
                        MatrixNorm(quantity, norm).result().magnitude
                        for norm in result.norms
                    )
                )
            expected_hamiltonian.append(expected[0])
            expected_boundary.append(expected[1])
            expected_unmatched.append(expected[2])
        hamiltonian = np.asarray(expected_hamiltonian)
        boundary = np.asarray(expected_boundary)
        unmatched = np.asarray(expected_unmatched)
        discrepancies = {
            "residual_norm_hamiltonian_maximum_absolute_error": float(
                np.max(np.abs(result.hamiltonian.magnitude - hamiltonian))
            ),
            "residual_norm_boundary_maximum_absolute_error": float(
                np.max(np.abs(result.boundary.magnitude - boundary))
            ),
            "residual_norm_unmatched_maximum_absolute_error": float(
                np.max(np.abs(result.unmatched.magnitude - unmatched))
            ),
            "residual_norm_consistent_maximum": float(
                np.max(result.consistent.magnitude)
            ),
            "residual_norm_eigensolver_relative_maximum": float(
                np.max(result.eigensolver_relative.magnitude)
            ),
            "residual_norm_boundary_ratio_maximum_absolute_error": float(
                np.max(
                    np.abs(
                        result.boundary_relative.magnitude
                        - result.boundary.magnitude / result.hamiltonian.magnitude
                    )
                )
            ),
            "residual_norm_unmatched_ratio_maximum_absolute_error": float(
                np.max(
                    np.abs(
                        result.unmatched_relative.magnitude
                        - result.unmatched.magnitude / result.hamiltonian.magnitude
                    )
                )
            ),
            "residual_norm_eigensolver_ratio_maximum_absolute_error": float(
                np.max(
                    np.abs(
                        result.eigensolver_relative.magnitude
                        - result.eigensolver.magnitude / result.hamiltonian.magnitude
                    )
                )
            ),
        }
        unitless = Unitless()
        raw_tolerance = float(256.0 * np.finfo(np.float64).eps * np.max(hamiltonian))
        return Piab1dResidualNormSweepReference(
            comparisons={
                name: MaximumAbsoluteErrorComparison(
                    observed=ScalarQuantity(value, unitless),
                    reference=ScalarQuantity(0.0, unitless),
                    tolerance=ScalarQuantity(
                        raw_tolerance
                        if name
                        in {
                            "residual_norm_hamiltonian_maximum_absolute_error",
                            "residual_norm_boundary_maximum_absolute_error",
                            "residual_norm_unmatched_maximum_absolute_error",
                            "residual_norm_consistent_maximum",
                        }
                        else 1.0e-12,
                        unitless,
                    ),
                )
                for name, value in discrepancies.items()
            }
        )
