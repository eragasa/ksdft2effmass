"""Concrete right-handed diamond geometry composed with PhysKit bond owners."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

import numpy as np
from projectkoios.numerics.numpy.typing import Float64Array
from projectkoios.physkit.periodic import DirectLattice3D
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)
from projectkoios.physkit.solidstate.tb.slater_koster import (
    HomopolarSp3sStarBondGeometry,
    HomopolarSp3sStarSpatialBasis,
    RealCubicOrbitalComponentEnum,
    SlaterKosterBasisCenter,
    SlaterKosterDirectedBond,
    SlaterKosterSpatialBasisCoordinate,
    SlaterKosterSpatialBasisDefinition,
)
from projectkoios.physkit.units import (
    PhysicalUnit,
    ScalarQuantity,
    UnitSystem,
    VectorQuantity,
)

ANGSTROM = PhysicalUnit("angstrom")

ORIGIN_CENTER_IDENTIFIER = "diamond_origin_center"
QUARTER_CENTER_IDENTIFIER = "diamond_body_diagonal_quarter_center"


class DiamondSublattice(IntEnum):
    """Ordered centers in the two-atom diamond primitive cell."""

    ORIGIN = 0
    BODY_DIAGONAL_QUARTER = 1

    @property
    def center_identifier(self) -> str:
        """Return the descriptive identifier used by structured basis and bonds."""
        if self is DiamondSublattice.ORIGIN:
            return ORIGIN_CENTER_IDENTIFIER
        return QUARTER_CENTER_IDENTIFIER


_FIRST_NEIGHBOR_CELLS = (
    (0, 0, 0),
    (-1, 0, 0),
    (0, -1, 0),
    (0, 0, -1),
)
_SECOND_NEIGHBOR_POSITIVE_CELLS = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, -1, 0),
    (1, 0, -1),
    (0, 1, -1),
)


@dataclass(frozen=True, slots=True, kw_only=True)
class DiamondNeighborBond:
    """One concrete directed diamond-neighbor relation in primitive coordinates."""

    shell: int
    source: DiamondSublattice
    target: DiamondSublattice
    target_cell: tuple[int, int, int]

    def __post_init__(self) -> None:
        if type(self.shell) is not int:
            raise TypeError("shell must be a built-in int")
        if self.shell not in (1, 2):
            raise ValueError("shell must be 1 or 2")
        if type(self.source) is not DiamondSublattice:
            raise TypeError("source must be DiamondSublattice")
        if type(self.target) is not DiamondSublattice:
            raise TypeError("target must be DiamondSublattice")
        if (
            type(self.target_cell) is not tuple
            or len(self.target_cell) != 3
            or any(type(component) is not int for component in self.target_cell)
        ):
            raise TypeError("target_cell must be a length-3 tuple of built-in ints")

        if self.shell == 1:
            if self.source is self.target:
                raise ValueError("first-neighbor bonds must join opposite sublattices")
            allowed = (
                _FIRST_NEIGHBOR_CELLS
                if self.source is DiamondSublattice.ORIGIN
                else tuple(
                    (-cell[0], -cell[1], -cell[2]) for cell in _FIRST_NEIGHBOR_CELLS
                )
            )
        else:
            if self.source is not self.target:
                raise ValueError("second-neighbor bonds must stay on one sublattice")
            positive = _SECOND_NEIGHBOR_POSITIVE_CELLS
            allowed = positive + tuple(
                (-cell[0], -cell[1], -cell[2]) for cell in positive
            )
        if self.target_cell not in allowed:
            raise ValueError("target_cell does not belong to the declared shell")

    @property
    def directed_bond(self) -> SlaterKosterDirectedBond:
        """Return the PhysKit ordinary-cell bond with descriptive center identifiers."""
        return SlaterKosterDirectedBond(
            ordinary_cell_displacement=LatticeDisplacement(
                dimension=LatticeDimension.THREE,
                components=self.target_cell,
            ),
            source_center_identifier=self.source.center_identifier,
            target_center_identifier=self.target.center_identifier,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class DiamondSp3sStarGeometry:
    r"""Right-handed two-center diamond geometry in metal-style units.

    The conventional cubic lattice parameter uses angstrom. The primitive direct
    vectors, expressed as columns after division by the lattice parameter, are

    .. math::

       a_1/a=(1/2,0,1/2),\quad a_2/a=(1/2,1/2,0),\quad
       a_3/a=(0,1/2,1/2).

    The ordered centers are the primitive origin and body-diagonal quarter point.
    Reusable spatial-basis, directed-bond, and direction mechanics are delegated to
    Project Koios PhysKit.
    """

    lattice_parameter: ScalarQuantity

    def __post_init__(self) -> None:
        if type(self.lattice_parameter) is not ScalarQuantity:
            raise TypeError("lattice_parameter must be ScalarQuantity")
        if self.lattice_parameter.unit != ANGSTROM:
            raise ValueError("lattice_parameter must be in angstrom")
        if self.lattice_parameter.magnitude <= 0.0:
            raise ValueError("lattice_parameter must be positive")

    @property
    def normalized_direct_lattice(self) -> DirectLattice3D:
        """Return the PhysKit direct lattice normalized by the lattice parameter."""
        return DirectLattice3D(
            np.asarray((0.5, 0.0, 0.5), dtype=np.float64),
            np.asarray((0.5, 0.5, 0.0), dtype=np.float64),
            np.asarray((0.0, 0.5, 0.5), dtype=np.float64),
        )

    @property
    def spatial_basis(self) -> HomopolarSp3sStarSpatialBasis:
        """Return the exact PhysKit spatial basis for the two diamond centers."""
        unit = UnitSystem.NONDIMENSIONAL.length_unit
        centers = tuple(
            SlaterKosterBasisCenter(
                identifier=sublattice.center_identifier,
                fractional_coordinate=VectorQuantity(
                    magnitude=self._site_fractional(sublattice),
                    unit=unit,
                ),
            )
            for sublattice in DiamondSublattice
        )
        components = (
            (RealCubicOrbitalComponentEnum.s, 0),
            (RealCubicOrbitalComponentEnum.p_x, 0),
            (RealCubicOrbitalComponentEnum.p_y, 0),
            (RealCubicOrbitalComponentEnum.p_z, 0),
            (RealCubicOrbitalComponentEnum.s, 1),
        )
        definition = SlaterKosterSpatialBasisDefinition(
            display_identifier="diamond-spinless-sp3s-star",
            centers=centers,
            coordinates=tuple(
                SlaterKosterSpatialBasisCoordinate(
                    center_identifier=center.identifier,
                    orbital_component=component,
                    radial_channel=radial_channel,
                )
                for center in centers
                for component, radial_channel in components
            ),
        )
        return HomopolarSp3sStarSpatialBasis(definition=definition)

    @property
    def first_neighbor_bonds(self) -> tuple[DiamondNeighborBond, ...]:
        """Return four unique origin-to-quarter first-neighbor representatives."""
        return tuple(
            DiamondNeighborBond(
                shell=1,
                source=DiamondSublattice.ORIGIN,
                target=DiamondSublattice.BODY_DIAGONAL_QUARTER,
                target_cell=cell,
            )
            for cell in _FIRST_NEIGHBOR_CELLS
        )

    @property
    def second_neighbor_positive_bonds(self) -> tuple[DiamondNeighborBond, ...]:
        """Return six positive representatives on the origin fcc sublattice."""
        return tuple(
            DiamondNeighborBond(
                shell=2,
                source=DiamondSublattice.ORIGIN,
                target=DiamondSublattice.ORIGIN,
                target_cell=cell,
            )
            for cell in _SECOND_NEIGHBOR_POSITIVE_CELLS
        )

    @property
    def second_neighbor_positive_bonds_by_sublattice(
        self,
    ) -> tuple[DiamondNeighborBond, ...]:
        """Return six positive representatives for each of the two fcc sublattices."""
        return tuple(
            DiamondNeighborBond(
                shell=2,
                source=sublattice,
                target=sublattice,
                target_cell=cell,
            )
            for sublattice in DiamondSublattice
            for cell in _SECOND_NEIGHBOR_POSITIVE_CELLS
        )

    @property
    def second_neighbor_bonds(self) -> tuple[DiamondNeighborBond, ...]:
        """Return the complete 12-vector shell on the origin fcc sublattice."""
        positive = self.second_neighbor_positive_bonds
        negative = tuple(
            DiamondNeighborBond(
                shell=2,
                source=DiamondSublattice.ORIGIN,
                target=DiamondSublattice.ORIGIN,
                target_cell=(
                    -bond.target_cell[0],
                    -bond.target_cell[1],
                    -bond.target_cell[2],
                ),
            )
            for bond in positive
        )
        return positive + negative

    def primitive_displacement(self, *, bond: DiamondNeighborBond) -> Float64Array:
        """Return target minus source in primitive fractional coordinates."""
        if type(bond) is not DiamondNeighborBond:
            raise TypeError("bond must be DiamondNeighborBond")
        source = self._site_fractional(bond.source)
        target = self._site_fractional(bond.target)
        cell = np.asarray(bond.target_cell, dtype=np.float64)
        return self._immutable_array(cell + target - source)

    def normalized_cartesian_displacement(
        self,
        *,
        bond: DiamondNeighborBond,
    ) -> Float64Array:
        """Return target minus source divided by the conventional lattice parameter."""
        fractional = self.primitive_displacement(bond=bond)
        values = self.normalized_direct_lattice.primitive_basis_matrix @ fractional
        return self._immutable_array(values)

    def bond_geometry(
        self,
        *,
        bond: DiamondNeighborBond,
    ) -> HomopolarSp3sStarBondGeometry:
        """Return the PhysKit bond geometry in angstrom without shell inference."""
        normalized = self.normalized_cartesian_displacement(bond=bond)
        return HomopolarSp3sStarBondGeometry(
            directed_bond=bond.directed_bond,
            cartesian_displacement=VectorQuantity(
                magnitude=normalized * self.lattice_parameter.magnitude,
                unit=UnitSystem.METAL.length_unit,
            ),
            unit_system=UnitSystem.METAL,
        )

    def direction_cosines(self, *, bond: DiamondNeighborBond) -> Float64Array:
        """Return PhysKit-owned Cartesian direction cosines for one bond."""
        return self.bond_geometry(bond=bond).bond_direction.components.magnitude

    @staticmethod
    def _site_fractional(sublattice: DiamondSublattice) -> Float64Array:
        values = (
            (0.0, 0.0, 0.0)
            if sublattice is DiamondSublattice.ORIGIN
            else (0.25, 0.25, 0.25)
        )
        return DiamondSp3sStarGeometry._immutable_array(
            np.asarray(values, dtype=np.float64)
        )

    @staticmethod
    def _immutable_array(values: Float64Array) -> Float64Array:
        array = np.asarray(values, dtype="<f8")
        return np.frombuffer(array.tobytes(), dtype="<f8").reshape(array.shape)
