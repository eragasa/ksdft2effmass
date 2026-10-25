"""Software verification of cohesive PIAB1D diagnostic analyzers."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.physkit.linalg.matrix.norm import MatrixNormEnum
from projectkoios.physkit.units import (
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.analysis import MatrixNormDiagnosticOptions
from ksdft2effmass.model_systems.piab1d import (
    DiagnosticMethodsEnum,
    DiscreteSpectrumMaximumAbsoluteErrorAnalyzer,
    ProjectorIdempotencyAnalyzer,
    ScaledEigenpairResidualAnalyzer,
    SpectralReconstructionErrorAnalyzer,
    WeightedGramErrorAnalyzer,
    WeightedProjectorErrorAnalyzer,
)

pytestmark = pytest.mark.software_verification


class TestDiagnosticAnalyzers:
    """Own direct behavior of each PIAB1D diagnostic analyzer."""

    def test_discrete_spectrum__declared_reference__returns_maximum_error(self) -> None:
        energy = PhysicalUnit("electron_volt")
        analyzer = DiscreteSpectrumMaximumAbsoluteErrorAnalyzer(
            computed=VectorQuantity(np.array([1.0, 3.0]), energy),
            reference=VectorQuantity(np.array([1.0, 2.0]), energy),
            atol=ScalarQuantity(1.0e-12, energy),
            rtol=0.0,
        )

        observation = analyzer.result()

        assert analyzer.method is (
            DiagnosticMethodsEnum.discrete_spectrum_maximum_absolute_error
        )
        assert observation.value.magnitude == 1.0
        assert observation.options is None

    def test_scaled_eigenpair_residual__declared_vector__retains_values(self) -> None:
        residuals = VectorQuantity(np.array([1.0e-14, 2.0e-14]), Unitless())
        analyzer = ScaledEigenpairResidualAnalyzer(
            residuals=residuals,
            atol=ScalarQuantity(1.0e-12, Unitless()),
            rtol=0.0,
        )

        observation = analyzer.result()

        assert analyzer.method is DiagnosticMethodsEnum.scaled_eigenpair_residuals
        assert observation.value is residuals
        assert observation.options is None

    def test_spectral_reconstruction__exact_eigensystem__returns_zero(self) -> None:
        energy = PhysicalUnit("electron_volt")
        options = MatrixNormDiagnosticOptions(MatrixNormEnum.frobenius)
        analyzer = SpectralReconstructionErrorAnalyzer(
            hamiltonian=MatrixQuantity(np.diag([1.0, 2.0]), energy),
            eigenvalues=VectorQuantity(np.array([1.0, 2.0]), energy),
            eigenvectors=MatrixQuantity(np.eye(2), Unitless()),
            atol=ScalarQuantity(1.0e-12, energy),
            rtol=0.0,
            options=options,
        )

        observation = analyzer.result()

        assert analyzer.method is DiagnosticMethodsEnum.spectral_reconstruction_error
        assert observation.value.magnitude == 0.0
        assert observation.options is options

    def test_projector_idempotency__selected_norm__returns_declared_error(self) -> None:
        options = MatrixNormDiagnosticOptions(MatrixNormEnum.maximum_absolute_entry)
        analyzer = ProjectorIdempotencyAnalyzer(
            projector=MatrixQuantity(np.diag([1.0, 0.5]), Unitless()),
            atol=ScalarQuantity(1.0e-12, Unitless()),
            rtol=0.0,
            options=options,
        )

        observation = analyzer.result()

        assert analyzer.method is DiagnosticMethodsEnum.projector_idempotency_error
        assert observation.value.magnitude == 0.25
        assert observation.options is options

    def test_weighted_gram__identity__returns_zero(self) -> None:
        options = MatrixNormDiagnosticOptions(MatrixNormEnum.frobenius)
        analyzer = WeightedGramErrorAnalyzer(
            weighted_gram=MatrixQuantity(np.eye(2), Unitless()),
            atol=ScalarQuantity(1.0e-12, Unitless()),
            rtol=0.0,
            options=options,
        )

        observation = analyzer.result()

        assert analyzer.method is DiagnosticMethodsEnum.weighted_gram_error
        assert observation.value.magnitude == 0.0
        assert observation.options is options

    def test_weighted_projector__matching_projectors__returns_zero(self) -> None:
        options = MatrixNormDiagnosticOptions(MatrixNormEnum.frobenius)
        projector = MatrixQuantity(np.diag([1.0, 0.0]), Unitless())
        analyzer = WeightedProjectorErrorAnalyzer(
            weighted_projector=projector,
            projector=projector,
            atol=ScalarQuantity(1.0e-12, Unitless()),
            rtol=0.0,
            options=options,
        )

        observation = analyzer.result()

        assert analyzer.method is DiagnosticMethodsEnum.weighted_projector_error
        assert observation.value.magnitude == 0.0
        assert observation.options is options
