#!/usr/bin/env python3
"""Split regression thresholds from numerical-verification evidence."""

from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = (
    ROOT
    / "python/tests/numerical_verification/ksdft2effmass/operators/test__OperatorRecordResidualAnalyzer__floating_point.py"
)
TARGET = (
    ROOT
    / "python/tests/software_verification/ksdft2effmass/operators/test__OperatorRecordResidualAnalyzer__floating_point_regressions.py"
)
MAP = (
    ROOT
    / ".pi/evidence/test-evidence-repository-conformance/consolidated-correction-node-map.json"
)
ID_MAP = (
    ROOT
    / ".pi/evidence/test-evidence-repository-conformance/consolidated-correction-evidence-id-map.json"
)

MODULE_DOC = r"""Software verification of ``OperatorRecordResidualAnalyzer``.

Facet and represented meaning
-----------------------------
This class-owned module owns finite binary64 regression behavior at normal and
subnormal scales. Historical ``NV-ORA-007`` through ``NV-ORA-016`` identifiers remain recorded as
predecessors. Their software-verification successors are ``SV-ORA-007`` through
``SV-ORA-016`` because the threshold-only claims cannot retain a numerical-verification
classification.

Intrinsic and cross-object scope
--------------------------------
The SUT is ``OperatorRecordResidualAnalyzer``. Synthetic ``complex128`` represented
differences exercise scalar magnitude, Frobenius, and spectral paths in eV. Independent
expected values remain exact or hand-derived, but the 64-epsilon and eight-ULP rules are
bounded regression envelopes, not proven forward-error bounds for NumPy, LAPACK, or an
arbitrary SVD backend.

VVUQ and scientific exclusions
------------------------------
Passing establishes only that the listed supported environment and shapes remain inside
the unchanged regression envelopes without leaked RuntimeWarning and preserve the
public metric ordering. It does not claim numerical verification for those approximate
thresholds, prove backend-independent error bounds, establish physical correctness,
scientific validation, UQ, portability, or cross-language agreement.
"""

NUMERICAL_SOURCE = r'''r"""Numerical verification of ``OperatorRecordResidualAnalyzer``.

Facet and represented meaning
-----------------------------
This class-owned module owns the exact-zero floating-point facet for a represented
``1 x 1`` complex128 difference. The mathematical maximum-entry, Frobenius, and
spectral norms of the zero matrix are all exactly zero in eV.

Intrinsic and cross-object scope
--------------------------------
The SUT is ``OperatorRecordResidualAnalyzer``. A public compatible difference supplies
an exact zero matrix, and exact arithmetic supplies the independent oracle. RuntimeWarning
is promoted to error; no approximate tolerance or backend-dependent regression envelope
is accepted.

VVUQ and scientific exclusions
------------------------------
Passing establishes exact agreement with the stated zero-matrix mathematics and public
metric ordering for this shape and dtype. It does not establish nonzero floating-point
error bounds, arbitrary-matrix numerical behavior, physical correctness, scientific
validation, UQ, portability, or cross-language agreement.
"""

import warnings

import numpy as np
import numpy.typing as npt
import pytest

from ksdft2effmass.operators import (
    OperatorRecordComparisonResult,
    OperatorRecordCompatibilityResult,
    OperatorRecordDifferenceResult,
    OperatorRecordResidualAnalyzer,
)

pytestmark = pytest.mark.numerical_verification

SUT = OperatorRecordResidualAnalyzer


def make_zero_difference(
    matrix: npt.NDArray[np.complex128],
) -> OperatorRecordDifferenceResult:
    r"""Evidence ID
    Owns no identifier; supports ``NV-ORA-017``.
    Requirement
    Exact-zero analysis requires a compatible represented difference containing the
    supplied complex128 matrix in eV.
    Method
    Construct the public compatibility and difference ResultObjects directly; this
    helper performs no residual calculation and owns no assertion result.
    Oracle
    Literal identifiers, the empty compatibility issue tuple, the supplied matrix, and
    the eV unit determine the fixture independently of residual analysis.
    Acceptance
    The helper returns the public difference object with those exact constructor values.
    Interpretation
    A helper defect can invalidate setup but cannot independently pass the evidence.
    Limitations
    This synthetic fixture establishes no norm, physical, validation, UQ, portability,
    or cross-language claim.
    """
    return OperatorRecordDifferenceResult(
        OperatorRecordCompatibilityResult("reference", "candidate", ()), matrix, "eV"
    )


def execute_zero_without_runtime_warning(
    matrix: npt.NDArray[np.complex128],
) -> OperatorRecordComparisonResult:
    r"""Evidence ID
    Owns no identifier; supports ``NV-ORA-017``.
    Requirement
    Exact-zero residual execution must not leak a NumPy RuntimeWarning.
    Method
    Promote RuntimeWarning to error and invoke the public analyzer on the supplied
    compatible difference.
    Oracle
    Python warning-filter semantics independently require any emitted RuntimeWarning to
    fail the owning test.
    Acceptance
    Public execution returns normally and yields an OperatorRecordComparisonResult.
    Interpretation
    Failure identifies warning leakage, analyzer failure, or fixture error.
    Limitations
    The helper does not validate NumPy or establish behavior for nonzero matrices.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        return OperatorRecordResidualAnalyzer().execute(make_zero_difference(matrix))


def test_method__execute__exact_scalar_zero_path() -> None:
    r"""Evidence ID
    NV-ORA-017
    Requirement
    The maximum-entry, Frobenius, and spectral norms of an exact ``1 x 1`` zero
    complex128 represented difference are exactly zero eV.
    Method
    Execute the public analyzer on ``array([[0+0j]], dtype=complex128)`` while treating
    RuntimeWarning as an error, then inspect all three public metrics.
    Oracle
    By the definitions of maximum absolute entry, Frobenius norm, and induced spectral
    norm, every norm of the zero matrix is exactly zero without numerical approximation.
    Acceptance
    All three metrics equal ``0.0`` exactly and satisfy
    ``0 <= maximum <= spectral <= Frobenius``; no tolerance is used.
    Interpretation
    A pass verifies the exact zero-scale branch for this representation; failure
    identifies analyzer, warning-policy, fixture, or accepted-mathematics drift.
    Limitations
    This case establishes no nonzero forward-error bound, arbitrary-shape behavior,
    physical correctness, scientific validation, UQ, portability, or cross-language
    agreement.
    """
    matrix: npt.NDArray[np.complex128] = np.array([[0.0 + 0.0j]], dtype=np.complex128)

    result = execute_zero_without_runtime_warning(matrix)

    assert result.maximum_absolute_residual == 0.0
    assert result.spectral_residual == 0.0
    assert result.frobenius_residual == 0.0
    assert (
        0.0
        <= result.maximum_absolute_residual
        <= result.spectral_residual
        <= result.frobenius_residual
    )
'''


def source_offset(lines: list[str], line: int, column: int) -> int:
    """Return the source offset for an AST coordinate."""
    return sum(len(item) for item in lines[: line - 1]) + column


def main() -> None:
    """Create the software-regression owner and retain exact-zero numerical evidence."""
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    module_expr = tree.body[0]
    assert isinstance(module_expr, ast.Expr) and isinstance(
        module_expr.value, ast.Constant
    )
    zero = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "test_method__execute__exact_scalar_zero_path"
    )
    replacements = [
        (
            source_offset(
                lines, module_expr.value.lineno, module_expr.value.col_offset
            ),
            source_offset(
                lines, module_expr.value.end_lineno, module_expr.value.end_col_offset
            ),
            'r"""' + MODULE_DOC + '"""',
        ),
        (
            source_offset(lines, zero.lineno, zero.col_offset),
            source_offset(lines, zero.end_lineno, zero.end_col_offset),
            "",
        ),
    ]
    software = source
    for start, end, replacement in sorted(replacements, reverse=True):
        software = software[:start] + replacement + software[end:]
    software = software.replace(
        "pytestmark = pytest.mark.numerical_verification",
        "pytestmark = pytest.mark.software_verification",
    )
    for value in range(7, 17):
        software = software.replace(f"NV-ORA-{value:03d}", f"SV-ORA-{value:03d}")
    TARGET.write_text(software.rstrip() + "\n", encoding="utf-8")
    SOURCE.write_text(NUMERICAL_SOURCE, encoding="utf-8")

    old_prefix = SOURCE.relative_to(ROOT).as_posix()
    new_prefix = TARGET.relative_to(ROOT).as_posix()
    old_nodes: list[str] = []
    new_nodes: list[str] = []
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef) or not node.name.startswith("test_"):
            continue
        if node.name == "test_method__execute__exact_scalar_zero_path":
            continue
        marks = next(
            (
                decorator
                for decorator in node.decorator_list
                if isinstance(decorator, ast.Call)
                and isinstance(decorator.func, ast.Attribute)
                and decorator.func.attr == "parametrize"
            ),
            None,
        )
        case_ids: list[str | None] = [None]
        if (
            marks is not None
            and len(marks.args) >= 2
            and isinstance(marks.args[1], ast.Name)
        ):
            inventory = next(
                item
                for item in tree.body
                if isinstance(item, ast.Assign)
                and any(
                    isinstance(target, ast.Name) and target.id == marks.args[1].id
                    for target in item.targets
                )
            )
            assert isinstance(inventory.value, (ast.Tuple, ast.List))
            case_ids = [
                next(
                    keyword.value.value
                    for keyword in element.keywords
                    if keyword.arg == "id" and isinstance(keyword.value, ast.Constant)
                )
                for element in inventory.value.elts
                if isinstance(element, ast.Call)
            ]
        for case_id in case_ids:
            suffix = node.name if case_id is None else f"{node.name}[{case_id}]"
            old_nodes.append(f"{old_prefix}::{suffix}")
            new_nodes.append(f"{new_prefix}::{suffix}")
    exact_zero_node = (
        f"{old_prefix}::test_method__execute__exact_scalar_zero_path"
    )
    old_nodes.append(exact_zero_node)
    new_nodes.append(exact_zero_node)
    payload = {
        "schema_version": 1,
        "expected_old_node_ids": old_nodes,
        "expected_new_node_ids": new_nodes,
        "mappings": [
            {"old_node_id": old, "new_node_id": new}
            for old, new in zip(old_nodes, new_nodes, strict=True)
        ],
    }
    MAP.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    id_map = {
        "schema_version": 1,
        "reason": "Threshold-only floating-point regression claims were corrected from numerical to software verification without inventing a backend-independent bound.",
        "retired_predecessor_evidence_ids": [
            f"NV-ORA-{value:03d}" for value in range(7, 17)
        ],
        "new_evidence_ids": [f"SV-ORA-{value:03d}" for value in range(7, 17)],
        "mappings": [
            {
                "old_evidence_id": f"NV-ORA-{value:03d}",
                "new_evidence_id": f"SV-ORA-{value:03d}",
            }
            for value in range(7, 17)
        ],
    }
    ID_MAP.write_text(json.dumps(id_map, indent=2) + "\n", encoding="utf-8")
    print(
        "moved 10 threshold-regression nodes to software verification; retained NV-ORA-017 as exact numerical verification"
    )


if __name__ == "__main__":
    main()
