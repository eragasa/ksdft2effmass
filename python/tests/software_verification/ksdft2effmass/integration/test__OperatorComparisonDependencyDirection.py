r"""Integration evidence for the operator-comparison module dependency direction.

This technical integration module, rather than an Analyzer object test, owns the
architecture contract ``records -> compatibility -> difference -> residuals ->
comparison``. It parses only first-party module imports and verifies that every
comparison-subsystem relative import points to the same or an earlier approved
layer. This is software verification of package topology, not Analyzer behavior,
numerical verification, scientific validation, or uncertainty quantification.
Failure indicates an architecture regression or an evidence-contract defect that
requires investigation; passing does not establish scientific correctness.
"""

import ast
from pathlib import Path

import pytest

pytestmark = pytest.mark.software_verification

MODULE_ORDER = (
    "records",
    "compatibility",
    "difference",
    "residuals",
    "comparison",
)


def local_imports(module_path: Path) -> tuple[str, ...]:
    """Return direct relative imports within the operator package.

    Evidence ID
        Supporting projection for ``SV-ORCD-001``; it owns no separate evidence
        ID.
    Requirement
        Dependency evidence must inspect maintained first-party package edges.
    Method
        Parse one module and retain level-one ``from .<module> import`` targets.
    Oracle
        Python's public AST identifies relative import statements explicitly.
    Acceptance
        The tuple contains every direct approved-subsystem relative import in
        source traversal order.
    Interpretation
        Returned names are the source-declared local dependency edges.
    Limitations
        Dynamic imports are outside the current package contract and this helper
        does not execute imports, assess Analyzer behavior, perform scientific
        validation, or perform uncertainty quantification.
    """

    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    return tuple(
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and node.level == 1
        and node.module is not None
        and node.module in MODULE_ORDER
    )


def test_operator_comparison_modules_follow_approved_dependency_direction() -> None:
    """SV-ORCD-001: enforce acyclic comparison-subsystem dependency direction.

    Requirement
        A module may import only earlier comparison-subsystem layers; in
        particular, compatibility cannot import difference, residuals, or
        comparison.
    Method
        Parse each maintained module and compare every local edge with the
        approved rank tuple.
    Oracle
        The active architecture contract defines ``MODULE_ORDER``.
    Acceptance
        Every imported comparison-subsystem module has a strictly lower rank.
    Interpretation
        Passing establishes the maintained static dependency-direction gate.
    Limitations
        This is package integration evidence, not public Analyzer behavior,
        scientific validation, or uncertainty quantification; it makes no claim
        about physical or numerical validity.
    """

    operators_dir = (
        Path(__file__).resolve().parents[4] / "src" / "ksdft2effmass" / "operators"
    )
    rank = {module_name: index for index, module_name in enumerate(MODULE_ORDER)}

    for module_name in MODULE_ORDER:
        for imported_name in local_imports(operators_dir / f"{module_name}.py"):
            assert rank[imported_name] < rank[module_name], (
                f"{module_name}.py imports non-earlier layer {imported_name}.py"
            )
