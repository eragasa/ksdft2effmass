r"""Software verification of workflow cpn python snakes and deferred engine isolation.

Facet and represented meaning
--------------------------------------
Software verification of Workflow CPN Python isolation from SNAKES and deferred
engine/persistence scope, a static software boundary rather than engine behavior.

Intrinsic and cross-object scope
--------------------------------
The Workflow CPN Python SNAKES and deferred-engine isolation boundary is the primary
artifact owner. Absence of named deferred paths and direct SNAKES import roots is the
exact static oracle.

VVUQ and scientific exclusions
------------------------------
Passing confirms only the inspected direct isolation boundary; failure indicates
deferred-scope or evidence drift. Numerical verification, scientific validation,
uncertainty quantification, physical correctness, dynamic/transitive dependency absence,
engine correctness, and cross-language conformance are excluded."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[5]
pytestmark = pytest.mark.software_verification


def test_artifact__snakes_isolation__excludes_deferred_engine_scope() -> None:
    """Evidence ID
    SV-CPN-033

    Requirement
    The P1 Workflow CPN Python runtime has no named deferred engine/persistence path and
    no direct SNAKES import root.

    Method
    Check absence of ``engines`` and ``persistence.py``; parse all top-level Python
    modules and collect direct import roots; no warnings are expected.

    Oracle
    The accepted P1 scope excludes those paths and the ``snakes`` import root.

    Acceptance
    Both deferred paths are absent and no inspected direct import root equals
    ``snakes``.

    Interpretation
    Pass supports bounded P1 isolation; failure may indicate deferred-scope, dependency,
    or evidence drift.

    Limitations
    Dynamic and transitive dependencies are not detected, and no SNAKES implementation
    is validated. Scientific validation, UQ, and cross-language conformance are
    excluded."""
    source = REPO_ROOT / "python/src/ksdft2effmass/workflows/cpn"
    assert not (source / "engines").exists()
    assert not (source / "persistence.py").exists()
    trees = tuple(ast.parse(path.read_text()) for path in source.glob("*.py"))
    imported_roots = {
        alias.name.split(".")[0]
        for tree in trees
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    } | {
        node.module.split(".")[0]
        for tree in trees
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    }
    assert "snakes" not in imported_roots
