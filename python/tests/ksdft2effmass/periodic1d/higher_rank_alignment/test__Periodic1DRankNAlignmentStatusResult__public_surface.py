"""Tests for the maintained higher-rank alignment public surface."""

import ast
import importlib
from pathlib import Path

import pytest

import ksdft2effmass.periodic1d as periodic1d
from ksdft2effmass.periodic1d import higher_rank_alignment
from ksdft2effmass.periodic1d.higher_rank_alignment import gauge_alignment
from ksdft2effmass.periodic1d.rankN.alignment.result import (
    Periodic1DRankNAlignmentStatusResult,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNAlignmentStatusResult:
    """Establish explicit exports and isolate calculation-local donor code."""

    def test__package__exports_every_declared_public_name(self) -> None:
        for name in higher_rank_alignment.__all__:
            assert getattr(periodic1d, name) is getattr(higher_rank_alignment, name)
            assert "D1" not in name

    def test__status_result__belongs_to_the_rankN_alignment_partition(self) -> None:
        assert (
            higher_rank_alignment.Periodic1DRankNAlignmentStatusResult
            is Periodic1DRankNAlignmentStatusResult
        )
        assert Periodic1DRankNAlignmentStatusResult.__module__ == (
            "ksdft2effmass.periodic1d.rankN.alignment.result.status"
        )

    def test__gauge_alignment_package__exports_only_scientific_definitions(
        self,
    ) -> None:
        assert gauge_alignment.__all__ == [
            "NyquistModeDispositionEnum",
            "NyquistModeDispositionWireMapping",
            "Periodic1DRankNGaugeAlignment",
        ]

    def test__package__does_not_reexport_internal_analysis_actions(self) -> None:
        internal_names = (
            "Periodic1DRankNGaugeAlignmentAnalysisRequest",
            "Periodic1DRankNGaugeAlignmentAnalyzer",
            "Periodic1DRankNEvaluationIndependenceAnalyzer",
            "Periodic1DRankNEvaluationIndependenceResult",
            "Periodic1DRankNRefinementAnalysis",
            "Periodic1DRankNRefinementAnalysisRequest",
            "Periodic1DRankNRefinementAnalyzer",
            "Periodic1DRankNCoreInvariantReference",
            "Periodic1DRankNCoreInvariantReferenceAnalyzer",
            "Periodic1DRankNCoreInvariantReferenceRequest",
            "Periodic1DRankNFourierReference",
            "Periodic1DRankNFourierReferenceAnalyzer",
            "Periodic1DRankNFourierReferenceRequest",
            "Periodic1DRankNProcrustesReference",
            "Periodic1DRankNProcrustesReferenceAnalyzer",
            "Periodic1DRankNProcrustesReferenceRequest",
            "Periodic1DRankNTransportReference",
            "Periodic1DRankNTransportReferenceAnalyzer",
            "Periodic1DRankNTransportReferenceRequest",
        )

        assert all(name not in higher_rank_alignment.__all__ for name in internal_names)
        assert all(not hasattr(higher_rank_alignment, name) for name in internal_names)

    def test__records__belong_to_their_partitioned_owner_modules(self) -> None:
        expected_modules = {
            "Periodic1DRankNAlignmentCalculationControls": "calculation",
            "Periodic1DRankNAlignmentCalculationRequest": "calculation",
            "Periodic1DRankNAlignmentCalculationResult": "calculation_result",
            "Periodic1DRankNAlignmentStatusResult": "result.status",
            "Periodic1DRankNAlignmentTransportBackendFailureResult": (
                "result.frame_transport"
            ),
            "Periodic1DRankNAlignmentTransportLinkResult": ("result.frame_transport"),
            "Periodic1DRankNAlignmentTransportOwnerResult": ("result.frame_transport"),
            "Periodic1DRankNGaugeAlignmentMeshResult": (
                "gauge_alignment.results.alignment"
            ),
            "Periodic1DRankNMeshCalculationResult": ("gauge_alignment.results.mesh"),
            "Periodic1DRankNSupportResult": "rankN.support_truncation.result",
            "Periodic1DRankNFrameErrorResult": "diagnostics.frame",
            "Periodic1DRankNMatrixComparisonResult": "diagnostics.matrix",
            "Periodic1DRankNMatrixErrorResult": "diagnostics.matrix",
            "Periodic1DRankNModelDiagnostics": "diagnostics.model",
            "Periodic1DRankNProcrustesDiagnostics": "diagnostics.model",
            "Periodic1DRankNBlockRefinementResult": "refinement_results",
            "Periodic1DRankNScalarRefinementResult": "refinement_results",
        }

        for name, module_suffix in expected_modules.items():
            record = getattr(higher_rank_alignment, name)
            assert record.__module__.endswith(f".{module_suffix}")

        analyzer_module = (
            higher_rank_alignment.Periodic1DRankNAlignmentAnalyzer.__module__
        )
        assert analyzer_module.endswith(".analysis.calculation")

        calculation_module = importlib.import_module(
            "ksdft2effmass.periodic1d.higher_rank_alignment.calculation"
        )
        moved_names = expected_modules.keys() - {
            "Periodic1DRankNAlignmentCalculationControls",
            "Periodic1DRankNAlignmentCalculationRequest",
        }
        assert all(not hasattr(calculation_module, name) for name in moved_names)

    def test__source__does_not_import_calculation_workflow_material(self) -> None:
        package = Path(higher_rank_alignment.__file__).resolve().parent

        for path in package.rglob("*.py"):
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
