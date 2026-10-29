"""Composition of independent PIAB1D reference analyses."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from ksdft2effmass.verification import MaximumAbsoluteErrorComparison

from ...result import Piab1dCalculationResult
from ...visualizations.data import Piab1dVisualizationData
from .core import Piab1dCoreReferenceAnalyzer, Piab1dCoreReferenceRequest
from .decomposition import (
    Piab1dKineticPotentialDecompositionReferenceAnalyzer,
    Piab1dKineticPotentialDecompositionReferenceRequest,
)
from .eigenpair_convergence import (
    Piab1dEigenpairSweepReferenceAnalyzer,
    Piab1dEigenpairSweepReferenceRequest,
)
from .finite_algebraic_diagnostics import (
    Piab1dFiniteAlgebraicDiagnosticsReferenceAnalyzer,
    Piab1dFiniteAlgebraicDiagnosticsReferenceRequest,
)
from .residual_norms import (
    Piab1dResidualNormSweepReferenceAnalyzer,
    Piab1dResidualNormSweepReferenceRequest,
)


@dataclass(frozen=True, slots=True)
class Piab1dIndependentReference:
    """Retain the disjoint comparison inventory from all reference analyses."""

    comparisons: Mapping[str, MaximumAbsoluteErrorComparison]

    def __post_init__(self) -> None:
        if not self.comparisons:
            raise ValueError("independent reference comparisons must be nonempty")
        object.__setattr__(
            self,
            "comparisons",
            MappingProxyType(dict(self.comparisons)),
        )


@dataclass(frozen=True, slots=True, eq=False)
class Piab1dIndependentReferenceRequest:
    """Bind one result and its verifier-derived visualization projection."""

    result: Piab1dCalculationResult
    visualization_data: Piab1dVisualizationData

    def __post_init__(self) -> None:
        """Admit the complete typed aggregate-reference request."""
        if type(self.result) is not Piab1dCalculationResult:
            raise TypeError("result must be Piab1dCalculationResult")
        if type(self.visualization_data) is not Piab1dVisualizationData:
            raise TypeError("visualization_data must be Piab1dVisualizationData")


class Piab1dIndependentReferenceAnalyzer:
    """Compose independent analyses for one bound PIAB1D subject."""

    __slots__ = ("_request",)

    def __init__(self, request: Piab1dIndependentReferenceRequest) -> None:
        if type(request) is not Piab1dIndependentReferenceRequest:
            raise TypeError("request must be Piab1dIndependentReferenceRequest")
        self._request = request

    @property
    def request(self) -> Piab1dIndependentReferenceRequest:
        """Return the complete immutable aggregate-reference request."""
        return self._request

    def execute(self) -> Piab1dIndependentReference:
        """Compose all independent PIAB1D reference comparisons.

        Returns
        -------
        Piab1dIndependentReference
            Immutable collision-free mapping of operation-qualified comparisons.

        Raises
        ------
        ValueError
            Independent comparison names collide or reconstructed values violate a
            scientific-operation contract.

        Notes
        -----
        This composition never invokes a production PIAB1D analyzer. Each reference
        owner reconstructs its target directly from declared equations and typed
        source data.
        """
        result = self.request.result
        visualization_data = self.request.visualization_data
        core = Piab1dCoreReferenceAnalyzer(
            Piab1dCoreReferenceRequest(result, visualization_data)
        ).execute()
        eigenpair_sweep = Piab1dEigenpairSweepReferenceAnalyzer(
            Piab1dEigenpairSweepReferenceRequest(result.eigenpair_sweep)
        ).execute()
        residual_norms = Piab1dResidualNormSweepReferenceAnalyzer(
            Piab1dResidualNormSweepReferenceRequest(result.residual_norm_sweep)
        ).execute()
        algebraic_diagnostics = Piab1dFiniteAlgebraicDiagnosticsReferenceAnalyzer(
            Piab1dFiniteAlgebraicDiagnosticsReferenceRequest(
                result.finite_algebraic_diagnostics
            )
        ).execute()
        decomposition = Piab1dKineticPotentialDecompositionReferenceAnalyzer(
            Piab1dKineticPotentialDecompositionReferenceRequest(
                result.kinetic_potential_decomposition,
                result.hamiltonian.matrix("reduced_hamiltonian"),
            )
        ).execute()
        inventories = (
            core.comparisons,
            eigenpair_sweep.comparisons,
            residual_norms.comparisons,
            algebraic_diagnostics.comparisons,
            decomposition.comparisons,
        )
        names: set[str] = set()
        comparisons: dict[str, MaximumAbsoluteErrorComparison] = {}
        for inventory in inventories:
            overlap = names.intersection(inventory)
            if overlap:
                raise ValueError(
                    "independent reference comparison names must be unique"
                )
            names.update(inventory)
            comparisons.update(inventory)
        return Piab1dIndependentReference(comparisons=comparisons)
