"""Independent verification of finite PIAB1D algebraic diagnostics."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

import numpy as np
from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.verification import MaximumAbsoluteErrorComparison

from ..finite_algebraic_diagnostics import Piab1dFiniteAlgebraicDiagnostics


@dataclass(frozen=True, slots=True)
class Piab1dFiniteAlgebraicDiagnosticsReference:
    """Retain scale-aware comparisons for finite algebraic discrepancies."""

    comparisons: Mapping[str, MaximumAbsoluteErrorComparison]

    def __post_init__(self) -> None:
        if not self.comparisons:
            raise ValueError("finite algebraic comparisons must be nonempty")
        object.__setattr__(
            self, "comparisons", MappingProxyType(dict(self.comparisons))
        )


@dataclass(frozen=True, slots=True, eq=False)
class Piab1dFiniteAlgebraicDiagnosticsReferenceRequest:
    """Bind one admitted finite-algebraic diagnostic result for verification."""

    result: Piab1dFiniteAlgebraicDiagnostics

    def __post_init__(self) -> None:
        """Admit the complete typed finite-algebraic reference request."""
        if type(self.result) is not Piab1dFiniteAlgebraicDiagnostics:
            raise TypeError("result must be Piab1dFiniteAlgebraicDiagnostics")


class Piab1dFiniteAlgebraicDiagnosticsReferenceAnalyzer:
    """Apply independent bounds to one bound algebraic-diagnostic result."""

    __slots__ = ("_request",)

    def __init__(
        self, request: Piab1dFiniteAlgebraicDiagnosticsReferenceRequest
    ) -> None:
        if type(request) is not Piab1dFiniteAlgebraicDiagnosticsReferenceRequest:
            raise TypeError(
                "request must be Piab1dFiniteAlgebraicDiagnosticsReferenceRequest"
            )
        self._request = request

    @property
    def request(self) -> Piab1dFiniteAlgebraicDiagnosticsReferenceRequest:
        """Return the complete immutable finite-algebraic reference request."""
        return self._request

    def execute(self) -> Piab1dFiniteAlgebraicDiagnosticsReference:
        """Evaluate independently derived floating-point diagnostic bounds.

        Returns
        -------
        Piab1dFiniteAlgebraicDiagnosticsReference
            Comparisons against dimension- and operator-scale-aware bounds.

        Raises
        ------
        ValueError
            Grid metadata or a diagnostic observation violates its typed contract.

        Notes
        -----
        These bounds qualify finite floating-point identities. They do not measure
        continuum discretization error or scientific-model validity.
        """
        result = self.request.result
        definition = result.definition
        maximum_dimension = max(definition.interior_points)
        spacing = definition.length / (maximum_dimension + 1.0)
        prefactor = 1.0 / (2.0 * definition.mass * spacing**2)
        hamiltonian_frobenius = prefactor * np.sqrt(6.0 * maximum_dimension - 2.0)
        energy_tolerance = float(
            1024.0
            * np.finfo(np.float64).eps
            * maximum_dimension
            * hamiltonian_frobenius
        )
        projector_tolerance = float(
            1024.0 * np.finfo(np.float64).eps * maximum_dimension
        )
        observations = {
            "finite_algebraic_discrete_spectrum_maximum": result.discrete_spectrum,
            "finite_algebraic_spectral_reconstruction_maximum": (
                result.spectral_reconstruction
            ),
            "finite_algebraic_projector_idempotency_maximum": (
                result.projector_idempotency
            ),
            "finite_algebraic_retained_coordinate_maximum": result.retained_coordinates,
            "finite_algebraic_retained_embedding_maximum": result.retained_embedding,
            "finite_algebraic_spectral_leakage_maximum": result.spectral_leakage,
        }
        unitless = Unitless()
        return Piab1dFiniteAlgebraicDiagnosticsReference(
            comparisons={
                name: MaximumAbsoluteErrorComparison(
                    observed=ScalarQuantity(
                        float(np.max(observation.magnitude)), unitless
                    ),
                    reference=ScalarQuantity(0.0, unitless),
                    tolerance=ScalarQuantity(
                        projector_tolerance
                        if name == "finite_algebraic_projector_idempotency_maximum"
                        else energy_tolerance,
                        unitless,
                    ),
                )
                for name, observation in observations.items()
            }
        )
