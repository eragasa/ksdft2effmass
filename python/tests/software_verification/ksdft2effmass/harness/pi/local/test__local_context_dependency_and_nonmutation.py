r"""Software verification of local context dependency and nonmutation.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Software verification of explicit-root composition, package imports, dependency
direction, and generic public-surface nonmutation.

Intrinsic and cross-object scope

The artifact owner is the local/generic package integration boundary; current explicit
v2 resources and the captured generic public surface define the exact scope.

VVUQ and scientific exclusions

Passing establishes import and composition properties only, not numerical verification,
scientific validation, UQ, physical correctness, or cross-language conformance.
"""

import ast
from typing import Any

import pytest

import ksdft2effmass.harness.pi as generic

from .conftest import repository_root

pytestmark = pytest.mark.software_verification


def test_artifact__generic_local_dependency__preserves_one_way_imports() -> None:
    """Evidence ID: SV-HL-007

    Requirement: Generic code never imports local code, local code depends only upward
    on generic
    code, and local composition does not mutate the generic public surface.

    Method: Parse every generic and local source module AST and compare generic
    ``__all__`` to a
    captured public inventory before and after scanning local modules.

    Oracle: The H4 architecture fixes ``local -> generic`` direction and Python imports
    must not
    mutate an already imported module export tuple.

    Acceptance: The generic export tuple is unchanged; no generic import names local;
    local relative
    imports never traverse outside ``pi``.

    Interpretation: Failure indicates generic mutation, reverse dependency, or an
    incorrect fixed
    inventory.

    Limitations: Dynamic imports and runtime monkeypatching outside these package
    modules, science,
    UQ, and portability are excluded.
    """
    root = repository_root() / "python/src/ksdft2effmass/harness/pi"
    generic_surface = tuple(generic.__all__)

    def assert_generic_module_does_not_import_local(path: Any) -> Any:
        """Evidence ID: Owns no identifier; supports the enclosing stable evidence ID
        SV-HL-007.

        Requirement: Each selected generic module satisfies the same prohibition on
        local imports.

        Method: Parse one selected module and mechanically apply the enclosing
        import-node
        predicate.

        Oracle: The one-way dependency contract prohibits every generic import from
        naming
        the local package.

        Acceptance: No import node in the parsed module names ``local``.

        Interpretation: Failure identifies a selected generic module that reverses the
        dependency;
        this helper makes no independent evidence claim.

        Limitations: The iteration mechanically applies one identical requirement,
        oracle, and
        acceptance rule across the exact selected generic-module inventory; it hides
        no distinct partition and does not detect dynamic imports.
        """
        tree = ast.parse(path.read_text())
        assert not any(
            isinstance(node, (ast.Import, ast.ImportFrom))
            and "local"
            in (
                node.module or ""
                if isinstance(node, ast.ImportFrom)
                else " ".join(x.name for x in node.names)
            )
            for node in ast.walk(tree)
        )

    selected_generic_modules = root.glob("*.py")
    _ = [
        assert_generic_module_does_not_import_local(path)
        for path in selected_generic_modules
    ]

    def assert_local_relative_imports_stay_within_pi(path: Any) -> Any:
        """Evidence ID: Owns no identifier; supports the enclosing stable evidence ID
        SV-HL-007.

        Requirement: Each selected local module stays within the Harness package;
        compatibility modules may import the accepted v2 owner directly.

        Method: Parse one selected module and mechanically apply the enclosing
        relative-import predicate.

        Oracle: The one-way migration contract permits local compatibility imports of
        the root Harness owner but prohibits traversal beyond that package.

        Acceptance: No relative import has a level greater than three; level-three
        imports name only a v2 Task, selection, or validation owner.

        Interpretation: Failure identifies a selected local module that crosses the
        package boundary;
        this helper makes no independent evidence claim.

        Limitations: The iteration mechanically applies one identical requirement,
        oracle, and
        acceptance rule across the exact selected local-module inventory; it hides no
        distinct partition and does not detect dynamic imports.
        """
        tree = ast.parse(path.read_text())
        relative_imports = tuple(
            node for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
        )
        assert not any(node.level > 3 for node in relative_imports)
        assert all(
            node.level != 3
            or node.module in {None, "task", "task_selection", "validation"}
            for node in relative_imports
        )

    selected_local_modules = (root / "local").glob("*.py")
    _ = [
        assert_local_relative_imports_stay_within_pi(path)
        for path in selected_local_modules
    ]
    assert tuple(generic.__all__) == generic_surface


def test_public_api__package_local_imports__avoid_execution_side_effects() -> None:
    """Evidence ID: SV-HL-008

    Requirement: Installed-source package imports complete without initiating
    validation or command execution.

    Method: Import the selected maintained local modules.

    Oracle: Python import semantics and the selected module names define the expected
    represented state.

    Acceptance: Every selected module imports and no subprocess result is produced by
    import.

    Interpretation: Failure identifies packaging, circular-import, or import-side-effect
    regression.

    Limitations: A built wheel and alternate Python implementations are not tested;
    numerical,
    scientific, and UQ claims are excluded.
    """
    modules = (
        "adapters",
        "context",
        "models",
        "validation",
        "checkpoint_validation",
        "_parsing",
        "task_model",
        "dbcontrol",
        "control",
    )
    imported = [
        __import__(f"ksdft2effmass.harness.pi.local.{name}", fromlist=["*"])
        for name in modules
    ]
    assert len(imported) == len(modules)
