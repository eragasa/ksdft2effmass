"""Thin direct repository renderer for maintained Python evidence conformance.

The command invokes the project-local validation Action directly. It never launches
pytest, invokes another CLI, parses command output, or treats the generated module
inventory as source authority.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from ksdft2effmass.harness.pi.conformance.python.corpus import (
    _PythonTestModuleCorpusBuilder,
    _PythonTestModuleInput,
)
from ksdft2effmass.harness.pi.conformance.python.nodes import (
    _PythonTestNodeProjector,
)
from ksdft2effmass.harness.pi.local import (
    HarnessValidationRequest,
    HarnessValidator,
)
from ksdft2effmass.harness.pi.local.conformance_inputs import (
    _PythonConformanceInputResolver,
)
from ksdft2effmass.harness.pi.local.control.configuration_inputs import (
    _HarnessConfigurationInputResolver,
)

CLAIM_BOUNDARY = [
    "semantic cohesion",
    "oracle independence",
    "field completeness beyond declared structural inventories",
    "mathematical correctness",
    "tolerance adequacy",
    "scientific validation",
    "uncertainty quantification",
    "human acceptance",
]


def run(argv: Sequence[str] | None = None) -> int:
    """Validate source-derived repository Python evidence and render stable JSON."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        request = HarnessValidationRequest(args.repository_root)
        configuration = (
            _HarnessConfigurationInputResolver()
            .execute(request.repository_root)
            .configuration.python_conformance
        )
        inputs = _PythonConformanceInputResolver().execute(
            request.repository_root,
            pyproject_path=Path(configuration.pyproject_path),
            test_root_path=Path(configuration.test_root),
            profile_path=Path(configuration.profile_matrix_path),
            migration_path=Path(configuration.migration_map_path),
        )
    except (OSError, TypeError, ValueError) as exc:
        print(
            json.dumps(
                {
                    "error": str(exc),
                    "schema_version": 1,
                    "status": "INVALID_INPUT",
                },
                ensure_ascii=True,
                separators=(",", ":"),
                sort_keys=True,
            )
        )
        return 2
    try:
        result = HarnessValidator().execute(request)
        conformance = result.checks[0]
        module_inputs = tuple(
            _PythonTestModuleInput(
                path.as_posix(), (inputs.repository_root / path).read_bytes()
            )
            for path in inputs.module_paths
        )
        corpus = _PythonTestModuleCorpusBuilder().execute(module_inputs)
        nodes = _PythonTestNodeProjector().execute(corpus.models)
        owner_count = sum(
            function.is_test for model in corpus.models for function in model.functions
        )
    except Exception as exc:  # noqa: BLE001 - exact command-boundary translation
        print(
            json.dumps(
                {
                    "error": f"{type(exc).__name__}: {exc}",
                    "schema_version": 1,
                    "status": "INTERNAL_ERROR",
                },
                ensure_ascii=True,
                separators=(",", ":"),
                sort_keys=True,
            )
        )
        return 3
    findings = [
        {"code": code, "path": path, "message": message, "severity": "error"}
        for code, path, message in conformance.findings
    ]
    payload = {
        "schema_version": 1,
        "status": conformance.status,
        "claim_boundary": CLAIM_BOUNDARY,
        "counts": {
            "baseline_modules": 182,
            "baseline_collected_nodes": 2383,
            "discovered_modules": len(corpus.models),
            "collected_nodes": len(nodes),
            "findings": len(findings),
        },
        "findings": findings,
        "structural_result": {
            "status": conformance.status,
            "counts": {"unique_evidence_owners": owner_count},
        },
    }
    print(
        json.dumps(
            payload,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 1 if conformance.status == "FAIL" else 0
