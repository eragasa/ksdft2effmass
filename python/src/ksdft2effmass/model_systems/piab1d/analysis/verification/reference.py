"""Composition of independent PIAB1D reference analyses."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from ksdft2effmass.verification import MaximumAbsoluteErrorComparison

from ...result import Piab1dCalculationResult
from ...visualizations.data import Piab1dVisualizationData
from .core import Piab1dCoreReferenceAnalyzer
from .decomposition import (
    Piab1dKineticPotentialDecompositionReferenceAnalyzer,
)
from .eigenpair_convergence import Piab1dEigenpairSweepReferenceAnalyzer
from .finite_algebraic_diagnostics import (
    Piab1dFiniteAlgebraicDiagnosticsReferenceAnalyzer,
)
from .residual_norms import Piab1dResidualNormSweepReferenceAnalyzer


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


class Piab1dIndependentReferenceAnalyzer:
    """Compose independent operation-specific PIAB1D reference analyses."""

    __slots__ = (
        "core_analyzer",
        "eigenpair_sweep_analyzer",
        "residual_norm_sweep_analyzer",
        "finite_algebraic_diagnostics_analyzer",
        "decomposition_analyzer",
    )

    def __init__(self) -> None:
        self.core_analyzer = Piab1dCoreReferenceAnalyzer()
        self.eigenpair_sweep_analyzer = Piab1dEigenpairSweepReferenceAnalyzer()
        self.residual_norm_sweep_analyzer = Piab1dResidualNormSweepReferenceAnalyzer()
        self.finite_algebraic_diagnostics_analyzer = (
            Piab1dFiniteAlgebraicDiagnosticsReferenceAnalyzer()
        )
        self.decomposition_analyzer = (
            Piab1dKineticPotentialDecompositionReferenceAnalyzer()
        )

    def execute(
        self,
        result: Piab1dCalculationResult,
        visualization_data: Piab1dVisualizationData,
    ) -> Piab1dIndependentReference:
        """Compose all independent PIAB1D reference comparisons.

        Parameters
        ----------
        result
            Typed production calculation aggregate.
        visualization_data
            Verifier-derived visualization projection reconstructed from ``result``.

        Returns
        -------
        Piab1dIndependentReference
            Immutable collision-free mapping of operation-qualified comparisons.

        Raises
        ------
        TypeError
            A supplied aggregate has the wrong type.
        ValueError
            Independent comparison names collide or reconstructed values violate a
            scientific-operation contract.

        Notes
        -----
        This composition never invokes a production PIAB1D analyzer. Each reference
        owner reconstructs its target directly from declared equations and typed
        source data.
        """
        core = self.core_analyzer.execute(result, visualization_data)
        eigenpair_sweep = self.eigenpair_sweep_analyzer.execute(result.eigenpair_sweep)
        residual_norms = self.residual_norm_sweep_analyzer.execute(
            result.residual_norm_sweep
        )
        algebraic_diagnostics = self.finite_algebraic_diagnostics_analyzer.execute(
            result.finite_algebraic_diagnostics
        )
        decomposition = self.decomposition_analyzer.execute(
            result.kinetic_potential_decomposition,
            result.hamiltonian.matrix("reduced_hamiltonian"),
        )
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
