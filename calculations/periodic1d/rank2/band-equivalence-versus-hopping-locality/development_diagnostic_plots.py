"""Render validated development diagnostics without recomputing scientific analyses."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from development_diagnostics import (
    DiagnosticBundle,
    DiagnosticTable,
    DiagnosticTableData,
)
from matplotlib.figure import Figure


def _series(
    table: DiagnosticTableData,
    rows: tuple[tuple[str, ...], ...],
    column: str,
) -> np.ndarray:
    return np.asarray(
        tuple(table.number(row, column) for row in rows), dtype=np.float64
    )


def plot_hamiltonian_and_spectral_errors(
    bundle: DiagnosticBundle,
    *,
    parent_hopping_scale: float = 1.0,
    amplitude: float = math.pi / 4.0,
) -> Figure:
    """Compare matrix, spectral, locality, and perturbation-bound channels."""
    if type(bundle) is not DiagnosticBundle:
        raise TypeError("bundle must be a DiagnosticBundle")
    table = bundle.table(DiagnosticTable.TRUNCATION_CONSEQUENCES)
    rows = tuple(
        sorted(
            table.selected(
                parent_hopping_scale=parent_hopping_scale,
                amplitude=amplitude,
            ),
            key=lambda row: table.integer(row, "maximum_range"),
        )
    )
    if not rows:
        raise ValueError("no truncation rows match the selected parent and amplitude")
    ranges = _series(table, rows, "maximum_range")
    figure, axes = plt.subplots(2, 2, figsize=(10.5, 7.5), constrained_layout=True)
    axes[0, 0].semilogy(
        ranges,
        _series(table, rows, "comparison_maximum_total_hamiltonian_error"),
        "o-",
        label="Hamiltonian",
    )
    axes[0, 0].semilogy(
        ranges,
        _series(table, rows, "comparison_maximum_total_band_error"),
        "s-",
        label="bands",
    )
    axes[0, 0].set_title("(a) maximum total error")
    axes[0, 0].set_ylabel("normalized error")
    axes[0, 0].legend(frameon=False)
    axes[0, 1].semilogy(
        ranges,
        _series(table, rows, "comparison_maximum_truncation_hamiltonian_error"),
        "o-",
        label="Hamiltonian",
    )
    axes[0, 1].semilogy(
        ranges,
        _series(table, rows, "comparison_maximum_truncation_band_error"),
        "s-",
        label="bands",
    )
    axes[0, 1].set_title("(b) deliberate truncation")
    axes[0, 1].legend(frameon=False)
    reference_power = np.sqrt(_series(table, rows, "reference_ordinary_omitted_power"))
    comparison_power = np.sqrt(
        _series(table, rows, "comparison_ordinary_omitted_power")
    )
    axes[1, 0].loglog(
        reference_power,
        _series(table, rows, "reference_rms_truncation_hamiltonian_error"),
        "o",
        label="reference",
    )
    axes[1, 0].loglog(
        comparison_power,
        _series(table, rows, "comparison_rms_truncation_hamiltonian_error"),
        "s",
        label="comparison",
    )
    finite_values = np.concatenate((reference_power, comparison_power))
    lower = float(np.min(finite_values[finite_values > 0.0]))
    upper = float(np.max(finite_values))
    axes[1, 0].plot([lower, upper], [lower, upper], "k--", linewidth=1.0)
    axes[1, 0].set_title("(c) Parseval check")
    axes[1, 0].set_xlabel(r"$\sqrt{P_{\mathrm{omitted}}}$")
    axes[1, 0].set_ylabel("RMS Hamiltonian error")
    axes[1, 0].legend(frameon=False)
    hamiltonian_bound = math.sqrt(2.0) * _series(
        table, rows, "comparison_maximum_total_hamiltonian_error"
    )
    spectral = _series(table, rows, "comparison_maximum_total_band_error")
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
    """Plot gap, Procrustes, closure, and frame checks."""
    if type(bundle) is not DiagnosticBundle:
        raise TypeError("bundle must be a DiagnosticBundle")
    table = bundle.table(DiagnosticTable.PARENT_FAMILY_SUMMARY)
    rows = table.rows
    scales = _series(table, rows, "parent_hopping_scale")
    figure, axes = plt.subplots(2, 2, figsize=(10.5, 7.5), constrained_layout=True)
    axes[0, 0].plot(scales, _series(table, rows, "minimum_sampled_external_gap"), "o-")
    axes[0, 0].set_title("(a) sampled external gap")
    axes[0, 0].set_ylabel(r"gap / $E_{\mathrm{ref}}$")
    axes[0, 1].plot(
        scales,
        _series(table, rows, "minimum_sampled_transport_singular_value"),
        "o-",
        label="minimum singular value",
    )
    axes[0, 1].set_title("(b) transport conditioning")
    axes[0, 1].set_ylabel("unitless")
    axes[1, 0].plot(
        scales,
        _series(table, rows, "closure_holonomy_phase_0"),
        "o-",
        label="phase 1",
    )
    axes[1, 0].plot(
        scales,
        _series(table, rows, "closure_holonomy_phase_1"),
        "s-",
        label="phase 2",
    )
    axes[1, 0].set_title("(c) closure holonomy phase set")
    axes[1, 0].set_ylabel("radian")
    axes[1, 0].legend(frameon=False)
    axes[1, 1].semilogy(
        scales,
        _series(table, rows, "maximum_transport_procrustes_residual"),
        "o-",
        label="Procrustes residual",
    )
    axes[1, 1].semilogy(
        scales,
        _series(table, rows, "maximum_transport_unitarity_defect"),
        "s-",
        label="transport unitarity residual",
    )
    axes[1, 1].semilogy(
        scales,
        _series(table, rows, "periodic_closure_defect"),
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
    if type(tolerance) is not float or not math.isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("tolerance must be a finite positive built-in float")
    selected = tuple(
        decision
        for decision in bundle.sampled_range_decisions((tolerance,)).decisions
        if decision.tolerance == tolerance
    )
    scales = tuple(dict.fromkeys(item.parent_hopping_scale for item in selected))
    amplitudes = tuple(dict.fromkeys(item.amplitude for item in selected))

    def resolved(value: int | None) -> float:
        if value is None:
            raise ValueError("selected tolerance contains unresolved sampled decisions")
        return float(value)

    specifications = (
        (
            lambda item: item.band_sampled_range_inflation,
            "(a) spectral range inflation",
            "viridis",
        ),
        (
            lambda item: item.hamiltonian_sampled_range_inflation,
            "(b) Hamiltonian range inflation",
            "viridis",
        ),
        (
            lambda item: item.comparison_band_first_passing_range,
            "(c) comparison spectral cutoff",
            "viridis",
        ),
        (
            lambda item: (
                None
                if item.comparison_band_first_passing_range is None
                or item.comparison_hamiltonian_first_passing_range is None
                else item.comparison_hamiltonian_first_passing_range
                - item.comparison_band_first_passing_range
            ),
            "(d) comparison Hamiltonian minus spectral cutoff",
            "coolwarm",
        ),
    )
    figure, axes = plt.subplots(2, 2, figsize=(10.5, 7.5), constrained_layout=True)
    for axis, (project, title, color_map) in zip(
        axes.flat, specifications, strict=True
    ):
        values = np.asarray(
            [
                [
                    resolved(
                        project(
                            next(
                                item
                                for item in selected
                                if item.parent_hopping_scale == scale
                                and item.amplitude == amplitude
                            )
                        )
                    )
                    for amplitude in amplitudes
                ]
                for scale in scales
            ],
            dtype=np.float64,
        )
        limit = float(np.max(np.abs(values)))
        image_options: dict[str, float] = {}
        if color_map == "coolwarm":
            image_options = {"vmin": -max(1.0, limit), "vmax": max(1.0, limit)}
        image = axis.imshow(
            values,
            aspect="auto",
            origin="lower",
            extent=(min(amplitudes), max(amplitudes), min(scales), max(scales)),
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
