#!/usr/bin/env python3
"""Replace the 105 independently identified generated M3 prose blocks."""

from __future__ import annotations

import ast
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GENERATED = re.compile(
    r"The public .* contract must|method and oracle|interpretation and limitations"
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


def offset(lines: list[str], line: int, column: int) -> int:
    """Return the source offset for an AST coordinate."""
    return sum(len(value) for value in lines[: line - 1]) + column


def owner(path: Path) -> str:
    """Return the maintained class or artifact owner encoded by a path."""
    match = re.search(r"test__([^/]+?)(?:__[^/]*)?\.py$", path.name)
    assert match is not None
    return match.group(1).replace("_", " ")


def behavior(name: str) -> str:
    """Render a stable semantic partition from a maintained function name."""
    value = name.removeprefix("test_")
    value = value.split("__", 1)[-1] if "__" in value else value
    return value.replace("__", ": ").replace("_", " ")


def requirement(path: Path, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """State the externally visible requirement owned by one affected function."""
    name = node.name
    artifact = owner(path)
    if not name.startswith("test_"):
        helper_requirements = {
            "fixture_names": "Fixture discovery returns the exact versioned JSON filenames for the requested valid or invalid family.",
            "load_json": "Schema evidence needs decoded JSON values from the named repository artifact without changing their bytes or meaning.",
            "compatible_result": "Difference-result fixtures require an explicitly compatible audit carrying the requested reference and candidate identifiers.",
            "make_result": "Value-semantics cases require a valid difference result while independently selecting its matrix, unit, and compatibility audit.",
            "comparison_result": "Comparison-result cases require a valid baseline whose public fields can be overridden one partition at a time.",
            "make_issue": "Compatibility-result cases require a public issue with the requested mismatch code and canonical record identifiers.",
            "make_record": "Differencer and comparator cases require independently valid synthetic records with controlled identifiers, matrices, and energy units.",
            "valid_payload": "Structural deserialization cases require one complete schema-version-1 payload before changing a single structural partition.",
            "mutated": "Value-deserialization cases require deterministic replacement of one declared JSON path while all other payload values remain valid.",
            "raw_number": "Overflow evidence requires inserting one raw JSON numeric token without accidental string coercion by the test fixture.",
            "difference": "Residual analysis accepts a compatible represented difference with the supplied complex128 matrix and explicit eV unit.",
            "execute_without_runtime_warning": "Residual execution for finite synthetic matrices must not leak a NumPy RuntimeWarning.",
            "assert_nonzero_normal_close": "A nonzero normal binary64 result is compared with a nonzero independently calculated reference under the declared local regression envelope.",
            "binary64_ulp_distance": "The ULP regression check compares nonnegative binary64 bit patterns by their monotone unsigned encoding.",
            "assert_subnormal_ulp_close": "A subnormal regression result must remain positive and within the declared inclusive ULP envelope of a positive subnormal reference.",
            "assert_ordering": "Stored residual metrics satisfy the public order zero <= maximum <= spectral <= Frobenius.",
            "assert_metric": "An analytical residual metric is either exactly zero or a nonzero normal binary64 value within its declared forward-error criterion.",
        }
        return helper_requirements.get(
            name,
            f"The {artifact} evidence fixture constructs the controlled public input used by its supported tests.",
        )
    phrase = behavior(name)
    if "DifferenceResult" in artifact:
        if "eq" in name:
            return "OperatorRecordDifferenceResult equality is exact over compatibility_result, matrix, and energy_unit, and rejects unrelated types."
        if "frozen" in name:
            return "Every public OperatorRecordDifferenceResult field is frozen after construction."
        if "owns source" in phrase:
            return "OperatorRecordDifferenceResult copies caller matrix data and exposes storage that cannot be made writeable."
        return f"OperatorRecordDifferenceResult enforces this represented-data partition: {phrase}."
    if "ComparisonResult" in artifact:
        if "eq" in name:
            return "OperatorRecordComparisonResult equality is exact over every declared public field and distinguishes each field independently."
        if "immutable" in name:
            return "Every declared OperatorRecordComparisonResult public field rejects post-construction assignment."
        return f"OperatorRecordComparisonResult enforces this structural-result partition: {phrase}."
    if "CompatibilityResult" in artifact:
        if "eq" in name:
            return "OperatorRecordCompatibilityResult equality is exact over both identifiers and the canonical issues tuple."
        if "immutable" in name:
            return "Every declared OperatorRecordCompatibilityResult public field rejects post-construction assignment."
        return f"OperatorRecordCompatibilityResult enforces this compatibility-audit partition: {phrase}."
    if "Differencer" in artifact:
        return f"OperatorRecordDifferencer publicly enforces the candidate-minus-reference operation partition: {phrase}."
    if "JsonSerializer" in artifact:
        return f"OperatorRecordJsonSerializer enforces this version-1 JSON boundary partition: {phrase}."
    if "json fixtures" in artifact.lower():
        return f"The version-1 golden fixture family has this exact runtime interoperability property: {phrase}."
    if "json schema" in artifact.lower():
        return f"The public version-1 JSON Schema has this exact structural property: {phrase}."
    if "ResidualAnalyzer" in artifact:
        return f"OperatorRecordResidualAnalyzer enforces this public residual-analysis partition: {phrase}."
    if "Comparator" in artifact:
        return f"OperatorRecordComparator has this explicit differencer-then-analyzer Workflow property: {phrase}."
    return f"The public {artifact} contract fixes this exact partition: {phrase}."


def method(path: Path, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Describe the public operation and controlled partition actually exercised."""
    name = node.name
    partition = behavior(name)
    if not name.startswith("test_"):
        return f"Construct or inspect only the named synthetic fixture operation ({partition}); the helper owns no assertion result and introduces no hidden oracle."
    if "json_schema" in path.name:
        return f"Load the public schema and named literal fixture partition ({partition}), then apply Draft 2020-12 validation without invoking serializer private helpers."
    if "json_fixtures" in path.name:
        return f"Enumerate the checked-in version-1 fixtures for {partition} and pass each case through the documented public serializer boundary."
    if "JsonSerializer" in path.name:
        return f"Invoke serialize() or deserialize() on the explicit schema-version-1 partition ({partition}); warnings and coercive fallback behavior are not accepted."
    if "Differencer" in path.name:
        return f"Construct independently valid reference and candidate records for {partition}, then invoke execute() and inspect only public results or errors."
    if "ResidualAnalyzer" in path.name:
        return f"Construct the declared complex128 represented difference for {partition}, invoke execute() with RuntimeWarning promoted to error where numerical operations occur, and inspect public outputs."
    if "Comparator" in path.name:
        return f"Construct the declared public dependencies and records for {partition}, execute the Workflow, and compare it with explicit differencer-then-analyzer composition."
    return f"Construct valid baseline instances, change only the named {partition} partition, and observe constructor, field, equality, hash, or public-API behavior as applicable."


def oracle(path: Path) -> str:
    """Name the independent oracle family for an affected maintained module."""
    name = path.name
    if "json_schema" in name:
        return "The checked-in Draft 2020-12 schema, its literal required-field vocabulary, and the classified valid/invalid fixture manifest define the expected structural result."
    if "json_fixtures" in name:
        return "The checked-in valid, schema-invalid, unknown-value, and wrong-semantic-type filename inventories define both membership and the layer expected to accept or reject each file."
    if "JsonSerializer" in name:
        return "The public version-1 schema, fixed wire-field vocabulary, literal JSON grammar, and DataObject constructor invariants determine the expected text, value, or exception independently of serializer private methods."
    if "Differencer" in name:
        return "Literal elementwise candidate-minus-reference arithmetic, exact metadata, compatibility rules, and the public structured-error taxonomy determine the result independently of the differencer implementation."
    if "ResidualAnalyzer" in name:
        return "Exact scalar identities, hand-derived matrix norms where stated, Python exception semantics, and the public structured-error taxonomy determine the expected result independently of analyzer private helpers."
    if "Comparator" in name:
        return "Explicit public composition of a separately constructed OperatorRecordDifferencer and OperatorRecordResidualAnalyzer fixes the expected Workflow result and propagated errors."
    if "DifferenceResult" in name:
        return "The literal constructor inputs, exact ndarray values, declared public-field inventory, frozen dataclass semantics, and Python equality/hash rules determine the expected result."
    if "ComparisonResult" in name or "CompatibilityResult" in name:
        return "Literal constructor values, the declared public-field inventory where completeness is claimed, frozen dataclass semantics, and Python equality/hash rules determine the result independently."
    return "The accepted public contract and literal expected values in the case define the result without using production private helpers."


def acceptance(path: Path, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """State the exact acceptance family encoded by the function body."""
    if not node.name.startswith("test_"):
        return "The helper returns exactly the requested fixture value or applies only the documented comparison; all pass/fail assertions remain in the owning test."
    calls = {
        call.func.id
        for call in ast.walk(node)
        if isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
    }
    raises = [
        ast.unparse(call.args[0])
        for call in ast.walk(node)
        if isinstance(call, ast.Call)
        and isinstance(call.func, ast.Attribute)
        and call.func.attr == "raises"
        and call.args
    ]
    if raises:
        return f"The named partition raises exactly {' or '.join(dict.fromkeys(raises))} with the asserted public message, code, or attached result; no alternate exception is accepted."
    if "assert_subnormal_ulp_close" in calls:
        return "Each expected and actual scalar is strictly positive, their unsigned binary64 encodings differ by at most eight ULPs inclusively, and zero cannot satisfy acceptance."
    if "assert_nonzero_normal_close" in calls:
        return "Each scalar is finite and nonzero and its absolute error is at most 64*epsilon*abs(expected), with a strictly positive bound smaller than the expected magnitude."
    if "json_schema" in path.name:
        return "Schema validity, exact fixture membership, and acceptance or rejection by Draft 2020-12 validation agree exactly with the declared fixture class."
    if "eq" in node.name:
        return "The equal baseline compares equal, every independently varied inventoried field compares unequal, and comparison with an unrelated object is false."
    if "frozen" in node.name or "immutable" in node.name:
        return "Assignment to every field named by FROZEN_FIELDS raises FrozenInstanceError; no declared public field is omitted."
    return "All literal values, arrays, field names, ordering relations, object identities, absences, and deterministic text asserted by the case match exactly; no approximate fallback is used."


def interpretation(path: Path) -> str:
    """Give bounded pass/failure meaning for the owned evidence family."""
    if "json_schema" in path.name or "json_fixtures" in path.name:
        return "A pass supports only the declared schema/fixture layer agreement; failure identifies schema drift, fixture misclassification, runtime-layer drift, or an evidence defect."
    if "ResidualAnalyzer" in path.name:
        return "A pass supports only the stated represented residual or error-boundary case; failure may identify analyzer, oracle, backend/environment, fixture, or accepted-contract drift."
    return "A pass supports only this named public-contract partition; failure identifies implementation drift, an incorrect controlled input, an oracle defect, or accepted-contract inconsistency."


def limitations(path: Path) -> str:
    """State exclusions without inflating the owned evidence class."""
    if "floating_point" in path.name:
        return "Approximate nonzero cases are bounded binary64 regression checks for the listed shapes and environment, not numerical-verification proofs for arbitrary matrices or backends; they establish no physical correctness, scientific validation, UQ, portability, or cross-language agreement."
    if "analytical_norms" in path.name:
        return "The synthetic matrices cover only the stated shapes, complex128 precision, eV units, and scales; they do not establish physical correctness, scientific validation, UQ, portability, or cross-language agreement."
    return "The synthetic software cases do not establish numerical verification, physical correctness, scientific validation, UQ, portability, exhaustive inputs, or cross-language agreement."


def evidence_id(doc: str) -> str:
    """Preserve the existing stable identifier declaration verbatim."""
    value = doc.split("Evidence ID", 1)[1].split("Requirement", 1)[0].strip()
    return " ".join(value.split())


def render(fields: dict[str, str], indent: int) -> str:
    """Render the seven exact fields with deterministic wrapping."""
    pad = " " * indent
    lines: list[str] = []
    for label in FIELDS:
        lines.append(label)
        lines.extend(
            textwrap.wrap(
                fields[label],
                width=88 - indent,
                break_long_words=False,
                break_on_hyphens=False,
            )
        )
    body = ("\n" + pad).join(lines)
    return f'r"""{body}\n{pad}"""'


def main() -> None:
    """Correct every generated block and fail unless the reviewed count is exact."""
    paths = sorted(
        path
        for path in (ROOT / "python/tests").rglob("test*.py")
        if GENERATED.search(path.read_text(encoding="utf-8"))
    )
    corrected = 0
    for path in paths:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        lines = source.splitlines(keepends=True)
        replacements: list[tuple[int, int, str]] = []
        for node in tree.body:
            if (
                not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                or not node.body
            ):
                continue
            expr = node.body[0]
            if (
                not isinstance(expr, ast.Expr)
                or not isinstance(expr.value, ast.Constant)
                or not isinstance(expr.value.value, str)
            ):
                continue
            doc = ast.get_docstring(node, clean=True) or ""
            if not GENERATED.search(doc):
                continue
            fields = {
                "Evidence ID": evidence_id(doc),
                "Requirement": requirement(path, node),
                "Method": method(path, node),
                "Oracle": oracle(path),
                "Acceptance": acceptance(path, node),
                "Interpretation": interpretation(path),
                "Limitations": limitations(path),
            }
            replacements.append(
                (
                    offset(lines, expr.value.lineno, expr.value.col_offset),
                    offset(lines, expr.value.end_lineno, expr.value.end_col_offset),
                    render(fields, node.col_offset + 4),
                )
            )
            corrected += 1
        for start, end, replacement in sorted(replacements, reverse=True):
            source = source[:start] + replacement + source[end:]
        path.write_text(source, encoding="utf-8")
    if corrected != 105 or len(paths) != 21:
        raise SystemExit(
            f"expected 105 generated blocks in 21 modules, found {corrected} in {len(paths)}"
        )
    print("corrected 105 generated evidence blocks across 21 maintained modules")


if __name__ == "__main__":
    main()
