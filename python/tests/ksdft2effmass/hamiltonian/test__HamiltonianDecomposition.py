"""Verification for the reusable Hamiltonian decomposition composition."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.physkit.units import (
    MatrixQuantity,
    Unitless,
    VectorQuantity,
)

import ksdft2effmass.hamiltonian as hamiltonian_package
from ksdft2effmass.hamiltonian import (
    Hamiltonian,
    HamiltonianDecomposition,
    OrthogonalSpectralSubspace,
    ReducedHamiltonian,
)

pytestmark = pytest.mark.software_verification


class TestHamiltonianDecomposition:
    """Own composition, dimension independence, and public-surface behavior."""

    @staticmethod
    def reduced(matrix: MatrixQuantity) -> ReducedHamiltonian:
        dimension = matrix.magnitude.shape[0]
        identity = MatrixQuantity(np.eye(dimension), Unitless())
        return ReducedHamiltonian(
            matrix=matrix,
            spectral_subspace=OrthogonalSpectralSubspace(
                eigenvalues=VectorQuantity(
                    np.arange(dimension, dtype=float), Unitless()
                ),
                basis_vectors=identity,
            ),
            embedded=Hamiltonian(matrix=matrix),
        )

    def test_execute__two_dimensional_input__runs_verifies_and_visualizes(self) -> None:
        hamiltonian = MatrixQuantity(
            np.array([[2.0, 0.25], [0.25, 5.0]], dtype=np.float64),
            Unitless(),
        )
        shift = MatrixQuantity(
            np.array([[0.5, -0.75], [-0.75, -0.25]], dtype=np.float64),
            Unitless(),
        )

        result = HamiltonianDecomposition(self.reduced(hamiltonian), shift).execute()

        assert result.verification.passed
        assert result.verification.issues == ()
        np.testing.assert_allclose(
            result.calculation.alternative_kinetic.magnitude
            + result.calculation.alternative_potential.magnitude,
            hamiltonian.magnitude,
            rtol=0.0,
            atol=2.0e-14,
        )
        np.testing.assert_array_equal(
            result.calculation.alternative_potential.magnitude,
            shift.magnitude,
        )
        assert result.visualization.media_type == "image/png"
        assert result.visualization.png.startswith(b"\x89PNG\r\n\x1a\n")

    @pytest.mark.numerical_verification
    def test_execute__piab1d_declared_shift__preserves_model_class_norms(self) -> None:
        reduced_hamiltonian = MatrixQuantity(
            np.array(
                [
                    [
                        4.884897716341421,
                        -9.782766946686441e-15,
                        -5.948489225594269e-15,
                    ],
                    [
                        -1.1169260312949949e-14,
                        18.950400107362785,
                        -3.3526846137020598e-15,
                    ],
                    [
                        -3.0400725571433525e-15,
                        -3.748539189034861e-15,
                        40.49999999999998,
                    ],
                ],
                dtype=np.float64,
            ),
            Unitless(),
        )
        shift = MatrixQuantity(
            np.array(
                [
                    [0.5, 1.0, 0.4],
                    [1.0, -0.25, -0.75],
                    [0.4, -0.75, 0.75],
                ],
                dtype=np.float64,
            ),
            Unitless(),
        )

        result = HamiltonianDecomposition(
            self.reduced(reduced_hamiltonian), shift
        ).execute()

        observed = tuple(
            fit.unexplained_frobenius_norm.magnitude
            for fit in result.calculation.model_class_fits
        )
        expected = (
            1.9966638842495916,
            1.8560711193270587,
            0.5656854249492381,
            0.0,
        )
        np.testing.assert_allclose(observed, expected, rtol=0.0, atol=2.0e-15)

    def test_constructor__nonsymmetric_shift__fails_before_calculation(self) -> None:
        hamiltonian = MatrixQuantity(np.eye(2), Unitless())
        shift = MatrixQuantity(
            np.array([[0.0, 1.0], [0.0, 0.0]], dtype=np.float64),
            Unitless(),
        )

        with pytest.raises(ValueError, match="shift must be real symmetric"):
            HamiltonianDecomposition(self.reduced(hamiltonian), shift).execute()

    def test_constructor__boolean_numeric_controls__rejects(self) -> None:
        hamiltonian = MatrixQuantity(np.eye(2), Unitless())
        shift = MatrixQuantity(np.zeros((2, 2)), Unitless())

        with pytest.raises(TypeError, match="absolute_tolerance"):
            HamiltonianDecomposition(
                self.reduced(hamiltonian),
                shift,
                absolute_tolerance=True,
            )
        with pytest.raises(TypeError, match="visualization_dpi"):
            HamiltonianDecomposition(
                self.reduced(hamiltonian),
                shift,
                visualization_dpi=True,
            )

    def test_package__public_surface__exports_hamiltonian_domain_objects(self) -> None:
        assert hamiltonian_package.__all__ == [
            "Hamiltonian",
            "HamiltonianDecomposition",
            "HamiltonianVerification",
            "HermitianHamiltonian",
            "OrthogonalHamiltonianBlockAnalyzer",
            "OrthogonalHamiltonianBlockResult",
            "OrthogonalSpectralSubspace",
            "OrthogonalSpectralSubspaceSelector",
            "ReducedHamiltonian",
            "SpectralReduction",
            "SpectralReductionVerification",
            "SpectralSubspace",
        ]
