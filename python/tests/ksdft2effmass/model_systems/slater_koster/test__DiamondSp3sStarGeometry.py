"""Software verification for right-handed diamond neighbor geometry."""

from __future__ import annotations

import math

import numpy as np
import pytest
from projectkoios.physkit.periodic import DirectLattice3D
from projectkoios.physkit.units import PhysicalUnit, ScalarQuantity

from ksdft2effmass.model_systems.slater_koster import (
    DiamondNeighborBond,
    DiamondSp3sStarGeometry,
    DiamondSublattice,
)

pytestmark = pytest.mark.software_verification


class TestDiamondSp3sStarGeometry:
    """Own primitive-basis handedness and complete-shell geometry checks."""

    def test_normalized_direct_lattice__declared_basis__is_right_handed(self) -> None:
        geometry = self._geometry()

        lattice = geometry.normalized_direct_lattice

        assert isinstance(lattice, DirectLattice3D)
        assert lattice.is_right_handed
        np.testing.assert_array_equal(
            lattice.primitive_basis_matrix,
            np.asarray(
                (
                    (0.5, 0.5, 0.0),
                    (0.0, 0.5, 0.5),
                    (0.5, 0.0, 0.5),
                )
            ),
        )

    def test_first_neighbor_bonds__four_tetrahedral_vectors__are_complete(self) -> None:
        geometry = self._geometry()

        displacements = np.asarray(
            [
                geometry.normalized_cartesian_displacement(bond)
                for bond in geometry.first_neighbor_bonds
            ]
        )

        assert len(geometry.first_neighbor_bonds) == 4
        np.testing.assert_allclose(
            np.linalg.norm(displacements, axis=1),
            math.sqrt(3.0) / 4.0,
            rtol=0.0,
            atol=1.0e-15,
        )
        np.testing.assert_allclose(
            displacements.sum(axis=0),
            np.zeros(3),
            rtol=0.0,
            atol=0.0,
        )
        np.testing.assert_allclose(
            displacements @ displacements.T,
            np.full((4, 4), -1.0 / 16.0) + np.eye(4) / 4.0,
            rtol=0.0,
            atol=0.0,
        )

    def test_second_neighbor_bonds__twelve_fcc_vectors__are_pair_closed(self) -> None:
        geometry = self._geometry()

        displacements = {
            tuple(geometry.normalized_cartesian_displacement(bond))
            for bond in geometry.second_neighbor_bonds
        }

        assert len(displacements) == 12
        assert all(
            tuple(-value for value in vector) in displacements
            for vector in displacements
        )
        assert all(
            math.isclose(
                float(np.linalg.norm(vector)),
                math.sqrt(0.5),
                rel_tol=0.0,
                abs_tol=1.0e-15,
            )
            for vector in displacements
        )

    def test_neighbor_bond__wrong_sublattice_or_cell_for_shell__rejects(self) -> None:
        with pytest.raises(ValueError, match="opposite sublattices"):
            DiamondNeighborBond(
                shell=1,
                source=DiamondSublattice.A,
                target=DiamondSublattice.A,
                target_cell=(0, 0, 0),
            )
        with pytest.raises(ValueError, match="declared shell"):
            DiamondNeighborBond(
                shell=2,
                source=DiamondSublattice.B,
                target=DiamondSublattice.B,
                target_cell=(0, 0, 0),
            )

    def test_lattice_parameter__wrong_unit_or_nonpositive__rejects(self) -> None:
        with pytest.raises(ValueError, match="angstrom"):
            DiamondSp3sStarGeometry(ScalarQuantity(5.4, PhysicalUnit("bohr")))
        with pytest.raises(ValueError, match="positive"):
            DiamondSp3sStarGeometry(ScalarQuantity(0.0, PhysicalUnit("angstrom")))

    @staticmethod
    def _geometry() -> DiamondSp3sStarGeometry:
        return DiamondSp3sStarGeometry(ScalarQuantity(5.4, PhysicalUnit("angstrom")))
