"""Software verification of complete PIAB1D analysis."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.physkit.linalg.matrix.norm import MatrixNormEnum
from projectkoios.physkit.qm.piab1d import Piab1D
from projectkoios.physkit.qm.piab1d.tise_fd import Piab1dTiseFdSolver
from projectkoios.physkit.units import Unitless, UnitSystem

from ksdft2effmass.analysis import DiagnosticObservation
from ksdft2effmass.model_systems import BaseModelSystemAnalyzer
from ksdft2effmass.model_systems.piab1d import (
    DiagnosticMethodsEnum,
    Piab1dAnalyzer,
    Piab1dDiagnostics,
    diagnostic_method_names,
)

pytestmark = pytest.mark.software_verification
SUT = Piab1dAnalyzer


class TestPiab1dAnalyzer:
    """Own the correlated analysis returned for one finite PIAB1D solution."""

    def test_execute__declared_finite_solution__returns_complete_analysis(self) -> None:
        model = Piab1D(length=1.0, mass=1.0, unit_system=UnitSystem.NONDIMENSIONAL)
        solution = Piab1dTiseFdSolver(model=model).solve(interior_points=8)

        analyzer = SUT()
        result = analyzer.execute(solution, retained_dimension=3)

        assert isinstance(analyzer, BaseModelSystemAnalyzer)
        assert result.solution is solution
        assert result.reduced_hamiltonian.spectral_subspace.dimension == 3
        assert result.reduced_hamiltonian.spectral_subspace.full_dimension == 8
        assert result.hamiltonian_blocks.hamiltonian.matrix is solution.hamiltonian
        assert result.discrete_closed_form.magnitude.shape == (8,)
        assert result.continuum_closed_form.magnitude.shape == (8,)
        assert result.quadrature_normalized_eigenvectors.magnitude.shape == (8, 8)
        assert result.weighted_gram.magnitude.shape == (3, 3)
        assert result.weighted_projector.magnitude.shape == (8, 8)
        np.testing.assert_array_equal(
            result.consistent_reduction.magnitude, np.zeros((8, 8))
        )
        np.testing.assert_allclose(
            result.unmatched_reduction.magnitude,
            result.discarded_sector.magnitude,
            rtol=0.0,
            atol=1.0e-13,
        )
        np.testing.assert_allclose(
            result.weighted_gram.magnitude,
            np.eye(3),
            rtol=0.0,
            atol=1.0e-13,
        )
        np.testing.assert_allclose(
            result.weighted_projector.magnitude,
            result.reduced_hamiltonian.spectral_subspace.projector.magnitude,
            rtol=0.0,
            atol=1.0e-13,
        )
        observations = result.diagnostics.observations
        assert set(observations) == set(DiagnosticMethodsEnum)
        assert set(diagnostic_method_names) == set(DiagnosticMethodsEnum)
        assert all(
            isinstance(observation, DiagnosticObservation)
            for observation in observations.values()
        )
        assert observations[
            DiagnosticMethodsEnum.scaled_eigenpair_residuals
        ].value.magnitude.shape == (8,)
        assert all(
            observation.atol.magnitude == 1.0e-12
            for observation in observations.values()
        )
        assert all(observation.rtol == 0.0 for observation in observations.values())
        matrix_methods = {
            DiagnosticMethodsEnum.spectral_reconstruction_error,
            DiagnosticMethodsEnum.projector_idempotency_error,
            DiagnosticMethodsEnum.weighted_gram_error,
            DiagnosticMethodsEnum.weighted_projector_error,
        }
        assert all(
            observations[method].options is not None
            and observations[method].options.matrix_norm is MatrixNormEnum.frobenius
            for method in matrix_methods
        )
        assert isinstance(
            observations[DiagnosticMethodsEnum.scaled_eigenpair_residuals].atol.unit,
            Unitless,
        )

        reconstructed = Piab1dDiagnostics.from_json(result.diagnostics.to_json())
        assert set(reconstructed.observations) == set(DiagnosticMethodsEnum)
        assert (
            reconstructed.observations[
                DiagnosticMethodsEnum.projector_idempotency_error
            ].options
            is not None
        )
