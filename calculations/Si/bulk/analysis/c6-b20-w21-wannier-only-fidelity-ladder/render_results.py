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
RESULT = ROOT / "result-v2.json"
SURFACE = (
    ROOT.parent / "c6-b20-w21-refitted-ws-shell-witness-posthoc/witness-surface-v2.json"
)
FIGURES = ROOT / "figures"
LADDER_PDF = FIGURES / "wannier-fidelity-ladder.pdf"
LADDER_PNG = FIGURES / "wannier-fidelity-ladder.png"
FEATURE_PDF = FIGURES / "source-relative-feature-fidelity.pdf"
FEATURE_PNG = FIGURES / "source-relative-feature-fidelity.png"
MANIFEST = FIGURES / "figure-manifest.json"
STATUS = "wannier-only-fidelity-ladder-producer-checked-development-not-independently-verified"
MODELS = ("H-shell-05", "H-shell-10", "H-shell-16")
COLORS = ("#0072B2", "#E69F00", "#009E73")


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


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    for path in (LADDER_PDF, LADDER_PNG, FEATURE_PDF, FEATURE_PNG, MANIFEST):
        if path.exists():
            raise FileExistsError(
                f"refusing to overwrite retained figure artifact: {path}"
            )
    result_value: JsonValue = json.loads(RESULT.read_text(encoding="utf-8"))
    result = mapping(result_value, "result")
    if result.get("status") != STATUS:
        raise RuntimeError("result has the wrong assurance status")
    surface_value: JsonValue = json.loads(SURFACE.read_text(encoding="utf-8"))
    surface = mapping(surface_value, "surface")
    retained = {
        string(mapping(item, "example")["shell_id"], "shell id"): mapping(
            item, "example"
        )
        for item in values(
            surface["illustrative_threshold_witnesses"], "surface examples"
        )
        if mapping(item, "example").get("witness_found") is True
    }
    meshes = [
        mapping(item, "dense mesh")
        for item in values(result["level_2_dense_meshes"], "dense meshes")
    ]
    exact = mapping(result["level_1_exact_operator"], "exact operator")

    spectral_x = np.arange(4, dtype=np.float64)
    operator_x = np.arange(5, dtype=np.float64)
    figure, axes = plt.subplots(1, 2, figsize=(11.0, 4.7), layout="constrained")
    for model, color in zip(MODELS, COLORS, strict=True):
        example = retained[model]
        spectral = [numeric(example["attained_tau_1"], "retained tau_1")]
        operator = [numeric(example["attained_tau_2"], "retained tau_2")]
        sampled_operator: list[float] = []
        for mesh in meshes:
            record = mapping(
                mapping(mesh["models"], "mesh models")[model], "mesh model"
            )
            spectral.append(
                numeric(
                    mapping(
                        record["ordered_spectrum_all_bands"], "spectral statistics"
                    )["rms_ev"],
                    "spectral RMS",
                )
            )
            sampled_operator.append(
                numeric(
                    mapping(record["sampled_operator"], "sampled operator")[
                        "rms_frobenius_per_state_ev"
                    ],
                    "operator RMS",
                )
            )
        operator.append(
            numeric(
                mapping(exact[model], "exact operator")[
                    "normalized_brillouin_zone_rms_frobenius_per_state_ev"
                ],
                "exact operator RMS",
            )
        )
        operator.extend(sampled_operator)
        axes[0].plot(
            spectral_x,
            spectral,
            marker="o",
            linewidth=1.8,
            color=color,
            label=model,
        )
        axes[1].plot(
            operator_x,
            operator,
            marker="o",
            linewidth=1.8,
            color=color,
            label=model,
        )
    axes[0].set_yscale("log")
    axes[0].set_xticks(spectral_x, ("fitted 408", r"$12^3$", r"$20^3$", r"$32^3$"))
    axes[0].set_ylabel("RMS ordered-spectrum error (eV)")
    axes[0].set_title("Spectral fidelity without refitting")
    axes[1].set_yscale("log")
    axes[1].set_xticks(
        operator_x,
        ("fitted 408", "Parseval", r"$12^3$", r"$20^3$", r"$32^3$"),
    )
    axes[1].set_ylabel("RMS Frobenius error per state (eV)")
    axes[1].set_title("Operator fidelity without refitting")
    for axis in axes:
        axis.grid(which="both", alpha=0.22)
        axis.legend(fontsize=8)
    figure.suptitle(
        "Frozen Wannier-shell witnesses across increasing evaluation fidelity\n"
        "producer-checked development; not independently verified"
    )
    figure.savefig(LADDER_PDF, bbox_inches="tight")
    figure.savefig(LADDER_PNG, dpi=240, bbox_inches="tight")
    plt.close(figure)

    features = mapping(result["level_3_source_relative_features"], "features")
    gap_change = np.asarray(
        [
            abs(
                numeric(
                    mapping(features[model], "feature model")["indirect_gap_change_ev"],
                    "gap change",
                )
            )
            * 1000.0
            for model in MODELS
        ],
        dtype=np.float64,
    )
    displacement = np.asarray(
        [
            numeric(
                mapping(features[model], "feature model")[
                    "maximum_valley_displacement_inverse_angstrom"
                ],
                "valley displacement",
            )
            for model in MODELS
        ],
        dtype=np.float64,
    )
    hessian = np.asarray(
        [
            numeric(
                mapping(features[model], "feature model")[
                    "maximum_hessian_frobenius_relative_change"
                ],
                "Hessian change",
            )
            * 100.0
            for model in MODELS
        ],
        dtype=np.float64,
    )
    mass = np.asarray(
        [
            numeric(
                mapping(features[model], "feature model")[
                    "maximum_principal_mass_absolute_relative_change"
                ],
                "mass change",
            )
            * 100.0
            for model in MODELS
        ],
        dtype=np.float64,
    )
    x = np.arange(len(MODELS), dtype=np.float64)
    figure, axes = plt.subplots(2, 2, figsize=(10.2, 7.3), layout="constrained")
    panels = (
        (axes[0, 0], gap_change, "|indirect-gap change| (meV)"),
        (axes[0, 1], displacement, r"maximum valley displacement ($\AA^{-1}$)"),
        (axes[1, 0], hessian, "maximum Hessian relative change (%)"),
        (axes[1, 1], mass, "maximum principal-mass relative change (%)"),
    )
    for axis, data, ylabel in panels:
        bars = axis.bar(x, data, color=COLORS, edgecolor="black", linewidth=0.55)
        axis.set_xticks(x, MODELS)
        axis.set_ylabel(ylabel)
        axis.grid(axis="y", alpha=0.22)
        axis.bar_label(bars, fmt="%.3g", padding=3, fontsize=8)
    figure.suptitle(
        "Source-relative feature fidelity of frozen Wannier-shell witnesses\n"
        "full C6-B20-W21 Wannier operator is the reference, not DFT"
    )
    figure.savefig(FEATURE_PDF, bbox_inches="tight")
    figure.savefig(FEATURE_PNG, dpi=240, bbox_inches="tight")
    plt.close(figure)

    manifest: JsonObject = {
        "schema_version": 1,
        "status": STATUS,
        "result": identity(RESULT),
        "retained_408_surface": identity(SURFACE),
        "renderer": identity(Path(__file__)),
        "figures": {
            path.name: identity(path)
            for path in (LADDER_PDF, LADDER_PNG, FEATURE_PDF, FEATURE_PNG)
        },
    }
    MANIFEST.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
