"""Immutable admitted visualization values."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from typing import ClassVar

import matplotlib.image as mpimg


class BaseVisualization:
    """Identify an immutable admitted visualization value."""

    __slots__ = ()


@dataclass(frozen=True, slots=True)
class PngVisualization[PlotT: Enum](BaseVisualization):
    """Retain one validated PNG associated with a closed plot identifier."""

    plot: PlotT
    png: bytes
    media_type: ClassVar[str] = "image/png"

    def __post_init__(self) -> None:
        if not isinstance(self.plot, Enum):
            raise TypeError("plot must be an Enum member")
        if type(self.plot.value) is not str or not self.plot.value:
            raise TypeError("plot values must be nonempty built-in strings")
        filename = self.plot.value
        windows_stem = filename.split(".", maxsplit=1)[0].rstrip(" .").upper()
        windows_reserved = {
            "AUX",
            "CON",
            "NUL",
            "PRN",
            *(f"COM{index}" for index in range(1, 10)),
            *(f"LPT{index}" for index in range(1, 10)),
        }
        if (
            filename in {".", ".."}
            or filename.endswith((" ", "."))
            or any(
                ord(character) < 32 or character in '<>:"/\\|?*'
                for character in filename
            )
            or windows_stem in windows_reserved
        ):
            raise ValueError("plot values must be cross-platform-safe basenames")
        if len(filename) <= len(".png") or not filename.endswith(".png"):
            raise ValueError("plot values must be basenames ending in .png")
        if type(self.png) is not bytes:
            raise TypeError("png must be built-in bytes")
        if not self.png.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("png must contain the PNG signature")
        try:
            decoded = mpimg.imread(BytesIO(self.png), format="png")
        except (OSError, SyntaxError, ValueError) as error:
            raise ValueError("png must contain a decodable PNG image") from error
        if decoded.ndim not in {2, 3} or decoded.size == 0:
            raise ValueError("png must contain a nonempty PNG image")

    @property
    def filename(self) -> str:
        """Return the safe PNG basename supplied by the plot enumeration."""
        value = self.plot.value
        if type(value) is not str:
            raise TypeError("plot values must remain built-in strings")
        return value
