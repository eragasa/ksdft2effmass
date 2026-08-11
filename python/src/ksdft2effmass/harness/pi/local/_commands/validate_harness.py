"""Stable thin renderer for deterministic project-local repository validation."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

from ksdft2effmass.harness.pi.local.validation import (
    HarnessValidationRequest,
    HarnessValidator,
)


def run(argv: Sequence[str] | None = None) -> int:
    """Validate one explicit repository root and render deterministic JSON."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        request = HarnessValidationRequest(args.repository_root)
        request.repository_root.resolve(strict=True)
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
    print(
        json.dumps(
            asdict(result),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 1 if result.status == "FAIL" else 0
