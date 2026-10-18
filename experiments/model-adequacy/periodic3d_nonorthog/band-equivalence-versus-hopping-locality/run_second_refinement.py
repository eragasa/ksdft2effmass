"""Run the second bounded silicon-inspired mesh-refinement point."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from run_development import DEFINITION, construct_artifacts, write_artifacts
from run_first_refinement import REFINEMENT as FIRST_REFINEMENT

from ksdft2effmass.application.band_equivalence_locality import (
    BandEquivalenceLocalityRefinementAssessor,
    BandEquivalenceLocalityRefinementRequest,
)

REFINEMENT = replace(DEFINITION, construction_size=32, evaluation_size=65)


def main() -> int:
    """Calculate, verify, and assess the complete development ladder."""
    requests = (DEFINITION, FIRST_REFINEMENT, REFINEMENT)
    artifacts = tuple(construct_artifacts(request) for request in requests)
    results = tuple(result for result, _ in artifacts)
    verifications = tuple(verification for _, verification in artifacts)
    if not all(item.diagnostics.passes for item in verifications):
        raise RuntimeError("independent refinement-ladder verification failed")
    experiment = Path(__file__).resolve().parent
    outputs = (
        experiment / "analysis" / "development",
        experiment / "analysis" / "development-refinement" / "N16",
        experiment / "analysis" / "development-refinement" / "N32",
    )
    for output, result, verification in zip(
        outputs, results, verifications, strict=True
    ):
        write_artifacts(output, result, verification)
    assessment = BandEquivalenceLocalityRefinementAssessor().execute(
        BandEquivalenceLocalityRefinementRequest(results)
    )
    assessment.document.write_to(
        experiment
        / "analysis"
        / "development-refinement"
        / "development-refinement-assessment.json"
    )
    print(
        f"family={REFINEMENT.family.value} lifecycle=development "
        "construction_sizes=8,16,32 verification=pass "
        f"disposition={assessment.assessment.momentum_disposition}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
