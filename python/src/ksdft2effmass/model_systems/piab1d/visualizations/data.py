"""Authenticated PIAB1D visualization projection."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.analysis import (
    RelativeErrorConvergenceResult,
    TailProbabilitySelection,
)
from ksdft2effmass.analysis.operators import KineticPotentialDecompositionResult
from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.visualizations import BaseVisualizationData

from ..analysis.finite_algebraic_diagnostics import Piab1dFiniteAlgebraicDiagnostics
from ..analysis.grid_sweep import Piab1dEigenpairSweepResult
from ..analysis.residual_norms import Piab1dResidualNormSweepResult


@dataclass(frozen=True, slots=True, eq=False)
class Piab1dVisualizationData(BaseVisualizationData):
    """Retain immutable typed PIAB1D data projected by the verifier.

    Parameters
    ----------
    length
        Positive box length quantity.
    retained_dimension
        Positive number of retained low-energy states.
    computed_energies, continuum_energies
        Represented and analytical full-spectrum energy vectors.
    eigenvectors, quadrature_eigenvectors
        Euclidean and quadrature-normalized eigenvector matrices.
    consistent, unmatched, boundary
        Distinct full-space Hamiltonian analysis matrices.
    continuum_coordinates, continuum_wavefunctions
        Analytical sampling grid and retained-mode wavefunctions.
    selection
        Tail-probability retained-dimension selection.
    convergence_interior_points, convergence_modes, convergence
        Low-mode refinement inventory and values.
    eigenpair_sweep
        Full-spectrum dispersion and eigenpair observations.
    residual_norm_sweep
        Canonical grid-indexed operator and residual norms.
    finite_algebraic_diagnostics
        Grid-indexed finite matrix-identity discrepancies.
    kinetic_potential_decomposition
        Retained-space component pairs and model-class fits.

    Raises
    ------
    TypeError
        A field has the wrong domain type or inventory element type.
    ValueError
        Units, shapes, dimensions, grids, modes, or cross-field conventions disagree.

    Notes
    -----
    This record is derived from the authoritative calculation result by the verifier.
    Its canonical JSON digest is stored in ``Piab1dVerification`` before rendering.
    """

    length: ScalarQuantity
    retained_dimension: int
    computed_energies: VectorQuantity
    continuum_energies: VectorQuantity
    eigenvectors: MatrixQuantity
    quadrature_eigenvectors: MatrixQuantity
    consistent: MatrixQuantity
    unmatched: MatrixQuantity
    boundary: MatrixQuantity
    continuum_coordinates: VectorQuantity
    continuum_wavefunctions: MatrixQuantity
    selection: TailProbabilitySelection
    convergence_interior_points: tuple[int, ...]
    convergence_modes: tuple[int, ...]
    convergence: RelativeErrorConvergenceResult
    eigenpair_sweep: Piab1dEigenpairSweepResult
    residual_norm_sweep: Piab1dResidualNormSweepResult
    finite_algebraic_diagnostics: Piab1dFiniteAlgebraicDiagnostics
    kinetic_potential_decomposition: KineticPotentialDecompositionResult

    def __post_init__(self) -> None:
        if not isinstance(self.length, ScalarQuantity):
            raise TypeError("length must be ScalarQuantity")
        if self.length.magnitude <= 0.0:
            raise ValueError("length must be positive")
        if type(self.retained_dimension) is not int or self.retained_dimension <= 0:
            raise TypeError("retained_dimension must be a positive built-in integer")
        for name, value, expected_type in (
            ("computed_energies", self.computed_energies, VectorQuantity),
            ("continuum_energies", self.continuum_energies, VectorQuantity),
            ("eigenvectors", self.eigenvectors, MatrixQuantity),
            (
                "quadrature_eigenvectors",
                self.quadrature_eigenvectors,
                MatrixQuantity,
            ),
            ("consistent", self.consistent, MatrixQuantity),
            ("unmatched", self.unmatched, MatrixQuantity),
            ("boundary", self.boundary, MatrixQuantity),
            ("continuum_coordinates", self.continuum_coordinates, VectorQuantity),
            ("continuum_wavefunctions", self.continuum_wavefunctions, MatrixQuantity),
        ):
            if not isinstance(value, expected_type):
                raise TypeError(f"{name} must be {expected_type.__name__}")
        if self.computed_energies.unit != self.continuum_energies.unit:
            raise ValueError("computed and continuum energy units must agree")
        energy_unit = self.computed_energies.unit
        if any(
            matrix.unit != energy_unit
            for matrix in (self.consistent, self.unmatched, self.boundary)
        ):
            raise ValueError("visualized Hamiltonian matrices must use the energy unit")
        if not isinstance(self.eigenvectors.unit, Unitless):
            raise ValueError("Euclidean eigenvectors must be unitless")
        if self.continuum_coordinates.unit != self.length.unit:
            raise ValueError("continuum coordinates and box length units must agree")
        if self.continuum_wavefunctions.unit != self.quadrature_eigenvectors.unit:
            raise ValueError("analytical and quadrature wavefunction units must agree")
        if not isinstance(self.selection, TailProbabilitySelection):
            raise TypeError("selection must be TailProbabilitySelection")
        if not isinstance(self.convergence, RelativeErrorConvergenceResult):
            raise TypeError("convergence must be RelativeErrorConvergenceResult")
        if not isinstance(self.eigenpair_sweep, Piab1dEigenpairSweepResult):
            raise TypeError("eigenpair_sweep must be Piab1dEigenpairSweepResult")
        if not isinstance(self.residual_norm_sweep, Piab1dResidualNormSweepResult):
            raise TypeError("residual_norm_sweep must be Piab1dResidualNormSweepResult")
        if not isinstance(
            self.finite_algebraic_diagnostics, Piab1dFiniteAlgebraicDiagnostics
        ):
            raise TypeError(
                "finite_algebraic_diagnostics must be Piab1dFiniteAlgebraicDiagnostics"
            )
        if not isinstance(
            self.kinetic_potential_decomposition,
            KineticPotentialDecompositionResult,
        ):
            raise TypeError("kinetic-potential decomposition has the wrong result type")
        if not (
            self.eigenpair_sweep.definition
            == self.residual_norm_sweep.definition
            == self.finite_algebraic_diagnostics.definition
        ):
            raise ValueError("visualization grid-sweep sections must agree")
        for name, values in (
            ("convergence_interior_points", self.convergence_interior_points),
            ("convergence_modes", self.convergence_modes),
        ):
            if not isinstance(values, tuple) or any(
                type(value) is not int or value <= 0 for value in values
            ):
                raise TypeError(f"{name} must contain positive built-in integers")
        points = self.computed_energies.magnitude.size
        retained = self.retained_dimension
        if points <= 0 or retained > points:
            raise ValueError("retained_dimension must not exceed the parent dimension")
        if self.continuum_energies.magnitude.shape != (points,):
            raise ValueError("continuum_energies must match the parent dimension")
        for name, matrix in (
            ("eigenvectors", self.eigenvectors),
            ("quadrature_eigenvectors", self.quadrature_eigenvectors),
            ("consistent", self.consistent),
            ("unmatched", self.unmatched),
            ("boundary", self.boundary),
        ):
            if matrix.magnitude.shape != (points, points):
                raise ValueError(f"{name} must match the parent matrix shape")
        samples = self.continuum_coordinates.magnitude.size
        if self.continuum_wavefunctions.magnitude.shape != (samples, retained):
            raise ValueError(
                "continuum wavefunctions must match samples and retained modes"
            )
        if self.selection.probabilities.magnitude.shape != (points,):
            raise ValueError("selection probabilities must cover the parent dimension")
        levels, modes = self.convergence.relative_errors.magnitude.shape
        if len(self.convergence_interior_points) != levels:
            raise ValueError("convergence points must cover every refinement level")
        if len(self.convergence_modes) != modes:
            raise ValueError("convergence modes must label every error series")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        """Compose reusable scientific values without JSON normalization."""
        return {
            "length": self.length,
            "retained_dimension": self.retained_dimension,
            "computed_energies": self.computed_energies,
            "continuum_energies": self.continuum_energies,
            "eigenvectors": self.eigenvectors,
            "quadrature_eigenvectors": self.quadrature_eigenvectors,
            "consistent": self.consistent,
            "unmatched": self.unmatched,
            "boundary": self.boundary,
            "continuum_coordinates": self.continuum_coordinates,
            "continuum_wavefunctions": self.continuum_wavefunctions,
            "selection": self.selection,
            "convergence_interior_points": self.convergence_interior_points,
            "convergence_modes": self.convergence_modes,
            "convergence": self.convergence,
            "eigenpair_sweep": self.eigenpair_sweep,
            "residual_norm_sweep": self.residual_norm_sweep,
            "finite_algebraic_diagnostics": self.finite_algebraic_diagnostics,
            "kinetic_potential_decomposition": self.kinetic_potential_decomposition,
        }

    @classmethod
    def _from_mapping(
        cls,
        values: Mapping[str, SerializableValue],
    ) -> Self:
        """Recompose reusable values restored by the generic JSON codec."""
        expected = {
            "length",
            "retained_dimension",
            "computed_energies",
            "continuum_energies",
            "eigenvectors",
            "quadrature_eigenvectors",
            "consistent",
            "unmatched",
            "boundary",
            "continuum_coordinates",
            "continuum_wavefunctions",
            "selection",
            "convergence_interior_points",
            "convergence_modes",
            "convergence",
            "eigenpair_sweep",
            "residual_norm_sweep",
            "finite_algebraic_diagnostics",
            "kinetic_potential_decomposition",
        }
        if set(values) != expected:
            raise ValueError("visualization data fields do not match the contract")
        length = values["length"]
        retained_dimension = values["retained_dimension"]
        computed_energies = values["computed_energies"]
        continuum_energies = values["continuum_energies"]
        eigenvectors = values["eigenvectors"]
        quadrature_eigenvectors = values["quadrature_eigenvectors"]
        consistent = values["consistent"]
        unmatched = values["unmatched"]
        boundary = values["boundary"]
        continuum_coordinates = values["continuum_coordinates"]
        continuum_wavefunctions = values["continuum_wavefunctions"]
        selection = values["selection"]
        convergence_points = values["convergence_interior_points"]
        convergence_modes = values["convergence_modes"]
        convergence = values["convergence"]
        eigenpair_sweep = values["eigenpair_sweep"]
        residual_norm_sweep = values["residual_norm_sweep"]
        algebraic_diagnostics = values["finite_algebraic_diagnostics"]
        decomposition = values["kinetic_potential_decomposition"]
        if not isinstance(length, ScalarQuantity):
            raise TypeError("length must decode to ScalarQuantity")
        if type(retained_dimension) is not int:
            raise TypeError("retained_dimension must decode to a built-in integer")
        if not isinstance(computed_energies, VectorQuantity):
            raise TypeError("computed_energies must decode to VectorQuantity")
        if not isinstance(continuum_energies, VectorQuantity):
            raise TypeError("continuum_energies must decode to VectorQuantity")
        if not isinstance(eigenvectors, MatrixQuantity):
            raise TypeError("eigenvectors must decode to MatrixQuantity")
        if not isinstance(quadrature_eigenvectors, MatrixQuantity):
            raise TypeError("quadrature_eigenvectors must decode to MatrixQuantity")
        if not isinstance(consistent, MatrixQuantity):
            raise TypeError("consistent must decode to MatrixQuantity")
        if not isinstance(unmatched, MatrixQuantity):
            raise TypeError("unmatched must decode to MatrixQuantity")
        if not isinstance(boundary, MatrixQuantity):
            raise TypeError("boundary must decode to MatrixQuantity")
        if not isinstance(continuum_coordinates, VectorQuantity):
            raise TypeError("continuum_coordinates must decode to VectorQuantity")
        if not isinstance(continuum_wavefunctions, MatrixQuantity):
            raise TypeError("continuum_wavefunctions must decode to MatrixQuantity")
        if not isinstance(selection, Mapping):
            raise TypeError("selection must decode to a mapping")
        if not isinstance(convergence, Mapping):
            raise TypeError("convergence must decode to a mapping")
        if not isinstance(eigenpair_sweep, Mapping):
            raise TypeError("eigenpair_sweep must decode to a mapping")
        if not isinstance(residual_norm_sweep, Mapping):
            raise TypeError("residual_norm_sweep must decode to a mapping")
        if not isinstance(algebraic_diagnostics, Mapping):
            raise TypeError("finite_algebraic_diagnostics must decode to a mapping")
        if not isinstance(decomposition, Mapping):
            raise TypeError("kinetic_potential_decomposition must decode to a mapping")
        if not isinstance(convergence_points, tuple) or any(
            type(item) is not int for item in convergence_points
        ):
            raise TypeError(
                "convergence_interior_points must decode to an integer tuple"
            )
        if not isinstance(convergence_modes, tuple) or any(
            type(item) is not int for item in convergence_modes
        ):
            raise TypeError("convergence_modes must decode to an integer tuple")
        return cls(
            length=length,
            retained_dimension=retained_dimension,
            computed_energies=computed_energies,
            continuum_energies=continuum_energies,
            eigenvectors=eigenvectors,
            quadrature_eigenvectors=quadrature_eigenvectors,
            consistent=consistent,
            unmatched=unmatched,
            boundary=boundary,
            continuum_coordinates=continuum_coordinates,
            continuum_wavefunctions=continuum_wavefunctions,
            selection=TailProbabilitySelection.from_dict(selection),
            convergence_interior_points=convergence_points,
            convergence_modes=convergence_modes,
            convergence=RelativeErrorConvergenceResult.from_dict(convergence),
            eigenpair_sweep=Piab1dEigenpairSweepResult.from_dict(eigenpair_sweep),
            residual_norm_sweep=Piab1dResidualNormSweepResult.from_dict(
                residual_norm_sweep
            ),
            finite_algebraic_diagnostics=Piab1dFiniteAlgebraicDiagnostics.from_dict(
                algebraic_diagnostics
            ),
            kinetic_potential_decomposition=KineticPotentialDecompositionResult.from_dict(
                decomposition
            ),
        )
