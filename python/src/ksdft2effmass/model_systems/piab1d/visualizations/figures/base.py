"""PIAB1D figure-data binding."""

from ksdft2effmass.visualizations import BaseFigure

from ..data import Piab1dVisualizationData


class _Piab1dFigure(BaseFigure):
    """Bind authenticated PIAB1D data to one model-specific figure action."""

    __slots__ = ("_data",)

    def __init__(self, data: Piab1dVisualizationData) -> None:
        if not isinstance(data, Piab1dVisualizationData):
            raise TypeError("data must be Piab1dVisualizationData")
        self._data = data
