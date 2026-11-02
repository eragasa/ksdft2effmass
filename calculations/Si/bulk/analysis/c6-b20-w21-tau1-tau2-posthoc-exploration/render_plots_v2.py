from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap
from numpy.typing import NDArray

RealArray = NDArray[np.float64]
type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
RESULT = ROOT / "result.json"
FIGURES = ROOT / "figures-v2"
MANIFEST = FIGURES / "figure-manifest.json"
STATUS = (
    "post-hoc-producer-checked-development-exploration-not-independently-verified"
)


def mapping(value: JsonValue, name: str) -> JsonObject:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be a mapping")
    return value


def values(value: JsonValue, name: str) -> list[JsonValue]:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list")
    return value


def numeric(value: JsonValue, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    return float(value)


def string(value: JsonValue, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def minimum_support_grid(
    spectral: RealArray,
    operator: RealArray,
    cost: NDArray[np.int64],
) -> tuple[RealArray, RealArray, RealArray]:
    x = np.logspace(
        np.log10(float(np.min(spectral)) * 0.65),
        np.log10(float(np.max(spectral)) * 1.25),
        320,
    )
    y = np.logspace(
        np.log10(float(np.min(operator)) * 0.65),
        np.log10(float(np.max(operator)) * 1.25),
        320,
    )
    grid = np.full((len(y), len(x)), np.nan, dtype=np.float64)
    for row, tau_2 in enumerate(y):
        for column, tau_1 in enumerate(x):
            feasible = (spectral <= tau_1) & (operator <= tau_2)
            if np.any(feasible):
                grid[row, column] = float(np.min(cost[feasible]))
    return x, y, grid


def render_map(
    *,
    candidates: list[JsonObject],
    spectral_key: str,
    operator_key: str,
    spectral_label: str,
    operator_label: str,
    title: str,
    output_stem: str,
) -> None:
    reduced = [
        item for item in candidates if item["proper_reduced_candidate"] is True
    ]
    spectral = np.asarray(
        [numeric(item[spectral_key], spectral_key) for item in reduced],
        dtype=np.float64,
    )
    operator = np.asarray(
        [numeric(item[operator_key], operator_key) for item in reduced],
        dtype=np.float64,
    )
    cost = np.asarray(
        [
            int(numeric(item["included_representative_count"], "support cost"))
            for item in reduced
        ],
        dtype=np.int64,
    )
    shell_ids = [string(item["shell_id"], "shell id") for item in reduced]
    x, y, grid = minimum_support_grid(spectral, operator, cost)
    unique_costs = np.unique(cost)
    colors = plt.get_cmap("viridis", len(unique_costs))(np.arange(len(unique_costs)))
    colormap = ListedColormap(colors)
    colormap.set_bad("#eeeeee")
    boundaries = np.concatenate(
        (
            [unique_costs[0] - 0.5],
            0.5 * (unique_costs[:-1] + unique_costs[1:]),
            [unique_costs[-1] + 0.5],
        )
    )
    norm = BoundaryNorm(boundaries, colormap.N)
    figure, axes = plt.subplots(
        1,
        2,
        figsize=(12.5, 5.2),
        layout="constrained",
    )
    scatter = axes[0].scatter(
        spectral,
        operator,
        c=cost,
        cmap=colormap,
        norm=norm,
        edgecolors="black",
        linewidths=0.6,
        s=58,
        zorder=4,
    )
    axes[0].plot(spectral, operator, color="0.55", linewidth=0.8, zorder=2)
    for index, shell_id in enumerate(shell_ids):
        if index in (0, 2, 4, 6, 8, 10, 12, 14, 16):
            axes[0].annotate(
                shell_id.replace("H-shell-", "H"),
                (spectral[index], operator[index]),
                xytext=(5, 4),
                textcoords="offset points",
                fontsize=6.5,
            )
    axes[0].set_xscale("log")
    axes[0].set_yscale("log")
    axes[0].set_xlabel(spectral_label)
    axes[0].set_ylabel(operator_label)
    axes[0].set_title("requirements of each proper reduced shell")
    axes[0].grid(which="both", alpha=0.22)
    axes[0].text(
        0.02,
        0.02,
        "H17 full-support control = (0,0), excluded from feasibility",
        transform=axes[0].transAxes,
        fontsize=7,
        va="bottom",
    )
    mesh = axes[1].pcolormesh(x, y, grid, cmap=colormap, norm=norm, shading="auto")
    axes[1].scatter(
        spectral,
        operator,
        facecolors="none",
        edgecolors="black",
        linewidths=0.65,
        s=32,
        zorder=5,
    )
    axes[1].set_xscale("log")
    axes[1].set_yscale("log")
    axes[1].set_xlabel(r"post-hoc spectral threshold, $\tau_1$")
    axes[1].set_ylabel(r"post-hoc operator threshold, $\tau_2$")
    axes[1].set_title("minimum retained support witness")
    axes[1].grid(which="both", alpha=0.15)
    axes[1].text(
        0.02,
        0.98,
        "gray: no proper reduced shell satisfies both",
        transform=axes[1].transAxes,
        fontsize=7,
        va="top",
    )
    colorbar = figure.colorbar(
        mesh,
        ax=axes,
        location="right",
        shrink=0.82,
        pad=0.025,
    )
    colorbar.set_label("minimum included Wigner–Seitz representatives")
    colorbar.set_ticks(unique_costs[::2])
    figure.suptitle(title)
    figure.text(
        0.5,
        0.008,
        STATUS,
        ha="center",
        va="bottom",
        fontsize=7,
    )
    figure.savefig(FIGURES / f"{output_stem}.pdf", bbox_inches="tight")
    figure.savefig(FIGURES / f"{output_stem}.png", dpi=220, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    if FIGURES.exists():
        raise FileExistsError(f"refusing to overwrite retained figures: {FIGURES}")
    result_value: JsonValue = json.loads(RESULT.read_text(encoding="utf-8"))
    result = mapping(result_value, "result")
    if result.get("status") != STATUS:
        raise RuntimeError("result has the wrong assurance status")
    candidates = [
        mapping(item, "candidate")
        for item in values(result["candidates"], "candidates")
    ]
    FIGURES.mkdir()
    render_map(
        candidates=candidates,
        spectral_key="tau_1_spectral_rms",
        operator_key="tau_2_operator_rms_per_state",
        spectral_label=r"required RMS spectral threshold $\tau_1$",
        operator_label=r"required RMS operator threshold $\tau_2$",
        title=(
            r"Post-hoc $\tau_1$–$\tau_2$ feasibility map: RMS losses"
            "\nproper native Wigner–Seitz shell reductions only"
        ),
        output_stem="tau1-tau2-rms-map",
    )
    render_map(
        candidates=candidates,
        spectral_key="spectral_maximum",
        operator_key="operator_maximum_per_state",
        spectral_label="required maximum spectral threshold",
        operator_label="required maximum operator threshold",
        title=(
            r"Post-hoc $\tau_1$–$\tau_2$ feasibility map: maximum losses"
            "\nproper native Wigner–Seitz shell reductions only"
        ),
        output_stem="tau1-tau2-maximum-map",
    )
    figure_files = sorted(FIGURES.iterdir())
    if len(figure_files) != 4:
        raise RuntimeError("expected two PDF and two PNG figures")
    manifest: JsonObject = {
        "schema_version": 1,
        "status": STATUS,
        "result": {
            "path": str(RESULT),
            "byte_size": RESULT.stat().st_size,
            "sha256": sha256(RESULT),
        },
        "renderer": {
            "path": str(Path(__file__)),
            "byte_size": Path(__file__).stat().st_size,
            "sha256": sha256(Path(__file__)),
        },
        "figures": {
            path.name: {
                "byte_size": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in figure_files
        },
    }
    MANIFEST.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
