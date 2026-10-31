"""Software verification for five-scale retained-evidence coverage."""

from __future__ import annotations

from pathlib import Path

import pytest
from five_scale_consistency import (
    FiveScaleEvidenceCoverageAssessor,
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


class TestFiveScaleEvidenceCoverageAssessor:
    """Verify the retained and unmatched truncation scopes."""

    def test_assess__preserves_partial_direct_v2_coverage(self) -> None:
        source = FiveScaleSourceIntegrityAssessor().assess(
            results_directory=RESULTS,
            direct_v2_calculation=DIRECT_V2,
        )

        coverage = FiveScaleEvidenceCoverageAssessor().assess(
            direct_v2_record=source.direct_v2_record,
            parent_hopping_scales=(0.0, 0.25, 0.5, 0.75, 1.0),
            development_truncation_rows=2_805,
        )

        assert coverage.direct_v2_truncation_rows == 561
        assert coverage.unmatched_development_truncation_rows == 2_244
        assert coverage.complete_retained_coverage is False
