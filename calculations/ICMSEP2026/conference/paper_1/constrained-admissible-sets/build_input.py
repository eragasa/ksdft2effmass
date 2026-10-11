#!/usr/bin/env python3
"""Materialize canonical M3 input JSON from its human-readable configuration."""

from __future__ import annotations

import argparse
import hashlib
import json
import tomllib
from pathlib import Path
from typing import Never, cast

ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = ROOT.parents[4]


def fail(message: str) -> Never:
    """Reject malformed or inconsistent configuration."""
    raise ValueError(message)


def mapping(value: object, context: str) -> dict[str, object]:
    """Require a mapping with string keys."""
    if type(value) is not dict or any(type(key) is not str for key in value):
        fail(f"{context} must be a table with string keys")
    return value


def exact(value: dict[str, object], keys: set[str], context: str) -> None:
    """Require exactly the declared keys."""
    if set(value) != keys:
        fail(f"{context} fields must be exactly {sorted(keys)}")


def text(value: object, context: str) -> str:
    """Require a nonempty built-in string."""
    if type(value) is not str or not value:
        fail(f"{context} must be a nonempty string")
    return value


def number(value: object, context: str) -> float:
    """Require a finite built-in TOML number and reject booleans."""
    if type(value) not in (int, float):
        fail(f"{context} must be numeric")
    result = float(cast(int | float, value))
    if not (-float("inf") < result < float("inf")):
        fail(f"{context} must be finite")
    return result


def number_pair(value: object, context: str) -> list[float]:
    """Decode a length-two finite numeric array."""
    if type(value) is not list or len(value) != 2:
        fail(f"{context} must be a length-two array")
    return [number(value[0], f"{context}[0]"), number(value[1], f"{context}[1]")]


def numbers(value: object, context: str) -> list[float]:
    """Decode a nonempty finite numeric array."""
    if type(value) is not list or not value:
        fail(f"{context} must be a nonempty array")
    return [number(item, f"{context}[{index}]") for index, item in enumerate(value)]


def integers(value: object, context: str) -> list[int]:
    """Decode a nonempty built-in integer array."""
    if type(value) is not list or not value:
        fail(f"{context} must be a nonempty array")
    result: list[int] = []
    for index, item in enumerate(value):
        if type(item) is not int:
            fail(f"{context}[{index}] must be an integer")
        result.append(item)
    return result


def thresholds(value: object, context: str) -> dict[str, object]:
    """Decode one configured threshold pair."""
    payload = mapping(value, context)
    exact(
        payload,
        {"case_id", "spectral_rms_threshold", "operator_rms_threshold"},
        context,
    )
    return {
        "case_id": text(payload["case_id"], f"{context}.case_id"),
        "spectral_rms_threshold": number(
            payload["spectral_rms_threshold"], f"{context}.spectral_rms_threshold"
        ),
        "operator_rms_threshold": number(
            payload["operator_rms_threshold"], f"{context}.operator_rms_threshold"
        ),
    }


def canonical_json(value: object) -> bytes:
    """Return the retained canonical JSON representation."""
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def build_document(configuration_path: Path) -> dict[str, object]:
    """Build the self-contained M3 input document."""
    raw: object = tomllib.loads(configuration_path.read_text(encoding="utf-8"))
    configuration = mapping(raw, "configuration")
    exact(
        configuration,
        {
            "schema",
            "calculation_id",
            "candidate_family",
            "parameter_order",
            "energy_shift_ratio_bounds",
            "splitting_scale_bounds",
            "alignment_family",
            "alignment_angles",
            "loss_normalization",
            "compatible_witness",
            "locality_ranges",
            "separation_metric",
            "separation_resolution",
            "quadratic_absolute_tolerance",
            "verification_absolute_tolerance",
            "multiband_baseline",
            "loss_energy_scale",
            "compatible_thresholds",
            "separated_thresholds",
        },
        "configuration",
    )
    if configuration["schema"] != (
        "ksdft2effmass.periodic1d.constrained-admissible-set-configuration.v1"
    ):
        fail("unexpected configuration schema")
    baseline_reference = mapping(
        configuration["multiband_baseline"], "multiband_baseline"
    )
    exact(baseline_reference, {"input_path", "sha256"}, "multiband_baseline")
    relative_path = Path(
        text(baseline_reference["input_path"], "multiband_baseline.input_path")
    )
    if relative_path.is_absolute() or ".." in relative_path.parts:
        fail("multiband_baseline.input_path must be repository-relative")
    baseline_path = REPOSITORY_ROOT / relative_path
    baseline_bytes = baseline_path.read_bytes()
    expected_digest = text(baseline_reference["sha256"], "multiband_baseline.sha256")
    if len(expected_digest) != 64 or any(
        character not in "0123456789abcdef" for character in expected_digest
    ):
        fail("multiband_baseline.sha256 must be a lowercase SHA-256 digest")
    if hashlib.sha256(baseline_bytes).hexdigest() != expected_digest:
        fail("referenced M2 input does not match its configured SHA-256 digest")
    baseline_raw: object = json.loads(baseline_bytes)
    baseline = mapping(baseline_raw, "referenced M2 input")
    scale = mapping(configuration["loss_energy_scale"], "loss_energy_scale")
    exact(scale, {"magnitude", "unit"}, "loss_energy_scale")
    if text(scale["unit"], "loss_energy_scale.unit") != "1":
        fail("loss_energy_scale.unit must be '1'")
    scale_magnitude = number(scale["magnitude"], "loss_energy_scale.magnitude")
    if scale_magnitude <= 0.0:
        fail("loss_energy_scale.magnitude must be positive")
    parameter_order = configuration["parameter_order"]
    if parameter_order != ["energy_shift_ratio", "splitting_scale"]:
        fail("parameter_order differs from the M3 v1 contract")
    literal_controls = {
        "candidate_family": (
            "trace-plus-energy-shift-and-positive-traceless-splitting-v1"
        ),
        "alignment_family": "finite-one-global-real-rotation-v1",
        "loss_normalization": "sqrt(sum-frobenius-squared/(N*rank))/scale",
        "separation_metric": "euclidean-parameter-distance",
    }
    for name, expected in literal_controls.items():
        if text(configuration[name], name) != expected:
            fail(f"{name} differs from the M3 v1 contract")
    bounds = (
        number_pair(
            configuration["energy_shift_ratio_bounds"], "energy_shift_ratio_bounds"
        ),
        number_pair(configuration["splitting_scale_bounds"], "splitting_scale_bounds"),
    )
    if any(lower >= upper for lower, upper in bounds) or bounds[1][0] <= 0.0:
        fail("parameter bounds must be ordered with positive splitting scale")
    angles = numbers(configuration["alignment_angles"], "alignment_angles")
    if angles != sorted(set(angles)):
        fail("alignment_angles must be unique and increasing")
    locality_ranges = integers(configuration["locality_ranges"], "locality_ranges")
    if locality_ranges != sorted(set(locality_ranges)) or locality_ranges[0] < 0:
        fail("locality_ranges must be unique, increasing, and nonnegative")
    compatible_thresholds = thresholds(
        configuration["compatible_thresholds"], "compatible_thresholds"
    )
    separated_thresholds = thresholds(
        configuration["separated_thresholds"], "separated_thresholds"
    )
    if compatible_thresholds["case_id"] != "compatible":
        fail("compatible threshold case_id differs from the M3 v1 contract")
    if separated_thresholds["case_id"] != "separated":
        fail("separated threshold case_id differs from the M3 v1 contract")
    for threshold_set in (compatible_thresholds, separated_thresholds):
        if (
            number(threshold_set["spectral_rms_threshold"], "spectral threshold") <= 0.0
            or number(threshold_set["operator_rms_threshold"], "operator threshold")
            <= 0.0
        ):
            fail("all admissible-set thresholds must be positive")
    compatible_witness = number_pair(
        configuration["compatible_witness"], "compatible_witness"
    )
    if any(
        coordinate < lower or coordinate > upper
        for coordinate, (lower, upper) in zip(compatible_witness, bounds, strict=True)
    ):
        fail("compatible_witness lies outside the configured domain")
    separation_resolution = number(
        configuration["separation_resolution"], "separation_resolution"
    )
    quadratic_tolerance = number(
        configuration["quadratic_absolute_tolerance"],
        "quadratic_absolute_tolerance",
    )
    verification_tolerance = number(
        configuration["verification_absolute_tolerance"],
        "verification_absolute_tolerance",
    )
    if min(separation_resolution, quadratic_tolerance, verification_tolerance) <= 0.0:
        fail("resolution and tolerances must be positive")
    return {
        "schema": "ksdft2effmass.periodic1d.constrained-admissible-set-input.v1",
        "calculation_id": text(configuration["calculation_id"], "calculation_id"),
        "multiband_baseline": baseline,
        "candidate_family": literal_controls["candidate_family"],
        "parameter_order": parameter_order,
        "energy_shift_ratio_bounds": bounds[0],
        "splitting_scale_bounds": bounds[1],
        "alignment_family": literal_controls["alignment_family"],
        "alignment_angles": angles,
        "loss_energy_scale": {"magnitude": scale_magnitude, "unit": "1"},
        "loss_normalization": literal_controls["loss_normalization"],
        "compatible_thresholds": compatible_thresholds,
        "separated_thresholds": separated_thresholds,
        "compatible_witness": compatible_witness,
        "locality_ranges": locality_ranges,
        "separation_metric": literal_controls["separation_metric"],
        "separation_resolution": separation_resolution,
        "quadratic_absolute_tolerance": quadratic_tolerance,
        "verification_absolute_tolerance": verification_tolerance,
    }


def main() -> None:
    """Write or check the canonical derived input."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail unless input.json already equals the generated bytes",
    )
    arguments = parser.parse_args()
    generated = canonical_json(build_document(ROOT / "configuration.toml"))
    destination = ROOT / "input.json"
    if arguments.check:
        if not destination.is_file() or destination.read_bytes() != generated:
            fail("input.json is not the canonical configuration-derived document")
        print("m3_input_configuration=PASS")
        return
    destination.write_bytes(generated)
    print(f"wrote {destination}")


if __name__ == "__main__":
    main()
