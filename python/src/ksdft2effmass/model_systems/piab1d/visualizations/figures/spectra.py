"""PIAB1D spectrum, state, and wavefunction figures."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ksdft2effmass.visualizations import BaseFigure, BasePlot, BaseSubplot

from ..data import Piab1dVisualizationData
from .base import _Piab1dFigure


class _Piab1dSpectrumPlot(BasePlot):
    """Draw continuum and represented energies with the retained cutoff."""

    __slots__ = ("_data",)

    def __init__(self, data: Piab1dVisualizationData) -> None:
        self._data = data

    def draw(self, axis: Axes) -> None:
        data = self._data
        points = data.computed_energies.magnitude.size
        mode_numbers = np.arange(1, points + 1)
        axis.plot(
            mode_numbers,
            data.continuum_energies.magnitude,
            "o-",
            label="continuum",
        )
        axis.plot(
            mode_numbers,
            data.computed_energies.magnitude,
            "s--",
            label="finite difference",
        )
        axis.axvline(
            data.retained_dimension + 0.5,
            color="black",
            linewidth=0.8,
            linestyle=":",
        )


class _Piab1dSpectrumSubplot(BaseSubplot):
    """Compose the spectrum plot with energy-axis presentation."""

    __slots__ = ("_plot",)

    def __init__(self, data: Piab1dVisualizationData) -> None:
        self._plot = _Piab1dSpectrumPlot(data)

    def draw(self, axis: Axes) -> None:
        self._plot.draw(axis)
        axis.set_xlabel("mode index")
        axis.set_ylabel("nondimensional energy")
        axis.set_title("PIAB1D spectrum")
        axis.legend()


class _Piab1dRetainedStatesPlot(BasePlot):
    """Draw normalized retained eigenvectors at vertically offset levels."""

    __slots__ = ("_data",)

    def __init__(self, data: Piab1dVisualizationData) -> None:
        self._data = data

    def draw(self, axis: Axes) -> None:
        data = self._data
        points = data.computed_energies.magnitude.size
        coordinates = np.linspace(0.0, data.length.magnitude, points + 2)[1:-1]
        for mode in range(data.retained_dimension):
            vector = data.eigenvectors.magnitude[:, mode]
            amplitude = vector / np.max(np.abs(vector))
            axis.plot(coordinates, amplitude + 2.0 * mode, label=f"mode {mode + 1}")


class _Piab1dRetainedStatesSubplot(BaseSubplot):
    """Compose retained-state curves with position-axis presentation."""

    __slots__ = ("_plot",)

    def __init__(self, data: Piab1dVisualizationData) -> None:
        self._plot = _Piab1dRetainedStatesPlot(data)

    def draw(self, axis: Axes) -> None:
        self._plot.draw(axis)
        axis.set_xlabel("position")
        axis.set_ylabel("normalized amplitude + offset")
        axis.set_title("Retained discrete states")
        axis.legend()


class _Piab1dSpectrumAndStatesFigure(BaseFigure):
    """Compose independently owned spectrum and retained-state subplots."""

    __slots__ = ("_data",)

    def __init__(self, data: Piab1dVisualizationData) -> None:
        self._data = data

    def draw(self) -> Figure:
        figure, axes = plt.subplots(
            1,
            2,
            figsize=(10.0, 4.0),
            constrained_layout=True,
        )
        _Piab1dSpectrumSubplot(self._data).draw(axes[0])
        _Piab1dRetainedStatesSubplot(self._data).draw(axes[1])
        return figure


class _ContinuumWavefunctionLadderFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        data = self._data
        if data.retained_dimension != 3:
            raise ValueError("the ladder plot requires exactly three retained states")
        colors = ("#0072B2", "#D55E00", "#009E73")
        figure, axis = plt.subplots(figsize=(5.2, 5.0), constrained_layout=True)
        for mode, color in zip(range(1, 4), colors, strict=True):
            energy = data.continuum_energies.magnitude[mode - 1]
            wavefunction = data.continuum_wavefunctions.magnitude[:, mode - 1]
            axis.axhline(energy, color=color, linewidth=0.8, alpha=0.45)
            axis.plot(
                data.continuum_coordinates.magnitude,
                energy + 2.4 * wavefunction,
                color=color,
                linewidth=2.0,
            )
            axis.text(
                1.015,
                energy,
                rf"$E_{mode}$",
                color=color,
                va="center",
                ha="left",
            )
        self._style_axis(axis, "Continuum eigenfunctions")
        return figure

    def _style_axis(self, axis: Axes, title: str) -> None:
        axis.axvline(0.0, color="black", linewidth=1.2)
        axis.axvline(1.0, color="black", linewidth=1.2)
        axis.set_xlim(-0.04, 1.04)
        axis.set_xlabel(r"position $x/L$")
        axis.set_ylabel("energy")
        axis.set_title(title)
        axis.spines[["top", "right"]].set_visible(False)


class _DiscreteWavefunctionLadderFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        data = self._data
        if data.retained_dimension != 3:
            raise ValueError("the ladder plot requires exactly three retained states")
        points = data.computed_energies.magnitude.size
        length = data.length.magnitude
        coordinates = np.linspace(0.0, length, points + 2)[1:-1]
        plotted_coordinates = np.concatenate(([0.0], coordinates / length, [1.0]))
        colors = ("#0072B2", "#D55E00", "#009E73")
        figure, axis = plt.subplots(figsize=(5.2, 5.0), constrained_layout=True)
        for mode, color in zip(range(1, 4), colors, strict=True):
            energy = data.computed_energies.magnitude[mode - 1]
            values = np.concatenate(
                (
                    [0.0],
                    data.quadrature_eigenvectors.magnitude[:, mode - 1],
                    [0.0],
                )
            )
            axis.axhline(energy, color=color, linewidth=0.8, alpha=0.45)
            axis.plot(
                plotted_coordinates,
                energy + 2.4 * values,
                color=color,
                linewidth=1.2,
                alpha=0.65,
            )
            axis.scatter(
                plotted_coordinates,
                energy + 2.4 * values,
                color=color,
                s=23,
                zorder=3,
            )
            axis.text(
                1.015,
                energy,
                rf"$E_{{{mode},\Delta x}}$",
                color=color,
                va="center",
                ha="left",
            )
        axis.axvline(0.0, color="black", linewidth=1.2)
        axis.axvline(1.0, color="black", linewidth=1.2)
        axis.set_xlim(-0.04, 1.04)
        axis.set_xlabel(r"position $x/L$")
        axis.set_ylabel("energy")
        axis.set_title(rf"Finite-grid wavefunctions ($N={points + 2}$)")
        axis.spines[["top", "right"]].set_visible(False)
        return figure
