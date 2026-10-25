"""Typed PIAB1D represented-grid sweep analysis."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

import numpy as np
from projectkoios.physkit.linalg.matrix.norm import MatrixNorm, MatrixNormEnum
from projectkoios.physkit.qm.piab1d import Piab1D
from projectkoios.physkit.qm.piab1d.tise_fd import Piab1dTiseFdSolver
from projectkoios.physkit.units import (
    MatrixQuantity,
    Unitless,
    UnitSystem,
    VectorQuantity,
)

from ksdft2effmass.analysis import RelativeErrorConvergenceResult
from ksdft2effmass.analysis.operators import RealSymmetricEigenpairDiagnosticAnalyzer
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .finite_algebraic_diagnostics import Piab1dFiniteAlgebraicDiagnostics
from .residual_norms import Piab1dResidualNormSweepResult


@dataclass(frozen=True, slots=True)
class Piab1dGridSweepDefinition(BaseTypedRecord):
    """Declare the nondimensional PIAB1D grids and fixed modes to analyze.

    Parameters
    ----------
    length
        Positive nondimensional box length.
    mass
        Positive nondimensional particle mass.
    interior_points
        Strictly increasing interior grid dimensions, each at least two.
    retained_dimension
        Positive reduction dimension present on every declared grid.
    fixed_modes
        Strictly increasing positive one-based modes present on at least one grid.

    Raises
    ------
    TypeError
        A scalar or inventory member has the wrong exact type.
    ValueError
        Positivity, ordering, or represented-mode availability fails.
    """

    length: float
    mass: float
    interior_points: tuple[int, ...]
    retained_dimension: int
    fixed_modes: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.length) is not float or not np.isfinite(self.length):
            raise TypeError("length must be a finite built-in float")
        if type(self.mass) is not float or not np.isfinite(self.mass):
            raise TypeError("mass must be a finite built-in float")
        if self.length <= 0.0 or self.mass <= 0.0:
            raise ValueError("length and mass must be positive")
        if (
            not isinstance(self.interior_points, tuple)
            or not self.interior_points
            or any(
                type(value) is not int or value < 2 for value in self.interior_points
            )
            or any(
                right <= left
                for left, right in zip(
                    self.interior_points[:-1],
                    self.interior_points[1:],
                    strict=True,
                )
            )
        ):
            raise ValueError("interior_points must be strictly increasing integers")
        if (
            type(self.retained_dimension) is not int
            or self.retained_dimension <= 0
            or self.retained_dimension > min(self.interior_points)
        ):
            raise ValueError("retained_dimension must exist on every grid")
        if (
            not isinstance(self.fixed_modes, tuple)
            or not self.fixed_modes
            or any(type(value) is not int or value <= 0 for value in self.fixed_modes)
            or any(
                right <= left
                for left, right in zip(
                    self.fixed_modes[:-1],
                    self.fixed_modes[1:],
                    strict=True,
                )
            )
        ):
            raise ValueError(
                "fixed_modes must be strictly increasing positive integers"
            )
        if max(self.fixed_modes) > max(self.interior_points):
            raise ValueError("fixed modes must occur in at least one represented grid")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "length": self.length,
            "mass": self.mass,
            "interior_points": self.interior_points,
            "retained_dimension": self.retained_dimension,
            "fixed_modes": self.fixed_modes,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "length",
            "mass",
            "interior_points",
            "retained_dimension",
            "fixed_modes",
        }:
            raise ValueError("grid-sweep definition fields do not match")
        length = values["length"]
        mass = values["mass"]
        points = values["interior_points"]
        retained_dimension = values["retained_dimension"]
        modes = values["fixed_modes"]
        if type(length) is not float or type(mass) is not float:
            raise TypeError("length and mass must decode to built-in floats")
        if type(retained_dimension) is not int:
            raise TypeError("retained_dimension must decode to a built-in integer")
        if not isinstance(points, tuple) or not isinstance(modes, tuple):
            raise TypeError("grid and mode inventories must decode to tuples")
        return cls(
            length=length,
            mass=mass,
            interior_points=points,
            retained_dimension=retained_dimension,
            fixed_modes=modes,
        )


@dataclass(frozen=True, slots=True, eq=False)
class Piab1dEigenpairSweepResult(BaseTypedRecord):
    """Retain flattened full-spectrum observations across represented grids.

    Parameters
    ----------
    definition
        Shared grid and mode declaration.
    grid_offsets
        Cumulative offsets delimiting each full spectrum in flattened vectors.
    mode_numbers
        Concatenated one-based mode inventory for every grid.
    spacings
        One nondimensional spacing per grid.
    fractional_mode_indices
        Flattened ``n / (N + 1)`` coordinates.
    relative_energy_errors
        Nonnegative continuum-relative energy discrepancies.
    nodal_overlap_defects
        Nonnegative sign-invariant discrete sine-vector overlap defects.
    scaled_eigenpair_residuals
        Nonnegative scale-safe residuals for every represented eigenpair.

    Raises
    ------
    TypeError
        A field has the wrong typed representation.
    ValueError
        Offsets, modes, units, spacing correspondence, shapes, or signs are invalid.
    """

    definition: Piab1dGridSweepDefinition
    grid_offsets: tuple[int, ...]
    mode_numbers: tuple[int, ...]
    spacings: VectorQuantity
    fractional_mode_indices: VectorQuantity
    relative_energy_errors: VectorQuantity
    nodal_overlap_defects: VectorQuantity
    scaled_eigenpair_residuals: VectorQuantity

    def __post_init__(self) -> None:
        if not isinstance(self.definition, Piab1dGridSweepDefinition):
            raise TypeError("definition must be Piab1dGridSweepDefinition")
        expected_offsets = [0]
        for dimension in self.definition.interior_points:
            expected_offsets.append(expected_offsets[-1] + dimension)
        if self.grid_offsets != tuple(expected_offsets):
            raise ValueError("grid_offsets must delimit every represented spectrum")
        count = expected_offsets[-1]
        expected_modes = tuple(
            mode
            for dimension in self.definition.interior_points
            for mode in range(1, dimension + 1)
        )
        if self.mode_numbers != expected_modes:
            raise ValueError("mode_numbers must enumerate every represented spectrum")
        if not isinstance(self.spacings, VectorQuantity):
            raise TypeError("spacings must be VectorQuantity")
        if self.spacings.magnitude.shape != (len(self.definition.interior_points),):
            raise ValueError("spacings must cover every represented grid")
        if not isinstance(self.spacings.unit, Unitless):
            raise ValueError("spacings must use the declared nondimensional unit")
        expected_spacings = np.asarray(
            tuple(
                self.definition.length / (dimension + 1.0)
                for dimension in self.definition.interior_points
            ),
            dtype=np.float64,
        )
        if not np.array_equal(self.spacings.magnitude, expected_spacings):
            raise ValueError("spacings must match the declared represented grids")
        for name, values in (
            ("fractional_mode_indices", self.fractional_mode_indices),
            ("relative_energy_errors", self.relative_energy_errors),
            ("nodal_overlap_defects", self.nodal_overlap_defects),
            ("scaled_eigenpair_residuals", self.scaled_eigenpair_residuals),
        ):
            if not isinstance(values, VectorQuantity):
                raise TypeError(f"{name} must be VectorQuantity")
            if not isinstance(values.unit, Unitless):
                raise ValueError(f"{name} must be unitless")
            if values.magnitude.shape != (count,):
                raise ValueError(f"{name} must cover every represented eigenpair")
        if np.any(self.relative_energy_errors.magnitude < 0.0):
            raise ValueError("relative energy errors must be nonnegative")
        if np.any(self.nodal_overlap_defects.magnitude < 0.0):
            raise ValueError("nodal overlap defects must be nonnegative")
        if np.any(self.scaled_eigenpair_residuals.magnitude < 0.0):
            raise ValueError("scaled eigenpair residuals must be nonnegative")

    def fixed_mode_convergence(self, mode: int) -> RelativeErrorConvergenceResult:
        """Extract one fixed-mode continuum convergence series.

        Parameters
        ----------
        mode
            Positive one-based mode contained in the definition's fixed-mode
            inventory.

        Returns
        -------
        RelativeErrorConvergenceResult
            Grid spacings, continuum relative errors, and adjacent-grid observed
            orders for the requested mode.

        Raises
        ------
        TypeError
            ``mode`` is not a built-in integer.
        ValueError
            The mode is undeclared, occurs on fewer than two grids, or contains a
            nonpositive relative error that makes the logarithmic order undefined.
        """
        if type(mode) is not int:
            raise TypeError("mode must be a built-in integer")
        if mode not in self.definition.fixed_modes:
            raise ValueError("mode must belong to the declared fixed-mode inventory")
        grid_indices = tuple(
            index
            for index, dimension in enumerate(self.definition.interior_points)
            if mode <= dimension
        )
        if len(grid_indices) < 2:
            raise ValueError("a fixed-mode convergence series requires two grids")
        eigenpair_indices = tuple(
            self.grid_offsets[index] + mode - 1 for index in grid_indices
        )
        spacings = self.spacings.magnitude[np.asarray(grid_indices, dtype=np.int64)]
        errors = self.relative_energy_errors.magnitude[
            np.asarray(eigenpair_indices, dtype=np.int64)
        ]
        if np.any(errors <= 0.0):
            raise ValueError("fixed-mode relative errors must be positive")
        orders = np.log(errors[:-1] / errors[1:]) / np.log(spacings[:-1] / spacings[1:])
        unitless = Unitless()
        return RelativeErrorConvergenceResult(
            spacings=VectorQuantity(spacings, unitless),
            relative_errors=MatrixQuantity(errors[:, None], unitless),
            order_columns=(0,),
            observed_orders=MatrixQuantity(orders[:, None], unitless),
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "definition": self.definition,
            "grid_offsets": self.grid_offsets,
            "mode_numbers": self.mode_numbers,
            "spacings": self.spacings,
            "fractional_mode_indices": self.fractional_mode_indices,
            "relative_energy_errors": self.relative_energy_errors,
            "nodal_overlap_defects": self.nodal_overlap_defects,
            "scaled_eigenpair_residuals": self.scaled_eigenpair_residuals,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "definition",
            "grid_offsets",
            "mode_numbers",
            "spacings",
            "fractional_mode_indices",
            "relative_energy_errors",
            "nodal_overlap_defects",
            "scaled_eigenpair_residuals",
        }
        if set(values) != required:
            raise ValueError("eigenpair-sweep result fields do not match")
        definition_value = values["definition"]
        if isinstance(definition_value, Piab1dGridSweepDefinition):
            definition = definition_value
        elif isinstance(definition_value, Mapping):
            definition = Piab1dGridSweepDefinition.from_dict(definition_value)
        else:
            raise TypeError("definition must be typed or decode to a mapping")
        offsets = values["grid_offsets"]
        modes = values["mode_numbers"]
        spacings = values["spacings"]
        fractions = values["fractional_mode_indices"]
        errors = values["relative_energy_errors"]
        overlaps = values["nodal_overlap_defects"]
        residuals = values["scaled_eigenpair_residuals"]
        if not isinstance(offsets, tuple) or not isinstance(modes, tuple):
            raise TypeError("offsets and modes must decode to tuples")
        if (
            not isinstance(spacings, VectorQuantity)
            or not isinstance(fractions, VectorQuantity)
            or not isinstance(errors, VectorQuantity)
            or not isinstance(overlaps, VectorQuantity)
            or not isinstance(residuals, VectorQuantity)
        ):
            raise TypeError("sweep observations must decode to vector quantities")
        return cls(
            definition=definition,
            grid_offsets=offsets,
            mode_numbers=modes,
            spacings=spacings,
            fractional_mode_indices=fractions,
            relative_energy_errors=errors,
            nodal_overlap_defects=overlaps,
            scaled_eigenpair_residuals=residuals,
        )


@dataclass(frozen=True, slots=True, eq=False)
class Piab1dGridSweepAnalysis(BaseTypedRecord):
    """Compose all observations derived from one set of grid solves.

    Parameters
    ----------
    eigenpairs
        Complete flattened eigenpair sweep.
    residual_norms
        Grid-indexed canonical residual norms.
    finite_algebraic_diagnostics
        Grid-indexed finite matrix-identity discrepancies.

    Raises
    ------
    TypeError
        A component has the wrong result type.
    ValueError
        Components do not share the same exact grid-sweep definition.
    """

    eigenpairs: Piab1dEigenpairSweepResult
    residual_norms: Piab1dResidualNormSweepResult
    finite_algebraic_diagnostics: Piab1dFiniteAlgebraicDiagnostics

    def __post_init__(self) -> None:
        if not isinstance(self.eigenpairs, Piab1dEigenpairSweepResult):
            raise TypeError("eigenpairs must be Piab1dEigenpairSweepResult")
        if not isinstance(self.residual_norms, Piab1dResidualNormSweepResult):
            raise TypeError("residual_norms must be Piab1dResidualNormSweepResult")
        if not isinstance(
            self.finite_algebraic_diagnostics, Piab1dFiniteAlgebraicDiagnostics
        ):
            raise TypeError(
                "finite_algebraic_diagnostics must be Piab1dFiniteAlgebraicDiagnostics"
            )
        if not (
            self.eigenpairs.definition
            == self.residual_norms.definition
            == self.finite_algebraic_diagnostics.definition
        ):
            raise ValueError("grid-sweep result sections must share one definition")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "eigenpairs": self.eigenpairs,
            "residual_norms": self.residual_norms,
            "finite_algebraic_diagnostics": self.finite_algebraic_diagnostics,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "eigenpairs",
            "residual_norms",
            "finite_algebraic_diagnostics",
        }:
            raise ValueError("grid-sweep analysis fields do not match")
        eigenpairs_value = values["eigenpairs"]
        residuals_value = values["residual_norms"]
        algebraic_value = values["finite_algebraic_diagnostics"]
        eigenpairs = (
            eigenpairs_value
            if isinstance(eigenpairs_value, Piab1dEigenpairSweepResult)
            else Piab1dEigenpairSweepResult.from_dict(eigenpairs_value)
            if isinstance(eigenpairs_value, Mapping)
            else None
        )
        residuals = (
            residuals_value
            if isinstance(residuals_value, Piab1dResidualNormSweepResult)
            else Piab1dResidualNormSweepResult.from_dict(residuals_value)
            if isinstance(residuals_value, Mapping)
            else None
        )
        algebraic = (
            algebraic_value
            if isinstance(algebraic_value, Piab1dFiniteAlgebraicDiagnostics)
            else Piab1dFiniteAlgebraicDiagnostics.from_dict(algebraic_value)
            if isinstance(algebraic_value, Mapping)
            else None
        )
        if eigenpairs is None or residuals is None or algebraic is None:
            raise TypeError("grid-sweep sections must be typed or decode to mappings")
        return cls(
            eigenpairs=eigenpairs,
            residual_norms=residuals,
            finite_algebraic_diagnostics=algebraic,
        )


class Piab1dGridSweepAnalyzer:
    """Solve each declared grid once and retain full-spectrum observations."""

    __slots__ = ("eigenpair_analyzer",)

    def __init__(self) -> None:
        self.eigenpair_analyzer = RealSymmetricEigenpairDiagnosticAnalyzer()

    def execute(self, definition: Piab1dGridSweepDefinition) -> Piab1dGridSweepAnalysis:
        """Solve every declared grid once and derive all sweep families.

        Parameters
        ----------
        definition
            Nondimensional box parameters, strictly increasing grid dimensions,
            retained dimension, and fixed modes.

        Returns
        -------
        Piab1dGridSweepAnalysis
            Correlated full-spectrum, residual-norm, and finite-algebraic observations
            sharing the exact same grid definition and eigensolutions.

        Raises
        ------
        TypeError
            ``definition`` is not a ``Piab1dGridSweepDefinition``.
        ValueError
            A generated quantity violates a typed result invariant.

        Notes
        -----
        A single eigensolver call serves every diagnostic family on each grid. The
        method therefore prevents cross-family drift in represented dimensions,
        eigenvector gauges, and solver results.
        """
        if not isinstance(definition, Piab1dGridSweepDefinition):
            raise TypeError("definition must be Piab1dGridSweepDefinition")
        solver = Piab1dTiseFdSolver(
            model=Piab1D(
                length=definition.length,
                mass=definition.mass,
                unit_system=UnitSystem.NONDIMENSIONAL,
            )
        )
        offsets = [0]
        modes: list[int] = []
        spacings: list[float] = []
        fractions: list[float] = []
        energy_errors: list[float] = []
        overlap_defects: list[float] = []
        scaled_residuals: list[float] = []
        norms = (
            MatrixNormEnum.frobenius,
            MatrixNormEnum.spectral,
            MatrixNormEnum.maximum_absolute_entry,
        )
        hamiltonian_norms: list[tuple[float, ...]] = []
        consistent_norms: list[tuple[float, ...]] = []
        boundary_norms: list[tuple[float, ...]] = []
        unmatched_norms: list[tuple[float, ...]] = []
        eigensolver_norms: list[tuple[float, ...]] = []
        discrete_spectrum_discrepancies: list[float] = []
        spectral_reconstruction_discrepancies: list[float] = []
        projector_idempotency_discrepancies: list[float] = []
        retained_coordinate_discrepancies: list[float] = []
        retained_embedding_discrepancies: list[float] = []
        spectral_leakage_norms: list[float] = []
        for dimension in definition.interior_points:
            solution = solver.solve(interior_points=dimension)
            diagnostics = self.eigenpair_analyzer.execute(solution.eigensystem)
            computed = solution.energies.magnitude
            continuum_modes = np.arange(1, dimension + 1, dtype=np.float64)
            continuum = (
                continuum_modes**2
                * np.pi**2
                / (2.0 * definition.mass * definition.length**2)
            )
            nodes = np.arange(1, dimension + 1, dtype=np.float64)
            # The discrete sine basis is Euclidean-normalized on interior nodes;
            # continuum quadrature normalization is a separate core-analysis value.
            analytical_vectors = np.sqrt(2.0 / (dimension + 1.0)) * np.sin(
                np.pi * nodes[:, None] * continuum_modes[None, :] / (dimension + 1.0)
            )
            overlaps = np.abs(
                np.sum(solution.eigenvectors.magnitude * analytical_vectors, axis=0)
            )
            spacings.append(definition.length / (dimension + 1.0))
            modes.extend(range(1, dimension + 1))
            fractions.extend(continuum_modes / (dimension + 1.0))
            energy_errors.extend(np.abs(computed - continuum) / continuum)
            overlap_defects.extend(np.maximum(0.0, 1.0 - overlaps))
            scaled_residuals.extend(diagnostics.scaled_column_residuals.magnitude)
            hamiltonian = solution.hamiltonian.to_dense()
            hamiltonian_values = hamiltonian.magnitude
            retained_vectors = solution.eigenvectors.magnitude[
                :, : definition.retained_dimension
            ]
            reduction = retained_vectors.T
            embedding = retained_vectors
            # These maps stay rectangular. Only the represented and reduced
            # Hamiltonians are square operators in their respective coordinates.
            projector = embedding @ reduction
            reduced = reduction @ hamiltonian_values @ embedding
            embedded = embedding @ reduced @ reduction
            consistent = embedded - embedding @ reduced @ reduction
            unmatched = embedded - hamiltonian_values
            # The cyclic matrix is a comparison reference, not a second PIAB1D
            # boundary condition. Their difference isolates the endpoint realization.
            cyclic = hamiltonian_values.copy()
            cyclic[0, -1] = hamiltonian_values[0, 1]
            cyclic[-1, 0] = hamiltonian_values[1, 0]
            boundary = hamiltonian_values - cyclic
            matrices = (
                hamiltonian_values,
                consistent,
                boundary,
                unmatched,
                diagnostics.algebraic_residual.magnitude,
            )
            observed = tuple(
                tuple(
                    MatrixNorm(MatrixQuantity(matrix, hamiltonian.unit), norm)
                    .result()
                    .magnitude
                    for norm in norms
                )
                for matrix in matrices
            )
            hamiltonian_norms.append(observed[0])
            consistent_norms.append(observed[1])
            boundary_norms.append(observed[2])
            unmatched_norms.append(observed[3])
            eigensolver_norms.append(observed[4])
            exact_discrete = solution.closed_form_discrete_energies().magnitude
            expected_retained = np.diag(exact_discrete[: definition.retained_dimension])
            complement = np.eye(dimension) - projector
            discrete_spectrum_discrepancies.append(
                float(np.max(np.abs(computed - exact_discrete)))
            )
            spectral_reconstruction_discrepancies.append(
                float(
                    np.linalg.norm(
                        hamiltonian_values
                        - solution.eigenvectors.magnitude
                        @ np.diag(computed)
                        @ solution.eigenvectors.magnitude.T,
                        ord="fro",
                    )
                )
            )
            projector_idempotency_discrepancies.append(
                float(np.linalg.norm(projector @ projector - projector, ord="fro"))
            )
            retained_coordinate_discrepancies.append(
                float(np.linalg.norm(reduced - expected_retained, ord="fro"))
            )
            retained_embedding_discrepancies.append(
                float(
                    np.linalg.norm(
                        embedded - embedding @ reduced @ reduction,
                        ord="fro",
                    )
                )
            )
            spectral_leakage_norms.append(
                float(
                    np.linalg.norm(
                        complement @ hamiltonian_values @ retained_vectors,
                        ord="fro",
                    )
                )
            )
            offsets.append(offsets[-1] + dimension)
        unitless = Unitless()
        eigenpairs = Piab1dEigenpairSweepResult(
            definition=definition,
            grid_offsets=tuple(offsets),
            mode_numbers=tuple(modes),
            spacings=VectorQuantity(np.asarray(spacings, dtype=np.float64), unitless),
            fractional_mode_indices=VectorQuantity(
                np.asarray(fractions, dtype=np.float64), unitless
            ),
            relative_energy_errors=VectorQuantity(
                np.asarray(energy_errors, dtype=np.float64), unitless
            ),
            nodal_overlap_defects=VectorQuantity(
                np.asarray(overlap_defects, dtype=np.float64), unitless
            ),
            scaled_eigenpair_residuals=VectorQuantity(
                np.asarray(scaled_residuals, dtype=np.float64), unitless
            ),
        )
        hamiltonian_array = np.asarray(hamiltonian_norms, dtype=np.float64)
        if np.any(hamiltonian_array <= 0.0):
            raise ValueError("Hamiltonian norms must be positive")
        raw_arrays = tuple(
            np.asarray(values, dtype=np.float64)
            for values in (
                consistent_norms,
                boundary_norms,
                unmatched_norms,
                eigensolver_norms,
            )
        )
        residual_norms = Piab1dResidualNormSweepResult(
            definition=definition,
            norms=norms,
            hamiltonian=MatrixQuantity(hamiltonian_array, unitless),
            consistent=MatrixQuantity(raw_arrays[0], unitless),
            boundary=MatrixQuantity(raw_arrays[1], unitless),
            unmatched=MatrixQuantity(raw_arrays[2], unitless),
            eigensolver=MatrixQuantity(raw_arrays[3], unitless),
            consistent_relative=MatrixQuantity(
                raw_arrays[0] / hamiltonian_array, unitless
            ),
            boundary_relative=MatrixQuantity(
                raw_arrays[1] / hamiltonian_array, unitless
            ),
            unmatched_relative=MatrixQuantity(
                raw_arrays[2] / hamiltonian_array, unitless
            ),
            eigensolver_relative=MatrixQuantity(
                raw_arrays[3] / hamiltonian_array, unitless
            ),
        )
        algebraic_diagnostics = Piab1dFiniteAlgebraicDiagnostics(
            definition=definition,
            discrete_spectrum=VectorQuantity(
                np.asarray(discrete_spectrum_discrepancies), unitless
            ),
            spectral_reconstruction=VectorQuantity(
                np.asarray(spectral_reconstruction_discrepancies), unitless
            ),
            projector_idempotency=VectorQuantity(
                np.asarray(projector_idempotency_discrepancies), unitless
            ),
            retained_coordinates=VectorQuantity(
                np.asarray(retained_coordinate_discrepancies), unitless
            ),
            retained_embedding=VectorQuantity(
                np.asarray(retained_embedding_discrepancies), unitless
            ),
            spectral_leakage=VectorQuantity(
                np.asarray(spectral_leakage_norms), unitless
            ),
        )
        return Piab1dGridSweepAnalysis(
            eigenpairs=eigenpairs,
            residual_norms=residual_norms,
            finite_algebraic_diagnostics=algebraic_diagnostics,
        )
