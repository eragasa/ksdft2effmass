"""Software evidence for the frozen nearest-neighbor silicon model class."""

from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest

from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.solid_state import (
    SiliconDiamondSp3sStarNearestNeighborConstructor,
    SiliconDiamondSp3sStarNearestNeighborModel,
    SiliconSp3sStarBlochHamiltonianConstructor,
    SiliconSp3sStarNearestNeighborParameters,
    SiliconSp3sStarParameter,
)

pytestmark = [pytest.mark.software_verification, pytest.mark.unit]


class TestSiliconDiamondSp3sStarNearestNeighborConstructor:
    """Establish the frozen basis, channels, symmetries, and Fourier convention."""

    @staticmethod
    def _parameters() -> SiliconSp3sStarNearestNeighborParameters:
        return SiliconSp3sStarNearestNeighborParameters(
            s_onsite=-4.2,
            p_onsite=1.1,
            s_star_onsite=6.3,
            ss_sigma=-1.8,
            sp_sigma=2.2,
            s_star_p_sigma=1.7,
            pp_sigma=3.0,
            pp_pi=-1.0,
        )

    @classmethod
    def _model(cls) -> SiliconDiamondSp3sStarNearestNeighborModel:
        return SiliconDiamondSp3sStarNearestNeighborModel(
            identifier="synthetic-silicon-nearest-neighbor-model",
            basis_identifier="A-then-B-sp3s-star-cubic-orbitals",
            parameters=cls._parameters(),
            lattice_constant=ScalarQuantity(5.43, PhysicalUnit("angstrom")),
            energy_unit=PhysicalUnit("electron_volt"),
            energy_reference="synthetic-zero",
        )

    def test_parameter_record_rejects_non_float_and_nonfinite_values(self) -> None:
        values = dict(
            s_onsite=-4.2,
            p_onsite=1.1,
            s_star_onsite=6.3,
            ss_sigma=-1.8,
            sp_sigma=2.2,
            s_star_p_sigma=1.7,
            pp_sigma=3.0,
            pp_pi=-1.0,
        )
        for invalid in (True, 1, "1.0"):
            candidate = values | {"pp_pi": invalid}
            with pytest.raises(TypeError, match="pp_pi must be a built-in float"):
                SiliconSp3sStarNearestNeighborParameters(**candidate)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="pp_pi must be finite"):
            SiliconSp3sStarNearestNeighborParameters(
                **(values | {"pp_pi": float("nan")})
            )

    def test_model_freezes_geometry_basis_spin_and_overlap(self) -> None:
        model = self._model()
        operator = SiliconDiamondSp3sStarNearestNeighborConstructor().execute(model)

        assert model.basis_labels == (
            "A:s",
            "A:px",
            "A:py",
            "A:pz",
            "A:s*",
            "B:s",
            "B:px",
            "B:py",
            "B:pz",
            "B:s*",
        )
        np.testing.assert_array_equal(
            model.primitive_vectors_in_cubic_axes.magnitude,
            np.asarray(
                (
                    (0.0, 0.5, 0.5),
                    (0.5, 0.0, 0.5),
                    (0.5, 0.5, 0.0),
                )
            ),
        )
        np.testing.assert_array_equal(
            model.basis_positions_in_cubic_axes.magnitude,
            np.asarray(((0.0, 0.0, 0.0), (0.25, 0.25, 0.25))),
        )
        np.testing.assert_array_equal(
            operator.overlap_matrix.magnitude, np.eye(10, dtype=np.complex128)
        )
        assert operator.cell_displacements == (
            (-1, 0, 0),
            (0, -1, 0),
            (0, 0, -1),
            (0, 0, 0),
            (0, 0, 1),
            (0, 1, 0),
            (1, 0, 0),
        )

    def test_constructor_exposes_complete_linear_operator_components(self) -> None:
        model = self._model()
        operator = SiliconDiamondSp3sStarNearestNeighborConstructor().execute(model)

        assert tuple(component.parameter for component in operator.components) == tuple(
            SiliconSp3sStarParameter
        )
        reconstructed = np.zeros((7, 10, 10), dtype=np.complex128)
        for component in operator.components:
            reconstructed += model.parameters.coefficient(
                component.parameter
            ) * np.asarray([block.magnitude for block in component.blocks])
        np.testing.assert_array_equal(
            reconstructed,
            np.asarray([block.magnitude for block in operator.blocks]),
        )

    def test_component_record_rejects_noncanonical_parameter_blocks(self) -> None:
        operator = SiliconDiamondSp3sStarNearestNeighborConstructor().execute(
            self._model()
        )
        ss_component = next(
            component
            for component in operator.components
            if component.parameter is SiliconSp3sStarParameter.SS_SIGMA
        )
        zero_blocks = tuple(
            ComplexMatrixQuantity(np.zeros((10, 10), dtype=np.complex128), Unitless())
            for _ in ss_component.blocks
        )

        with pytest.raises(ValueError, match="canonical parameter basis operator"):
            replace(ss_component, blocks=zero_blocks)

    def test_directed_tetrahedral_bond_uses_declared_parity_signs(self) -> None:
        operator = SiliconDiamondSp3sStarNearestNeighborConstructor().execute(
            self._model()
        )
        sp_component = next(
            component
            for component in operator.components
            if component.parameter is SiliconSp3sStarParameter.SP_SIGMA
        )
        origin_index = sp_component.cell_displacements.index((0, 0, 0))
        block = sp_component.blocks[origin_index].magnitude
        direction = np.full(3, 1.0 / np.sqrt(3.0))

        np.testing.assert_allclose(block[0, 6:9], direction, rtol=0.0, atol=0.0)
        np.testing.assert_allclose(block[1:4, 5], -direction, rtol=0.0, atol=0.0)
        np.testing.assert_allclose(block[5, 1:4], -direction, rtol=0.0, atol=0.0)
        np.testing.assert_allclose(block[6:9, 0], direction, rtol=0.0, atol=0.0)

    def test_all_directed_bonds_use_declared_sp_and_s_star_p_signs(self) -> None:
        operator = SiliconDiamondSp3sStarNearestNeighborConstructor().execute(
            self._model()
        )
        components = {
            component.parameter: component for component in operator.components
        }
        directed_bonds = (
            ((0, 0, 0), (1, 1, 1)),
            ((-1, 0, 0), (1, -1, -1)),
            ((0, -1, 0), (-1, 1, -1)),
            ((0, 0, -1), (-1, -1, 1)),
        )
        for displacement, signs in directed_bonds:
            direction = np.asarray(signs) / np.sqrt(3.0)
            index = operator.cell_displacements.index(displacement)
            sp_block = (
                components[SiliconSp3sStarParameter.SP_SIGMA].blocks[index].magnitude
            )
            s_star_p_block = (
                components[SiliconSp3sStarParameter.S_STAR_P_SIGMA]
                .blocks[index]
                .magnitude
            )
            np.testing.assert_allclose(sp_block[0, 6:9], direction, rtol=0.0, atol=0.0)
            np.testing.assert_allclose(sp_block[1:4, 5], -direction, rtol=0.0, atol=0.0)
            np.testing.assert_allclose(
                s_star_p_block[4, 6:9], direction, rtol=0.0, atol=0.0
            )
            np.testing.assert_allclose(
                s_star_p_block[1:4, 9], -direction, rtol=0.0, atol=0.0
            )

    def test_omitted_nearest_neighbor_channels_are_exact_zero(self) -> None:
        operator = SiliconDiamondSp3sStarNearestNeighborConstructor().execute(
            self._model()
        )
        displacement_index = operator.cell_displacements.index((-1, 0, 0))
        directed_ab = operator.blocks[displacement_index].magnitude[0:5, 5:10]

        assert directed_ab[0, 4] == 0.0
        assert directed_ab[4, 0] == 0.0
        assert directed_ab[4, 4] == 0.0
        np.testing.assert_array_equal(
            operator.blocks[displacement_index].magnitude[0:5, 0:5],
            np.zeros((5, 5)),
        )

    def test_gamma_point_respects_tetrahedral_p_orbital_symmetry(self) -> None:
        parameters = SiliconSp3sStarNearestNeighborParameters(
            s_onsite=0.0,
            p_onsite=0.0,
            s_star_onsite=0.0,
            ss_sigma=0.0,
            sp_sigma=2.0,
            s_star_p_sigma=0.0,
            pp_sigma=3.0,
            pp_pi=-1.0,
        )
        model = SiliconDiamondSp3sStarNearestNeighborModel(
            identifier="tetrahedral-symmetry-case",
            basis_identifier="A-then-B-sp3s-star-cubic-orbitals",
            parameters=parameters,
            lattice_constant=ScalarQuantity(1.0, PhysicalUnit("angstrom")),
            energy_unit=PhysicalUnit("electron_volt"),
            energy_reference="zero",
        )
        operator = SiliconDiamondSp3sStarNearestNeighborConstructor().execute(model)
        samples = SiliconSp3sStarBlochHamiltonianConstructor().execute(
            operator, MatrixQuantity(np.zeros((1, 3)), Unitless())
        )
        ab = samples.matrices[0].magnitude[0:5, 5:10]

        np.testing.assert_allclose(ab[0, 1:4], np.zeros(3), atol=1.0e-15)
        np.testing.assert_allclose(ab[1:4, 0], np.zeros(3), atol=1.0e-15)
        np.testing.assert_allclose(ab[1:4, 1:4], (4.0 / 3.0) * np.eye(3), atol=1.0e-15)

    def test_real_and_reciprocal_operators_are_hermitian(self) -> None:
        operator = SiliconDiamondSp3sStarNearestNeighborConstructor().execute(
            self._model()
        )
        indexed = dict(zip(operator.cell_displacements, operator.blocks, strict=True))
        for displacement, block in indexed.items():
            reverse = (-displacement[0], -displacement[1], -displacement[2])
            np.testing.assert_array_equal(
                indexed[reverse].magnitude, block.magnitude.conj().T
            )

        samples = SiliconSp3sStarBlochHamiltonianConstructor().execute(
            operator,
            MatrixQuantity(
                np.asarray(((0.0, 0.0, 0.0), (0.17, -0.31, 0.43))), Unitless()
            ),
        )
        for matrix in samples.matrices:
            np.testing.assert_allclose(
                matrix.magnitude, matrix.magnitude.conj().T, atol=2.0e-15
            )

    def test_positive_cell_fourier_phase_matches_complex_hand_oracle(self) -> None:
        parameters = SiliconSp3sStarNearestNeighborParameters(
            s_onsite=0.0,
            p_onsite=0.0,
            s_star_onsite=0.0,
            ss_sigma=1.0,
            sp_sigma=0.0,
            s_star_p_sigma=0.0,
            pp_sigma=0.0,
            pp_pi=0.0,
        )
        model = replace(self._model(), parameters=parameters)
        operator = SiliconDiamondSp3sStarNearestNeighborConstructor().execute(model)
        q = np.asarray((0.17, -0.31, 0.43))
        samples = SiliconSp3sStarBlochHamiltonianConstructor().execute(
            operator,
            MatrixQuantity(np.asarray((q, q + (1.0, -2.0, 3.0))), Unitless()),
        )
        expected_ab = (
            1.0
            + np.exp(-2j * np.pi * q[0])
            + np.exp(-2j * np.pi * q[1])
            + np.exp(-2j * np.pi * q[2])
        )

        assert abs(expected_ab.imag) > 0.1
        np.testing.assert_allclose(
            samples.matrices[0].magnitude[0, 5],
            expected_ab,
            rtol=0.0,
            atol=1.0e-15,
        )
        np.testing.assert_allclose(
            samples.matrices[0].magnitude,
            samples.matrices[1].magnitude,
            atol=1.0e-14,
        )

    def test_bloch_samples_reject_matrices_unrelated_to_the_operator(self) -> None:
        operator = SiliconDiamondSp3sStarNearestNeighborConstructor().execute(
            self._model()
        )
        samples = SiliconSp3sStarBlochHamiltonianConstructor().execute(
            operator, MatrixQuantity(np.zeros((1, 3)), Unitless())
        )
        corrupted = ComplexMatrixQuantity(
            samples.matrices[0].magnitude + np.eye(10),
            samples.matrices[0].unit,
        )

        with pytest.raises(ValueError, match="positive-phase Fourier sum"):
            replace(samples, matrices=(corrupted,))

    def test_zero_hopping_limit_is_the_declared_onsite_operator(self) -> None:
        parameters = SiliconSp3sStarNearestNeighborParameters(
            s_onsite=-4.0,
            p_onsite=1.0,
            s_star_onsite=6.0,
            ss_sigma=0.0,
            sp_sigma=0.0,
            s_star_p_sigma=0.0,
            pp_sigma=0.0,
            pp_pi=0.0,
        )
        model = SiliconDiamondSp3sStarNearestNeighborModel(
            identifier="onsite-limit",
            basis_identifier="A-then-B-sp3s-star-cubic-orbitals",
            parameters=parameters,
            lattice_constant=ScalarQuantity(5.43, PhysicalUnit("angstrom")),
            energy_unit=PhysicalUnit("electron_volt"),
            energy_reference="zero",
        )
        operator = SiliconDiamondSp3sStarNearestNeighborConstructor().execute(model)
        samples = SiliconSp3sStarBlochHamiltonianConstructor().execute(
            operator,
            MatrixQuantity(
                np.asarray(((0.0, 0.0, 0.0), (0.23, 0.37, -0.11))), Unitless()
            ),
        )
        expected = np.diag((-4.0, 1.0, 1.0, 1.0, 6.0) * 2)

        for matrix in samples.matrices:
            np.testing.assert_array_equal(matrix.magnitude, expected)
