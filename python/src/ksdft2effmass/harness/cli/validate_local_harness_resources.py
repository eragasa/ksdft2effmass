"""Thin CLI adapter for explicit current Harness resource composition."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

from ksdft2effmass.harness.pi.local.resource_composition_validation import (
    _LocalHarnessResourceCompositionValidator,
    _LocalHarnessResourceValidationRequest,
    _LocalHarnessResourceValidationResult,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--generic-resource-root", type=Path, required=True)
    parser.add_argument("--local-resource-root", type=Path, required=True)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--generic-manifest", type=Path, required=True)
    parser.add_argument("--local-manifest", type=Path, required=True)
    return parser


def _emit(payload: dict[str, object]) -> None:
    print(json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True))


def _payload(result: _LocalHarnessResourceValidationResult) -> dict[str, object]:
    return {
        "issues": [asdict(issue) for issue in result.issues],
        "resources": [
            {
                "issues": [asdict(issue) for issue in resource.issues],
                "resource_id": resource.resource_id,
                "status": resource.status,
            }
            for resource in result.resources
        ],
        "schema_version": 1,
        "stage": result.stage,
        "status": result.status,
    }


def run(argv: Sequence[str] | None = None) -> int:
    """Parse explicit paths, invoke the composition owner once, and render JSON."""
    args = _parser().parse_args(argv)
    request = _LocalHarnessResourceValidationRequest(
        args.repository_root,
        args.generic_resource_root,
        args.local_resource_root,
        args.profile,
        args.generic_manifest,
        args.local_manifest,
    )
    try:
        result = _LocalHarnessResourceCompositionValidator().execute(request)
    except (OSError, TypeError, ValueError) as exc:
        _emit(
            {
                "error": str(exc),
                "resources": [],
                "schema_version": 1,
                "stage": "input",
                "status": "INVALID_INPUT",
            }
        )
        return 2
    except Exception as exc:  # noqa: BLE001 - last-resort command boundary
        _emit(
            {
                "error": f"{type(exc).__name__}: {exc}",
                "resources": [],
                "schema_version": 1,
                "stage": "internal",
                "status": "INTERNAL_ERROR",
            }
        )
        return 3
    _emit(_payload(result))
    return 1 if result.status == "FAIL" else 0
