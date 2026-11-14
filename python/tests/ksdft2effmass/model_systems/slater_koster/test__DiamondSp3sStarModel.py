"""Synthetic verification of the KSD diamond ``sp3s*`` composition."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.numerics.numpy.typing import Complex128Matrix, Float64Array
from projectkoios.physkit.periodic.lattice.hopping import DenseBlockHoppingModel
from projectkoios.physkit.solidstate.tb.bloch import DenseBlockHoppingBlochEvaluator
from projectkoios.physkit.solidstate.tb.slater_koster import (
    HOMOPOLAR_SP3S_STAR_CHANNEL_ORDER,
    HomopolarSp3sStarCellGaugeModelAssembler,
)
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    UnitSystem,
)

import ksdft2effmass.model_systems as model_systems_package
import ksdft2effmass.model_systems.slater_koster as slater_koster_package
from ksdft2effmass.hamiltonian import HermitianHamiltonian
from ksdft2effmass.model_systems.slater_koster import (
    DiamondSp3sStarBlochHamiltonianEvaluation,
    DiamondSp3sStarGeometry,
    DiamondSp3sStarModel,
    DiamondSp3sStarParameters,
)
from ksdft2effmass.periodic.operators.basis import (
    PeriodicBasisFamily,
    SlaterKosterOrbital,
    SlaterKosterOrbitalBasisCoordinate,
)

pytestmark = pytest.mark.software_verification


class TestDiamondSp3sStarModel:
    """Own concrete composition, owner delegation, and represented symmetries."""

    def test_public_surface__retired_orbital_index__has_no_compatibility_alias(
        self,
    ) -> None:
        assert "Sp3sStarOrbitalIndex" not in slater_koster_package.__all__
        assert not hasattr(slater_koster_package, "Sp3sStarOrbitalIndex")
        assert "Sp3sStarOrbitalIndex" not in model_systems_package.__all__
        assert not hasattr(model_systems_package, "Sp3sStarOrbitalIndex")

    def test_basis_identity__model_order__uses_descriptive_center_coordinates(
        self,
    ) -> None:
        basis = self._model().basis_identity

        assert basis.family is PeriodicBasisFamily.SLATER_KOSTER_ORBITAL
        assert basis.dimension == 10
        assert basis.coordinates[0] == SlaterKosterOrbitalBasisCoordinate(
            site_label="diamond_origin_center",
            orbital=SlaterKosterOrbital.S,
        )
        assert basis.coordinates[4] == SlaterKosterOrbitalBasisCoordinate(
            site_label="diamond_origin_center",
            orbital=SlaterKosterOrbital.S_STAR,
        )
        assert basis.coordinates[5] == SlaterKosterOrbitalBasisCoordinate(
            site_label="diamond_body_diagonal_quarter_center",
            orbital=SlaterKosterOrbital.S,
        )
        assert basis.coordinates[-1] == SlaterKosterOrbitalBasisCoordinate(
            site_label="diamond_body_diagonal_quarter_center",
            orbital=SlaterKosterOrbital.S_STAR,
        )

    def test_cell_gauge_model__composition__uses_physkit_model_owner(self) -> None:
        model = self._model().cell_gauge_model

        assert type(model) is DenseBlockHoppingModel
        assert model.basis_size == 10
        assert model.basis_identifier == "diamond-spinless-sp3s-star"
        assert model.energy_unit == PhysicalUnit("electron_volt")
        assert tuple(term.displacement.components for term in model.terms) == (
            (-1, 0, 0),
            (-1, 0, 1),
            (-1, 1, 0),
            (0, -1, 0),
            (0, -1, 1),
            (0, 0, -1),
            (0, 0, 0),
            (0, 0, 1),
            (0, 1, -1),
            (0, 1, 0),
            (1, -1, 0),
            (1, 0, -1),
            (1, 0, 0),
        )

    def test_linear_hopping_bloch__reconstructs_direct_hopping_model(self) -> None:
        model = self._model()
        points = MatrixQuantity(
            magnitude=np.asarray(
                (
                    (0.0, 0.0, 0.0),
                    (0.137, -0.281, 0.419),
                )
            ),
            unit=UnitSystem.NONDIMENSIONAL.length_unit,
        )

        evaluation = model.linear_hopping_bloch(fractional_wave_vectors=points)
        parameterization = evaluation.parameterization
        direct = DenseBlockHoppingBlochEvaluator().evaluate(
            HomopolarSp3sStarCellGaugeModelAssembler()
            .execute(definition=parameterization.definition)
            .model,
            points,
        )

        assert parameterization.parameter_group_identifiers == (
            "diamond-first-neighbor",
            "diamond-second-neighbor",
        )
        assert parameterization.channel_order == HOMOPOLAR_SP3S_STAR_CHANNEL_ORDER
        assert tuple(len(models) for models in parameterization.channel_models) == (
            7,
            7,
        )
        first_integrals = parameterization.definition.parameter_groups[
            0
        ].integrals.ordered_quantities
        assert first_integrals[5].magnitude == 0.0
        assert first_integrals[6].magnitude == 0.0
        for sample_index, expected in enumerate(direct.bloch_matrices):
            reconstructed = np.zeros((10, 10), dtype=np.complex128)
            for group, channel_matrices in zip(
                parameterization.definition.parameter_groups,
                evaluation.bloch_matrices,
                strict=True,
            ):
                for scalar, sample_matrices in zip(
                    group.integrals.ordered_quantities,
                    channel_matrices,
                    strict=True,
                ):
                    reconstructed += (
                        scalar.magnitude * sample_matrices[sample_index].magnitude
                    )
            np.testing.assert_allclose(
                reconstructed,
                expected.magnitude,
                rtol=0.0,
                atol=2.0e-14,
            )

    def test_two_center_hopping__direction_reversal__transposes_map(self) -> None:
        model = self._model()
        direction = np.asarray((1.0, -2.0, 3.0)) / np.sqrt(14.0)

        forward = model.two_center_hopping(shell=2, direction_cosines=direction)
        reverse = model.two_center_hopping(shell=2, direction_cosines=-direction)

        np.testing.assert_array_equal(reverse, forward.T)
        assert forward.flags.writeable is False
        assert forward[0, 1] == pytest.approx(direction[0] * 0.2)
        assert forward[1, 0] == pytest.approx(-direction[0] * 0.2)
        assert forward[0, 4] == pytest.approx(0.6)
        assert forward[4, 4] == pytest.approx(0.7)
        first = model.two_center_hopping(shell=1, direction_cosines=direction)
        assert first[0, 4] == 0.0
        assert first[4, 4] == 0.0

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

        evaluation = model.hamiltonian_at(fractional_k=k_point)
        matrix = self._matrix(model, k_point)
        reverse = self._matrix(model, -k_point)

        assert type(evaluation) is DiamondSp3sStarBlochHamiltonianEvaluation
        assert type(evaluation.hamiltonian) is HermitianHamiltonian
        np.testing.assert_array_equal(matrix, matrix.conjugate().T)
        np.testing.assert_allclose(
            reverse,
            matrix.conjugate(),
            rtol=0.0,
            atol=4.0e-15,
        )

    def test_hamiltonian_at__evaluation__correlates_model_fiber_and_basis(
        self,
    ) -> None:
        model = self._model()
        fractional_k = np.asarray((0.137, -0.281, 0.419))
        expected_k = fractional_k.copy()

        evaluation = model.hamiltonian_at(fractional_k=fractional_k)
        fractional_k[:] = 0.0

        assert evaluation.model is model
        assert evaluation.basis_identity is model.basis_identity
        np.testing.assert_array_equal(evaluation.fractional_k, expected_k)
        assert evaluation.fractional_k.flags.writeable is False
        assert type(evaluation.hamiltonian.matrix) is ComplexMatrixQuantity
        assert evaluation.hamiltonian.matrix.magnitude.shape == (10, 10)

    def test_evaluation_construction__wrong_matrix_dimension__raises_value_error(
        self,
    ) -> None:
        model = self._model()
        source = model.hamiltonian_at(fractional_k=np.zeros(3))

        with pytest.raises(ValueError, match="ten-orbital basis"):
            DiamondSp3sStarBlochHamiltonianEvaluation(
                model=model,
                fractional_k=np.zeros(3),
                hamiltonian=HermitianHamiltonian(
                    matrix=ComplexMatrixQuantity(
                        np.eye(2, dtype=np.complex128),
                        source.hamiltonian.matrix.unit,
                    )
                ),
            )

    def test_hamiltonian_at__reciprocal_shift__obeys_center_gauge_covariance(
        self,
    ) -> None:
        model = self._model()
        k_point = np.asarray((0.13, 0.27, -0.19))
        reciprocal_shift = np.asarray((1.0, -2.0, 0.0))
        site_phase = np.exp(2.0j * np.pi * reciprocal_shift @ np.full(3, 0.25))
        gauge = np.diag(np.asarray((1.0,) * 5 + (site_phase,) * 5))

        np.testing.assert_allclose(
            gauge.conjugate().T @ gauge,
            np.eye(10),
            rtol=0.0,
            atol=np.finfo(np.float64).eps,
        )
        shifted = self._matrix(model, k_point + reciprocal_shift)
        expected = gauge.conjugate().T @ self._matrix(model, k_point) @ gauge

        np.testing.assert_allclose(shifted, expected, rtol=0.0, atol=1.0e-14)

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
            model.hamiltonian_at(fractional_k=np.zeros(3, dtype=np.bool_))
        with pytest.raises(TypeError, match="real numbers excluding booleans"):
            model.hamiltonian_at(fractional_k=np.full(3, "0.0", dtype=np.str_))

    def test_hamiltonian_at__binary64_overflow__rejects_without_clipping(self) -> None:
        maximum = np.finfo(np.float64).max
        model = DiamondSp3sStarModel(
            geometry=self._model().geometry,
            parameters=DiamondSp3sStarParameters.from_vector_ev(
                values=np.full(15, maximum)
            ),
        )

        with pytest.raises(OverflowError, match="overflowed"):
            model.hamiltonian_at(fractional_k=np.zeros(3))
        with pytest.raises(OverflowError, match="phase argument overflowed"):
            self._model().hamiltonian_at(fractional_k=np.full(3, maximum))

    @staticmethod
    def _matrix(
        model: DiamondSp3sStarModel,
        fractional_k: Float64Array,
    ) -> Complex128Matrix:
        matrix = model.hamiltonian_at(fractional_k=fractional_k).hamiltonian.matrix
        assert isinstance(matrix, ComplexMatrixQuantity)
        return matrix.magnitude

    @staticmethod
    def _model() -> DiamondSp3sStarModel:
        return DiamondSp3sStarModel(
            geometry=DiamondSp3sStarGeometry(
                lattice_parameter=ScalarQuantity(5.4, PhysicalUnit("angstrom"))
            ),
            parameters=DiamondSp3sStarParameters.from_vector_ev(
                values=np.asarray(
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
