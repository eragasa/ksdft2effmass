r"""Software verification of Quantum ESPRESSO integration dependency direction.

Evidence profile: routine

Bounded artifact scope: package imports across the concrete QE integration boundary.

Facet and represented meaning

The artifact verifies the accepted inward dependency direction between application,
QE integration, calculators, and workflows.

Intrinsic and cross-object scope

Static import targets beneath the maintained source packages are covered. Runtime
behavior, parsing, execution, adaptation, and normalized-observation assembly belong
to their existing cohesive evidence owners.

VVUQ and scientific exclusions

This is structural software verification only. It performs no calculator execution and
establishes no numerical verification, scientific validation, uncertainty
quantification, or human acceptance.
"""

import ast
import importlib.util
from pathlib import Path

import pytest

pytestmark = pytest.mark.software_verification


class TestQuantumEspressoIntegrationDependencyDirection:
    """Own package-level QE integration dependency-direction evidence."""

    @staticmethod
    def imported_names(
        source_root: Path, source_paths: tuple[Path, ...]
    ) -> tuple[str, ...]:
        """Return package-resolved import targets from maintained source.

        Evidence ID: Helper owns no identifier.

        Requirement: Support dependency checks without importing scanned modules.

        Method: Parse each maintained Python source, resolve relative imports against
        its exact package, and retain complete module and imported-member targets.

        Oracle: Consuming test methods own all assertions.

        Acceptance: Return one deterministic tuple of absolute import targets.

        Interpretation: Parsing or relative-resolution failure blocks the consuming
        structural evidence.

        Limitations: Static imports do not establish runtime dependency use.
        """
        trees = tuple(
            (path, ast.parse(path.read_text(encoding="utf-8"))) for path in source_paths
        )
        nodes = tuple((path, node) for path, tree in trees for node in ast.walk(tree))
        direct_names = tuple(
            alias.name
            for _, node in nodes
            if isinstance(node, ast.Import)
            for alias in node.names
        )
        from_nodes = tuple(
            (path, node) for path, node in nodes if isinstance(node, ast.ImportFrom)
        )
        from_modules = tuple(
            importlib.util.resolve_name(
                f"{'.' * node.level}{node.module or ''}",
                ".".join(path.relative_to(source_root).parent.parts),
            )
            if node.level
            else (node.module or "")
            for path, node in from_nodes
        )
        from_members = tuple(
            f"{module_name}.{alias.name}"
            for path, node in from_nodes
            for module_name in (
                importlib.util.resolve_name(
                    f"{'.' * node.level}{node.module or ''}",
                    ".".join(path.relative_to(source_root).parent.parts),
                )
                if node.level
                else (node.module or ""),
            )
            for alias in node.names
        )
        return direct_names + from_modules + from_members

    def test_artifact__dependency__inner_packages_import_no_integration(self) -> None:
        """Evidence ID: SV-QE-INTEGRATION-VERIFY-001

        Requirement: Calculator and Workflow packages never import a concrete
        integration implementation.

        Acceptance: Their parsed import targets contain no integration package or
        relative integration segment.
        """
        package_root = Path(__file__).resolve().parents[5] / "src" / "ksdft2effmass"
        calculator_paths = tuple(sorted((package_root / "calculators").rglob("*.py")))
        workflow_paths = tuple(sorted((package_root / "workflows").rglob("*.py")))
        source_paths = calculator_paths + workflow_paths

        assert calculator_paths
        assert workflow_paths
        forbidden_prefixes = (
            "integration",
            "ksdft2effmass.integration",
        )
        imported_names = self.imported_names(package_root.parent, source_paths)

        assert not any(
            name == prefix or name.startswith(f"{prefix}.")
            for name in imported_names
            for prefix in forbidden_prefixes
        )

    def test_artifact__dependency__integration_imports_no_outward_owner(self) -> None:
        """Evidence ID: SV-QE-INTEGRATION-VERIFY-002

        Requirement: QE integration imports only inward calculator, Workflow, and
        neutral-domain owners rather than application or other outward composition.

        Acceptance: Parsed integration imports contain no application, campaign,
        analysis, persistence, or Harness package segment.
        """
        package_root = Path(__file__).resolve().parents[5] / "src" / "ksdft2effmass"
        source_paths = tuple(
            sorted((package_root / "integration" / "quantum_espresso").rglob("*.py"))
        )

        assert source_paths
        forbidden_prefixes = (
            "analysis",
            "application",
            "campaigns",
            "harness",
            "ksdft2effmass.analysis",
            "ksdft2effmass.application",
            "ksdft2effmass.campaigns",
            "ksdft2effmass.harness",
            "ksdft2effmass.persistence",
            "persistence",
        )
        imported_names = self.imported_names(package_root.parent, source_paths)

        assert not any(
            name == prefix or name.startswith(f"{prefix}.")
            for name in imported_names
            for prefix in forbidden_prefixes
        )
