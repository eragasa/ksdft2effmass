"""Software verification for five-scale source admission."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from five_scale_consistency import FiveScaleSourceIntegrityAssessor

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


class TestFiveScaleSourceIntegrityAssessor:
    """Verify exact source bytes and canonical direct-v2 admission."""

    def test_assess__binds_declared_bytes_and_typed_record(self) -> None:
        assessment = FiveScaleSourceIntegrityAssessor().assess(
            results_directory=RESULTS,
            direct_v2_calculation=DIRECT_V2,
        )

        assert len(assessment.source_integrity.development_sources) == 5
        assert assessment.direct_v2_record.to_json() == DIRECT_V2.read_bytes()

    def test_assess__rejects_changed_source_bytes(self, tmp_path: Path) -> None:
        copied = tmp_path / "results"
        shutil.copytree(RESULTS, copied)
        path = copied / "truncation-summary.csv"
        path.write_bytes(path.read_bytes() + b"\n")

        with pytest.raises(ValueError, match="audited digest"):
            FiveScaleSourceIntegrityAssessor().assess(
                results_directory=copied,
                direct_v2_calculation=DIRECT_V2,
            )
