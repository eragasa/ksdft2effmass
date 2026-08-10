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

import pytest

ROOT = Path(__file__).resolve().parents[6]

pytestmark = pytest.mark.software_verification


def test_artifact__generic_python_imports__prohibit_local_and_project_domains() -> None:
    """Evidence ID: SV-HARNESS-041

    Requirement: Generic Python must not import local harness code or project-domain
    modules through absolute or relative import syntax.

    Method: Resolve every production import against its containing package and exercise
    controlled absolute and relative import examples before scanning the generic tree.

    Oracle: Python's relative-import level semantics and the H1 generic-to-local and
    project-domain dependency prohibitions determine each absolute target.

    Acceptance: Controlled examples resolve to their exact absolute targets, and no
    actual target starts with a prohibited package.

    Interpretation: Failure identifies either an import-resolution oracle defect or an
    architecture dependency-direction defect in production source.

    Limitations: AST inspection does not detect dynamic imports or establish scientific
    correctness.
    """
    prohibited = (
        "ksdft2effmass.harness.pi.local",
        "ksdft2effmass.operators",
        "ksdft2effmass.workflows",
    )
    source_root = ROOT / "python/src"
    generic_root = source_root / "ksdft2effmass/harness/pi"

    def import_targets(source: str, path: Path) -> tuple[str, ...]:
        relative = path.relative_to(source_root).with_suffix("")
        module_parts = list(relative.parts)
        package_parts = (
            list(relative.parent.parts)
            if path.name == "__init__.py"
            else module_parts[:-1]
        )
        targets: list[str] = []

        def collect_import_targets(node: ast.AST) -> None:
            if isinstance(node, ast.Import):
                targets.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    keep = len(package_parts) - (node.level - 1)
                    base_parts = package_parts[: max(keep, 0)]
                else:
                    base_parts = []
                if node.module:
                    base_parts.extend(node.module.split("."))
                base = ".".join(base_parts)
                if base:
                    targets.append(base)
                targets.extend(
                    ".".join((*base_parts, alias.name))
                    for alias in node.names
                    if alias.name != "*"
                )

        _ = [
            collect_import_targets(node)
            for node in ast.walk(ast.parse(source, filename=str(path)))
        ]
        return tuple(targets)

    controlled_path = generic_root / "dbcontrol/example.py"
    controlled = {
        "import ksdft2effmass.harness.pi.local": ("ksdft2effmass.harness.pi.local",),
        "from ksdft2effmass.harness.pi.local import dbcontrol": (
            "ksdft2effmass.harness.pi.local",
            "ksdft2effmass.harness.pi.local.dbcontrol",
        ),
        "from ..local import dbcontrol": (
            "ksdft2effmass.harness.pi.local",
            "ksdft2effmass.harness.pi.local.dbcontrol",
        ),
        "from ...pi.local import adapters": (
            "ksdft2effmass.harness.pi.local",
            "ksdft2effmass.harness.pi.local.adapters",
        ),
        "from .. import local": (
            "ksdft2effmass.harness.pi",
            "ksdft2effmass.harness.pi.local",
        ),
    }
    assert {
        source: import_targets(source, controlled_path) for source in controlled
    } == controlled

    def assert_import_direction(path: Path) -> None:
        targets = import_targets(path.read_text(encoding="utf-8"), path)
        assert not any(target.startswith(prohibited) for target in targets), path

    _ = [
        assert_import_direction(path)
        for path in generic_root.rglob("*.py")
        if "local" not in path.relative_to(generic_root).parts
    ]


def test_artifact__dbcontrol_modules__contain_no_module_level_functions() -> None:
    """Evidence ID: software-verification.harness.dbcontrol-ownership.no-module-functions

    Requirement: Every production transformation in both R2.1 dbcontrol packages is
    owned by a cohesive object rather than a module-level implementation function.

    Method: Parse every Python module under the generic and project-local dbcontrol
    package roots and inspect only direct module-body nodes.

    Oracle: Direct ``ast.FunctionDef`` and ``ast.AsyncFunctionDef`` nodes represent
    module-level functions; methods occur beneath class nodes.

    Acceptance: Neither package contains a direct module-level function node.

    Interpretation: Failure identifies regression of the accepted R2.1 ownership
    boundary.

    Limitations: Structural ownership does not by itself prove behavioral cohesion or
    public API compatibility.
    """  # noqa: E501
    roots = (
        ROOT / "python/src/ksdft2effmass/harness/pi/dbcontrol",
        ROOT / "python/src/ksdft2effmass/harness/pi/local/dbcontrol",
    )

    def assert_no_module_functions(path: Path) -> None:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        assert not any(
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            for node in tree.body
        ), path

    _ = [
        assert_no_module_functions(path)
        for root in roots
        for path in root.rglob("*.py")
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
