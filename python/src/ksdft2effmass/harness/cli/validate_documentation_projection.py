"""CLI adapter for explicit documentation-projection validation."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from ksdft2effmass.harness.pi.local.documentation_projection_validation import (
    _DocumentationProjectionValidator,
)


def run(argv: Sequence[str] | None = None) -> int:
    """Validate explicit files, render explicit context, and check exact bytes."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--instance", type=Path, required=True)
    parser.add_argument("--profile-schema", type=Path)
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--context", type=Path)
    parser.add_argument("--expected", type=Path)
    parser.add_argument("--generated", type=Path)
    args = parser.parse_args(argv)
    result = _DocumentationProjectionValidator().execute(
        args.schema,
        args.instance,
        (
            args.profile_schema,
            args.profile,
            args.context,
            args.expected,
            args.generated,
        ),
    )
    payload = {
        "diagnostics": list(result.diagnostics),
        "schema_version": 1,
        "status": result.status,
    }
    print(json.dumps(payload, separators=(",", ":"), sort_keys=True))
    return 0 if not result.diagnostics else 1
