#!/usr/bin/env python3
"""Post-hoc analytic operator-threshold sensitivity for the sealed M3 result."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import TextIO, cast

import matplotlib
import numpy as np

matplotlib.use("Agg")
from matplotlib import pyplot as plt

DIRECTORY = Path(__file__).resolve().parent
REPOSITORY = DIRECTORY.parents[4]
INPUT_PATH = DIRECTORY / "input.json"
RESULT_PATH = DIRECTORY / "result.json"
FIGURE_DATA_PATH = DIRECTORY / "figure-data.csv"
FIGURE_PATH = DIRECTORY / "operator-threshold-sensitivity.png"
REPORT_PATH = DIRECTORY / "report.md"
SOFTWARE_PATH = DIRECTORY / "software.json"
TOLERANCE = 1.0e-12


def mapping(value: object, name: str) -> dict[str, object]:
    """Return a string-keyed mapping or fail closed."""
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise TypeError(f"{name} must be an object with string keys")
    return cast(dict[str, object], value)


def array(value: object, name: str) -> list[object]:
    """Return a JSON array or fail closed."""
    if not isinstance(value, list):
        raise TypeError(f"{name} must be an array")
    return cast(list[object], value)


def number(value: object, name: str) -> float:
    """Return a finite built-in JSON number while rejecting Booleans."""
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be a number")
    result = float(cast(int | float, value))
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def integer(value: object, name: str) -> int:
    """Return a built-in integer while rejecting Booleans."""
    if type(value) is not int:
        raise TypeError(f"{name} must be an integer")
    return value


def text(value: object, name: str) -> str:
    """Return a nonempty built-in string."""
    if type(value) is not str or not value:
        raise TypeError(f"{name} must be a nonempty string")
    return value


def exact(payload: dict[str, object], keys: set[str], name: str) -> None:
    """Require one exact key set."""
    if set(payload) != keys:
        raise ValueError(f"{name} has unexpected keys")


def sha256(path: Path) -> str:
    """Return the SHA-256 digest of one file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def correlate_package_manifest(source_path: Path, manifest_path: Path) -> None:
    """Require the package manifest to bind the exact consumed result bytes."""
    entries: dict[str, str] = {}
    for line_number, line in enumerate(
        manifest_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        parts = line.split("  ", maxsplit=1)
        if (
            len(parts) != 2
            or len(parts[0]) != 64
            or any(character not in "0123456789abcdef" for character in parts[0])
            or not parts[1]
        ):
            raise ValueError(f"malformed source manifest line {line_number}")
        digest, relative_path = parts
        if relative_path in entries:
            raise ValueError("source package manifest contains duplicate paths")
        entries[relative_path] = digest
    retained_digest = entries.get(source_path.name)
    if retained_digest is None:
        raise ValueError("source package manifest does not bind the source result")
    if retained_digest != sha256(source_path):
        raise ValueError("source package manifest/result correlation mismatch")


def quadratic(payload: object, name: str) -> dict[str, object]:
    """Strictly decode the retained axis-aligned quadratic fields."""
    value = mapping(payload, name)
    exact(
        value,
        {
            "alignment_angle",
            "center",
            "channel_id",
            "minimum_squared_loss",
            "quadratic_matrix",
        },
        name,
    )
    center_values = array(value["center"], f"{name} center")
    matrix_values = array(value["quadratic_matrix"], f"{name} matrix")
    if len(center_values) != 2 or len(matrix_values) != 2:
        raise ValueError(f"{name} must be rank two")
    rows = [array(row, f"{name} matrix row") for row in matrix_values]
    if any(len(row) != 2 for row in rows):
        raise ValueError(f"{name} matrix must be 2x2")
    center = [number(item, f"{name} center") for item in center_values]
    matrix = [[number(item, f"{name} matrix") for item in row] for row in rows]
    minimum = number(value["minimum_squared_loss"], f"{name} minimum")
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if minimum < 0.0:
        raise ValueError(f"{name} minimum squared loss must be nonnegative")
    if abs(matrix[0][1] - matrix[1][0]) > TOLERANCE:
        raise ValueError(f"{name} quadratic matrix is not symmetric")
    if matrix[0][0] <= 0.0 or matrix[1][1] <= 0.0 or determinant <= 0.0:
        raise ValueError(f"{name} quadratic matrix is not positive definite")
    if abs(matrix[0][1]) > TOLERANCE or abs(matrix[1][0]) > TOLERANCE:
        raise ValueError(f"{name} is not axis aligned within tolerance")
    if abs(center[0]) > TOLERANCE:
        raise ValueError(f"{name} shift center is not zero within tolerance")
    return {
        "alignment_angle": value["alignment_angle"],
        "center": center,
        "matrix": matrix,
        "minimum": minimum,
    }


def accepted_lambda_interval(
    loss: dict[str, object],
    threshold: float,
    bounds: tuple[float, float],
) -> tuple[float, float] | None:
    """Return the accepted splitting interval at the zero-shift center."""
    center = cast(list[float], loss["center"])
    matrix = cast(list[list[float]], loss["matrix"])
    remaining = threshold * threshold - cast(float, loss["minimum"])
    if remaining < -TOLERANCE:
        return None
    radius = math.sqrt(max(0.0, remaining) / matrix[1][1])
    lower = max(bounds[0], center[1] - radius)
    upper = min(bounds[1], center[1] + radius)
    if lower > upper + TOLERANCE:
        return None
    return (lower, upper)


def operator_maximum(
    losses: list[dict[str, object]],
    threshold: float,
    bounds: tuple[float, float],
) -> tuple[float, float] | None:
    """Return the maximum accepted splitting and owning angle."""
    candidates: list[tuple[float, float]] = []
    for loss in losses:
        interval = accepted_lambda_interval(loss, threshold, bounds)
        if interval is None:
            continue
        angle = number(loss["alignment_angle"], "operator angle")
        candidates.append((interval[1], angle))
    return max(candidates) if candidates else None


def package_version(name: str) -> str:
    """Return one installed package version or an explicit unavailable marker."""
    try:
        return version(name)
    except PackageNotFoundError:
        return "unavailable"


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write deterministic human-readable JSON."""
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def write_csv(stream: TextIO, rows: list[dict[str, object]]) -> None:
    """Write deterministic LF-terminated figure data."""
    fields = [
        "operator_threshold",
        "operator_maximum_splitting_scale",
        "exact_set_separation",
        "disposition",
        "active_alignment_angle",
    ]
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(
            {
                key: format(value, ".17g") if isinstance(value, float) else value
                for key, value in row.items()
            }
        )


def main() -> None:
    """Reconstruct the threshold transition and retain its post-hoc diagram."""
    input_payload = mapping(json.loads(INPUT_PATH.read_text()), "input")
    exact(
        input_payload,
        {
            "analysis_id",
            "fixed_spectral_threshold",
            "operator_threshold_count",
            "operator_threshold_maximum",
            "operator_threshold_minimum",
            "schema",
            "source_package_sha256sums_sha256",
            "source_result_path",
            "source_result_sha256",
        },
        "input",
    )
    if text(input_payload["schema"], "schema") != (
        "ksdft2effmass.periodic1d.constrained-admissible-set-"
        "threshold-sensitivity-input.v1"
    ):
        raise ValueError("unexpected input schema")
    source_path_text = text(input_payload["source_result_path"], "source path")
    source_path = (REPOSITORY / source_path_text).resolve()
    if not source_path.is_file() or not source_path.is_relative_to(
        REPOSITORY.resolve()
    ):
        raise ValueError("source result must be a repository file")
    if sha256(source_path) != text(
        input_payload["source_result_sha256"], "source digest"
    ):
        raise ValueError("source result digest mismatch")
    package_manifest = source_path.parent / "SHA256SUMS"
    if sha256(package_manifest) != text(
        input_payload["source_package_sha256sums_sha256"], "package digest"
    ):
        raise ValueError("source package manifest digest mismatch")
    correlate_package_manifest(source_path, package_manifest)

    source = mapping(json.loads(source_path.read_text()), "source result")
    quadratics = mapping(source["training_quadratic_losses"], "quadratics")
    spectral = quadratic(quadratics["spectral"], "spectral quadratic")
    operator_losses = [
        quadratic(item, "operator quadratic")
        for item in array(quadratics["operator_components"], "operator components")
    ]
    definition = mapping(source["definition"], "definition")
    splitting_bounds_values = array(
        definition["splitting_scale_bounds"], "splitting bounds"
    )
    if len(splitting_bounds_values) != 2:
        raise ValueError("splitting bounds must contain two values")
    splitting_bounds = (
        number(splitting_bounds_values[0], "lower splitting bound"),
        number(splitting_bounds_values[1], "upper splitting bound"),
    )
    spectral_threshold = number(
        input_payload["fixed_spectral_threshold"], "spectral threshold"
    )
    spectral_interval = accepted_lambda_interval(
        spectral, spectral_threshold, splitting_bounds
    )
    if spectral_interval is None:
        raise ValueError("fixed spectral admissible set is empty")
    spectral_minimum = spectral_interval[0]

    minimum_operator_threshold = min(
        math.sqrt(
            cast(float, loss["minimum"])
            + cast(list[list[float]], loss["matrix"])[1][1]
            * (
                min(
                    max(cast(list[float], loss["center"])[1], splitting_bounds[0]),
                    splitting_bounds[1],
                )
                - cast(list[float], loss["center"])[1]
            )
            ** 2
        )
        for loss in operator_losses
    )
    transition_candidates = []
    for loss in operator_losses:
        center = cast(list[float], loss["center"])
        matrix = cast(list[list[float]], loss["matrix"])
        transition_candidates.append(
            (
                math.sqrt(
                    cast(float, loss["minimum"])
                    + matrix[1][1] * (spectral_minimum - center[1]) ** 2
                ),
                number(loss["alignment_angle"], "operator angle"),
            )
        )
    transition_threshold, transition_angle = min(transition_candidates)
    separation_resolution = number(
        definition["separation_resolution"], "separation resolution"
    )
    resolution_boundary_splitting = spectral_minimum - separation_resolution
    resolution_candidates = []
    for loss in operator_losses:
        center = cast(list[float], loss["center"])
        matrix = cast(list[list[float]], loss["matrix"])
        resolution_candidates.append(
            math.sqrt(
                cast(float, loss["minimum"])
                + matrix[1][1] * (resolution_boundary_splitting - center[1]) ** 2
            )
        )
    resolution_crossing_threshold = min(resolution_candidates)
    original_parameter_threshold = min(
        math.sqrt(
            cast(float, loss["minimum"])
            + cast(list[list[float]], loss["matrix"])[1][1]
            * (1.0 - cast(list[float], loss["center"])[1]) ** 2
        )
        for loss in operator_losses
    )

    threshold_minimum = number(
        input_payload["operator_threshold_minimum"], "operator threshold minimum"
    )
    threshold_maximum = number(
        input_payload["operator_threshold_maximum"], "operator threshold maximum"
    )
    threshold_count = integer(
        input_payload["operator_threshold_count"], "operator threshold count"
    )
    if threshold_count < 2 or threshold_minimum >= threshold_maximum:
        raise ValueError("threshold grid must be increasing and nontrivial")
    thresholds = np.linspace(threshold_minimum, threshold_maximum, threshold_count)
    rows: list[dict[str, object]] = []
    for threshold_value in thresholds:
        threshold = float(threshold_value)
        maximum = operator_maximum(operator_losses, threshold, splitting_bounds)
        if maximum is None:
            raise ValueError("plotted threshold grid contains an empty operator set")
        operator_upper, angle = maximum
        separation = max(0.0, spectral_minimum - operator_upper)
        if separation > separation_resolution:
            disposition = "certified-separated"
        elif separation > 0.0:
            disposition = "positive-separation-below-resolution"
        else:
            disposition = "compatible-witness"
        rows.append(
            {
                "operator_threshold": threshold,
                "operator_maximum_splitting_scale": operator_upper,
                "exact_set_separation": separation,
                "disposition": disposition,
                "active_alignment_angle": angle,
            }
        )

    marker_rows = []
    for threshold in (0.31, transition_threshold, original_parameter_threshold, 0.33):
        maximum = operator_maximum(operator_losses, threshold, splitting_bounds)
        if maximum is None:
            raise ValueError("marker threshold has an empty operator set")
        marker_rows.append(
            {
                "operator_threshold": threshold,
                "operator_maximum_splitting_scale": maximum[0],
                "exact_set_separation": max(0.0, spectral_minimum - maximum[0]),
                "active_alignment_angle": maximum[1],
            }
        )

    result: dict[str, object] = {
        "analysis_id": text(input_payload["analysis_id"], "analysis id"),
        "schema": (
            "ksdft2effmass.periodic1d.constrained-admissible-set-"
            "threshold-sensitivity-result.v1"
        ),
        "status": "post-hoc-exploratory-reanalysis",
        "source_result_path": source_path_text,
        "source_result_sha256": sha256(source_path),
        "fixed_spectral_threshold": spectral_threshold,
        "spectral_minimum_splitting_scale": spectral_minimum,
        "minimum_feasible_operator_threshold": minimum_operator_threshold,
        "separation_resolution": separation_resolution,
        "resolution_crossing_operator_threshold": resolution_crossing_threshold,
        "compatibility_transition_operator_threshold": transition_threshold,
        "transition_alignment_angle": transition_angle,
        "original_model_operator_threshold": original_parameter_threshold,
        "designed_markers": marker_rows,
        "threshold_grid": rows,
        "interpretation": (
            "Exact only for the frozen axis-aligned two-parameter quadratics, "
            "compact domain, fixed spectral threshold, and nine constant rotations."
        ),
    }
    write_json(RESULT_PATH, result)
    with FIGURE_DATA_PATH.open("w", encoding="utf-8", newline="") as stream:
        write_csv(stream, rows)

    x = np.asarray([cast(float, row["operator_threshold"]) for row in rows])
    y = np.asarray([cast(float, row["exact_set_separation"]) for row in rows])
    fig, axis = plt.subplots(figsize=(7.2, 4.4), constrained_layout=True)
    axis.axvspan(
        threshold_minimum,
        resolution_crossing_threshold,
        color="#d95f02",
        alpha=0.12,
        label="resolved separation",
    )
    axis.axvspan(
        resolution_crossing_threshold,
        transition_threshold,
        color="#e9c46a",
        alpha=0.14,
        label="positive, below resolution",
    )
    axis.axvspan(
        transition_threshold,
        threshold_maximum,
        color="#1b9e77",
        alpha=0.10,
        label="compatible",
    )
    axis.plot(x, y, color="#264653", linewidth=2.2, label=r"exact $\delta^*$")
    axis.axhline(
        separation_resolution,
        color="#6c757d",
        linestyle="--",
        label=f"resolution {separation_resolution:.2f}",
    )
    axis.axvline(0.31, color="#d95f02", linestyle=":", linewidth=1.8)
    axis.axvline(0.33, color="#1b9e77", linestyle=":", linewidth=1.8)
    axis.axvline(
        transition_threshold,
        color="#111111",
        linestyle="--",
        linewidth=1.5,
        label=f"transition {transition_threshold:.6f}",
    )
    axis.scatter(
        [0.31, 0.33],
        [
            marker_rows[0]["exact_set_separation"],
            marker_rows[-1]["exact_set_separation"],
        ],
        color=["#d95f02", "#1b9e77"],
        zorder=5,
    )
    axis.annotate(
        "designed separated case",
        (0.31, marker_rows[0]["exact_set_separation"]),
        xytext=(8, 9),
        textcoords="offset points",
        fontsize=8,
    )
    axis.annotate(
        "designed compatible case",
        (0.33, marker_rows[-1]["exact_set_separation"]),
        xytext=(-105, 12),
        textcoords="offset points",
        fontsize=8,
    )
    axis.set_xlabel(r"operator threshold $\tau_O$ at fixed $\tau_S=0.03$")
    axis.set_ylabel(r"exact admissible-set distance $\delta^*$")
    axis.set_title("Post-hoc M3 operator-threshold sensitivity")
    axis.set_xlim(threshold_minimum, threshold_maximum)
    axis.set_ylim(bottom=-0.004)
    axis.grid(alpha=0.22)
    axis.legend(fontsize=8, loc="upper right")
    fig.savefig(FIGURE_PATH, dpi=180)
    plt.close(fig)

    REPORT_PATH.write_text(
        "\n".join(
            [
                "# Post-hoc M3 threshold sensitivity",
                "",
                (
                    "This exploratory reanalysis uses the sealed M3 training "
                    "quadratics; it is not part of the prospective confirmatory "
                    "protocol."
                ),
                "",
                f"- fixed spectral threshold: `{spectral_threshold:.17g}`;",
                (
                    "- minimum feasible operator threshold: "
                    f"`{minimum_operator_threshold:.17g}`;"
                ),
                (
                    f"- resolution crossing: `{resolution_crossing_threshold:.17g}` "
                    f"for resolution `{separation_resolution:.17g}`;"
                ),
                (
                    f"- compatibility transition: `{transition_threshold:.17g}` at "
                    f"angle `{transition_angle:.17g}`;"
                ),
                (
                    "- operator threshold needed to admit the original model: "
                    f"`{original_parameter_threshold:.17g}`;"
                ),
                (
                    "- exact separation at `0.31`: "
                    f"`{marker_rows[0]['exact_set_separation']:.17g}`; and"
                ),
                "- exact separation at `0.33`: `0`.",
                "",
                (
                    "The designed thresholds lie on opposite sides of the analytic "
                    "transition. This describes only the frozen synthetic family "
                    "and does not calibrate physical tolerances."
                ),
                "",
            ]
        ),
        encoding="utf-8",
    )
    write_json(
        SOFTWARE_PATH,
        {
            "schema": "ksdft2effmass.synthetic-analysis-software.v1",
            "execution_scope": "local-post-hoc-no-external-calculator",
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "executable": sys.executable,
            "packages": {
                "matplotlib": package_version("matplotlib"),
                "numpy": package_version("numpy"),
            },
        },
    )


if __name__ == "__main__":
    main()
