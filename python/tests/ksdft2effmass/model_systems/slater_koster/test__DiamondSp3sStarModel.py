"""Synthetic verification of the diamond ``sp3s*`` Hamiltonian map."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.numerics.numpy.typing import Complex128Matrix, Float64Array
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
)

from ksdft2effmass.hamiltonian import HermitianHamiltonian
from ksdft2effmass.model_systems.slater_koster import (
    DiamondSp3sStarGeometry,
    DiamondSp3sStarModel,
    DiamondSp3sStarParameters,
)

pytestmark = pytest.mark.software_verification


class TestDiamondSp3sStarModel:
    """Own Slater--Koster signs, phases, Hermiticity, and cubic symmetry."""

    def test_two_center_hopping__direction_reversal__transposes_map(self) -> None:
        model = self._model()
        direction = np.asarray((1.0, -2.0, 3.0)) / np.sqrt(14.0)

        forward = model.two_center_hopping(2, direction)
        reverse = model.two_center_hopping(2, -direction)

        np.testing.assert_array_equal(reverse, forward.T)
        assert forward.flags.writeable is False
        assert forward[0, 1] == pytest.approx(direction[0] * 0.2)
        assert forward[1, 0] == pytest.approx(-direction[0] * 0.2)
        assert forward[0, 4] == pytest.approx(0.6)
        assert forward[4, 4] == pytest.approx(0.7)
        assert model.two_center_hopping(1, direction)[0, 4] == 0.0
        assert model.two_center_hopping(1, direction)[4, 4] == 0.0

    def test_hamiltonian_at__gamma__matches_complete_shell_sums(self) -> None:
        matrix = self._matrix(self._model(), np.zeros(3))

        expected_same_site = np.diag((-3.8, 5.4, 5.4, 5.4, 15.4))
        expected_same_site[0, 4] = 7.2
        expected_same_site[4, 0] = 7.2
        expected_cross_site = np.diag((8.0, 56.0 / 3.0, 56.0 / 3.0, 56.0 / 3.0, 0.0))
        np.testing.assert_allclose(
            matrix[0:5, 0:5], expected_same_site, rtol=0.0, atol=2.0e-15
        )
        np.testing.assert_allclose(
            matrix[0:5, 5:10], expected_cross_site, rtol=0.0, atol=4.0e-15
        )

    def test_hamiltonian_at__generic_k__is_hermitian_and_time_reversal_symmetric(
        self,
    ) -> None:
        model = self._model()
        k_point = np.asarray((0.137, -0.281, 0.419))

        hamiltonian = model.hamiltonian_at(k_point)
        matrix = self._matrix(model, k_point)
        reverse = self._matrix(model, -k_point)

        assert isinstance(hamiltonian, HermitianHamiltonian)
        np.testing.assert_array_equal(matrix, matrix.conjugate().T)
        np.testing.assert_allclose(
            reverse,
            matrix.conjugate(),
            rtol=0.0,
            atol=4.0e-15,
        )

    def test_hamiltonian_at__reciprocal_shift__obeys_center_gauge_covariance(
        self,
    ) -> None:
        model = self._model()
        k_point = np.asarray((0.13, 0.27, -0.19))
        reciprocal_shift = np.asarray((1.0, -2.0, 0.0))
        site_phase = np.exp(2.0j * np.pi * reciprocal_shift @ np.full(3, 0.25))
        gauge = np.diag(np.asarray((1.0,) * 5 + (site_phase,) * 5))

        shifted = self._matrix(model, k_point + reciprocal_shift)
        expected = gauge.conjugate().T @ self._matrix(model, k_point) @ gauge

        np.testing.assert_allclose(shifted, expected, rtol=0.0, atol=1.0e-14)
        np.testing.assert_allclose(
            np.linalg.eigvalsh(shifted),
            np.linalg.eigvalsh(expected),
            rtol=0.0,
            atol=1.0e-14,
        )

    def test_hamiltonian_at__cartesian_axis_permutation__preserves_spectrum(
        self,
    ) -> None:
        model = self._model()
        direct = model.geometry.normalized_direct_lattice.primitive_basis_matrix
        reduced_cartesian_k = np.asarray((0.11, -0.23, 0.37))
        permutation = np.asarray(((0.0, 1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)))
        k_point = direct.T @ reduced_cartesian_k
        permuted_k_point = direct.T @ permutation @ reduced_cartesian_k

        eigenvalues = np.linalg.eigvalsh(self._matrix(model, k_point))
        permuted_eigenvalues = np.linalg.eigvalsh(self._matrix(model, permuted_k_point))

        np.testing.assert_allclose(
            permuted_eigenvalues, eigenvalues, rtol=0.0, atol=3.0e-14
        )

    def test_hamiltonian_at__boolean_or_numeric_string__rejects(self) -> None:
        model = self._model()

        with pytest.raises(TypeError, match="real numbers excluding booleans"):
            model.hamiltonian_at(np.zeros(3, dtype=np.bool_))
        with pytest.raises(TypeError, match="real numbers excluding booleans"):
            model.hamiltonian_at(np.full(3, "0.0", dtype=np.str_))

    def test_hamiltonian_at__binary64_overflow__rejects_without_clipping(self) -> None:
        maximum = np.finfo(np.float64).max
        model = DiamondSp3sStarModel(
            geometry=self._model().geometry,
            parameters=DiamondSp3sStarParameters.from_vector_ev(np.full(15, maximum)),
        )

        with pytest.raises(OverflowError, match="overflowed"):
            model.hamiltonian_at(np.zeros(3))
        with pytest.raises(OverflowError, match="phase argument overflowed"):
            self._model().hamiltonian_at(np.full(3, maximum))

    @staticmethod
    def _matrix(
        model: DiamondSp3sStarModel,
        fractional_k: Float64Array,
    ) -> Complex128Matrix:
        matrix = model.hamiltonian_at(fractional_k).matrix
        assert isinstance(matrix, ComplexMatrixQuantity)
        return matrix.magnitude

    @staticmethod
    def _model() -> DiamondSp3sStarModel:
        return DiamondSp3sStarModel(
            geometry=DiamondSp3sStarGeometry(
                ScalarQuantity(5.4, PhysicalUnit("angstrom"))
            ),
            parameters=DiamondSp3sStarParameters.from_vector_ev(
                np.asarray(
                    (
                        -5.0,
                        1.0,
                        7.0,
                        2.0,
                        3.0,
                        4.0,
                        5.0,
                        6.0,
                        0.1,
                        0.2,
                        0.3,
                        0.4,
                        0.5,
                        0.6,
                        0.7,
                    )
                )
            ),
        )
