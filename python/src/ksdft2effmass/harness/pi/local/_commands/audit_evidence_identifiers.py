"""Thin read-only command for explicit maintained evidence-identifier auditing."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from ksdft2effmass.harness.pi import (
    ProjectProfile,
    ProjectProfileLoader,
    ValidationIssue,
)
from ksdft2effmass.harness.pi.evidence import IdentifierAuditor, IdentifierAuditResult


def _explicit_file(root: Path, supplied: Path, label: str) -> Path:
    candidate = supplied if supplied.is_absolute() else root / supplied
    resolved = candidate.resolve(strict=True)
    if not resolved.is_relative_to(root):
        raise ValueError(f"{label} must resolve beneath root")
    if candidate.is_symlink() or not resolved.is_file():
        raise ValueError(f"{label} must name a regular nonsymlink file")
    return resolved


def _load_modules(root: Path, inventory_path: Path) -> tuple[tuple[str, bytes], ...]:
    try:
        inventory: Any = json.loads(inventory_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("inventory must contain valid JSON") from exc
    if type(inventory) is not dict or type(inventory.get("modules")) is not list:
        raise ValueError("inventory must contain a modules array")
    entries = inventory["modules"]
    if not entries:
        raise ValueError("modules must be nonempty")
    if inventory.get("expected_module_count") != len(entries):
        raise ValueError("inventory module count does not match its modules array")
    modules: list[tuple[str, bytes]] = []
    seen: set[str] = set()
    for entry in entries:
        if type(entry) is not dict:
            raise ValueError("inventory module entries must be objects")
        raw_path = entry.get("path")
        expected_digest = entry.get("content_sha256")
        if type(raw_path) is not str or type(expected_digest) is not str:
            raise ValueError("inventory entries require path and content_sha256")
        if raw_path in seen:
            raise ValueError("inventory module paths must be unique")
        seen.add(raw_path)
        path = _explicit_file(root, Path(raw_path), "inventoried module")
        payload = path.read_bytes()
        if hashlib.sha256(payload).hexdigest() != expected_digest:
            raise ValueError(f"inventoried module identity mismatch: {raw_path}")
        modules.append((raw_path, payload))
    return tuple(modules)


def _issue_object(issue: ValidationIssue) -> dict[str, object]:
    return {
        "code": issue.code,
        "message": issue.message,
        "path": issue.path,
        "related_ids": list(issue.related_ids),
        "severity": issue.severity,
        "subject_id": issue.subject_id,
    }


def _command_object(
    result: IdentifierAuditResult, module_count: int
) -> dict[str, object]:
    issue_counts = Counter(issue.code for issue in result.validation.issues)
    return {
        "counts": {
            "inventoried_modules": module_count,
            "issues": len(result.validation.issues),
            "issues_by_code": dict(sorted(issue_counts.items())),
            "occurrences": len(result.occurrences),
            "unique_evidence_ids": len(
                {occurrence.evidence_id for occurrence in result.occurrences}
            ),
        },
        "findings": [_issue_object(issue) for issue in result.validation.issues],
        "occurrences": [
            {
                "evidence_id": occurrence.evidence_id,
                "line": occurrence.line,
                "path": occurrence.path,
            }
            for occurrence in result.occurrences
        ],
        "schema_version": 1,
        "status": result.validation.status,
    }


def run(argv: Sequence[str] | None = None) -> int:
    """Audit only explicitly inventoried modules beneath an explicit root.

    Exit status ``0`` means structural PASS or WARN, ``1`` means audit FAIL,
    ``2`` means invalid command input, and ``3`` is the last-resort boundary.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--inventory", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if not args.root.is_absolute():
            raise ValueError("root must be absolute")
        root = args.root.resolve(strict=True)
        if args.root.is_symlink() or not root.is_dir():
            raise ValueError("root must name a regular nonsymlink directory")
        profile_path = _explicit_file(root, args.profile, "profile")
        inventory_path = _explicit_file(root, args.inventory, "inventory")
        loaded = ProjectProfileLoader().execute(
            profile_path.read_bytes(), None, (1,), (1,)
        )
        if loaded.validation.status == "FAIL":
            raise ValueError("profile does not satisfy the supported contract")
        if type(loaded.profile) is not ProjectProfile:
            raise AssertionError("profile loader returned the wrong record kind")
        modules = _load_modules(root, inventory_path)
        result = IdentifierAuditor().execute(modules, loaded.profile)
        payload = _command_object(result, len(modules))
        exit_status = 1 if result.validation.status == "FAIL" else 0
    except (TypeError, ValueError, OSError) as exc:
        payload = {"error": str(exc), "schema_version": 1, "status": "ERROR"}
        exit_status = 2
    print(
        json.dumps(
            payload,
            ensure_ascii=True,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return exit_status
