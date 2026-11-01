"""Typed periodic-one-dimensional hopping-diagnostic range inventories."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.periodic1d.translations import (
    Periodic1DSymmetricTranslationRange,
    Periodic1DSymmetricTranslationRangeInventory,
)

from .base import Periodic1DHoppingLocality


@dataclass(frozen=True, slots=True)
class Periodic1DHoppingDiagnosticRangeInventory(Periodic1DHoppingLocality):
    """Retain ordered symmetric ranges for unchanged-coefficient diagnostics.

    Membership states that the ranges are diagnostic partitions only. It does not
    authorize coefficient removal or identify retained finite support.
    """

    ranges: tuple[Periodic1DSymmetricTranslationRange, ...]

    def __post_init__(self) -> None:
        Periodic1DSymmetricTranslationRangeInventory(self.ranges)

    @classmethod
    def from_maximum_ranges(
        cls,
        maximum_ranges: tuple[int, ...],
    ) -> Periodic1DHoppingDiagnosticRangeInventory:
        """Construct one diagnostic inventory from exact integer range labels."""
        neutral = Periodic1DSymmetricTranslationRangeInventory.from_maximum_ranges(
            maximum_ranges
        )
        return cls(neutral.ranges)

    @property
    def maximum_ranges(self) -> tuple[int, ...]:
        """Return the ordered diagnostic range labels."""
        return tuple(value.maximum_range for value in self.ranges)


__all__ = ["Periodic1DHoppingDiagnosticRangeInventory"]
