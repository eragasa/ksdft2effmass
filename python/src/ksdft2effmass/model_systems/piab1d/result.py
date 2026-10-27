"""Typed root result consumed by PIAB1D verification."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Self

import numpy as np
from projectkoios.physkit.units import Unitless

from ksdft2effmass.analysis import (
    RelativeErrorConvergenceResult,
    TailProbabilitySelection,
)
from ksdft2effmass.analysis.operators import KineticPotentialDecompositionResult
from ksdft2effmass.model_systems.result_sections import (
    AnalyticalSamplingResultSection,
    EigensystemResultSection,
    HamiltonianResultSection,
    QuadratureResultSection,
    SpectralReductionResultSection,
)
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .analysis.finite_algebraic_diagnostics import Piab1dFiniteAlgebraicDiagnostics
from .analysis.grid_sweep import Piab1dEigenpairSweepResult
from .analysis.residual_norms import Piab1dResidualNormSweepResult
from .configuration import Piab1dConfiguration
from .diagnostics import Piab1dDiagnostics


@dataclass(frozen=True, slots=True)
class Piab1dConvergenceResult(BaseTypedRecord):
    """Retain a declared refinement inventory and convergence analysis.

    Parameters
    ----------
    interior_points
        Positive represented dimensions in refinement order.
    modes
        Positive one-based continuum modes represented by analysis columns.
    analysis
        Typed spacings, relative errors, and observed orders.

    Raises
    ------
    TypeError
        An inventory or analysis value has the wrong type.
    """

    interior_points: tuple[int, ...]
    modes: tuple[int, ...]
    analysis: RelativeErrorConvergenceResult

    def __post_init__(self) -> None:
        for values, name in (
            (self.interior_points, "interior_points"),
            (self.modes, "modes"),
        ):
            if (
                not isinstance(values, tuple)
                or not values
                or any(type(value) is not int or value <= 0 for value in values)
            ):
                raise TypeError(f"{name} must contain positive built-in integers")
        if not isinstance(self.analysis, RelativeErrorConvergenceResult):
            raise TypeError("analysis must be RelativeErrorConvergenceResult")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "interior_points": self.interior_points,
            "modes": self.modes,
            "analysis": self.analysis,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {"interior_points", "modes", "analysis"}:
            raise ValueError("convergence-result fields do not match")
        points = values["interior_points"]
        modes = values["modes"]
        analysis_value = values["analysis"]
        if not isinstance(points, tuple) or not isinstance(modes, tuple):
            raise TypeError("convergence inventories must decode to tuples")
        if not isinstance(analysis_value, Mapping):
            raise TypeError("convergence analysis must decode to a mapping")
        return cls(
            interior_points=points,
            modes=modes,
            analysis=RelativeErrorConvergenceResult.from_dict(analysis_value),
        )


@dataclass(frozen=True, slots=True)
class Piab1dSelectionResult(BaseTypedRecord):
    """Retain one parameterized tail-probability selection.

    Parameters
    ----------
    beta
        Positive finite inverse-energy parameter in the nondimensional convention.
    selection
        Reusable probabilities, omitted tails, tolerance, and selected count.

    Raises
    ------
    TypeError
        ``selection`` has the wrong domain type.
    ValueError
        ``beta`` is nonfinite or nonpositive.

    Notes
    -----
    This record stores an illustrative truncation criterion. It does not declare a
    physical thermal ensemble.
    """

    beta: float
    selection: TailProbabilitySelection

    def __post_init__(self) -> None:
        if (
            type(self.beta) is not float
            or not np.isfinite(self.beta)
            or self.beta <= 0.0
        ):
            raise ValueError("beta must be a positive finite built-in float")
        if not isinstance(self.selection, TailProbabilitySelection):
            raise TypeError("selection must be TailProbabilitySelection")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {"beta": self.beta, "selection": self.selection}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if not {"beta", "selection"}.issubset(values):
            raise ValueError("selection-result fields are incomplete")
        beta = values["beta"]
        selection_value = values["selection"]
        if type(beta) is not float:
            raise TypeError("beta must decode to a built-in float")
        if not isinstance(selection_value, Mapping):
            raise TypeError("selection must decode to a mapping")
        return cls(
            beta=beta,
            selection=TailProbabilitySelection.from_dict(selection_value),
        )


@dataclass(frozen=True, slots=True, eq=False)
class Piab1dCalculationResult(BaseTypedRecord):
    """Compose every authoritative section required by PIAB1D verification.

    Parameters
    ----------
    calculation_family
        Exact ``"piab1d-spectral-reduction"`` calculation-family identity.
    configuration
        Nondimensional model and represented-grid declaration.
    hamiltonian
        Parent, reduced, embedded, cyclic-reference, and boundary matrices.
    eigensystem
        Computed and analytical spectra plus Euclidean and quadrature eigenvectors.
    reduction
        Coordinate maps, orthogonal blocks, and reduction residual analyses.
    quadrature
        Rule identity, version, name, spacing, interior weights, weighted Gram matrix,
        and weighted projector.
    diagnostics
        Tolerance-bearing core diagnostic observations.
    analytical_sampling
        Continuum coordinates and wavefunction samples used by visualization.
    convergence
        Declared low-mode refinement series.
    selection
        Parameterized tail-probability retained-dimension selection.
    eigenpair_sweep
        Full represented-spectrum observations across all declared grids.
    residual_norm_sweep
        Canonical operator and eigensolver norm observations.
    finite_algebraic_diagnostics
        Grid-indexed finite matrix-identity discrepancies.
    kinetic_potential_decomposition
        Physical and shifted retained-space decompositions with model-class fits.
    supplementary
        Additional typed producer metadata not interpreted by core verification.

    Raises
    ------
    TypeError
        A section has the wrong exact domain type.
    ValueError
        Calculation identity, dimensions, units, grids, or correlated conventions
        disagree across sections.

    Notes
    -----
    Authoritative scientific values occur once in this aggregate. Visualization data
    is a verifier-derived projection and is not stored as a second authority.
    """

    calculation_family: str
    configuration: Piab1dConfiguration
    hamiltonian: HamiltonianResultSection
    eigensystem: EigensystemResultSection
    reduction: SpectralReductionResultSection
    quadrature: QuadratureResultSection
    diagnostics: Piab1dDiagnostics
    analytical_sampling: AnalyticalSamplingResultSection
    convergence: Piab1dConvergenceResult
    selection: Piab1dSelectionResult
    eigenpair_sweep: Piab1dEigenpairSweepResult
    residual_norm_sweep: Piab1dResidualNormSweepResult
    finite_algebraic_diagnostics: Piab1dFiniteAlgebraicDiagnostics
    kinetic_potential_decomposition: KineticPotentialDecompositionResult
    supplementary: Mapping[str, SerializableValue]

    def __post_init__(self) -> None:
        if self.calculation_family != "piab1d-spectral-reduction":
            raise ValueError("calculation_family does not identify PIAB1D reduction")
        if not isinstance(
            self.kinetic_potential_decomposition,
            KineticPotentialDecompositionResult,
        ):
            raise TypeError("kinetic-potential decomposition has the wrong result type")
        if not isinstance(self.supplementary, Mapping):
            raise TypeError("supplementary must be a mapping")
        energy_units = {
            self.hamiltonian.matrix("parent_hamiltonian").unit,
            self.eigensystem.vector("computed_discrete").unit,
            self.reduction.matrix("retained").unit,
            self.kinetic_potential_decomposition.physical_kinetic.unit,
        }
        if len(energy_units) != 1:
            raise ValueError(
                "Hamiltonian, eigensystem, and reduction energy units must agree"
            )
        if any(not isinstance(unit, Unitless) for unit in energy_units):
            raise ValueError("PIAB1D energy values must use the nondimensional unit")
        dimension = self.configuration.interior_points
        retained = self.configuration.retained_dimension
        decomposition_shape = (
            self.kinetic_potential_decomposition.physical_kinetic.magnitude.shape
        )
        if decomposition_shape != (retained, retained):
            raise ValueError("decomposition must act on the retained coordinate space")
        if self.hamiltonian.matrix("parent_hamiltonian").magnitude.shape != (
            dimension,
            dimension,
        ):
            raise ValueError(
                "configuration and represented Hamiltonian dimensions disagree"
            )
        if self.reduction.matrix("reduction").magnitude.shape != (
            retained,
            dimension,
        ):
            raise ValueError("configuration and reduction-map dimensions disagree")
        if self.quadrature.text("rule_identifier") != (
            "projectkoios.numerics.quadrature.uniform_closed_interval_trapezoidal"
        ):
            raise ValueError("quadrature rule identifier is unsupported")
        if self.quadrature.integer("rule_version") != 1:
            raise ValueError("quadrature rule version is unsupported")
        if self.quadrature.text("rule") != (
            "uniform interior restriction of the closed-interval trapezoidal rule"
        ):
            raise ValueError("quadrature rule name is unsupported")
        if self.quadrature.vector("interior_weights").magnitude.size != dimension:
            raise ValueError("quadrature and represented dimensions disagree")
        if (
            self.analytical_sampling.vector("coordinates").unit
            != self.quadrature.scalar("spacing").unit
        ):
            raise ValueError(
                "analytical coordinates and quadrature length units must agree"
            )
        if not (
            self.eigenpair_sweep.definition
            == self.residual_norm_sweep.definition
            == self.finite_algebraic_diagnostics.definition
        ):
            raise ValueError("grid-sweep sections must share one definition")
        if (
            self.eigenpair_sweep.definition.length != self.configuration.length
            or self.eigenpair_sweep.definition.mass != self.configuration.mass
        ):
            raise ValueError("grid sweep and core PIAB1D configurations must agree")
        if (
            self.analytical_sampling.matrix("wavefunctions").unit
            != self.eigensystem.matrix("quadrature_normalized").unit
        ):
            raise ValueError(
                "analytical and quadrature-normalized wavefunction units must agree"
            )
        object.__setattr__(
            self, "supplementary", MappingProxyType(dict(self.supplementary))
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        values = dict(self.supplementary)
        values.update(
            {
                "calculation_family": self.calculation_family,
                "configuration": self.configuration,
                "matrices": self.hamiltonian,
                "spectra": {
                    name: self.eigensystem.values[name]
                    for name in (
                        "computed_discrete",
                        "discrete_closed_form",
                        "continuum_closed_form",
                    )
                },
                "eigenvectors": {
                    name: self.eigensystem.values[name]
                    for name in ("euclidean", "quadrature_normalized")
                },
                "coordinate_maps": {
                    name: self.reduction.values[name]
                    for name in ("reduction", "embedding", "projector")
                },
                "orthogonal_blocks": {
                    name: self.reduction.values[name]
                    for name in (
                        "retained",
                        "retained_to_discarded",
                        "discarded_to_retained",
                        "discarded",
                    )
                },
                "piab1d_analysis": {
                    name: self.reduction.values[name]
                    for name in ("consistent", "unmatched", "discarded_sector")
                },
                "quadrature": self.quadrature,
                "diagnostics": self.diagnostics,
                "analytical_sampling": self.analytical_sampling,
                "convergence": self.convergence,
                "retained_dimension_selection": self.selection,
                "eigenpair_sweep": self.eigenpair_sweep,
                "residual_norm_sweep": self.residual_norm_sweep,
                "finite_algebraic_diagnostics": self.finite_algebraic_diagnostics,
                "kinetic_potential_decomposition": (
                    self.kinetic_potential_decomposition
                ),
            }
        )
        return values

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        def section(name: str) -> Mapping[str, SerializableValue]:
            value = values.get(name)
            if not isinstance(value, Mapping):
                raise TypeError(f"{name} must be a mapping")
            return value

        spectra = section("spectra")
        eigenvectors = section("eigenvectors")
        maps = section("coordinate_maps")
        blocks = section("orthogonal_blocks")
        analysis = section("piab1d_analysis")
        known = {
            "calculation_family",
            "configuration",
            "matrices",
            "spectra",
            "eigenvectors",
            "coordinate_maps",
            "orthogonal_blocks",
            "piab1d_analysis",
            "quadrature",
            "diagnostics",
            "analytical_sampling",
            "convergence",
            "retained_dimension_selection",
            "eigenpair_sweep",
            "residual_norm_sweep",
            "finite_algebraic_diagnostics",
            "kinetic_potential_decomposition",
        }
        family = values.get("calculation_family")
        if type(family) is not str:
            raise TypeError("calculation_family must be a built-in string")
        return cls(
            calculation_family=family,
            configuration=Piab1dConfiguration.from_dict(section("configuration")),
            hamiltonian=HamiltonianResultSection.from_dict(section("matrices")),
            eigensystem=EigensystemResultSection.from_dict(
                {
                    name: (spectra if name in spectra else eigenvectors)[name]
                    for name in EigensystemResultSection.field_types
                }
            ),
            reduction=SpectralReductionResultSection.from_dict(
                {**maps, **blocks, **analysis}
            ),
            quadrature=QuadratureResultSection.from_dict(
                {
                    name: section("quadrature")[name]
                    for name in QuadratureResultSection.field_types
                }
            ),
            diagnostics=Piab1dDiagnostics.from_dict(section("diagnostics")),
            analytical_sampling=AnalyticalSamplingResultSection.from_dict(
                section("analytical_sampling")
            ),
            convergence=Piab1dConvergenceResult.from_dict(section("convergence")),
            selection=Piab1dSelectionResult.from_dict(
                section("retained_dimension_selection")
            ),
            eigenpair_sweep=Piab1dEigenpairSweepResult.from_dict(
                section("eigenpair_sweep")
            ),
            residual_norm_sweep=Piab1dResidualNormSweepResult.from_dict(
                section("residual_norm_sweep")
            ),
            finite_algebraic_diagnostics=Piab1dFiniteAlgebraicDiagnostics.from_dict(
                section("finite_algebraic_diagnostics")
            ),
            kinetic_potential_decomposition=KineticPotentialDecompositionResult.from_dict(
                section("kinetic_potential_decomposition")
            ),
            supplementary={
                name: value for name, value in values.items() if name not in known
            },
        )
