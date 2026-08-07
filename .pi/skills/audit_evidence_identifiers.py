#!/usr/bin/env -S python/.venv/bin/python
"""Audit executable ownership of migrated VVUQ evidence identifiers.

The ``Evidence ID`` field of a migrated pytest test-function docstring is the
deterministic owner declaration for one explicit ``SV-...-###`` or
``NV-...-###`` identifier, or one same-stem inclusive ``...-### through
...-###`` range for a parametrized test. Historical docstrings remain supported:
when no ``Evidence ID`` field exists, their first line is the owner declaration.
Other mentions in module, helper, or test prose are references and do not create
ownership. This distinction avoids false duplicate findings from raw grep.

The default mode fails on duplicate ownership, class/hierarchy disagreement,
syntax errors, or missing VVUQ module markers. It reports test functions without
an owner declaration as migration warnings. ``--strict`` also fails on those
warnings and is the authoritative EvidenceIdentifierAuditBlock once the audited
surface is declared fully migrated.
"""

from __future__ import annotations

import argparse
import ast
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEST_ROOT = ROOT / "python" / "tests"
EVIDENCE_ID = re.compile(r"\b((?:SV|NV)-[A-Z][A-Z0-9]*-\d{3})\b")
EVIDENCE_RANGE = re.compile(
    r"(?P<start>(?:SV|NV)-[A-Z][A-Z0-9]*-\d{3})(?:``)?\s+through\s+"
    r"(?:``)?(?P<end>(?:SV|NV)-[A-Z][A-Z0-9]*-\d{3})"
)


@dataclass(frozen=True, slots=True)
class Owner:
    """One executable test-function evidence owner."""

    path: Path
    function: str
    evidence_class: str


def iter_test_modules() -> list[tuple[Path, str, str]]:
    """Return maintained software/numerical modules and expected markers."""

    modules: list[tuple[Path, str, str]] = []
    for relative, prefix, marker in (
        ("software_verification", "SV", "software_verification"),
        ("numerical_verification", "NV", "numerical_verification"),
    ):
        root = TEST_ROOT / relative
        modules.extend(
            (path, prefix, marker) for path in sorted(root.rglob("test__*.py"))
        )
    return modules


def dotted_name(node: ast.expr) -> str | None:
    """Return one statically represented dotted expression name."""

    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)
        return f"{parent}.{node.attr}" if parent else None
    return None


def module_markers(tree: ast.Module) -> list[str]:
    """Return executable module-level ``pytestmark`` marker expressions."""

    markers: list[str] = []
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if not any(
            isinstance(target, ast.Name) and target.id == "pytestmark"
            for target in targets
        ):
            continue
        value = node.value
        if value is None:
            continue
        values = value.elts if isinstance(value, (ast.List, ast.Tuple)) else [value]
        markers.extend(
            name for item in values if (name := dotted_name(item)) is not None
        )
    return markers


def owner_declaration(docstring: str) -> tuple[str, list[str]]:
    """Return the fielded owner body or historical first-line declaration."""

    field_matches = list(re.finditer(r"(?m)^Evidence ID\s*$", docstring))
    if len(field_matches) > 1:
        return "", ["docstring contains multiple Evidence ID fields"]
    if not field_matches:
        return (docstring.splitlines()[0] if docstring else ""), []

    start = field_matches[0].end()
    requirement = re.search(r"(?m)^Requirement\s*$", docstring[start:])
    if requirement is None:
        # A historical module may mention an ``Evidence ID`` heading while using
        # combined or differently ordered fields. Its first line remains the
        # durable owner until the complete unified grammar is adopted.
        return (docstring.splitlines()[0] if docstring else ""), []
    body = docstring[start : start + requirement.start()].strip()
    if not body:
        return "", ["Evidence ID field is empty"]
    return body, []


def declared_evidence_ids(declaration: str) -> tuple[list[str], list[str]]:
    """Expand one owner identifier or one normalized inclusive range."""

    declaration_errors: list[str] = []
    ranges = list(EVIDENCE_RANGE.finditer(declaration))
    if len(ranges) > 1:
        return [], ["first-line owner declaration contains multiple ranges"]
    if ranges:
        match = ranges[0]
        start = match.group("start")
        end = match.group("end")
        start_stem, start_number = start.rsplit("-", 1)
        end_stem, end_number = end.rsplit("-", 1)
        if start_stem != end_stem or int(end_number) < int(start_number):
            return [], [f"invalid evidence range {start} through {end}"]
        remainder = declaration[: match.start()] + declaration[match.end() :]
        if EVIDENCE_ID.search(remainder):
            declaration_errors.append(
                "first-line range declaration also contains a separate "
                "evidence identifier"
            )
        width = len(start_number)
        declared = [
            f"{start_stem}-{number:0{width}d}"
            for number in range(int(start_number), int(end_number) + 1)
        ]
        return declared, declaration_errors

    declared = sorted(set(EVIDENCE_ID.findall(declaration)))
    if len(declared) > 1:
        declaration_errors.append(
            "first-line owner declaration contains multiple identifiers "
            "without one range"
        )
    return declared, declaration_errors


def run_self_test() -> list[str]:
    """Exercise range expansion and executable marker extraction."""

    failures: list[str] = []
    expanded, errors = declared_evidence_ids(
        "Execute ``NV-ABC-001`` through ``NV-ABC-003``."
    )
    if expanded != ["NV-ABC-001", "NV-ABC-002", "NV-ABC-003"] or errors:
        failures.append("inclusive range expansion failed")
    _, malformed_errors = declared_evidence_ids("Own SV-A-001 and SV-A-002.")
    if not malformed_errors:
        failures.append("ambiguous multiple-identifier declaration was not rejected")
    fielded, field_errors = owner_declaration(
        "Summary.\n\nEvidence ID\n    ``SV-A-004``.\nRequirement\n    Public rule."
    )
    if fielded != "``SV-A-004``." or field_errors:
        failures.append("fielded Evidence ID extraction failed")
    historical, historical_errors = owner_declaration("SV-A-005: historical owner.")
    if historical != "SV-A-005: historical owner." or historical_errors:
        failures.append("historical first-line extraction failed")
    legacy_field, legacy_errors = owner_declaration(
        "NV-A-006: historical owner.\n\nEvidence ID\n    ``NV-A-006``.\n"
        "Requirement and method\n    Legacy combined field."
    )
    if legacy_field != "NV-A-006: historical owner." or legacy_errors:
        failures.append("historical combined-field fallback failed")
    tree = ast.parse(
        '"""pytestmark = pytest.mark.numerical_verification"""\n'
        "pytestmark = pytest.mark.software_verification\n"
    )
    if module_markers(tree) != ["pytest.mark.software_verification"]:
        failures.append("module marker extraction accepted non-executable marker text")
    return failures


def main() -> int:
    """Run the deterministic ownership, prefix, hierarchy, and marker audit."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict",
        action="store_true",
        help="fail when any test function lacks a fielded or historical evidence owner",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run deterministic parser probes before auditing the repository",
    )
    args = parser.parse_args()

    if args.self_test:
        self_test_failures = run_self_test()
        print(f"self_test_failures={len(self_test_failures)}")
        for failure in self_test_failures:
            print(f"ERROR: {failure}")
        if self_test_failures:
            return 1

    owners: dict[str, list[Owner]] = {}
    missing: list[tuple[Path, str]] = []
    errors: list[str] = []
    module_count = 0
    function_count = 0

    for path, expected_prefix, expected_marker in iter_test_modules():
        module_count += 1
        source = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError as error:
            errors.append(f"{path}: syntax error: {error}")
            continue

        expected_marker_name = f"pytest.mark.{expected_marker}"
        declared_markers = module_markers(tree)
        if declared_markers != [expected_marker_name]:
            errors.append(
                f"{path}: expected exactly [{expected_marker_name!r}] as executable "
                f"module marker, found {declared_markers!r}"
            )

        for node in tree.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not node.name.startswith("test_"):
                continue
            function_count += 1
            docstring = ast.get_docstring(node) or ""
            declaration, field_errors = owner_declaration(docstring)
            declared, declaration_errors = declared_evidence_ids(declaration)
            declaration_errors = field_errors + declaration_errors
            errors.extend(
                f"{path}:{node.name}: {error}" for error in declaration_errors
            )
            if not declared:
                missing.append((path, node.name))
                continue
            for evidence_id in declared:
                owner = Owner(
                    path=path, function=node.name, evidence_class=expected_prefix
                )
                owners.setdefault(evidence_id, []).append(owner)
                if not evidence_id.startswith(f"{expected_prefix}-"):
                    errors.append(
                        f"{path}:{node.name}: {evidence_id} conflicts with "
                        f"{expected_prefix} hierarchy"
                    )

    for evidence_id, declared_owners in sorted(owners.items()):
        if len(declared_owners) <= 1:
            continue
        locations = ", ".join(
            f"{owner.path.relative_to(ROOT)}:{owner.function}"
            for owner in declared_owners
        )
        errors.append(f"{evidence_id}: multiple executable owners: {locations}")

    print(f"evidence_modules={module_count}")
    print(f"test_functions={function_count}")
    print(f"owned_evidence_identifiers={len(owners)}")
    print(f"unowned_test_functions={len(missing)}")
    print(f"audit_errors={len(errors)}")

    for path, function in missing:
        print(
            f"WARNING: {path.relative_to(ROOT)}:{function}: "
            "no Evidence ID field or historical first-line owner"
        )
    for error in errors:
        print(f"ERROR: {error}")

    if errors or (args.strict and missing):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
