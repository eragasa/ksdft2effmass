"""Software verification for five-scale cutoff-decision consistency."""

from __future__ import annotations

from pathlib import Path

import pytest
from development_diagnostics import DiagnosticBundle, DiagnosticTable
from five_scale_evidence_assessment import FiveScaleCutoffConsistencyAssessor

pytestmark = pytest.mark.software_verification

RESULTS = (
    Path(__file__).resolve().parents[1] / "simulations" / "development" / "results"
)


class TestFiveScaleCutoffConsistencyAssessor:
    """Verify stored support decisions and adjacent-mesh stability."""

    def test_assess__reproduces_threshold_values_and_decisions(self) -> None:
        bundle = DiagnosticBundle.load(RESULTS)

        result = FiveScaleCutoffConsistencyAssessor().assess(
            truncation=bundle.table(DiagnosticTable.TRUNCATION_CONSEQUENCES),
            refinement=bundle.table(DiagnosticTable.TRUNCATION_REFINEMENT),
        )

        assert result.threshold_decision_comparisons == 660
        assert result.threshold_value_comparisons == 1_252
        assert result.threshold_value_maximum_defect == 0.0
        assert result.decision_changes_128_to_256 == 0
        assert result.decision_changes_256_to_512 == 0
