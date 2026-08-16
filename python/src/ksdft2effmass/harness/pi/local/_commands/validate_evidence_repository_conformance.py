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

from ksdft2effmass.harness.pi.evidence.python_conformance.corpus import (
    _PythonTestModuleCorpusBuilder,
    _PythonTestModuleInput,
)
from ksdft2effmass.harness.pi.evidence.python_conformance.nodes import (
    _PythonTestNodeProjector,
)
from ksdft2effmass.harness.pi.local import (
    HarnessValidationRequest,
    HarnessValidator,
)
from ksdft2effmass.harness.pi.local.control.inputs import (
    _HarnessProjectionInputResolver,
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
        inputs = _HarnessProjectionInputResolver().execute(request.repository_root)
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
        evidence = result.checks[0]
        module_inputs = tuple(
            _PythonTestModuleInput(
                path.as_posix(), (inputs.request.repository_root / path).read_bytes()
            )
            for path in inputs.request.evidence_module_paths
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
        for code, path, message in evidence.findings
    ]
    payload = {
        "schema_version": 1,
        "status": evidence.status,
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
            "status": evidence.status,
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
    return 1 if evidence.status == "FAIL" else 0
