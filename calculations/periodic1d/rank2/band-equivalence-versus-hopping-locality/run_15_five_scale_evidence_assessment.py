#!/usr/bin/env python3
"""Assess the bounded five-scale evidence after producing development controls."""

from __future__ import annotations

from pathlib import Path

from five_scale_evidence_assessment import FiveScaleConsistencyAssessor

CALCULATION = Path(__file__).resolve().parent
RESULTS = CALCULATION / "simulations" / "development" / "results"
DIRECT_V2_CALCULATION = (
    CALCULATION
    / "executions"
    / "direct-embedded-rank2-controlled-v2"
    / "results"
    / "calculation.json"
)


def main() -> None:
    """Run the read-only assessment and print its explicit evidence boundaries."""
    assessment = FiveScaleConsistencyAssessor().assess(
        results_directory=RESULTS,
        direct_v2_calculation=DIRECT_V2_CALCULATION,
    )
    tables = assessment.table_reproduction
    coverage = assessment.evidence_coverage
    momentum = assessment.momentum_disposition

    print(f"development_sources={len(assessment.source_integrity.development_sources)}")
    print(f"parent_hopping_scales={len(tables.parent_hopping_scales)}")
    print(f"truncation_rows={tables.truncation_consequence_rows}")
    print(f"direct_v2_truncation_rows={coverage.direct_v2_truncation_rows}")
    print(
        "unmatched_development_truncation_rows="
        f"{coverage.unmatched_development_truncation_rows}"
    )
    print(f"complete_retained_coverage={coverage.complete_retained_coverage}")
    print(
        "momentum_semantic_equivalence_established="
        f"{momentum.semantic_equivalence_established}"
    )


if __name__ == "__main__":
    main()
