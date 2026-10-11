"""Canonical signed-axis lattice-displacement orbits and integer shells.

This target-relative PhysKit candidate composes the existing finite-domain and integral-
symmetry primitives.  It does not select a campaign shell sequence, fit coefficients,
or define scientific acceptance thresholds.
"""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.physkit.core.results import ResultsObject
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)
from projectkoios.physkit.periodic.lattice.symmetry import (
    IntegralLatticeOperation,
    LatticeDisplacementTransformer,
)


class SquareLatticeD4OperationSetConstructor:
    """Construct the exact eight signed-axis operations of square-lattice ``D4``."""

    __slots__ = ()

    def execute(self) -> tuple[IntegralLatticeOperation, ...]:
        """Return identity, rotations, and reflections in one stable order."""
        dimension = LatticeDimension.TWO
        return (
            IntegralLatticeOperation("d4.identity", dimension, ((1, 0), (0, 1))),
            IntegralLatticeOperation("d4.rotate-90", dimension, ((0, -1), (1, 0))),
            IntegralLatticeOperation("d4.rotate-180", dimension, ((-1, 0), (0, -1))),
            IntegralLatticeOperation("d4.rotate-270", dimension, ((0, 1), (-1, 0))),
            IntegralLatticeOperation("d4.reflect-x", dimension, ((1, 0), (0, -1))),
            IntegralLatticeOperation("d4.reflect-y", dimension, ((-1, 0), (0, 1))),
            IntegralLatticeOperation(
                "d4.reflect-diagonal", dimension, ((0, 1), (1, 0))
            ),
            IntegralLatticeOperation(
                "d4.reflect-antidiagonal", dimension, ((0, -1), (-1, 0))
            ),
        )


@dataclass(frozen=True, slots=True)
class LatticeDisplacementOrbit(ResultsObject):
    """One canonical orbit under a supplied signed-axis operation set."""

    representative: LatticeDisplacement
    members: tuple[LatticeDisplacement, ...]

    def __post_init__(self) -> None:
        """Require canonical ordering, unique members, and one squared radius."""
        if type(self.representative) is not LatticeDisplacement:
            raise TypeError("representative must be LatticeDisplacement")
        if type(self.members) is not tuple or any(
            type(member) is not LatticeDisplacement for member in self.members
        ):
            raise TypeError("members must be a tuple of LatticeDisplacement")
        if not self.members:
            raise ValueError("members must be nonempty")
        if any(
            member.dimension is not self.representative.dimension
            for member in self.members
        ):
            raise ValueError("orbit member dimensions must agree")
        components = tuple(member.components for member in self.members)
        if components != tuple(sorted(set(components))):
            raise ValueError("orbit members must be canonically sorted and unique")
        if self.representative != self.members[0]:
            raise ValueError("representative must be the first canonical member")
        if any(
            _squared_radius(member) != self.squared_radius for member in self.members
        ):
            raise ValueError("signed-axis orbit members must share a squared radius")

    @property
    def multiplicity(self) -> int:
        """Return the exact number of represented displacements in the orbit."""
        return len(self.members)

    @property
    def squared_radius(self) -> int:
        """Return the exact integer index-space squared radius."""
        return _squared_radius(self.representative)


@dataclass(frozen=True, slots=True)
class LatticeDisplacementOrbitPartition(ResultsObject):
    """Retain one complete canonical partition of a finite displacement inventory."""

    displacements: tuple[LatticeDisplacement, ...]
    operations: tuple[IntegralLatticeOperation, ...]
    orbits: tuple[LatticeDisplacementOrbit, ...]

    def __post_init__(self) -> None:
        """Reconstruct coverage, invariance, dimensions, and deterministic ordering."""
        if type(self.displacements) is not tuple or any(
            type(value) is not LatticeDisplacement for value in self.displacements
        ):
            raise TypeError("displacements must be a tuple of LatticeDisplacement")
        if not self.displacements:
            raise ValueError("displacements must be nonempty")
        dimension = self.displacements[0].dimension
        if any(value.dimension is not dimension for value in self.displacements):
            raise ValueError("displacement dimensions must agree")
        displacement_components = tuple(
            value.components for value in self.displacements
        )
        if displacement_components != tuple(sorted(set(displacement_components))):
            raise ValueError("displacements must be canonically sorted and unique")

        if type(self.operations) is not tuple or any(
            type(value) is not IntegralLatticeOperation for value in self.operations
        ):
            raise TypeError("operations must be a tuple of IntegralLatticeOperation")
        if not self.operations:
            raise ValueError("operations must be nonempty")
        if any(value.dimension is not dimension for value in self.operations):
            raise ValueError("operation and displacement dimensions must agree")
        if any(not value.is_signed_axis_permutation for value in self.operations):
            raise ValueError("operations must be signed axis permutations")
        identifiers = tuple(value.identifier for value in self.operations)
        matrices = tuple(value.matrix for value in self.operations)
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("operation identifiers must be unique")
        if len(matrices) != len(set(matrices)):
            raise ValueError("operation matrices must be unique")

        if type(self.orbits) is not tuple or any(
            type(value) is not LatticeDisplacementOrbit for value in self.orbits
        ):
            raise TypeError("orbits must be a tuple of LatticeDisplacementOrbit")
        if not self.orbits:
            raise ValueError("orbits must be nonempty")
        orbit_keys = tuple(
            (orbit.squared_radius, orbit.representative.components)
            for orbit in self.orbits
        )
        if orbit_keys != tuple(sorted(orbit_keys)):
            raise ValueError("orbits must be ordered by radius and representative")
        flattened = tuple(member for orbit in self.orbits for member in orbit.members)
        if len(flattened) != len(set(flattened)):
            raise ValueError("orbits must be disjoint")
        if set(flattened) != set(self.displacements):
            raise ValueError("orbits must exactly cover the displacement inventory")

        transformer = LatticeDisplacementTransformer()
        for orbit in self.orbits:
            members = set(orbit.members)
            for member in orbit.members:
                transformed = {
                    transformer.execute(operation, member)
                    for operation in self.operations
                }
                if transformed != members:
                    raise ValueError(
                        "every orbit must be invariant under the complete operation set"
                    )

    @property
    def multiplicity(self) -> int:
        """Return the total number of represented displacements."""
        return sum(orbit.multiplicity for orbit in self.orbits)


class LatticeDisplacementOrbitPartitioner:
    """Partition a closed finite inventory under signed-axis operations."""

    __slots__ = ()

    def execute(
        self,
        displacements: tuple[LatticeDisplacement, ...],
        operations: tuple[IntegralLatticeOperation, ...],
    ) -> LatticeDisplacementOrbitPartition:
        """Return the deterministic orbit partition or fail on nonclosure."""
        if type(displacements) is not tuple or any(
            type(value) is not LatticeDisplacement for value in displacements
        ):
            raise TypeError("displacements must be a tuple of LatticeDisplacement")
        if not displacements:
            raise ValueError("displacements must be nonempty")
        if type(operations) is not tuple or any(
            type(value) is not IntegralLatticeOperation for value in operations
        ):
            raise TypeError("operations must be a tuple of IntegralLatticeOperation")
        if not operations:
            raise ValueError("operations must be nonempty")
        dimension = displacements[0].dimension
        if any(value.dimension is not dimension for value in displacements):
            raise ValueError("displacement dimensions must agree")
        if any(value.dimension is not dimension for value in operations):
            raise ValueError("operation and displacement dimensions must agree")
        if any(not value.is_signed_axis_permutation for value in operations):
            raise ValueError("operations must be signed axis permutations")

        ordered = tuple(sorted(displacements, key=lambda value: value.components))
        if len(ordered) != len(set(ordered)):
            raise ValueError("displacements must be unique")
        inventory = set(ordered)
        transformer = LatticeDisplacementTransformer()
        remaining = set(ordered)
        orbits: list[LatticeDisplacementOrbit] = []
        while remaining:
            seed = min(remaining, key=lambda value: value.components)
            members = {transformer.execute(operation, seed) for operation in operations}
            if seed not in members:
                raise ValueError("operation set must contain the orbit seed")
            if not members <= inventory:
                raise ValueError("displacement inventory is not operation-closed")
            stable = {
                transformer.execute(operation, member)
                for member in members
                for operation in operations
            }
            if stable != members:
                raise ValueError("operation set does not generate stable orbits")
            orbit_members = tuple(sorted(members, key=lambda value: value.components))
            orbits.append(LatticeDisplacementOrbit(orbit_members[0], orbit_members))
            remaining -= members
        ordered_orbits = tuple(
            sorted(
                orbits,
                key=lambda orbit: (
                    orbit.squared_radius,
                    orbit.representative.components,
                ),
            )
        )
        return LatticeDisplacementOrbitPartition(
            ordered,
            operations,
            ordered_orbits,
        )


@dataclass(frozen=True, slots=True)
class LatticeDisplacementShell(ResultsObject):
    """One exact integer squared-radius shell containing complete orbits."""

    squared_radius: int
    orbits: tuple[LatticeDisplacementOrbit, ...]

    def __post_init__(self) -> None:
        if type(self.squared_radius) is not int:
            raise TypeError("squared_radius must be a built-in integer")
        if self.squared_radius < 0:
            raise ValueError("squared_radius must be nonnegative")
        if type(self.orbits) is not tuple or any(
            type(orbit) is not LatticeDisplacementOrbit for orbit in self.orbits
        ):
            raise TypeError("orbits must be a tuple of LatticeDisplacementOrbit")
        if not self.orbits:
            raise ValueError("orbits must be nonempty")
        if any(orbit.squared_radius != self.squared_radius for orbit in self.orbits):
            raise ValueError("shell orbits must share the declared squared radius")
        representatives = tuple(
            orbit.representative.components for orbit in self.orbits
        )
        if representatives != tuple(sorted(set(representatives))):
            raise ValueError("shell orbits must be canonically ordered and unique")

    @property
    def multiplicity(self) -> int:
        """Return the represented block count in this exact shell."""
        return sum(orbit.multiplicity for orbit in self.orbits)


@dataclass(frozen=True, slots=True)
class LatticeDisplacementShellInventory(ResultsObject):
    """Correlate one orbit partition with all exact squared-radius shells."""

    partition: LatticeDisplacementOrbitPartition
    shells: tuple[LatticeDisplacementShell, ...]

    def __post_init__(self) -> None:
        if type(self.partition) is not LatticeDisplacementOrbitPartition:
            raise TypeError("partition must be LatticeDisplacementOrbitPartition")
        if type(self.shells) is not tuple or any(
            type(shell) is not LatticeDisplacementShell for shell in self.shells
        ):
            raise TypeError("shells must be a tuple of LatticeDisplacementShell")
        if not self.shells:
            raise ValueError("shells must be nonempty")
        radii = tuple(shell.squared_radius for shell in self.shells)
        if radii != tuple(sorted(set(radii))):
            raise ValueError("shell radii must be strictly increasing")
        flattened = tuple(orbit for shell in self.shells for orbit in shell.orbits)
        if flattened != self.partition.orbits:
            raise ValueError("shells must preserve and exactly cover partition orbits")

    def orbits_through(
        self, maximum_squared_radius: int, /
    ) -> tuple[LatticeDisplacementOrbit, ...]:
        """Return all complete orbits through an inclusive integer radius."""
        if type(maximum_squared_radius) is not int:
            raise TypeError("maximum_squared_radius must be a built-in integer")
        if maximum_squared_radius < 0:
            raise ValueError("maximum_squared_radius must be nonnegative")
        return tuple(
            orbit
            for shell in self.shells
            if shell.squared_radius <= maximum_squared_radius
            for orbit in shell.orbits
        )


class LatticeDisplacementShellInventoryConstructor:
    """Group a canonical orbit partition into exact integer-radius shells."""

    __slots__ = ()

    def execute(
        self, partition: LatticeDisplacementOrbitPartition
    ) -> LatticeDisplacementShellInventory:
        if type(partition) is not LatticeDisplacementOrbitPartition:
            raise TypeError("partition must be LatticeDisplacementOrbitPartition")
        radii = tuple(sorted({orbit.squared_radius for orbit in partition.orbits}))
        shells = tuple(
            LatticeDisplacementShell(
                radius,
                tuple(
                    orbit
                    for orbit in partition.orbits
                    if orbit.squared_radius == radius
                ),
            )
            for radius in radii
        )
        return LatticeDisplacementShellInventory(partition, shells)


def _squared_radius(displacement: LatticeDisplacement) -> int:
    return sum(value * value for value in displacement.components)


__all__ = [
    "LatticeDisplacementOrbit",
    "LatticeDisplacementOrbitPartition",
    "LatticeDisplacementOrbitPartitioner",
    "LatticeDisplacementShell",
    "LatticeDisplacementShellInventory",
    "LatticeDisplacementShellInventoryConstructor",
    "SquareLatticeD4OperationSetConstructor",
]
