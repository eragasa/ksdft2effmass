#!/usr/bin/env python3
"""Independently audit retained mass conventions and cyclic-mode conversion records."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import cast

import numpy as np
from numpy.typing import NDArray

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]
type IntegerMode = tuple[int, int, int]
type Float64Array = NDArray[np.float64]

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[4]
MASS_RESULT = (
    REPOSITORY / "calculations/Si/bulk/analysis/"
    "c6-b20-w21-wannier-only-comprehensive-band-edge/result.json"
)
GAUGE_RESULT = (
    REPOSITORY / "calculations/Si/bulk/analysis/"
    "c6-b20-w21-gauge-alignment-locality/result.json"
)
MASS_RESULT_SHA256 = "533dfcbed4883793bb84d1a13d1a8f62f7bb7f99b02d3ab07bb3ea99f78b0764"
GAUGE_RESULT_SHA256 = "0b802463af64be191b3fdedc07f732120de735efce227d1ae94cd6225f1b3ea4"
MODEL_NAMES = ("full-source", "H-shell-05", "H-shell-10", "H-shell-16")
VALLEY_LABELS = ("+x", "+y", "+z", "-x", "-y", "-z")
PRIMARY_STEP = 0.002
ABSOLUTE_TOLERANCE = 1.0e-12
CONSTRUCTION_SIZE = 6
NEGATIVE_NYQUIST = -CONSTRUCTION_SIZE // 2


def sha256_bytes(content: bytes) -> str:
    """Return the SHA-256 identity of one byte string."""
    return hashlib.sha256(content).hexdigest()


def canonical_json(payload: JsonObject) -> bytes:
    """Encode one deterministic JSON object."""
    return (
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")


def read_authenticated(path: Path, expected_sha256: str) -> JsonObject:
    """Authenticate and decode one retained JSON object."""
    content = path.read_bytes()
    observed = sha256_bytes(content)
    if observed != expected_sha256:
        raise ValueError(f"source identity differs for {path}: {observed}")
    value = cast(JsonValue, json.loads(content))
    if type(value) is not dict:
        raise ValueError(f"{path} must contain one JSON object")
    return value


def require_object(value: JsonValue, name: str) -> JsonObject:
    """Return one exact JSON object."""
    if type(value) is not dict:
        raise ValueError(f"{name} must be an object")
    return value


def require_list(value: JsonValue, name: str) -> list[JsonValue]:
    """Return one exact JSON array."""
    if type(value) is not list:
        raise ValueError(f"{name} must be an array")
    return value


def require_string(value: JsonValue, name: str) -> str:
    """Return one exact nonempty JSON string."""
    if type(value) is not str or not value:
        raise ValueError(f"{name} must be a nonempty string")
    return value


def require_float(value: JsonValue, name: str) -> float:
    """Return one finite JSON real number without admitting booleans."""
    if type(value) not in {int, float}:
        raise ValueError(f"{name} must be a real number")
    result = float(cast(int | float, value))
    if not np.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def real_array(value: JsonValue, name: str, shape: tuple[int, ...]) -> Float64Array:
    """Return one finite real array of the declared shape."""
    array = np.asarray(require_list(value, name), dtype=np.float64)
    if array.shape != shape or not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must have finite shape {shape}")
    return array


def matrix_maximum_absolute(value: Float64Array) -> float:
    """Return one maximum absolute array entry."""
    return float(np.max(np.abs(value)))


def primary_stencil(valley: JsonObject, name: str) -> JsonObject:
    """Return the exact retained primary curvature stencil."""
    matches: list[JsonObject] = []
    for index, value in enumerate(
        require_list(valley.get("stencils"), f"{name}.stencils")
    ):
        stencil = require_object(value, f"{name}.stencils[{index}]")
        if (
            require_float(
                stencil.get("step_inverse_angstrom"),
                f"{name}.stencils[{index}].step",
            )
            == PRIMARY_STEP
        ):
            matches.append(stencil)
    if len(matches) != 1:
        raise ValueError(f"{name} must retain exactly one primary stencil")
    return matches[0]


def audit_mass_conventions(payload: JsonObject) -> JsonObject:
    """Recompute all retained valley and equal-population mass conventions."""
    electron_edge = require_object(payload.get("electron_edge"), "electron_edge")
    model_records: list[JsonValue] = []
    global_maximum = 0.0
    for model_name in MODEL_NAMES:
        model = require_object(electron_edge.get(model_name), model_name)
        valleys = require_object(model.get("valleys"), f"{model_name}.valleys")
        if tuple(valleys) != VALLEY_LABELS:
            raise ValueError(f"{model_name} valley order or identity changed")
        inverse_tensors: list[Float64Array] = []
        density_terms: list[float] = []
        valley_records: list[JsonValue] = []
        local_maxima: list[float] = []
        for label in VALLEY_LABELS:
            valley = require_object(valleys.get(label), f"{model_name}.{label}")
            inverse_tensor = real_array(
                valley.get("primary_inverse_mass_tensor_in_inverse_electron_masses"),
                f"{model_name}.{label}.inverse_mass_tensor",
                (3, 3),
            )
            mass_tensor = real_array(
                valley.get("primary_mass_tensor_in_electron_masses"),
                f"{model_name}.{label}.mass_tensor",
                (3, 3),
            )
            stencil = primary_stencil(valley, f"{model_name}.{label}")
            principal_masses = real_array(
                stencil.get("principal_masses_electron"),
                f"{model_name}.{label}.principal_masses",
                (3,),
            )
            inverse_product_error = matrix_maximum_absolute(
                inverse_tensor @ mass_tensor - np.eye(3, dtype=np.float64)
            )
            eigenvalue_error = matrix_maximum_absolute(
                np.sort(np.linalg.eigvalsh(mass_tensor)) - np.sort(principal_masses)
            )
            determinant = float(np.linalg.det(mass_tensor))
            if determinant <= 0.0:
                raise ValueError(
                    f"{model_name}.{label} mass determinant is not positive"
                )
            recomputed_dos = float(np.cbrt(determinant))
            retained_dos = require_float(
                stencil.get("single_valley_dos_mass_electron"),
                f"{model_name}.{label}.single_valley_dos",
            )
            recomputed_conductivity = float(3.0 / np.trace(inverse_tensor))
            retained_conductivity = require_float(
                stencil.get("single_valley_conductivity_mass_electron"),
                f"{model_name}.{label}.single_valley_conductivity",
            )
            dos_error = abs(recomputed_dos - retained_dos)
            conductivity_error = abs(recomputed_conductivity - retained_conductivity)
            local_maximum = max(
                inverse_product_error,
                eigenvalue_error,
                dos_error,
                conductivity_error,
            )
            global_maximum = max(global_maximum, local_maximum)
            local_maxima.append(local_maximum)
            inverse_tensors.append(inverse_tensor)
            density_terms.append(float(np.sqrt(determinant)))
            valley_records.append(
                {
                    "label": label,
                    "mass_inverse_identity_maximum_absolute": inverse_product_error,
                    "principal_mass_eigenvalue_maximum_absolute": eigenvalue_error,
                    "single_valley_dos_mass_recomputed_electron": recomputed_dos,
                    "single_valley_dos_mass_absolute_difference": dos_error,
                    "single_valley_conductivity_mass_recomputed_electron": (
                        recomputed_conductivity
                    ),
                    "single_valley_conductivity_mass_absolute_difference": (
                        conductivity_error
                    ),
                }
            )
        average_inverse = np.mean(np.stack(inverse_tensors, axis=0), axis=0)
        retained_average_inverse = real_array(
            model.get(
                "equal_population_average_inverse_mass_tensor_in_inverse_electron_masses"
            ),
            f"{model_name}.average_inverse_mass_tensor",
            (3, 3),
        )
        average_inverse_error = matrix_maximum_absolute(
            average_inverse - retained_average_inverse
        )
        recomputed_family_dos = float(np.sum(density_terms) ** (2.0 / 3.0))
        retained_family_dos = require_float(
            model.get("six_valley_dos_mass_convention_electron"),
            f"{model_name}.six_valley_dos",
        )
        family_dos_error = abs(recomputed_family_dos - retained_family_dos)
        recomputed_family_conductivity = float(3.0 / np.trace(average_inverse))
        retained_family_conductivity = require_float(
            model.get("equal_population_conductivity_mass_convention_electron"),
            f"{model_name}.equal_population_conductivity",
        )
        family_conductivity_error = abs(
            recomputed_family_conductivity - retained_family_conductivity
        )
        model_maximum = max(
            average_inverse_error,
            family_dos_error,
            family_conductivity_error,
            *local_maxima,
        )
        global_maximum = max(global_maximum, model_maximum)
        model_records.append(
            {
                "model": model_name,
                "valley_count": len(VALLEY_LABELS),
                "valley_population_convention": (
                    "equal population over six retained signed-axis valleys"
                ),
                "average_inverse_mass_tensor_recomputed": average_inverse.tolist(),
                "average_inverse_mass_tensor_maximum_absolute_difference": (
                    average_inverse_error
                ),
                "six_valley_dos_mass_recomputed_electron": recomputed_family_dos,
                "six_valley_dos_mass_absolute_difference": family_dos_error,
                "equal_population_conductivity_mass_recomputed_electron": (
                    recomputed_family_conductivity
                ),
                "equal_population_conductivity_mass_absolute_difference": (
                    family_conductivity_error
                ),
                "average_inverse_mass_tensor_eigenvalues": np.linalg.eigvalsh(
                    average_inverse
                ).tolist(),
                "maximum_absolute_difference": model_maximum,
                "valleys": valley_records,
            }
        )
    return {
        "outcome": "passed" if global_maximum <= ABSOLUTE_TOLERANCE else "failed",
        "absolute_tolerance": ABSOLUTE_TOLERANCE,
        "maximum_absolute_difference": global_maximum,
        "dos_definition": "[sum_v sqrt(det(M_v))]^(2/3)",
        "conductivity_definition": "3 / trace[(1/6) sum_v M_v^(-1)]",
        "models": model_records,
    }


def cyclic_conjugate(mode: IntegerMode) -> IntegerMode:
    """Return the centered size-six cyclic representative of one negative mode."""
    result: list[int] = []
    for component in mode:
        value = -component
        if value > CONSTRUCTION_SIZE // 2 - 1:
            value -= CONSTRUCTION_SIZE
        result.append(value)
    return result[0], result[1], result[2]


def fcc_metric(mode: IntegerMode) -> int:
    """Return the retained integer FCC metric label."""
    n1, n2, n3 = mode
    return 2 * (n1 * n1 + n2 * n2 + n3 * n3 + n1 * n2 + n1 * n3 + n2 * n3)


def mode_from_json(value: JsonValue, name: str) -> IntegerMode:
    """Return one exact three-dimensional integer mode."""
    values = require_list(value, name)
    if len(values) != 3 or any(type(component) is not int for component in values):
        raise ValueError(f"{name} must be a length-three integer mode")
    return cast(int, values[0]), cast(int, values[1]), cast(int, values[2])


def audit_conversion(payload: JsonObject) -> tuple[JsonObject, JsonObject]:
    """Reconstruct the exact cyclic inventory and ordinary selection ledger."""
    displacement = require_object(
        payload.get("displacement_power"), "displacement_power"
    )
    retained_modes = tuple(
        mode_from_json(value, f"integer_modes[{index}]")
        for index, value in enumerate(
            require_list(displacement.get("integer_modes"), "integer_modes")
        )
    )
    expected_retained = tuple(itertools.product(range(-2, 3), repeat=3))
    if retained_modes != expected_retained:
        raise ValueError("retained ordinary displacement inventory changed")
    metric_values = require_list(
        displacement.get("metric_shell_values"), "metric_shell_values"
    )
    physical_radii = require_list(
        displacement.get("physical_radii_angstrom"), "physical_radii_angstrom"
    )
    reference_power = require_list(
        displacement.get("reference_power_per_state_ev2"), "reference_power"
    )
    attacked_power = require_list(
        displacement.get("attacked_identity_power_per_state_ev2"), "attacked_power"
    )
    lengths = {
        len(retained_modes),
        len(metric_values),
        len(physical_radii),
        len(reference_power),
        len(attacked_power),
    }
    if lengths != {125}:
        raise ValueError(
            "retained displacement-aligned arrays must each have length 125"
        )
    geometry = require_object(payload.get("geometry"), "geometry")
    lattice_parameter = require_float(
        geometry.get("lattice_parameter_angstrom"), "lattice parameter"
    )
    ordinary_lookup = {mode: index for index, mode in enumerate(retained_modes)}
    records: list[JsonValue] = []
    metric_error = 0.0
    radius_error = 0.0
    for cyclic_index, mode_value in enumerate(
        itertools.product(range(NEGATIVE_NYQUIST, CONSTRUCTION_SIZE // 2), repeat=3)
    ):
        mode = (mode_value[0], mode_value[1], mode_value[2])
        retained = NEGATIVE_NYQUIST not in mode
        record: JsonObject = {
            "cyclic_flat_index": cyclic_index,
            "cyclic_mode": list(mode),
            "cyclic_conjugate_mode": list(cyclic_conjugate(mode)),
            "action": "retained_identity" if retained else "removed_negative_nyquist",
            "ordinary_flat_index": None,
            "ordinary_mode": None,
            "fcc_metric_shell_value": None,
            "physical_radius_angstrom": None,
            "reference_power_per_state_ev2": None,
            "attacked_identity_power_per_state_ev2": None,
        }
        if retained:
            ordinary_index = ordinary_lookup[mode]
            metric = fcc_metric(mode)
            radius = lattice_parameter * np.sqrt(float(metric)) / 2.0
            retained_metric = require_float(
                metric_values[ordinary_index], f"metric[{ordinary_index}]"
            )
            retained_radius = require_float(
                physical_radii[ordinary_index], f"radius[{ordinary_index}]"
            )
            metric_error = max(metric_error, abs(float(metric) - retained_metric))
            radius_error = max(radius_error, abs(radius - retained_radius))
            record.update(
                {
                    "ordinary_flat_index": ordinary_index,
                    "ordinary_mode": list(mode),
                    "fcc_metric_shell_value": metric,
                    "physical_radius_angstrom": retained_radius,
                    "reference_power_per_state_ev2": require_float(
                        reference_power[ordinary_index],
                        f"reference_power[{ordinary_index}]",
                    ),
                    "attacked_identity_power_per_state_ev2": require_float(
                        attacked_power[ordinary_index],
                        f"attacked_power[{ordinary_index}]",
                    ),
                }
            )
        records.append(record)
    retained_count = sum(
        require_string(require_object(record, "record")["action"], "action")
        == "retained_identity"
        for record in records
    )
    removed_count = len(records) - retained_count
    summary: JsonObject = {
        "outcome": (
            "passed"
            if retained_count == 125
            and removed_count == 91
            and metric_error <= ABSOLUTE_TOLERANCE
            and radius_error <= ABSOLUTE_TOLERANCE
            else "failed"
        ),
        "construction_size": CONSTRUCTION_SIZE,
        "cyclic_axis": list(range(-3, 3)),
        "ordinary_axis": list(range(-2, 3)),
        "cyclic_mode_count": len(records),
        "ordinary_mode_count": retained_count,
        "removed_negative_nyquist_mode_count": removed_count,
        "selection_rule": (
            "retain a cyclic mode iff no component equals -N/2; retained modes map "
            "identically"
        ),
        "ordering": "first component outermost, third component innermost",
        "maximum_metric_shell_absolute_difference": metric_error,
        "maximum_physical_radius_absolute_difference_angstrom": radius_error,
        "coefficient_matrix_boundary": (
            "The source result retains ordinary-mode powers but not all 216 cyclic "
            "coefficient matrices; removed-mode coefficient values and power are not "
            "independently reconstructed by this audit."
        ),
    }
    ledger: JsonObject = {
        "schema_version": 1,
        "record_type": "c6_b20_w21_cyclic_to_ordinary_conversion_ledger",
        "source_result_sha256": GAUGE_RESULT_SHA256,
        "summary": summary,
        "records": records,
    }
    return summary, ledger


def write_exclusive(path: Path, content: bytes) -> None:
    """Create one retained artifact without replacement."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(content)


def execute(output_root: Path) -> None:
    """Run both independent checks and retain deterministic audit records."""
    output_root = output_root.resolve()
    result_path = output_root / "result.json"
    ledger_path = output_root / "conversion-ledger.json"
    manifest_path = output_root / "manifest.json"
    for path in (result_path, ledger_path, manifest_path):
        if path.exists():
            raise FileExistsError(f"refusing to overwrite {path}")
    mass_payload = read_authenticated(MASS_RESULT, MASS_RESULT_SHA256)
    gauge_payload = read_authenticated(GAUGE_RESULT, GAUGE_RESULT_SHA256)
    mass_audit = audit_mass_conventions(mass_payload)
    conversion_audit, ledger = audit_conversion(gauge_payload)
    outcome = (
        "passed"
        if mass_audit["outcome"] == "passed" and conversion_audit["outcome"] == "passed"
        else "failed"
    )
    script_path = Path(__file__).resolve()
    result = canonical_json(
        {
            "schema_version": 1,
            "record_type": "c6_b20_w21_independent_numerical_convention_audit",
            "status": (
                "independent-formula-and-inventory-audit-not-full-scientific-reconstruction"
            ),
            "outcome": outcome,
            "sources": {
                "comprehensive_band_edge_result": {
                    "path": str(MASS_RESULT.relative_to(REPOSITORY)),
                    "sha256": MASS_RESULT_SHA256,
                },
                "gauge_alignment_locality_result": {
                    "path": str(GAUGE_RESULT.relative_to(REPOSITORY)),
                    "sha256": GAUGE_RESULT_SHA256,
                },
            },
            "audit_script_sha256": sha256_bytes(script_path.read_bytes()),
            "mass_convention_audit": mass_audit,
            "cyclic_to_ordinary_conversion_audit": conversion_audit,
            "claim_boundary": (
                "Independent recomputation of retained mass formulas and exact integer "
                "conversion inventory only; not independent reconstruction of the "
                "Hamiltonian fields, Fourier coefficients, removed-mode power, support "
                "errors, optimization, valleys, or band-edge calculations."
            ),
        }
    )
    ledger_bytes = canonical_json(ledger)
    write_exclusive(result_path, result)
    write_exclusive(ledger_path, ledger_bytes)
    readme_path = ROOT / "README.md"
    manifest = canonical_json(
        {
            "schema_version": 1,
            "record_type": "c6_b20_w21_independent_numerical_convention_audit_manifest",
            "artifacts": [
                {
                    "path": "result.json",
                    "bytes": len(result),
                    "sha256": sha256_bytes(result),
                },
                {
                    "path": "conversion-ledger.json",
                    "bytes": len(ledger_bytes),
                    "sha256": sha256_bytes(ledger_bytes),
                },
                {
                    "path": str(script_path.relative_to(REPOSITORY)),
                    "bytes": script_path.stat().st_size,
                    "sha256": sha256_bytes(script_path.read_bytes()),
                },
                {
                    "path": str(readme_path.relative_to(REPOSITORY)),
                    "bytes": readme_path.stat().st_size,
                    "sha256": sha256_bytes(readme_path.read_bytes()),
                },
            ],
        }
    )
    write_exclusive(manifest_path, manifest)
    if outcome != "passed":
        raise RuntimeError("one or more numerical-convention audits failed")


def main() -> None:
    """Parse an explicit fresh output directory and run the audit."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, required=True)
    arguments = parser.parse_args()
    execute(arguments.output_root)


if __name__ == "__main__":
    main()
