from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

RealArray = NDArray[np.float64]
type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
RESULT = ROOT / "result.json"
PLOT_DATA = ROOT / "plot-data.json"
FIGURES = ROOT / "figures"
MODELS = ("full-source", "H-shell-05", "H-shell-10", "H-shell-16")
DISPLAY = {
    "full-source": "Full source",
    "H-shell-05": "H-shell-05",
    "H-shell-10": "H-shell-10",
    "H-shell-16": "H-shell-16",
}
COLORS = {
    "full-source": "#111111",
    "H-shell-05": "#d55e00",
    "H-shell-10": "#0072b2",
    "H-shell-16": "#009e73",
}
BRANCH_COLORS = ("#0072b2", "#cc79a7", "#d55e00")
BRANCH_NAMES = ("lower", "middle", "upper")


def load_module(path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(
        "c6_b20_w21_comprehensive_edge_renderer_source", path
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load analysis producer")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def mapping(value: JsonValue, name: str) -> JsonObject:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be a mapping")
    return value


def numeric(value: JsonValue, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    return float(value)


def directional_plot_data() -> JsonObject:
    analysis = load_module(ROOT / "run_analysis.py")
    _, evaluator, _, reciprocal, _ = analysis.reconstruct()
    inverse = np.linalg.inv(reciprocal)
    q = np.linspace(-0.02, 0.02, 161, dtype=np.float64)
    q_values: list[JsonValue] = [float(value) for value in q]
    data: JsonObject = {
        "q_inverse_angstrom": q_values,
        "energy_reference": "each model's ordered band-3 energy at Gamma",
        "models": {},
    }
    models = mapping(data["models"], "models")
    for model_index, model_name in enumerate(MODELS):
        gamma = analysis.eigenvalues_at(
            evaluator, model_index, np.zeros((1, 3), dtype=np.float64)
        )[0]
        direction_data: JsonObject = {}
        for direction_name, direction in analysis.DIRECTIONS.items():
            points = np.asarray(
                [
                    analysis.cartesian_point(
                        np.zeros(3, dtype=np.float64), distance * direction, inverse
                    )
                    for distance in q
                ],
                dtype=np.float64,
            )
            eigenvalues = analysis.eigenvalues_at(evaluator, model_index, points)
            direction_data[direction_name] = {
                "ordered_valence_cluster_energies_relative_to_gamma_vbm_mev": (
                    1000.0 * (eigenvalues[:, 1:4] - gamma[3])
                ).tolist()
            }
        models[model_name] = direction_data
    return data


def save(figure: Figure, stem: str) -> None:
    figure.savefig(FIGURES / f"{stem}.pdf", bbox_inches="tight")
    figure.savefig(FIGURES / f"{stem}.png", bbox_inches="tight", dpi=220)
    plt.close(figure)


def render_gamma(result: JsonObject) -> None:
    cluster = mapping(result["gamma_valence_cluster"], "cluster")
    splits = [
        1000.0
        * numeric(mapping(cluster[model], model)["cluster_splitting_ev"], "split")
        for model in MODELS
    ]
    angles = [
        180.0
        / np.pi
        * numeric(
            mapping(cluster[model], model)["maximum_cluster_principal_angle_radians"],
            "angle",
        )
        for model in MODELS
    ]
    x = np.arange(len(MODELS))
    colors = [COLORS[model] for model in MODELS]
    figure, axes = plt.subplots(1, 2, figsize=(9.2, 3.8))
    axes[0].bar(x, splits, color=colors)
    axes[0].set_yscale("log")
    axes[0].set_ylabel("$\\Gamma$ three-band splitting (meV)")
    axes[0].set_title("Internal valence-cluster degeneracy")
    axes[1].bar(x, angles, color=colors)
    axes[1].set_ylabel("Maximum principal angle (degrees)")
    axes[1].set_title("Source-cluster subspace rotation")
    for axis in axes:
        axis.set_xticks(
            x, [DISPLAY[model] for model in MODELS], rotation=25, ha="right"
        )
        axis.grid(axis="y", alpha=0.25)
    figure.suptitle(
        "Subspace preservation does not guarantee preservation of internal degeneracy"
    )
    figure.tight_layout()
    save(figure, "gamma-valence-cluster-fidelity")


def render_dispersions(plot_data: JsonObject) -> None:
    q = np.asarray(plot_data["q_inverse_angstrom"], dtype=np.float64)
    models = mapping(plot_data["models"], "plot models")
    figure, axes = plt.subplots(4, 3, figsize=(11.5, 11.5), sharex=True, sharey=True)
    for row, model in enumerate(MODELS):
        model_data = mapping(models[model], model)
        for column, direction in enumerate(("100", "110", "111")):
            axis = axes[row, column]
            energies = np.asarray(
                mapping(model_data[direction], direction)[
                    "ordered_valence_cluster_energies_relative_to_gamma_vbm_mev"
                ],
                dtype=np.float64,
            )
            for branch in range(3):
                axis.plot(
                    q,
                    energies[:, branch],
                    color=BRANCH_COLORS[branch],
                    linewidth=1.5,
                    label=BRANCH_NAMES[branch],
                )
            axis.axvline(0.0, color="#777777", linewidth=0.6)
            axis.axhline(0.0, color="#777777", linewidth=0.6)
            axis.grid(alpha=0.2)
            if row == 0:
                axis.set_title(f"[{direction[0]}{direction[1]}{direction[2]}]")
            if column == 0:
                axis.set_ylabel(f"{DISPLAY[model]}\n$E-E_{{v,\\Gamma}}$ (meV)")
            if row == 3:
                axis.set_xlabel("Signed displacement ($\\mathrm{\\AA}^{-1}$)")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.965),
        ncol=3,
        frameon=False,
    )
    figure.suptitle("Ordered non-SOC valence-cluster branches near $\\Gamma$", y=0.997)
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.93))
    save(figure, "directional-valence-cluster-dispersions")


def render_valence_sensitivity(result: JsonObject) -> None:
    directional = mapping(result["directional_valence_cluster"], "directional")
    figure, axes = plt.subplots(4, 3, figsize=(11.5, 11.5), sharex=True)
    for row, model in enumerate(MODELS):
        model_data = mapping(directional[model], model)
        for column, direction in enumerate(("100", "110", "111")):
            axis = axes[row, column]
            windows = mapping(model_data[direction], direction)["windows"]
            if not isinstance(windows, list):
                raise TypeError("windows must be a list")
            x = np.asarray(
                [
                    numeric(
                        mapping(item, "window")["fit_window_inverse_angstrom"], "window"
                    )
                    for item in windows
                ],
                dtype=np.float64,
            )
            for branch_index, branch_name in enumerate(BRANCH_NAMES):
                masses: list[float] = []
                valid_x: list[float] = []
                for x_value, window_value in zip(x, windows, strict=True):
                    branches = mapping(window_value, "window")["branches"]
                    if not isinstance(branches, list):
                        raise TypeError("branches must be a list")
                    mass = mapping(branches[branch_index], "branch")[
                        "apparent_directional_hole_mass_electron"
                    ]
                    if isinstance(mass, (int, float)) and not isinstance(mass, bool):
                        valid_x.append(float(x_value))
                        masses.append(float(mass))
                axis.plot(
                    valid_x,
                    masses,
                    marker="o",
                    color=BRANCH_COLORS[branch_index],
                    label=branch_name,
                )
            axis.set_yscale("log")
            axis.grid(alpha=0.2)
            if row == 0:
                axis.set_title(f"[{direction[0]}{direction[1]}{direction[2]}]")
            if column == 0:
                axis.set_ylabel(f"{DISPLAY[model]}\nApparent mass ($m_e$)")
            if row == 3:
                axis.set_xlabel("Fit half-window ($\\mathrm{\\AA}^{-1}$)")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.965),
        ncol=3,
        frameon=False,
    )
    figure.suptitle(
        "Fit-window sensitivity exposes the lack of unique ordered-branch hole tensors",
        y=0.997,
    )
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.93))
    save(figure, "directional-valence-mass-sensitivity")


def render_electron(result: JsonObject) -> None:
    electron = mapping(result["electron_edge"], "electron")
    x = np.arange(len(MODELS))
    colors = [COLORS[model] for model in MODELS]
    dos = [
        numeric(
            mapping(electron[model], model)["six_valley_dos_mass_convention_electron"],
            "DOS mass",
        )
        for model in MODELS
    ]
    conductivity = [
        numeric(
            mapping(electron[model], model)[
                "equal_population_conductivity_mass_convention_electron"
            ],
            "conductivity mass",
        )
        for model in MODELS
    ]
    stencil = []
    for model in MODELS:
        valleys = mapping(mapping(electron[model], model)["valleys"], "valleys")
        stencil.append(
            100.0
            * max(
                numeric(
                    mapping(valley, "valley")[
                        "maximum_principal_mass_relative_stencil_spread"
                    ],
                    "stencil spread",
                )
                for valley in valleys.values()
            )
        )
    figure, axes = plt.subplots(1, 3, figsize=(13.5, 3.8))
    axes[0].bar(x, dos, color=colors)
    axes[0].set_ylabel("Six-valley DOS-mass convention ($m_e$)")
    axes[1].bar(x, conductivity, color=colors)
    axes[1].set_ylabel("Equal-population conductivity-mass convention ($m_e$)")
    axes[2].bar(x, stencil, color=colors)
    axes[2].set_ylabel("Maximum stencil spread (%)")
    for axis in axes:
        axis.set_xticks(
            x, [DISPLAY[model] for model in MODELS], rotation=25, ha="right"
        )
        axis.grid(axis="y", alpha=0.25)
    figure.suptitle("Derived conduction-valley mass diagnostics")
    figure.tight_layout(w_pad=2.2)
    save(figure, "derived-electron-mass-fidelity")


def render_high_symmetry(result: JsonObject) -> None:
    edges = mapping(result["high_symmetry_edges"], "edges")
    labels = ("Gamma", "X", "L")
    x = np.arange(len(labels))
    width = 0.19
    figure, axes = plt.subplots(1, 2, figsize=(10.0, 3.9))
    for index, model in enumerate(MODELS):
        model_edges = mapping(edges[model], model)
        gaps = [
            numeric(mapping(model_edges[label], label)["minimum_direct_gap_ev"], "gap")
            for label in labels
        ]
        axes[0].bar(
            x + (index - 1.5) * width,
            gaps,
            width=width,
            color=COLORS[model],
            label=DISPLAY[model],
        )
    spread_labels = ("X", "L")
    x_spread = np.arange(2)
    for index, model in enumerate(MODELS):
        model_edges = mapping(edges[model], model)
        spreads = [
            1000.0
            * numeric(
                mapping(model_edges[label], label)["symmetry_spread_ev"], "spread"
            )
            for label in spread_labels
        ]
        axes[1].bar(
            x_spread + (index - 1.5) * width,
            spreads,
            width=width,
            color=COLORS[model],
        )
    axes[0].set_xticks(x, ("$\\Gamma$", "X", "L"))
    axes[0].set_ylabel("Minimum direct gap (eV)")
    axes[0].set_title("High-symmetry direct gaps")
    axes[1].set_xticks(x_spread, spread_labels)
    axes[1].set_yscale("log")
    axes[1].set_ylabel("Equivalent-point gap spread (meV)")
    axes[1].set_title("Cubic-symmetry diagnostic")
    for axis in axes:
        axis.grid(axis="y", alpha=0.25)
    axes[0].legend(frameon=False, fontsize=8)
    figure.tight_layout()
    save(figure, "high-symmetry-edge-fidelity")


def main() -> None:
    if PLOT_DATA.exists() or FIGURES.exists():
        raise FileExistsError("refusing to overwrite retained plot artifacts")
    result = mapping(json.loads(RESULT.read_text(encoding="utf-8")), "result")
    plot_data = directional_plot_data()
    PLOT_DATA.write_text(
        json.dumps(plot_data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    FIGURES.mkdir()
    render_gamma(result)
    render_dispersions(plot_data)
    render_valence_sensitivity(result)
    render_electron(result)
    render_high_symmetry(result)


if __name__ == "__main__":
    main()
