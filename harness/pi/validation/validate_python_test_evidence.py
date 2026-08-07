#!/usr/bin/env python3
"""Validate structural conventions on explicitly supplied Python test paths.

This tool does not establish oracle independence, mathematical correctness,
tolerance adequacy, scientific validity, uncertainty quantification, or human
acceptance.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

HEADINGS = (
    "Facet and represented meaning",
    "Intrinsic and cross-object scope",
    "VVUQ and scientific exclusions",
)
SUPERSEDED_HEADINGS = (
    "Evidence class and represented meaning",
    "Owned contract, oracle, and scope",
)
FIELDS = (
    "Evidence ID",
    "Requirement",
    "Method",
    "Oracle",
    "Acceptance",
    "Interpretation",
    "Limitations",
)
SURFACES = (
    "constructor",
    "field",
    "property",
    "method",
    "classmethod",
    "staticmethod",
    "protocol",
    "public_api",
    "artifact",
    "workflow",
)
NAME_RE = re.compile(
    r"^test_(" + "|".join(SURFACES) + r")__[a-z][a-z0-9_]*__[a-z][a-z0-9_]*$"
)
ID_RE = re.compile(r"\b(?:[A-Z][A-Z0-9]*-)+[0-9]{3,}\b")
SEMANTIC_PARAM_RE = re.compile(
    r"^(?:[a-z][a-z0-9]*(?:_[a-z0-9]+)*|(?:[A-Z][A-Z0-9]*-)+[0-9]{3,}-[a-z][a-z0-9]*(?:[-_][a-z0-9]+)*)$"
)
EVIDENCE_OPENINGS = {
    "software_verification": "Software verification",
    "numerical_verification": "Numerical verification",
    "scientific_validation": "Scientific validation",
    "uncertainty_quantification": "Uncertainty quantification",
}


def finding(
    code: str, path: Path, message: str, line: int | None = None
) -> dict[str, Any]:
    value: dict[str, Any] = {
        "code": code,
        "message": message,
        "path": path.as_posix(),
        "severity": "error",
    }
    if line is not None:
        value["line"] = line
    return value


def sections(doc: str | None, labels: tuple[str, ...]) -> tuple[bool, str]:
    if not doc:
        return False, "docstring is missing"
    positions: list[int] = []
    for label in labels:
        matches = list(re.finditer(rf"(?m)^\s*{re.escape(label)}\s*:?\s*$", doc))
        if len(matches) != 1:
            return False, f"{label!r} must occur exactly once"
        positions.append(matches[0].start())
        end = matches[0].end()
        next_start = min(
            (
                m.start()
                for other in labels
                for m in re.finditer(rf"(?m)^\s*{re.escape(other)}\s*:?\s*$", doc)
                if m.start() > end
            ),
            default=len(doc),
        )
        if not doc[end:next_start].strip():
            return False, f"{label!r} has an empty body"
    if positions != sorted(positions):
        return False, "required sections are out of order"
    return True, ""


@dataclass(frozen=True)
class ParameterCaseInventory:
    """Statically resolved parameter cases and inventory-specific findings."""

    elements: tuple[ast.expr, ...] | None
    findings: tuple[tuple[str, str], ...]
    named: bool


def assigned_names(target: ast.expr) -> set[str]:
    """Return simple names stored anywhere in one assignment target."""
    if isinstance(target, ast.Name):
        return {target.id}
    if isinstance(target, (ast.List, ast.Tuple)):
        return {name for element in target.elts for name in assigned_names(element)}
    return set()


def module_scope_statements(tree: ast.Module) -> tuple[ast.stmt, ...]:
    """Return statements executed at module scope, including compound bodies."""
    statements: list[ast.stmt] = []

    def visit(node: ast.AST) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                statements.append(child)
                continue
            if isinstance(child, ast.stmt):
                statements.append(child)
            visit(child)

    visit(tree)
    return tuple(statements)


def imported_module_names(tree: ast.Module) -> set[str]:
    """Return names introduced by imports in module-executed statements."""
    names: set[str] = set()
    for statement in module_scope_statements(tree):
        if isinstance(statement, ast.Import):
            names.update(
                alias.asname or alias.name.split(".", 1)[0] for alias in statement.names
            )
        elif isinstance(statement, ast.ImportFrom):
            names.update(alias.asname or alias.name for alias in statement.names)
    return names


def module_assignments(tree: ast.Module, name: str) -> list[ast.Assign | ast.AnnAssign]:
    """Return module-level ordinary assignments that store one requested name."""
    assignments: list[ast.Assign | ast.AnnAssign] = []
    for statement in tree.body:
        if isinstance(statement, ast.Assign) and any(
            name in assigned_names(target) for target in statement.targets
        ):
            assignments.append(statement)
        elif isinstance(statement, ast.AnnAssign) and name in assigned_names(
            statement.target
        ):
            assignments.append(statement)
    return assignments


def inventory_mutation_findings(
    tree: ast.Module,
    name: str,
    assignment: ast.Assign | ast.AnnAssign,
) -> list[tuple[str, str]]:
    """Reject module-level reassignment and statically visible inventory mutation."""
    findings: list[tuple[str, str]] = []
    for statement in module_scope_statements(tree):
        if statement is assignment:
            continue
        if isinstance(statement, ast.Assign) and any(
            name in assigned_names(target) for target in statement.targets
        ):
            findings.append(
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} is reassigned",
                )
            )
        elif isinstance(statement, ast.AnnAssign) and name in assigned_names(
            statement.target
        ):
            findings.append(
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} is reassigned",
                )
            )
        elif isinstance(statement, ast.AugAssign) and (
            isinstance(statement.target, ast.Name) and statement.target.id == name
        ):
            findings.append(
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} uses augmented assignment",
                )
            )
    mutating_methods = {"append", "clear", "extend", "insert", "reverse", "sort"}
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == name
            and node.func.attr in mutating_methods
        ):
            findings.append(
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} is mutated with "
                    f"{node.func.attr}()",
                )
            )
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(
                isinstance(target, ast.Subscript)
                and isinstance(target.value, ast.Name)
                and target.value.id == name
                for target in targets
            ):
                findings.append(
                    (
                        "TE.PARAMETER_INVENTORY",
                        f"named parameter inventory {name!r} is mutated by "
                        "subscript assignment",
                    )
                )
    return findings


def resolve_parameter_case_inventory(
    tree: ast.Module, decorator: ast.Call
) -> ParameterCaseInventory:
    """Resolve inline cases or one restricted module-local named literal inventory."""
    values = decorator.args[1] if len(decorator.args) > 1 else None
    if isinstance(values, (ast.List, ast.Tuple)):
        return ParameterCaseInventory(tuple(values.elts), (), False)
    if not isinstance(values, ast.Name):
        return ParameterCaseInventory(
            None,
            (
                (
                    "TE.PARAMETER_ID",
                    "parameterization requires a literal case list and explicit IDs",
                ),
            ),
            False,
        )
    name = values.id
    if name in imported_module_names(tree):
        return ParameterCaseInventory(
            None,
            (
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} must not be imported",
                ),
            ),
            True,
        )
    assignments = module_assignments(tree, name)
    if not assignments:
        return ParameterCaseInventory(
            None,
            (
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} is unresolved in this module",
                ),
            ),
            True,
        )
    if len(assignments) != 1:
        return ParameterCaseInventory(
            None,
            (
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} must have exactly one "
                    "module-level assignment",
                ),
            ),
            True,
        )
    assignment = assignments[0]
    targets = (
        assignment.targets
        if isinstance(assignment, ast.Assign)
        else [assignment.target]
    )
    if len(targets) != 1 or not isinstance(targets[0], ast.Name):
        return ParameterCaseInventory(
            None,
            (
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} requires one "
                    "simple-name assignment",
                ),
            ),
            True,
        )
    if assignment.lineno >= decorator.lineno:
        return ParameterCaseInventory(
            None,
            (
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} must be assigned before "
                    "its consuming decorator",
                ),
            ),
            True,
        )
    value = assignment.value
    if not isinstance(value, (ast.List, ast.Tuple)):
        return ParameterCaseInventory(
            None,
            (
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} must be assigned directly "
                    "to a literal tuple or list",
                ),
            ),
            True,
        )
    if any(isinstance(element, ast.Starred) for element in value.elts):
        return ParameterCaseInventory(
            None,
            (
                (
                    "TE.PARAMETER_INVENTORY",
                    f"named parameter inventory {name!r} must not contain "
                    "starred expansion",
                ),
            ),
            True,
        )
    findings = inventory_mutation_findings(tree, name, assignment)
    return ParameterCaseInventory(tuple(value.elts), tuple(findings), True)


def semantic_parameter_id_problem(value: str) -> str | None:
    """Return the existing semantic-ID finding text for one static string."""
    unstable = (
        not SEMANTIC_PARAM_RE.fullmatch(value)
        or bool(re.fullmatch(r"(?:case[_-]?)?[0-9]+", value, re.IGNORECASE))
        or "::" in value
        or "/" in value
        or "\\" in value
        or bool(re.search(r"0x[0-9a-f]+", value, re.IGNORECASE))
        or any(0xD800 <= ord(char) <= 0xDFFF or char.isspace() for char in value)
    )
    if unstable:
        return f"pathological, ordinal, raw, or nonsemantic parameter ID {value!r}"
    return None


def decorator_parameter_findings(
    node: ast.FunctionDef | ast.AsyncFunctionDef, tree: ast.Module
) -> list[tuple[str, str]]:
    """Validate inline and named parameter case IDs without executing test code."""
    findings: list[tuple[str, str]] = []
    for dec in node.decorator_list:
        call = dec if isinstance(dec, ast.Call) else None
        if call is None or not (
            isinstance(call.func, ast.Attribute) and call.func.attr == "parametrize"
        ):
            continue
        ids = next((kw.value for kw in call.keywords if kw.arg == "ids"), None)
        resolution = resolve_parameter_case_inventory(tree, call)
        findings.extend(resolution.findings)
        if resolution.elements is None:
            continue
        explicit: list[str] = []
        if isinstance(ids, (ast.List, ast.Tuple)) and not resolution.named:
            explicit = [
                item.value
                for item in ids.elts
                if isinstance(item, ast.Constant) and isinstance(item.value, str)
            ]
            if len(explicit) != len(ids.elts):
                findings.append(
                    ("TE.PARAMETER_ID", "parameter IDs must be literal strings")
                )
        elif ids is None:
            for item in resolution.elements:
                valid_call = (
                    isinstance(item, ast.Call)
                    and isinstance(item.func, ast.Attribute)
                    and item.func.attr == "param"
                    and (
                        not resolution.named
                        or (
                            isinstance(item.func.value, ast.Name)
                            and item.func.value.id == "pytest"
                        )
                    )
                )
                if not valid_call:
                    message = (
                        "named parameter inventory elements must be direct "
                        "pytest.param(...) calls"
                        if resolution.named
                        else "parameterization requires explicit ids=... or "
                        "pytest.param(id=...)"
                    )
                    findings.append(
                        (
                            "TE.PARAMETER_INVENTORY"
                            if resolution.named
                            else "TE.PARAMETER_ID",
                            message,
                        )
                    )
                    continue
                assert isinstance(item, ast.Call)
                id_keywords = [kw.value for kw in item.keywords if kw.arg == "id"]
                if len(id_keywords) != 1:
                    findings.append(
                        (
                            "TE.PARAMETER_ID",
                            "every pytest.param case requires exactly one id=...",
                        )
                    )
                elif not (
                    isinstance(id_keywords[0], ast.Constant)
                    and isinstance(id_keywords[0].value, str)
                ):
                    findings.append(
                        (
                            "TE.PARAMETER_ID",
                            "every pytest.param id=... must be a static string literal",
                        )
                    )
                else:
                    explicit.append(id_keywords[0].value)
        elif resolution.named:
            findings.append(
                (
                    "TE.PARAMETER_INVENTORY",
                    "named parameter inventories own their explicit pytest.param "
                    "IDs and cannot use decorator ids=",
                )
            )
        else:
            findings.append(
                (
                    "TE.PARAMETER_ID",
                    "parameterization requires a literal case list and explicit IDs",
                )
            )
        if resolution.named and len(explicit) != len(set(explicit)):
            findings.append(
                ("TE.PARAMETER_ID", "named parameter inventory IDs must be unique")
            )
        for value in explicit:
            problem = semantic_parameter_id_problem(value)
            if problem is not None:
                findings.append(("TE.PARAMETER_ID", problem))
    return findings


def validate_file(
    path: Path, owner: dict[str, Any], seen_ids: dict[str, str]
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (OSError, UnicodeError, SyntaxError) as exc:
        return [finding("TE.PARSE", path, str(exc))]
    module_doc = ast.get_docstring(tree, clean=False)
    first_line = (module_doc or "").splitlines()[0].strip() if module_doc else ""
    mode, sut = owner.get("mode"), owner.get("sut")
    evidence_class = owner.get("evidence_class")
    opening_label = (
        EVIDENCE_OPENINGS.get(evidence_class)
        if isinstance(evidence_class, str)
        else None
    )
    artifact = owner.get("artifact")
    if opening_label is None:
        out.append(
            finding(
                "TE.EVIDENCE_CLASS",
                path,
                "evidence_class must be software_verification, "
                "numerical_verification, scientific_validation, or "
                "uncertainty_quantification",
            )
        )
        expected_opening = None
    elif mode == "class_owned" and isinstance(sut, str) and sut:
        expected_opening = f"{opening_label} of ``{sut}``."
    elif mode == "artifact_owned" and isinstance(artifact, str) and artifact.strip():
        expected_opening = f"{opening_label} of {artifact}."
    else:
        expected_opening = None
    if (
        not source.startswith('r"""')
        or expected_opening is None
        or first_line != expected_opening
    ):
        out.append(
            finding(
                "TE.MODULE_OPENING",
                path,
                "raw module opening must exactly match structured ownership; "
                f"expected {expected_opening!r}",
            )
        )
    ok, detail = sections(module_doc, HEADINGS)
    if not ok:
        out.append(finding("TE.MODULE_DOC", path, detail))
    for heading in SUPERSEDED_HEADINGS:
        if module_doc and re.search(rf"(?m)^\s*{re.escape(heading)}\s*$", module_doc):
            out.append(
                finding(
                    "TE.SUPERSEDED_HEADING",
                    path,
                    f"superseded heading is prohibited: {heading}",
                )
            )
    if mode not in {"class_owned", "artifact_owned"}:
        out.append(
            finding("TE.OWNERSHIP", path, "mode must be class_owned or artifact_owned")
        )
    if mode == "class_owned":
        expected = re.compile(
            rf"^test__{re.escape(str(sut))}(?:__[a-z][a-z0-9_]*)?\.py$"
        )
        if not isinstance(sut, str) or not sut or not expected.fullmatch(path.name):
            out.append(
                finding(
                    "TE.SUT_FILENAME",
                    path,
                    "class-owned filename must agree with the supplied SUT",
                )
            )
        assignment = next(
            (
                n
                for n in tree.body
                if isinstance(n, (ast.Assign, ast.AnnAssign))
                and any(
                    isinstance(t, ast.Name) and t.id == "SUT"
                    for t in (n.targets if isinstance(n, ast.Assign) else [n.target])
                )
            ),
            None,
        )
        value = assignment.value if assignment else None
        if not isinstance(value, ast.Name) or value.id != sut:
            out.append(
                finding(
                    "TE.SUT_ASSIGNMENT",
                    path,
                    "SUT assignment must name the supplied public class",
                )
            )
        imported = {
            alias.asname or alias.name
            for node in tree.body
            if isinstance(node, ast.ImportFrom)
            for alias in node.names
        }
        if sut not in imported:
            out.append(
                finding(
                    "TE.SUT_IMPORT",
                    path,
                    "supplied SUT must be imported through an explicit public import",
                )
            )
    elif mode == "artifact_owned":
        if not isinstance(artifact, str) or not artifact.strip():
            out.append(
                finding(
                    "TE.ARTIFACT_OWNER",
                    path,
                    "artifact_owned input must name one concrete artifact",
                )
            )
        if not re.fullmatch(r"test__[a-z][a-z0-9_]*\.py", path.name):
            out.append(
                finding(
                    "TE.ARTIFACT_FILENAME",
                    path,
                    "artifact-owned filename must be descriptive lowercase snake case",
                )
            )
    for node in (
        n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    ):
        is_test = node.name.startswith("test_")
        if is_test and not NAME_RE.fullmatch(node.name):
            out.append(
                finding(
                    "TE.TEST_NAME",
                    path,
                    "test name violates semantic surface/facet/behavior grammar",
                    node.lineno,
                )
            )
        if not is_test and node.name.startswith("_"):
            out.append(
                finding(
                    "TE.HELPER_PRIVATE",
                    path,
                    "evidence helper must have a nonprivate semantic name",
                    node.lineno,
                )
            )
        if not is_test and (
            node.name in {"helper", "setup", "check"}
            or re.search(r"_[0-9]+$", node.name)
        ):
            out.append(
                finding(
                    "TE.HELPER_NAME", path, "helper name is not semantic", node.lineno
                )
            )
        if any(
            isinstance(child, (ast.For, ast.AsyncFor, ast.While))
            for child in ast.walk(node)
        ):
            out.append(
                finding(
                    "TE.HIDDEN_LOOP",
                    path,
                    "test/helper contains a loop that hides collected case identity",
                    node.lineno,
                )
            )
        for code, param_detail in decorator_parameter_findings(node, tree):
            out.append(finding(code, path, param_detail, node.lineno))
        ok, detail = sections(ast.get_docstring(node, clean=False), FIELDS)
        if not ok:
            out.append(finding("TE.FUNCTION_DOC", path, detail, node.lineno))
            continue
        doc = ast.get_docstring(node, clean=False) or ""
        ids = ID_RE.findall(doc.split("Requirement", 1)[0])
        if is_test:
            if len(ids) != 1:
                out.append(
                    finding(
                        "TE.EVIDENCE_ID",
                        path,
                        "test must declare exactly one evidence ID",
                        node.lineno,
                    )
                )
            for eid in ids:
                if eid in seen_ids:
                    out.append(
                        finding(
                            "TE.DUPLICATE_ID",
                            path,
                            f"{eid} already occurs at {seen_ids[eid]}",
                            node.lineno,
                        )
                    )
                else:
                    seen_ids[eid] = f"{path.as_posix()}:{node.lineno}"
        elif "owns no identifier" not in doc.split("Requirement", 1)[0].lower():
            out.append(
                finding(
                    "TE.HELPER_ID",
                    path,
                    "helper must say it owns no identifier; referenced supported "
                    "IDs are not owned",
                    node.lineno,
                )
            )
    return out


def static_parameter_case_count(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    tree: ast.Module,
) -> int | None:
    """Return the static collected case product, or None when not derivable."""
    counts: list[int] = []
    for dec in node.decorator_list:
        if not (
            isinstance(dec, ast.Call)
            and isinstance(dec.func, ast.Attribute)
            and dec.func.attr == "parametrize"
        ):
            continue
        resolution = resolve_parameter_case_inventory(tree, dec)
        if resolution.elements is None or resolution.findings:
            return None
        counts.append(len(resolution.elements))
    if not counts:
        return 0
    result = 1
    for count in counts:
        result *= count
    return result


def load_ownership(
    path: Path, supplied: list[str]
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], list[dict[str, Any]]]:
    """Load closed structured ownership without raising on malformed input."""
    out: list[dict[str, Any]] = []
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [], {}, [finding("TE.OWNERSHIP_INPUT", path, str(exc))]
    if (
        not isinstance(value, dict)
        or set(value) != {"modules", "schema_version"}
        or value.get("schema_version") != 1
        or not isinstance(value.get("modules"), list)
    ):
        return (
            [],
            {},
            [
                finding(
                    "TE.OWNERSHIP_INPUT",
                    path,
                    "ownership must be a closed schema-version-1 object with "
                    "modules list",
                )
            ],
        )
    seen_paths: set[str] = set()
    by_path: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(value["modules"]):
        entry_issue_start = len(out)
        if not isinstance(item, dict):
            out.append(
                finding(
                    "TE.OWNERSHIP_ENTRY", path, f"modules[{index}] must be an object"
                )
            )
            continue
        allowed = {"path", "mode", "evidence_class", "sut", "artifact"}
        if not set(item) <= allowed:
            out.append(
                finding(
                    "TE.OWNERSHIP_KEYS", path, f"modules[{index}] has unexpected keys"
                )
            )
        raw_path = item.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            out.append(
                finding(
                    "TE.OWNERSHIP_PATH",
                    path,
                    f"modules[{index}].path must be a nonempty string",
                )
            )
            continue
        if raw_path in seen_paths:
            out.append(
                finding(
                    "TE.DUPLICATE_OWNERSHIP_PATH",
                    path,
                    f"duplicate ownership path {raw_path!r}",
                )
            )
            continue
        seen_paths.add(raw_path)
        mode = item.get("mode")
        if mode not in {"class_owned", "artifact_owned"}:
            out.append(
                finding("TE.OWNERSHIP_MODE", path, f"modules[{index}].mode is invalid")
            )
        if item.get("evidence_class") not in EVIDENCE_OPENINGS:
            out.append(
                finding(
                    "TE.EVIDENCE_CLASS",
                    path,
                    f"modules[{index}].evidence_class is invalid",
                )
            )
        if mode == "class_owned":
            if (
                set(item) != {"path", "mode", "evidence_class", "sut"}
                or not isinstance(item.get("sut"), str)
                or not item["sut"]
            ):
                out.append(
                    finding(
                        "TE.OWNERSHIP_SUT",
                        path,
                        f"modules[{index}] requires only a nonempty string sut",
                    )
                )
        elif mode == "artifact_owned" and (
            set(item) != {"path", "mode", "evidence_class", "artifact"}
            or not isinstance(item.get("artifact"), str)
            or not item["artifact"].strip()
        ):
            out.append(
                finding(
                    "TE.OWNERSHIP_ARTIFACT",
                    path,
                    f"modules[{index}] requires only a concrete nonempty artifact",
                )
            )
        if len(out) == entry_issue_start:
            by_path[raw_path] = item
    if set(by_path) != set(supplied):
        out.append(
            finding(
                "TE.OWNERSHIP_COVERAGE",
                path,
                "ownership paths must exactly equal explicitly supplied paths",
            )
        )
    return value["modules"], by_path, out


def validate_migration(path: Path) -> list[dict[str, Any]]:
    """Validate a closed, complete one-to-one old/new node inventory and map."""
    out: list[dict[str, Any]] = []
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [finding("TE.MIGRATION_INPUT", path, str(exc))]
    required = {
        "schema_version",
        "expected_old_node_ids",
        "expected_new_node_ids",
        "mappings",
    }
    if (
        not isinstance(value, dict)
        or set(value) != required
        or value.get("schema_version") != 1
    ):
        return [
            finding(
                "TE.MIGRATION_INPUT",
                path,
                "migration input must have the exact schema-version-1 keys",
            )
        ]
    old_expected, new_expected, mappings = (
        value.get("expected_old_node_ids"),
        value.get("expected_new_node_ids"),
        value.get("mappings"),
    )
    for label, inventory in (("old", old_expected), ("new", new_expected)):
        if (
            not isinstance(inventory, list)
            or any(not isinstance(item, str) or not item for item in inventory)
            or len(inventory) != len(set(inventory))
        ):
            out.append(
                finding(
                    "TE.MIGRATION_INVENTORY",
                    path,
                    f"expected {label} inventory must contain unique nonempty strings",
                )
            )
    if not isinstance(mappings, list):
        out.append(finding("TE.MIGRATION_INPUT", path, "mappings must be a list"))
        return out
    pairs: list[tuple[str, str]] = []
    for index, item in enumerate(mappings):
        if (
            not isinstance(item, dict)
            or set(item) != {"old_node_id", "new_node_id"}
            or not isinstance(item.get("old_node_id"), str)
            or not item.get("old_node_id")
            or not isinstance(item.get("new_node_id"), str)
            or not item.get("new_node_id")
        ):
            out.append(
                finding(
                    "TE.MIGRATION_ENTRY",
                    path,
                    f"mappings[{index}] must be one exact nonempty old/new pair",
                )
            )
            continue
        pairs.append((item["old_node_id"], item["new_node_id"]))
    old_actual = [item[0] for item in pairs]
    new_actual = [item[1] for item in pairs]
    if len(old_actual) != len(set(old_actual)) or len(new_actual) != len(
        set(new_actual)
    ):
        out.append(
            finding(
                "TE.MIGRATION_ONE_TO_ONE", path, "mapping sides must both be unique"
            )
        )
    if (
        isinstance(old_expected, list)
        and isinstance(new_expected, list)
        and (
            set(old_actual) != set(old_expected)
            or set(new_actual) != set(new_expected)
            or len(pairs) != len(old_expected)
            or len(pairs) != len(new_expected)
        )
    ):
        out.append(
            finding(
                "TE.MIGRATION_INCOMPLETE",
                path,
                "mapping must exactly cover both expected node inventories",
            )
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="explicit test module paths; directories are rejected",
    )
    parser.add_argument(
        "--ownership",
        required=True,
        type=Path,
        help="JSON with modules[{path,mode,evidence_class,sut?|artifact?}]",
    )
    parser.add_argument(
        "--migration-map",
        type=Path,
        help="JSON with mappings[{old_node_id,new_node_id}]",
    )
    args = parser.parse_args()
    findings: list[dict[str, Any]] = []
    supplied = [p.as_posix() for p in args.paths]
    if len(supplied) != len(set(supplied)):
        findings.append(
            finding(
                "TE.DUPLICATE_PATH", args.ownership, "supplied paths must be unique"
            )
        )
    entries, by_path, ownership_findings = load_ownership(args.ownership, supplied)
    findings.extend(ownership_findings)
    seen: dict[str, str] = {}
    for path in args.paths:
        if not path.is_file() or path.is_symlink():
            findings.append(
                finding(
                    "TE.EXPLICIT_PATH", path, "supplied path must be a regular file"
                )
            )
            continue
        owner = by_path.get(path.as_posix())
        if owner is not None:
            findings.extend(validate_file(path, owner, seen))
    if args.migration_map:
        findings.extend(validate_migration(args.migration_map))
    tests = helpers = parameterized = 0
    static_parameter_cases = 0
    static_parameter_cases_known = True
    for path in args.paths:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except OSError, UnicodeError, SyntaxError:
            continue
        functions = [
            node
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        tests += sum(node.name.startswith("test_") for node in functions)
        helpers += sum(not node.name.startswith("test_") for node in functions)
        for node in functions:
            count = static_parameter_case_count(node, tree)
            if count is None:
                static_parameter_cases_known = False
            elif count:
                parameterized += 1
                static_parameter_cases += count
    findings_by_code: dict[str, int] = {}
    for item in findings:
        findings_by_code[item["code"]] = findings_by_code.get(item["code"], 0) + 1
    ownership_counts = {
        kind: sum(
            item.get("mode") == kind for item in entries if isinstance(item, dict)
        )
        for kind in ("class_owned", "artifact_owned")
    }
    evidence_class_counts = {
        kind: sum(
            item.get("evidence_class") == kind
            for item in entries
            if isinstance(item, dict)
        )
        for kind in EVIDENCE_OPENINGS
    }
    result = {
        "claim_boundary": [
            "oracle independence",
            "mathematical correctness",
            "property/surface correctness",
            "test cohesion",
            "tolerance adequacy",
            "scientific validity",
            "uncertainty quantification",
            "human acceptance",
        ],
        "counts": {
            "artifact_owned_modules": ownership_counts["artifact_owned"],
            "class_owned_modules": ownership_counts["class_owned"],
            "evidence_class_modules": evidence_class_counts,
            "findings_by_code": dict(sorted(findings_by_code.items())),
            "helper_functions": helpers,
            "modules": len(args.paths),
            "parameterized_functions": parameterized,
            "static_collected_parameter_cases": static_parameter_cases
            if static_parameter_cases_known
            else None,
            "test_functions": tests,
            "unique_evidence_owners": len(seen),
        },
        "findings": findings,
        "paths": supplied,
        "schema_version": 1,
        "status": "PASS" if not findings else "FAIL",
    }
    print(json.dumps(result, ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
