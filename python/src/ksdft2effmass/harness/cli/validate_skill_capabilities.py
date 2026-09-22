"""CLI adapter for repository-local skill capability validation."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from ksdft2effmass.harness.pi.local.skill_capability_validation import (
    _SkillCapabilityInventoryValidator,
)


def run(argv: Sequence[str] | None = None) -> int:
    """Validate all deterministic skill-capability inventory invariants."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--inventory", type=Path)
    args = parser.parse_args(argv)
    root = args.repository_root.resolve(strict=True)
    inventory_path = args.inventory or (
        root / ".pi/skills/skill-capability-inventory.json"
    )
    if not inventory_path.is_absolute():
        inventory_path = root / inventory_path
    result = _SkillCapabilityInventoryValidator().execute(root, inventory_path)
    print(f"skill_records={result.skill_records}")
    print(f"filesystem_skills={result.filesystem_skills}")
    print(f"cpn_review_blocks={result.review_blocks}")
    print(f"deterministic_tool_blocks={result.tool_blocks}")
    print(f"validation_errors={len(result.errors)}")
    for error in result.errors:
        print(f"ERROR: {error}")
    return 1 if result.errors else 0
