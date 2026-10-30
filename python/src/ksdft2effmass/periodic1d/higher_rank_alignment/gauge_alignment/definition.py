"""Scientific gauge-alignment identities and their explicit wire mapping."""

from __future__ import annotations

from collections.abc import Mapping
from enum import Enum, auto, unique
from types import MappingProxyType
from typing import ClassVar, final


@unique
class Periodic1DHigherRankGaugeAlignment(Enum):
    """Identify one prescribed retained-space gauge alignment."""

    IDENTITY = auto()
    GLOBAL_UNITARY = auto()
    POINTWISE_UNITARY = auto()
    KNOWN_INVERSE_ORACLE = auto()


@final
class GaugeAlignmentWireMapping:
    """Own the strict bidirectional mapping for gauge-alignment wire values."""

    _ToWireMap: ClassVar[Mapping[Periodic1DHigherRankGaugeAlignment, str]] = (
        MappingProxyType(
            {
                Periodic1DHigherRankGaugeAlignment.IDENTITY: "identity",
                Periodic1DHigherRankGaugeAlignment.GLOBAL_UNITARY: "global-unitary",
                Periodic1DHigherRankGaugeAlignment.POINTWISE_UNITARY: (
                    "pointwise-unitary"
                ),
                Periodic1DHigherRankGaugeAlignment.KNOWN_INVERSE_ORACLE: (
                    "known-inverse-oracle"
                ),
            }
        )
    )
    _FromWireMap: ClassVar[
        Mapping[str, Periodic1DHigherRankGaugeAlignment]
    ] = MappingProxyType(
        {
            wire_value: gauge_alignment
            for gauge_alignment, wire_value in _ToWireMap.items()
        }
    )

    @classmethod
    def to_wire(cls, value: Periodic1DHigherRankGaugeAlignment) -> str:
        """Return the canonical wire value for one exact domain enum."""
        if type(value) is not Periodic1DHigherRankGaugeAlignment:
            raise TypeError("value must be Periodic1DHigherRankGaugeAlignment")
        return cls._ToWireMap[value]

    @classmethod
    def from_wire(cls, value: str) -> Periodic1DHigherRankGaugeAlignment:
        """Return the domain enum for one supported canonical wire value."""
        if type(value) is not str:
            raise TypeError("value must be a built-in string")
        if value not in cls._FromWireMap:
            raise ValueError("unsupported gauge alignment")
        return cls._FromWireMap[value]


__all__ = [
    "GaugeAlignmentWireMapping",
    "Periodic1DHigherRankGaugeAlignment",
]
