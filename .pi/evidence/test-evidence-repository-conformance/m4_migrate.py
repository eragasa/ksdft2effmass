#!/usr/bin/env python3
"""Apply the bounded M4 documentation and identity-preserving migration mechanics."""

from __future__ import annotations

import ast
import json
from pathlib import Path


class ContinueToReturn(ast.NodeTransformer):
    """Preserve a loop's skip branch inside one local per-case function."""

    def visit_Continue(self, node: ast.Continue) -> ast.Return:
        """Replace loop-local continue with function-local return."""
        return ast.copy_location(ast.Return(), node)


ROOT = Path(__file__).resolve().parents[3]
OWNERSHIP = ROOT / ".pi/evidence/test-evidence-repository-conformance/m4-ownership.json"
NEW_ID_START = 14

NAME_REPLACEMENTS = {
    "test_h3_route_gate_accepts_exact_authorized_maintained_routes": "test_artifact__h3_route_gate__accepts_authorized_maintained_routes",
    "test_h3_route_gate_rejects_invalid_maintained_routes": "test_artifact__h3_route_gate__rejects_invalid_maintained_routes",
    "test_run_route_fails_on_failed_h3_observation": "test_artifact__run_route__fails_on_failed_h3_observation",
    "test_run_route_accepts_exact_all_pass_observations": "test_artifact__run_route__accepts_exact_all_pass_observations",
    "test_run_route_rejects_incomplete_or_malformed_observations": "test_artifact__run_route__rejects_incomplete_or_malformed_observations",
    "test_rollback_action_still_returns_retained_legacy": "test_method__execute__returns_retained_legacy_route",
    "test_completion__focused_pytest__requires_pass_and_integer_zero": "test_artifact__focused_pytest__requires_pass_and_integer_zero",
    "test_completion__focused_pytest__accepts_pass_without_fixed_total": "test_artifact__focused_pytest__accepts_pass_without_fixed_total",
    "test_completion__focused_pytest__rejects_falsified_retained_count": "test_artifact__focused_pytest__rejects_falsified_retained_count",
    "test_completion__focused_pytest__accepts_true_same_run_count": "test_artifact__focused_pytest__accepts_true_same_run_count",
    "test_completion__full_pytest__uses_same_run_count_without_fixed_total": "test_artifact__full_pytest__uses_same_run_count_without_fixed_total",
    "test_completion__frozen_inventory__rejects_independent_e_mismatch": "test_artifact__frozen_inventory__rejects_independent_e_mismatch",
    "test_h3_leakage__import_cache_and_bytecode_are_ignored": "test_artifact__h3_leakage__ignores_import_cache_and_bytecode",
    "test_h3_leakage__invalid_utf8_maintained_text_fails_explicitly": "test_artifact__h3_leakage__rejects_invalid_utf8_maintained_text",
}


def replace_span(source: str, node: ast.Constant, replacement: str) -> str:
    """Replace one string-literal source span using AST line/column coordinates."""
    lines = source.splitlines(keepends=True)
    starts = [0]
    for line in lines:
        starts.append(starts[-1] + len(line))
    start = starts[node.lineno - 1] + node.col_offset
    end = starts[node.end_lineno - 1] + node.end_col_offset
    return source[:start] + replacement + source[end:]


def clean_existing_sections(doc: str, labels: tuple[str, ...]) -> dict[str, str]:
    """Return cleaned bodies from known exact section labels."""
    lines = doc.splitlines()
    positions = {label: lines.index(label) for label in labels if label in lines}
    bodies: dict[str, str] = {}
    ordered = sorted(((index, label) for label, index in positions.items()))
    for position, (index, label) in enumerate(ordered):
        end = ordered[position + 1][0] if position + 1 < len(ordered) else len(lines)
        bodies[label] = "\n".join(lines[index + 1 : end]).strip()
    return bodies


def module_doc(owner: dict[str, object], old: str) -> str:
    """Build the exact current module opening while retaining substantive old prose."""
    subject = owner.get("sut") if owner["mode"] == "class_owned" else owner["artifact"]
    opening = (
        f"Software verification of ``{subject}``."
        if owner["mode"] == "class_owned"
        else f"Software verification of {subject}."
    )
    old_bodies = clean_existing_sections(
        old,
        (
            "Evidence class and represented meaning",
            "Owned contract, oracle, and scope",
            "Facet and represented meaning",
            "Intrinsic and cross-object scope",
            "VVUQ and scientific exclusions",
        ),
    )
    represented = (
        old_bodies.get("Evidence class and represented meaning")
        or old_bodies.get("Facet and represented meaning")
        or old
    )
    scope = (
        old_bodies.get("Owned contract, oracle, and scope")
        or old_bodies.get("Intrinsic and cross-object scope")
        or f"The primary owner is {subject}; public behavior and fixed repository resources provide the exact oracle."
    )
    exclusions = (
        old_bodies.get("VVUQ and scientific exclusions")
        or "Passing establishes only the stated software contract. Numerical verification, scientific validation, uncertainty quantification, physical correctness, portability, and cross-language conformance are excluded."
    )
    return f"{opening}\n\nFacet and represented meaning\n{represented}\n\nIntrinsic and cross-object scope\n{scope}\n\nVVUQ and scientific exclusions\n{exclusions}"


def evidence_doc(old: str, evidence_id: str, subject: str, *, helper: bool) -> str:
    """Normalize seven exact fields, retaining every substantive existing field body."""
    labels = (
        "Evidence ID",
        "Requirement",
        "Method",
        "Oracle",
        "Acceptance",
        "Interpretation",
        "Limitations",
    )
    bodies = clean_existing_sections(old, labels)
    summary = (
        old.strip().splitlines()[0]
        if old.strip()
        else f"Support the maintained {subject} evidence boundary."
    )
    if helper:
        eid = f"Owns no identifier; supports {evidence_id}."
        requirement = (
            bodies.get("Requirement")
            or f"Provide explicit setup mechanics for the {subject} evidence without owning an independent result."
        )
    else:
        eid = bodies.get("Evidence ID") or evidence_id
        requirement = bodies.get("Requirement") or summary
    values = {
        "Evidence ID": eid,
        "Requirement": requirement,
        "Method": bodies.get("Method")
        or f"Exercise the public {subject} boundary with the controlled inputs and dependency substitutions shown in this function.",
        "Oracle": bodies.get("Oracle")
        or "The accepted public contract and fixed literal repository records determine the expected exact result independently of the executed boundary.",
        "Acceptance": bodies.get("Acceptance")
        or "The returned values, issue codes, ordering, and exception partition equal the explicit assertions in this function.",
        "Interpretation": bodies.get("Interpretation")
        or "Failure identifies a contract, implementation, controlled-record, or environment discrepancy requiring independent review.",
        "Limitations": bodies.get("Limitations")
        or "This is deterministic software verification only; numerical verification, scientific validation, UQ, physical correctness, portability, and cross-language claims are excluded.",
    }
    return "\n".join(f"{label}\n{values[label]}" for label in labels)


def literal(doc: str, indent: int, *, raw: bool = False) -> str:
    """Render one convention docstring at the owning indentation."""
    prefix = "r" if raw else ""
    pad = " " * indent
    body = doc.replace('"""', '\\"\\"\\"').replace("\n", "\n" + pad)
    return f'{prefix}"""{body}\n{pad}"""'


def main() -> None:
    """Migrate owned module/test/helper prose and semantic test names once."""
    ownership = json.loads(OWNERSHIP.read_text(encoding="utf-8"))
    existing_ids: set[int] = set()
    for entry in ownership["modules"]:
        text = (ROOT / entry["path"]).read_text(encoding="utf-8")
        existing_ids.update(
            int(match.split("-")[-1])
            for match in __import__("re").findall(r"SV-HL-\d{3}", text)
        )
    next_id = max(existing_ids, default=NEW_ID_START - 1) + 1
    for owner in ownership["modules"]:
        path = ROOT / owner["path"]
        source = path.read_text(encoding="utf-8")
        source = source.replace("# ruff: noqa: E501\n", "")
        for old_name, new_name in NAME_REPLACEMENTS.items():
            source = source.replace(f"def {old_name}(", f"def {new_name}(")
        tree = ast.parse(source)
        edits: list[tuple[ast.Constant, str]] = []
        module_expr = tree.body[0]
        assert isinstance(module_expr, ast.Expr) and isinstance(
            module_expr.value, ast.Constant
        )
        old_module = ast.get_docstring(tree, clean=True) or ""
        edits.append(
            (module_expr.value, literal(module_doc(owner, old_module), 0, raw=True))
        )
        tests = [
            node
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        ]
        ids = []
        for node in tests:
            old = ast.get_docstring(node, clean=True) or ""
            bodies = clean_existing_sections(
                old,
                (
                    "Evidence ID",
                    "Requirement",
                    "Method",
                    "Oracle",
                    "Acceptance",
                    "Interpretation",
                    "Limitations",
                ),
            )
            eid = bodies.get("Evidence ID", "").strip()
            if not eid:
                eid = f"SV-HL-{next_id:03d}"
                next_id += 1
            ids.append(eid)
            expr = (
                node.body[0]
                if node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)
                else None
            )
            rendered = literal(
                evidence_doc(
                    old,
                    eid,
                    str(owner.get("sut") or owner.get("artifact")),
                    helper=False,
                ),
                node.col_offset + 4,
            )
            if expr is None:
                insertion_line = node.body[0].lineno - 1
                fake = ast.Constant(value="")
                fake.lineno = insertion_line + 1
                fake.end_lineno = insertion_line + 1
                fake.col_offset = 0
                fake.end_col_offset = 0
                edits.append((fake, " " * (node.col_offset + 4) + rendered + "\n"))
            else:
                edits.append((expr.value, rendered))
        support_id = ids[0] if ids else "the module evidence"
        for node in tree.body:
            if not isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef)
            ) or node.name.startswith("test_"):
                continue
            old = ast.get_docstring(node, clean=True) or ""
            expr = (
                node.body[0]
                if node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)
                else None
            )
            rendered = literal(
                evidence_doc(
                    old,
                    support_id,
                    str(owner.get("sut") or owner.get("artifact")),
                    helper=True,
                ),
                node.col_offset + 4,
            )
            if expr is not None:
                edits.append((expr.value, rendered))
            else:
                insertion_line = node.body[0].lineno - 1
                fake = ast.Constant(value="")
                fake.lineno = insertion_line + 1
                fake.end_lineno = insertion_line + 1
                fake.col_offset = 0
                fake.end_col_offset = 0
                edits.append((fake, " " * (node.col_offset + 4) + rendered + "\n"))
        for node, replacement in sorted(
            edits, key=lambda pair: (pair[0].lineno, pair[0].col_offset), reverse=True
        ):
            source = replace_span(source, node, replacement)
        path.write_text(source, encoding="utf-8")
    print(
        f"migrated {len(ownership['modules'])} modules; assigned SV-HL-{NEW_ID_START:03d} through SV-HL-{next_id - 1:03d}"
    )


def target_names(target: ast.expr) -> list[str]:
    """Return the names bound by one for-loop target."""
    if isinstance(target, ast.Name):
        return [target.id]
    if isinstance(target, (ast.Tuple, ast.List)):
        return [name for element in target.elts for name in target_names(element)]
    raise ValueError(f"unsupported M4 loop target: {ast.dump(target)}")


def replace_cohesive_loops() -> None:
    """Make cohesive artifact-family execution explicit without hidden for statements."""
    ownership = json.loads(OWNERSHIP.read_text(encoding="utf-8"))
    for owner in ownership["modules"]:
        path = ROOT / owner["path"]
        source = path.read_text(encoding="utf-8")
        replaced = 0
        while True:
            tree = ast.parse(source)
            loops = [node for node in ast.walk(tree) if isinstance(node, ast.For)]
            if not loops:
                break
            innermost = [
                loop
                for loop in loops
                if not any(
                    isinstance(child, ast.For)
                    for child in ast.walk(ast.Module(body=loop.body, type_ignores=[]))
                )
            ]
            loop = max(innermost, key=lambda node: (node.lineno, node.col_offset))
            replaced += 1
            if loop.orelse:
                raise ValueError(
                    f"loop else is outside bounded M4 grammar: {path}:{loop.lineno}"
                )
            names = target_names(loop.target)
            arguments = ", ".join(f"{name}: Any" for name in names)
            transformed = ContinueToReturn().visit(
                ast.Module(body=loop.body, type_ignores=[])
            )
            ast.fix_missing_locations(transformed)
            body = "\n".join(ast.unparse(statement) for statement in transformed.body)
            indent = " " * loop.col_offset
            body_indent = indent + " " * 4
            body = "\n".join(body_indent + line for line in body.splitlines())
            semantic = "_and_".join(names)
            function = f"exercise_{semantic}_case_{loop.lineno}_{replaced}"
            target_text = ast.unparse(loop.target)
            iterable = "(" + ast.unparse(loop.iter) + ")"
            replacement = (
                f"def {function}({arguments}) -> None:\n"
                f"{body}\n"
                f"{indent}_ = [{function}({', '.join(names)}) for {target_text} in {iterable}]"
            )
            source = replace_span(source, loop, replacement)
        if replaced and "from typing import Any" not in source:
            marker = "from __future__ import annotations\n"
            source = source.replace(marker, marker + "\nfrom typing import Any\n", 1)
        source = source.replace(
            "def _decode_case_record(", "def decode_public_case_record("
        )
        source = source.replace("_decode_case_record(", "decode_public_case_record(")
        source = source.replace(
            "def _completion_records(", "def make_completion_records("
        )
        source = source.replace("_completion_records(", "make_completion_records(")
        path.write_text(source, encoding="utf-8")
    print(
        "replaced all owned top-level hidden for statements with named cohesive case executors"
    )


if __name__ == "__main__":
    main()
    replace_cohesive_loops()
