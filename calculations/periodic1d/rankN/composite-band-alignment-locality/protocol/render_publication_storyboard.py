#!/usr/bin/env python3
"""Render publication-oriented rank-N storyboard figures from the admitted cache.

The cache is integrity-admitted but unsealed and not independently verified in full.
These figures are iterative presentation prototypes, not publication acceptance.
"""

from __future__ import annotations

import math
import sys
from collections.abc import Callable
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.colors import LogNorm
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

PROTOCOL = Path(__file__).resolve().parent
CALCULATION = PROTOCOL.parent
OUTPUT = PROTOCOL / "figures" / "storyboard"
sys.path.insert(0, str(CALCULATION))

from analysis.development.cache import (  # noqa: E402
    HigherRankDevelopmentAdmittedCacheReader,
    HigherRankDevelopmentCacheReadRequest,
)
from analysis.development.plots import (  # noqa: E402
    HigherRankDevelopmentFigureData,
    HigherRankDevelopmentFigureDataConstructor,
    HigherRankDevelopmentFigureDataRequest,
)

PLOT_FLOOR = 1.0e-18
ANCHOR_RANK = 8
ANCHOR_DEPTH = 4
GAUGE_LABELS = ("identity", "global", "pointwise", "oracle")
GAUGE_COLORS = ("#202020", "#0072B2", "#009E73", "#D55E00")
GAUGE_MARKERS = ("o", "s", "^", "D")
DEPTH_COLORS = ("#0072B2", "#009E73", "#E69F00", "#D55E00")
RANK_MARKERS = ("o", "s", "^", "D")
STORYBOARD_STEMS = (
    "01-alignment-information-hierarchy",
    "02-rank-depth-scaling",
    "03-locality-and-support-consequences",
    "04-separated-error-channels",
    "05-claim-operands-and-unresolved-boundary",
    "06-numerical-controls",
)

STYLE = {
    "font.family": "DejaVu Sans",
    "font.size": 8.2,
    "axes.titlesize": 9.0,
    "axes.labelsize": 8.6,
    "axes.linewidth": 0.75,
    "xtick.labelsize": 7.6,
    "ytick.labelsize": 7.6,
    "legend.fontsize": 7.0,
    "lines.linewidth": 1.45,
    "lines.markersize": 4.0,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.facecolor": "white",
}


def _data() -> HigherRankDevelopmentFigureData:
    cache = HigherRankDevelopmentAdmittedCacheReader(
        HigherRankDevelopmentCacheReadRequest(
            cache_directory=CALCULATION / "results" / "development-cache"
        )
    ).execute()
    return HigherRankDevelopmentFigureDataConstructor(
        HigherRankDevelopmentFigureDataRequest(cache.calculation_results)
    ).execute()


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


def _grid(axis: Axes, *, logarithmic: bool = False) -> None:
    axis.grid(which="both" if logarithmic else "major", alpha=0.20, linewidth=0.55)


def _save(figure: Figure, stem: str) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    metadata = {
        "Title": stem.replace("-", " ").title(),
        "Subject": (
            "Calculated integrity-admitted unsealed design prototype; "
            "not independently verified in full"
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


def _floored(values: np.ndarray) -> np.ndarray:
    return np.maximum(np.asarray(values, dtype=np.float64), PLOT_FLOOR)


def _anchor_indices(data: HigherRankDevelopmentFigureData) -> tuple[int, int]:
    return (
        data.retained_ranks.index(ANCHOR_RANK),
        data.circuit_depths.index(ANCHOR_DEPTH),
    )


def _gauge_legend() -> tuple[Line2D, ...]:
    return tuple(
        Line2D(
            [],
            [],
            color=color,
            marker=marker,
            label=label,
        )
        for label, color, marker in zip(
            GAUGE_LABELS, GAUGE_COLORS, GAUGE_MARKERS, strict=True
        )
    )


def _case_legend(data: HigherRankDevelopmentFigureData) -> tuple[Line2D, ...]:
    rank_handles = tuple(
        Line2D(
            [],
            [],
            color="0.25",
            marker=marker,
            linestyle="none",
            label=rf"$r={rank}$",
        )
        for rank, marker in zip(data.retained_ranks, RANK_MARKERS, strict=True)
    )
    depth_handles = tuple(
        Line2D(
            [],
            [],
            color=color,
            linewidth=2.0,
            label=rf"$L={depth}$",
        )
        for depth, color in zip(data.circuit_depths, DEPTH_COLORS, strict=True)
    )
    return (*rank_handles, *depth_handles)


def _categorical_case_scatter(
    axis: Axes,
    values: np.ndarray,
    data: HigherRankDevelopmentFigureData,
    *,
    mark_exact_zeros: bool = False,
) -> None:
    for gauge_index in range(len(data.gauge_alignment_names)):
        for rank_index, marker in enumerate(RANK_MARKERS):
            for depth_index, color in enumerate(DEPTH_COLORS):
                case_index = rank_index * len(data.circuit_depths) + depth_index
                offset = 0.018 * (case_index - 7.5)
                value = values[rank_index, depth_index, gauge_index]
                if math.isfinite(float(value)):
                    exact_zero = mark_exact_zeros and float(value) == 0.0
                    if exact_zero:
                        axis.scatter(
                            gauge_index + offset,
                            PLOT_FLOOR,
                            color=color,
                            marker="x",
                            linewidth=0.8,
                            s=25,
                            zorder=3,
                        )
                    else:
                        axis.scatter(
                            gauge_index + offset,
                            max(float(value), PLOT_FLOOR),
                            color=color,
                            marker=marker,
                            edgecolor="white",
                            linewidth=0.35,
                            s=25,
                            zorder=3,
                        )
    axis.set_xticks(range(len(GAUGE_LABELS)), GAUGE_LABELS, rotation=15)
    axis.set_yscale("log")
    _grid(axis, logarithmic=True)


def _render_alignment_information(data: HigherRankDevelopmentFigureData) -> None:
    final = 1
    figure, axes = plt.subplots(2, 2, figsize=(7.15, 5.5), constrained_layout=True)
    fields = (
        (
            data.frame_recovery[:, :, final, :],
            "Reference-frame recovery",
            r"normalized frame residual",
        ),
        (
            data.support_two_tail[:, :, final, :],
            r"Hopping tail beyond $S=2$",
            r"normalized omitted-block norm",
        ),
        (
            data.support_two_total_spectrum[:, :, final, :],
            r"Total spectral consequence at $S=2$",
            r"normalized maximum spectral error",
        ),
        (
            data.operator_recovery[:, :, final, :],
            "Direct represented-field integrity",
            r"normalized operator reconstruction defect",
        ),
    )
    for index, (values, title, ylabel) in enumerate(fields):
        axis = axes.ravel()[index]
        _categorical_case_scatter(
            axis,
            values,
            data,
            mark_exact_zeros=index == 3,
        )
        axis.set_title(title)
        axis.set_ylabel(ylabel)
        _panel(axis, f"({chr(ord('a') + index)})")
    axes[1, 1].text(
        0.34,
        0.12,
        r"$\times$: exact zero placed at display floor",
        transform=axes[1, 1].transAxes,
        fontsize=6.4,
    )
    figure.legend(
        handles=_case_legend(data),
        loc="outside upper center",
        ncol=8,
        frameon=False,
    )
    _save(figure, "01-alignment-information-hierarchy")


def _annotated_heatmap(
    figure: Figure,
    axis: Axes,
    values: np.ndarray,
    data: HigherRankDevelopmentFigureData,
    *,
    title: str,
    colorbar_label: str,
    threshold: float | None = None,
    condition: Callable[[float], bool] | None = None,
) -> None:
    finite = values[np.isfinite(values)]
    positive = finite[finite > 0.0]
    minimum = max(float(np.min(positive)) if positive.size else PLOT_FLOOR, PLOT_FLOOR)
    maximum = max(float(np.max(finite)) if finite.size else minimum, minimum * 10.0)
    image = axis.imshow(
        _floored(values),
        origin="lower",
        aspect="auto",
        cmap="cividis",
        norm=LogNorm(vmin=minimum, vmax=maximum),
    )
    axis.set_xticks(
        range(len(data.circuit_depths)),
        tuple(str(depth) for depth in data.circuit_depths),
    )
    axis.set_yticks(
        range(len(data.retained_ranks)),
        tuple(str(rank) for rank in data.retained_ranks),
    )
    axis.set_xlabel("circuit depth $L$")
    axis.set_ylabel("retained rank $r$")
    axis.set_title(title)
    for row in range(values.shape[0]):
        for column in range(values.shape[1]):
            value = float(values[row, column])
            if math.isfinite(value):
                axis.text(
                    column,
                    row,
                    f"{value:.1e}",
                    ha="center",
                    va="center",
                    fontsize=5.6,
                    color="white" if value < math.sqrt(minimum * maximum) else "black",
                )
                if threshold is not None and condition is not None:
                    passed = condition(value)
                    axis.add_patch(
                        Rectangle(
                            (column - 0.48, row - 0.48),
                            0.96,
                            0.96,
                            fill=False,
                            edgecolor="#009E73" if passed else "#D55E00",
                            linewidth=1.3,
                        )
                    )
    colorbar = figure.colorbar(image, ax=axis, pad=0.02)
    colorbar.set_label(colorbar_label)


def _render_rank_depth_scaling(data: HigherRankDevelopmentFigureData) -> None:
    final = 1
    identity = 0
    global_unitary = 1
    pointwise = 2
    figure, axes = plt.subplots(2, 2, figsize=(7.15, 5.55), constrained_layout=True)
    panels = (
        (
            data.support_two_tail[:, :, final, identity],
            r"Identity hopping tail beyond $S=2$",
            "normalized omitted-block norm",
        ),
        (
            data.support_two_total_spectrum[:, :, final, identity],
            r"Identity total spectral error at $S=2$",
            "normalized spectral error",
        ),
        (
            data.frame_recovery[:, :, final, global_unitary],
            "Global-unitary frame residual",
            "normalized frame residual",
        ),
        (
            data.support_two_total_spectrum[:, :, final, pointwise],
            r"Pointwise control at $S=2$",
            "normalized spectral error",
        ),
    )
    for index, (values, title, label) in enumerate(panels):
        axis = axes.ravel()[index]
        _annotated_heatmap(
            figure,
            axis,
            values,
            data,
            title=title,
            colorbar_label=label,
        )
        _panel(axis, f"({chr(ord('a') + index)})")
    _save(figure, "02-rank-depth-scaling")


def _render_locality_support(data: HigherRankDevelopmentFigureData) -> None:
    rank_index, depth_index = _anchor_indices(data)
    supports = np.asarray(data.support_radii, dtype=np.float64)
    translations = np.abs(data.block_translations)
    positive_translations = np.unique(translations)
    figure, axes = plt.subplots(2, 2, figsize=(7.15, 5.5), constrained_layout=True)

    for gauge_index, (label, color, marker) in enumerate(
        zip(GAUGE_LABELS, GAUGE_COLORS, GAUGE_MARKERS, strict=True)
    ):
        axes[0, 0].semilogy(
            supports,
            _floored(data.support_tail[rank_index, depth_index, gauge_index]),
            color=color,
            marker=marker,
            label=label,
        )
        block_values = data.block_norms[rank_index, depth_index, gauge_index]
        collapsed = np.asarray(
            [
                np.max(block_values[np.isclose(translations, translation)])
                for translation in positive_translations
            ],
            dtype=np.float64,
        )
        axes[0, 1].semilogy(
            positive_translations,
            _floored(collapsed),
            color=color,
            marker=marker,
            markevery=max(1, len(positive_translations) // 12),
            label=label,
        )
        axes[1, 0].semilogy(
            supports,
            _floored(data.total_operator[rank_index, depth_index, gauge_index]),
            color=color,
            marker=marker,
            label=label,
        )
        axes[1, 1].semilogy(
            supports,
            _floored(data.total_spectrum[rank_index, depth_index, gauge_index]),
            color=color,
            marker=marker,
            label=label,
        )

    axes[0, 0].set_title("Unchanged-coefficient hopping tails")
    axes[0, 0].set_ylabel("normalized omitted-block norm")
    axes[0, 1].set_title("Fourier block-power profile")
    axes[0, 1].set_ylabel("normalized block norm")
    axes[0, 1].axvline(2.0, color="0.35", linestyle="--", label="reference support")
    axes[1, 0].set_title("Total operator consequence")
    axes[1, 0].set_ylabel("normalized maximum operator error")
    axes[1, 1].set_title("Total spectral consequence")
    axes[1, 1].set_ylabel("normalized maximum spectral error")
    for axis in axes.ravel():
        axis.set_xlabel("cutoff $S$" if axis is not axes[0, 1] else r"$|R|$")
        _grid(axis, logarithmic=True)
    for index, axis in enumerate(axes.ravel()):
        _panel(axis, f"({chr(ord('a') + index)})")
    figure.legend(
        handles=_gauge_legend(),
        loc="outside upper center",
        ncol=4,
        frameon=False,
    )
    _save(figure, "03-locality-and-support-consequences")


def _render_error_channels(data: HigherRankDevelopmentFigureData) -> None:
    rank_index, depth_index = _anchor_indices(data)
    supports = np.asarray(data.support_radii, dtype=np.float64)
    figure, axes = plt.subplots(2, 2, figsize=(7.15, 5.55), constrained_layout=True)
    for gauge_index, axis in enumerate(axes.ravel()):
        interpolation = float(
            data.interpolation_spectrum[rank_index, depth_index, gauge_index]
        )
        axis.semilogy(
            supports,
            np.full_like(supports, max(interpolation, PLOT_FLOOR)),
            color="#0072B2",
            linestyle=":",
            label="interpolation",
        )
        axis.semilogy(
            supports,
            _floored(data.truncation_spectrum[rank_index, depth_index, gauge_index]),
            color="#E69F00",
            linestyle="--",
            marker="s",
            markerfacecolor="white",
            label="truncation only",
        )
        axis.semilogy(
            supports,
            _floored(data.total_spectrum[rank_index, depth_index, gauge_index]),
            color="#009E73",
            marker="o",
            label="total",
        )
        axis.set_title(GAUGE_LABELS[gauge_index])
        axis.set_xlabel("retained-support cutoff $S$")
        axis.set_ylabel("normalized maximum spectral error")
        _grid(axis, logarithmic=True)
        _panel(axis, f"({chr(ord('a') + gauge_index)})")
    figure.legend(
        handles=(
            Line2D([], [], color="#0072B2", linestyle=":", label="interpolation"),
            Line2D(
                [],
                [],
                color="#E69F00",
                linestyle="--",
                marker="s",
                markerfacecolor="white",
                label="truncation only",
            ),
            Line2D([], [], color="#009E73", marker="o", label="total"),
        ),
        loc="outside upper center",
        ncol=3,
        frameon=False,
    )
    _save(figure, "04-separated-error-channels")


def _render_claim_operands(data: HigherRankDevelopmentFigureData) -> None:
    final = 1
    identity = 0
    global_unitary = 1
    oracle = 3
    figure, axes = plt.subplots(2, 2, figsize=(7.15, 5.55), constrained_layout=True)
    panels = (
        (
            data.support_two_tail[:, :, final, identity],
            r"Identity tail at $S=2$",
            "normalized omitted-block norm",
            1.0e-6,
            lambda value: value >= 1.0e-6,
        ),
        (
            data.support_two_tail[:, :, final, oracle],
            r"Oracle tail at $S=2$",
            "normalized omitted-block norm",
            1.0e-10,
            lambda value: value <= 1.0e-10,
        ),
        (
            data.support_two_total_spectrum[:, :, final, identity],
            r"Identity total spectral error at $S=2$",
            "normalized spectral error",
            1.0e-6,
            lambda value: value >= 1.0e-6,
        ),
        (
            data.frame_recovery[:, :, final, global_unitary],
            "Global frame residual (supporting only)",
            "normalized frame residual",
            1.0e-6,
            lambda value: value >= 1.0e-6,
        ),
    )
    for index, (values, title, label, threshold, condition) in enumerate(panels):
        axis = axes.ravel()[index]
        _annotated_heatmap(
            figure,
            axis,
            values,
            data,
            title=title,
            colorbar_label=label,
            threshold=threshold,
            condition=condition,
        )
        _panel(axis, f"({chr(ord('a') + index)})")
    axes[1, 1].text(
        0.5,
        -0.27,
        "Frozen global represented-operator operand is not retained;\n"
        "the complete claim disposition remains unresolved.",
        transform=axes[1, 1].transAxes,
        ha="center",
        va="top",
        fontsize=6.4,
        color="#D55E00",
    )
    _save(figure, "05-claim-operands-and-unresolved-boundary")


def _render_numerical_controls(data: HigherRankDevelopmentFigureData) -> None:
    figure, axes = plt.subplots(2, 3, figsize=(7.15, 5.1), constrained_layout=True)
    flat_axes = axes.ravel()

    coarse = data.refinement_coarse.ravel()
    fine = data.refinement_fine.ravel()
    finite = np.isfinite(coarse) & np.isfinite(fine)
    coarse_finite = _floored(coarse[finite])
    fine_finite = _floored(fine[finite])
    lower = min(float(np.min(coarse_finite)), float(np.min(fine_finite)))
    upper = max(float(np.max(coarse_finite)), float(np.max(fine_finite)))
    flat_axes[0].loglog(
        coarse_finite,
        fine_finite,
        linestyle="none",
        marker="o",
        markersize=2.7,
        alpha=0.55,
        color="#0072B2",
    )
    flat_axes[0].plot((lower, upper), (lower, upper), color="0.25", linestyle="--")
    flat_axes[0].set_title("Paired mesh values")
    flat_axes[0].set_xlabel("coarse mesh")
    flat_axes[0].set_ylabel("fine mesh")

    utilization = data.refinement_change_over_tolerance
    maxima = np.nanmax(utilization, axis=(0, 1, 2))
    refinement_positions = np.arange(len(data.refinement_labels))
    flat_axes[1].barh(
        refinement_positions,
        maxima,
        color="#009E73",
    )
    flat_axes[1].axvline(1.0, color="0.25", linestyle="--", label="pass boundary")
    flat_axes[1].set_xscale("log")
    refinement_tick_labels = (
        "interp.\noperator",
        "interp.\nspectrum",
        "tail\n$S=2$",
        "trunc. operator\n$S=2$",
        "trunc. spectrum\n$S=2$",
        "total operator\n$S=2$",
        "total spectrum\n$S=2$",
    )
    flat_axes[1].set_yticks(refinement_positions, refinement_tick_labels)
    flat_axes[1].invert_yaxis()
    flat_axes[1].set_title("Maximum gate utilization")
    flat_axes[1].set_xlabel("change / tolerance")
    flat_axes[1].legend(frameon=False, fontsize=6.0)

    qualified_counts = np.sum(data.qualified[:, :, 1, :], axis=(0, 1))
    flat_axes[2].bar(
        np.arange(len(GAUGE_LABELS)),
        qualified_counts,
        color=GAUGE_COLORS,
    )
    flat_axes[2].set_xticks(np.arange(len(GAUGE_LABELS)), GAUGE_LABELS, rotation=20)
    flat_axes[2].set_ylim(0.0, 19.0)
    flat_axes[2].set_title("Final-mesh qualified cases")
    flat_axes[2].set_ylabel("qualified cases out of 16")
    for index, count in enumerate(qualified_counts):
        flat_axes[2].text(index, float(count) + 0.25, str(int(count)), ha="center")

    decomposition = np.nanmax(data.decomposition_defect, axis=(0, 1, 3))
    flat_axes[3].bar(
        np.arange(len(GAUGE_LABELS)),
        _floored(decomposition),
        color=GAUGE_COLORS,
    )
    flat_axes[3].set_yscale("log")
    flat_axes[3].set_xticks(np.arange(len(GAUGE_LABELS)), GAUGE_LABELS, rotation=20)
    flat_axes[3].set_title("Residual decomposition defect")
    flat_axes[3].set_ylabel("maximum normalized defect")

    pareto_counts = np.sum(data.pareto_efficient, axis=3)
    for gauge_index, (color, marker) in enumerate(
        zip(GAUGE_COLORS, GAUGE_MARKERS, strict=True)
    ):
        x = np.full(pareto_counts[:, :, gauge_index].size, gauge_index, dtype=float)
        x += np.linspace(-0.12, 0.12, x.size)
        flat_axes[4].scatter(
            x,
            pareto_counts[:, :, gauge_index].ravel(),
            color=color,
            marker=marker,
            edgecolor="white",
            linewidth=0.35,
        )
    flat_axes[4].set_xticks(np.arange(len(GAUGE_LABELS)), GAUGE_LABELS, rotation=20)
    flat_axes[4].set_title("Sampled Pareto support counts")
    flat_axes[4].set_ylabel("nondominated supports per case")

    pointwise = 2
    oracle = 3
    case_axis = np.arange(16)
    frame_difference = np.abs(
        data.frame_recovery[:, :, 1, pointwise] - data.frame_recovery[:, :, 1, oracle]
    ).ravel()
    spectrum_difference = np.abs(
        data.support_two_total_spectrum[:, :, 1, pointwise]
        - data.support_two_total_spectrum[:, :, 1, oracle]
    ).ravel()
    flat_axes[5].semilogy(
        case_axis,
        _floored(frame_difference),
        color="#0072B2",
        marker="o",
        label="frame recovery",
    )
    positive_spectrum = spectrum_difference > 0.0
    flat_axes[5].semilogy(
        case_axis[positive_spectrum],
        spectrum_difference[positive_spectrum],
        color="#D55E00",
        marker="s",
        label=r"$S=2$ spectral consequence",
    )
    flat_axes[5].scatter(
        case_axis[~positive_spectrum],
        np.full(np.sum(~positive_spectrum), PLOT_FLOOR),
        color="#D55E00",
        marker="x",
        label="exact zero (display floor)",
    )
    flat_axes[5].set_title("Pointwise–oracle agreement")
    flat_axes[5].set_xlabel("rank/depth case index")
    flat_axes[5].set_ylabel("absolute difference")
    flat_axes[5].legend(frameon=False, fontsize=6.0)

    for index, axis in enumerate(flat_axes):
        _grid(axis, logarithmic=index in {0, 1, 3, 5})
        axis.text(
            0.015,
            0.985,
            f"({chr(ord('a') + index)})",
            transform=axis.transAxes,
            fontsize=9.2,
            fontweight="bold",
            va="top",
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.82},
        )
    _save(figure, "06-numerical-controls")


def main() -> int:
    """Render the complete publication-storyboard inventory from admitted cache data."""
    data = _data()
    renderers: tuple[Callable[[HigherRankDevelopmentFigureData], None], ...] = (
        _render_alignment_information,
        _render_rank_depth_scaling,
        _render_locality_support,
        _render_error_channels,
        _render_claim_operands,
        _render_numerical_controls,
    )
    if len(renderers) != len(STORYBOARD_STEMS):
        raise RuntimeError("Storyboard renderer and filename inventories differ")
    with mpl.rc_context(STYLE):  # type: ignore[arg-type]
        for render in renderers:
            render(data)
    expected_paths = {
        OUTPUT / f"{stem}.{suffix}"
        for stem in STORYBOARD_STEMS
        for suffix in ("pdf", "png")
    }
    actual_paths = set(OUTPUT.glob("*"))
    if actual_paths != expected_paths:
        raise RuntimeError("Rendered storyboard does not match the closed inventory")
    for path in sorted(expected_paths):
        print(path.relative_to(CALCULATION))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
