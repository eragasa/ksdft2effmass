"""Typed integer-index inventories for periodic one-dimensional representations."""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)

from .base import Periodic1DCapability


@dataclass(frozen=True, slots=True)
class Periodic1DSymmetricTranslationRange(Periodic1DCapability):
    """Identify the complete ordinary-translation interval from ``-R`` to ``R``.

    This is a neutral integer-index range. It does not state whether the interval is
    used for diagnostics or retained support, and it carries no physical distance.
    """

    maximum_range: int

    def __post_init__(self) -> None:
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in integer")
        if self.maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")

    @property
    def translations(self) -> tuple[int, ...]:
        """Return every ordinary translation in the closed symmetric interval."""
        return tuple(range(-self.maximum_range, self.maximum_range + 1))


@dataclass(frozen=True, slots=True)
class Periodic1DSymmetricTranslationRangeInventory(Periodic1DCapability):
    """Retain an ordered, strictly increasing inventory of symmetric ranges."""

    ranges: tuple[Periodic1DSymmetricTranslationRange, ...]

    def __post_init__(self) -> None:
        if type(self.ranges) is not tuple or not self.ranges:
            raise TypeError("ranges must be a nonempty tuple")
        if any(
            type(value) is not Periodic1DSymmetricTranslationRange
            for value in self.ranges
        ):
            raise TypeError("ranges must contain exact symmetric translation ranges")
        maximum_ranges = tuple(value.maximum_range for value in self.ranges)
        if maximum_ranges != tuple(sorted(set(maximum_ranges))):
            raise ValueError("maximum ranges must be unique and strictly increasing")

    @classmethod
    def from_maximum_ranges(
        cls,
        maximum_ranges: tuple[int, ...],
    ) -> Periodic1DSymmetricTranslationRangeInventory:
        """Construct an inventory from exact nonnegative integer range labels."""
        if type(maximum_ranges) is not tuple or not maximum_ranges:
            raise TypeError("maximum_ranges must be a nonempty tuple")
        return cls(
            tuple(
                Periodic1DSymmetricTranslationRange(value) for value in maximum_ranges
            )
        )

    @property
    def maximum_ranges(self) -> tuple[int, ...]:
        """Return the ordered integer range labels."""
        return tuple(value.maximum_range for value in self.ranges)


@dataclass(frozen=True, slots=True)
class Periodic1DOrdinaryTranslationInventory(Periodic1DCapability):
    """Retain sorted, unique, conjugate-closed ordinary cell translations.

    These integers label distinct ordinary-lattice cells. They are not cyclic
    equivalence classes and carry no physical distance until combined with explicit
    :class:`~ksdft2effmass.periodic1d.geometry.Periodic1DLatticeGeometry`.
    """

    translations: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.translations) is not tuple or not self.translations:
            raise TypeError("translations must be a nonempty tuple")
        if any(type(value) is not int for value in self.translations):
            raise TypeError("translations must contain built-in integers")
        if self.translations != tuple(sorted(set(self.translations))):
            raise ValueError("translations must be unique and strictly increasing")
        if 0 not in self.translations:
            raise ValueError("ordinary translation inventory must contain zero")
        admitted = set(self.translations)
        if any(-value not in admitted for value in self.translations):
            raise ValueError("ordinary translation inventory must be conjugate-closed")

    @property
    def maximum_range(self) -> int:
        """Return the largest represented absolute cell displacement."""
        return max(abs(value) for value in self.translations)

    @property
    def displacements(self) -> tuple[LatticeDisplacement, ...]:
        """Return the exact PhysKit one-dimensional displacement inventory."""
        return tuple(
            LatticeDisplacement(LatticeDimension.ONE, (translation,))
            for translation in self.translations
        )


@dataclass(frozen=True, slots=True)
class Periodic1DCyclicRepresentativeInventory(Periodic1DCapability):
    """Retain complete centered representatives of one finite cyclic cell domain.

    An even domain has one negative-Nyquist representative whose positive counterpart
    denotes the same cyclic class. An odd domain has no Nyquist class, so every centered
    representative also identifies a distinct ordinary translation.
    """

    representatives: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.representatives) is not tuple or not self.representatives:
            raise TypeError("representatives must be a nonempty tuple")
        if any(type(value) is not int for value in self.representatives):
            raise TypeError("representatives must contain built-in integers")
        point_count = len(self.representatives)
        if point_count < 2:
            raise ValueError(
                "cyclic representative inventory must have size at least two"
            )
        half_size = point_count // 2
        expected = (
            tuple(range(-half_size, half_size))
            if point_count % 2 == 0
            else tuple(range(-half_size, half_size + 1))
        )
        if self.representatives != expected:
            raise ValueError(
                "cyclic representatives must equal the complete centered inventory"
            )

    @property
    def point_count(self) -> int:
        """Return the even finite cyclic domain size."""
        return len(self.representatives)

    @property
    def has_nyquist_class(self) -> bool:
        """Return whether the even cyclic domain contains one Nyquist class."""
        return self.point_count % 2 == 0

    @property
    def negative_nyquist_representative(self) -> int:
        """Return the unique centered representative of an even-domain Nyquist class."""
        if not self.has_nyquist_class:
            raise ValueError("an odd cyclic domain has no Nyquist class")
        return self.representatives[0]

    @property
    def ordinary_translation_inventory(self) -> Periodic1DOrdinaryTranslationInventory:
        """Return ordinary translations after removing any cyclic Nyquist class."""
        translations = (
            self.representatives[1:] if self.has_nyquist_class else self.representatives
        )
        return Periodic1DOrdinaryTranslationInventory(translations)


__all__ = [
    "Periodic1DCyclicRepresentativeInventory",
    "Periodic1DOrdinaryTranslationInventory",
    "Periodic1DSymmetricTranslationRange",
    "Periodic1DSymmetricTranslationRangeInventory",
]
