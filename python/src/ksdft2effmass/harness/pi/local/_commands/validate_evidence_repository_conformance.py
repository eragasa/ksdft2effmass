"""Fail closed unless every maintained Python test module conforms.

This local completion gate binds the generic structural validator to the explicit
ksdft2effmass repository inventory. Structural success does not establish semantic
cohesion, oracle independence, mathematics, scientific validation, UQ, or human
acceptance.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

CLAIM_BOUNDARY = [
    "semantic cohesion",
    "oracle independence",
    "field completeness beyond declared structural inventories",
    "mathematical correctness",
    "tolerance adequacy",
    "scientific validation",
    "uncertainty quantification",
    "human acceptance",
]


def issue(code: str, path: str, message: str) -> dict[str, str]:
    """Return one stable repository-conformance finding."""
    return {"code": code, "path": path, "message": message, "severity": "error"}


def maintained_modules(test_root: Path) -> list[Path]:
    """Discover regular Python modules with top-level pytest test functions."""
    modules: list[Path] = []
    for path in sorted(test_root.rglob("*.py")):
        if path.is_symlink() or "__pycache__" in path.parts:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except OSError, UnicodeError, SyntaxError:
            modules.append(path)
            continue
        if any(
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
            for node in tree.body
        ):
            modules.append(path)
    return modules


def collected_node_count(repository_root: Path) -> tuple[int | None, str]:
    """Collect the maintained pytest tree and return its exact expanded node count."""
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q"],
        cwd=repository_root / "python",
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    output = completed.stdout + completed.stderr
    if completed.returncode != 0:
        return None, output[-4000:]
    lines = [line for line in completed.stdout.splitlines() if "::test_" in line]
    return len(lines), output[-4000:]


def run(argv: Sequence[str] | None = None) -> int:
    """Validate inventory closure, identities, structural rules, and collection."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", required=True, type=Path)
    args = parser.parse_args(argv)
    root = args.repository_root.resolve(strict=True)
    inventory_path = root / ".pi/evidence/python-conformance/module-inventory.json"
    schema_path = root / "harness/pi/schemas/evidence/module-inventory.schema.json"
    validator_path = root / "python/src/cli/validate_python_conformance.py"
    findings: list[dict[str, Any]] = []
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        findings.append(
            issue("TE.REPOSITORY_INPUT", inventory_path.as_posix(), str(error))
        )
        inventory = None
        schema = None
    if isinstance(schema, dict) and isinstance(inventory, dict):
        for schema_error in Draft202012Validator(schema).iter_errors(inventory):
            findings.append(
                issue(
                    "TE.REPOSITORY_SCHEMA",
                    inventory_path.relative_to(root).as_posix(),
                    f"{list(schema_error.absolute_path)}: {schema_error.message}",
                )
            )
    modules = maintained_modules(root / "python/tests")
    relative_modules = [path.relative_to(root).as_posix() for path in modules]
    entries: list[dict[str, Any]] = []
    if isinstance(inventory, dict) and isinstance(inventory.get("modules"), list):
        entries = [entry for entry in inventory["modules"] if isinstance(entry, dict)]
        declared = [
            value for entry in entries if isinstance(value := entry.get("path"), str)
        ]
        if len(declared) != len(set(declared)):
            findings.append(
                issue(
                    "TE.REPOSITORY_DUPLICATE_PATH",
                    inventory_path.as_posix(),
                    "inventory paths must be unique",
                )
            )
        if set(declared) != set(relative_modules):
            missing = sorted(set(relative_modules) - set(declared))
            stale = sorted(set(declared) - set(relative_modules))
            findings.append(
                issue(
                    "TE.REPOSITORY_COVERAGE",
                    inventory_path.relative_to(root).as_posix(),
                    "inventory must exactly cover maintained modules; "
                    f"missing={missing}, stale={stale}",
                )
            )
        if inventory.get("expected_module_count") != len(relative_modules):
            findings.append(
                issue(
                    "TE.REPOSITORY_MODULE_COUNT",
                    inventory_path.relative_to(root).as_posix(),
                    f"expected {inventory.get('expected_module_count')} modules "
                    f"but discovered {len(relative_modules)}",
                )
            )
        for entry in entries:
            raw_path = entry.get("path")
            if not isinstance(raw_path, str):
                continue
            path = root / raw_path
            if path.is_file():
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                if entry.get("content_sha256") != digest:
                    findings.append(
                        issue(
                            "TE.REPOSITORY_IDENTITY",
                            raw_path,
                            "content SHA-256 differs from the maintained inventory",
                        )
                    )
            if entry.get("conformance_status") != "conforming":
                findings.append(
                    issue(
                        "TE.REPOSITORY_STATUS",
                        raw_path,
                        "module is not recorded as conforming",
                    )
                )
    collection_count, collection_output = collected_node_count(root)
    if collection_count is None:
        findings.append(
            issue(
                "TE.REPOSITORY_COLLECTION",
                "python/tests",
                f"pytest collection failed: {collection_output}",
            )
        )
    elif isinstance(inventory, dict) and collection_count != inventory.get(
        "expected_collected_node_count"
    ):
        findings.append(
            issue(
                "TE.REPOSITORY_COLLECTION_COUNT",
                inventory_path.relative_to(root).as_posix(),
                "expected "
                f"{inventory.get('expected_collected_node_count')} collected nodes "
                f"but collected {collection_count}",
            )
        )
    structural_result: dict[str, Any] | None = None
    if not findings and relative_modules:
        completed = subprocess.run(
            [
                sys.executable,
                str(validator_path),
                "--profile-matrix",
                "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json",
                "--migration-map",
                ".pi/evidence/python-conformance/r2.3-private-owner-migration.json",
                *relative_modules,
            ],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        try:
            structural_result = json.loads(completed.stdout)
        except json.JSONDecodeError:
            findings.append(
                issue(
                    "TE.REPOSITORY_STRUCTURAL",
                    validator_path.relative_to(root).as_posix(),
                    completed.stdout[-4000:] or completed.stderr[-4000:],
                )
            )
        else:
            findings.extend(structural_result.get("findings", []))
    result = {
        "schema_version": 1,
        "status": "PASS" if not findings else "FAIL",
        "claim_boundary": CLAIM_BOUNDARY,
        "counts": {
            "baseline_modules": inventory.get("baseline_module_count")
            if isinstance(inventory, dict)
            else None,
            "baseline_collected_nodes": inventory.get("baseline_collected_node_count")
            if isinstance(inventory, dict)
            else None,
            "discovered_modules": len(relative_modules),
            "collected_nodes": collection_count,
            "findings": len(findings),
        },
        "findings": findings,
        "structural_result": structural_result,
    }
    print(json.dumps(result, ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0 if not findings else 1
