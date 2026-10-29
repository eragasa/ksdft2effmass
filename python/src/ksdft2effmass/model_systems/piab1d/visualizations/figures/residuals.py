"""PIAB1D residual figures."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm
from matplotlib.figure import Figure

from .base import _Piab1dFigure


class _ResidualMatricesFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        residuals = (
            ("consistent reduction", self._data.consistent.magnitude),
            ("embedded minus parent", self._data.unmatched.magnitude),
            ("Dirichlet minus cyclic", self._data.boundary.magnitude),
        )
        maximum = max(float(np.max(np.abs(matrix))) for _, matrix in residuals)
        if maximum == 0.0:
            raise ValueError("residual rendering requires a nonzero matrix")
        normalization = TwoSlopeNorm(vmin=-maximum, vcenter=0.0, vmax=maximum)
        figure, axes = plt.subplots(1, 3, figsize=(12.0, 3.8), constrained_layout=True)
        image = None
        for axis, (title, matrix) in zip(axes, residuals, strict=True):
            image = axis.imshow(matrix, cmap="coolwarm", norm=normalization)
            axis.set_title(title)
            axis.set_xlabel("column")
            axis.set_ylabel("row")
        if image is None:
            raise RuntimeError("no residual matrix was rendered")
        figure.colorbar(image, ax=axes, shrink=0.8, label="matrix entry")
        return figure


class _OperatorResidualNormsFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        result = self._data.residual_norm_sweep
        points = np.asarray(result.definition.interior_points) + 2
        marker_interval = max(points.size // 12, 1)
        figure, axes = plt.subplots(2, 2, figsize=(11.8, 8.0), constrained_layout=True)
        series = (
            (
                "unmatched compression",
                result.unmatched,
                result.unmatched_relative,
                "#D55E00",
            ),
            (
                "boundary realization",
                result.boundary,
                result.boundary_relative,
                "#0072B2",
            ),
        )
        for label, raw, _, color in series:
            axes[0, 0].loglog(
                points,
                raw.magnitude[:, 0],
                "-o",
                color=color,
                markevery=marker_interval,
                markersize=4,
                label=label,
            )
        axes[0, 0].set(title="Raw Frobenius norms", ylabel=r"$\|R\|_F$")
        norm_labels = ("Frobenius", "spectral", "maximum absolute entry")
        for column, (axis, norm_label) in enumerate(
            zip(axes.flat[1:], norm_labels, strict=True)
        ):
            for label, _, relative, color in series:
                axis.semilogx(
                    points,
                    relative.magnitude[:, column],
                    "-o",
                    color=color,
                    markevery=marker_interval,
                    markersize=4,
                    label=label,
                )
            axis.set(title=norm_label, ylabel="same-grid norm ratio")
        for axis in axes.flat:
            axis.set_xlabel("closed-interval grid points")
            axis.grid(True, which="both", alpha=0.25)
            axis.legend(frameon=False)
        figure.suptitle(
            "Operator residuals under canonical matrix norms", fontweight="bold"
        )
        return figure


class _EigensolverResidualNormsFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        result = self._data.residual_norm_sweep
        points = np.asarray(result.definition.interior_points) + 2
        labels = ("Frobenius", "spectral", "maximum absolute entry")
        colors = ("#0072B2", "#D55E00", "#009E73")
        figure, axis = plt.subplots(figsize=(8.0, 4.8), constrained_layout=True)
        for column, (label, color) in enumerate(zip(labels, colors, strict=True)):
            axis.loglog(
                points,
                result.eigensolver_relative.magnitude[:, column],
                "-o",
                color=color,
                markevery=max(points.size // 12, 1),
                markersize=4,
                label=label,
            )
        axis.set(
            title="Discrete eigensolver residuals under canonical norms",
            xlabel="closed-interval grid points",
            ylabel="same-grid norm ratio",
        )
        axis.grid(True, which="both", alpha=0.25)
        axis.legend(frameon=False)
        axis.text(
            0.50,
            0.05,
            "Solver diagnostic only—not continuum error",
            transform=axis.transAxes,
        )
        return figure
