#!/usr/bin/env python3
"""Render an iterative publication-figure storyboard from development tables.

These figures are design prototypes. They do not replace complete-five-scale retained
results, independent verification, or the authenticated rendering lifecycle.
"""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.colors import BoundaryNorm
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

PROTOCOL = Path(__file__).resolve().parent
CALCULATION = PROTOCOL.parent
RESULTS = CALCULATION / "simulations" / "development" / "results"
INPUTS = CALCULATION / "simulations" / "development" / "inputs"
OUTPUT = PROTOCOL / "figures" / "storyboard"

AMPLITUDE_TICKS = (0.0, math.pi / 8.0, math.pi / 4.0)
AMPLITUDE_LABELS = ("0", r"$\pi/8$", r"$\pi/4$")
SCALES = (0.0, 0.25, 0.5, 0.75, 1.0)
SCALE_COLORS = ("#202020", "#0072B2", "#009E73", "#E69F00", "#D55E00")
SCALE_MARKERS = ("o", "s", "D", "^", "v")
ERROR_FLOOR = 1.0e-18
POWER_FLOOR = 1.0e-34
TARGET = 1.0e-8

STYLE = {
    "font.family": "DejaVu Sans",
    "font.size": 8.2,
    "axes.titlesize": 9.0,
    "axes.labelsize": 8.6,
    "axes.linewidth": 0.75,
    "xtick.labelsize": 7.7,
    "ytick.labelsize": 7.7,
    "legend.fontsize": 7.2,
    "lines.linewidth": 1.45,
    "lines.markersize": 3.8,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.facecolor": "white",
}


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def _number(row: dict[str, str], name: str) -> float:
    return float(row[name])


def _integer(row: dict[str, str], name: str) -> int:
    return int(row[name])


def _panel(axis: Axes, label: str) -> None:
    axis.text(
        -0.13,
        1.06,
        label,
        transform=axis.transAxes,
        fontsize=9.2,
        fontweight="bold",
        va="bottom",
    )


def _amplitude_axis(axis: Axes) -> None:
    axis.set_xticks(AMPLITUDE_TICKS, AMPLITUDE_LABELS)
    axis.set_xlabel(r"rotation amplitude $a$")


def _grid(axis: Axes, *, logarithmic: bool = False) -> None:
    axis.grid(which="both" if logarithmic else "major", alpha=0.20, linewidth=0.55)


def _save(figure: Figure, stem: str) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    metadata = {
        "Title": stem.replace("-", " ").title(),
        "Subject": (
            "Development-value design prototype; replace with verified "
            "complete-five-scale rendering"
        ),
    }
    figure.savefig(
        OUTPUT / f"{stem}.pdf",
        bbox_inches="tight",
        metadata=metadata,
    )
    figure.savefig(
        OUTPUT / f"{stem}.png",
        dpi=600,
        bbox_inches="tight",
        metadata=metadata,
    )
    plt.close(figure)


def _scale_legend() -> tuple[Line2D, ...]:
    return tuple(
        Line2D(
            [],
            [],
            color=color,
            marker=marker,
            linewidth=1.45,
            label=rf"$\rho={scale:g}$",
        )
        for scale, color, marker in zip(
            SCALES, SCALE_COLORS, SCALE_MARKERS, strict=True
        )
    )


def _family_rows(rows: Iterable[dict[str, str]], scale: float) -> list[dict[str, str]]:
    return sorted(
        (
            row
            for row in rows
            if math.isclose(
                _number(row, "parent_hopping_scale"),
                scale,
                rel_tol=0.0,
                abs_tol=1.0e-15,
            )
        ),
        key=lambda row: _number(row, "amplitude"),
    )


def _render_analytic_benchmark() -> None:
    analytic = _rows(INPUTS / "smooth-threshold-continuum.csv")
    amplitudes = np.asarray([_number(row, "a") for row in analytic])
    operator = np.asarray(
        [_number(row, "operator_threshold_over_sqrt_kappa") for row in analytic]
    )
    joint = np.asarray(
        [_number(row, "joint_threshold_over_sqrt_kappa") for row in analytic]
    )
    correlation = np.sqrt(np.maximum(0.0, 1.0 - operator**2))

    figure, axes = plt.subplots(1, 2, figsize=(7.15, 3.05), constrained_layout=True)
    axes[0].plot(amplitudes, correlation, color="#0072B2", label=r"$J_0(2a)$")
    axes[0].plot(
        amplitudes,
        operator,
        color="#D55E00",
        label=r"$\tau_{o,\min}/\sqrt{\kappa}$",
    )
    axes[0].plot(
        amplitudes,
        joint,
        color="#009E73",
        linestyle="--",
        label=r"$\tau_{o,\mathrm{joint}}(a;0)/\sqrt{\kappa}$",
    )
    _amplitude_axis(axes[0])
    axes[0].set_ylabel("normalized analytic quantity")
    axes[0].set_title("Exact flat-parent continuum")
    axes[0].legend(frameon=False, loc="center left")
    _grid(axes[0])
    _panel(axes[0], "(a)")

    squared_residual = operator**2
    axes[1].plot(
        squared_residual,
        squared_residual,
        color="#202020",
        linestyle="--",
        label=r"identity $P_{>0}/\kappa=\epsilon_{\min}^2/\kappa$",
    )
    sample_indices = np.linspace(0, len(amplitudes) - 1, 17, dtype=int)
    scatter = axes[1].scatter(
        squared_residual[sample_indices],
        squared_residual[sample_indices],
        c=amplitudes[sample_indices],
        cmap="cividis",
        edgecolor="white",
        linewidth=0.35,
        zorder=3,
    )
    colorbar = figure.colorbar(scatter, ax=axes[1], pad=0.02)
    colorbar.set_label(r"amplitude $a$")
    colorbar.set_ticks(AMPLITUDE_TICKS, labels=AMPLITUDE_LABELS)
    axes[1].set_xlabel(r"squared restricted residual $\epsilon_{\min}^2/\kappa$")
    axes[1].set_ylabel(r"induced non-onsite weight $P_{>0}/\kappa$")
    axes[1].set_title("Exact residual–locality identity")
    axes[1].legend(frameon=False, loc="upper left")
    axes[1].set_aspect("equal", adjustable="box")
    _grid(axes[1])
    _panel(axes[1], "(b)")
    _save(figure, "01-analytic-benchmark")


def _render_five_scale_core() -> None:
    rows = _rows(RESULTS / "parent-family-continuum.csv")
    figure, axes = plt.subplots(2, 2, figsize=(7.15, 5.65), constrained_layout=True)
    flat_axes = axes.ravel()
    for scale, color, marker in zip(SCALES, SCALE_COLORS, SCALE_MARKERS, strict=True):
        selected = _family_rows(rows, scale)
        amplitude = tuple(_number(row, "amplitude") for row in selected)
        markevery = max(1, len(selected) // 8)
        common = {
            "color": color,
            "marker": marker,
            "markevery": markevery,
            "markerfacecolor": "white",
            "markeredgewidth": 0.8,
        }
        flat_axes[0].semilogy(
            amplitude,
            np.maximum(
                tuple(_number(row, "maximum_band_defect") for row in selected),
                ERROR_FLOOR,
            ),
            **common,
        )
        flat_axes[1].plot(
            amplitude,
            tuple(
                _number(row, "minimum_operator_threshold_over_sqrt_kappa")
                for row in selected
            ),
            **common,
        )
        flat_axes[2].plot(
            amplitude,
            tuple(
                _number(row, "normalized_excess_nonzero_hopping_weight")
                for row in selected
            ),
            **common,
        )
        flat_axes[3].plot(
            tuple(
                _number(row, "normalized_squared_operator_residual") for row in selected
            ),
            tuple(
                _number(row, "normalized_excess_nonzero_hopping_weight")
                for row in selected
            ),
            **common,
        )

    flat_axes[0].set_title("Bands remain numerically indistinguishable")
    flat_axes[0].set_ylabel("maximum ordered-band defect")
    _amplitude_axis(flat_axes[0])
    _grid(flat_axes[0], logarithmic=True)

    flat_axes[1].set_title("Restricted representation mismatch grows")
    flat_axes[1].set_ylabel(r"$\epsilon_{\min}/\sqrt{\kappa_\rho}$")
    _amplitude_axis(flat_axes[1])
    _grid(flat_axes[1])

    flat_axes[2].set_title("Non-onsite hopping weight increases")
    flat_axes[2].set_ylabel(r"$[P_{>0}^{A}-P_{>0}^{H}]/\kappa_\rho$")
    _amplitude_axis(flat_axes[2])
    _grid(flat_axes[2])

    diagonal_limit = max(flat_axes[3].get_xlim()[1], flat_axes[3].get_ylim()[1])
    flat_axes[3].plot(
        (0.0, diagonal_limit),
        (0.0, diagonal_limit),
        color="0.25",
        linestyle="--",
        linewidth=1.0,
        label="flat identity",
    )
    flat_axes[3].set_title("Dispersion separates residual from locality")
    flat_axes[3].set_xlabel(r"$\epsilon_{\min}^2/\kappa_\rho$")
    flat_axes[3].set_ylabel(r"$[P_{>0}^{A}-P_{>0}^{H}]/\kappa_\rho$")
    flat_axes[3].legend(frameon=False, loc="upper left")
    _grid(flat_axes[3])

    for index, axis in enumerate(flat_axes):
        _panel(axis, f"({chr(ord('a') + index)})")
    figure.legend(
        handles=_scale_legend(),
        loc="outside upper center",
        ncol=5,
        frameon=False,
    )
    _save(figure, "02-five-scale-core-result")


def _render_locality_profiles() -> None:
    family = _rows(RESULTS / "parent-family-continuum.csv")
    tails = _rows(RESULTS / "nonflat-selected-hopping-tails.csv")
    power = _rows(RESULTS / "nonflat-hopping-power-map.csv")
    figure, axes = plt.subplots(1, 3, figsize=(7.15, 2.75), constrained_layout=True)

    for scale, color, marker in zip(SCALES, SCALE_COLORS, SCALE_MARKERS, strict=True):
        selected = _family_rows(family, scale)
        axes[0].plot(
            tuple(_number(row, "amplitude") for row in selected),
            tuple(
                _number(row, "comparison_nonzero_hopping_weight") for row in selected
            ),
            color=color,
            marker=marker,
            markevery=max(1, len(selected) // 8),
            markerfacecolor="white",
            markeredgewidth=0.8,
        )
    _amplitude_axis(axes[0])
    axes[0].set_ylabel(r"comparison non-onsite weight $P_{>0}^{A}$")
    axes[0].set_title("Family non-onsite weight")
    _grid(axes[0])
    _panel(axes[0], "(a)")

    tail_specs = (
        (0.0, "reference", "#202020", "^", True),
        (math.pi / 8.0, r"comparison, $a=\pi/8$", "#0072B2", "o", False),
        (math.pi / 4.0, r"comparison, $a=\pi/4$", "#D55E00", "s", False),
    )
    for amplitude, label, color, marker, reference in tail_specs:
        selected = sorted(
            (
                row
                for row in tails
                if math.isclose(
                    _number(row, "amplitude"),
                    amplitude,
                    rel_tol=0.0,
                    abs_tol=1.0e-15,
                )
            ),
            key=lambda row: _integer(row, "maximum_range"),
        )
        field = (
            "reference_normalized_tail_weight"
            if reference
            else "comparison_normalized_tail_weight"
        )
        axes[1].semilogy(
            tuple(_integer(row, "maximum_range") for row in selected),
            np.maximum(tuple(_number(row, field) for row in selected), POWER_FLOOR),
            color=color,
            marker=marker,
            label=label,
        )
    axes[1].set_xlabel(r"retained range $R_c$")
    axes[1].set_ylabel(r"weight outside $|R|\leq R_c$")
    axes[1].set_title(r"Cumulative tails ($\rho=1$)")
    axes[1].legend(frameon=False)
    _grid(axes[1], logarithmic=True)
    _panel(axes[1], "(b)")

    endpoint = [
        row
        for row in power
        if math.isclose(
            _number(row, "amplitude"),
            math.pi / 4.0,
            rel_tol=0.0,
            abs_tol=1.0e-15,
        )
    ]
    endpoint.sort(key=lambda row: _integer(row, "absolute_displacement"))
    displacements = tuple(_integer(row, "absolute_displacement") for row in endpoint)
    axes[2].semilogy(
        displacements,
        np.maximum(
            tuple(
                _number(row, "reference_normalized_hopping_weight") for row in endpoint
            ),
            POWER_FLOOR,
        ),
        color="#202020",
        marker="^",
        label="reference",
    )
    axes[2].semilogy(
        displacements,
        np.maximum(
            tuple(
                _number(row, "comparison_normalized_hopping_weight") for row in endpoint
            ),
            POWER_FLOOR,
        ),
        color="#D55E00",
        marker="s",
        label="comparison",
    )
    axes[2].set_xlabel(r"absolute displacement $|R|$")
    axes[2].set_ylabel("normalized block power")
    axes[2].set_title("Endpoint block power")
    axes[2].legend(frameon=False)
    _grid(axes[2], logarithmic=True)
    _panel(axes[2], "(c)")
    figure.legend(
        handles=_scale_legend(),
        loc="outside upper center",
        ncol=5,
        frameon=False,
    )
    _save(figure, "03-hopping-locality-profiles")


def _decision_rows(
    rows: Sequence[dict[str, str]], *, scale: float, tolerance: float
) -> list[dict[str, str]]:
    return sorted(
        (
            row
            for row in rows
            if math.isclose(
                _number(row, "parent_hopping_scale"),
                scale,
                rel_tol=0.0,
                abs_tol=1.0e-15,
            )
            and math.isclose(
                _number(row, "tolerance"),
                tolerance,
                rel_tol=1.0e-14,
                abs_tol=0.0,
            )
        ),
        key=lambda row: _number(row, "amplitude"),
    )


def _edges(values: Sequence[float]) -> np.ndarray:
    array = np.asarray(values, dtype=np.float64)
    midpoints = 0.5 * (array[:-1] + array[1:])
    return np.concatenate(
        (
            np.asarray([array[0] - 0.5 * (array[1] - array[0])]),
            midpoints,
            np.asarray([array[-1] + 0.5 * (array[-1] - array[-2])]),
        )
    )


def _render_equal_accuracy_range() -> None:
    rows = _rows(RESULTS / "sampled-range-decisions.csv")
    figure, axes = plt.subplots(2, 2, figsize=(7.15, 5.55), constrained_layout=True)
    for scale, color, marker in zip(SCALES, SCALE_COLORS, SCALE_MARKERS, strict=True):
        selected = _decision_rows(rows, scale=scale, tolerance=TARGET)
        amplitudes = tuple(_number(row, "amplitude") for row in selected)
        common = {
            "color": color,
            "marker": marker,
            "markevery": max(1, len(selected) // 8),
            "markerfacecolor": "white",
            "markeredgewidth": 0.8,
        }
        axes[0, 0].plot(
            amplitudes,
            tuple(
                _integer(row, "reference_band_first_passing_range") for row in selected
            ),
            **common,
        )
        axes[0, 1].plot(
            amplitudes,
            tuple(
                _integer(row, "comparison_band_first_passing_range") for row in selected
            ),
            **common,
        )
    axes[0, 0].set_title(r"Reference range at $\tau=10^{-8}$")
    axes[0, 0].set_ylabel(r"first passing cutoff $\widehat R_{c,H}^\star$")
    axes[0, 1].set_title(r"Comparison range at $\tau=10^{-8}$")
    axes[0, 1].set_ylabel(r"first passing cutoff $\widehat R_{c,A}^\star$")
    for axis in axes[0, :]:
        _amplitude_axis(axis)
        axis.set_ylim(-0.5, 16.5)
        _grid(axis)

    target_rows = [
        row
        for row in rows
        if math.isclose(_number(row, "tolerance"), TARGET, rel_tol=1.0e-14, abs_tol=0.0)
    ]
    amplitudes = sorted({_number(row, "amplitude") for row in target_rows})
    grid = np.empty((len(SCALES), len(amplitudes)), dtype=np.float64)
    for scale_index, scale in enumerate(SCALES):
        selected = _decision_rows(rows, scale=scale, tolerance=TARGET)
        grid[scale_index] = tuple(
            _integer(row, "band_sampled_range_inflation") for row in selected
        )
    maximum = int(np.max(grid))
    normalization = BoundaryNorm(np.arange(-0.5, maximum + 1.5, 1.0), ncolors=256)
    image = axes[1, 0].pcolormesh(
        _edges(tuple(4.0 * amplitude / math.pi for amplitude in amplitudes)),
        _edges(SCALES),
        grid,
        cmap="cividis",
        norm=normalization,
        shading="flat",
    )
    axes[1, 0].set_xticks((0.0, 0.5, 1.0), AMPLITUDE_LABELS)
    axes[1, 0].set_yticks(SCALES)
    axes[1, 0].set_xlabel(r"rotation amplitude $a$")
    axes[1, 0].set_ylabel(r"parent scale $\rho$")
    axes[1, 0].set_title(r"Range inflation $\Delta\widehat R_c^\star$ at $10^{-8}$")
    colorbar = figure.colorbar(image, ax=axes[1, 0], pad=0.02)
    colorbar.set_label("additional retained cells")
    colorbar.set_ticks(range(maximum + 1))

    endpoint_rows = sorted(
        (
            row
            for row in rows
            if math.isclose(
                _number(row, "parent_hopping_scale"),
                1.0,
                rel_tol=0.0,
                abs_tol=1.0e-15,
            )
            and math.isclose(
                _number(row, "amplitude"),
                math.pi / 4.0,
                rel_tol=0.0,
                abs_tol=1.0e-15,
            )
        ),
        key=lambda row: _number(row, "tolerance"),
        reverse=True,
    )
    tolerances = tuple(_number(row, "tolerance") for row in endpoint_rows)
    axes[1, 1].semilogx(
        tolerances,
        tuple(
            _integer(row, "reference_band_first_passing_range") for row in endpoint_rows
        ),
        color="#202020",
        marker="^",
        label="reference",
    )
    axes[1, 1].semilogx(
        tolerances,
        tuple(
            _integer(row, "comparison_band_first_passing_range")
            for row in endpoint_rows
        ),
        color="#D55E00",
        marker="s",
        label="comparison",
    )
    axes[1, 1].invert_xaxis()
    axes[1, 1].set_xlabel(r"sampled band-error target $\tau$")
    axes[1, 1].set_ylabel(r"first passing cutoff $\widehat R_c^\star$")
    axes[1, 1].set_title(r"Fully dispersive endpoint ($\rho=1$, $a=\pi/4$)")
    axes[1, 1].legend(frameon=False)
    axes[1, 1].set_ylim(-0.5, 16.5)
    _grid(axes[1, 1])

    for index, axis in enumerate(axes.ravel()):
        _panel(axis, f"({chr(ord('a') + index)})")
    figure.legend(
        handles=_scale_legend(),
        loc="outside upper center",
        ncol=5,
        frameon=False,
    )
    _save(figure, "04-equal-accuracy-range-inflation")


def _render_error_channels() -> None:
    rows = _rows(RESULTS / "truncation-consequences.csv")
    figure, axes = plt.subplots(2, 2, figsize=(7.15, 5.55), constrained_layout=True)
    reference_powers: list[float] = []
    for scale, color, marker in zip(SCALES, SCALE_COLORS, SCALE_MARKERS, strict=True):
        selected = [
            row
            for row in _family_rows(rows, scale)
            if _integer(row, "maximum_range") == 0
        ]
        amplitudes = tuple(_number(row, "amplitude") for row in selected)
        common = {
            "color": color,
            "marker": marker,
            "markevery": max(1, len(selected) // 8),
            "markerfacecolor": "white",
            "markeredgewidth": 0.8,
        }
        axes[0, 0].semilogy(
            amplitudes,
            np.maximum(
                tuple(_number(row, "comparison_nyquist_power") for row in selected),
                POWER_FLOOR,
            ),
            **common,
        )
        reference_powers.extend(
            _number(row, "reference_nyquist_power") for row in selected
        )
        axes[0, 1].semilogy(
            amplitudes,
            np.maximum(
                tuple(
                    _number(row, "comparison_maximum_interpolation_band_error")
                    for row in selected
                ),
                ERROR_FLOOR,
            ),
            **common,
        )
        endpoint = sorted(
            (
                row
                for row in _family_rows(rows, scale)
                if math.isclose(
                    _number(row, "amplitude"),
                    math.pi / 4.0,
                    rel_tol=0.0,
                    abs_tol=1.0e-15,
                )
            ),
            key=lambda row: _integer(row, "maximum_range"),
        )
        ranges = tuple(_integer(row, "maximum_range") for row in endpoint)
        axes[1, 0].semilogy(
            ranges,
            np.maximum(
                tuple(
                    _number(row, "comparison_maximum_truncation_band_error")
                    for row in endpoint
                ),
                ERROR_FLOOR,
            ),
            color=color,
            marker=marker,
            markevery=2,
            markerfacecolor="white",
            markeredgewidth=0.8,
        )
        axes[1, 1].semilogy(
            ranges,
            np.maximum(
                tuple(
                    _number(row, "comparison_maximum_total_band_error")
                    for row in endpoint
                ),
                ERROR_FLOOR,
            ),
            color=color,
            marker=marker,
            markevery=2,
            markerfacecolor="white",
            markeredgewidth=0.8,
        )

    axes[0, 0].axhspan(
        max(min(reference_powers), POWER_FLOOR),
        max(reference_powers),
        color="0.4",
        alpha=0.18,
        label="reference span",
    )
    axes[0, 0].set_title("Cyclic-to-ordinary conversion")
    axes[0, 0].set_ylabel(r"centered-Nyquist power $P_{\mathrm{Nyq}}$")
    axes[0, 0].legend(frameon=False, loc="upper left")
    axes[0, 1].set_title("Finite-interpolant discrepancy")
    axes[0, 1].set_ylabel(r"maximum spectral error / $E_{\mathrm{ref}}$")
    for axis in axes[0, :]:
        _amplitude_axis(axis)
        _grid(axis, logarithmic=True)

    axes[1, 0].set_title(r"Deliberate truncation only, $a=\pi/4$")
    axes[1, 0].set_ylabel(r"maximum spectral error / $E_{\mathrm{ref}}$")
    axes[1, 1].set_title(r"Total finite-range consequence, $a=\pi/4$")
    axes[1, 1].set_ylabel(r"maximum spectral error / $E_{\mathrm{ref}}$")
    for axis in axes[1, :]:
        axis.set_xlabel(r"retained range $R_c$")
        _grid(axis, logarithmic=True)

    for index, axis in enumerate(axes.ravel()):
        _panel(axis, f"({chr(ord('a') + index)})")
    figure.legend(
        handles=_scale_legend(),
        loc="outside upper center",
        ncol=5,
        frameon=False,
    )
    _save(figure, "05-separated-error-channels")


def _adjacent_decision_changes(
    rows: Sequence[dict[str, str]], field: str
) -> tuple[tuple[str, int], ...]:
    by_mesh: defaultdict[int, dict[tuple[float, float], int]] = defaultdict(dict)
    for row in rows:
        key = (
            _number(row, "parent_hopping_scale"),
            _number(row, "amplitude"),
        )
        by_mesh[_integer(row, "construction_mesh_size")][key] = _integer(row, field)
    meshes = sorted(by_mesh)
    changes: list[tuple[str, int]] = []
    for coarse, fine in zip(meshes[:-1], meshes[1:], strict=True):
        common = sorted(set(by_mesh[coarse]) & set(by_mesh[fine]))
        changes.append(
            (
                f"{coarse}→{fine}",
                sum(by_mesh[coarse][key] != by_mesh[fine][key] for key in common),
            )
        )
    return tuple(changes)


def _render_numerical_controls() -> None:
    summary = _rows(RESULTS / "parent-family-summary.csv")
    amplitude = _rows(RESULTS / "nonflat-amplitude-resolution.csv")
    truncation = _rows(RESULTS / "truncation-refinement.csv")
    figure, axes = plt.subplots(2, 3, figsize=(7.15, 5.1), constrained_layout=True)
    flat_axes = axes.ravel()

    scales = tuple(_number(row, "parent_hopping_scale") for row in summary)
    gaps = tuple(_number(row, "minimum_sampled_external_gap") for row in summary)
    singular = tuple(
        _number(row, "minimum_sampled_transport_singular_value") for row in summary
    )
    parent_change = tuple(
        _number(row, "maximum_final_parent_invariant_change") for row in summary
    )
    outcome_change = tuple(
        _number(row, "maximum_final_outcome_change") for row in summary
    )

    flat_axes[0].plot(scales, gaps, color="#0072B2", marker="o")
    flat_axes[0].axhline(1.0, color="#D55E00", linestyle="--", label="gate")
    flat_axes[0].set_title("External gap")
    flat_axes[0].set_ylabel(r"minimum sampled gap / $E_{\mathrm{ref}}$")
    flat_axes[0].legend(frameon=False)

    flat_axes[1].plot(scales, singular, color="#009E73", marker="s")
    flat_axes[1].axhline(0.99, color="#D55E00", linestyle="--", label="gate")
    flat_axes[1].set_title("Transport singular value")
    flat_axes[1].set_ylabel("minimum singular value")
    flat_axes[1].legend(frameon=False)

    flat_axes[2].semilogy(
        scales,
        np.maximum(parent_change, ERROR_FLOOR),
        color="#0072B2",
        marker="o",
        label="parent invariant",
    )
    flat_axes[2].semilogy(
        scales,
        np.maximum(outcome_change, ERROR_FLOOR),
        color="#D55E00",
        marker="s",
        label="outcome channel",
    )
    flat_axes[2].axhline(1.01e-8, color="0.25", linestyle="--", label="draft target")
    flat_axes[2].set_title("Final momentum changes")
    flat_axes[2].set_ylabel("maximum adjacent-mesh change")
    flat_axes[2].legend(frameon=False, fontsize=6.2)

    intervals = tuple(_integer(row, "amplitude_intervals") for row in amplitude)
    amplitude_fields = (
        ("maximum_correlation_midpoint_defect", "correlation", "#0072B2", "o"),
        (
            "maximum_operator_threshold_midpoint_defect",
            "operator threshold",
            "#D55E00",
            "s",
        ),
        (
            "maximum_nonzero_hopping_weight_midpoint_defect",
            "non-onsite weight",
            "#009E73",
            "^",
        ),
        ("maximum_hopping_block_power_midpoint_defect", "block power", "#CC79A7", "D"),
    )
    for field, label, color, marker in amplitude_fields:
        flat_axes[3].loglog(
            intervals,
            tuple(_number(row, field) for row in amplitude),
            color=color,
            marker=marker,
            label=label,
        )
    flat_axes[3].axhline(1.01e-8, color="0.25", linestyle="--", label="draft target")
    flat_axes[3].set_title("Amplitude midpoint defects")
    flat_axes[3].set_xlabel("uniform amplitude intervals")
    flat_axes[3].set_xscale("log", base=2)
    flat_axes[3].set_xticks(intervals, tuple(str(value) for value in intervals))
    flat_axes[3].set_ylabel("maximum midpoint defect")
    flat_axes[3].legend(frameon=False, fontsize=5.9)

    decision_fields = (
        ("reference_band_first_passing_range", "reference band", "#202020", "o"),
        ("comparison_band_first_passing_range", "comparison band", "#D55E00", "s"),
        (
            "reference_hamiltonian_first_passing_range",
            "reference matrix",
            "#0072B2",
            "^",
        ),
        (
            "comparison_hamiltonian_first_passing_range",
            "comparison matrix",
            "#009E73",
            "D",
        ),
    )
    x = np.arange(2)
    width = 0.18
    for offset, (field, label, color, _) in enumerate(decision_fields):
        changes = _adjacent_decision_changes(truncation, field)
        flat_axes[4].bar(
            x + (offset - 1.5) * width,
            tuple(value for _, value in changes),
            width=width,
            color=color,
            label=label,
        )
    change_labels = tuple(
        label
        for label, _ in _adjacent_decision_changes(truncation, decision_fields[0][0])
    )
    flat_axes[4].set_xticks(x, change_labels)
    flat_axes[4].set_title("Support-decision stability")
    flat_axes[4].set_xlabel("construction-mesh refinement")
    flat_axes[4].set_ylabel("changed decisions out of 165")
    flat_axes[4].set_ylim(-0.05, 1.0)
    flat_axes[4].text(
        0.5,
        0.48,
        "0 changes for every channel",
        transform=flat_axes[4].transAxes,
        ha="center",
        va="center",
        fontsize=7.0,
    )
    flat_axes[4].legend(frameon=False, fontsize=5.7)

    by_mesh: defaultdict[int, list[float]] = defaultdict(list)
    for row in truncation:
        by_mesh[_integer(row, "construction_mesh_size")].append(
            _number(row, "verification_discrepancy")
        )
    meshes = tuple(sorted(by_mesh))
    maxima = tuple(max(by_mesh[mesh]) for mesh in meshes)
    flat_axes[5].semilogy(meshes, maxima, color="#7A3E9D", marker="o")
    flat_axes[5].axhline(
        1.0e-10, color="0.25", linestyle="--", label="verification tolerance"
    )
    flat_axes[5].set_title("Independent reconstruction")
    flat_axes[5].set_xlabel("construction mesh size")
    flat_axes[5].set_ylabel("maximum verification discrepancy")
    flat_axes[5].legend(frameon=False, fontsize=6.2)

    for index, axis in enumerate(flat_axes):
        if index < 3:
            axis.set_xlabel(r"parent scale $\rho$")
        _grid(axis, logarithmic=index in {2, 3, 5})
        _panel(axis, f"({chr(ord('a') + index)})")
    _save(figure, "06-numerical-controls")


def main() -> int:
    """Render every design-prototype figure in narrative order."""
    renderers: tuple[Callable[[], None], ...] = (
        _render_analytic_benchmark,
        _render_five_scale_core,
        _render_locality_profiles,
        _render_equal_accuracy_range,
        _render_error_channels,
        _render_numerical_controls,
    )
    with mpl.rc_context(STYLE):  # type: ignore[arg-type]
        for render in renderers:
            render()
    for path in sorted(OUTPUT.glob("*")):
        print(path.relative_to(CALCULATION))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
