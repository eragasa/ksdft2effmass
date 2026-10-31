"""Immutable admitted real-space support policies."""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
    LatticeIntegerComponents,
)

from .base import RealSpaceSupportTruncation


@dataclass(frozen=True, slots=True)
class ConjugateClosedSupport(RealSpaceSupportTruncation):
    """Retain one explicit, ordered, conjugate-closed displacement group."""

    displacements: tuple[LatticeDisplacement, ...]

    def __post_init__(self) -> None:
        if type(self.displacements) is not tuple or not self.displacements:
            raise TypeError("displacements must be a nonempty tuple")
        if any(
            type(displacement) is not LatticeDisplacement
            for displacement in self.displacements
        ):
            raise TypeError(
                "displacements must contain exact LatticeDisplacement values"
            )
        dimension = self.displacements[0].dimension
        if any(
            displacement.dimension is not dimension
            for displacement in self.displacements
        ):
            raise ValueError("displacements must have one common lattice dimension")
        components = tuple(
            displacement.components for displacement in self.displacements
        )
        if components != tuple(sorted(set(components))):
            raise ValueError(
                "displacements must be lexicographically sorted and unique"
            )
        if not any(displacement.is_zero for displacement in self.displacements):
            raise ValueError("support must retain the zero displacement")
        component_set = set(components)
        for value in components:
            if len(value) == 1:
                conjugate: LatticeIntegerComponents = (-value[0],)
            elif len(value) == 2:
                conjugate = (-value[0], -value[1])
            else:
                conjugate = (-value[0], -value[1], -value[2])
            if conjugate not in component_set:
                raise ValueError(
                    "support must be closed under displacement conjugation"
                )

    @property
    def dimension(self) -> LatticeDimension:
        """Return the common lattice dimension."""
        return self.displacements[0].dimension

    @property
    def retained_displacement_count(self) -> int:
        """Return the number of explicitly retained displacements."""
        return len(self.displacements)


@dataclass(frozen=True, slots=True)
class SymmetricRangeSupport1D(RealSpaceSupportTruncation):
    """Admit every one-dimensional integer displacement from ``-R`` through ``R``."""

    maximum_range: int

    def __post_init__(self) -> None:
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in integer")
        if self.maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")

    @property
    def support(self) -> ConjugateClosedSupport:
        """Return the explicit conjugate-closed displacement inventory."""
        return ConjugateClosedSupport(
            tuple(
                LatticeDisplacement(LatticeDimension.ONE, (translation,))
                for translation in range(-self.maximum_range, self.maximum_range + 1)
            )
        )


@dataclass(frozen=True, slots=True)
class MetricShellSupportInventory(RealSpaceSupportTruncation):
    """Bind PhysKit displacements to contiguous ordinal metric-shell indices.

    The ordinal indices are admitted inputs, not recomputed here. The producer must
    obtain the shell partition from PhysKit-owned lattice geometry. This record verifies
    displacement ordering, contiguous ordinal indices, zero-shell identity, and
    conjugate-pair consistency before a cutoff is selected. Physical scaled-metric
    values remain a separate classification channel because they need not be
    contiguous.
    """

    displacements: tuple[LatticeDisplacement, ...]
    ordinal_shell_indices: tuple[int, ...]

    def __post_init__(self) -> None:
        support = ConjugateClosedSupport(self.displacements)
        if support.dimension not in (LatticeDimension.TWO, LatticeDimension.THREE):
            raise ValueError("metric-shell inventories require dimension two or three")
        if type(self.ordinal_shell_indices) is not tuple:
            raise TypeError("ordinal_shell_indices must be a tuple")
        if len(self.ordinal_shell_indices) != len(self.displacements):
            raise ValueError("ordinal_shell_indices must align with displacements")
        if any(type(value) is not int for value in self.ordinal_shell_indices):
            raise TypeError("ordinal_shell_indices must contain built-in integers")
        if any(value < 0 for value in self.ordinal_shell_indices):
            raise ValueError("ordinal_shell_indices must be nonnegative")
        admitted = set(self.ordinal_shell_indices)
        if admitted != set(range(max(admitted) + 1)):
            raise ValueError(
                "ordinal_shell_indices must form a contiguous inventory from zero"
            )
        by_components = {
            displacement.components: ordinal_shell_index
            for displacement, ordinal_shell_index in zip(
                self.displacements,
                self.ordinal_shell_indices,
                strict=True,
            )
        }
        zero_position = next(
            index
            for index, displacement in enumerate(self.displacements)
            if displacement.is_zero
        )
        if self.ordinal_shell_indices[zero_position] != 0:
            raise ValueError("the zero displacement must belong to shell zero")
        for components, shell_index in by_components.items():
            if len(components) == 2:
                conjugate: LatticeIntegerComponents = (
                    -components[0],
                    -components[1],
                )
            elif len(components) == 3:
                conjugate = (
                    -components[0],
                    -components[1],
                    -components[2],
                )
            else:
                raise RuntimeError("metric-shell support has invalid dimension")
            if by_components[conjugate] != shell_index:
                raise ValueError("conjugate displacements must share one shell index")

    @property
    def maximum_ordinal_shell_index(self) -> int:
        """Return the largest admitted ordinal shell index."""
        return max(self.ordinal_shell_indices)

    def support_through(
        self, maximum_ordinal_shell_index: int
    ) -> ConjugateClosedSupport:
        """Return every admitted displacement through one ordinal shell index."""
        if type(maximum_ordinal_shell_index) is not int:
            raise TypeError("maximum_ordinal_shell_index must be a built-in integer")
        if not (0 <= maximum_ordinal_shell_index <= self.maximum_ordinal_shell_index):
            raise ValueError(
                "maximum_ordinal_shell_index is outside the admitted inventory"
            )
        return ConjugateClosedSupport(
            tuple(
                displacement
                for displacement, ordinal_shell_index in zip(
                    self.displacements,
                    self.ordinal_shell_indices,
                    strict=True,
                )
                if ordinal_shell_index <= maximum_ordinal_shell_index
            )
        )


__all__ = [
    "ConjugateClosedSupport",
    "MetricShellSupportInventory",
    "SymmetricRangeSupport1D",
]
