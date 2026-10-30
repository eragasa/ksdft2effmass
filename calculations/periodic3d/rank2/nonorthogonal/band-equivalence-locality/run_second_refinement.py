"""Run the second bounded silicon-inspired mesh-refinement point."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.refinement import (
    BandEquivalenceLocalityRefinementAnalyzer,
)
from run_development import DEFINITION, construct_artifacts, write_artifacts
from run_first_refinement import REFINEMENT as FIRST_REFINEMENT

REFINEMENT = replace(DEFINITION, construction_size=32, evaluation_size=65)


def main() -> int:
    """Calculate, verify, and assess the complete development ladder."""
    requests = (DEFINITION, FIRST_REFINEMENT, REFINEMENT)
    artifacts = tuple(construct_artifacts(request) for request in requests)
    results = tuple(result for result, _ in artifacts)
    verifications = tuple(verification for _, verification in artifacts)
    if not all(item.passes for item in verifications):
        raise RuntimeError("independent refinement-ladder verification failed")
    development = Path(__file__).resolve().parent / "simulations" / "development"
    outputs = (
        development / "results" / "development",
        development / "results" / "refinement" / "N16",
        development / "results" / "refinement" / "N32",
    )
    for output, result, verification in zip(
        outputs, results, verifications, strict=True
    ):
        write_artifacts(output, result, verification)
    assessment = BandEquivalenceLocalityRefinementAnalyzer(
        results=tuple(result.diagnostics for result in results)
    ).execute()
    (
        development
        / "results"
        / "refinement"
        / "development-refinement-assessment.json"
    ).write_text(assessment.to_json(), encoding="utf-8")
    print(
        f"family={REFINEMENT.family.to_wire()} lifecycle=development "
        "construction_sizes=8,16,32 verification=pass "
        f"disposition={assessment.momentum_disposition}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
