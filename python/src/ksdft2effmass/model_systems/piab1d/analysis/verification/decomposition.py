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


class Piab1dKineticPotentialDecompositionReferenceAnalyzer:
    """Reconstruct decomposition matrices and model-class projections."""

    __slots__ = ()

    def execute(
        self,
        result: KineticPotentialDecompositionResult,
        reduced_hamiltonian: MatrixQuantity,
    ) -> Piab1dKineticPotentialDecompositionReference:
        """Reconstruct decomposition and model-class projection identities.

        Parameters
        ----------
        result
            Production decomposition with physical and illustrative component pairs.
        reduced_hamiltonian
            Authoritative reduced Hamiltonian from the typed calculation result.

        Returns
        -------
        Piab1dKineticPotentialDecompositionReference
            Eight independent comparisons covering components, reconstructions,
            projected matrices, residuals, and Frobenius norms.

        Raises
        ------
        TypeError
            Either input has the wrong domain type.
        ValueError
            The fixed scalar-to-real-symmetric model-class order differs.

        Notes
        -----
        Projection formulas are evaluated directly and do not call the production
        decomposition analyzer or model-class fitter.
        """
        if not isinstance(result, KineticPotentialDecompositionResult):
            raise TypeError("result must be KineticPotentialDecompositionResult")
        if not isinstance(reduced_hamiltonian, MatrixQuantity):
            raise TypeError("reduced_hamiltonian must be MatrixQuantity")
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
