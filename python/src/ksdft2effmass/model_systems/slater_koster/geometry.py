"""Exact right-handed diamond geometry and neighbor-shell maps."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

import numpy as np
from projectkoios.numerics.numpy.typing import Float64Array
from projectkoios.physkit.periodic import DirectLattice3D
from projectkoios.physkit.units import PhysicalUnit, ScalarQuantity

ANGSTROM = PhysicalUnit("angstrom")


class DiamondSublattice(IntEnum):
    """Ordered sites in the two-atom diamond primitive cell."""

    A = 0
    B = 1


@dataclass(frozen=True, slots=True)
class DiamondNeighborBond:
    """One directed neighbor relation in primitive-cell coordinates.

    ``target_cell`` identifies the target cell relative to the source cell. Site
    positions and Cartesian displacements are owned by
    :class:`DiamondSp3sStarGeometry`.
    """

    shell: int
    source: DiamondSublattice
    target: DiamondSublattice
    target_cell: tuple[int, int, int]

    def __post_init__(self) -> None:
        if type(self.shell) is not int:
            raise TypeError("shell must be an int")
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
            raise TypeError("target_cell must be a length-3 tuple of ints")
        if self.shell == 1:
            if self.source is self.target:
                raise ValueError("first-neighbor bonds must join opposite sublattices")
            allowed = (
                _FIRST_NEIGHBOR_CELLS
                if self.source is DiamondSublattice.A
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


@dataclass(frozen=True, slots=True)
class DiamondSp3sStarGeometry:
    r"""Right-handed homopolar diamond primitive-cell geometry.

    The conventional cubic lattice parameter ``a`` carries the exact PhysKit unit
    ``angstrom``. The normalized direct primitive vectors are matrix columns

    .. math::

       a_1/a=(1/2,0,1/2),\quad a_2/a=(1/2,1/2,0),\quad
       a_3/a=(0,1/2,1/2),

    and the two sites have primitive fractional coordinates ``(0,0,0)`` and
    ``(1/4,1/4,1/4)``. This ordered basis is right handed.
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
        """Return the PhysKit direct lattice normalized by ``a``."""
        return DirectLattice3D(
            np.asarray((0.5, 0.0, 0.5), dtype=np.float64),
            np.asarray((0.5, 0.5, 0.0), dtype=np.float64),
            np.asarray((0.0, 0.5, 0.5), dtype=np.float64),
        )

    @property
    def first_neighbor_bonds(self) -> tuple[DiamondNeighborBond, ...]:
        """Return the four unique directed A-to-B first-neighbor bonds.

        Reverse B-to-A bonds are their Hermitian conjugates and are not duplicated.
        """
        return tuple(
            DiamondNeighborBond(
                shell=1,
                source=DiamondSublattice.A,
                target=DiamondSublattice.B,
                target_cell=cell,
            )
            for cell in _FIRST_NEIGHBOR_CELLS
        )

    @property
    def second_neighbor_positive_bonds(self) -> tuple[DiamondNeighborBond, ...]:
        """Return six A-to-A representatives of the 12-vector second shell.

        The same displacement shell applies on sublattice B. Each omitted negative
        vector is generated as the Hermitian conjugate of its representative.
        """
        return tuple(
            DiamondNeighborBond(
                shell=2,
                source=DiamondSublattice.A,
                target=DiamondSublattice.A,
                target_cell=cell,
            )
            for cell in _SECOND_NEIGHBOR_POSITIVE_CELLS
        )

    @property
    def second_neighbor_bonds(self) -> tuple[DiamondNeighborBond, ...]:
        """Return the complete 12-vector A-to-A second-neighbor shell."""
        positive = self.second_neighbor_positive_bonds
        negative = tuple(
            DiamondNeighborBond(
                shell=2,
                source=DiamondSublattice.A,
                target=DiamondSublattice.A,
                target_cell=(
                    -bond.target_cell[0],
                    -bond.target_cell[1],
                    -bond.target_cell[2],
                ),
            )
            for bond in positive
        )
        return positive + negative

    def primitive_displacement(self, bond: DiamondNeighborBond) -> Float64Array:
        """Return ``target - source`` in primitive fractional coordinates."""
        if type(bond) is not DiamondNeighborBond:
            raise TypeError("bond must be DiamondNeighborBond")
        source = self._site_fractional(bond.source)
        target = self._site_fractional(bond.target)
        cell = np.asarray(bond.target_cell, dtype=np.float64)
        return self._immutable_array(cell + target - source)

    def normalized_cartesian_displacement(
        self,
        bond: DiamondNeighborBond,
    ) -> Float64Array:
        """Return ``(target - source) / a`` in conventional Cartesian axes."""
        fractional = self.primitive_displacement(bond)
        values = self.normalized_direct_lattice.primitive_basis_matrix @ fractional
        return self._immutable_array(values)

    def direction_cosines(self, bond: DiamondNeighborBond) -> Float64Array:
        """Return conventional-Cartesian direction cosines for one bond."""
        displacement = self.normalized_cartesian_displacement(bond)
        return self._immutable_array(displacement / np.linalg.norm(displacement))

    @staticmethod
    def _site_fractional(sublattice: DiamondSublattice) -> Float64Array:
        values = (
            (0.0, 0.0, 0.0) if sublattice is DiamondSublattice.A else (0.25, 0.25, 0.25)
        )
        return DiamondSp3sStarGeometry._immutable_array(
            np.asarray(values, dtype=np.float64)
        )

    @staticmethod
    def _immutable_array(values: Float64Array) -> Float64Array:
        array = np.asarray(values, dtype="<f8")
        return np.frombuffer(array.tobytes(), dtype="<f8").reshape(array.shape)
