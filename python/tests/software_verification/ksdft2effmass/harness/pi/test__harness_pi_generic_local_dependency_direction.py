"""Evidence class and represented meaning
Software verification of the generic-to-local dependency prohibition; no physical model,
mathematics, or numerical representation is involved.

Owned contract, oracle, and scope
The primary owner is the generic/local dependency-direction artifact. Accepted H1
direction rules and H3 generic/local manifests are independent oracles.

VVUQ and scientific exclusions
Passing establishes bounded import/resource direction only; numerical verification,
scientific validation, UQ, physical correctness, and authorization are excluded.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[6]

pytestmark = pytest.mark.software_verification


def test_artifact__generic_python_imports__prohibit_local_and_project_domains() -> None:
    """Evidence ID
    SV-HARNESS-041
    Requirement
    Generic Python must not import local harness code or project-domain modules.
    Method
    Parse every production module below the exact generic package root and inspect
    all import nodes without importing private behavior.
    Oracle
    H1 normatively states ``generic Python -/-> local Python`` and prohibits
    project-domain imports.
    Acceptance
    No import target contains ``harness.pi.local`` or begins with any project
    scientific-domain module.
    Interpretation
    Failure identifies an architecture dependency-direction defect in production source.
    Limitations
    AST import inspection does not prove absence of every possible dynamic
    dependency or establish scientific correctness.
    """
    prohibited = (
        "ksdft2effmass.harness.pi.local",
        "ksdft2effmass.operators",
        "ksdft2effmass.workflows",
    )
    for path in Path("python/src/ksdft2effmass/harness/pi").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        targets: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                targets.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                targets.append(node.module)
        assert not any(target.startswith(prohibited) for target in targets), path


def test_artifact__generic_resources__contain_no_project_local_identifiers() -> None:
    """Evidence ID
    SV-HARNESS-042
    Requirement
    Generic resources neither depend on local resource identities nor embed the
    project-local manifest identity.
    Method
    Read the accepted generic and local manifests and compare generic dependency
    closure with the exact local ID set and local manifest identity.
    Oracle
    H1 overlay rules and accepted H3 manifests fix extension-only local-to-generic
    direction.
    Acceptance
    Generic resource dependencies are disjoint from local resource IDs and canonical
    generic manifest text omits the local manifest ID.
    Interpretation
    Failure identifies accepted-resource leakage or a direction-contract discrepancy.
    Limitations
    This checks declared manifest dependencies and one explicit identity, not
    arbitrary prose semantics or runtime dispatch.
    """
    generic_path = ROOT / "harness/pi/resource-manifest.json"
    generic = json.loads(generic_path.read_text())
    local = json.loads((ROOT / "harness/local/resource-manifest.json").read_text())
    local_ids = {item["resource_id"] for item in local["resources"]}
    dependencies = {
        dep for item in generic["resources"] for dep in item["dependency_ids"]
    }
    assert dependencies.isdisjoint(local_ids)
    assert local["manifest_id"] not in generic_path.read_text()
