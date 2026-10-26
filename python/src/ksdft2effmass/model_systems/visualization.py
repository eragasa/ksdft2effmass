"""Base contracts for model-analysis visualization."""

from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from typing import ClassVar, Self, final

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ksdft2effmass.serialization import (
    SerializableValue,
    TypedJsonMappingDeserializer,
    TypedJsonMappingSerializer,
)

from .verification import BaseModelAnalysisVerification


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


class BaseModelAnalysisPlot(ABC):
    """Draw one model-analysis data relation on a caller-owned axis.

    A plot owns data-to-mark transformation only. It does not allocate a figure,
    choose a subplot layout, authenticate inputs, or encode presentation bytes.
    """

    __slots__ = ()

    @abstractmethod
    def draw(self, axis: Axes) -> None:
        """Draw one data relation without allocating a figure.

        Parameters
        ----------
        axis
            Caller-owned Matplotlib axis receiving the concrete data marks.
        """


class BaseModelAnalysisSubplot(ABC):
    """Compose plots and axis-local presentation on one caller-owned axis.

    Concrete subplots may combine any ordered set of model-specific plot actions and
    own axis labels, limits, scales, legends, and annotations. They do not choose the
    enclosing figure layout or encode output bytes.
    """

    __slots__ = ()

    @abstractmethod
    def draw(self, axis: Axes) -> None:
        """Draw one complete subplot.

        Parameters
        ----------
        axis
            Caller-owned Matplotlib axis receiving plots and local presentation.
        """


class BaseModelAnalysisFigure(ABC):
    """Allocate and compose one figure from model-analysis subplots.

    The figure owner chooses layout and figure-wide presentation while remaining
    independent of PNG encoding, filesystem publication, and authentication policy.
    """

    __slots__ = ()

    @abstractmethod
    def draw(self) -> Figure:
        """Return one fully composed in-memory Matplotlib figure.

        Returns
        -------
        matplotlib.figure.Figure
            Figure with its model-specific layout, subplots, and presentation.
        """


class BaseModelAnalysisFigureRenderer(ABC):
    """Encode one composed model-analysis figure as an immutable visualization."""

    __slots__ = ()

    @staticmethod
    @final
    def _encode_png(figure: Figure, dpi: int) -> bytes:
        """Encode and close one figure through the common in-memory PNG path."""
        if not isinstance(figure, Figure):
            raise TypeError("figure action must return a Matplotlib Figure")
        if type(dpi) is not int:
            raise TypeError("dpi must be a built-in int")
        if dpi <= 0:
            raise ValueError("dpi must be positive")
        output = BytesIO()
        try:
            figure.savefig(output, format="png", dpi=dpi)
        finally:
            plt.close(figure)
        return output.getvalue()

    @abstractmethod
    def visualize(self) -> BaseModelAnalysisVisualization:
        """Render and encode one immutable visualization value.

        Returns
        -------
        BaseModelAnalysisVisualization
            Validated in-memory value owned by the concrete figure renderer.
        """


@dataclass(frozen=True, slots=True)
class ModelAnalysisPngFigureRenderer[PlotT: Enum](BaseModelAnalysisFigureRenderer):
    """Encode one independently composed figure as an admitted PNG value.

    Parameters
    ----------
    plot
        Enum member supplying the canonical output filename.
    figure
        Figure action owning layout, subplots, and figure-wide presentation.
    dpi
        Positive built-in integer PNG resolution.

    Notes
    -----
    The renderer owns PNG encoding and closes the figure after the attempt. It does
    not own scientific data projection, axis content, layout, or filesystem writing.
    """

    plot: PlotT
    figure: BaseModelAnalysisFigure
    dpi: int

    def __post_init__(self) -> None:
        if not isinstance(self.plot, Enum):
            raise TypeError("plot must be an Enum member")
        if not isinstance(self.figure, BaseModelAnalysisFigure):
            raise TypeError("figure must be BaseModelAnalysisFigure")
        if type(self.dpi) is not int:
            raise TypeError("dpi must be a built-in int")
        if self.dpi <= 0:
            raise ValueError("dpi must be positive")

    def visualize(self) -> ModelAnalysisPngVisualization[PlotT]:
        """Draw, encode, close, and admit one PNG visualization.

        Returns
        -------
        ModelAnalysisPngVisualization[PlotT]
            Validated immutable PNG bytes associated with ``plot``.

        Raises
        ------
        TypeError
            The figure action returns a value other than a Matplotlib figure.
        ValueError
            The encoded bytes fail PNG admission.
        """
        png = self._encode_png(self.figure.draw(), self.dpi)
        return ModelAnalysisPngVisualization(plot=self.plot, png=png)


class BaseModelAnalysisVisualizer(ABC):
    """Authenticate data and define aggregate model-analysis visualization."""

    __slots__ = ()

    @staticmethod
    @final
    def _authenticate(
        data: BaseModelAnalysisVisualizationData,
        verification: BaseModelAnalysisVerification,
    ) -> None:
        """Require passing verification of the exact canonical projection bytes."""
        if not isinstance(data, BaseModelAnalysisVisualizationData):
            raise TypeError("data must be BaseModelAnalysisVisualizationData")
        if not isinstance(verification, BaseModelAnalysisVerification):
            raise TypeError("verification must be BaseModelAnalysisVerification")
        if not verification.passed:
            raise ValueError("visualization requires passing verification")
        digest = hashlib.sha256(data.to_json()).hexdigest()
        if verification.authenticated_visualization_data_sha256() != digest:
            raise ValueError(
                "verification authenticates different visualization data; "
                "digests differ"
            )

    @staticmethod
    @final
    def _require_complete_inventory[PlotT: Enum](
        visualizations: frozenset[ModelAnalysisPngVisualization[PlotT]],
        expected_plots: frozenset[PlotT],
    ) -> None:
        """Require visualizations to cover the exact declared plot inventory."""
        if {visualization.plot for visualization in visualizations} != expected_plots:
            raise RuntimeError(
                "visualization inventory differs from the declared plot inventory"
            )

    @abstractmethod
    def visualize(self) -> frozenset[BaseModelAnalysisVisualization]:
        """Render a unique immutable visualization set.

        Returns
        -------
        frozenset[BaseModelAnalysisVisualization]
            Complete concrete visualization inventory.
        """
