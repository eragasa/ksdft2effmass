"""Typed periodic-one-dimensional retained-support inventories."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.periodic1d.translations import (
    Periodic1DSymmetricTranslationRange,
    Periodic1DSymmetricTranslationRangeInventory,
)
from ksdft2effmass.real_space_support_truncation.support import (
    SymmetricRangeSupport1D,
)

from .base import Periodic1DSupportTruncation


@dataclass(frozen=True, slots=True)
class Periodic1DSymmetricSupportInventory(Periodic1DSupportTruncation):
    """Retain ordered candidate policies for irreversible symmetric support removal."""

    supports: tuple[SymmetricRangeSupport1D, ...]

    def __post_init__(self) -> None:
        if type(self.supports) is not tuple or not self.supports:
            raise TypeError("supports must be a nonempty tuple")
        if any(type(value) is not SymmetricRangeSupport1D for value in self.supports):
            raise TypeError("supports must contain exact symmetric-range policies")
        Periodic1DSymmetricTranslationRangeInventory(self.ranges)

    @classmethod
    def from_maximum_ranges(
        cls,
        maximum_ranges: tuple[int, ...],
    ) -> Periodic1DSymmetricSupportInventory:
        """Construct candidate retained-support policies from integer range labels."""
        neutral = Periodic1DSymmetricTranslationRangeInventory.from_maximum_ranges(
            maximum_ranges
        )
        return cls(
            tuple(
                SymmetricRangeSupport1D(value.maximum_range) for value in neutral.ranges
            )
        )

    @property
    def ranges(self) -> tuple[Periodic1DSymmetricTranslationRange, ...]:
        """Return the neutral ranges underlying the support policies."""
        return tuple(
            Periodic1DSymmetricTranslationRange(value.maximum_range)
            for value in self.supports
        )

    @property
    def maximum_ranges(self) -> tuple[int, ...]:
        """Return the ordered retained-support range labels."""
        return tuple(value.maximum_range for value in self.supports)


__all__ = ["Periodic1DSymmetricSupportInventory"]
