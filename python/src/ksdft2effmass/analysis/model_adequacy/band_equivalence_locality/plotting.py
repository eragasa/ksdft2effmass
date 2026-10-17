"""Plot replaceable bounded development diagnostics from validated JSON records."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import cast

import matplotlib
import numpy as np

from .constrained_bessel import (
    ConstrainedBesselGeometry,
    constrained_bessel_tail_diagnostic,
)
from .serialization import JsonValue

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402

_BLUE = "#0072B2"
_VERMILION = "#D55E00"
_GREEN = "#009E73"
_PURPLE = "#CC79A7"
_BLACK = "#202020"
_STYLE: dict[str, JsonValue] = {
    "font.family": "DejaVu Sans",
    "font.size": 7.5,
    "axes.titlesize": 8.5,
    "axes.labelsize": 8,
    "axes.linewidth": 0.7,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "legend.fontsize": 6.5,
    "lines.linewidth": 1.4,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.transparent": False,
}


def _panel_label(axis: plt.Axes, label: str) -> None:
    axis.text(
        -0.13,
        1.04,
        label,
        transform=axis.transAxes,
        fontsize=9,
        fontweight="bold",
        va="bottom",
        ha="left",
    )


def _save(figure: plt.Figure, stem: Path, title: str, subject: str) -> None:
    metadata = {"Title": title, "Subject": subject}
    figure.savefig(stem.with_suffix(".pdf"), bbox_inches="tight", metadata=metadata)
    figure.savefig(
        stem.with_suffix(".png"),
        dpi=600,
        bbox_inches="tight",
        metadata=metadata,
    )


def _object(value: JsonValue, name: str) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    return value


def _array(value: JsonValue, name: str) -> list[JsonValue]:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be an array")
    return value


def _number(value: JsonValue, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _integer(value: JsonValue, name: str) -> int:
    if type(value) is not int:
        raise ValueError(f"{name} must be an integer")
    return value


def _string(value: JsonValue, name: str) -> str:
    if type(value) is not str:
        raise ValueError(f"{name} must be a string")
    return value


def _load(path: Path) -> dict[str, JsonValue]:
    value = cast(JsonValue, json.loads(path.read_text()))
    return _object(value, str(path))


def _cases(document: dict[str, JsonValue]) -> list[dict[str, JsonValue]]:
    return [_object(value, "case") for value in _array(document["cases"], "cases")]


def _points(case: dict[str, JsonValue]) -> list[dict[str, JsonValue]]:
    return [_object(value, "point") for value in _array(case["points"], "points")]


def _maximum_interpolation(case: dict[str, JsonValue]) -> float:
    values: list[float] = []
    for point in _points(case):
        for representation in ("reference_interpolation", "comparison_interpolation"):
            channels = _object(point[representation], representation)
            values.append(
                _number(channels["maximum_hamiltonian"], "maximum_hamiltonian")
            )
    return max(values)


def _minimum_gap(case: dict[str, JsonValue]) -> float:
    return min(
        _number(point["minimum_sampled_external_gap"], "external isolation gap")
        for point in _points(case)
    )


def _selected_point(case: dict[str, JsonValue]) -> dict[str, JsonValue]:
    return max(
        _points(case),
        key=lambda point: (
            _number(point["parent_scale"], "parent_scale"),
            _number(point["amplitude"], "amplitude"),
        ),
    )


def _positive(value: float) -> float:
    return max(value, np.finfo(np.float64).tiny)


def _plot_mesh_summary(
    results: tuple[dict[str, JsonValue], ...],
    output: Path,
    title: str,
) -> None:
    sizes = tuple(
        _integer(result["construction_size"], "construction_size") for result in results
    )
    case_levels = tuple(_cases(result) for result in results)
    figure, axes = plt.subplots(1, 2, figsize=(11.0, 4.2), constrained_layout=True)
    for case_index, first_case in enumerate(case_levels[0]):
        cases = tuple(level[case_index] for level in case_levels)
        name = _string(first_case["name"], "case name")
        axes[0].plot(
            sizes,
            tuple(_positive(_maximum_interpolation(case)) for case in cases),
            marker="o",
            linewidth=2.0,
            label=name,
        )
        axes[1].plot(
            sizes,
            tuple(_minimum_gap(case) for case in cases),
            marker="o",
            linewidth=2.0,
            label=name,
        )
    axes[0].set_yscale("log")
    axes[0].set_xlabel("construction mesh size per coordinate, N")
    axes[0].set_ylabel("maximum interpolation matrix error / $E_{\\mathrm{ref}}$")
    axes[0].set_title("Withheld-mesh interpolation")
    axes[1].set_xlabel("construction mesh size per coordinate, N")
    axes[1].set_ylabel("sampled external isolation gap / $E_{\\mathrm{ref}}$")
    axes[1].set_title(
        "External retained-subspace isolation\n(not an internal band gap)"
    )
    for axis in axes:
        axis.set_xticks(sizes)
        axis.grid(True, alpha=0.25)
    axes[1].legend(fontsize=6.5, frameon=False)
    _panel_label(axes[0], "(a)")
    _panel_label(axes[1], "(b)")
    figure.suptitle(f"{title}: bounded mesh refinement", fontsize=11)
    _save(
        figure,
        output / "mesh-refinement-summary",
        f"{title}: bounded mesh refinement",
        "Replaceable development diagnostics; not convergence evidence",
    )
    plt.close(figure)


def _plot_scientific_story(
    smoke: dict[str, JsonValue],
    refinement: dict[str, JsonValue],
    output: Path,
    title: str,
) -> None:
    sizes = (
        _integer(smoke["construction_size"], "construction_size"),
        _integer(refinement["construction_size"], "construction_size"),
    )
    smoke_cases = _cases(smoke)
    refined_cases = _cases(refinement)
    colors = (_BLUE, _VERMILION, _GREEN, _PURPLE, _BLACK)
    figure = plt.figure(figsize=(7.2, 6.8), constrained_layout=True)
    grid = figure.add_gridspec(2, 6, height_ratios=(1.0, 1.08))
    axes = (
        figure.add_subplot(grid[0, 0:2]),
        figure.add_subplot(grid[0, 2:4]),
        figure.add_subplot(grid[0, 4:6]),
        figure.add_subplot(grid[1, 0:3]),
        figure.add_subplot(grid[1, 3:6]),
    )
    for index, (smoke_case, refined_case) in enumerate(
        zip(smoke_cases, refined_cases, strict=True)
    ):
        name = _string(smoke_case["name"], "case name")
        color = colors[index % len(colors)]
        axes[0].semilogy(
            sizes,
            (
                _positive(_maximum_interpolation(smoke_case)),
                _positive(_maximum_interpolation(refined_case)),
            ),
            marker="o",
            color=color,
            label=name,
        )
        axes[1].plot(
            sizes,
            (_minimum_gap(smoke_case), _minimum_gap(refined_case)),
            marker="o",
            color=color,
            label=name,
        )
        shells = _shell_rows(_selected_point(refined_case))
        shell_indices = [
            _integer(shell["shell_index"], "shell_index") for shell in shells
        ]
        omitted = np.asarray(
            [
                _positive(_number(shell["comparison_omitted_power"], "omitted_power"))
                for shell in shells
            ]
        )
        band_errors = np.asarray(
            [
                _positive(
                    _number(
                        _object(shell["comparison_total"], "comparison_total")[
                            "maximum_band"
                        ],
                        "maximum_band",
                    )
                )
                for shell in shells
            ]
        )
        axes[2].semilogy(
            shell_indices,
            omitted,
            marker="o",
            markersize=2.8,
            color=color,
            label=name,
        )
        axes[3].semilogy(
            shell_indices,
            band_errors,
            marker="o",
            markersize=2.8,
            color=color,
            label=name,
        )
        axes[4].loglog(
            np.sqrt(omitted),
            band_errors,
            marker="o",
            markersize=2.8,
            color=color,
            label=name,
        )
    axes[0].set_xlabel("construction mesh size $N$")
    axes[0].set_ylabel("maximum interpolation error / $E_{\\mathrm{ref}}$")
    axes[0].set_title("Withheld interpolation")
    axes[1].set_xlabel("construction mesh size $N$")
    axes[1].set_ylabel("external isolation / $E_{\\mathrm{ref}}$")
    axes[1].set_title("Retained-subspace isolation")
    axes[2].set_xlabel("physical shell cap")
    axes[2].set_ylabel("omitted power / $E_{\\mathrm{ref}}^2$")
    axes[2].set_title("Cumulative hopping tails")
    axes[3].set_xlabel("physical shell cap")
    axes[3].set_ylabel("maximum band error / $E_{\\mathrm{ref}}$")
    axes[3].set_title("Withheld spectral consequence")
    axes[4].set_xlabel(r"$\sqrt{P_{>S}}/E_{\mathrm{ref}}$")
    axes[4].set_ylabel("maximum band error / $E_{\\mathrm{ref}}$")
    axes[4].set_title("Tail power versus consequence")
    guide = np.logspace(-14, 0, 64)
    axes[4].loglog(guide, guide, "--", color="0.45", linewidth=1.0, label="$y=x$")
    for index, axis in enumerate(axes):
        axis.grid(which="both", alpha=0.2, linewidth=0.5)
        _panel_label(axis, f"({chr(97 + index)})")
    axes[0].set_xticks(sizes)
    axes[1].set_xticks(sizes)
    axes[1].text(
        0.03,
        0.05,
        "not an internal band gap",
        transform=axes[1].transAxes,
        fontsize=6.5,
    )
    axes[0].legend(frameon=False, fontsize=5.8)
    axes[2].legend(frameon=False, fontsize=5.8)
    axes[4].legend(frameon=False, fontsize=5.8)
    figure.suptitle(f"{title}: bounded scientific story", fontsize=11)
    _save(
        figure,
        output / "band-equivalence-locality-scientific-story",
        f"{title}: bounded scientific story",
        "Replaceable smoke and first-refinement diagnostics",
    )
    plt.close(figure)


def _shell_rows(point: dict[str, JsonValue]) -> list[dict[str, JsonValue]]:
    return [
        _object(value, "shell diagnostic")
        for value in _array(point["shell_diagnostics"], "shell_diagnostics")
    ]


def _plot_error_channel_decomposition(
    refinement: dict[str, JsonValue], output: Path, title: str
) -> None:
    cases = _cases(refinement)
    figure, axes = plt.subplots(
        len(cases),
        2,
        figsize=(10.5, 3.1 * len(cases)),
        squeeze=False,
        constrained_layout=True,
    )
    for row, case in enumerate(cases):
        name = _string(case["name"], "case name")
        point = _selected_point(case)
        shells = _shell_rows(point)
        shell_indices = [
            _integer(shell["shell_index"], "shell_index") for shell in shells
        ]
        interpolation = _object(
            point["comparison_interpolation"], "comparison_interpolation"
        )
        for column, channel in enumerate(("maximum_hamiltonian", "maximum_band")):
            truncation = [
                _positive(
                    _number(
                        _object(shell["comparison_truncation"], "truncation")[channel],
                        channel,
                    )
                )
                for shell in shells
            ]
            total = [
                _positive(
                    _number(
                        _object(shell["comparison_total"], "total")[channel],
                        channel,
                    )
                )
                for shell in shells
            ]
            interpolation_value = _positive(_number(interpolation[channel], channel))
            axis = axes[row, column]
            axis.axhline(
                interpolation_value,
                color=_BLACK,
                linestyle=":",
                linewidth=1.7,
                label="interpolation",
            )
            axis.plot(
                shell_indices,
                truncation,
                color=_BLUE,
                marker="o",
                markersize=2.8,
                label="deliberate truncation",
            )
            axis.plot(
                shell_indices,
                total,
                color=_VERMILION,
                linestyle="--",
                label="total versus direct",
            )
            axis.set_yscale("log")
            axis.set_xlabel("complete physical-metric shell index")
            axis.set_ylabel(f"{name}\nerror / $E_{{\\mathrm{{ref}}}}$")
            axis.grid(True, which="both", alpha=0.22, linewidth=0.5)
            axis.legend(frameon=False)
    axes[0, 0].set_title("Maximum Hamiltonian error", fontweight="bold")
    axes[0, 1].set_title("Maximum sorted-band error", fontweight="bold")
    for row in range(len(cases)):
        _panel_label(axes[row, 0], f"({chr(97 + 2 * row)})")
        _panel_label(axes[row, 1], f"({chr(98 + 2 * row)})")
    figure.suptitle(
        f"{title}: three-channel error decomposition\n"
        "refined-mesh endpoint comparison representation",
        fontsize=11,
    )
    _save(
        figure,
        output / "three-channel-error-decomposition",
        f"{title}: three-channel error decomposition",
        "Interpolation, deliberate truncation, and total error remain separate",
    )
    plt.close(figure)


def _plot_shell_profiles(
    smoke: dict[str, JsonValue],
    refinement: dict[str, JsonValue],
    output: Path,
    title: str,
) -> None:
    smoke_cases = _cases(smoke)
    refined_cases = _cases(refinement)
    figure, axes = plt.subplots(
        len(smoke_cases),
        2,
        figsize=(11.0, 3.1 * len(smoke_cases)),
        squeeze=False,
        constrained_layout=True,
    )
    for row, (smoke_case, refined_case) in enumerate(
        zip(smoke_cases, refined_cases, strict=True)
    ):
        name = _string(smoke_case["name"], "case name")
        for document_case, mesh_label, color in (
            (smoke_case, "smoke mesh", _VERMILION),
            (refined_case, "refined mesh", _GREEN),
        ):
            shells = _shell_rows(_selected_point(document_case))
            shell_indices = [
                _integer(shell["shell_index"], "shell_index") for shell in shells
            ]
            matrix_errors = [
                _positive(
                    _number(
                        _object(shell["comparison_total"], "comparison_total")[
                            "maximum_hamiltonian"
                        ],
                        "maximum_hamiltonian",
                    )
                )
                for shell in shells
            ]
            band_errors = [
                _positive(
                    _number(
                        _object(shell["comparison_total"], "comparison_total")[
                            "maximum_band"
                        ],
                        "maximum_band",
                    )
                )
                for shell in shells
            ]
            omitted = [
                _positive(_number(shell["comparison_omitted_power"], "omitted_power"))
                for shell in shells
            ]
            axes[row, 0].plot(
                shell_indices,
                matrix_errors,
                color=color,
                linewidth=2.0,
                label=f"{mesh_label}: matrix",
            )
            axes[row, 0].plot(
                shell_indices,
                band_errors,
                color=color,
                linestyle="--",
                linewidth=1.7,
                label=f"{mesh_label}: band",
            )
            axes[row, 1].plot(
                shell_indices,
                omitted,
                color=color,
                marker=".",
                linewidth=1.8,
                label=mesh_label,
            )
        axes[row, 0].set_yscale("log")
        axes[row, 1].set_yscale("log")
        axes[row, 0].set_ylabel(f"{name}\nerror / $E_{{\\mathrm{{ref}}}}$")
        axes[row, 1].set_ylabel("omitted block power / $E_{\\mathrm{ref}}^2$")
        for axis in axes[row]:
            axis.set_xlabel("complete physical-metric shell index")
            axis.grid(True, alpha=0.25)
        axes[row, 0].legend(fontsize=7, frameon=False)
        axes[row, 1].legend(fontsize=7, frameon=False)
    axes[0, 0].set_title("Endpoint total reconstruction errors")
    axes[0, 1].set_title("Endpoint comparison omitted power")
    for row in range(len(smoke_cases)):
        _panel_label(axes[row, 0], f"({chr(97 + 2 * row)})")
        _panel_label(axes[row, 1], f"({chr(98 + 2 * row)})")
    figure.suptitle(f"{title}: hopping-locality profiles", fontsize=11)
    _save(
        figure,
        output / "shell-locality-profiles",
        f"{title}: hopping-locality profiles",
        "Separated matrix, spectral, and omitted-power channels",
    )
    plt.close(figure)


def _decision_text(value: JsonValue) -> str:
    if value is None:
        return "U"
    return str(_integer(value, "first-passing shell"))


def _plot_first_passing_stability(
    smoke: dict[str, JsonValue],
    refinement: dict[str, JsonValue],
    output: Path,
    title: str,
) -> None:
    columns = (
        "reference_hamiltonian_shell",
        "reference_band_shell",
        "comparison_hamiltonian_shell",
        "comparison_band_shell",
    )
    column_labels = ("ref H", "ref bands", "comparison H", "comparison bands")
    rows: list[list[float]] = []
    annotations: list[list[str]] = []
    labels: list[str] = []
    for smoke_case, refined_case in zip(_cases(smoke), _cases(refinement), strict=True):
        case_name = _string(smoke_case["name"], "case name")
        for smoke_point, refined_point in zip(
            _points(smoke_case), _points(refined_case), strict=True
        ):
            smoke_decisions = _array(smoke_point["first_passing"], "first_passing")
            refined_decisions = _array(refined_point["first_passing"], "first_passing")
            for smoke_value, refined_value in zip(
                smoke_decisions, refined_decisions, strict=True
            ):
                smoke_decision = _object(smoke_value, "decision")
                refined_decision = _object(refined_value, "decision")
                values: list[float] = []
                texts: list[str] = []
                for column in columns:
                    before = smoke_decision[column]
                    after = refined_decision[column]
                    texts.append(f"{_decision_text(before)}→{_decision_text(after)}")
                    if before is None or after is None:
                        values.append(float("nan"))
                    else:
                        values.append(
                            float(_integer(after, column) - _integer(before, column))
                        )
                rows.append(values)
                annotations.append(texts)
                labels.append(
                    f"{case_name} | ρ={_number(smoke_point['parent_scale'], 'rho'):.0f}"
                    f" | a={_number(smoke_point['amplitude'], 'amplitude'):.3g}"
                    f" | τ={_number(smoke_decision['tolerance'], 'tolerance'):.0e}"
                )
    matrix = np.asarray(rows, dtype=np.float64)
    limit = max(1.0, float(np.nanmax(np.abs(matrix))))
    masked = np.ma.masked_invalid(matrix)
    colormap = matplotlib.colormaps["coolwarm"].copy()
    colormap.set_bad("#d9d9d9")
    figure_height = max(5.0, 0.31 * len(labels) + 1.8)
    figure, axis = plt.subplots(figsize=(10.5, figure_height), constrained_layout=True)
    image = axis.imshow(masked, cmap=colormap, vmin=-limit, vmax=limit, aspect="auto")
    axis.set_xticks(range(len(column_labels)), labels=column_labels)
    axis.set_yticks(range(len(labels)), labels=labels, fontsize=7)
    for row, texts in enumerate(annotations):
        for column_index, text in enumerate(texts):
            axis.text(column_index, row, text, ha="center", va="center", fontsize=7)
    axis.set_title(
        f"{title}: first-passing shell stability\n"
        "cell text is smoke→refinement; U means unresolved",
        fontweight="bold",
    )
    colorbar = figure.colorbar(image, ax=axis, shrink=0.7)
    colorbar.set_label("refinement shell minus smoke shell")
    _save(
        figure,
        output / "first-passing-shell-stability",
        f"{title}: first-passing shell stability",
        "Smoke-to-refinement sampled decision comparison",
    )
    plt.close(figure)


def _plot_constrained_tail(
    output: Path,
    title: str,
    geometry: ConstrainedBesselGeometry,
    shell_cap: int,
    kernel_cap: int,
) -> None:
    shells = tuple(range(shell_cap + 1))
    bounds = tuple(
        constrained_bessel_tail_diagnostic(
            geometry,
            math.pi / 4.0,
            shell,
            kernel_cap,
            1.0e-13,
        ).tail_power_upper_bound
        for shell in shells
    )
    figure, axis = plt.subplots(figsize=(7.2, 4.4), constrained_layout=True)
    axis.semilogy(
        shells,
        tuple(_positive(value) for value in bounds),
        color=_BLUE,
        marker="o",
        markersize=3.0,
    )
    axis.scatter((shell_cap,), (_positive(bounds[-1]),), color=_GREEN, zorder=3)
    axis.annotate(
        f"selected cap: {bounds[-1]:.4e}",
        (shell_cap, bounds[-1]),
        xytext=(-8, 12),
        textcoords="offset points",
        ha="right",
        fontsize=9,
    )
    axis.set_xlabel("complete physical-metric shell cap")
    axis.set_ylabel("certified normalized scalar-tail upper bound")
    axis.set_title(
        f"{title}: constrained-Bessel tail\n"
        "binary64 evaluation with declared $10^{-13}$ coefficient margin",
        fontweight="bold",
    )
    axis.grid(True, which="both", alpha=0.2, linewidth=0.5)
    _panel_label(axis, "(a)")
    _save(
        figure,
        output / "constrained-bessel-tail-certificate",
        f"{title}: constrained-Bessel tail",
        "Bounded evaluation of an analytic tail certificate",
    )
    plt.close(figure)


def write_development_plots(
    smoke_result: Path,
    refinement_result: Path,
    output: Path,
    title: str,
    constrained_geometry: ConstrainedBesselGeometry | None = None,
    constrained_shell_cap: int | None = None,
    constrained_kernel_cap: int | None = None,
    intermediate_result: Path | None = None,
) -> tuple[Path, ...]:
    """Write family-owned plots from existing replaceable development records."""
    for name, path in (
        ("smoke_result", smoke_result),
        ("refinement_result", refinement_result),
        ("output", output),
    ):
        if not isinstance(path, Path):
            raise TypeError(f"{name} must be pathlib.Path")
    if intermediate_result is not None and not isinstance(intermediate_result, Path):
        raise TypeError("intermediate_result must be pathlib.Path or None")
    if type(title) is not str or not title:
        raise ValueError("title must be a nonempty string")
    if (constrained_geometry is None) != (constrained_shell_cap is None) or (
        constrained_geometry is None
    ) != (constrained_kernel_cap is None):
        raise ValueError("all constrained-tail controls must be supplied together")
    output.mkdir(parents=True, exist_ok=True)
    smoke = _load(smoke_result)
    refinement = _load(refinement_result)
    mesh_results = (
        (smoke, _load(intermediate_result), refinement)
        if intermediate_result is not None
        else (smoke, refinement)
    )
    with matplotlib.rc_context(_STYLE):  # type: ignore[arg-type]
        _plot_scientific_story(smoke, refinement, output, title)
        _plot_mesh_summary(mesh_results, output, title)
        _plot_error_channel_decomposition(refinement, output, title)
        _plot_shell_profiles(smoke, refinement, output, title)
        _plot_first_passing_stability(smoke, refinement, output, title)
    stems = [
        output / "band-equivalence-locality-scientific-story",
        output / "mesh-refinement-summary",
        output / "three-channel-error-decomposition",
        output / "shell-locality-profiles",
        output / "first-passing-shell-stability",
    ]
    if constrained_geometry is not None:
        if type(constrained_geometry) is not ConstrainedBesselGeometry:
            raise TypeError("constrained_geometry must be ConstrainedBesselGeometry")
        assert constrained_shell_cap is not None
        assert constrained_kernel_cap is not None
        with matplotlib.rc_context(_STYLE):  # type: ignore[arg-type]
            _plot_constrained_tail(
                output,
                title,
                constrained_geometry,
                constrained_shell_cap,
                constrained_kernel_cap,
            )
        stems.append(output / "constrained-bessel-tail-certificate")
    return tuple(
        path
        for stem in stems
        for path in (stem.with_suffix(".pdf"), stem.with_suffix(".png"))
    )


__all__ = ["write_development_plots"]
