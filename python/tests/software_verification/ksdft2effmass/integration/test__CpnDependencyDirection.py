"""Artifact-owned verification of approved CPN dependency direction.

Evidence class: software verification. The tests use synthetic contract artifacts and
independent language/runtime or static-structure oracles. Passing is not numerical
verification, scientific validation, uncertainty quantification, engine execution,
persistence, or Rust conformance evidence.
Static AST inspection is the method; the approved production layering and absence
of deferred dependencies are the acceptance oracles. A failure indicates architecture
drift, not scientific invalidity.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[5]
pytestmark = pytest.mark.software_verification


def test_cpn_sv_p1_032_dependency_direction() -> None:
    """SV-CPN-032: enforce the approved production import layering.

    Requirement: neutral modules import only named predecessor layers. Method:
    parse every production module with the standard-library AST. Independent
    oracle: the approved per-module predecessor map below. Acceptance requires
    every relative import to be a subset. Failure indicates architectural
    dependency drift. Runtime behavior and scientific validity are excluded.
    """
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
    for module, predecessors in allowed.items():
        tree = ast.parse((source / f"{module}.py").read_text())
        imports = {
            n.module
            for n in ast.walk(tree)
            if isinstance(n, ast.ImportFrom) and n.level == 1 and n.module
        }
        assert imports <= predecessors, (module, imports - predecessors)
