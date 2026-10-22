"""Software and analytic controls for the Vogl 1983 LCAO model."""

from __future__ import annotations

from dataclasses import fields
from pathlib import Path

import numpy as np
import pytest
from vogl1983_lcao_sp3sstar import (
    Vogl1983BasisIndex,
    Vogl1983Compound,
    Vogl1983HamiltonianBlocks,
    Vogl1983LcaoSp3sStarModel,
    Vogl1983StructureFactors,
    Vogl1983Table1,
)

TABLE_PATH = Path(__file__).resolve().parents[1] / "table1.json"


class TestVogl1983LcaoSp3sStarModel:
    """Check the accepted table and the finite Bloch representation."""

    @staticmethod
    def table() -> Vogl1983Table1:
        """Load the calculation-owned Table 1 document."""
        return Vogl1983Table1.from_json(TABLE_PATH)

    def test_table_has_complete_printed_inventory(self) -> None:
        """The typed table contains the 16 printed compounds and 13 values each."""
        table = self.table()

        assert table.compounds == tuple(Vogl1983Compound)
        assert len(table.rows) == 16
        assert all(len(fields(row.parameters)) == 13 for row in table.rows)
        assert table.doi == "10.1016/0022-3697(83)90064-1"

    def test_silicon_row_matches_vogl_table(self) -> None:
        """The silicon values are the accepted four-decimal Table 1 values."""
        parameters = self.table().parameters_for(Vogl1983Compound.SI)

        assert parameters.e_s_a == -4.2000
        assert parameters.e_p_a == 1.7150
        assert parameters.e_s_c == -4.2000
        assert parameters.e_p_c == 1.7150
        assert parameters.e_s_star_a == 6.6850
        assert parameters.e_s_star_c == 6.6850
        assert parameters.v_s_s == -8.3000
        assert parameters.v_x_x == 1.7150
        assert parameters.v_x_y == 4.5750
        assert parameters.v_s_a_p_c == 5.7292
        assert parameters.v_s_c_p_a == 5.7292
        assert parameters.v_s_star_a_p_c == 5.3749
        assert parameters.v_p_a_s_star_c == 5.3749

    def test_basis_is_ten_orbital_anion_then_cation_order(self) -> None:
        """The basis index contract is explicit and complete."""
        assert tuple(index.value for index in Vogl1983BasisIndex) == tuple(range(10))
        assert Vogl1983BasisIndex.S_A.value == 0
        assert Vogl1983BasisIndex.S_STAR_A.value == 4
        assert Vogl1983BasisIndex.S_C.value == 5
        assert Vogl1983BasisIndex.S_STAR_C.value == 9

    def test_structure_factors_have_gamma_and_x_controls(self) -> None:
        """Equation (6) reduces to its analytic Gamma and X values."""
        gamma = Vogl1983LcaoSp3sStarModel.structure_factors((0.0, 0.0, 0.0))
        x_point = Vogl1983LcaoSp3sStarModel.structure_factors((0.0, 0.0, 1.0))

        assert isinstance(gamma, Vogl1983StructureFactors)
        np.testing.assert_array_equal(
            gamma.as_array(),
            np.asarray((1.0, 0.0, 0.0, 0.0)),
        )
        np.testing.assert_allclose(
            x_point.as_array(),
            np.asarray((0.0, 0.0, 0.0, 1.0j)),
            rtol=0.0,
            atol=1.0e-15,
        )
        assert not gamma.as_array().flags.writeable
        assert not x_point.as_array().flags.writeable

    def test_structure_factors_match_published_bond_phase_combinations(
        self,
    ) -> None:
        """Equation (6) equals the four signed tetrahedral phase averages."""
        q = np.asarray((0.173, -0.281, 0.419))
        tetrahedral_directions = np.asarray(
            (
                (1.0, 1.0, 1.0),
                (1.0, -1.0, -1.0),
                (-1.0, 1.0, -1.0),
                (-1.0, -1.0, 1.0),
            )
        )
        combination_signs = np.asarray(
            (
                (1.0, 1.0, 1.0, 1.0),
                (1.0, 1.0, -1.0, -1.0),
                (1.0, -1.0, 1.0, -1.0),
                (1.0, -1.0, -1.0, 1.0),
            )
        )
        bond_phases = np.exp(0.5j * np.pi * (tetrahedral_directions @ q))
        expected = 0.25 * combination_signs @ bond_phases

        np.testing.assert_allclose(
            Vogl1983LcaoSp3sStarModel.structure_factors(q).as_array(),
            expected,
            rtol=0.0,
            atol=1.0e-15,
        )

    def test_hamiltonian_blocks_are_named_owned_and_read_only(self) -> None:
        """The paper-level block record owns immutable five-by-five arrays."""
        model = Vogl1983LcaoSp3sStarModel.from_table(self.table(), "Si")

        blocks = model.hamiltonian_blocks((0.173, -0.281, 0.419))

        assert isinstance(blocks, Vogl1983HamiltonianBlocks)
        assert blocks.onsite_anion.shape == (5, 5)
        assert blocks.anion_to_cation.shape == (5, 5)
        assert blocks.onsite_cation.shape == (5, 5)
        assert not blocks.onsite_anion.flags.writeable
        assert not blocks.anion_to_cation.flags.writeable
        assert not blocks.onsite_cation.flags.writeable

    def test_hamiltonian_is_read_only_and_hermitian(self) -> None:
        """The finite representation is a read-only 10 by 10 Hermitian matrix."""
        model = Vogl1983LcaoSp3sStarModel.from_table(self.table(), Vogl1983Compound.SI)

        hamiltonian = model.hamiltonian((0.173, -0.281, 0.419))

        assert hamiltonian.shape == (10, 10)
        assert hamiltonian.dtype == np.complex128
        assert not hamiltonian.flags.writeable
        np.testing.assert_array_equal(hamiltonian, hamiltonian.conjugate().T)

    def test_hamiltonian_entries_follow_published_basis_and_parameter_slots(
        self,
    ) -> None:
        """Named entries expose the paper's onsite, hopping, and zero pattern."""
        model = Vogl1983LcaoSp3sStarModel.from_table(self.table(), "Si")
        q = (0.173, -0.281, 0.419)
        factors = model.structure_factors(q)
        g_0 = factors.g0
        g_1 = factors.g1
        hamiltonian = model.hamiltonian(q)
        p = model.parameters
        basis = Vogl1983BasisIndex

        assert hamiltonian[basis.S_A, basis.S_A] == p.e_s_a
        assert hamiltonian[basis.P_X_A, basis.P_X_A] == p.e_p_a
        assert hamiltonian[basis.S_STAR_C, basis.S_STAR_C] == p.e_s_star_c
        assert hamiltonian[basis.S_A, basis.S_C] == p.v_s_s * g_0
        assert hamiltonian[basis.S_A, basis.P_X_C] == p.v_s_a_p_c * g_1
        assert hamiltonian[basis.P_X_A, basis.S_C] == -p.v_s_c_p_a * g_1
        assert hamiltonian[basis.P_X_A, basis.P_X_C] == p.v_x_x * g_0
        assert hamiltonian[basis.P_X_A, basis.S_STAR_C] == (-p.v_p_a_s_star_c * g_1)
        assert hamiltonian[basis.S_STAR_A, basis.P_X_C] == (p.v_s_star_a_p_c * g_1)
        assert hamiltonian[basis.S_A, basis.S_STAR_C] == 0.0
        assert hamiltonian[basis.S_STAR_A, basis.S_C] == 0.0
        assert hamiltonian[basis.S_STAR_A, basis.S_STAR_C] == 0.0

    def test_every_table_row_constructs_finite_gamma_and_x_spectra(self) -> None:
        """Every accepted Table 1 row defines a finite ten-band model."""
        table = self.table()

        for compound in table.compounds:
            model = Vogl1983LcaoSp3sStarModel.from_table(table, compound)
            for wavevector in ((0.0, 0.0, 0.0), (0.0, 0.0, 1.0)):
                energies = model.band_energies(wavevector)
                assert energies.shape == (10,)
                assert np.all(np.isfinite(energies))
                assert np.all(np.diff(energies) >= 0.0)

    def test_silicon_gamma_spectrum_matches_table2_control(self) -> None:
        """The Table 1 model reproduces the printed silicon Gamma energies."""
        model = Vogl1983LcaoSp3sStarModel.from_table(self.table(), "Si")

        energies = model.band_energies((0.0, 0.0, 0.0))

        np.testing.assert_allclose(
            energies,
            np.asarray(
                (
                    -12.50,
                    0.0,
                    0.0,
                    0.0,
                    3.43,
                    3.43,
                    3.43,
                    4.10,
                    6.685,
                    6.685,
                )
            ),
            rtol=0.0,
            atol=5.0e-14,
        )
        assert not energies.flags.writeable

    def test_band_energies_are_periodic_under_fcc_reciprocal_vector(self) -> None:
        """Bloch eigenvalues are periodic under one primitive reciprocal vector."""
        model = Vogl1983LcaoSp3sStarModel.from_table(self.table(), "Si")
        q = np.asarray((0.173, -0.281, 0.419))
        reciprocal_vector = np.asarray((1.0, 1.0, -1.0))

        np.testing.assert_allclose(
            model.band_energies(q),
            model.band_energies(q + reciprocal_vector),
            rtol=0.0,
            atol=1.0e-13,
        )

    @pytest.mark.parametrize(
        ("wavevector", "exception"),
        [
            ((0.0, 0.0), ValueError),
            ((0.0, 0.0, float("nan")), ValueError),
            ((True, False, True), TypeError),
            (("0", "0", "0"), TypeError),
            ((0.0 + 0.0j, 0.0, 0.0), TypeError),
        ],
    )
    def test_wavevector_validation_fails_closed(
        self,
        wavevector: tuple[float | bool | str | complex, ...],
        exception: type[Exception],
    ) -> None:
        """Invalid public wavevector values are rejected rather than coerced."""
        with pytest.raises(exception):
            Vogl1983LcaoSp3sStarModel.structure_factors(wavevector)
