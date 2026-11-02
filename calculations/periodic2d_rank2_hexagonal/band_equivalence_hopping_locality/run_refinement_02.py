"""Run the second bounded graphene-inspired mesh-refinement point."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from run_nominal_calculation import DEFINITION, construct_artifacts, write_artifacts
from run_refinement_01 import REFINEMENT as FIRST_REFINEMENT

from ksdft2effmass.band_equivalence_hopping_locality.refinement import (
    BandEquivalenceHoppingLocalityRefinementAnalyzer,
)
from ksdft2effmass.band_equivalence_hopping_locality.refinement_recording import (
    BandEquivalenceHoppingLocalityRefinementAssessmentRecorder,
)

REFINEMENT = replace(DEFINITION, construction_size=64, evaluation_size=129)


def main() -> int:
    """Calculate, verify, and assess the complete development ladder."""
    requests = (DEFINITION, FIRST_REFINEMENT, REFINEMENT)
    artifacts = tuple(construct_artifacts(request) for request in requests)
    analyses = tuple(analysis for analysis, _, _ in artifacts)
    results = tuple(result for _, result, _ in artifacts)
    verifications = tuple(verification for _, _, verification in artifacts)
    if not all(item.passes for item in verifications):
        raise RuntimeError("independent refinement-ladder verification failed")
    replaceable = Path(__file__).resolve().parent / "simulations" / "replaceable"
    outputs = (
        replaceable / "results" / "nominal",
        replaceable / "results" / "refinement" / "N32",
        replaceable / "results" / "refinement" / "N64",
    )
    for output, result, verification in zip(
        outputs, results, verifications, strict=True
    ):
        write_artifacts(output, result, verification)
    assessment = BandEquivalenceHoppingLocalityRefinementAnalyzer(
        results=analyses
    ).execute()
    assessment_record = BandEquivalenceHoppingLocalityRefinementAssessmentRecorder(
        assessment
    ).result()
    (
        replaceable
        / "results"
        / "refinement"
        / "development-refinement-assessment.json"
    ).write_bytes(assessment_record.to_json())
    print(
        f"family={REFINEMENT.family.to_wire()} lifecycle=development "
        "construction_sizes=16,32,64 verification=pass "
        f"disposition={assessment.momentum_disposition}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
