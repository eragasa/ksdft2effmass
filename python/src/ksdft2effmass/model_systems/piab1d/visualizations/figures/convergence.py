"""PIAB1D convergence and retained-dimension figures."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .base import _Piab1dFigure


class _RetainedDimensionSelectionFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        data = self._data
        dimensions = np.arange(
            1,
            data.selection.probabilities.magnitude.size + 1,
            dtype=np.int64,
        )
        tolerance_axis = np.logspace(-8.0, np.log10(0.35), 2000)
        required_dimensions = np.asarray(
            [
                dimensions[
                    np.flatnonzero(
                        data.selection.omitted_probabilities.magnitude
                        <= candidate_tolerance
                    )[0]
                ]
                for candidate_tolerance in tolerance_axis
            ],
            dtype=np.int64,
        )
        figure, axis = plt.subplots(figsize=(7.6, 4.8), constrained_layout=True)
        axis.step(
            tolerance_axis,
            required_dimensions,
            where="post",
            color="#0072B2",
            linewidth=2.2,
            label=r"required dimension $M_\star(\tau)$",
        )
        axis.annotate(
            rf"$\tau={data.selection.tolerance:.2f}\;\Longrightarrow\;"
            rf"M_\star={data.selection.selected_count}$",
            xy=(data.selection.tolerance, data.selection.selected_count),
            xytext=(
                data.selection.tolerance * 2.0,
                data.selection.selected_count + 0.65,
            ),
            arrowprops={"arrowstyle": "->", "color": "black"},
        )
        axis.set(
            title="Required retained dimension versus a priori tolerance",
            xlabel=r"omitted-probability tolerance $\tau$",
            ylabel=r"minimum retained dimension $M_\star(\tau)$",
            yticks=dimensions,
            xscale="log",
        )
        axis.grid(True, which="both", alpha=0.25)
        axis.legend(frameon=False, loc="upper right")
        return figure


class _ConvergenceSeriesFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        data = self._data
        convergence = data.convergence
        spacings = convergence.spacings.magnitude
        point_counts = np.asarray(data.convergence_interior_points, dtype=np.int64) + 2
        marker_interval = max(point_counts.size // 12, 1)
        colors = ("#0072B2", "#D55E00", "#009E73")
        figure, axes = plt.subplots(1, 2, figsize=(11.5, 4.5), constrained_layout=True)
        error_axis, order_axis = axes
        order_modes = tuple(
            data.convergence_modes[column] for column in convergence.order_columns
        )
        for column, (mode, color) in enumerate(zip(order_modes, colors, strict=True)):
            mode_column = data.convergence_modes.index(mode)
            error_axis.loglog(
                spacings,
                convergence.relative_errors.magnitude[:, mode_column],
                "-",
                color=color,
                marker="o",
                markevery=marker_interval,
                markersize=4,
                label=rf"mode $n={mode}$",
            )
            order_axis.plot(
                point_counts[1:],
                convergence.observed_orders.magnitude[:, column],
                "-",
                color=color,
                marker="o",
                markevery=marker_interval,
                markersize=4,
                label=rf"mode $n={mode}$",
            )
        reference = spacings**2
        reference *= 0.8 * error_axis.get_ylim()[1] / reference[0]
        error_axis.loglog(
            spacings,
            reference,
            "k--",
            alpha=0.65,
            label=r"$O((\Delta x)^2)$",
        )
        error_axis.invert_xaxis()
        error_axis.set(
            title="Fixed-mode eigenvalue convergence",
            xlabel=r"grid spacing $\Delta x$",
            ylabel="relative energy error",
        )
        error_axis.grid(True, which="both", alpha=0.25)
        error_axis.legend(frameon=False)
        order_axis.axhline(2.0, color="black", linestyle="--", alpha=0.65)
        order_axis.set(
            title="Observed order between refinements",
            xlabel=r"closed-interval grid points $N$",
            ylabel="observed order",
        )
        order_axis.grid(True, alpha=0.25)
        order_axis.legend(frameon=False)
        figure.suptitle(
            "Particle-in-a-box grid-refinement series",
            fontsize=14,
            fontweight="bold",
        )
        return figure


class _ConvergenceModeSweepFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        data = self._data
        convergence = data.convergence
        selected_indices = np.unique(
            np.linspace(
                0,
                len(data.convergence_interior_points) - 1,
                7,
                dtype=np.int64,
            )
        )
        figure, axis = plt.subplots(figsize=(7.6, 4.8), constrained_layout=True)
        colors = plt.colormaps["viridis"](np.linspace(0.08, 0.9, selected_indices.size))
        for index, color in zip(selected_indices, colors, strict=True):
            axis.semilogy(
                data.convergence_modes,
                convergence.relative_errors.magnitude[index],
                "o-",
                color=color,
                label=rf"$N={data.convergence_interior_points[index] + 2}$",
            )
        axis.set(
            title="Error across mode index and grid resolution",
            xlabel="fixed continuum mode index $n$",
            ylabel="relative energy error",
            xticks=data.convergence_modes,
        )
        axis.grid(True, which="both", alpha=0.25)
        axis.legend(frameon=False, ncol=2)
        return figure


class _HigherEigenpairSweepFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        sweep = self._data.eigenpair_sweep
        dimensions = sweep.definition.interior_points
        selected = np.unique(np.linspace(0, len(dimensions) - 1, 7, dtype=np.int64))
        colors = plt.colormaps["viridis"](np.linspace(0.08, 0.9, selected.size))
        figure, axes = plt.subplots(1, 2, figsize=(11.8, 4.5), constrained_layout=True)
        energy_axis, vector_axis = axes
        floor = np.finfo(np.float64).eps
        for grid_index, color in zip(selected, colors, strict=True):
            start = sweep.grid_offsets[int(grid_index)]
            stop = sweep.grid_offsets[int(grid_index) + 1]
            fraction = sweep.fractional_mode_indices.magnitude[start:stop]
            energy_axis.semilogy(
                fraction,
                sweep.relative_energy_errors.magnitude[start:stop],
                "-",
                color=color,
                label=rf"$N={dimensions[int(grid_index)] + 2}$",
            )
            vector_axis.semilogy(
                fraction,
                np.maximum(sweep.nodal_overlap_defects.magnitude[start:stop], floor),
                ".",
                color=color,
                label=rf"$N={dimensions[int(grid_index)] + 2}$",
            )
        energy_axis.set(
            title="Eigenvalue dispersion across the spectrum",
            xlabel=r"fractional mode index $n/(N-1)$",
            ylabel="relative energy error",
        )
        vector_axis.set(
            title="Agreement with continuum sine at grid nodes",
            xlabel=r"fractional mode index $n/(N-1)$",
            ylabel=r"nodal overlap defect $1-|\langle v,s_n\rangle|$",
        )
        for axis in axes:
            axis.grid(True, which="both", alpha=0.25)
            axis.legend(frameon=False)
        figure.suptitle(
            "Higher-index particle-in-a-box eigenpair sweep",
            fontsize=14,
            fontweight="bold",
        )
        return figure


class _HigherModeConvergenceFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        sweep = self._data.eigenpair_sweep
        fixed_modes = sweep.definition.fixed_modes
        colors = plt.colormaps["tab10"](np.linspace(0.0, 0.8, len(fixed_modes)))
        figure, axes = plt.subplots(1, 2, figsize=(11.5, 4.5), constrained_layout=True)
        error_axis, order_axis = axes
        for mode, color in zip(fixed_modes, colors, strict=True):
            convergence = sweep.fixed_mode_convergence(mode)
            dimensions = np.asarray(
                tuple(
                    value for value in sweep.definition.interior_points if mode <= value
                ),
                dtype=np.int64,
            )
            marker_interval = max(dimensions.size // 12, 1)
            error_axis.loglog(
                convergence.spacings.magnitude,
                convergence.relative_errors.magnitude[:, 0],
                "-o",
                color=color,
                markevery=marker_interval,
                markersize=4,
                label=rf"$n={mode}$",
            )
            order_axis.plot(
                dimensions[1:] + 2,
                convergence.observed_orders.magnitude[:, 0],
                "-o",
                color=color,
                markevery=marker_interval,
                markersize=4,
                label=rf"$n={mode}$",
            )
        reference_spacings = sweep.spacings.magnitude
        reference = reference_spacings**2
        reference *= 0.8 * error_axis.get_ylim()[1] / reference[0]
        error_axis.loglog(
            reference_spacings,
            reference,
            "k--",
            alpha=0.65,
            label=r"$O((\Delta x)^2)$",
        )
        error_axis.invert_xaxis()
        error_axis.set(
            title="Fixed higher-mode refinement",
            xlabel=r"grid spacing $\Delta x$",
            ylabel="relative energy error",
        )
        order_axis.axhline(2.0, color="black", linestyle="--", alpha=0.65)
        order_axis.set(
            title="Observed order between refinements",
            xlabel=r"closed-interval grid points $N$",
            ylabel="observed order",
        )
        for axis in axes:
            axis.grid(True, which="both", alpha=0.25)
            axis.legend(frameon=False)
        figure.suptitle(
            "Convergence of fixed higher eigenvalues",
            fontsize=14,
            fontweight="bold",
        )
        return figure
