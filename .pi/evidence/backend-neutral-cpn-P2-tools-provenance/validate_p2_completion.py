#!/usr/bin/env python3
"""Validate structural P2 completion conditions without frozen test totals."""

from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "python/src/ksdft2effmass/provenance"
TESTS = ROOT / "python/tests/software_verification/ksdft2effmass/provenance"
SCHEMA = ROOT / "specification/provenance/v1"
REQUIRED_DOCS = (
    "docs/api/provenance.md",
    "docs/concepts/provenance-and-artifacts.md",
    "docs/user-guide/provenance-and-artifacts.md",
    "docs/user-guide/external-tool-lifecycle.md",
    "docs/verification/provenance-contract.rst",
)
BANNED_TEXT = (
    "workflows.cpn",
    "import snakes",
    "from snakes",
    "import subprocess",
    "from subprocess",
    "scheduler",
    "service_locator",
    "backend_registry",
)


def main() -> int:
    issues: list[str] = []
    init_path = SOURCE / "__init__.py"
    if not init_path.is_file():
        issues.append("missing public provenance package")
        exports: tuple[str, ...] = ()
    else:
        namespace: dict[str, object] = {}
        try:
            tree = ast.parse(init_path.read_text(encoding="utf-8"))
            assignment = next(
                node
                for node in tree.body
                if isinstance(node, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets)
            )
            value = ast.literal_eval(assignment.value)
            exports = tuple(value) if isinstance(value, (tuple, list)) else ()
        except (OSError, UnicodeError, SyntaxError, StopIteration, ValueError):
            exports = ()
            issues.append("public __all__ is not a literal tuple or list")
        if not exports or len(exports) != len(set(exports)) or tuple(sorted(exports)) != exports:
            issues.append("public __all__ must be nonempty, unique, and sorted")

    for path in SOURCE.glob("*.py"):
        text = path.read_text(encoding="utf-8").lower()
        for banned in BANNED_TEXT:
            if banned in text:
                issues.append(f"forbidden dependency text {banned!r} in {path.relative_to(ROOT)}")

    if exports and TESTS.is_dir():
        module_names = {path.name for path in TESTS.glob("test__*.py")}
        for name in exports:
            if name.endswith(("Status", "Kind", "Stage", "Algorithm", "ErrorCode")):
                continue
            expected = f"test__{name}.py"
            if expected not in module_names:
                issues.append(f"missing class-owned module {expected}")
        for path in TESTS.glob("test__*.py"):
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, SyntaxError):
                issues.append(f"unparseable test module {path.relative_to(ROOT)}")
                continue
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
                    if "__" not in node.name:
                        issues.append(f"nonsemantic test name {path.name}:{node.name}")
    elif not TESTS.is_dir():
        issues.append("missing class-owned provenance test directory")

    schemas = tuple(SCHEMA.glob("*.schema.json")) if SCHEMA.is_dir() else ()
    fixtures = tuple(SCHEMA.glob("fixtures/**/*.json")) if SCHEMA.is_dir() else ()
    if not schemas:
        issues.append("missing provenance schemas")
    if not fixtures:
        issues.append("missing provenance fixtures")
    for relative in REQUIRED_DOCS:
        if not (ROOT / relative).is_file():
            issues.append(f"missing maintained document {relative}")

    result = {
        "schema_version": 1,
        "task_id": "P2",
        "status": "PASS" if not issues else "FAIL",
        "observed": {
            "public_exports": len(exports),
            "class_owned_modules": len(tuple(TESTS.glob('test__*.py'))) if TESTS.is_dir() else 0,
            "schemas": len(schemas),
            "fixtures": len(fixtures),
        },
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
