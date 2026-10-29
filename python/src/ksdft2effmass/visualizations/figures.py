"""Domain-neutral Matplotlib composition contracts."""

from abc import ABC, abstractmethod

from matplotlib.axes import Axes
from matplotlib.figure import Figure


class BasePlot(ABC):
    """Draw one data relation on a caller-owned axis."""

    __slots__ = ()

    @abstractmethod
    def draw(self, axis: Axes) -> None:
        """Draw one data relation without allocating a figure."""


class BaseSubplot(ABC):
    """Compose plots and axis-local presentation on a caller-owned axis."""

    __slots__ = ()

    @abstractmethod
    def draw(self, axis: Axes) -> None:
        """Draw one complete subplot."""


class BaseFigure(ABC):
    """Allocate and compose one in-memory Matplotlib figure."""

    __slots__ = ()

    @abstractmethod
    def draw(self) -> Figure:
        """Return one fully composed in-memory Matplotlib figure."""
