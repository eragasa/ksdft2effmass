#!/usr/bin/env python3
"""Verify the version-2 finite-domain plan with small-cell aliasing controls."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import cast

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    FiniteDomainEffectsCaseInventoryJsonSerializer,
)

EXECUTION_ID = "finite-domain-defect-planning-v2"
CALCULATION_FAMILY = "periodic2d-rank-defect"
type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


def canonical_json(payload: dict[str, JsonValue]) -> bytes:
    """Encode one verification record deterministically."""
    return (
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")


def read_object(path: Path) -> dict[str, JsonValue]:
    """Read one JSON object through the closed calculation representation."""
    value = cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
    if type(value) is not dict:
        raise ValueError(f"{path} must contain a JSON object")
    return value


def require_string(payload: dict[str, JsonValue], key: str) -> str:
    """Return one required nonempty string field."""
    value = payload.get(key)
    if type(value) is not str or not value:
        raise ValueError(f"{key} must be a nonempty string")
    return value


def require_int(payload: dict[str, JsonValue], key: str) -> int:
    """Return one required integer field without admitting booleans."""
    value = payload.get(key)
    if type(value) is not int:
        raise ValueError(f"{key} must be an integer")
    return value


def verify(execution_root: Path) -> None:
    """Authenticate and verify one no-overwrite planning package."""
    execution_root = execution_root.resolve()
    calculation_root = Path(__file__).resolve().parent
    planning_script = calculation_root / "run_05_plan_finite_domain_controls.py"
    execution_path = execution_root / "execution.json"
    input_path = execution_root / "inputs" / "definition.json"
    result_path = execution_root / "results" / "case-inventory.json"
    verification_root = execution_root / "verification"
    temporary_root = execution_root / ".verification.incomplete"
    if verification_root.exists() or temporary_root.exists():
        raise FileExistsError("refusing to overwrite finite-domain plan verification")
    if not all(
        path.is_file()
        for path in (planning_script, execution_path, input_path, result_path)
    ):
        raise FileNotFoundError("the finite-domain planning package is incomplete")

    execution = read_object(execution_path)
    if require_int(execution, "schema_version") != 1:
        raise ValueError("execution schema version must equal 1")
    if (
        require_string(execution, "record_type")
        != "finite_domain_effects_planning_execution"
    ):
        raise ValueError("execution record type is not supported")
    if require_string(execution, "execution_id") != EXECUTION_ID:
        raise ValueError("execution identifier does not match")
    if require_string(execution, "calculation_family") != CALCULATION_FAMILY:
        raise ValueError("calculation family does not match")
    if require_string(execution, "execution_status") != "not_executed":
        raise ValueError("planning package must remain unexecuted")
    if (
        require_string(execution, "planning_script_sha256")
        != hashlib.sha256(planning_script.read_bytes()).hexdigest()
    ):
        raise ValueError("planning script identity does not match")

    input_bytes = input_path.read_bytes()
    result_bytes = result_path.read_bytes()
    if (
        require_string(execution, "input_sha256")
        != hashlib.sha256(input_bytes).hexdigest()
    ):
        raise ValueError("definition identity does not match")
    if (
        require_string(execution, "result_sha256")
        != hashlib.sha256(result_bytes).hexdigest()
    ):
        raise ValueError("case-inventory identity does not match")

    definition_record = read_object(input_path)
    if require_int(definition_record, "schema_version") != 1:
        raise ValueError("definition schema version must equal 1")
    if (
        require_string(definition_record, "record_type")
        != "finite_domain_effects_study_definition"
    ):
        raise ValueError("definition record type is not supported")
    if definition_record.get("execution_authorized_by_this_record") is not False:
        raise ValueError("definition must not authorize execution")

    serializer = FiniteDomainEffectsCaseInventoryJsonSerializer()
    inventory = serializer.deserialize(result_bytes)
    definition = inventory.definition
    if definition_record.get("definition") != serializer.definition_payload(definition):
        raise ValueError("definition input and retained plan do not match")
    if definition.identifier != (
        "research-monograph.impurity-defect-2d.finite-domain-effects.v2"
    ):
        raise ValueError("study identifier does not match the adopted definition")
    if tuple(shape.extents for shape in definition.area_shapes) != (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (8, 8),
        (10, 10),
        (12, 12),
        (16, 16),
    ):
        raise ValueError("area-channel shapes do not match")
    if tuple(shape.extents for shape in definition.shape_shapes) != (
        (8, 18),
        (9, 16),
        (12, 12),
        (16, 9),
        (18, 8),
    ):
        raise ValueError("shape-channel shapes do not match")
    if definition.defect_identifiers != (
        "directional_nearest_neighbor",
        "finite_range_diagonal_nonlocal",
    ):
        raise ValueError("defect inventory does not match")
    if definition.twist_mesh.counts != (9, 9):
        raise ValueError("twist mesh does not match")
    if (
        definition.isotropic_parent_identifier != "isotropic_lambda_0p5_0p5_0"
        or definition.orientation_source_parent_identifier
        != "anisotropic_lambda_0p3_0p7_0"
        or definition.orientation_swapped_parent_identifier
        != "anisotropic_lambda_0p7_0p3_0"
    ):
        raise ValueError("parent identifiers do not match")
    if len(inventory.isotropic_cases) != 2268:
        raise ValueError("isotropic case count does not match")
    if len(inventory.orientation_cases) != 324:
        raise ValueError("orientation case count does not match")
    if inventory.operator_evaluation_count != 3240:
        raise ValueError("proposed operator-evaluation count does not match")
    if require_int(execution, "isotropic_case_count") != 2268:
        raise ValueError("execution isotropic count does not match")
    if require_int(execution, "orientation_case_count") != 324:
        raise ValueError("execution orientation count does not match")
    if require_int(execution, "proposed_operator_evaluation_count") != 3240:
        raise ValueError("execution evaluation count does not match")

    verification_bytes = canonical_json(
        {
            "schema_version": 1,
            "record_type": "finite_domain_effects_planning_verification",
            "calculation_family": CALCULATION_FAMILY,
            "execution_id": EXECUTION_ID,
            "outcome": "passed",
            "execution_status": "not_executed",
            "input_sha256": hashlib.sha256(input_bytes).hexdigest(),
            "result_sha256": hashlib.sha256(result_bytes).hexdigest(),
            "planning_script_sha256": hashlib.sha256(
                planning_script.read_bytes()
            ).hexdigest(),
            "verification_script_sha256": hashlib.sha256(
                Path(__file__).resolve().read_bytes()
            ).hexdigest(),
            "verified_isotropic_case_count": 2268,
            "verified_orientation_case_count": 324,
            "verified_proposed_operator_evaluation_count": 3240,
            "claim_boundary": (
                "Verification authenticates and reconstructs an execution-free plan "
                "only. The 1x1 through 5x5 cases remain periodic-aliasing controls. It "
                "verifies no operator, spectrum, isolated-defect trend, convergence "
                "trend, material claim, uncertainty statement, or protected "
                "calculation."
            ),
        }
    )
    temporary_root.mkdir()
    (temporary_root / "verification.json").write_bytes(verification_bytes)
    temporary_root.rename(verification_root)


def main() -> None:
    """Parse the execution root and verify its planning artifacts."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--execution-root", type=Path, required=True)
    arguments = parser.parse_args()
    verify(arguments.execution_root)


if __name__ == "__main__":
    main()
