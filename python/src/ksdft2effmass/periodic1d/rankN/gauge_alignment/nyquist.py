"""Nyquist-mode disposition and its canonical wire mapping."""

from __future__ import annotations

from collections.abc import Mapping
from enum import Enum, auto, unique
from types import MappingProxyType
from typing import ClassVar, final


@unique
class NyquistModeDispositionEnum(Enum):
    """State the mathematical disposition of a self-inverse Nyquist mode."""

    ABSENT_ON_ODD_MESH = auto()


@final
class NyquistModeDispositionWireMapping:
    """Own the strict bidirectional wire mapping for Nyquist-mode dispositions."""

    _ToWireMap: ClassVar[Mapping[NyquistModeDispositionEnum, str]] = MappingProxyType(
        {NyquistModeDispositionEnum.ABSENT_ON_ODD_MESH: ("absent-on-odd-mesh")}
    )
    _FromWireMap: ClassVar[Mapping[str, NyquistModeDispositionEnum]] = MappingProxyType(
        {"absent-on-odd-mesh": (NyquistModeDispositionEnum.ABSENT_ON_ODD_MESH)}
    )

    @classmethod
    def to_wire(cls, value: NyquistModeDispositionEnum) -> str:
        """Return the canonical wire value for one exact domain enum."""
        if type(value) is not NyquistModeDispositionEnum:
            raise TypeError("value must be NyquistModeDispositionEnum")
        return cls._ToWireMap[value]

    @classmethod
    def from_wire(cls, value: str) -> NyquistModeDispositionEnum:
        """Return the domain enum for one supported canonical wire value."""
        if type(value) is not str:
            raise TypeError("value must be a built-in string")
        if value not in cls._FromWireMap:
            raise ValueError("unsupported Nyquist-mode disposition")
        return cls._FromWireMap[value]


__all__ = [
    "NyquistModeDispositionEnum",
    "NyquistModeDispositionWireMapping",
]
