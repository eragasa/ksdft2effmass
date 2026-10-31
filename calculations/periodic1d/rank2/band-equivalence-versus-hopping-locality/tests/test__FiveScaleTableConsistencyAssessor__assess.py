"""Software verification for five-scale table reproduction."""

from __future__ import annotations

from pathlib import Path

import pytest
from development_diagnostics import DiagnosticBundle, DiagnosticTable
from five_scale_evidence_assessment import FiveScaleTableConsistencyAssessor

pytestmark = pytest.mark.software_verification

RESULTS = (
    Path(__file__).resolve().parents[1] / "simulations" / "development" / "results"
)


class TestFiveScaleTableConsistencyAssessor:
    """Verify complete inventories and exact derived-table reproduction."""

    def test_assess__reproduces_complete_five_scale_tables(self) -> None:
        bundle = DiagnosticBundle.load(RESULTS)

        result = FiveScaleTableConsistencyAssessor().assess(
            continuum=bundle.table(DiagnosticTable.PARENT_FAMILY_CONTINUUM),
            parent_summary=bundle.table(DiagnosticTable.PARENT_FAMILY_SUMMARY),
            truncation=bundle.table(DiagnosticTable.TRUNCATION_CONSEQUENCES),
            truncation_summary=bundle.table(DiagnosticTable.TRUNCATION_SUMMARY),
            refinement=bundle.table(DiagnosticTable.TRUNCATION_REFINEMENT),
        )

        assert result.parent_hopping_scales == (0.0, 0.25, 0.5, 0.75, 1.0)
        assert result.parent_family_surface_rows == 165
        assert result.truncation_consequence_rows == 2_805
        assert result.truncation_refinement_rows == 495
        assert result.parent_endpoint_value_comparisons == 10
        assert result.parent_endpoint_maximum_defect == 0.0
        assert result.truncation_summary_value_comparisons == 45
        assert result.truncation_summary_maximum_defect == 0.0
