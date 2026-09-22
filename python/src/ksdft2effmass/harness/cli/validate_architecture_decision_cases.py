"""CLI adapter for controlled architecture-decision case validation."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from ksdft2effmass.harness.pi.local.architecture_decision_case_validation import (
    _ArchitectureDecisionCaseSetValidator,
)


def run(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", required=True, type=Path)
    args = parser.parse_args(argv)
    root = args.repository_root.resolve(strict=True)
    result = _ArchitectureDecisionCaseSetValidator().execute(root)
    payload = {
        "schema_version": 1,
        "fixture_scope": result.fixture_scope,
        "applicable_cases": result.applicable_cases,
        "non_applicable_cases": result.non_applicable_cases,
        "status": result.status,
        "issues": list(result.issues),
    }
    print(json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0 if not result.issues else 1
