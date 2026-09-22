"""Thin CLI renderer for maintained repository Python-evidence conformance."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

from ksdft2effmass.harness.pi.local.evidence_repository_conformance import (
    _EvidenceRepositoryConformanceValidator,
)
from ksdft2effmass.harness.pi.local.validation import HarnessValidationRequest


def run(argv: Sequence[str] | None = None) -> int:
    """Parse one root, invoke repository conformance once, and render stable JSON."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        request = HarnessValidationRequest(args.repository_root)
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
        result = _EvidenceRepositoryConformanceValidator().execute(request)
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
    payload = {
        "schema_version": 1,
        "status": result.status,
        "claim_boundary": list(result.claim_boundary),
        "counts": {
            "baseline_modules": result.baseline_modules,
            "baseline_collected_nodes": result.baseline_collected_nodes,
            "discovered_modules": result.discovered_modules,
            "collected_nodes": result.collected_nodes,
            "findings": len(result.findings),
        },
        "findings": [asdict(finding) for finding in result.findings],
        "structural_result": {
            "status": result.status,
            "counts": {"unique_evidence_owners": result.unique_evidence_owners},
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
    return 1 if result.status == "FAIL" else 0
