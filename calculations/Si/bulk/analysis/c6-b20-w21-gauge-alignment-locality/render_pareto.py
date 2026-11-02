from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

RealArray = NDArray[np.float64]
type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
RESULT = ROOT / "result.json"
FIGURES = ROOT / "figures"
PDF = FIGURES / "pareto-support-error-frontiers.pdf"
PNG = FIGURES / "pareto-support-error-frontiers.png"
MANIFEST = FIGURES / "pareto-figure-manifest.json"
STATUS = "producer-checked-development-analysis-not-independently-verified"
FLOOR = 1.0e-16


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


def pareto_mask(cost: RealArray, error: RealArray) -> NDArray[np.bool_]:
    order = np.argsort(cost, kind="stable")
    selected = np.zeros(len(cost), dtype=np.bool_)
    best = np.inf
    for index in order:
        if error[index] < best:
            selected[index] = True
            best = error[index]
    return selected


def main() -> None:
    for path in (PDF, PNG, MANIFEST):
        if path.exists():
            raise FileExistsError(f"refusing to overwrite retained Pareto artifact: {path}")
    result_value: JsonValue = json.loads(RESULT.read_text(encoding="utf-8"))
    result = mapping(result_value, "result")
    if result.get("status") != STATUS:
        raise RuntimeError("result has the wrong assurance status")
    alignments = [
        mapping(item, "alignment")
        for item in values(result["alignments"], "alignments")
    ]
    channels = (
        ("maximum_matrix_frobenius_normalized", "maximum matrix Frobenius"),
        ("root_mean_square_matrix_frobenius_normalized", "RMS matrix Frobenius"),
        ("maximum_ordered_spectrum_normalized", "maximum ordered spectrum"),
        ("root_mean_square_ordered_spectrum_normalized", "RMS ordered spectrum"),
    )
    styles = {
        "identity": ("attacked / identity", "--", "s"),
        "global-unitary": ("global unitary", "-.", "D"),
        "pointwise-unitary": ("pointwise polar", ":", "^"),
        "known-inverse-oracle": ("known inverse", (0, (5, 1, 1, 1)), "v"),
    }
    figure, axes = plt.subplots(2, 2, figsize=(11.5, 8.2), sharex=True)
    for axis, (key, title) in zip(axes.flat, channels, strict=True):
        first_shells = [
            mapping(item, "shell")
            for item in values(alignments[0]["shells"], "shells")
        ]
        cost = np.asarray(
            [numeric(shell["retained_block_count"], "block count") for shell in first_shells],
            dtype=np.float64,
        )
        reference = np.asarray(
            [
                numeric(
                    mapping(shell["reference_total_errors"], "reference errors")[key],
                    key,
                )
                for shell in first_shells
            ],
            dtype=np.float64,
        )
        reference_pareto = pareto_mask(cost, reference)
        axis.plot(
            cost,
            np.maximum(reference, FLOOR),
            color="0.65",
            linewidth=0.8,
            marker="o",
            markerfacecolor="none",
            markersize=4,
            label="reference complete curve",
        )
        axis.scatter(
            cost[reference_pareto],
            np.maximum(reference[reference_pareto], FLOOR),
            color="black",
            marker="o",
            s=34,
            label="reference Pareto points",
            zorder=5,
        )
        for alignment in alignments:
            name = string(alignment["alignment"], "alignment")
            label, linestyle, marker = styles[name]
            shells = [
                mapping(item, "shell")
                for item in values(alignment["shells"], "shells")
            ]
            comparison = np.asarray(
                [
                    numeric(
                        mapping(shell["comparison_total_errors"], "comparison errors")[
                            key
                        ],
                        key,
                    )
                    for shell in shells
                ],
                dtype=np.float64,
            )
            selected = pareto_mask(cost, comparison)
            axis.plot(
                cost,
                np.maximum(comparison, FLOOR),
                color="black",
                linestyle=linestyle,
                linewidth=0.75,
                alpha=0.55,
            )
            axis.scatter(
                cost[selected],
                np.maximum(comparison[selected], FLOOR),
                facecolors="white",
                edgecolors="black",
                marker=marker,
                s=30,
                label=f"{label} Pareto",
                zorder=6,
            )
        axis.set_yscale("log")
        axis.set_title(title)
        axis.set_ylabel("total error normalized by 1 eV")
        axis.grid(which="both", alpha=0.25)
    for axis in axes[1, :]:
        axis.set_xlabel("retained complete rank-10 lattice blocks")
    axes[0, 1].legend(fontsize=7, ncol=2)
    figure.suptitle(
        "Discrete support-error Pareto frontiers\n"
        "filled/hollow emphasized markers are non-dominated observed supports"
    )
    figure.text(
        0.5,
        0.008,
        STATUS,
        ha="center",
        va="bottom",
        fontsize=7,
    )
    figure.tight_layout(rect=(0, 0.04, 1, 0.94))
    figure.savefig(PDF, bbox_inches="tight")
    figure.savefig(PNG, dpi=220, bbox_inches="tight")
    plt.close(figure)
    manifest: JsonObject = {
        "schema_version": 1,
        "status": STATUS,
        "pareto_rule": (
            "a support is retained exactly when no observed complete-shell support has "
            "both no greater block count and no greater error with at least one strict"
        ),
        "interpolation_performed": False,
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
