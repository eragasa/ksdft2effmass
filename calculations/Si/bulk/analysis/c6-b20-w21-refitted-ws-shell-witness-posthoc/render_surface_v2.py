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
IntArray = NDArray[np.int64]
type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
RESULT = ROOT / "result.json"
FIGURES = ROOT / "figures-v2"
PDF = FIGURES / "single-refitted-witness-surface.pdf"
PNG = FIGURES / "single-refitted-witness-surface.png"
SURFACE = ROOT / "witness-surface-v2.json"
MANIFEST = FIGURES / "figure-manifest.json"
STATUS = (
    "post-hoc-refitted-ws-producer-checked-development-not-independently-verified"
)
EXAMPLE_THRESHOLDS = (
    (1.0, 1.0),
    (0.5, 0.5),
    (0.1, 0.15),
    (0.05, 0.1),
    (0.02, 0.04),
    (0.01, 0.02),
    (0.002, 0.006),
    (0.001, 0.002),
    (0.0004, 0.001),
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


def identity(path: Path) -> JsonObject:
    return {
        "path": str(path),
        "byte_size": path.stat().st_size,
        "sha256": sha256(path),
    }


def run_length_encode(row: IntArray) -> list[JsonValue]:
    runs: list[JsonValue] = []
    start = 0
    current = int(row[0])
    for index in range(1, len(row)):
        value = int(row[index])
        if value == current:
            continue
        runs.append([start, index, current])
        start = index
        current = value
    runs.append([start, len(row), current])
    return runs


def select_example(
    witnesses: list[JsonObject], tau_1: float, tau_2: float
) -> JsonObject:
    feasible = [
        witness
        for witness in witnesses
        if numeric(witness["tau_1_spectral_rms"], "tau_1") <= tau_1
        and numeric(witness["tau_2_operator_rms_per_state"], "tau_2") <= tau_2
    ]
    if not feasible:
        return {"tau_1": tau_1, "tau_2": tau_2, "witness_found": False}
    minimum_cost = min(
        int(numeric(witness["included_representative_count"], "cost"))
        for witness in feasible
    )
    minimum_cost_witnesses = [
        witness
        for witness in feasible
        if int(numeric(witness["included_representative_count"], "cost"))
        == minimum_cost
    ]
    selected = min(
        minimum_cost_witnesses,
        key=lambda witness: (
            max(
                numeric(witness["tau_1_spectral_rms"], "tau_1") / tau_1,
                numeric(witness["tau_2_operator_rms_per_state"], "tau_2")
                / tau_2,
            ),
            numeric(witness["tau_1_spectral_rms"], "tau_1"),
            numeric(witness["tau_2_operator_rms_per_state"], "tau_2"),
        ),
    )
    return {
        "tau_1": tau_1,
        "tau_2": tau_2,
        "witness_found": True,
        "shell_id": selected["shell_id"],
        "included_representative_count": minimum_cost,
        "attained_tau_1": selected["tau_1_spectral_rms"],
        "attained_tau_2": selected["tau_2_operator_rms_per_state"],
        "alpha": selected["alpha"],
    }


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    for path in (PDF, PNG, SURFACE, MANIFEST):
        if path.exists():
            raise FileExistsError(f"refusing to overwrite retained surface artifact: {path}")
    result_value: JsonValue = json.loads(RESULT.read_text(encoding="utf-8"))
    result = mapping(result_value, "result")
    if result.get("status") != STATUS:
        raise RuntimeError("result has the wrong assurance status")
    all_witnesses = [
        mapping(item, "witness")
        for item in values(result["witnesses"], "witnesses")
    ]
    witnesses = [
        witness for witness in all_witnesses if witness["optimizer_success"] is True
    ]
    if not witnesses:
        raise RuntimeError("no converged constructive witnesses are available")
    for index, witness in enumerate(witnesses):
        witness["surface_witness_id"] = f"W{index:04d}"
    spectral = np.asarray(
        [numeric(witness["tau_1_spectral_rms"], "tau_1") for witness in witnesses],
        dtype=np.float64,
    )
    operator = np.asarray(
        [
            numeric(witness["tau_2_operator_rms_per_state"], "tau_2")
            for witness in witnesses
        ],
        dtype=np.float64,
    )
    cost = np.asarray(
        [
            int(numeric(witness["included_representative_count"], "cost"))
            for witness in witnesses
        ],
        dtype=np.int64,
    )
    x_edges = np.unique(
        np.concatenate(
            ([float(np.min(spectral)) * 0.65], spectral, [float(np.max(spectral)) * 1.25])
        )
    )
    y_edges = np.unique(
        np.concatenate(
            ([float(np.min(operator)) * 0.65], operator, [float(np.max(operator)) * 1.25])
        )
    )
    x_centers = np.sqrt(x_edges[:-1] * x_edges[1:])
    y_centers = np.sqrt(y_edges[:-1] * y_edges[1:])
    selected_index = np.full(
        (len(y_centers), len(x_centers)), -1, dtype=np.int64
    )
    selected_cost = np.full(
        (len(y_centers), len(x_centers)), np.iinfo(np.int64).max, dtype=np.int64
    )
    selected_score = np.full(
        (len(y_centers), len(x_centers)), np.inf, dtype=np.float64
    )
    for witness_index, (tau_1, tau_2, support_cost) in enumerate(
        zip(spectral, operator, cost, strict=True)
    ):
        first_column = int(np.searchsorted(x_centers, tau_1, side="left"))
        first_row = int(np.searchsorted(y_centers, tau_2, side="left"))
        if first_column == len(x_centers) or first_row == len(y_centers):
            continue
        cost_view = selected_cost[first_row:, first_column:]
        score_view = selected_score[first_row:, first_column:]
        index_view = selected_index[first_row:, first_column:]
        local_score = np.maximum(
            tau_1 / x_centers[None, first_column:],
            tau_2 / y_centers[first_row:, None],
        )
        replace = (support_cost < cost_view) | (
            (support_cost == cost_view) & (local_score < score_view)
        )
        cost_view[replace] = support_cost
        score_view[replace] = local_score[replace]
        index_view[replace] = witness_index
    feasible = selected_index >= 0
    plotted_cost = np.asarray(selected_cost, dtype=np.float64)
    plotted_cost[~feasible] = np.nan
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
    active_indices = np.unique(selected_index[feasible])
    literal = [
        witness
        for witness in witnesses
        if numeric(witness["spectral_scalarization_weight"], "weight") == -1.0
    ]
    figure, axis = plt.subplots(figsize=(9.4, 7.2), layout="constrained")
    mesh = axis.pcolormesh(
        x_edges,
        y_edges,
        plotted_cost,
        cmap=colormap,
        norm=norm,
        shading="flat",
        edgecolors="none",
        linewidth=0.0,
    )
    axis.scatter(
        spectral[active_indices],
        operator[active_indices],
        s=16,
        facecolors="white",
        edgecolors="black",
        linewidths=0.45,
        alpha=0.9,
        label="active fitted witness",
        zorder=5,
    )
    axis.scatter(
        [numeric(witness["tau_1_spectral_rms"], "literal tau_1") for witness in literal],
        [
            numeric(witness["tau_2_operator_rms_per_state"], "literal tau_2")
            for witness in literal
        ],
        marker="x",
        s=30,
        color="#d62728",
        linewidths=0.9,
        label=r"literal truncation ($\alpha_s=1$)",
        zorder=6,
    )
    axis.set_xscale("log")
    axis.set_yscale("log")
    axis.set_xlabel(r"post-hoc RMS spectral threshold, $\tau_1$")
    axis.set_ylabel(r"post-hoc RMS operator threshold, $\tau_2$")
    axis.set_title(
        r"Single fitted-shell witness surface $W_{\alpha}(\tau_1,\tau_2)$"
        "\none scale per retained native Wigner–Seitz shell, "
        r"$0\leq\alpha_s\leq2$"
        "\npost-hoc producer-checked development; not independently verified"
    )
    axis.grid(which="both", alpha=0.14)
    axis.text(
        0.015,
        0.985,
        "gray: no converged witness found in the bounded search\n"
        "gray is not a global infeasibility certificate",
        transform=axis.transAxes,
        va="top",
        fontsize=8,
        bbox={"facecolor": "white", "edgecolor": "0.7", "alpha": 0.88},
    )
    colorbar = figure.colorbar(mesh, ax=axis, shrink=0.88, pad=0.025)
    colorbar.set_label("representatives in the minimum-support fitted witness")
    colorbar.set_ticks(unique_costs)
    colorbar.ax.tick_params(labelsize=7)
    axis.legend(loc="lower right", fontsize=8)
    figure.savefig(PDF, bbox_inches="tight")
    figure.savefig(PNG, dpi=240, bbox_inches="tight")
    plt.close(figure)

    surface: JsonObject = {
        "schema_version": 1,
        "status": STATUS,
        "source_result": identity(RESULT),
        "witness_filter": "optimizer_success is true",
        "explicit_converged_witness_count": len(witnesses),
        "active_surface_witness_count": len(active_indices),
        "selection": {
            "primary": "minimum included-representative count",
            "tie_break": "minimum max(attained_tau_1/tau_1, attained_tau_2/tau_2), then retained input order",
            "failure_meaning": "no converged constructive witness found; not certified infeasibility",
        },
        "x_edges_tau_1": x_edges.tolist(),
        "y_edges_tau_2": y_edges.tolist(),
        "row_major_witness_index_runs": [
            run_length_encode(row) for row in selected_index
        ],
        "witness_index": [
            {
                "surface_index": index,
                "surface_witness_id": witness["surface_witness_id"],
                "shell_id": witness["shell_id"],
                "included_representative_count": witness[
                    "included_representative_count"
                ],
                "tau_1_spectral_rms": witness["tau_1_spectral_rms"],
                "tau_2_operator_rms_per_state": witness[
                    "tau_2_operator_rms_per_state"
                ],
                "alpha": witness["alpha"],
            }
            for index, witness in enumerate(witnesses)
        ],
        "illustrative_threshold_witnesses": [
            select_example(witnesses, tau_1, tau_2)
            for tau_1, tau_2 in EXAMPLE_THRESHOLDS
        ],
    }
    SURFACE.write_text(
        json.dumps(surface, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    manifest: JsonObject = {
        "schema_version": 1,
        "status": STATUS,
        "result": identity(RESULT),
        "surface": identity(SURFACE),
        "renderer": identity(Path(__file__)),
        "figures": {path.name: identity(path) for path in (PDF, PNG)},
    }
    MANIFEST.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
