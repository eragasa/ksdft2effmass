"""Stable command-line surface for authoritative harness control state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .dbcontrol import (
    HarnessControlMigrationRequest,
    HarnessControlMigrationResult,
    HarnessControlMigrator,
    HarnessControlVerificationResult,
    HarnessControlVerifier,
)


def main() -> int:
    """Migrate or verify one explicitly selected repository root."""
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("migrate", "verify"))
    parser.add_argument("--repository-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.repository_root.resolve()
    result: HarnessControlMigrationResult | HarnessControlVerificationResult
    if args.action == "migrate":
        result = HarnessControlMigrator().execute(HarnessControlMigrationRequest(root))
    else:
        result = HarnessControlVerifier().execute(root)
    print(
        json.dumps(
            {name: getattr(result, name) for name in result.__dataclass_fields__},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
