"""Software verification for five-scale momentum dispositions."""

from __future__ import annotations

from pathlib import Path

import pytest
from development_diagnostics import DiagnosticBundle, DiagnosticTable
from five_scale_consistency import (
    FiveScaleMomentumDispositionAssessor,
    FiveScaleSourceIntegrityAssessor,
)

pytestmark = pytest.mark.software_verification

CALCULATION_ROOT = Path(__file__).resolve().parents[1]
RESULTS = CALCULATION_ROOT / "simulations" / "development" / "results"
DIRECT_V2 = (
    CALCULATION_ROOT
    / "executions"
    / "direct-embedded-rank2-controlled-v2"
    / "results"
    / "calculation.json"
)


class TestFiveScaleMomentumDispositionAssessor:
    """Verify that distinct diagnostic outcomes remain explicit."""

    def test_assess__does_not_equate_donor_and_installed_outcomes(self) -> None:
        source = FiveScaleSourceIntegrityAssessor().assess(
            results_directory=RESULTS,
            direct_v2_calculation=DIRECT_V2,
        )
        parent_summary = DiagnosticBundle.load(RESULTS).table(
            DiagnosticTable.PARENT_FAMILY_SUMMARY
        )

        disposition = FiveScaleMomentumDispositionAssessor().assess(
            parent_summary=parent_summary,
            direct_v2_record=source.direct_v2_record,
            parent_hopping_scales=(0.0, 0.25, 0.5, 0.75, 1.0),
        )

        assert disposition.donor_dispositions == ("converged",) * 5
        assert disposition.installed_direct_v2_disposition.endswith(
            "MomentumRefinementUnresolved"
        )
        assert disposition.semantic_equivalence_established is False
