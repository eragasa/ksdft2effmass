#!/usr/bin/env python3
"""Qualify retained synthetic parents through maintained construction routes."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import resource
import subprocess
import time
from pathlib import Path

import numpy as np
import scipy  # type: ignore[import-untyped]

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    ParentQualificationCalculationWorkflow,
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


def repository_revision(root: Path) -> str:
    """Return the current repository revision without modifying history."""
    completed = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def repository_dirty(root: Path) -> bool:
    """Return whether tracked or untracked work is present."""
    completed = subprocess.run(
        ("git", "status", "--porcelain"),
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return bool(completed.stdout)


def write_exclusive(path: Path, payload: bytes) -> None:
    """Create one retained artifact without replacement."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(payload)


def execute(request_path: Path, execution_root: Path) -> None:
    """Run one bounded local parent qualification Workflow."""
    request_path = request_path.resolve(strict=True)
    execution_root = execution_root.resolve()
    result_path = execution_root / "results" / "result.json"
    execution_path = execution_root / "execution.json"
    versions_path = execution_root / "software-versions.json"
    for path in (result_path, execution_path, versions_path):
        if path.exists():
            raise FileExistsError(f"refusing to overwrite {path}")
    request_bytes = request_path.read_bytes()
    started = time.perf_counter()
    workflow = ParentQualificationCalculationWorkflow().execute(request_bytes)
    runtime = time.perf_counter() - started
    peak_memory_bytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if platform.system() != "Darwin":
        peak_memory_bytes *= 1024
    definition = workflow.result.definition
    envelope = definition.resource_envelope
    if runtime > float(envelope.maximum_runtime_seconds):
        raise RuntimeError("parent qualification exceeded its runtime envelope")
    if peak_memory_bytes > int(envelope.maximum_peak_memory_gib * 1024**3):
        raise RuntimeError("parent qualification exceeded its memory envelope")
    if len(workflow.serialized_result) > int(
        envelope.maximum_retained_output_mib * 1024**2
    ):
        raise RuntimeError("parent qualification exceeded its retained-output envelope")

    calculation_root = Path(__file__).resolve().parent
    repository_root = calculation_root.parent.parent.resolve()
    script_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result_sha256 = hashlib.sha256(workflow.serialized_result).hexdigest()
    write_exclusive(result_path, workflow.serialized_result)
    versions = canonical_json(
        {
            "schema_version": 1,
            "record_type": "periodic2d_rank_defect_parent_qualification_versions",
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        }
    )
    write_exclusive(versions_path, versions)
    execution = canonical_json(
        {
            "schema_version": 1,
            "record_type": "periodic2d_rank_defect_parent_qualification_execution",
            "calculation_family": CALCULATION_FAMILY,
            "execution_id": EXECUTION_ID,
            "execution_status": "completed",
            "external_execution": False,
            "network_access": False,
            "accepted_parent_projection_read": True,
            "defect_campaign_executed": False,
            "request_path": request_path.relative_to(repository_root).as_posix(),
            "request_sha256": hashlib.sha256(request_bytes).hexdigest(),
            "result_sha256": result_sha256,
            "calculation_script_sha256": script_sha256,
            "criterion_status": "pass" if workflow.result.passes else "fail",
            "parent_count": len(workflow.result.parents),
            "perturbation_count": len(workflow.result.perturbations),
            "parent_route_evaluations": sum(
                value.route_evaluations for value in workflow.result.parents
            ),
            "defect_route_evaluations": sum(
                value.route_evaluations for value in workflow.result.perturbations
            ),
            "resource_observation": {
                "runtime_seconds": runtime,
                "peak_memory_bytes": peak_memory_bytes,
                "retained_result_bytes": len(workflow.serialized_result),
            },
            "repository": {
                "revision": repository_revision(repository_root),
                "working_tree_dirty": repository_dirty(repository_root),
            },
            "claim_boundary": definition.claim_boundary,
        }
    )
    write_exclusive(execution_path, execution)


def main() -> None:
    """Parse retained request and output locations."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--execution-root", type=Path, required=True)
    arguments = parser.parse_args()
    execute(arguments.request, arguments.execution_root)


if __name__ == "__main__":
    main()
