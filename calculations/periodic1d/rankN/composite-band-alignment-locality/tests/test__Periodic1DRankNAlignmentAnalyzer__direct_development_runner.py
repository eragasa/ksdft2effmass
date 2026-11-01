"""Structural tests for the maintained direct development runner."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic1DRankNAlignmentAnalyzer:
    """Establish direct owner composition and development-only output semantics."""

    def test__source__uses_direct_owners_without_workflow_imports(self) -> None:
        runner = Path(__file__).resolve().parents[1] / "run_01_calculation.py"
        source = runner.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(runner))
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
        assert "Periodic1DRankNAlignmentAnalyzer" in source
        assert "NumpyBatchedComplexUnitaryProcrustesSolver" in source
        assert "ClosedLoopPolarFrameTransporter" in source
        assert "FinitePeriodicMatrixFourierTransformer" in source
        assert "FinitePeriodicMatrixFourierTensorEvaluator" in source
        assert "ScalarRefinementAnalyzer" in source
        assert "calculation_infrastructure_sha256" in source
        assert "analysis/development/plots.py" not in source

    def test__source__uses_gauge_alignment_vocabulary_and_disclaims_evidence(
        self,
    ) -> None:
        runner = Path(__file__).resolve().parents[1] / "run_01_calculation.py"
        source = runner.read_text(encoding="utf-8")

        assert '"gauge_alignment"' in source
        assert '"final_mesh_gauge_alignments"' in source
        assert '"scientific_evidence": False' in source
        assert '"channel"' not in source
        assert all(old_value not in source for old_value in ("A0", "A1", "A2", "A3"))
