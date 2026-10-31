"""Ordinary Enum ownership for explicit stable string mapping values."""

from __future__ import annotations

from enum import Enum
from typing import Self


class StringWireEnum(Enum):
    """Provide exact string mapping for an ordinary, closed Enum vocabulary.

    This behavior-only base intentionally does not inherit :class:`str`. Concrete
    domain enums own their members, while retained records explicitly call
    :meth:`to_wire` from ``_mapping`` and :meth:`from_wire` from ``_from_mapping``.
    """

    def __init__(self, value: str) -> None:
        """Reject non-string member values while the concrete Enum is defined."""
        if type(value) is not str:
            raise TypeError("StringWireEnum member values must be built-in strings")

    def to_wire(self) -> str:
        """Return this member's exact built-in string mapping value."""
        if type(self.value) is not str:
            raise TypeError("StringWireEnum member values must be built-in strings")
        return self.value

    @classmethod
    def from_wire(cls, wire: str) -> Self:
        """Reconstruct one exact member from a built-in string mapping value."""
        if type(wire) is not str:
            raise TypeError("wire must be a built-in string")
        for member in cls:
            if member.to_wire() == wire:
                return member
        raise ValueError(f"unsupported {cls.__name__} wire label: {wire!r}")


__all__ = ["StringWireEnum"]
