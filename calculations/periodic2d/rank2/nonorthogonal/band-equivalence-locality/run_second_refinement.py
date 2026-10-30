"""Run the second bounded graphene-inspired mesh-refinement point."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.refinement import (
    BandEquivalenceLocalityRefinementAnalyzer,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.refinement_recording import (
    BandEquivalenceLocalityRefinementAssessmentRecorder,
)
from run_development import DEFINITION, construct_artifacts, write_artifacts
from run_first_refinement import REFINEMENT as FIRST_REFINEMENT

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
    development = Path(__file__).resolve().parent / "simulations" / "development"
    outputs = (
        development / "results" / "development",
        development / "results" / "refinement" / "N32",
        development / "results" / "refinement" / "N64",
    )
    for output, result, verification in zip(
        outputs, results, verifications, strict=True
    ):
        write_artifacts(output, result, verification)
    assessment = BandEquivalenceLocalityRefinementAnalyzer(results=analyses).execute()
    assessment_record = BandEquivalenceLocalityRefinementAssessmentRecorder(
        assessment
    ).result()
    (
        development
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
