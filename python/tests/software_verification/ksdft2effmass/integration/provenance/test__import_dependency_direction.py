"""Evidence class and represented meaning
Software verification of provenance package import dependency direction and isolation.
Owned contract, oracle, and scope
The static Python import topology is the artifact owner; the approved internal layering
and forbidden roots are exact oracles.
VVUQ and scientific exclusions
Evidence excludes dynamic/transitive imports, execution behavior, numerical
verification, scientific validation, UQ, and cross-language conformance.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[6]
SOURCE = REPO_ROOT / "python/src/ksdft2effmass/provenance"
pytestmark = pytest.mark.software_verification

EXPECTED_INTERNAL_IMPORTS = {
    "__init__.py": {
        "actions",
        "external_execution",
        "external_tools",
        "records",
        "serialization",
        "tool_observations",
    },
    "actions.py": {"external_execution", "records"},
    "external_execution.py": set(),
    "external_tools.py": set(),
    "records.py": set(),
    "serialization.py": {
        "actions",
        "external_execution",
        "external_tools",
        "records",
        "tool_observations",
    },
    "tool_observations.py": set(),
}
FORBIDDEN_ROOTS = {"snakes", "subprocess"}
FORBIDDEN_TEXT = (
    "workflows.cpn",
    "scheduler",
    "backend_registry",
    "mutable_client",
    "service_locator",
)


def _imports(path: Path) -> tuple[set[str], set[str]]:
    """Evidence ID
    Supports SV-PROV-070 and SV-PROV-071 and owns no separate identifier.
    Requirement
    Extract direct root and relative provenance imports from one source module.
    Method
    Parse Python AST and inspect Import and ImportFrom nodes only.
    Oracle
    Python AST import syntax defines the extraction.
    Acceptance
    Return direct root names and level-one relative module names.
    Interpretation
    Helper failure is static-analysis setup failure.
    Limitations
    Dynamic and transitive imports are excluded.
    """
    roots: set[str] = set()
    internal: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level == 1 and node.module:
                internal.add(node.module.split(".")[0])
            elif node.level == 0 and node.module:
                roots.add(node.module.split(".")[0])
    return roots, internal


def test_artifact__internal_import_graph__matches_approved_layering() -> None:
    """Evidence ID
    SV-PROV-070
    Requirement
    Declaration, observation, and execution records are dependency-minimal; actions
    consumes exact execution records, serialization consumes exact record families, and
    __init__ only aggregates public modules.
    Method
    Parse every exact source module and compare level-one imports with a fixed adjacency
    map.
    Oracle
    The accepted P2 decomposition fixes EXPECTED_INTERNAL_IMPORTS.
    Acceptance
    Source filename set and every direct internal edge set match exactly.
    Interpretation
    Failure indicates module inventory or dependency-direction drift.
    Limitations
    Function-call architecture and dynamic imports are not assessed.
    """
    paths = {path.name: path for path in SOURCE.glob("*.py")}
    assert set(paths) == set(EXPECTED_INTERNAL_IMPORTS)
    for name, expected in EXPECTED_INTERNAL_IMPORTS.items():
        assert _imports(paths[name])[1] == expected


def test_artifact__backend_and_runtime_isolation__excludes_forbidden_dependencies() -> (
    None
):
    """Evidence ID
    SV-PROV-071
    Requirement
    Provenance production modules do not depend directly on CPN, SNAKES, subprocess,
    backend registries, schedulers, service locators, or mutable clients.
    Method
    Inspect AST import roots and lowercase source text for exact prohibited architecture
    tokens.
    Oracle
    The human-approved P2 durable-boundary exclusions fix the forbidden inventory.
    Acceptance
    No inspected source contains a forbidden root or token.
    Interpretation
    Failure indicates unauthorized backend/runtime responsibility leakage or a
    conservative text hit requiring review.
    Limitations
    Dynamic and transitive dependencies and semantically equivalent unnamed designs are
    not detected.
    """
    for path in SOURCE.glob("*.py"):
        roots, _ = _imports(path)
        assert roots.isdisjoint(FORBIDDEN_ROOTS), path
        text = path.read_text(encoding="utf-8").lower()
        for forbidden in FORBIDDEN_TEXT:
            assert forbidden not in text, (path, forbidden)
