#!/usr/bin/env python3
"""Independently verify one authored folding/null-control execution."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import cast

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    FoldingNullIndependentVerificationWorkflow,
)

EXECUTION_ID = "folding-null-controls-v1"
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
    """Authenticate and independently reconstruct one folding/null result."""
    execution_root = execution_root.resolve()
    calculation_root = Path(__file__).resolve().parent
    calculation_script = calculation_root / "run_03_folding_null_controls.py"
    execution_path = execution_root / "execution.json"
    result_path = execution_root / "results" / "result.json"
    verification_root = execution_root / "verification"
    temporary_root = execution_root / ".verification.incomplete"
    if verification_root.exists() or temporary_root.exists():
        raise FileExistsError("refusing to overwrite folding/null-control verification")
    if not all(
        path.is_file() for path in (calculation_script, execution_path, result_path)
    ):
        raise FileNotFoundError(
            "the authored folding/null-control execution is incomplete"
        )

    execution = read_object(execution_path)
    if require_int(execution, "schema_version") != 1:
        raise ValueError("execution schema_version must equal 1")
    if (
        require_string(execution, "record_type")
        != "periodic2d_rank_defect_folding_null_execution"
    ):
        raise ValueError("execution record_type is not supported")
    if require_string(execution, "execution_id") != EXECUTION_ID:
        raise ValueError("execution identifier does not match")
    if require_string(execution, "calculation_family") != CALCULATION_FAMILY:
        raise ValueError("calculation family does not match")
    if execution.get("external_execution") is not False:
        raise ValueError("folding/null controls must not report external execution")
    if execution.get("accepted_parent_read") is not False:
        raise ValueError(
            "folding/null controls must not report an accepted-parent read"
        )
    if (
        require_string(execution, "calculation_script_sha256")
        != hashlib.sha256(calculation_script.read_bytes()).hexdigest()
    ):
        raise ValueError("calculation script identity does not match")

    result_bytes = result_path.read_bytes()
    if (
        require_string(execution, "result_sha256")
        != hashlib.sha256(result_bytes).hexdigest()
    ):
        raise ValueError("result identity does not match")
    workflow = FoldingNullIndependentVerificationWorkflow().execute(
        result_bytes,
        verification_relative_tolerance=1.0e-10,
        verification_absolute_tolerance=5.0e-13,
    )
    verified = workflow.verification
    result = verified.source
    if require_int(execution, "case_count") != len(result.cases):
        raise ValueError("execution case count does not match the result")
    if require_string(execution, "criterion_status") != (
        "pass" if result.passes else "fail"
    ):
        raise ValueError("execution criterion status does not match the result")

    if not verified.passes:
        raise ValueError("independent folding/null verification failed")
    verification_bytes = canonical_json(
        {
            "schema_version": 1,
            "record_type": "periodic2d_rank_defect_folding_null_verification",
            "calculation_family": CALCULATION_FAMILY,
            "execution_id": EXECUTION_ID,
            "outcome": "passed",
            "result_sha256": hashlib.sha256(result_bytes).hexdigest(),
            "calculation_script_sha256": hashlib.sha256(
                calculation_script.read_bytes()
            ).hexdigest(),
            "verification_script_sha256": hashlib.sha256(
                Path(__file__).resolve().read_bytes()
            ).hexdigest(),
            "case_count": len(result.cases),
            "criterion_status": "pass" if result.passes else "fail",
            "reconstruction_passed": verified.reconstruction_passed,
            "criteria_match": verified.criteria_match,
            "maximum_metric_absolute_difference": (
                verified.maximum_metric_absolute_difference
            ),
            "claim_boundary": (
                "Independent reconstruction of authored dimensionless folding and "
                "null-extraction metrics only; not accepted-parent "
                "verification, material validation, convergence evidence, UQ, or "
                "protected calculation authority."
            ),
        }
    )
    temporary_root.mkdir()
    (temporary_root / "verification.json").write_bytes(verification_bytes)
    temporary_root.rename(verification_root)


def main() -> None:
    """Parse the execution root and verify its authored folding/null-control result."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--execution-root", type=Path, required=True)
    arguments = parser.parse_args()
    verify(arguments.execution_root)


if __name__ == "__main__":
    main()
