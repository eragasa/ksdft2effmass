#!/usr/bin/env python3
"""Independently verify one retained periodic-2D parent qualification."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import resource
import time
from pathlib import Path
from typing import cast

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    ParentQualificationIndependentVerificationWorkflow,
    ParentQualificationResultJsonSerializer,
)

EXECUTION_ID = "parent-qualification-v1"
CALCULATION_FAMILY = "periodic2d-rank-defect"

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


def canonical_json(payload: dict[str, JsonValue]) -> bytes:
    """Encode one retained record deterministically."""
    return (
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")


def read_object(path: Path) -> dict[str, JsonValue]:
    """Read one retained JSON object."""
    value = cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
    if type(value) is not dict:
        raise ValueError(f"{path} must contain a JSON object")
    return value


def require_string(payload: dict[str, JsonValue], key: str) -> str:
    """Return one required nonempty string."""
    value = payload.get(key)
    if type(value) is not str or not value:
        raise ValueError(f"{key} must be a nonempty string")
    return value


def require_int(payload: dict[str, JsonValue], key: str) -> int:
    """Return one required built-in integer."""
    value = payload.get(key)
    if type(value) is not int:
        raise ValueError(f"{key} must be an integer")
    return value


def write_exclusive(path: Path, payload: bytes) -> None:
    """Create one retained artifact without replacement."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(payload)


def verify(execution_root: Path) -> None:
    """Authenticate and independently reconstruct one parent qualification."""
    execution_root = execution_root.resolve(strict=True)
    calculation_root = Path(__file__).resolve().parent
    calculation_script = calculation_root / "run_07_qualify_parents.py"
    execution_path = execution_root / "execution.json"
    request_path = execution_root / "inputs" / "request.json"
    result_path = execution_root / "results" / "result.json"
    versions_path = execution_root / "software-versions.json"
    verification_path = execution_root / "verification" / "verification.json"
    manifest_path = execution_root / "manifest.json"
    for path in (verification_path, manifest_path):
        if path.exists():
            raise FileExistsError(f"refusing to overwrite {path}")
    for path in (
        calculation_script,
        execution_path,
        request_path,
        result_path,
        versions_path,
    ):
        if not path.is_file():
            raise FileNotFoundError(f"parent qualification artifact is absent: {path}")

    execution = read_object(execution_path)
    if require_int(execution, "schema_version") != 1:
        raise ValueError("execution schema_version must equal 1")
    if require_string(execution, "record_type") != (
        "periodic2d_rank_defect_parent_qualification_execution"
    ):
        raise ValueError("execution record_type is not supported")
    if require_string(execution, "execution_id") != EXECUTION_ID:
        raise ValueError("execution identifier differs")
    if require_string(execution, "calculation_family") != CALCULATION_FAMILY:
        raise ValueError("calculation family differs")
    if execution.get("external_execution") is not False:
        raise ValueError("parent qualification must remain local")
    if execution.get("defect_campaign_executed") is not False:
        raise ValueError("parent qualification must not execute the defect campaign")
    if (
        require_string(execution, "calculation_script_sha256")
        != hashlib.sha256(calculation_script.read_bytes()).hexdigest()
    ):
        raise ValueError("calculation script identity differs")
    request_bytes = request_path.read_bytes()
    result_bytes = result_path.read_bytes()
    if (
        require_string(execution, "request_sha256")
        != hashlib.sha256(request_bytes).hexdigest()
    ):
        raise ValueError("request identity differs")
    if (
        require_string(execution, "result_sha256")
        != hashlib.sha256(result_bytes).hexdigest()
    ):
        raise ValueError("result identity differs")

    source = ParentQualificationResultJsonSerializer().deserialize(result_bytes)
    started = time.perf_counter()
    workflow = ParentQualificationIndependentVerificationWorkflow().execute(
        result_bytes,
        verification_absolute_tolerance=(
            source.definition.tolerances.reconstruction_absolute
        ),
    )
    runtime = time.perf_counter() - started
    peak_memory_bytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if platform.system() != "Darwin":
        peak_memory_bytes *= 1024
    envelope = source.definition.resource_envelope
    if runtime > float(envelope.maximum_runtime_seconds):
        raise RuntimeError("independent verification exceeded its runtime envelope")
    if peak_memory_bytes > int(envelope.maximum_peak_memory_gib * 1024**3):
        raise RuntimeError("independent verification exceeded its memory envelope")
    verified = workflow.verification
    if not verified.passes:
        raise ValueError("independent parent qualification verification failed")
    if require_string(execution, "criterion_status") != (
        "pass" if source.passes else "fail"
    ):
        raise ValueError("execution criterion status differs")

    verification_script = Path(__file__).resolve()
    verification_bytes = canonical_json(
        {
            "schema_version": 1,
            "record_type": ("periodic2d_rank_defect_parent_qualification_verification"),
            "calculation_family": CALCULATION_FAMILY,
            "execution_id": EXECUTION_ID,
            "outcome": "passed",
            "request_sha256": hashlib.sha256(request_bytes).hexdigest(),
            "result_sha256": hashlib.sha256(result_bytes).hexdigest(),
            "calculation_script_sha256": hashlib.sha256(
                calculation_script.read_bytes()
            ).hexdigest(),
            "verification_script_sha256": hashlib.sha256(
                verification_script.read_bytes()
            ).hexdigest(),
            "criterion_status": "pass" if source.passes else "fail",
            "reconstruction_passed": verified.reconstruction_passed,
            "criteria_match": verified.criteria_match,
            "maximum_metric_absolute_difference": (
                verified.maximum_metric_absolute_difference
            ),
            "reconstructed_parent_route_evaluations": (
                verified.reconstructed_parent_route_evaluations
            ),
            "reconstructed_defect_route_evaluations": (
                verified.reconstructed_defect_route_evaluations
            ),
            "resource_observation": {
                "runtime_seconds": runtime,
                "peak_memory_bytes": peak_memory_bytes,
            },
            "claim_boundary": (
                "Independent reconstruction of accepted historical dimensionless "
                "synthetic parent capability only; not material validation, "
                "finite-domain convergence, uncertainty quantification, or defect "
                "campaign execution authority."
            ),
        }
    )
    write_exclusive(verification_path, verification_bytes)

    artifact_paths = (
        request_path,
        result_path,
        execution_path,
        versions_path,
        calculation_script,
        verification_script,
        verification_path,
    )
    repository_root = calculation_root.parent.parent.resolve()
    artifacts: list[JsonValue] = []
    for path in artifact_paths:
        relative = (
            path.relative_to(execution_root).as_posix()
            if path.is_relative_to(execution_root)
            else path.relative_to(repository_root).as_posix()
        )
        artifacts.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    manifest = canonical_json(
        {
            "schema_version": 1,
            "record_type": "periodic2d_rank_defect_parent_qualification_manifest",
            "execution_id": EXECUTION_ID,
            "artifacts": artifacts,
            "dense_matrices_retained": False,
        }
    )
    write_exclusive(manifest_path, manifest)


def main() -> None:
    """Parse one retained execution root and independently verify it."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--execution-root", type=Path, required=True)
    arguments = parser.parse_args()
    verify(arguments.execution_root)


if __name__ == "__main__":
    main()
