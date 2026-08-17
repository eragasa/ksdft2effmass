"""Command-line adapter for derived Harness projection synchronization."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

from ksdft2effmass.harness.pi.local.control.inputs import (
    _HarnessProjectionInputResolver,
)
from ksdft2effmass.harness.pi.local.dbcontrol.migration import (
    _HarnessProjectionSynchronizer,
)
from ksdft2effmass.harness.pi.local.dbcontrol.records import (
    _HarnessProjectionSyncResult,
    _HarnessProjectionVerificationResult,
)
from ksdft2effmass.harness.pi.local.dbcontrol.verification import (
    _HarnessProjectionVerifier,
)


def _verification_passed(result: _HarnessProjectionVerificationResult) -> bool:
    """Return whether every represented control verification check agrees."""
    return (
        result.integrity_check == "ok"
        and result.foreign_key_issue_count == 0
        and result.semantic_digest == result.reconstructed_semantic_digest
        and result.projections_identical
        and result.schema_version_agrees
        and result.sql_identical
        and result.manifest_identical
        and not result.findings
    )


def cli_main(argv: Sequence[str] | None = None) -> int:
    """Synchronize or compare derived projections for one repository root."""
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("sync", "check"))
    parser.add_argument("--repository-root", type=Path, required=True)
    args = parser.parse_args(argv)
    root = args.repository_root.resolve()
    try:
        result = _execute(args.action, root)
    except (TypeError, ValueError) as exc:
        print(json.dumps({"error": str(exc), "status": "INVALID_INPUT"}))
        return 2
    except Exception as exc:  # noqa: BLE001 - exact command-boundary translation
        print(
            json.dumps(
                {"error": f"{type(exc).__name__}: {exc}", "status": "INTERNAL_ERROR"}
            )
        )
        return 3
    print(json.dumps(asdict(result), indent=2))
    if isinstance(result, _HarnessProjectionVerificationResult):
        return 0 if _verification_passed(result) else 1
    return 0


def _execute(
    action: str, root: Path
) -> _HarnessProjectionSyncResult | _HarnessProjectionVerificationResult:
    """Execute one action from the exact repository-owned configuration sources."""
    if action == "sync":
        inputs = _HarnessProjectionInputResolver().execute(root)
        return _HarnessProjectionSynchronizer().execute(inputs.request)
    return _HarnessProjectionVerifier().execute(root)


main = cli_main


if __name__ == "__main__":
    raise SystemExit(cli_main())
