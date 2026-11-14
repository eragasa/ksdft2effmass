from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import NDArray

RealArray = NDArray[np.float64]
type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
RESULT = ROOT / "result.json"
FIGURES = ROOT / "figures"
STATUS = "producer-checked-development-analysis-not-independently-verified"
FLOOR = 1.0e-16
ALIGNMENT_LABELS = {
    "identity": "attacked / identity",
    "global-unitary": "global unitary",
    "pointwise-unitary": "pointwise polar",
    "known-inverse-oracle": "known inverse",
}
LINE_STYLES = {
    "identity": "--",
    "global-unitary": "-.",
    "pointwise-unitary": ":",
    "known-inverse-oracle": (0, (5, 1, 1, 1)),
}


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


def array(value: JsonValue, name: str) -> RealArray:
    return np.asarray(values(value, name), dtype=np.float64)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def footer(figure: Figure) -> None:
    figure.text(
        0.5,
        0.008,
        STATUS,
        ha="center",
        va="bottom",
        fontsize=7,
    )


def save(figure: Figure, directory: Path, stem: str) -> None:
    footer(figure)
    figure.savefig(directory / f"{stem}.pdf", bbox_inches="tight")
    figure.savefig(directory / f"{stem}.png", dpi=220, bbox_inches="tight")
    plt.close(figure)


def log_line(
    axis: Axes,
    x: RealArray,
    y: RealArray,
    *,
    label: str,
    linestyle: str | tuple[int, tuple[int, ...]] = "-",
    marker: str | None = None,
) -> None:
    below = y < FLOOR
    plotted = np.maximum(y, FLOOR)
    axis.plot(
        x,
        plotted,
        color="black",
        linestyle=linestyle,
        marker=marker,
        markersize=3.5,
        linewidth=1.25,
        label=label,
    )
    if np.any(below):
        axis.scatter(
            x[below],
            np.full(np.count_nonzero(below), FLOOR),
            marker="v",
            facecolors="none",
            edgecolors="black",
            s=28,
            zorder=5,
        )
    axis.set_yscale("log")


def alignment_records(result: JsonObject) -> list[JsonObject]:
    return [
        mapping(item, "alignment")
        for item in values(result["alignments"], "alignments")
    ]


def shell_arrays(
    alignment: JsonObject, channel: str, error_key: str
) -> tuple[RealArray, RealArray]:
    shells = [mapping(item, "shell") for item in values(alignment["shells"], "shells")]
    radius = np.asarray(
        [
            numeric(shell["physical_radius_angstrom"], "shell radius")
            for shell in shells
        ],
        dtype=np.float64,
    )
    error = np.asarray(
        [
            numeric(
                mapping(shell[f"{channel}_total_errors"], "error record")[error_key],
                error_key,
            )
            for shell in shells
        ],
        dtype=np.float64,
    )
    return radius, error


def make_schematic(result: JsonObject, directory: Path) -> None:
    operator = mapping(result["operator"], "operator")
    attack = mapping(result["attack"], "attack")
    figure, axis = plt.subplots(figsize=(10.5, 4.5))
    axis.set_xlim(0.0, 10.0)
    axis.set_ylim(0.0, 4.0)
    axis.axis("off")
    boxes = (
        (
            0.3,
            2.35,
            2.1,
            1.05,
            "Authenticated rank-10\nWannier Hamiltonian\nC6 construction field",
        ),
        (
            2.9,
            2.35,
            2.1,
            1.05,
            "Frozen depth-2\nGivens attack\n$\\pi/8$, axis harmonics",
        ),
        (5.5, 2.35, 1.8, 1.05, "Four alignment\nchannels"),
        (7.8, 2.35, 1.9, 1.05, "Finite-cyclic\nFourier blocks\n125 displacements"),
        (3.0, 0.45, 2.0, 1.05, "408 ordered\ndevelopment points\ncomplete spectra"),
        (
            5.7,
            0.45,
            2.0,
            1.05,
            "Shell support curves\n$q \\leq 48$\nno target threshold",
        ),
    )
    for x, y, width, height, text in boxes:
        axis.add_patch(
            plt.Rectangle(
                (x, y), width, height, fill=False, edgecolor="black", linewidth=1.2
            )
        )
        axis.text(x + width / 2.0, y + height / 2.0, text, ha="center", va="center")
    for start, end in (
        ((2.4, 2.88), (2.9, 2.88)),
        ((5.0, 2.88), (5.5, 2.88)),
        ((7.3, 2.88), (7.8, 2.88)),
        ((1.35, 2.35), (3.0, 1.5)),
        ((6.4, 2.35), (6.7, 1.5)),
    ):
        axis.annotate(
            "", xy=end, xytext=start, arrowprops={"arrowstyle": "->", "color": "black"}
        )
    axis.text(
        0.3,
        0.12,
        f"operator: {string(operator['identifier'], 'operator identifier')}\n"
        f"attack: {string(attack['identity'], 'attack identity')}",
        fontsize=7,
        va="bottom",
    )
    axis.set_title("Hamiltonian-only gauge-alignment/locality development experiment")
    figure.tight_layout(rect=(0, 0.05, 1, 1))
    save(figure, directory, "experiment-schematic")


def make_alignment_invariance(result: JsonObject, directory: Path) -> None:
    records = alignment_records(result)
    labels = [
        ALIGNMENT_LABELS[string(item["alignment"], "alignment")] for item in records
    ]
    metrics = (
        ("maximum_aligned_frame_defect", "aligned-frame defect"),
        ("maximum_direct_matrix_difference_ev", "direct matrix difference (eV)"),
        (
            "maximum_direct_ordered_spectrum_difference_ev",
            "complete-spectrum difference (eV)",
        ),
    )
    figure, axes = plt.subplots(1, 3, figsize=(12.5, 4.2))
    for axis, (key, title) in zip(axes, metrics, strict=True):
        y = np.asarray([numeric(item[key], key) for item in records], dtype=np.float64)
        plotted = np.maximum(y, FLOOR)
        positions = np.arange(len(records))
        axis.bar(positions, plotted, color="white", edgecolor="black", hatch="//")
        below = y < FLOOR
        if np.any(below):
            axis.scatter(
                positions[below],
                np.full(np.count_nonzero(below), FLOOR),
                marker="v",
                facecolors="none",
                edgecolors="black",
            )
        axis.set_yscale("log")
        axis.set_xticks(positions, labels, rotation=28, ha="right")
        axis.set_title(title)
        axis.grid(axis="y", which="both", alpha=0.25)
    figure.suptitle("Alignment residuals and representation invariance")
    figure.tight_layout(rect=(0, 0.05, 1, 0.93))
    save(figure, directory, "alignment-invariance")


def make_fourier_power(result: JsonObject, directory: Path) -> None:
    records = alignment_records(result)
    first = records[0]
    shells = [mapping(item, "shell") for item in values(first["shells"], "shells")]
    radius = np.asarray(
        [numeric(item["physical_radius_angstrom"], "radius") for item in shells]
    )
    reference = np.asarray(
        [
            numeric(item["reference_shell_power_per_state_ev2"], "power")
            for item in shells
        ]
    )
    reference_omitted = np.asarray(
        [
            numeric(item["reference_omitted_power_per_state_ev2"], "power")
            for item in shells
        ]
    )
    figure, axes = plt.subplots(1, 2, figsize=(11.5, 4.4))
    log_line(axes[0], radius, reference, label="reference", marker="o")
    log_line(axes[1], radius, reference_omitted, label="reference", marker="o")
    for record in records:
        name = string(record["alignment"], "alignment")
        record_shells = [
            mapping(item, "shell") for item in values(record["shells"], "shells")
        ]
        shell_power = np.asarray(
            [
                numeric(item["comparison_shell_power_per_state_ev2"], "power")
                for item in record_shells
            ]
        )
        omitted = np.asarray(
            [
                numeric(item["comparison_omitted_power_per_state_ev2"], "power")
                for item in record_shells
            ]
        )
        log_line(
            axes[0],
            radius,
            shell_power,
            label=ALIGNMENT_LABELS[name],
            linestyle=LINE_STYLES[name],
        )
        log_line(
            axes[1],
            radius,
            omitted,
            label=ALIGNMENT_LABELS[name],
            linestyle=LINE_STYLES[name],
        )
    axes[0].set_title("power assigned to each complete shell")
    axes[1].set_title("power beyond retained shell")
    for axis in axes:
        axis.set_xlabel("physical block radius (Å)")
        axis.set_ylabel("power / retained state (eV$^2$)")
        axis.grid(which="both", alpha=0.25)
    axes[1].legend(fontsize=8)
    figure.suptitle("Finite-cyclic Fourier-power redistribution")
    figure.tight_layout(rect=(0, 0.05, 1, 0.93))
    save(figure, directory, "fourier-power-redistribution")


def make_support_frontiers(result: JsonObject, directory: Path) -> None:
    records = alignment_records(result)
    channels = (
        ("maximum_matrix_frobenius_normalized", "maximum matrix Frobenius"),
        ("root_mean_square_matrix_frobenius_normalized", "RMS matrix Frobenius"),
        ("maximum_ordered_spectrum_normalized", "maximum ordered spectrum"),
        ("root_mean_square_ordered_spectrum_normalized", "RMS ordered spectrum"),
    )
    figure, axes = plt.subplots(2, 2, figsize=(11.5, 8.2), sharex=True)
    for axis, (key, title) in zip(axes.flat, channels, strict=True):
        radius, reference = shell_arrays(records[0], "reference", key)
        log_line(axis, radius, reference, label="reference", marker="o")
        for record in records:
            name = string(record["alignment"], "alignment")
            _, comparison = shell_arrays(record, "comparison", key)
            log_line(
                axis,
                radius,
                comparison,
                label=ALIGNMENT_LABELS[name],
                linestyle=LINE_STYLES[name],
            )
        axis.set_title(title)
        axis.set_ylabel("error normalized by 1 eV")
        axis.grid(which="both", alpha=0.25)
    for axis in axes[1, :]:
        axis.set_xlabel("physical block radius (Å)")
    axes[0, 1].legend(fontsize=8)
    figure.suptitle("Complete support-error curves and alignment controls")
    figure.tight_layout(rect=(0, 0.04, 1, 0.95))
    save(figure, directory, "support-error-frontiers")


def minimum_attained_radius(
    reference_error: RealArray,
    comparison_error: RealArray,
    radius: RealArray,
) -> RealArray:
    attained = np.full(reference_error.shape, np.nan, dtype=np.float64)
    for index, target in enumerate(reference_error):
        satisfying = np.flatnonzero(comparison_error <= target)
        if len(satisfying) > 0:
            attained[index] = radius[int(satisfying[0])]
    return attained


def make_equal_error_support(result: JsonObject, directory: Path) -> None:
    records = alignment_records(result)
    channels = (
        ("maximum_matrix_frobenius_normalized", "maximum matrix"),
        ("root_mean_square_matrix_frobenius_normalized", "RMS matrix"),
        ("maximum_ordered_spectrum_normalized", "maximum spectrum"),
        ("root_mean_square_ordered_spectrum_normalized", "RMS spectrum"),
    )
    figure, axes = plt.subplots(2, 2, figsize=(10.8, 8.2), sharex=True, sharey=True)
    for axis, (key, title) in zip(axes.flat, channels, strict=True):
        radius, reference_error = shell_arrays(records[0], "reference", key)
        axis.plot(radius, radius, color="0.65", linestyle="--", label="equal support")
        for record in records:
            name = string(record["alignment"], "alignment")
            _, comparison_error = shell_arrays(record, "comparison", key)
            attained = minimum_attained_radius(
                reference_error, comparison_error, radius
            )
            finite = np.isfinite(attained)
            axis.step(
                radius[finite],
                attained[finite],
                where="post",
                color="black",
                linestyle=LINE_STYLES[name],
                label=ALIGNMENT_LABELS[name],
            )
            if np.any(~finite):
                axis.scatter(
                    radius[~finite],
                    np.full(np.count_nonzero(~finite), radius[-1]),
                    marker="x",
                    color="black",
                )
        axis.set_title(title)
        axis.grid(alpha=0.25)
    for axis in axes[1, :]:
        axis.set_xlabel("reference support radius (Å)")
    for axis in axes[:, 0]:
        axis.set_ylabel("minimum comparison radius\nat equal attained error (Å)")
    axes[0, 1].legend(fontsize=8)
    figure.suptitle(
        "Equal-attained-error support projection (no interpolated crossings)"
    )
    figure.tight_layout(rect=(0, 0.04, 1, 0.95))
    save(figure, directory, "equal-attained-error-support")


def make_spectrum_equivalence(result: JsonObject, directory: Path) -> None:
    spectra = mapping(result["evaluation_spectra"], "evaluation spectra")
    reference = array(spectra["reference_rank10_ev"], "reference spectrum")
    attacked = array(spectra["attacked_rank10_ev"], "attacked spectrum")
    residual = array(
        spectra["maximum_pointwise_attack_difference_ev"], "spectrum residual"
    )
    points = np.arange(reference.shape[0], dtype=np.float64)
    figure, axes = plt.subplots(1, 2, figsize=(12.0, 4.5))
    for band in range(reference.shape[1]):
        label_reference = "reference" if band == 0 else None
        label_attacked = "attacked" if band == 0 else None
        axes[0].plot(
            points,
            reference[:, band],
            color="black",
            linewidth=0.75,
            label=label_reference,
        )
        axes[0].plot(
            points,
            attacked[:, band],
            color="0.55",
            linestyle="--",
            linewidth=0.65,
            label=label_attacked,
        )
    log_line(axes[1], points, residual, label="pointwise maximum", marker=None)
    axes[0].set_xlabel("ordered revealed-development point index")
    axes[0].set_ylabel("energy (eV)")
    axes[0].set_title("all ten represented eigenvalues")
    axes[0].legend()
    axes[1].set_xlabel("ordered revealed-development point index")
    axes[1].set_ylabel("maximum eigenvalue difference (eV)")
    axes[1].set_title("complete-spectrum invariance residual")
    axes[1].grid(which="both", alpha=0.25)
    figure.suptitle("Complete rank-10 spectrum equivalence at 408 ordered points")
    figure.tight_layout(rect=(0, 0.05, 1, 0.93))
    save(figure, directory, "complete-spectrum-equivalence")


def make_transport(result: JsonObject, directory: Path) -> None:
    records = alignment_records(result)
    labels = [
        ALIGNMENT_LABELS[string(item["alignment"], "alignment")] for item in records
    ]
    metrics = (
        ("minimum_transport_singular_value", "minimum link singular value", False),
        (
            "maximum_transport_procrustes_residual",
            "maximum link Procrustes residual",
            True,
        ),
        (
            "maximum_transport_unitarity_defect",
            "maximum transport unitarity defect",
            True,
        ),
        ("maximum_transport_rank_cutoff", "maximum applied rank cutoff", True),
        ("maximum_plaquette_phase", "maximum plaquette phase", True),
    )
    figure, axes = plt.subplots(2, 3, figsize=(12.2, 7.5))
    positions = np.arange(len(records))
    for axis, (key, title, logarithmic) in zip(axes.flat, metrics, strict=False):
        y = np.asarray([numeric(item[key], key) for item in records], dtype=np.float64)
        plotted = np.maximum(y, FLOOR) if logarithmic else y
        axis.bar(positions, plotted, color="white", edgecolor="black", hatch="..")
        if logarithmic:
            axis.set_yscale("log")
            below = y < FLOOR
            if np.any(below):
                axis.scatter(
                    positions[below],
                    np.full(np.count_nonzero(below), FLOOR),
                    marker="v",
                    facecolors="none",
                    edgecolors="black",
                )
        axis.set_xticks(positions, labels, rotation=28, ha="right")
        axis.set_title(title)
        axis.grid(axis="y", which="both", alpha=0.25)
    closure_axis = axes.flat[5]
    for index, record in enumerate(records):
        closure = array(record["maximum_absolute_closure_phases"], "closure phases")
        closure_axis.plot(
            np.arange(len(closure)),
            np.maximum(closure, FLOOR),
            color="black",
            linestyle=list(LINE_STYLES.values())[index],
            label=labels[index],
        )
        below = closure < FLOOR
        if np.any(below):
            closure_axis.scatter(
                np.arange(len(closure))[below],
                np.full(np.count_nonzero(below), FLOOR),
                marker="v",
                facecolors="none",
                edgecolors="black",
            )
    closure_axis.set_yscale("log")
    closure_axis.set_title("maximum absolute closure phase by axis")
    closure_axis.set_xlabel("periodic axis")
    closure_axis.set_xticks((0, 1, 2))
    closure_axis.grid(which="both", alpha=0.25)
    closure_axis.legend(fontsize=7)
    figure.suptitle("Frame-transport diagnostics")
    figure.tight_layout(rect=(0, 0.04, 1, 0.95))
    save(figure, directory, "transport-diagnostics")


def make_displacement_power(result: JsonObject, directory: Path) -> None:
    power = mapping(result["displacement_power"], "displacement power")
    radius = array(power["physical_radii_angstrom"], "radii")
    reference = array(power["reference_power_per_state_ev2"], "reference power")
    attacked = array(power["attacked_identity_power_per_state_ev2"], "attacked power")
    modes = np.asarray(values(power["integer_modes"], "integer modes"), dtype=np.int64)
    order = np.lexsort((modes[:, 2], modes[:, 1], modes[:, 0], radius))
    figure, axes = plt.subplots(1, 2, figsize=(12.0, 4.5))
    axes[0].scatter(
        radius,
        np.maximum(reference, FLOOR),
        facecolors="none",
        edgecolors="black",
        marker="o",
        label="reference",
    )
    axes[0].scatter(
        radius,
        np.maximum(attacked, FLOOR),
        color="black",
        marker="x",
        label="attacked / identity",
    )
    axes[0].set_yscale("log")
    axes[0].set_xlabel("physical block radius (Å)")
    axes[0].set_ylabel("block power / retained state (eV$^2$)")
    axes[0].set_title("power by physical displacement radius")
    axes[0].legend()
    axes[1].plot(
        np.arange(len(order)),
        np.maximum(reference[order], FLOOR),
        color="black",
        marker="o",
        markersize=2.5,
        linewidth=0.6,
        label="reference",
    )
    axes[1].plot(
        np.arange(len(order)),
        np.maximum(attacked[order], FLOOR),
        color="0.45",
        linestyle="--",
        marker="x",
        markersize=2.5,
        linewidth=0.6,
        label="attacked / identity",
    )
    axes[1].set_yscale("log")
    axes[1].set_xlabel("canonical displacement order (radius then integer mode)")
    axes[1].set_ylabel("block power / retained state (eV$^2$)")
    axes[1].set_title("all 125 ordinary finite-cyclic blocks")
    axes[1].legend()
    for axis in axes:
        axis.grid(which="both", alpha=0.25)
    figure.suptitle("Per-displacement finite-cyclic block power")
    figure.tight_layout(rect=(0, 0.05, 1, 0.93))
    save(figure, directory, "displacement-block-power")


def make_direct_parent(result: JsonObject, directory: Path) -> None:
    spectra = mapping(result["evaluation_spectra"], "evaluation spectra")
    represented = array(spectra["reference_rank10_ev"], "represented spectrum")
    parent = array(spectra["matched_parent_rank10_ev"], "matched parent spectrum")
    residual = array(spectra["represented_minus_matched_parent_ev"], "parent residual")
    points = np.arange(represented.shape[0], dtype=np.float64)
    point_maximum = np.max(np.abs(residual), axis=1)
    figure, axes = plt.subplots(1, 2, figsize=(12.2, 4.6))
    for band in range(represented.shape[1]):
        axes[0].plot(
            points,
            parent[:, band],
            color="0.6",
            linestyle="--",
            linewidth=0.65,
            label="matched parent" if band == 0 else None,
        )
        axes[0].plot(
            points,
            represented[:, band],
            color="black",
            linewidth=0.75,
            label="represented rank 10" if band == 0 else None,
        )
    axes[0].set_xlabel("ordered revealed-development point index")
    axes[0].set_ylabel("energy (eV; no fitted shift)")
    axes[0].set_title("injectively matched spectra")
    axes[0].legend()
    log_line(axes[1], points, point_maximum, label="maximum matched-band residual")
    axes[1].set_xlabel("ordered revealed-development point index")
    axes[1].set_ylabel("maximum absolute residual (eV)")
    axes[1].set_title("direct-parent development discrepancy")
    axes[1].grid(which="both", alpha=0.25)
    figure.suptitle("Direct-parent overlay: development evidence, not a gauge effect")
    figure.tight_layout(rect=(0, 0.05, 1, 0.93))
    save(figure, directory, "direct-parent-overlay")


def main() -> None:
    if FIGURES.exists():
        raise FileExistsError(f"refusing to overwrite retained figures: {FIGURES}")
    result_value: JsonValue = json.loads(RESULT.read_text(encoding="utf-8"))
    result = mapping(result_value, "result")
    if result.get("status") != STATUS:
        raise RuntimeError(
            "result assurance label is not the authorized producer-only status"
        )
    with tempfile.TemporaryDirectory(prefix="ksd-gauge-locality-plots-") as temporary:
        temporary_path = Path(temporary)
        make_schematic(result, temporary_path)
        make_alignment_invariance(result, temporary_path)
        make_fourier_power(result, temporary_path)
        make_support_frontiers(result, temporary_path)
        make_equal_error_support(result, temporary_path)
        make_spectrum_equivalence(result, temporary_path)
        make_transport(result, temporary_path)
        make_displacement_power(result, temporary_path)
        make_direct_parent(result, temporary_path)
        rendered = sorted(temporary_path.iterdir())
        if len(rendered) != 18:
            raise RuntimeError("renderer did not produce nine PDF and nine PNG figures")
        FIGURES.mkdir()
        for path in rendered:
            shutil.copy2(path, FIGURES / path.name)
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
            for path in sorted(FIGURES.iterdir())
        },
    }
    (FIGURES / "figure-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
