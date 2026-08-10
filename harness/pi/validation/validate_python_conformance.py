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

_EVIDENCE_PACKAGE = import_module(
    "".join(("ksdft2", "effmass.harness.pi.evidence"))  # noqa: FLY002 - generic identity
)
PythonConformanceFinding = _EVIDENCE_PACKAGE.PythonConformanceFinding
PythonConformanceRequest = _EVIDENCE_PACKAGE.PythonConformanceRequest
PythonModuleSource = _EVIDENCE_PACKAGE.PythonModuleSource
PythonConformanceResult = _EVIDENCE_PACKAGE.PythonConformanceResult
PythonConformanceValidator = _EVIDENCE_PACKAGE.PythonConformanceValidator


def _read(path: Path) -> tuple[bytes | None, str | None]:
    try:
        return path.read_bytes(), None
    except OSError as exc:
        return None, str(exc)


def _source(path: Path) -> Any:
    rendered = path.as_posix()
    if not path.is_file() or path.is_symlink():
        return PythonModuleSource(rendered, None, False)
    payload, error = _read(path)
    return PythonModuleSource(rendered, payload, True, error)


def _finding_object(finding: Any) -> dict[str, object]:
    if type(finding) is not PythonConformanceFinding:
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
    args = parser.parse_args()
    parsed_models: tuple[Any, ...] = ()
    source_inputs: tuple[Any, ...]
    if args.ownership is not None:
        if args.ownership.as_posix().endswith("module-inventory.json"):
            parser.error("generated module inventory is projection-only")
        ownership_payload, ownership_error = _read(args.ownership)
        ownership_path = args.ownership.as_posix()
        source_inputs = tuple(_source(path) for path in args.paths)
    else:
        parser_impl = import_module(
            "ksdft2effmass.harness.pi.evidence.python_conformance.parser"
        )
        entries = []
        models = []
        sources = []
        for path in args.paths:
            payload = path.read_bytes()
            model = parser_impl.parse_module(path.as_posix(), payload)
            models.append(model)
            sources.append(PythonModuleSource(path.as_posix(), payload))
            entry = {
                "path": path.as_posix(),
                "mode": model.ownership_kind,
                "evidence_class": model.evidence_class,
                "evidence_profile": model.evidence_profile,
            }
            entry["sut" if model.ownership_kind == "class_owned" else "artifact"] = (
                model.owner_subject
            )
            entries.append(entry)
        ownership_payload = json.dumps(
            {"schema_version": 1, "modules": entries}, separators=(",", ":")
        ).encode()
        ownership_error = None
        ownership_path = "<source-embedded-module-declarations>"
        parsed_models = tuple(models)
        source_inputs = tuple(sources)
    migration_payload: bytes | None = None
    migration_error: str | None = None
    if args.migration_map is not None:
        migration_payload, migration_error = _read(args.migration_map)
    profile_payload: bytes | None = None
    profile_error: str | None = None
    if args.profile_matrix is not None:
        profile_payload, profile_error = _read(args.profile_matrix)
    request = PythonConformanceRequest(
        source_inputs,
        ownership_path,
        ownership_payload,
        ownership_error,
        args.migration_map.as_posix() if args.migration_map is not None else None,
        migration_payload,
        migration_error,
        args.profile_matrix.as_posix() if args.profile_matrix is not None else None,
        profile_payload,
        profile_error,
        parsed_models,
    )
    result = PythonConformanceValidator().execute(request)
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
