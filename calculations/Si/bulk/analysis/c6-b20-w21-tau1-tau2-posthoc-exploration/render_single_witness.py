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
FIGURES = ROOT / "figures-v5"
PDF = FIGURES / "single-witness-surface.pdf"
PNG = FIGURES / "single-witness-surface.png"
MANIFEST = FIGURES / "single-witness-manifest.json"
STATUS = "post-hoc-producer-checked-development-exploration-not-independently-verified"


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


def main() -> None:
    if FIGURES.exists():
        raise FileExistsError(
            f"refusing to overwrite retained witness directory: {FIGURES}"
        )
    FIGURES.mkdir()
    result_value: JsonValue = json.loads(RESULT.read_text(encoding="utf-8"))
    result = mapping(result_value, "result")
    if result.get("status") != STATUS:
        raise RuntimeError("result has the wrong assurance status")
    candidates = [
        mapping(item, "candidate")
        for item in values(result["candidates"], "candidates")
        if mapping(item, "candidate")["proper_reduced_candidate"] is True
    ]
    spectral = np.asarray(
        [
            numeric(item["tau_1_spectral_rms"], "tau_1 requirement")
            for item in candidates
        ],
        dtype=np.float64,
    )
    operator = np.asarray(
        [
            numeric(item["tau_2_operator_rms_per_state"], "tau_2 requirement")
            for item in candidates
        ],
        dtype=np.float64,
    )
    cost = np.asarray(
        [
            int(numeric(item["included_representative_count"], "support cost"))
            for item in candidates
        ],
        dtype=np.int64,
    )
    shell_ids = [string(item["shell_id"], "shell id") for item in candidates]
    x_edges = np.unique(
        np.concatenate(
            (
                np.asarray([float(np.min(spectral)) * 0.65]),
                spectral,
                np.asarray([float(np.max(spectral)) * 1.25]),
            )
        )
    )
    y_edges = np.unique(
        np.concatenate(
            (
                np.asarray([float(np.min(operator)) * 0.65]),
                operator,
                np.asarray([float(np.max(operator)) * 1.25]),
            )
        )
    )
    witness_cost = np.full(
        (len(y_edges) - 1, len(x_edges) - 1), np.nan, dtype=np.float64
    )
    witness_index = np.full((len(y_edges) - 1, len(x_edges) - 1), -1, dtype=np.int64)
    for row, (lower_y, upper_y) in enumerate(
        zip(y_edges[:-1], y_edges[1:], strict=True)
    ):
        tau_2 = float(np.sqrt(lower_y * upper_y))
        for column, (lower_x, upper_x) in enumerate(
            zip(x_edges[:-1], x_edges[1:], strict=True)
        ):
            tau_1 = float(np.sqrt(lower_x * upper_x))
            feasible = np.flatnonzero((spectral <= tau_1) & (operator <= tau_2))
            if len(feasible) == 0:
                continue
            selected = int(feasible[int(np.argmin(cost[feasible]))])
            witness_cost[row, column] = float(cost[selected])
            witness_index[row, column] = selected
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
    figure, axis = plt.subplots(figsize=(9.4, 7.2), layout="constrained")
    mesh = axis.pcolormesh(
        x_edges,
        y_edges,
        witness_cost,
        cmap=colormap,
        norm=norm,
        shading="flat",
        edgecolors=(0.0, 0.0, 0.0, 0.10),
        linewidth=0.25,
    )
    axis.scatter(
        spectral,
        operator,
        facecolors="white",
        edgecolors="black",
        s=42,
        linewidths=0.75,
        zorder=5,
        label="candidate requirement corner",
    )
    for index, shell_id in enumerate(shell_ids):
        is_upper_right = index == int(np.argmax(spectral + operator))
        axis.annotate(
            shell_id.replace("H-shell-", "H"),
            (spectral[index], operator[index]),
            xytext=(-5, -7) if is_upper_right else (4, 4),
            textcoords="offset points",
            horizontalalignment="right" if is_upper_right else "left",
            verticalalignment="top" if is_upper_right else "bottom",
            fontsize=6.5,
            zorder=6,
        )
    axis.set_xscale("log")
    axis.set_yscale("log")
    axis.set_xlabel(r"post-hoc RMS spectral threshold, $\tau_1$")
    axis.set_ylabel(r"post-hoc RMS operator threshold, $\tau_2$")
    axis.set_title(
        r"Single minimum-support witness surface $W(\tau_1,\tau_2)$"
        "\nproper native Wigner–Seitz shell reductions; exact threshold cells"
        "\nproducer-checked development, not independently verified"
    )
    axis.grid(which="both", alpha=0.15)
    axis.text(
        0.015,
        0.985,
        "gray: no proper reduced witness\nH17 full source at (0,0) is excluded",
        transform=axis.transAxes,
        va="top",
        fontsize=8,
        bbox={"facecolor": "white", "edgecolor": "0.7", "alpha": 0.85},
    )
    colorbar = figure.colorbar(mesh, ax=axis, shrink=0.88, pad=0.025)
    colorbar.set_label("representatives in the unique minimum-support witness")
    colorbar.set_ticks(unique_costs.astype(np.float64).tolist())
    colorbar.ax.tick_params(labelsize=7)
    axis.legend(loc="lower right", fontsize=8)
    figure.savefig(PDF, bbox_inches="tight")
    figure.savefig(PNG, dpi=240, bbox_inches="tight")
    plt.close(figure)
    manifest: JsonObject = {
        "schema_version": 1,
        "status": STATUS,
        "surface_definition": (
            "W(tau_1,tau_2) is the proper reduced candidate with the smallest exact "
            "included-representative count among candidates satisfying both primary "
            "RMS threshold inequalities"
        ),
        "cell_construction": (
            "exact requirement coordinates define logarithmic rectangular threshold "
            "cells; no numerical interpolation or smoothing is used"
        ),
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
            for path in (PDF, PNG)
        },
    }
    MANIFEST.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
