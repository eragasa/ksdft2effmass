r"""Software verification of Workflow control-ingress dependency direction.

Evidence profile: routine

Bounded artifact scope: imports beneath ``ksdft2effmass.workflows.control`` and
``ksdft2effmass.workflows.runs``.

Facet and represented meaning

This module verifies the selected effect port introduces no Workflow dependency on
calculator or integration implementations.

Intrinsic and cross-object scope

Cross-package dependency direction belongs to this artifact. Runtime effect behavior
belongs to ``SimulationDispatchAdapter`` and application composition.

VVUQ and scientific exclusions

This is structural software verification only. Source imports establish no runtime
execution, scientific validation, uncertainty quantification, or human acceptance.
"""

import ast
from pathlib import Path

import pytest

pytestmark = pytest.mark.software_verification


class TestControlIngressDependencyDirection:
    """Own dependency-direction evidence for Workflow control."""

    def test_artifact__dependency__prohibits_calculator_and_integration_imports(
        self,
    ) -> None:
        """Keep application and calculator implementations outside Workflow control.

        Evidence ID: SV-WCI-DEPENDENCY-001

        Requirement: Control source imports neither ``ksdft2effmass.calculators`` nor
        ``ksdft2effmass.integration``.

        Acceptance: Parsed absolute and relative import targets contain neither
        prohibited package segment.
        """
        source_root = (
            Path(__file__).parents[5]
            / "src"
            / "ksdft2effmass"
            / "workflows"
            / "control"
        )
        imported_names: list[str] = []
        for source_path in sorted(source_root.glob("*.py")):
            tree = ast.parse(source_path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported_names.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module is not None:
                    imported_names.append(node.module)
        assert all("calculators" not in name for name in imported_names)
        assert all("integration" not in name for name in imported_names)

    def test_artifact__dependency__run_state_does_not_import_control(self) -> None:
        """Keep durable WorkflowRun authority state below control ActionObjects.

        Evidence ID: SV-WCI-DEPENDENCY-002

        Requirement: Run-owned authority, records, aggregate, and replay source never
        import ``ksdft2effmass.workflows.control``.

        Acceptance: Parsed imports beneath ``workflows.runs`` contain no control
        package segment.
        """
        source_root = (
            Path(__file__).parents[5] / "src" / "ksdft2effmass" / "workflows" / "runs"
        )
        imported_names: list[str] = []
        for source_path in sorted(source_root.glob("*.py")):
            tree = ast.parse(source_path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported_names.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module is not None:
                    imported_names.append(node.module)
        assert all("control" not in name for name in imported_names)
