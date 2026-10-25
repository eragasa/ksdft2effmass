#!/usr/bin/env python3
"""Calculate one direct PIAB1D spectral-reduction execution."""

from __future__ import annotations

import hashlib
import platform
from pathlib import Path

import numpy as np
from projectkoios.physkit.qm.piab1d import Piab1D
from projectkoios.physkit.qm.piab1d.tise_analytical import (
    Piab1DAnalyticalSolution,
)
from projectkoios.physkit.qm.piab1d.tise_fd import Piab1dTiseFdSolver
from projectkoios.physkit.thermal.statmech.qm import CanonicalLevelProbabilityModel
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    UnitSystem,
    VectorQuantity,
)

from ksdft2effmass.analysis import (
    RelativeErrorConvergenceAnalyzer,
    TailProbabilitySelector,
)
from ksdft2effmass.analysis.operators import KineticPotentialDecompositionAnalyzer
from ksdft2effmass.hamiltonian import OrthogonalSpectralSubspace
from ksdft2effmass.model_systems.piab1d import (
    Piab1dAnalyzer,
    Piab1dGridSweepAnalyzer,
    Piab1dGridSweepDefinition,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

# Authored calculation configuration. These values are Python source, not wire input.
EXECUTION_ID = "direct-core-n8-m3"
LENGTH = 1.0
MASS = 1.0
INTERIOR_POINTS = 8
RETAINED_DIMENSION = 3
EVIDENCE_STATUS = "illustrative numerical experiment"
THERMAL_BETA = 0.1
OMITTED_PROBABILITY_TOLERANCE = 0.01
script_path = Path(__file__).resolve()
calculation_directory = script_path.parent
execution_directory = calculation_directory / "executions" / EXECUTION_ID
if execution_directory.exists():
    raise FileExistsError(f"refusing to overwrite {execution_directory}")

model = Piab1D(length=LENGTH, mass=MASS, unit_system=UnitSystem.NONDIMENSIONAL)
solution = Piab1dTiseFdSolver(model=model).solve(interior_points=INTERIOR_POINTS)
analysis = Piab1dAnalyzer().execute(solution, RETAINED_DIMENSION)
reduced_hamiltonian = analysis.reduced_hamiltonian
subspace = reduced_hamiltonian.spectral_subspace
if not isinstance(subspace, OrthogonalSpectralSubspace):
    raise TypeError("the PIAB1D analysis must retain an orthogonal spectral subspace")
if not isinstance(reduced_hamiltonian.matrix, MatrixQuantity) or not isinstance(
    reduced_hamiltonian.embedded.matrix, MatrixQuantity
):
    raise TypeError("the PIAB1D reduction must remain real")
blocks = analysis.hamiltonian_blocks
if (
    not isinstance(blocks.retained, MatrixQuantity)
    or not isinstance(blocks.retained_to_discarded, MatrixQuantity)
    or not isinstance(blocks.discarded_to_retained, MatrixQuantity)
    or not isinstance(blocks.discarded, MatrixQuantity)
):
    raise TypeError("the PIAB1D Hamiltonian blocks must remain real")

quadrature_rule = analysis.quadrature_rule
quadrature_weights = quadrature_rule.interior_weights
diagnostics = analysis.diagnostics.to_dict()
decomposition_shift = MatrixQuantity(
    np.asarray(
        [
            [0.5, 1.0, 0.4],
            [1.0, -0.25, -0.75],
            [0.4, -0.75, 0.75],
        ],
        dtype=np.float64,
    ),
    reduced_hamiltonian.matrix.unit,
)
kinetic_potential_decomposition = KineticPotentialDecompositionAnalyzer().execute(
    reduced_hamiltonian.matrix,
    decomposition_shift,
)
grid_sweep = Piab1dGridSweepAnalyzer().execute(
    Piab1dGridSweepDefinition(
        length=LENGTH,
        mass=MASS,
        interior_points=tuple(range(8, 257)),
        retained_dimension=3,
        fixed_modes=(8, 16, 32),
    )
)
canonical_probabilities = CanonicalLevelProbabilityModel(
    thermal_energy=ScalarQuantity(
        1.0 / THERMAL_BETA,
        solution.energies.unit,
    )
).evaluate(energies=solution.energies)
selection = TailProbabilitySelector().execute(
    canonical_probabilities.probabilities,
    float(OMITTED_PROBABILITY_TOLERANCE),
)
analytical = Piab1DAnalyticalSolution(model=model).evaluate(count=INTERIOR_POINTS)
continuum_coordinates = VectorQuantity(
    np.linspace(0.0, LENGTH, 800),
    model.length_quantity.unit,
)
sampled_continuum = analytical.eigenfunctions(coordinates=continuum_coordinates)
continuum_amplitudes = np.column_stack(
    tuple(
        eigenfunction.amplitudes.magnitude
        for eigenfunction in sampled_continuum.eigenfunctions[:RETAINED_DIMENSION]
    )
)
if np.any(continuum_amplitudes.imag != 0.0):
    raise ValueError("PIAB1D analytical eigenfunctions must be real")
continuum_wavefunctions = MatrixQuantity(
    continuum_amplitudes.real,
    sampled_continuum.eigenfunctions[0].amplitudes.unit,
)
convergence_interior_points = tuple(range(8, 257))
convergence_modes = tuple(range(1, 7))
convergence_solutions = tuple(
    Piab1dTiseFdSolver(model=model).solve(interior_points=points)
    for points in convergence_interior_points
)
convergence_spacings = VectorQuantity(
    np.asarray(
        [item.grid_spacing.magnitude for item in convergence_solutions],
        dtype=np.float64,
    ),
    convergence_solutions[0].grid_spacing.unit,
)
convergence_approximations = MatrixQuantity(
    np.vstack(
        tuple(
            item.closed_form_discrete_energies().magnitude[: len(convergence_modes)]
            for item in convergence_solutions
        )
    ),
    solution.energies.unit,
)
convergence_references = MatrixQuantity(
    np.tile(
        analytical.energies.magnitude[: len(convergence_modes)],
        (len(convergence_interior_points), 1),
    ),
    analytical.energies.unit,
)
convergence = RelativeErrorConvergenceAnalyzer().execute(
    spacings=convergence_spacings,
    approximations=convergence_approximations,
    references=convergence_references,
    order_columns=(0, 1, 2),
)
result = {
    "schema_version": 1,
    "calculation_family": "piab1d-spectral-reduction",
    "execution_id": EXECUTION_ID,
    "evidence_status": EVIDENCE_STATUS,
    "claim_boundary": (
        "Calculated finite-dimensional illustrative result; not material validation, "
        "continuum convergence evidence, or publication acceptance."
    ),
    "configuration": {
        "unit_system": "nondimensional",
        "hbar": 1.0,
        "length": LENGTH,
        "mass": MASS,
        "interior_points": INTERIOR_POINTS,
        "retained_dimension": RETAINED_DIMENSION,
        "boundary_condition": "homogeneous Dirichlet",
        "grid_convention": "uniform full grid with interior-only Hamiltonian",
    },
    "state_spaces": {
        "parent": {
            "identifier": "interior Dirichlet grid coordinates",
            "dimension": INTERIOR_POINTS,
        },
        "reduced": {
            "identifier": "lowest discrete spectral coordinates",
            "dimension": RETAINED_DIMENSION,
        },
    },
    "spectra": {
        "computed_discrete": solution.energies,
        "discrete_closed_form": analysis.discrete_closed_form,
        "continuum_closed_form": analysis.continuum_closed_form,
    },
    "coordinate_maps": {
        "reduction": subspace.reduction_map,
        "embedding": subspace.embedding_map,
        "projector": subspace.projector,
    },
    "matrices": {
        "parent_hamiltonian": solution.hamiltonian.to_dense(),
        "reduced_hamiltonian": reduced_hamiltonian.matrix,
        "embedded_reduced_hamiltonian": reduced_hamiltonian.embedded.matrix,
        "cyclic_reference": analysis.cyclic_reference,
        "boundary_realization": analysis.boundary_realization,
    },
    "orthogonal_blocks": {
        "retained": blocks.retained,
        "retained_to_discarded": blocks.retained_to_discarded,
        "discarded_to_retained": blocks.discarded_to_retained,
        "discarded": blocks.discarded,
    },
    "piab1d_analysis": {
        "consistent": analysis.consistent_reduction,
        "unmatched": analysis.unmatched_reduction,
        "discarded_sector": analysis.discarded_sector,
    },
    "eigenvectors": {
        "euclidean": solution.eigenvectors,
        "euclidean_normalization": "finite-dimensional Euclidean",
        "quadrature_normalized": analysis.quadrature_normalized_eigenvectors,
    },
    "quadrature": {
        "rule_identifier": quadrature_rule.rule_identifier,
        "rule_version": quadrature_rule.rule_version,
        "rule": "uniform interior restriction of the closed-interval trapezoidal rule",
        "spacing": ScalarQuantity(
            float(quadrature_rule.spacing),
            model.length_quantity.unit,
        ),
        "interior_weights": VectorQuantity(
            quadrature_weights,
            model.length_quantity.unit,
        ),
        "weighted_gram": analysis.weighted_gram,
        "weighted_projector": analysis.weighted_projector,
        "interpretation": (
            "The interior weight matrix is the constant scalar hI for this uniform "
            "homogeneous-Dirichlet grid."
        ),
    },
    "diagnostics": diagnostics,
    "analytical_sampling": {
        "coordinates": continuum_coordinates,
        "wavefunctions": continuum_wavefunctions,
    },
    "convergence": {
        "interior_points": convergence_interior_points,
        "modes": convergence_modes,
        "analysis": convergence,
    },
    "eigenpair_sweep": grid_sweep.eigenpairs,
    "residual_norm_sweep": grid_sweep.residual_norms,
    "finite_algebraic_diagnostics": grid_sweep.finite_algebraic_diagnostics,
    "kinetic_potential_decomposition": kinetic_potential_decomposition,
    "retained_dimension_selection": {
        "beta": THERMAL_BETA,
        "selection": selection,
        "interpretation": (
            "Canonical weights over the complete finite discrete spectrum; the "
            "selection is an illustrative a priori criterion, not validation."
        ),
    },
    "provenance": {
        "script_path": script_path.relative_to(
            calculation_directory.parents[1]
        ).as_posix(),
        "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "eigensolver": "PhysKit Piab1dTiseFdSolver",
    },
}

codec = TypedJsonValueCodec()
result_bytes = codec.serialize_bytes(result)
result_sha256 = hashlib.sha256(result_bytes).hexdigest()
temporary_directory = execution_directory.with_name(f".{EXECUTION_ID}.incomplete")
if temporary_directory.exists():
    raise FileExistsError(f"refusing to overwrite {temporary_directory}")
(temporary_directory / "results").mkdir(parents=True)
(temporary_directory / "results" / "result.json").write_bytes(result_bytes)
execution = {
    "schema_version": 1,
    "calculation_family": "piab1d-spectral-reduction",
    "execution_id": EXECUTION_ID,
    "execution_kind": "local deterministic Python calculation",
    "outcome": "completed",
    "evidence_status": EVIDENCE_STATUS,
    "result_path": "results/result.json",
    "result_sha256": result_sha256,
    "claim_boundary": result["claim_boundary"],
}
(temporary_directory / "execution.json").write_bytes(codec.serialize_bytes(execution))
temporary_directory.rename(execution_directory)
