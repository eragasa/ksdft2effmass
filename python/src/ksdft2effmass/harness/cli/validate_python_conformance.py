"""Thin CLI adapter for explicit Python test-evidence conformance."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from ksdft2effmass.harness.pi.conformance.python import (
    PythonConformanceFinding,
    PythonConformanceResult,
)
from ksdft2effmass.harness.pi.local.python_conformance_command import (
    _PythonConformanceCommandValidator,
)


def _finding_object(finding: PythonConformanceFinding) -> dict[str, object]:
    value: dict[str, object] = {
        "code": finding.code,
        "message": finding.message,
        "path": finding.path,
        "severity": finding.severity,
    }
    if finding.line is not None:
        value["line"] = finding.line
    return value


def _result_object(result: PythonConformanceResult) -> dict[str, object]:
    return {
        "claim_boundary": list(result.claim_boundary),
        "counts": {
            "artifact_owned_modules": result.artifact_owned_modules,
            "class_owned_modules": result.class_owned_modules,
            "evidence_class_modules": dict(result.evidence_class_modules),
            "findings_by_code": dict(result.findings_by_code),
            "helper_functions": result.helper_functions,
            "modules": result.modules,
            "parameterized_functions": result.parameterized_functions,
            "static_collected_parameter_cases": result.static_collected_parameter_cases,
            "test_functions": result.test_functions,
            "unique_evidence_owners": result.unique_evidence_owners,
        },
        "findings": [_finding_object(finding) for finding in result.findings],
        "paths": list(result.paths),
        "schema_version": result.schema_version,
        "status": result.status,
    }


def run(argv: Sequence[str] | None = None) -> int:
    """Parse explicit inputs, invoke conformance once, and render canonical JSON."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="explicit test module paths; directories are rejected",
    )
    parser.add_argument(
        "--ownership",
        type=Path,
        help="legacy explicit JSON metadata; generated inventories are not accepted",
    )
    parser.add_argument(
        "--migration-map",
        type=Path,
        help="JSON with mappings[{old_node_id,new_node_id}]",
    )
    parser.add_argument(
        "--profile-matrix",
        type=Path,
        help="explicit versioned Python evidence-profile matrix JSON",
    )
    args = parser.parse_args(argv)
    try:
        result = _PythonConformanceCommandValidator().execute(
            tuple(args.paths),
            args.ownership,
            args.migration_map,
            args.profile_matrix,
        )
    except ValueError as exc:
        parser.error(str(exc))
    print(
        json.dumps(
            _result_object(result),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0 if result.status == "PASS" else 1
