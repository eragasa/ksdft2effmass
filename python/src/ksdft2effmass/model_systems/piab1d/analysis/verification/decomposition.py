"""Independent verification of kinetic-potential decomposition results."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

import numpy as np
from projectkoios.physkit.units import MatrixQuantity, ScalarQuantity, Unitless

from ksdft2effmass.analysis.operators import KineticPotentialDecompositionResult
from ksdft2effmass.verification import MaximumAbsoluteErrorComparison


@dataclass(frozen=True, slots=True)
class Piab1dKineticPotentialDecompositionReference:
    """Retain independent comparisons for one retained-space decomposition."""

    comparisons: Mapping[str, MaximumAbsoluteErrorComparison]

    def __post_init__(self) -> None:
        if not self.comparisons:
            raise ValueError("decomposition comparisons must be nonempty")
        object.__setattr__(
            self, "comparisons", MappingProxyType(dict(self.comparisons))
        )


@dataclass(frozen=True, slots=True, eq=False)
class Piab1dKineticPotentialDecompositionReferenceRequest:
    """Bind one admitted decomposition and its authoritative reduced Hamiltonian."""

    result: KineticPotentialDecompositionResult
    reduced_hamiltonian: MatrixQuantity

    def __post_init__(self) -> None:
        """Admit type, shape, and unit correlation for independent reconstruction."""
        if type(self.result) is not KineticPotentialDecompositionResult:
            raise TypeError("result must be KineticPotentialDecompositionResult")
        if not isinstance(self.reduced_hamiltonian, MatrixQuantity):
            raise TypeError("reduced_hamiltonian must be MatrixQuantity")
        if (
            self.reduced_hamiltonian.magnitude.shape
            != self.result.physical_kinetic.magnitude.shape
        ):
            raise ValueError("reduced_hamiltonian shape must match the decomposition")
        if self.reduced_hamiltonian.unit != self.result.physical_kinetic.unit:
            raise ValueError("reduced_hamiltonian unit must match the decomposition")


class Piab1dKineticPotentialDecompositionReferenceAnalyzer:
    """Reconstruct one bound decomposition and its model-class projections."""

    __slots__ = ("_request",)

    def __init__(
        self, request: Piab1dKineticPotentialDecompositionReferenceRequest
    ) -> None:
        if type(request) is not Piab1dKineticPotentialDecompositionReferenceRequest:
            raise TypeError(
                "request must be Piab1dKineticPotentialDecompositionReferenceRequest"
            )
        self._request = request

    @property
    def request(self) -> Piab1dKineticPotentialDecompositionReferenceRequest:
        """Return the complete immutable decomposition-reference request."""
        return self._request

    def execute(self) -> Piab1dKineticPotentialDecompositionReference:
        """Reconstruct decomposition and model-class projection identities.

        Returns
        -------
        Piab1dKineticPotentialDecompositionReference
            Eight independent comparisons covering components, reconstructions,
            projected matrices, residuals, and Frobenius norms.

        Raises
        ------
        ValueError
            The fixed scalar-to-real-symmetric model-class order differs.

        Notes
        -----
        Projection formulas are evaluated directly and do not call the production
        decomposition analyzer or model-class fitter.
        """
        result = self.request.result
        reduced_hamiltonian = self.request.reduced_hamiltonian
        hamiltonian = reduced_hamiltonian.magnitude
        shift = result.alternative_potential.magnitude
        rows, columns = np.indices(shift.shape)
        candidates = (
            np.eye(shift.shape[0]) * np.trace(shift) / shift.shape[0],
            np.diag(np.diag(shift)),
            np.where(np.abs(rows - columns) <= 1, shift, 0.0),
            shift,
        )
        names = ("scalar", "diagonal", "tridiagonal", "real_symmetric")
        if tuple(value.name for value in result.model_class_fits) != names:
            raise ValueError("decomposition model-class ordering differs")
        discrepancies = {
            "decomposition_physical_kinetic_maximum_absolute_error": float(
                np.max(np.abs(result.physical_kinetic.magnitude - hamiltonian))
            ),
            "decomposition_physical_potential_maximum_absolute_error": float(
                np.max(np.abs(result.physical_potential.magnitude))
            ),
            "decomposition_alternative_kinetic_maximum_absolute_error": float(
                np.max(
                    np.abs(result.alternative_kinetic.magnitude - (hamiltonian - shift))
                )
            ),
            "decomposition_physical_reconstruction_error": (
                result.physical_reconstruction_error.magnitude
            ),
            "decomposition_alternative_reconstruction_error": (
                result.alternative_reconstruction_error.magnitude
            ),
            "decomposition_model_fit_maximum_absolute_error": float(
                max(
                    np.max(np.abs(fit.best_fit.magnitude - candidate))
                    for fit, candidate in zip(
                        result.model_class_fits, candidates, strict=True
                    )
                )
            ),
            "decomposition_model_residual_maximum_absolute_error": float(
                max(
                    np.max(
                        np.abs(fit.unexplained_residual.magnitude - (shift - candidate))
                    )
                    for fit, candidate in zip(
                        result.model_class_fits, candidates, strict=True
                    )
                )
            ),
            "decomposition_model_norm_maximum_absolute_error": float(
                max(
                    abs(
                        fit.unexplained_frobenius_norm.magnitude
                        - np.linalg.norm(shift - candidate, ord="fro")
                    )
                    for fit, candidate in zip(
                        result.model_class_fits, candidates, strict=True
                    )
                )
            ),
        }
        unitless = Unitless()
        return Piab1dKineticPotentialDecompositionReference(
            comparisons={
                name: MaximumAbsoluteErrorComparison(
                    observed=ScalarQuantity(float(value), unitless),
                    reference=ScalarQuantity(0.0, unitless),
                    tolerance=ScalarQuantity(1.0e-12, unitless),
                )
                for name, value in discrepancies.items()
            }
        )
