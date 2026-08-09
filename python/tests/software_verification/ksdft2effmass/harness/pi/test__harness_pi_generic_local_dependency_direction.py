r"""Software verification of harness pi generic local dependency direction.

Facet and represented meaning

Software verification of the generic-to-local dependency prohibition; no physical model,
mathematics, or numerical representation is involved.

Intrinsic and cross-object scope

The primary owner is the generic/local dependency-direction artifact. Maintained
direction rules and selected generic/local manifests are independent oracles.

VVUQ and scientific exclusions

Passing establishes bounded import/resource direction only; numerical verification,
scientific validation, UQ, physical correctness, and authorization are excluded.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[6]

pytestmark = pytest.mark.software_verification


def test_artifact__generic_python_imports__prohibit_local_and_project_domains() -> None:
    """Evidence ID: SV-HARNESS-041

    Requirement: Generic Python must not import local harness code or project-domain
    modules.

    Method: Parse every production module below the exact generic package root and
    inspect
    all import nodes without importing private behavior.

    Oracle: H1 normatively states ``generic Python -/-> local Python`` and prohibits
    project-domain imports.

    Acceptance: No import target contains ``harness.pi.local`` or begins with any
    project
    scientific-domain module.

    Interpretation: Failure identifies an architecture dependency-direction defect in
    production source.

    Limitations: AST import inspection does not prove absence of every possible dynamic
    dependency or establish scientific correctness.
    """
    prohibited = (
        "ksdft2effmass.harness.pi.local",
        "ksdft2effmass.operators",
        "ksdft2effmass.workflows",
    )

    def exercise_path_case_54_2(path: Any) -> Any:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        targets: list[str] = []

        def exercise_node_case_57_1(node: Any) -> Any:
            if isinstance(node, ast.Import):
                targets.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                targets.append(node.module)

        _ = [exercise_node_case_57_1(node) for node in ast.walk(tree)]
        assert not any(target.startswith(prohibited) for target in targets), path

    _ = [
        exercise_path_case_54_2(path)
        for path in (Path("python/src/ksdft2effmass/harness/pi").glob("*.py"))
    ]


def test_artifact__generic_resources__contain_no_project_local_identifiers() -> None:
    """Evidence ID: SV-HARNESS-042

    Requirement: Generic resources neither depend on nor embed project-local identities,
    paths, or runtime-state roots.

    Method: Read the selected generic and local manifests, compare dependency closure,
    and inspect only manifest-selected generic textual resources for explicit prohibited
    project spellings.

    Oracle: The maintained extension-only rule, local manifest identity and resource
    IDs, and project-local path boundary fix the prohibited direction.

    Acceptance: Generic dependencies are disjoint from local IDs, generic selected text
    omits local IDs and manifest identity, and no selected text contains the project
    package name, local resource root, or runtime-state root.

    Interpretation: Failure identifies accepted-resource leakage or a direction-contract
    discrepancy.

    Limitations: This checks explicit identities and path spellings, not arbitrary
    semantic equivalence, dynamic strings, authorization, science, or runtime dispatch.
    """
    generic_path = ROOT / "harness/pi/resource-manifest.json"
    generic = json.loads(generic_path.read_text())
    local = json.loads((ROOT / "harness/local/resource-manifest.json").read_text())
    local_ids = {item["resource_id"] for item in local["resources"]}
    dependencies = {
        dep for item in generic["resources"] for dep in item["dependency_ids"]
    }
    assert dependencies.isdisjoint(local_ids)
    selected_text = "\n".join(
        (ROOT / "harness/pi" / item["path"]).read_text(encoding="utf-8")
        for item in generic["resources"]
    )
    assert local["manifest_id"] not in selected_text
    assert all(resource_id not in selected_text for resource_id in local_ids)
    assert "ksdft2effmass" not in selected_text.casefold()
    assert "harness/local/" not in selected_text
    assert ".pi/" not in selected_text
