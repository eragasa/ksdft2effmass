#!/usr/bin/env python3
"""Materialize canonical M4 input JSON from the editable TOML protocol source."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Never, cast

import tomllib

ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = ROOT.parents[4]


def fail(message: str) -> Never:
    """Reject malformed or inconsistent protocol configuration."""
    raise ValueError(message)


def mapping(value: object, context: str) -> dict[str, object]:
    """Require a mapping with built-in string keys."""
    if type(value) is not dict or any(type(key) is not str for key in value):
        fail(f"{context} must be a table with string keys")
    return value


def exact(value: dict[str, object], keys: set[str], context: str) -> None:
    """Require exactly the declared fields."""
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
    if not math.isfinite(result):
        fail(f"{context} must be finite")
    return result


def boolean(value: object, context: str) -> bool:
    """Require a built-in Boolean."""
    if type(value) is not bool:
        fail(f"{context} must be Boolean")
    return value


def integer_list(value: object, context: str) -> list[int]:
    """Require a nonempty increasing list of built-in integers."""
    if type(value) is not list or not value:
        fail(f"{context} must be a nonempty array")
    result: list[int] = []
    for index, item in enumerate(value):
        if type(item) is not int:
            fail(f"{context}[{index}] must be an integer")
        result.append(item)
    if result != sorted(set(result)):
        fail(f"{context} must be unique and increasing")
    return result


def pair(value: object, context: str) -> list[float]:
    """Require a length-two finite numeric array."""
    if type(value) is not list or len(value) != 2:
        fail(f"{context} must be a length-two array")
    return [number(value[0], f"{context}[0]"), number(value[1], f"{context}[1]")]


def pairs(value: object, context: str) -> list[list[float]]:
    """Require a nonempty array of finite numeric pairs."""
    if type(value) is not list or not value:
        fail(f"{context} must be a nonempty array")
    return [pair(item, f"{context}[{index}]") for index, item in enumerate(value)]


def table_array(value: object, context: str) -> list[dict[str, object]]:
    """Require a nonempty TOML array of tables."""
    if type(value) is not list or not value:
        fail(f"{context} must be a nonempty array of tables")
    return [mapping(item, f"{context}[{index}]") for index, item in enumerate(value)]


def digest(value: object, context: str) -> str:
    """Require one lowercase hexadecimal SHA-256 digest."""
    result = text(value, context)
    if len(result) != 64 or any(character not in "0123456789abcdef" for character in result):
        fail(f"{context} must be a lowercase SHA-256 digest")
    return result


def repository_path(value: object, context: str) -> Path:
    """Require a repository-relative path without parent traversal."""
    result = Path(text(value, context))
    if result.is_absolute() or ".." in result.parts:
        fail(f"{context} must be repository-relative")
    return result


def verify_bound_file(path_value: object, digest_value: object, context: str) -> dict[str, str]:
    """Verify one configured repository file identity."""
    relative = repository_path(path_value, f"{context}.path")
    expected = digest(digest_value, f"{context}.sha256")
    actual = hashlib.sha256((REPOSITORY_ROOT / relative).read_bytes()).hexdigest()
    if actual != expected:
        fail(f"{context} does not match its configured SHA-256 digest")
    return {"path": relative.as_posix(), "sha256": expected}


def geometry(value: dict[str, object], context: str) -> dict[str, object]:
    """Decode one positive-orientation two-dimensional primitive basis."""
    exact(value, {"geometry_id", "primitive_basis_rows", "role"}, context)
    basis = pairs(value["primitive_basis_rows"], f"{context}.primitive_basis_rows")
    if len(basis) != 2:
        fail(f"{context}.primitive_basis_rows must contain two rows")
    determinant = basis[0][0] * basis[1][1] - basis[0][1] * basis[1][0]
    if determinant <= 0.0 or not math.isfinite(determinant):
        fail(f"{context} must have finite positive orientation")
    return {
        "geometry_id": text(value["geometry_id"], f"{context}.geometry_id"),
        "primitive_basis_rows": basis,
        "role": text(value["role"], f"{context}.role"),
    }


def parent(value: dict[str, object], context: str) -> dict[str, object]:
    """Decode one synthetic cosine parent."""
    exact(
        value,
        {"parent_id", "geometry_id", "lambda_1", "lambda_2", "lambda_12", "role"},
        context,
    )
    return {
        "parent_id": text(value["parent_id"], f"{context}.parent_id"),
        "geometry_id": text(value["geometry_id"], f"{context}.geometry_id"),
        "lambda_1": number(value["lambda_1"], f"{context}.lambda_1"),
        "lambda_2": number(value["lambda_2"], f"{context}.lambda_2"),
        "lambda_12": number(value["lambda_12"], f"{context}.lambda_12"),
        "role": text(value["role"], f"{context}.role"),
    }


def canonical_json(value: object) -> bytes:
    """Return canonical retained JSON bytes."""
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
    """Build and validate the complete protocol input document."""
    raw: object = tomllib.loads(configuration_path.read_text(encoding="utf-8"))
    configuration = mapping(raw, "configuration")
    exact(
        configuration,
        {
            "schema",
            "calculation_id",
            "protocol_status",
            "evidence_status",
            "operator",
            "representations",
            "sampling",
            "geometries",
            "parents",
            "verification_criteria",
            "historical_square_baseline",
            "dependencies",
            "execution",
        },
        "configuration",
    )
    if configuration["schema"] != "ksdft2effmass.periodic2d.common-space-configuration.v1":
        fail("unexpected configuration schema")

    operator = mapping(configuration["operator"], "operator")
    exact(
        operator,
        {
            "coordinate_convention",
            "bloch_momentum_convention",
            "bloch_seam_phase",
            "kinetic_operator",
            "kinetic_coefficient",
            "potential_family",
            "potential_mean",
            "energy_zero",
            "energy_unit",
            "spin_convention",
        },
        "operator",
    )
    literal_operator = {
        "coordinate_convention": "fractional-cell-coordinates",
        "bloch_momentum_convention": "turns-along-direct-primitive-axes",
        "bloch_seam_phase": "exp(+2*pi*i*kappa_dot_q)",
        "kinetic_operator": "minus-cartesian-laplacian",
        "potential_family": "lambda_1*cos(2*pi*s_1)+lambda_2*cos(2*pi*s_2)+lambda_12*cos(2*pi*s_1)*cos(2*pi*s_2)",
        "energy_zero": "zero-cell-average-potential",
        "energy_unit": "1",
        "spin_convention": "spinless-scalar",
    }
    for key, expected in literal_operator.items():
        if text(operator[key], f"operator.{key}") != expected:
            fail(f"operator.{key} differs from the v1 contract")
    if number(operator["kinetic_coefficient"], "operator.kinetic_coefficient") != 1.0:
        fail("operator.kinetic_coefficient must be 1")
    if number(operator["potential_mean"], "operator.potential_mean") != 0.0:
        fail("operator.potential_mean must be 0")

    representations = mapping(configuration["representations"], "representations")
    exact(
        representations,
        {
            "plane_wave_ordering",
            "finite_difference_ordering",
            "common_space_map",
            "common_space_cutoff",
            "plane_wave_cutoffs",
            "plane_wave_reference_cutoff",
            "finite_difference_extents",
            "compared_low_band_count",
        },
        "representations",
    )
    plane_cutoffs = integer_list(representations["plane_wave_cutoffs"], "representations.plane_wave_cutoffs")
    finite_extents = integer_list(representations["finite_difference_extents"], "representations.finite_difference_extents")
    for field in ("common_space_cutoff", "plane_wave_reference_cutoff", "compared_low_band_count"):
        if type(representations[field]) is not int:
            fail(f"representations.{field} must be an integer")
    common_cutoff = cast(int, representations["common_space_cutoff"])
    reference_cutoff = cast(int, representations["plane_wave_reference_cutoff"])
    band_count = cast(int, representations["compared_low_band_count"])
    if common_cutoff < 0 or reference_cutoff != plane_cutoffs[-1] or band_count <= 0:
        fail("representation cutoffs and band count are inconsistent")
    if min(finite_extents) < 2 * common_cutoff + 1:
        fail("every finite-difference extent must resolve the common plane-wave basis")

    sampling = mapping(configuration["sampling"], "sampling")
    exact(sampling, {"primary_momenta", "diagnostic_momenta"}, "sampling")
    primary = pairs(sampling["primary_momenta"], "sampling.primary_momenta")
    diagnostic = pairs(sampling["diagnostic_momenta"], "sampling.diagnostic_momenta")
    if any(not (-0.5 <= component < 0.5) for momentum in primary + diagnostic for component in momentum):
        fail("all reduced momenta must lie in [-0.5, 0.5)")
    if {tuple(momentum) for momentum in primary} & {tuple(momentum) for momentum in diagnostic}:
        fail("primary and diagnostic momentum sets must be disjoint")

    geometries = [
        geometry(item, f"geometries[{index}]")
        for index, item in enumerate(table_array(configuration["geometries"], "geometries"))
    ]
    geometry_ids = [cast(str, item["geometry_id"]) for item in geometries]
    if len(geometry_ids) != len(set(geometry_ids)):
        fail("geometry identifiers must be unique")
    parents = [
        parent(item, f"parents[{index}]")
        for index, item in enumerate(table_array(configuration["parents"], "parents"))
    ]
    parent_ids = [cast(str, item["parent_id"]) for item in parents]
    if len(parent_ids) != len(set(parent_ids)):
        fail("parent identifiers must be unique")
    if any(item["geometry_id"] not in geometry_ids for item in parents):
        fail("every parent must reference a configured geometry")

    criteria = mapping(configuration["verification_criteria"], "verification_criteria")
    criterion_fields = {
        "hermiticity_absolute_tolerance",
        "common_map_isometry_frobenius_tolerance",
        "analytic_symbol_absolute_tolerance",
        "resolved_potential_block_absolute_tolerance",
        "independent_reconstruction_absolute_tolerance",
        "plane_wave_reference_low_band_tolerance",
    }
    exact(criteria, criterion_fields, "verification_criteria")
    decoded_criteria = {key: number(criteria[key], f"verification_criteria.{key}") for key in sorted(criterion_fields)}
    if min(decoded_criteria.values()) <= 0.0:
        fail("verification tolerances must be positive")

    baseline = mapping(configuration["historical_square_baseline"], "historical_square_baseline")
    exact(
        baseline,
        {"input_path", "input_sha256", "result_path", "result_sha256", "comparison_role"},
        "historical_square_baseline",
    )
    baseline_input = verify_bound_file(baseline["input_path"], baseline["input_sha256"], "historical_square_baseline.input")
    baseline_result = verify_bound_file(baseline["result_path"], baseline["result_sha256"], "historical_square_baseline.result")

    dependencies = mapping(configuration["dependencies"], "dependencies")
    exact(dependencies, {"physkit_revision", "physkit_laplacian", "plane_wave_owner", "comparison_owner"}, "dependencies")
    decoded_dependencies = {key: text(dependencies[key], f"dependencies.{key}") for key in sorted(dependencies)}
    if len(decoded_dependencies["physkit_revision"]) != 40:
        fail("dependencies.physkit_revision must be a full Git revision")

    execution = mapping(configuration["execution"], "execution")
    exact(execution, {"local_only", "external_calculators", "remote_execution", "production_execution"}, "execution")
    decoded_execution = {key: boolean(execution[key], f"execution.{key}") for key in sorted(execution)}
    if decoded_execution != {
        "external_calculators": False,
        "local_only": True,
        "production_execution": False,
        "remote_execution": False,
    }:
        fail("execution boundary differs from the local synthetic v1 contract")

    return {
        "schema": "ksdft2effmass.periodic2d.common-space-input.v1",
        "calculation_id": text(configuration["calculation_id"], "calculation_id"),
        "protocol_status": text(configuration["protocol_status"], "protocol_status"),
        "evidence_status": text(configuration["evidence_status"], "evidence_status"),
        "operator": {
            **literal_operator,
            "kinetic_coefficient": 1.0,
            "potential_mean": 0.0,
        },
        "representations": {
            "plane_wave_ordering": text(representations["plane_wave_ordering"], "representations.plane_wave_ordering"),
            "finite_difference_ordering": text(representations["finite_difference_ordering"], "representations.finite_difference_ordering"),
            "common_space_map": text(representations["common_space_map"], "representations.common_space_map"),
            "common_space_cutoff": common_cutoff,
            "plane_wave_cutoffs": plane_cutoffs,
            "plane_wave_reference_cutoff": reference_cutoff,
            "finite_difference_extents": finite_extents,
            "compared_low_band_count": band_count,
        },
        "sampling": {"primary_momenta": primary, "diagnostic_momenta": diagnostic},
        "geometries": geometries,
        "parents": parents,
        "verification_criteria": decoded_criteria,
        "historical_square_baseline": {
            "input": baseline_input,
            "result": baseline_result,
            "comparison_role": text(baseline["comparison_role"], "historical_square_baseline.comparison_role"),
        },
        "dependencies": decoded_dependencies,
        "execution": decoded_execution,
    }


def main() -> None:
    """Write or check the canonical generated input."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail unless input.json equals the canonical generated bytes",
    )
    arguments = parser.parse_args()
    generated = canonical_json(build_document(ROOT / "configuration.toml"))
    destination = ROOT / "input.json"
    if arguments.check:
        if not destination.is_file() or destination.read_bytes() != generated:
            fail("input.json is not the canonical configuration-derived document")
        print("m4_input_configuration=PASS")
        return
    destination.write_bytes(generated)
    print(f"wrote {destination}")


if __name__ == "__main__":
    main()
