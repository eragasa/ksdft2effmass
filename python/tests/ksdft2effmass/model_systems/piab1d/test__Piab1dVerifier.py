"""Software verification of independent successor PIAB1D verification."""

from __future__ import annotations

import hashlib
import math

import numpy as np
import pytest
from projectkoios.physkit.qm.piab1d import Piab1D
from projectkoios.physkit.qm.piab1d.tise_fd import Piab1dTiseFdSolver
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    UnitSystem,
    VectorQuantity,
)

from ksdft2effmass.analysis import (
    RelativeErrorConvergenceResult,
    TailProbabilitySelectionRequest,
    TailProbabilitySelector,
)
from ksdft2effmass.analysis.operators import (
    KineticPotentialDecompositionAnalyzer,
    KineticPotentialDecompositionRequest,
    RetainedModelClassFitRequest,
    RetainedModelClassFitter,
)
from ksdft2effmass.hamiltonian import OrthogonalSpectralSubspace
from ksdft2effmass.model_systems import (
    BaseModelAnalysisVerifier,
    ModelAnalysisVerificationResult,
)
from ksdft2effmass.model_systems.piab1d import (
    Piab1dAnalysis,
    Piab1dAnalysisRequest,
    Piab1dAnalyzer,
    Piab1dCalculationResult,
    Piab1dGridSweepAnalyzer,
    Piab1dGridSweepDefinition,
    Piab1dIndependentReference,
    Piab1dIndependentReferenceAnalyzer,
    Piab1dVerification,
    Piab1dVerifier,
    Piab1dVisualizationData,
)
from ksdft2effmass.serialization import (
    BaseTypedRecord,
    SerializableValue,
    TypedJsonValueCodec,
)

pytestmark = pytest.mark.software_verification
SUT = Piab1dVerifier


class TestPiab1dVerifier:
    """Own independent checks and final verification wire boundaries."""

    def test_result__decoded_successor_mapping__passes_independent_checks(self) -> None:
        solution = Piab1dTiseFdSolver(
            model=Piab1D(
                length=1.0,
                mass=1.0,
                unit_system=UnitSystem.NONDIMENSIONAL,
            )
        ).solve(interior_points=8)
        analysis: Piab1dAnalysis = Piab1dAnalyzer(
            Piab1dAnalysisRequest(solution, 3)
        ).execute()
        reduction = analysis.reduced_hamiltonian
        subspace = reduction.spectral_subspace
        assert isinstance(subspace, OrthogonalSpectralSubspace)
        assert isinstance(reduction.matrix, MatrixQuantity)
        assert isinstance(reduction.embedded.matrix, MatrixQuantity)
        blocks = analysis.hamiltonian_blocks
        assert isinstance(blocks.retained, MatrixQuantity)
        assert isinstance(blocks.retained_to_discarded, MatrixQuantity)
        assert isinstance(blocks.discarded_to_retained, MatrixQuantity)
        assert isinstance(blocks.discarded, MatrixQuantity)
        decoded_diagnostics = TypedJsonValueCodec().deserialize_bytes(
            analysis.diagnostics.to_json()
        )
        boltzmann_factors = [
            math.exp(-0.1 * value) for value in solution.energies.magnitude
        ]
        partition_function = math.fsum(boltzmann_factors)
        probabilities = VectorQuantity(
            np.asarray(boltzmann_factors, dtype=np.float64) / partition_function,
            Unitless(),
        )
        selection = TailProbabilitySelector(
            TailProbabilitySelectionRequest(probabilities, 0.01)
        ).execute()
        continuum_coordinates = np.linspace(0.0, 1.0, 800)
        continuum_wavefunctions = np.column_stack(
            tuple(
                np.sqrt(2.0) * np.sin(mode * np.pi * continuum_coordinates)
                for mode in range(1, 4)
            )
        )
        convergence_points = np.arange(8, 257, dtype=np.int64)
        convergence_modes = np.arange(1, 7, dtype=np.int64)
        convergence_spacings = 1.0 / (convergence_points + 1)
        convergence_arguments = (
            convergence_modes[None, :]
            * np.pi
            / (2.0 * (convergence_points[:, None] + 1))
        )
        convergence_errors = (
            1.0 - (np.sin(convergence_arguments) / convergence_arguments) ** 2
        )
        convergence_orders = np.log(
            convergence_errors[:-1, :3] / convergence_errors[1:, :3]
        ) / np.log(convergence_spacings[:-1, None] / convergence_spacings[1:, None])
        grid_sweep = Piab1dGridSweepAnalyzer().execute(
            Piab1dGridSweepDefinition(
                length=1.0,
                mass=1.0,
                interior_points=(8, 9),
                retained_dimension=3,
                fixed_modes=(8,),
            )
        )
        eigenpair_sweep = grid_sweep.eigenpairs
        decomposition_shift = MatrixQuantity(
            np.asarray(
                [
                    [0.5, 1.0, 0.4],
                    [1.0, -0.25, -0.75],
                    [0.4, -0.75, 0.75],
                ]
            ),
            reduction.matrix.unit,
        )
        decomposition = KineticPotentialDecompositionAnalyzer(
            KineticPotentialDecompositionRequest(reduction.matrix, decomposition_shift),
            RetainedModelClassFitter(RetainedModelClassFitRequest(decomposition_shift)),
        ).execute()
        visualization_data = Piab1dVisualizationData(
            length=solution.model.length_quantity,
            retained_dimension=3,
            computed_energies=solution.energies,
            continuum_energies=analysis.continuum_closed_form,
            eigenvectors=solution.eigenvectors,
            quadrature_eigenvectors=analysis.quadrature_normalized_eigenvectors,
            consistent=analysis.consistent_reduction,
            unmatched=analysis.unmatched_reduction,
            boundary=analysis.boundary_realization,
            continuum_coordinates=VectorQuantity(continuum_coordinates, Unitless()),
            continuum_wavefunctions=MatrixQuantity(continuum_wavefunctions, Unitless()),
            selection=selection,
            convergence_interior_points=tuple(
                int(value) for value in convergence_points
            ),
            convergence_modes=tuple(int(value) for value in convergence_modes),
            convergence=RelativeErrorConvergenceResult(
                spacings=VectorQuantity(convergence_spacings, Unitless()),
                relative_errors=MatrixQuantity(convergence_errors, Unitless()),
                order_columns=(0, 1, 2),
                observed_orders=MatrixQuantity(convergence_orders, Unitless()),
            ),
            eigenpair_sweep=eigenpair_sweep,
            residual_norm_sweep=grid_sweep.residual_norms,
            finite_algebraic_diagnostics=grid_sweep.finite_algebraic_diagnostics,
            kinetic_potential_decomposition=decomposition,
        )
        result: dict[str, SerializableValue] = {
            "calculation_family": "piab1d-spectral-reduction",
            "configuration": {
                "unit_system": "nondimensional",
                "hbar": 1.0,
                "length": 1.0,
                "mass": 1.0,
                "interior_points": 8,
                "retained_dimension": 3,
                "boundary_condition": "homogeneous Dirichlet",
                "grid_convention": ("uniform full grid with interior-only Hamiltonian"),
                "euclidean_normalization": "finite-dimensional Euclidean",
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
                "reduced_hamiltonian": reduction.matrix,
                "embedded_reduced_hamiltonian": reduction.embedded.matrix,
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
                "quadrature_normalized": analysis.quadrature_normalized_eigenvectors,
            },
            "quadrature": {
                "rule_identifier": (
                    "projectkoios.numerics.quadrature."
                    "uniform_closed_interval_trapezoidal"
                ),
                "rule_version": 1,
                "rule": (
                    "uniform interior restriction of the closed-interval "
                    "trapezoidal rule"
                ),
                "spacing": ScalarQuantity(
                    float(analysis.quadrature_rule.spacing),
                    Unitless(),
                ),
                "interior_weights": VectorQuantity(
                    analysis.quadrature_rule.interior_weights,
                    Unitless(),
                ),
                "weighted_gram": analysis.weighted_gram,
                "weighted_projector": analysis.weighted_projector,
            },
            "diagnostics": decoded_diagnostics,
            "analytical_sampling": {
                "coordinates": visualization_data.continuum_coordinates,
                "wavefunctions": visualization_data.continuum_wavefunctions,
            },
            "convergence": {
                "interior_points": visualization_data.convergence_interior_points,
                "modes": visualization_data.convergence_modes,
                "analysis": visualization_data.convergence,
            },
            "eigenpair_sweep": eigenpair_sweep,
            "residual_norm_sweep": grid_sweep.residual_norms,
            "finite_algebraic_diagnostics": grid_sweep.finite_algebraic_diagnostics,
            "kinetic_potential_decomposition": decomposition,
            "retained_dimension_selection": {
                "beta": 0.1,
                "selection": selection,
            },
        }

        result_wire = TypedJsonValueCodec().serialize_bytes(result)
        decoded_result = TypedJsonValueCodec().deserialize_bytes(result_wire)
        assert isinstance(decoded_result, dict)
        typed_result = Piab1dCalculationResult.from_dict(decoded_result)
        reference = Piab1dIndependentReferenceAnalyzer().execute(
            typed_result,
            visualization_data,
        )
        assert isinstance(reference, Piab1dIndependentReference)
        assert len(reference.comparisons) == 79
        with pytest.raises(TypeError):
            reference.comparisons["new"] = reference.comparisons[
                "parent_hamiltonian_maximum_absolute_error"
            ]

        verifier = SUT(result_wire=result_wire)
        verification_result = verifier.result()
        verification = verification_result.verification

        assert isinstance(verifier, BaseModelAnalysisVerifier)
        assert isinstance(verification_result, ModelAnalysisVerificationResult)
        assert verification_result.visualization_data.to_json() == (
            visualization_data.to_json()
        )
        assert verification.passed is True
        assert verification.subject_sha256 == hashlib.sha256(result_wire).hexdigest()
        assert len(verification.checks) == 79
        assert max(verification.checks.values()) <= 1.0e-12
        reconstructed = Piab1dVerification.from_json(verification.to_json())
        assert reconstructed.passed is True
        assert dict(reconstructed.checks) == dict(verification.checks)
        assert dict(reconstructed.check_tolerances) == dict(
            verification.check_tolerances
        )

    def test_init__empty_checks__rejects_vacuous_passing_record(self) -> None:
        with pytest.raises(ValueError, match="declared verification inventory"):
            Piab1dVerification(
                subject_sha256="a" * 64,
                visualization_data_sha256="b" * 64,
                components=(),
            )

    def test_type__verification_boundaries__are_final_base_methods(self) -> None:
        for name in ("to_dict", "from_dict", "to_json", "from_json"):
            assert name not in Piab1dVerification.__dict__
            method = BaseTypedRecord.__dict__[name]
            if isinstance(method, classmethod):
                method = method.__func__
            assert getattr(method, "__final__", False) is True
