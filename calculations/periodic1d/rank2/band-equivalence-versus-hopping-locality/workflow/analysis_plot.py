"""Plot validated 1-D diagnostic bundles without recomputing experiment results."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  # type: ignore[import-untyped]
from matplotlib.figure import Figure

from .analysis import DiagnosticBundle, DiagnosticTable


def _selected_truncation(
    bundle: DiagnosticBundle,
    parent_hopping_scale: float,
    amplitude: float,
) -> pd.DataFrame:
    table = bundle.table(DiagnosticTable.TRUNCATION_CONSEQUENCES)
    selected = table.loc[
        np.isclose(table["parent_hopping_scale"], parent_hopping_scale)
        & np.isclose(table["amplitude"], amplitude)
    ].copy()
    if selected.empty:
        raise ValueError("no truncation rows match the selected parent and amplitude")
    return selected.sort_values("maximum_range", kind="mergesort")


def plot_hamiltonian_and_spectral_errors(
    bundle: DiagnosticBundle,
    *,
    parent_hopping_scale: float = 1.0,
    amplitude: float = math.pi / 4.0,
) -> Figure:
    """Compare matrix, spectral, locality, and perturbation-bound channels."""
    if type(bundle) is not DiagnosticBundle:
        raise TypeError("bundle must be a DiagnosticBundle")
    selected = _selected_truncation(bundle, parent_hopping_scale, amplitude)
    ranges = selected["maximum_range"].to_numpy(dtype=np.int64)
    root_rank = math.sqrt(2.0)

    figure, axes = plt.subplots(2, 2, figsize=(10.5, 7.5), constrained_layout=True)

    axes[0, 0].semilogy(
        ranges,
        selected["comparison_maximum_total_hamiltonian_error"],
        "o-",
        label="Hamiltonian",
    )
    axes[0, 0].semilogy(
        ranges,
        selected["comparison_maximum_total_band_error"],
        "s-",
        label="bands",
    )
    axes[0, 0].set_title("(a) maximum total error")
    axes[0, 0].set_ylabel("normalized error")
    axes[0, 0].legend(frameon=False)

    axes[0, 1].semilogy(
        ranges,
        selected["comparison_maximum_truncation_hamiltonian_error"],
        "o-",
        label="Hamiltonian",
    )
    axes[0, 1].semilogy(
        ranges,
        selected["comparison_maximum_truncation_band_error"],
        "s-",
        label="bands",
    )
    axes[0, 1].set_title("(b) deliberate truncation")
    axes[0, 1].legend(frameon=False)

    axes[1, 0].loglog(
        np.sqrt(selected["reference_ordinary_omitted_power"]),
        selected["reference_rms_truncation_hamiltonian_error"],
        "o",
        label="reference",
    )
    axes[1, 0].loglog(
        np.sqrt(selected["comparison_ordinary_omitted_power"]),
        selected["comparison_rms_truncation_hamiltonian_error"],
        "s",
        label="comparison",
    )
    finite_values = np.concatenate(
        (
            np.sqrt(selected["reference_ordinary_omitted_power"].to_numpy()),
            np.sqrt(selected["comparison_ordinary_omitted_power"].to_numpy()),
        )
    )
    lower = float(np.min(finite_values[finite_values > 0.0]))
    upper = float(np.max(finite_values))
    axes[1, 0].plot([lower, upper], [lower, upper], "k--", linewidth=1.0)
    axes[1, 0].set_title("(c) Parseval check")
    axes[1, 0].set_xlabel(r"$\sqrt{P_{\mathrm{omitted}}}$")
    axes[1, 0].set_ylabel("RMS Hamiltonian error")
    axes[1, 0].legend(frameon=False)

    hamiltonian_bound = (
        root_rank * selected["comparison_maximum_total_hamiltonian_error"].to_numpy()
    )
    spectral = selected["comparison_maximum_total_band_error"].to_numpy()
    ratio = np.divide(
        spectral,
        hamiltonian_bound,
        out=np.zeros_like(spectral),
        where=hamiltonian_bound > 0.0,
    )
    axes[1, 1].plot(ranges, ratio, "o-")
    axes[1, 1].axhline(1.0, color="black", linestyle="--", linewidth=1.0)
    axes[1, 1].set_ylim(bottom=0.0)
    axes[1, 1].set_title("(d) spectral/Frobenius bound ratio")
    axes[1, 1].set_xlabel("maximum retained range")
    axes[1, 1].set_ylabel(r"$\epsilon_{\lambda,\max}/(\sqrt{2}\delta_{F,\max})$")

    for axis in axes.flat:
        axis.grid(alpha=0.2)
        if axis is not axes[1, 0]:
            axis.set_xlabel("maximum retained range")

    figure.suptitle(
        rf"Hamiltonian and spectral diagnostics: $\rho={parent_hopping_scale:g}$, "
        rf"$a={amplitude:.6g}$"
    )
    return figure


def plot_frame_and_sewing_diagnostics(bundle: DiagnosticBundle) -> Figure:
    """Plot gap, Procrustes, Wilson-like closure, and frame checks."""
    if type(bundle) is not DiagnosticBundle:
        raise TypeError("bundle must be a DiagnosticBundle")
    summary = bundle.table(DiagnosticTable.PARENT_FAMILY_SUMMARY)
    scales = summary["parent_hopping_scale"].to_numpy()

    figure, axes = plt.subplots(2, 2, figsize=(10.5, 7.5), constrained_layout=True)
    axes[0, 0].plot(scales, summary["minimum_sampled_external_gap"], "o-")
    axes[0, 0].set_title("(a) sampled external gap")
    axes[0, 0].set_ylabel(r"gap / $E_{\mathrm{ref}}$")

    axes[0, 1].plot(
        scales,
        summary["minimum_sampled_transport_singular_value"],
        "o-",
        label="minimum singular value",
    )
    axes[0, 1].set_title("(b) transport conditioning")
    axes[0, 1].set_ylabel("unitless")

    axes[1, 0].plot(
        scales,
        summary["closure_holonomy_phase_0"],
        "o-",
        label="phase 1",
    )
    axes[1, 0].plot(
        scales,
        summary["closure_holonomy_phase_1"],
        "s-",
        label="phase 2",
    )
    axes[1, 0].set_title("(c) closure holonomy phase set")
    axes[1, 0].set_ylabel("radian")
    axes[1, 0].legend(frameon=False)

    axes[1, 1].semilogy(
        scales,
        summary["maximum_transport_procrustes_residual"],
        "o-",
        label="Procrustes residual",
    )
    axes[1, 1].semilogy(
        scales,
        summary["maximum_transport_unitarity_defect"],
        "s-",
        label="transport unitarity residual",
    )
    axes[1, 1].semilogy(
        scales,
        summary["periodic_closure_defect"],
        "^-",
        label="periodic closure residual",
    )
    axes[1, 1].set_title("(d) frame and sewing diagnostics")
    axes[1, 1].set_ylabel("declared metric")
    axes[1, 1].legend(frameon=False)

    for axis in axes.flat:
        axis.set_xlabel(r"parent hopping scale $\rho$")
        axis.grid(alpha=0.2)
    return figure


def plot_sampled_range_decisions(
    bundle: DiagnosticBundle,
    *,
    tolerance: float = 1.0e-8,
) -> Figure:
    """Plot separate sampled matrix and spectral range decisions."""
    if type(bundle) is not DiagnosticBundle:
        raise TypeError("bundle must be a DiagnosticBundle")
    if type(tolerance) is not float or tolerance <= 0.0:
        raise ValueError("tolerance must be a positive built-in float")
    decisions = bundle.sampled_range_decisions((tolerance,))
    columns = (
        "band_sampled_range_inflation",
        "hamiltonian_sampled_range_inflation",
        "comparison_band_first_passing_range",
        "comparison_hamiltonian_first_passing_range",
    )
    numeric = decisions.copy()
    for column in columns:
        numeric[column] = pd.to_numeric(numeric[column], errors="coerce")
    if bool(numeric.loc[:, list(columns)].isna().any(axis=None)):
        raise ValueError(
            "selected tolerance contains unresolved sampled range decisions"
        )
    numeric["comparison_hamiltonian_minus_band_range"] = (
        numeric["comparison_hamiltonian_first_passing_range"]
        - numeric["comparison_band_first_passing_range"]
    )

    figure, axes = plt.subplots(2, 2, figsize=(10.5, 7.5), constrained_layout=True)
    specifications = (
        ("band_sampled_range_inflation", "(a) spectral range inflation", "viridis"),
        (
            "hamiltonian_sampled_range_inflation",
            "(b) Hamiltonian range inflation",
            "viridis",
        ),
        (
            "comparison_band_first_passing_range",
            "(c) comparison spectral cutoff",
            "viridis",
        ),
        (
            "comparison_hamiltonian_minus_band_range",
            "(d) comparison Hamiltonian minus spectral cutoff",
            "coolwarm",
        ),
    )
    for axis, (column, title, color_map) in zip(axes.flat, specifications, strict=True):
        grid = numeric.pivot(
            index="parent_hopping_scale", columns="amplitude", values=column
        )
        values = grid.to_numpy(dtype=np.float64)
        limit = float(np.max(np.abs(values)))
        image_options: dict[str, float | str] = {}
        if color_map == "coolwarm":
            image_options = {"vmin": -max(1.0, limit), "vmax": max(1.0, limit)}
        image = axis.imshow(
            values,
            aspect="auto",
            origin="lower",
            extent=(
                float(grid.columns.min()),
                float(grid.columns.max()),
                float(grid.index.min()),
                float(grid.index.max()),
            ),
            interpolation="nearest",
            cmap=color_map,
            **image_options,
        )
        axis.set_title(title)
        axis.set_xlabel(r"rotation amplitude $a$")
        axis.set_ylabel(r"parent hopping scale $\rho$")
        figure.colorbar(image, ax=axis, label="sampled range units")
    figure.suptitle(rf"First sampled passing ranges at $\tau={tolerance:.0e}$")
    return figure


def save_figure(figure: Figure, output_stem: Path) -> tuple[Path, Path]:
    """Write one figure as PDF and PNG and return both paths."""
    if type(figure) is not Figure:
        raise TypeError("figure must be a matplotlib Figure")
    if not isinstance(output_stem, Path):
        raise TypeError("output_stem must be a pathlib.Path")
    pdf = output_stem.with_suffix(".pdf")
    png = output_stem.with_suffix(".png")
    figure.savefig(pdf, bbox_inches="tight")
    figure.savefig(png, dpi=220, bbox_inches="tight")
    return pdf, png


__all__ = [
    "plot_frame_and_sewing_diagnostics",
    "plot_hamiltonian_and_spectral_errors",
    "plot_sampled_range_decisions",
    "save_figure",
]
