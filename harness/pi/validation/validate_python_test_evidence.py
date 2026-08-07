#!/usr/bin/env -S python/.venv/bin/python
"""Validate structural conventions on explicitly supplied Python test paths.

This compatibility wrapper performs explicit command-line file reads only.  The
package action does not establish oracle independence, mathematical correctness,
tolerance adequacy, scientific validity, uncertainty quantification, or human
acceptance.
"""

from __future__ import annotations

import argparse
import json
from importlib import import_module
from pathlib import Path
from typing import Any

_PACKAGE = import_module(
    "".join(("ksdft2", "effmass.harness.pi"))  # noqa: FLY002 - generic identity
)
PythonTestEvidenceFinding = _PACKAGE.PythonTestEvidenceFinding
PythonTestEvidenceRequest = _PACKAGE.PythonTestEvidenceRequest
PythonTestEvidenceSource = _PACKAGE.PythonTestEvidenceSource
PythonTestEvidenceValidationResult = _PACKAGE.PythonTestEvidenceValidationResult
ValidatePythonTestEvidence = _PACKAGE.ValidatePythonTestEvidence


def _read(path: Path) -> tuple[bytes | None, str | None]:
    try:
        return path.read_bytes(), None
    except OSError as exc:
        return None, str(exc)


def _source(path: Path) -> Any:
    rendered = path.as_posix()
    if not path.is_file() or path.is_symlink():
        return PythonTestEvidenceSource(rendered, None, False)
    payload, error = _read(path)
    return PythonTestEvidenceSource(rendered, payload, True, error)


def _finding_object(finding: Any) -> dict[str, object]:
    if type(finding) is not PythonTestEvidenceFinding:
        raise TypeError("finding has wrong type")
    value: dict[str, object] = {
        "code": finding.code,
        "message": finding.message,
        "path": finding.path,
        "severity": finding.severity,
    }
    if finding.line is not None:
        value["line"] = finding.line
    return value


def _result_object(result: Any) -> dict[str, object]:
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="explicit test module paths; directories are rejected",
    )
    parser.add_argument(
        "--ownership",
        required=True,
        type=Path,
        help="JSON with modules[{path,mode,evidence_class,sut?|artifact?}]",
    )
    parser.add_argument(
        "--migration-map",
        type=Path,
        help="JSON with mappings[{old_node_id,new_node_id}]",
    )
    args = parser.parse_args()
    ownership_payload, ownership_error = _read(args.ownership)
    migration_payload: bytes | None = None
    migration_error: str | None = None
    if args.migration_map is not None:
        migration_payload, migration_error = _read(args.migration_map)
    request = PythonTestEvidenceRequest(
        tuple(_source(path) for path in args.paths),
        args.ownership.as_posix(),
        ownership_payload,
        ownership_error,
        args.migration_map.as_posix() if args.migration_map is not None else None,
        migration_payload,
        migration_error,
    )
    result = ValidatePythonTestEvidence().execute(request)
    print(
        json.dumps(
            _result_object(result),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0 if result.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
