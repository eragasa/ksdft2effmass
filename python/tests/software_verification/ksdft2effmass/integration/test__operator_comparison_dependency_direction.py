r"""Software verification of OperatorComparisonDependencyDirection.

Facet and represented meaning

-----------------------------
This artifact-owned module owns the operator comparison dependency direction facet.
This technical integration module, rather than an Analyzer object test, owns the
architecture contract ``records -> compatibility -> difference -> residuals ->
comparison``. It parses only first-party module imports and verifies that every
comparison-subsystem relative import points to the same or an earlier approved
layer. This is software verification of package topology, not Analyzer behavior,
numerical verification, scientific validation, or uncertainty quantification.
Failure indicates an architecture regression or an evidence-contract defect that
requires investigation; passing does not establish scientific correctness.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``OperatorComparisonDependencyDirection``; collaborators only
construct inputs or expose public outcomes. Accepted public contracts, literal
expected values, Python language semantics, and assigned schema or fixture artifacts
provide the oracles. No runtime warning is accepted unless a test explicitly states
otherwise.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
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
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Dependency evidence must inspect maintained first-party package edges.

    Method: Parse one module and retain level-one ``from .<module> import`` targets.

    Oracle: Python's public AST identifies relative import statements explicitly.

    Acceptance: The tuple contains every direct approved-subsystem relative import in
    source
    traversal order.

    Interpretation: Returned names are the source-declared local dependency edges.

    Limitations: Dynamic imports are outside the current package contract and this
    helper does not
    execute imports, assess Analyzer behavior, perform scientific validation, or perform
    uncertainty quantification.
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


def test_artifact__operator_comparison_modules_follow_approved__agrees_exactly() -> (
    None
):
    r"""Evidence ID: SV-ORCD-001

    Requirement: A module may import only earlier comparison-subsystem layers; in
    particular,
    compatibility cannot import difference, residuals, or comparison.

    Method: Parse each maintained module and compare every local edge with the approved
    rank
    tuple.

    Oracle: The active architecture contract defines ``MODULE_ORDER``.

    Acceptance: Every imported comparison-subsystem module has a strictly lower rank.

    Interpretation: Passing establishes the maintained static dependency-direction gate.

    Limitations: This is package integration evidence, not public Analyzer behavior,
    scientific
    validation, or uncertainty quantification; it makes no claim about physical or
    numerical validity.
    """

    operators_dir = (
        Path(__file__).resolve().parents[4] / "src" / "ksdft2effmass" / "operators"
    )
    rank = {module_name: index for index, module_name in enumerate(MODULE_ORDER)}

    assert all(
        rank[imported_name] < rank[module_name]
        for module_name in MODULE_ORDER
        for imported_name in local_imports(operators_dir / f"{module_name}.py")
    ), "an operator-comparison module imports a non-earlier layer"
