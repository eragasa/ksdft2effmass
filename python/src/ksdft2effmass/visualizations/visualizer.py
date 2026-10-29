"""Authenticated aggregate visualization action."""

from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from enum import Enum
from typing import final

from ksdft2effmass.verification import VisualizationVerification

from .data import BaseVisualizationData
from .records import PngVisualization


class BaseVisualizer[
    DataT: BaseVisualizationData,
    VerificationT: VisualizationVerification,
    PlotT: Enum,
](ABC):
    """Bind authenticated projection input and enforce one closed output inventory."""

    __slots__ = ("_data", "_plots", "_verification")

    def __init__(
        self,
        *,
        data: DataT,
        verification: VerificationT,
        plots: tuple[PlotT, ...],
    ) -> None:
        if not isinstance(data, BaseVisualizationData):
            raise TypeError("data must be BaseVisualizationData")
        if not isinstance(verification, VisualizationVerification):
            raise TypeError("verification must be VisualizationVerification")
        if not isinstance(plots, tuple):
            raise TypeError("plots must be a tuple")
        if not plots:
            raise ValueError("plots must not be empty")
        if any(not isinstance(plot, Enum) for plot in plots):
            raise TypeError("plots must contain Enum members")
        if len(frozenset(plots)) != len(plots):
            raise ValueError("plots must contain unique Enum members")
        if any(type(plot) is not type(plots[0]) for plot in plots):
            raise TypeError("plots must belong to one Enum type")
        filenames = tuple(plot.value for plot in plots)
        if any(type(filename) is not str for filename in filenames):
            raise TypeError("plot values must be built-in strings")
        if len(frozenset(filenames)) != len(filenames):
            raise ValueError("plot values must be unique")
        if not verification.passed:
            raise ValueError("visualization requires passing verification")
        digest = hashlib.sha256(data.to_json()).hexdigest()
        if verification.authenticated_visualization_data_sha256() != digest:
            raise ValueError(
                "verification authenticates different visualization data; "
                "digests differ"
            )
        self._data = data
        self._verification = verification
        self._plots = plots

    @property
    def data(self) -> DataT:
        """Return the immutable authenticated projection."""
        return self._data

    @property
    def verification(self) -> VerificationT:
        """Return the constructor-bound verification aggregate."""
        return self._verification

    @property
    def plots(self) -> tuple[PlotT, ...]:
        """Return the complete ordered closed plot inventory."""
        return self._plots

    @final
    def visualize(self) -> frozenset[PngVisualization[PlotT]]:
        """Render and validate the complete closed visualization inventory."""
        visualizations = self._render()
        if not isinstance(visualizations, frozenset):
            raise TypeError("rendered visualizations must be a frozenset")
        if any(
            not isinstance(visualization, PngVisualization)
            for visualization in visualizations
        ):
            raise TypeError("rendered values must be PngVisualization")
        if len(visualizations) != len(self.plots) or {
            visualization.plot for visualization in visualizations
        } != set(self.plots):
            raise RuntimeError(
                "visualization inventory differs from the declared plot inventory"
            )
        return visualizations

    @abstractmethod
    def _render(self) -> frozenset[PngVisualization[PlotT]]:
        """Render one value for every constructor-bound plot member."""
