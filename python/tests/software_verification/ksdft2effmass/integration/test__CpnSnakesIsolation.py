"""Artifact-owned verification of SNAKES and deferred-engine isolation.

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


def test_cpn_sv_p1_033_snakes_isolation() -> None:
    """SV-CPN-033: exclude SNAKES and deferred adapter/persistence modules.

    Requirement: P1 remains backend-neutral and has no persistence boundary.
    Method: inspect filesystem owners and parse all production imports with AST.
    Independent oracle: absence of ``engines``, ``persistence.py``, and the
    ``snakes`` import root. Acceptance requires all three. Failure means deferred
    scope leaked into P1; it does not assess any SNAKES implementation itself.
    """
    source = REPO_ROOT / "python/src/ksdft2effmass/workflows/cpn"
    assert not (source / "engines").exists()
    assert not (source / "persistence.py").exists()
    for path in source.glob("*.py"):
        tree = ast.parse(path.read_text())
        roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                roots.add(node.module.split(".")[0])
        assert "snakes" not in roots, path
