"""Base contracts for model-analysis visualization."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from typing import ClassVar, Self, final

import matplotlib.image as mpimg

from ksdft2effmass.serialization import (
    SerializableValue,
    TypedJsonMappingDeserializer,
    TypedJsonMappingSerializer,
)


class BaseModelAnalysisVisualization:
    """Identify an immutable model-analysis visualization value."""

    __slots__ = ()


@dataclass(frozen=True, slots=True)
class ModelAnalysisPngVisualization[PlotT: Enum](BaseModelAnalysisVisualization):
    """Retain one immutable validated PNG associated with an enumerated plot.

    Parameters
    ----------
    plot
        Enum member whose value is a safe canonical ``.png`` basename.
    png
        Complete encoded PNG bytes.

    Raises
    ------
    TypeError
        ``plot`` is not an enum member or ``png`` is not bytes.
    ValueError
        The filename is unsafe or the bytes do not decode to a nonempty PNG image.

    Notes
    -----
    Successful decoding verifies the image container. It does not verify the
    scientific meaning of rendered pixels.
    """

    plot: PlotT
    png: bytes
    media_type: ClassVar[str] = "image/png"

    def __post_init__(self) -> None:
        if not isinstance(self.plot, Enum):
            raise TypeError("plot must be an Enum member")
        if type(self.plot.value) is not str or not self.plot.value:
            raise TypeError("plot values must be nonempty built-in strings")
        filename = self.plot.value
        if (
            "/" in filename
            or "\\" in filename
            or "\x00" in filename
            or filename in {".", ".."}
        ):
            raise ValueError("plot values must be safe basenames")
        if len(filename) <= len(".png") or not filename.endswith(".png"):
            raise ValueError("plot values must be basenames ending in .png")
        if not isinstance(self.png, bytes):
            raise TypeError("png must be bytes")
        try:
            decoded = mpimg.imread(BytesIO(self.png), format="png")
        except (OSError, SyntaxError, ValueError) as error:
            raise ValueError("png must contain a decodable PNG image") from error
        if decoded.ndim not in {2, 3} or decoded.size == 0:
            raise ValueError("png must contain a nonempty PNG image")

    @property
    def filename(self) -> str:
        """Return the stable basename supplied by the plot enumeration.

        Returns
        -------
        str
            Nonempty safe basename ending in ``.png``.

        Raises
        ------
        TypeError
            The enum value no longer has the required built-in string type.
        """
        value = self.plot.value
        if type(value) is not str:
            raise TypeError("plot values must remain built-in strings")
        return value


class BaseModelAnalysisVisualizationData(ABC):
    """Enforce final dictionary and JSON boundaries for visualization data."""

    __slots__ = ()

    @abstractmethod
    def _mapping(self) -> Mapping[str, SerializableValue]:
        """Return the concrete visualization data's typed mapping."""

    @classmethod
    @abstractmethod
    def _from_mapping(
        cls,
        values: Mapping[str, SerializableValue],
    ) -> Self:
        """Reconstruct concrete visualization data from its typed mapping."""

    @final
    def to_dict(self) -> Mapping[str, SerializableValue]:
        """Return the concrete visualization projection as typed values.

        Returns
        -------
        Mapping[str, SerializableValue]
            Domain-owned projection fields before generic JSON normalization.
        """
        return self._mapping()

    @classmethod
    @final
    def from_dict(
        cls,
        values: Mapping[str, SerializableValue],
    ) -> Self:
        """Reconstruct concrete visualization data from typed values.

        Parameters
        ----------
        values
            Decoded string-keyed scientific-value mapping.

        Returns
        -------
        Self
            Immutable validated visualization projection.

        Raises
        ------
        TypeError
            ``values`` or a field has the wrong type.
        ValueError
            The field inventory or a correlated visualization invariant is invalid.
        """
        if not isinstance(values, Mapping):
            raise TypeError("values must be a mapping")
        return cls._from_mapping(values)

    @final
    def to_json(self) -> bytes:
        """Return canonical JSON through the generic typed-value codec.

        Returns
        -------
        bytes
            Canonical UTF-8 bytes used for projection authentication.

        Notes
        -----
        The verifier hashes these exact bytes before composing its aggregate value.
        """
        return TypedJsonMappingSerializer().serialize(self.to_dict())

    @classmethod
    @final
    def from_json(cls, wire: bytes) -> Self:
        """Reconstruct visualization data from canonical JSON bytes.

        Parameters
        ----------
        wire
            Typed JSON bytes containing one complete projection.

        Returns
        -------
        Self
            Immutable validated projection.

        Raises
        ------
        TypeError
            The wire or a decoded field has the wrong type.
        ValueError
            JSON metadata or projection invariants are invalid.
        """
        values = TypedJsonMappingDeserializer().deserialize(wire)
        return cls.from_dict(values)


class BaseModelAnalysisVisualizationPlotter(ABC):
    """Define one cohesive model-analysis plot-rendering action."""

    __slots__ = ()

    @abstractmethod
    def visualize(self) -> BaseModelAnalysisVisualization:
        """Render one immutable visualization value.

        Returns
        -------
        BaseModelAnalysisVisualization
            Validated in-memory value owned by the concrete plotter.
        """


class BaseModelAnalysisVisualizer(ABC):
    """Define an aggregate model-analysis visualization action."""

    __slots__ = ()

    @abstractmethod
    def visualize(self) -> frozenset[BaseModelAnalysisVisualization]:
        """Render a unique immutable visualization set.

        Returns
        -------
        frozenset[BaseModelAnalysisVisualization]
            Complete concrete visualization inventory.
        """
