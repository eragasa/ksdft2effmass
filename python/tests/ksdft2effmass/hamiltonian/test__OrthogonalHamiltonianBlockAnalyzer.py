"""Software verification of orthogonal Hamiltonian block analysis."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.physkit.units import MatrixQuantity, Unitless, VectorQuantity

from ksdft2effmass.hamiltonian import (
    Hamiltonian,
    OrthogonalHamiltonianBlockAnalyzer,
    OrthogonalSpectralSubspace,
)

pytestmark = pytest.mark.software_verification
SUT = OrthogonalHamiltonianBlockAnalyzer


class TestOrthogonalHamiltonianBlockAnalyzer:
    """Own the uninterpreted four-block decomposition contract."""

    def test_execute__coupled_two_sector_matrix__returns_all_four_blocks(self) -> None:
        matrix = MatrixQuantity(np.array([[2.0, 1.0], [1.0, 3.0]]), Unitless())
        hamiltonian = Hamiltonian(matrix=matrix)
        subspace = OrthogonalSpectralSubspace(
            eigenvalues=VectorQuantity(np.array([2.0]), Unitless()),
            basis_vectors=MatrixQuantity(np.array([[1.0], [0.0]]), Unitless()),
        )

        result = SUT().execute(hamiltonian, subspace)

        assert result.hamiltonian is hamiltonian
        assert result.spectral_subspace is subspace
        np.testing.assert_array_equal(
            result.retained.magnitude, np.array([[2.0, 0.0], [0.0, 0.0]])
        )
        np.testing.assert_array_equal(
            result.retained_to_discarded.magnitude,
            np.array([[0.0, 1.0], [0.0, 0.0]]),
        )
        np.testing.assert_array_equal(
            result.discarded_to_retained.magnitude,
            np.array([[0.0, 0.0], [1.0, 0.0]]),
        )
        np.testing.assert_array_equal(
            result.discarded.magnitude, np.array([[0.0, 0.0], [0.0, 3.0]])
        )
        reconstructed = (
            result.retained.magnitude
            + result.retained_to_discarded.magnitude
            + result.discarded_to_retained.magnitude
            + result.discarded.magnitude
        )
        np.testing.assert_array_equal(reconstructed, matrix.magnitude)
