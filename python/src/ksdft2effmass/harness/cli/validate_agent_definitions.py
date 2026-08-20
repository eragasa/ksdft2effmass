"""Validate one explicit project Pi agent inventory without modifying it."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

from ksdft2effmass.harness.pi.local.agent_definition_validation import (
    _PiHarnessAgentDefinitionSetValidator,
)


def run(argv: Sequence[str] | None = None) -> int:
    """Run deterministic project-agent descriptor validation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--agent-root", required=True, type=Path)
    parser.add_argument("--settings", required=True, type=Path)
    parser.add_argument("--skill-root", required=True, action="append", type=Path)
    parser.add_argument("--allowed-external-override", action="append", default=[])
    args = parser.parse_args(argv)
    try:
        result = _PiHarnessAgentDefinitionSetValidator().execute(
            args.repository_root,
            args.agent_root,
            args.settings,
            tuple(args.skill_root),
            tuple(args.allowed_external_override),
        )
    except (TypeError, ValueError, OSError) as exc:
        print(json.dumps({"error": str(exc), "status": "INVALID_INPUT"}))
        return 2
    print(json.dumps(asdict(result), indent=2))
    return 0 if result.status == "PASS" else 1
