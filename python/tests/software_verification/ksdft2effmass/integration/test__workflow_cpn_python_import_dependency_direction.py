r"""Software verification of workflow cpn python import dependency direction.

Facet and represented meaning

--------------------------------------
Software verification of the Workflow CPN Python import-dependency direction, a static
source boundary rather than runtime or scientific behavior.

Intrinsic and cross-object scope

--------------------------------
The Workflow CPN Python import-dependency direction is the primary artifact owner. The
approved named predecessor-layer map is the exact static oracle for inspected relative
imports.

VVUQ and scientific exclusions

------------------------------
Passing confirms only the inspected import subset; failure indicates architecture or
evidence drift. Numerical verification, scientific validation, uncertainty
quantification, physical correctness, runtime behavior, absolute-import completeness,
and cross-language conformance are excluded."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[5]
pytestmark = pytest.mark.software_verification


def test_artifact__import_dependency_direction__follows_approved_layers() -> None:
    """Evidence ID: SV-CPN-032

    Requirement: Named Workflow CPN Python modules import only their approved
    predecessor layers
    through relative imports.

    Method: Parse each named production module with standard-library AST and collect
    level-one
    relative import modules; no warnings are expected.

    Oracle: The explicit per-module predecessor map is the approved architecture oracle.

    Acceptance: For every named module, the observed relative-import set is a subset of
    its approved
    predecessors.

    Interpretation: Pass supports the inspected dependency direction; failure may
    indicate architecture,
    source, or evidence-map drift.

    Limitations: New modules and absolute intra-package imports can evade this bounded
    oracle.
    Runtime behavior, scientific validation, UQ, and cross-language conformance are
    excluded."""
    source = REPO_ROOT / "python/src/ksdft2effmass/workflows/cpn"
    allowed = {
        "tokens": set(),
        "markings": {"tokens"},
        "expressions": {"markings", "tokens"},
        "errors": set(),
        "model": {"expressions", "markings"},
        "validation": {"expressions", "markings", "model"},
        "execution": {
            "errors",
            "expressions",
            "markings",
            "model",
            "tokens",
            "validation",
        },
    }
    imports_by_module = {
        module: {
            node.module
            for node in ast.walk(ast.parse((source / f"{module}.py").read_text()))
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module
        }
        for module in allowed
    }
    violations = {
        module: imports - allowed[module]
        for module, imports in imports_by_module.items()
        if not imports <= allowed[module]
    }
    assert violations == {}
