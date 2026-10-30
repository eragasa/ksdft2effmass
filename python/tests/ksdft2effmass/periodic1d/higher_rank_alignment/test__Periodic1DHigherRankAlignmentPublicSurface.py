"""Tests for the maintained higher-rank alignment public surface."""

import ast
import importlib
from pathlib import Path

import pytest

import ksdft2effmass.periodic1d as periodic1d
from ksdft2effmass.periodic1d import higher_rank_alignment
from ksdft2effmass.periodic1d.higher_rank_alignment import gauge_alignment

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DHigherRankAlignmentPublicSurface:
    """Establish explicit exports and isolate calculation-local donor code."""

    def test__package__exports_every_declared_public_name(self) -> None:
        for name in higher_rank_alignment.__all__:
            assert getattr(periodic1d, name) is getattr(higher_rank_alignment, name)
            assert "D1" not in name

    def test__gauge_alignment_package__exports_only_scientific_definitions(
        self,
    ) -> None:
        assert gauge_alignment.__all__ == [
            "NyquistModeDispositionEnum",
            "NyquistModeDispositionWireMapping",
            "Periodic1DHigherRankGaugeAlignment",
        ]

    def test__package__does_not_reexport_internal_analysis_actions(self) -> None:
        internal_names = (
            "Periodic1DHigherRankGaugeAlignmentAnalysisRequest",
            "Periodic1DHigherRankGaugeAlignmentAnalyzer",
            "Periodic1DHigherRankEvaluationIndependenceAnalyzer",
            "Periodic1DHigherRankEvaluationIndependenceResult",
            "Periodic1DHigherRankRefinementAnalysis",
            "Periodic1DHigherRankRefinementAnalysisRequest",
            "Periodic1DHigherRankRefinementAnalyzer",
        )

        assert all(name not in higher_rank_alignment.__all__ for name in internal_names)
        assert all(not hasattr(higher_rank_alignment, name) for name in internal_names)

    def test__records__belong_to_their_partitioned_owner_modules(self) -> None:
        expected_modules = {
            "Periodic1DHigherRankAlignmentCalculationControls": "calculation",
            "Periodic1DHigherRankAlignmentCalculationRequest": "calculation",
            "Periodic1DHigherRankAlignmentCalculationResult": "calculation_result",
            "Periodic1DHigherRankGaugeAlignmentMeshResult": "results",
            "Periodic1DHigherRankMeshCalculationResult": "results",
            "Periodic1DHigherRankSupportResult": "results",
            "Periodic1DHigherRankFrameErrorResult": "diagnostics",
            "Periodic1DHigherRankMatrixComparisonResult": "diagnostics",
            "Periodic1DHigherRankMatrixErrorResult": "diagnostics",
            "Periodic1DHigherRankModelDiagnostics": "diagnostics",
            "Periodic1DHigherRankProcrustesDiagnostics": "diagnostics",
            "Periodic1DHigherRankBlockRefinementResult": "refinement_results",
            "Periodic1DHigherRankScalarRefinementResult": "refinement_results",
        }

        for name, module_suffix in expected_modules.items():
            record = getattr(higher_rank_alignment, name)
            assert record.__module__.endswith(f".{module_suffix}")

        calculation_module = importlib.import_module(
            "ksdft2effmass.periodic1d.higher_rank_alignment.calculation"
        )
        moved_names = expected_modules.keys() - {
            "Periodic1DHigherRankAlignmentCalculationControls",
            "Periodic1DHigherRankAlignmentCalculationRequest",
        }
        assert all(not hasattr(calculation_module, name) for name in moved_names)

    def test__source__does_not_import_calculation_workflow_material(self) -> None:
        package = Path(higher_rank_alignment.__file__).resolve().parent

        for path in package.glob("*.py"):
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            imported_modules = {
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module is not None
            } | {
                alias.name
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            }
            assert all("workflow" not in module for module in imported_modules)
            assert "HigherRankD1" not in source
