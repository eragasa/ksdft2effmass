"""Software verification for signed-axis displacement orbits and shells."""

from __future__ import annotations

import pytest

from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)
from projectkoios.physkit.periodic.lattice.symmetry import (
    LatticeDisplacementTransformer,
)
from projectkoios.physkit.periodic.lattice.symmetry_orbits import (
    LatticeDisplacementOrbitPartition,
    LatticeDisplacementOrbitPartitioner,
    LatticeDisplacementShell,
    LatticeDisplacementShellInventoryConstructor,
    SquareLatticeD4OperationSetConstructor,
)


class TestLatticeDisplacementOrbitPartition:
    """Verify the exact HSH-sized combinatorics and fail-closed correlation."""

    @staticmethod
    def centered(side: int) -> tuple[LatticeDisplacement, ...]:
        half = side // 2
        return tuple(
            LatticeDisplacement(LatticeDimension.TWO, (first, second))
            for first in range(-half, half + 1)
            for second in range(-half, half + 1)
        )

    def test_d4_constructor_returns_the_exact_square_operation_set(self) -> None:
        operations = SquareLatticeD4OperationSetConstructor().execute()
        transformer = LatticeDisplacementTransformer()
        seed = LatticeDisplacement(LatticeDimension.TWO, (2, 1))

        images = {
            transformer.execute(operation, seed).components for operation in operations
        }

        assert tuple(
            (operation.identifier, operation.matrix) for operation in operations
        ) == (
            ("d4.identity", ((1, 0), (0, 1))),
            ("d4.rotate-90", ((0, -1), (1, 0))),
            ("d4.rotate-180", ((-1, 0), (0, -1))),
            ("d4.rotate-270", ((0, 1), (-1, 0))),
            ("d4.reflect-x", ((1, 0), (0, -1))),
            ("d4.reflect-y", ((-1, 0), (0, 1))),
            ("d4.reflect-diagonal", ((0, 1), (1, 0))),
            ("d4.reflect-antidiagonal", ((0, -1), (-1, 0))),
        )
        assert images == {
            (2, 1),
            (-1, 2),
            (-2, -1),
            (1, -2),
            (2, -1),
            (-2, 1),
            (1, 2),
            (-1, -2),
        }

    def test_partition_and_shells_reproduce_the_centered_15_by_15_inventory(
        self,
    ) -> None:
        partition = LatticeDisplacementOrbitPartitioner().execute(
            self.centered(15),
            SquareLatticeD4OperationSetConstructor().execute(),
        )
        shells = LatticeDisplacementShellInventoryConstructor().execute(partition)
        radii = (0, 1, 2, 4, 8, 18, 50, 98)

        assert len(partition.orbits) == 36
        assert partition.multiplicity == 225
        assert tuple(len(shells.orbits_through(radius)) for radius in radii) == (
            1,
            2,
            3,
            4,
            6,
            12,
            27,
            36,
        )
        assert tuple(
            sum(orbit.multiplicity for orbit in shells.orbits_through(radius))
            for radius in radii
        ) == (1, 5, 9, 13, 25, 61, 161, 225)
        assert shells.shells[-1].squared_radius == 98

    def test_partitioner_rejects_an_inventory_that_is_not_d4_closed(self) -> None:
        inventory = tuple(
            value for value in self.centered(3) if value.components != (-1, -1)
        )

        with pytest.raises(ValueError, match="not operation-closed"):
            LatticeDisplacementOrbitPartitioner().execute(
                inventory,
                SquareLatticeD4OperationSetConstructor().execute(),
            )

    def test_partition_record_rejects_missing_orbit_coverage(self) -> None:
        partition = LatticeDisplacementOrbitPartitioner().execute(
            self.centered(3),
            SquareLatticeD4OperationSetConstructor().execute(),
        )

        with pytest.raises(ValueError, match="exactly cover"):
            LatticeDisplacementOrbitPartition(
                partition.displacements,
                partition.operations,
                partition.orbits[:-1],
            )
        with pytest.raises(ValueError, match="ordered by radius"):
            LatticeDisplacementOrbitPartition(
                partition.displacements,
                partition.operations,
                tuple(reversed(partition.orbits)),
            )

    def test_shell_record_rejects_duplicate_orbits(self) -> None:
        partition = LatticeDisplacementOrbitPartitioner().execute(
            self.centered(3),
            SquareLatticeD4OperationSetConstructor().execute(),
        )
        orbit = partition.orbits[0]

        with pytest.raises(ValueError, match="unique"):
            LatticeDisplacementShell(orbit.squared_radius, (orbit, orbit))

    def test_shell_selection_rejects_boolean_and_negative_radii(self) -> None:
        partition = LatticeDisplacementOrbitPartitioner().execute(
            self.centered(3),
            SquareLatticeD4OperationSetConstructor().execute(),
        )
        shells = LatticeDisplacementShellInventoryConstructor().execute(partition)

        with pytest.raises(TypeError):
            shells.orbits_through(True)  # type: ignore[arg-type]
        with pytest.raises(ValueError):
            shells.orbits_through(-1)
