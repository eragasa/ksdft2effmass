#!/usr/bin/env python3
"""Run the authorized test-local strict ID audit over maintained evidence."""

from __future__ import annotations

import ast
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INVENTORY = (
    ROOT
    / ".pi/evidence/test-evidence-repository-conformance/maintained-test-inventory.json"
)
PROFILE = ROOT / "harness/local/profiles/ksdft2effmass-v2.json"
ID = re.compile(r"^([A-Z][A-Z0-9-]*)-(\d+)$")


def main() -> int:
    """Audit exact Evidence ID fields without changing production parser behavior."""
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    rules = {
        prefix: (minimum, maximum, width)
        for prefix, minimum, maximum, width in profile["evidence_namespace_rules"]
    }
    scope_rules = profile["evidence_scope_rules"]
    occurrences: list[tuple[str, str, str]] = []
    issues: list[dict[str, str]] = []
    for entry in inventory["modules"]:
        path = entry["path"]
        source = (ROOT / path).read_text(encoding="utf-8")
        tree = ast.parse(source)
        permitted = next(
            prefixes
            for scope, _evidence_class, prefixes in scope_rules
            if (scope["scope_kind"] == "file" and path == scope["path"])
            or (
                scope["scope_kind"] == "directory_tree"
                and path.startswith(scope["path"] + "/")
            )
        )
        for node in tree.body:
            if not isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef)
            ) or not node.name.startswith("test_"):
                continue
            doc = ast.get_docstring(node, clean=True) or ""
            match = re.search(r"(?ms)^Evidence ID\s*\n(.+?)\nRequirement$", doc)
            if match is None:
                issues.append({"code": "ID_FIELD", "path": f"{path}::{node.name}"})
                continue
            evidence_id = " ".join(
                line.strip()
                for line in match.group(1).splitlines()
                if line.strip() and not set(line.strip()) <= {"-"}
            )
            parsed = ID.fullmatch(evidence_id)
            if parsed is None:
                issues.append({"code": "ID_FORMAT", "path": f"{path}::{node.name}"})
                continue
            prefix, digits = parsed.groups()
            if prefix not in permitted or prefix not in rules:
                issues.append({"code": "ID_NAMESPACE", "path": f"{path}::{node.name}"})
                continue
            minimum, maximum, width = rules[prefix]
            if len(digits) != width or not minimum <= int(digits) <= maximum:
                issues.append({"code": "ID_RANGE", "path": f"{path}::{node.name}"})
                continue
            occurrences.append((evidence_id, path, node.name))
    duplicates = {
        evidence_id
        for evidence_id, count in Counter(item[0] for item in occurrences).items()
        if count > 1
    }
    issues.extend(
        {"code": "ID_DUPLICATE", "path": evidence_id}
        for evidence_id in sorted(duplicates)
    )
    payload = {
        "status": "PASS" if not issues else "FAIL",
        "audit_boundary": "test-local clean-docstring audit; production AuditEvidenceIdentifiers behavior unchanged",
        "modules": len(inventory["modules"]),
        "occurrences": len(occurrences),
        "unique_ids": len({item[0] for item in occurrences}),
        "issues": issues,
    }
    print(json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
