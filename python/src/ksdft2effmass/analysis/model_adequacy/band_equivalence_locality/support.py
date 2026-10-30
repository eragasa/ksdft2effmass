"""Dense signed-permutation shell inventories for the 2-D and 3-D experiments."""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
    LatticeIntegerComponents,
)


def _closed_components(
    dimension: LatticeDimension, values: tuple[int, ...]
) -> LatticeIntegerComponents:
    if dimension is LatticeDimension.TWO:
        return (values[0], values[1])
    if dimension is LatticeDimension.THREE:
        return (values[0], values[1], values[2])
    raise ValueError("signed-permutation shells require dimension two or three")


def _squared_radius(displacement: LatticeDisplacement) -> int:
    return sum(value * value for value in displacement.components)


@dataclass(frozen=True, slots=True)
class SignedPermutationShellInventoryDefinition:
    """Define every attainable square or cubic shell through an integer cap.

    ``maximum_squared_radius`` is a dimensionless squared lattice-index radius. It is
    an exact built-in integer and may be zero. The definition intentionally supports
    only two and three dimensions; the maintained 1-D experiment uses integer range
    cutoffs instead of orbit shells.
    """

    dimension: LatticeDimension
    maximum_squared_radius: int

    def __post_init__(self) -> None:
        """Validate the closed dimension and nonnegative exact cap."""
        if type(self.dimension) is not LatticeDimension:
            raise TypeError("dimension must be LatticeDimension")
        if self.dimension not in (LatticeDimension.TWO, LatticeDimension.THREE):
            raise ValueError("dimension must be TWO or THREE")
        if type(self.maximum_squared_radius) is not int:
            raise TypeError("maximum_squared_radius must be a built-in int")
        if self.maximum_squared_radius < 0:
            raise ValueError("maximum_squared_radius must be nonnegative")


@dataclass(frozen=True, slots=True)
class SignedPermutationOrbit:
    """Retain one complete orbit and its canonical nonnegative representative."""

    representative: LatticeDisplacement
    members: tuple[LatticeDisplacement, ...]

    def __post_init__(self) -> None:
        """Require a canonical representative and unique ordered complete members."""
        if type(self.representative) is not LatticeDisplacement:
            raise TypeError("representative must be LatticeDisplacement")
        if type(self.members) is not tuple or not self.members:
            raise TypeError("members must be a nonempty tuple")
        if any(type(member) is not LatticeDisplacement for member in self.members):
            raise TypeError("members must contain LatticeDisplacement values")
        if any(
            member.dimension is not self.representative.dimension
            for member in self.members
        ):
            raise ValueError("orbit member dimensions must match the representative")
        components = self.representative.components
        if any(value < 0 for value in components):
            raise ValueError("representative components must be nonnegative")
        if tuple(sorted(components, reverse=True)) != components:
            raise ValueError("representative components must be descending")
        ordered = tuple(sorted(self.members, key=lambda item: item.components))
        if ordered != self.members or len(set(self.members)) != len(self.members):
            raise ValueError("orbit members must be unique and canonically ordered")
        if self.representative not in self.members:
            raise ValueError("orbit must contain its representative")
        radius = _squared_radius(self.representative)
        if any(_squared_radius(member) != radius for member in self.members):
            raise ValueError("all orbit members must have one squared radius")

    @property
    def squared_radius(self) -> int:
        """Return the exact dimensionless squared lattice-index radius."""
        return _squared_radius(self.representative)


@dataclass(frozen=True, slots=True)
class SignedPermutationShell:
    """Retain all complete orbits at one attainable squared radius."""

    squared_radius: int
    orbits: tuple[SignedPermutationOrbit, ...]
    cumulative_support: tuple[LatticeDisplacement, ...]

    def __post_init__(self) -> None:
        """Validate shell radius, orbit ordering, and conjugate-closed support."""
        if type(self.squared_radius) is not int or self.squared_radius < 0:
            raise ValueError("squared_radius must be a nonnegative built-in int")
        if type(self.orbits) is not tuple or not self.orbits:
            raise TypeError("orbits must be a nonempty tuple")
        if any(type(orbit) is not SignedPermutationOrbit for orbit in self.orbits):
            raise TypeError("orbits must contain SignedPermutationOrbit values")
        if any(orbit.squared_radius != self.squared_radius for orbit in self.orbits):
            raise ValueError("all orbits must match the shell squared radius")
        representatives = tuple(
            orbit.representative.components for orbit in self.orbits
        )
        if representatives != tuple(sorted(representatives, reverse=True)):
            raise ValueError("shell orbits must use canonical representative order")
        if type(self.cumulative_support) is not tuple:
            raise TypeError("cumulative_support must be a tuple")
        if len(set(self.cumulative_support)) != len(self.cumulative_support):
            raise ValueError("cumulative_support must contain unique displacements")
        support_set = set(self.cumulative_support)
        for displacement in self.cumulative_support:
            negative = LatticeDisplacement(
                displacement.dimension,
                _closed_components(
                    displacement.dimension,
                    tuple(-value for value in displacement.components),
                ),
            )
            if negative not in support_set:
                raise ValueError("cumulative_support must be conjugate closed")


@dataclass(frozen=True, slots=True)
class SignedPermutationShellInventory:
    """Retain every attainable shell through one declared squared-radius cap."""

    definition: SignedPermutationShellInventoryDefinition
    shells: tuple[SignedPermutationShell, ...]

    def __post_init__(self) -> None:
        """Require a dense attainable-shell sequence beginning with the onsite shell."""
        if type(self.definition) is not SignedPermutationShellInventoryDefinition:
            raise TypeError(
                "definition must be SignedPermutationShellInventoryDefinition"
            )
        if type(self.shells) is not tuple or not self.shells:
            raise TypeError("shells must be a nonempty tuple")
        if any(type(shell) is not SignedPermutationShell for shell in self.shells):
            raise TypeError("shells must contain SignedPermutationShell values")
        radii = tuple(shell.squared_radius for shell in self.shells)
        if radii[0] != 0 or radii != tuple(sorted(set(radii))):
            raise ValueError(
                "shell radii must be unique, increasing, and begin at zero"
            )
        if radii[-1] > self.definition.maximum_squared_radius:
            raise ValueError("shell radius exceeds the declared cap")
        previous: set[LatticeDisplacement] = set()
        for shell in self.shells:
            current = set(shell.cumulative_support)
            if not previous < current:
                raise ValueError("every shell must strictly extend cumulative support")
            if any(_squared_radius(item) > shell.squared_radius for item in current):
                raise ValueError("cumulative support exceeds its shell radius")
            previous = current


class SignedPermutationShellInventoryBuilder:
    """Construct dense square or cubic orbit shells from a bound definition."""

    __slots__ = ("_definition",)

    def __init__(
        self,
        *,
        definition: SignedPermutationShellInventoryDefinition,
    ) -> None:
        if type(definition) is not SignedPermutationShellInventoryDefinition:
            raise TypeError(
                "definition must be SignedPermutationShellInventoryDefinition"
            )
        self._definition = definition

    @property
    def definition(self) -> SignedPermutationShellInventoryDefinition:
        """Return the exact shell-inventory definition bound to this builder."""
        return self._definition

    def execute(self) -> SignedPermutationShellInventory:
        """Return every attainable shell in canonical order."""
        definition = self._definition
        representatives = self._representatives()
        by_radius: dict[int, list[SignedPermutationOrbit]] = {}
        for representative in representatives:
            orbit = self._orbit(representative)
            by_radius.setdefault(orbit.squared_radius, []).append(orbit)

        support: set[LatticeDisplacement] = set()
        shells: list[SignedPermutationShell] = []
        for squared_radius in sorted(by_radius):
            orbits = tuple(
                sorted(
                    by_radius[squared_radius],
                    key=lambda item: item.representative.components,
                    reverse=True,
                )
            )
            for orbit in orbits:
                support.update(orbit.members)
            cumulative = tuple(
                sorted(
                    support,
                    key=lambda item: (_squared_radius(item), item.components),
                )
            )
            shells.append(
                SignedPermutationShell(
                    squared_radius=squared_radius,
                    orbits=orbits,
                    cumulative_support=cumulative,
                )
            )
        return SignedPermutationShellInventory(definition, tuple(shells))

    def _representatives(self) -> tuple[LatticeDisplacement, ...]:
        definition = self._definition
        limit = math.isqrt(definition.maximum_squared_radius)
        values: list[LatticeDisplacement] = []
        if definition.dimension is LatticeDimension.TWO:
            for first in range(limit + 1):
                for second in range(first + 1):
                    components_2d = (first, second)
                    if sum(value * value for value in components_2d) <= (
                        definition.maximum_squared_radius
                    ):
                        values.append(
                            LatticeDisplacement(definition.dimension, components_2d)
                        )
        else:
            for first in range(limit + 1):
                for second in range(first + 1):
                    for third in range(second + 1):
                        components_3d = (first, second, third)
                        if sum(value * value for value in components_3d) <= (
                            definition.maximum_squared_radius
                        ):
                            values.append(
                                LatticeDisplacement(definition.dimension, components_3d)
                            )
        return tuple(
            sorted(values, key=lambda item: (_squared_radius(item), item.components))
        )

    def _orbit(self, representative: LatticeDisplacement) -> SignedPermutationOrbit:
        dimension = representative.dimension
        member_components: set[LatticeIntegerComponents] = set()
        for permutation in set(itertools.permutations(representative.components)):
            for signs in itertools.product((-1, 1), repeat=dimension.value):
                values = tuple(
                    sign * value for sign, value in zip(signs, permutation, strict=True)
                )
                member_components.add(_closed_components(dimension, values))
        members = tuple(
            sorted(
                (
                    LatticeDisplacement(dimension, components)
                    for components in member_components
                ),
                key=lambda item: item.components,
            )
        )
        return SignedPermutationOrbit(representative, members)
