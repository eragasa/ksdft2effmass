#!/usr/bin/env python3
"""Independent reconstruction of the post-hoc M3 threshold-sensitivity result."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import cast

DIRECTORY = Path(__file__).resolve().parent
REPOSITORY = DIRECTORY.parents[4]
ABSOLUTE_TOLERANCE = 1.0e-12


def sha256(path: Path) -> str:
    """Return the SHA-256 digest of one file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mapping(value: object, name: str) -> dict[str, object]:
    """Require one JSON object with string keys."""
    if type(value) is not dict or any(type(key) is not str for key in value):
        raise TypeError(f"{name} must be an object with string keys")
    return cast(dict[str, object], value)


def array(value: object, name: str) -> list[object]:
    """Require one JSON array."""
    if type(value) is not list:
        raise TypeError(f"{name} must be an array")
    return cast(list[object], value)


def text(value: object, name: str) -> str:
    """Require one nonempty built-in string."""
    if type(value) is not str or not value:
        raise TypeError(f"{name} must be a nonempty string")
    return value


def integer(value: object, name: str) -> int:
    """Require one built-in integer while rejecting Booleans."""
    if type(value) is not int:
        raise TypeError(f"{name} must be an integer")
    return value


def exact(payload: dict[str, object], keys: set[str], name: str) -> None:
    """Require exactly the declared fields."""
    if set(payload) != keys:
        raise ValueError(f"{name} fields differ from the v1 contract")


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


def finite(value: object, name: str) -> float:
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be a number")
    result = float(cast(int | float, value))
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def close(actual: float, expected: float, name: str) -> float:
    """Return a bounded absolute defect or fail closed."""
    defect = abs(actual - expected)
    if defect > ABSOLUTE_TOLERANCE:
        raise ValueError(f"{name} defect {defect} exceeds {ABSOLUTE_TOLERANCE}")
    return defect


def quadratic_terms(
    payload: object,
    name: str,
    *,
    require_alignment_angle: bool,
) -> tuple[float | None, float, float, float]:
    """Decode and validate the axis-aligned positive-quadratic premise."""
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
    text(value["channel_id"], f"{name} channel")
    center_values = array(value["center"], f"{name} center")
    matrix_values = array(value["quadratic_matrix"], f"{name} matrix")
    if len(center_values) != 2 or len(matrix_values) != 2:
        raise ValueError(f"{name} must be rank two")
    rows = [array(row, f"{name} matrix row") for row in matrix_values]
    if any(len(row) != 2 for row in rows):
        raise ValueError(f"{name} matrix must be 2x2")
    center = [finite(item, f"{name} center") for item in center_values]
    matrix = [[finite(item, f"{name} matrix") for item in row] for row in rows]
    minimum = finite(value["minimum_squared_loss"], f"{name} minimum")
    if require_alignment_angle:
        angle: float | None = finite(value["alignment_angle"], f"{name} angle")
    else:
        if value["alignment_angle"] is not None:
            raise ValueError(f"{name} must be alignment invariant")
        angle = None
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if minimum < 0.0:
        raise ValueError(f"{name} minimum squared loss must be nonnegative")
    if abs(center[0]) > ABSOLUTE_TOLERANCE:
        raise ValueError(f"{name} shift center is not zero")
    if abs(matrix[0][1] - matrix[1][0]) > ABSOLUTE_TOLERANCE:
        raise ValueError(f"{name} quadratic matrix is not symmetric")
    if matrix[0][0] <= 0.0 or matrix[1][1] <= 0.0 or determinant <= 0.0:
        raise ValueError(f"{name} quadratic matrix is not positive definite")
    if (
        abs(matrix[0][1]) > ABSOLUTE_TOLERANCE
        or abs(matrix[1][0]) > ABSOLUTE_TOLERANCE
    ):
        raise ValueError(f"{name} quadratic is not axis aligned")
    return angle, center[1], minimum, matrix[1][1]


def main() -> None:
    """Independently reconstruct the retained post-hoc sensitivity result."""
    input_payload = mapping(
        json.loads((DIRECTORY / "input.json").read_text()), "input"
    )
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
    if text(input_payload["schema"], "input schema") != (
        "ksdft2effmass.periodic1d.constrained-admissible-set-"
        "threshold-sensitivity-input.v1"
    ):
        raise ValueError("unexpected input schema")
    result = mapping(json.loads((DIRECTORY / "result.json").read_text()), "result")
    exact(
        result,
        {
            "analysis_id",
            "compatibility_transition_operator_threshold",
            "designed_markers",
            "fixed_spectral_threshold",
            "interpretation",
            "minimum_feasible_operator_threshold",
            "original_model_operator_threshold",
            "resolution_crossing_operator_threshold",
            "schema",
            "separation_resolution",
            "source_result_path",
            "source_result_sha256",
            "spectral_minimum_splitting_scale",
            "status",
            "threshold_grid",
            "transition_alignment_angle",
        },
        "result",
    )
    if text(result["schema"], "result schema") != (
        "ksdft2effmass.periodic1d.constrained-admissible-set-"
        "threshold-sensitivity-result.v1"
    ):
        raise ValueError("unexpected result schema")
    if result["status"] != "post-hoc-exploratory-reanalysis":
        raise ValueError("result does not retain its post-hoc status")
    if result["analysis_id"] != input_payload["analysis_id"]:
        raise ValueError("analysis identity differs from input")
    source_path_text = text(input_payload["source_result_path"], "source path")
    source_path = (REPOSITORY / source_path_text).resolve()
    if not source_path.is_file() or not source_path.is_relative_to(
        REPOSITORY.resolve()
    ):
        raise ValueError("source result must be a repository file")
    source_digest = sha256(source_path)
    if source_digest != text(input_payload["source_result_sha256"], "source digest"):
        raise ValueError("source result digest mismatch")
    package_manifest = source_path.parent / "SHA256SUMS"
    if sha256(package_manifest) != text(
        input_payload["source_package_sha256sums_sha256"], "manifest digest"
    ):
        raise ValueError("source package manifest digest mismatch")
    correlate_package_manifest(source_path, package_manifest)
    if (
        result["source_result_path"] != source_path_text
        or result["source_result_sha256"] != source_digest
    ):
        raise ValueError("result source correlation differs from input")

    source = mapping(json.loads(source_path.read_text()), "source result")
    exact(
        source,
        {
            "baseline_summary",
            "cases",
            "definition",
            "schema",
            "scope",
            "training_quadratic_losses",
        },
        "source result",
    )
    if source["schema"] != (
        "ksdft2effmass.periodic1d.constrained-admissible-set-result.v1"
    ):
        raise ValueError("unexpected source-result schema")
    definition = mapping(source["definition"], "source definition")
    splitting_bounds = array(
        definition["splitting_scale_bounds"], "splitting bounds"
    )
    if len(splitting_bounds) != 2:
        raise ValueError("splitting bounds must contain two values")
    lower_bound, upper_bound = [
        finite(item, "splitting bound") for item in splitting_bounds
    ]
    if lower_bound >= upper_bound:
        raise ValueError("splitting bounds must be increasing")
    quadratics = mapping(source["training_quadratic_losses"], "quadratics")
    exact(quadratics, {"operator_components", "spectral"}, "quadratics")
    _, spectral_center, spectral_minimum_loss, spectral_curvature = quadratic_terms(
        quadratics["spectral"],
        "spectral quadratic",
        require_alignment_angle=False,
    )
    spectral_threshold = finite(
        input_payload["fixed_spectral_threshold"], "spectral threshold"
    )
    if spectral_threshold <= 0.0:
        raise ValueError("spectral threshold must be positive")
    spectral_budget = spectral_threshold**2 - spectral_minimum_loss
    if spectral_budget < -ABSOLUTE_TOLERANCE:
        raise ValueError("fixed spectral admissible set is empty")
    spectral_radius = math.sqrt(max(0.0, spectral_budget) / spectral_curvature)
    spectral_minimum = max(lower_bound, spectral_center - spectral_radius)

    operators: list[tuple[float, float, float, float]] = []
    for index, component in enumerate(
        array(quadratics["operator_components"], "operator components")
    ):
        angle, center, minimum, curvature = quadratic_terms(
            component,
            f"operator quadratic {index}",
            require_alignment_angle=True,
        )
        if angle is None:
            raise ValueError("operator quadratic must have an alignment angle")
        operators.append((angle, center, minimum, curvature))
    if not operators:
        raise ValueError("operator component inventory must be nonempty")

    def maximum(threshold: float) -> tuple[float, float]:
        candidates: list[tuple[float, float]] = []
        for angle, center, minimum, curvature in operators:
            remaining = threshold**2 - minimum
            if remaining < -ABSOLUTE_TOLERANCE:
                continue
            radius = math.sqrt(max(0.0, remaining) / curvature)
            interval_lower = max(lower_bound, center - radius)
            interval_upper = min(upper_bound, center + radius)
            if interval_lower <= interval_upper + ABSOLUTE_TOLERANCE:
                candidates.append((interval_upper, angle))
        if not candidates:
            raise ValueError("operator set is empty")
        return max(candidates)

    transition_threshold, transition_angle = min(
        (
            math.sqrt(minimum + curvature * (spectral_minimum - center) ** 2),
            angle,
        )
        for angle, center, minimum, curvature in operators
    )
    separation_resolution = finite(
        definition["separation_resolution"], "separation resolution"
    )
    if separation_resolution <= 0.0:
        raise ValueError("separation resolution must be positive")
    resolution_boundary_splitting = spectral_minimum - separation_resolution
    resolution_crossing = min(
        math.sqrt(minimum + curvature * (resolution_boundary_splitting - center) ** 2)
        for _, center, minimum, curvature in operators
    )
    original_threshold = min(
        math.sqrt(minimum + curvature * (1.0 - center) ** 2)
        for _, center, minimum, curvature in operators
    )
    minimum_feasible = min(
        math.sqrt(
            minimum
            + curvature * (min(max(center, lower_bound), upper_bound) - center) ** 2
        )
        for _, center, minimum, curvature in operators
    )

    defects = [
        close(
            finite(result["fixed_spectral_threshold"], "retained spectral threshold"),
            spectral_threshold,
            "fixed spectral threshold",
        ),
        close(
            finite(
                result["spectral_minimum_splitting_scale"], "retained spectral minimum"
            ),
            spectral_minimum,
            "spectral minimum",
        ),
        close(
            finite(
                result["minimum_feasible_operator_threshold"],
                "retained feasible threshold",
            ),
            minimum_feasible,
            "minimum feasible threshold",
        ),
        close(
            finite(result["separation_resolution"], "retained resolution"),
            separation_resolution,
            "separation resolution",
        ),
        close(
            finite(
                result["resolution_crossing_operator_threshold"],
                "retained resolution crossing",
            ),
            resolution_crossing,
            "resolution crossing",
        ),
        close(
            finite(
                result["compatibility_transition_operator_threshold"],
                "retained transition",
            ),
            transition_threshold,
            "compatibility transition",
        ),
        close(
            finite(result["transition_alignment_angle"], "retained transition angle"),
            transition_angle,
            "transition angle",
        ),
        close(
            finite(
                result["original_model_operator_threshold"],
                "retained original threshold",
            ),
            original_threshold,
            "original-model threshold",
        ),
    ]

    threshold_count = integer(
        input_payload["operator_threshold_count"], "operator threshold count"
    )
    threshold_minimum = finite(
        input_payload["operator_threshold_minimum"], "minimum threshold"
    )
    threshold_maximum = finite(
        input_payload["operator_threshold_maximum"], "maximum threshold"
    )
    if threshold_count < 2 or threshold_minimum >= threshold_maximum:
        raise ValueError("threshold grid must be increasing and nontrivial")
    rows = [
        mapping(item, f"threshold row {index}")
        for index, item in enumerate(array(result["threshold_grid"], "threshold grid"))
    ]
    if len(rows) != threshold_count:
        raise ValueError("threshold-grid length mismatch")
    row_keys = {
        "active_alignment_angle",
        "disposition",
        "exact_set_separation",
        "operator_maximum_splitting_scale",
        "operator_threshold",
    }
    for index, row in enumerate(rows):
        exact(row, row_keys, f"threshold row {index}")
        threshold = finite(row["operator_threshold"], "row threshold")
        expected_threshold = threshold_minimum + index * (
            threshold_maximum - threshold_minimum
        ) / (len(rows) - 1)
        defects.append(close(threshold, expected_threshold, "threshold coordinate"))
        operator_upper, angle = maximum(threshold)
        separation = max(0.0, spectral_minimum - operator_upper)
        defects.append(
            close(
                finite(row["operator_maximum_splitting_scale"], "operator maximum"),
                operator_upper,
                "operator maximum",
            )
        )
        defects.append(
            close(
                finite(row["exact_set_separation"], "set separation"),
                separation,
                "set separation",
            )
        )
        defects.append(
            close(
                finite(row["active_alignment_angle"], "active angle"),
                angle,
                "active angle",
            )
        )
        if separation > separation_resolution:
            expected_disposition = "certified-separated"
        elif separation > 0.0:
            expected_disposition = "positive-separation-below-resolution"
        else:
            expected_disposition = "compatible-witness"
        if row["disposition"] != expected_disposition:
            raise ValueError("disposition mismatch")

    marker_thresholds = (
        0.31,
        transition_threshold,
        original_threshold,
        0.33,
    )
    markers = [
        mapping(item, f"marker {index}")
        for index, item in enumerate(array(result["designed_markers"], "markers"))
    ]
    if len(markers) != len(marker_thresholds):
        raise ValueError("designed-marker length mismatch")
    marker_keys = {
        "active_alignment_angle",
        "exact_set_separation",
        "operator_maximum_splitting_scale",
        "operator_threshold",
    }
    for index, (marker, threshold) in enumerate(
        zip(markers, marker_thresholds, strict=True)
    ):
        exact(marker, marker_keys, f"marker {index}")
        defects.append(
            close(
                finite(marker["operator_threshold"], "marker threshold"),
                threshold,
                "marker threshold",
            )
        )
        operator_upper, angle = maximum(threshold)
        defects.extend(
            (
                close(
                    finite(
                        marker["operator_maximum_splitting_scale"],
                        "marker operator maximum",
                    ),
                    operator_upper,
                    "marker operator maximum",
                ),
                close(
                    finite(marker["exact_set_separation"], "marker separation"),
                    max(0.0, spectral_minimum - operator_upper),
                    "marker separation",
                ),
                close(
                    finite(marker["active_alignment_angle"], "marker angle"),
                    angle,
                    "marker angle",
                ),
            )
        )
    text(result["interpretation"], "interpretation")

    output = {
        "schema": (
            "ksdft2effmass.periodic1d.constrained-admissible-set-"
            "threshold-sensitivity-verification.v1"
        ),
        "status": "verified",
        "absolute_tolerance": ABSOLUTE_TOLERANCE,
        "maximum_absolute_defect": max(defects),
        "source_result_sha256": sha256(source_path),
        "checks": [
            "source-digests",
            "source-manifest-correlation",
            "post-hoc-status",
            "quadratic-premises",
            "spectral-boundary",
            "minimum-feasible-threshold",
            "resolution-crossing",
            "compatibility-transition",
            "original-model-threshold",
            "complete-threshold-grid",
            "designed-markers",
            "active-alignment-components",
            "dispositions",
        ],
    }
    (DIRECTORY / "verification.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
