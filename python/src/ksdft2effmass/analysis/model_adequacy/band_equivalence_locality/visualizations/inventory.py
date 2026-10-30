"""Closed baseline plot inventory for band-equivalence locality."""

from enum import Enum
from typing import Self


class BandEquivalenceLocalityVisualizationPlotEnum(Enum):
    """Name the single authenticated baseline plot."""

    def to_wire(self) -> str:
        """Return the stable wire label."""
        return str(self.value)

    @classmethod
    def from_wire(cls, wire: str) -> Self:
        """Reconstruct a plot identity from its stable wire label."""
        if type(wire) is not str:
            raise TypeError("wire must be a built-in string")
        for member in cls:
            if member.to_wire() == wire:
                return member
        raise ValueError(f"unsupported visualization plot wire label: {wire!r}")

    LOCALITY_REQUIREMENTS = "band-equivalence-locality-requirements.png"


__all__ = ["BandEquivalenceLocalityVisualizationPlotEnum"]
