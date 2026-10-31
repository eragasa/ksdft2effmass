"""Software verification for byte-bound five-scale consistency."""

from __future__ import annotations

import shutil
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
from five_scale_evidence_assessment import (
    FiveScaleConsistencyAssessor,
    FiveScaleCutoffDecisionConsistency,
    FiveScaleEvidenceCoverage,
    FiveScaleMomentumDisposition,
    FiveScaleSourceArtifactIntegrity,
    FiveScaleTableReproductionConsistency,
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


class TestFiveScaleConsistencyAssessor:
    """Establish bounded consistency and preserve explicit evidence gaps."""

    def test_assessment__binds_the_complete_five_scale_tables(self) -> None:
        assessment = FiveScaleConsistencyAssessor().assess(
            results_directory=RESULTS,
            direct_v2_calculation=DIRECT_V2,
        )
        source = assessment.source_integrity
        tables = assessment.table_reproduction
        decisions = assessment.cutoff_decisions

        assert type(source) is FiveScaleSourceArtifactIntegrity
        assert type(tables) is FiveScaleTableReproductionConsistency
        assert type(decisions) is FiveScaleCutoffDecisionConsistency
        assert len(source.development_sources) == 5
        assert tables.parent_hopping_scales == (0.0, 0.25, 0.5, 0.75, 1.0)
        assert len(tables.amplitudes) == 33
        assert tables.maximum_ranges == tuple(range(17))
        assert tables.construction_mesh_sizes == (128, 256, 512)
        assert tables.parent_family_surface_rows == 165
        assert tables.parent_family_summary_rows == 5
        assert tables.truncation_consequence_rows == 2_805
        assert tables.truncation_summary_rows == 5
        assert tables.truncation_refinement_rows == 495

        assert tables.parent_endpoint_value_comparisons == 10
        assert tables.parent_endpoint_maximum_defect == 0.0
        assert tables.truncation_summary_value_comparisons == 45
        assert tables.truncation_summary_maximum_defect == 0.0
        assert decisions.threshold_decision_comparisons == 660
        assert decisions.threshold_value_comparisons == 1_252
        assert decisions.threshold_value_maximum_defect == 0.0
        assert decisions.decision_changes_128_to_256 == 0
        assert decisions.decision_changes_256_to_512 == 0

    def test_assessment__preserves_semantic_and_retained_evidence_gaps(self) -> None:
        assessment = FiveScaleConsistencyAssessor().assess(
            results_directory=RESULTS,
            direct_v2_calculation=DIRECT_V2,
        )
        momentum = assessment.momentum_disposition
        coverage = assessment.evidence_coverage

        assert type(momentum) is FiveScaleMomentumDisposition
        assert type(coverage) is FiveScaleEvidenceCoverage
        assert momentum.donor_dispositions == ("converged",) * 5
        assert momentum.installed_direct_v2_disposition.endswith(
            "MomentumRefinementUnresolved"
        )
        assert momentum.semantic_equivalence_established is False
        assert coverage.development_truncation_rows == 2_805
        assert coverage.direct_v2_truncation_rows == 561
        assert coverage.unmatched_development_truncation_rows == 2_244
        assert coverage.complete_retained_coverage is False

    def test_values__are_immutable_and_reject_inconsistent_coverage(self) -> None:
        assessment = FiveScaleConsistencyAssessor().assess(
            results_directory=RESULTS,
            direct_v2_calculation=DIRECT_V2,
        )

        with pytest.raises(FrozenInstanceError):
            assessment.source_integrity.__setattr__("direct_v2_sha256", "0" * 64)
        with pytest.raises(ValueError, match="partition development rows"):
            FiveScaleEvidenceCoverage(
                development_truncation_rows=2_805,
                direct_v2_truncation_rows=561,
                unmatched_development_truncation_rows=2_243,
            )

    def test_assessment__rejects_changed_source_bytes(self, tmp_path: Path) -> None:
        copied = tmp_path / "results"
        shutil.copytree(RESULTS, copied)
        path = copied / "truncation-summary.csv"
        path.write_bytes(path.read_bytes() + b"\n")

        with pytest.raises(ValueError, match="audited digest"):
            FiveScaleConsistencyAssessor().assess(
                results_directory=copied,
                direct_v2_calculation=DIRECT_V2,
            )
