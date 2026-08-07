#!/usr/bin/env python3
"""Wrap M4 maintained evidence prose without changing executable statements."""

from __future__ import annotations

import ast
import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OWNERSHIP = ROOT / ".pi/evidence/test-evidence-repository-conformance/m4-ownership.json"
HEADINGS = {
    "Facet and represented meaning",
    "Intrinsic and cross-object scope",
    "VVUQ and scientific exclusions",
    "Evidence ID",
    "Requirement",
    "Method",
    "Oracle",
    "Acceptance",
    "Interpretation",
    "Limitations",
}


def offset(lines: list[str], line: int, column: int) -> int:
    """Return a character offset for one AST source coordinate."""
    return sum(len(value) for value in lines[: line - 1]) + column


def repair_generated_prose(doc: str, path: str) -> str:
    """Replace initial scaffold prose with contract-specific M4 evidence prose."""
    if "Exercise the public" not in doc:
        return doc
    if "h4_hc02_route" in path:
        values = {
            "Method": "Construct the named route or replay partition, substitute only the public route dependency, and invoke the maintained H3 gate or route consumer.",
            "Oracle": "The closed route schema, exact current-local check inventory, and retained-legacy observation shape fix the result independently of the consumer.",
            "Acceptance": "Status, command exit values, route identity, and issue text match exactly; no approximate or warning acceptance is used.",
            "Interpretation": "Failure identifies route-schema drift, consumer precedence drift, controlled-payload error, or stale current-resource evidence.",
        }
    elif "h4_replay_and_completion" in path:
        values = {
            "Method": "Load the retained replay or completion validator, alter only the named record field or disposable artifact, and execute its public validation boundary.",
            "Oracle": "Versioned H4 record structure, current maintained route resources, and exact hash or same-run count relations fix the expected outcome independently.",
            "Acceptance": "The named exact equality, diagnostic substring, status, count relation, or byte nonmutation must hold; no tolerance is used.",
            "Interpretation": "Failure identifies retained-validator drift, stale resource identity, incorrect controlled mutation, or a nonmutation boundary defect.",
        }
    elif "local_repository_validation" in path:
        values = {
            "Method": "Construct the named explicit repository selection, invoke ValidateLocalRepository, and compare its aggregate without ambient discovery.",
            "Oracle": "Public severity precedence and fixed ownership, checksum, skill, and evidence records determine the aggregate independently.",
            "Acceptance": "Result names, severity, issue codes, and missing-root exceptions match exactly.",
            "Interpretation": "Failure identifies composition drift, severity downgrade, ambient discovery, or a controlled-selection defect.",
        }
    else:
        values = {
            "Method": "Construct the named public input partition and invoke the declared owner without ambient discovery.",
            "Oracle": "The fixed public contract and literal record partition determine the exact expected result independently.",
            "Acceptance": "The named exact value, ordering, issue, or exception partition must hold without tolerance.",
            "Interpretation": "Failure identifies public-contract drift, stale controlled input, or an implementation defect.",
        }
    for label, value in values.items():
        next_labels = "|".join(
            re.escape(item)
            for item in ("Oracle", "Acceptance", "Interpretation", "Limitations")
            if item != label
        )
        doc = re.sub(
            rf"(?ms)^{re.escape(label)}\s*$.*?(?=^(?:{next_labels})\s*$)",
            f"{label}\n{value}\n",
            doc,
            count=1,
        )
    return doc


def render(doc: str, indent: int, raw: bool) -> str:
    """Render cleaned prose with headings and blank lines retained exactly."""
    width = 88 - indent
    output: list[str] = []
    for line in doc.splitlines():
        stripped = line.strip()
        if not stripped or stripped in HEADINGS:
            output.append(stripped)
            continue
        output.extend(
            textwrap.wrap(
                stripped,
                width=width,
                break_long_words=False,
                break_on_hyphens=False,
                subsequent_indent="",
            )
            or [""]
        )
    pad = " " * indent
    prefix = "r" if raw else ""
    body = "\n".join(output).replace("\n", "\n" + pad)
    return f'{prefix}"""{body}\n{pad}"""'


def main() -> None:
    """Wrap every owned module, top-level test, and top-level helper docstring."""
    ownership = json.loads(OWNERSHIP.read_text(encoding="utf-8"))
    for owner in ownership["modules"]:
        path = ROOT / owner["path"]
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        lines = source.splitlines(keepends=True)
        replacements: list[tuple[int, int, str]] = []
        owners: list[ast.Module | ast.FunctionDef | ast.AsyncFunctionDef] = [tree]
        owners.extend(
            node
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        )
        for node in owners:
            body = node.body
            if not body or not isinstance(body[0], ast.Expr):
                continue
            value = body[0].value
            if not isinstance(value, ast.Constant) or not isinstance(value.value, str):
                continue
            doc = ast.get_docstring(node, clean=True)
            if doc is None:
                continue
            doc = repair_generated_prose(doc, owner["path"])
            indent = 0 if isinstance(node, ast.Module) else node.col_offset + 4
            replacements.append(
                (
                    offset(lines, value.lineno, value.col_offset),
                    offset(lines, value.end_lineno, value.end_col_offset),
                    render(doc, indent, isinstance(node, ast.Module)),
                )
            )
        for start, end, replacement in sorted(replacements, reverse=True):
            source = source[:start] + replacement + source[end:]
        path.write_text(source, encoding="utf-8")
    print(f"wrapped maintained prose in {len(ownership['modules'])} M4 modules")


if __name__ == "__main__":
    main()
