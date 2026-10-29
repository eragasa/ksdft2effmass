"""PIAB1D finite-algebra and decomposition figures."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm
from matplotlib.figure import Figure

from .base import _Piab1dFigure


class _FiniteAlgebraicDiagnosticsFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        data = self._data.finite_algebraic_diagnostics
        points = np.asarray(data.definition.interior_points) + 2
        panels = (
            (
                "Spectral consistency",
                (
                    (data.discrete_spectrum, r"$\delta_E$", "#0072B2"),
                    (data.spectral_reconstruction, r"$\delta_{rec}$", "#D55E00"),
                ),
            ),
            (
                "Retained-operator consistency",
                (
                    (data.retained_coordinates, r"$\delta_{coord}$", "#009E73"),
                    (data.retained_embedding, r"$\delta_{embed}$", "#CC79A7"),
                    (data.spectral_leakage, r"$\delta_{leak}$", "#E69F00"),
                ),
            ),
            (
                "Projector idempotency",
                ((data.projector_idempotency, r"$\delta_{proj}$", "#56B4E9"),),
            ),
        )
        figure, axes = plt.subplots(3, 1, figsize=(8.2, 9.2), constrained_layout=True)
        for axis, (title, series) in zip(axes, panels, strict=True):
            positive = np.concatenate(
                tuple(
                    values.magnitude[values.magnitude > 0.0] for values, _, _ in series
                )
            )
            floor = (
                0.5 * float(np.min(positive))
                if positive.size
                else np.finfo(np.float64).eps
            )
            for values, label, color in series:
                axis.loglog(
                    points,
                    np.maximum(values.magnitude, floor),
                    color=color,
                    linewidth=1.8,
                    label=label,
                )
            axis.set(
                title=title,
                xlabel="closed-interval grid points",
                ylabel="algebraic discrepancy",
            )
            axis.grid(True, which="both", alpha=0.25)
            axis.legend(frameon=False)
        figure.suptitle(
            "Finite spectral and reduction diagnostics",
            fontsize=15,
            fontweight="bold",
        )
        return figure


class _KineticPotentialDecompositionFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        result = self._data.kinetic_potential_decomposition
        shift = result.alternative_potential.magnitude
        maximum = float(np.max(np.abs(shift)))
        if maximum == 0.0:
            raise ValueError("decomposition shift must be nonzero")
        figure, axes = plt.subplots(1, 2, figsize=(10.8, 4.4), constrained_layout=True)
        matrix_axis, fit_axis = axes
        image = matrix_axis.imshow(
            shift,
            cmap="RdBu_r",
            norm=TwoSlopeNorm(vmin=-maximum, vcenter=0.0, vmax=maximum),
            interpolation="nearest",
        )
        matrix_axis.set(
            title="Illustrative decomposition shift",
            xlabel="retained-coordinate column",
            ylabel="retained-coordinate row",
            xticks=np.arange(shift.shape[1]),
            yticks=np.arange(shift.shape[0]),
        )
        figure.colorbar(image, ax=matrix_axis, shrink=0.82)
        labels = ("scalar", "diagonal", "tridiagonal", "real\nsymmetric")
        values = tuple(
            fit.unexplained_frobenius_norm.magnitude for fit in result.model_class_fits
        )
        bars = fit_axis.bar(
            labels,
            values,
            color=("#CC79A7", "#E69F00", "#56B4E9", "#009E73"),
        )
        fit_axis.set(
            title="Unexplained residual after model-class fit",
            xlabel="admissible model class",
            ylabel=r"$\|K-V_{class}\|_F$",
        )
        fit_axis.grid(True, axis="y", alpha=0.25)
        scale = max(values)
        for bar, value in zip(bars, values, strict=True):
            fit_axis.text(
                bar.get_x() + bar.get_width() / 2.0,
                value + 0.025 * scale,
                f"{value:.3f}",
                ha="center",
                va="bottom",
            )
        figure.suptitle(
            "Kinetic-potential decomposition under declared model classes",
            fontsize=13,
            fontweight="bold",
        )
        return figure
