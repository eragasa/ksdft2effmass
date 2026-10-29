"""Figure rendering and PNG admission."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from io import BytesIO

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from .figures import BaseFigure
from .records import BaseVisualization, PngVisualization


class BaseFigureRenderer(ABC):
    """Encode one composed figure as an immutable visualization."""

    __slots__ = ()

    @abstractmethod
    def visualize(self) -> BaseVisualization:
        """Render and encode one immutable visualization value."""


@dataclass(frozen=True, slots=True)
class PngFigureRenderer[PlotT: Enum](BaseFigureRenderer):
    """Encode one independently composed figure as an admitted PNG value."""

    plot: PlotT
    figure: BaseFigure
    dpi: int

    def __post_init__(self) -> None:
        if not isinstance(self.plot, Enum):
            raise TypeError("plot must be an Enum member")
        if not isinstance(self.figure, BaseFigure):
            raise TypeError("figure must be BaseFigure")
        if type(self.dpi) is not int:
            raise TypeError("dpi must be a built-in int")
        if self.dpi <= 0:
            raise ValueError("dpi must be positive")

    def visualize(self) -> PngVisualization[PlotT]:
        """Draw, encode, close, and admit one PNG visualization."""
        figure = self.figure.draw()
        if not isinstance(figure, Figure):
            raise TypeError("figure action must return a Matplotlib Figure")
        output = BytesIO()
        try:
            figure.savefig(output, format="png", dpi=self.dpi)
        finally:
            plt.close(figure)
        return PngVisualization(plot=self.plot, png=output.getvalue())
