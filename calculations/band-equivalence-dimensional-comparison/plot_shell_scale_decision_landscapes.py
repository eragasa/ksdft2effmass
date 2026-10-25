"""Calculate and plot the eight sampled shell--scale decision landscapes."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Protocol, cast

from band_equivalence_workflow.decision_landscape_serialization import (
    DecisionLandscapeEnvironment,
    ShellScaleDecisionLandscapeArtifactWriter,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    BandEquivalenceLocalityRequest,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.decision_landscape import (
    ShellScaleDecisionLandscapeCalculator,
    ShellScaleDecisionLandscapeRequest,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.decision_landscape_plotting import (
    ShellScaleDecisionLandscapePlotRequest,
    ShellScaleDecisionLandscapePlotWriter,
)


class _DevelopmentDefinitionModule(Protocol):
    """Expose the typed request owned by one family composition root."""

    DEFINITION: BandEquivalenceLocalityRequest


CALCULATION_DIRECTORY = Path(__file__).resolve().parent
CALCULATIONS_DIRECTORY = CALCULATION_DIRECTORY.parent
FAMILY_DEFINITION_PATHS = (
    CALCULATIONS_DIRECTORY
    / "periodic2d"
    / "rank2"
    / "orthogonal"
    / "band-equivalence-locality"
    / "run_development.py",
    CALCULATIONS_DIRECTORY
    / "periodic2d"
    / "rank2"
    / "nonorthogonal"
    / "band-equivalence-locality"
    / "run_development.py",
    CALCULATIONS_DIRECTORY
    / "periodic3d"
    / "rank2"
    / "orthogonal"
    / "band-equivalence-locality"
    / "run_development.py",
    CALCULATIONS_DIRECTORY
    / "periodic3d"
    / "rank2"
    / "nonorthogonal"
    / "band-equivalence-locality"
    / "run_development.py",
)
OUTPUT_DIRECTORY = CALCULATION_DIRECTORY / "analysis" / "development" / "generated"


def _load_definition(path: Path, index: int) -> BandEquivalenceLocalityRequest:
    """Load one explicit family request without packaging experiment roots."""
    specification = importlib.util.spec_from_file_location(
        f"shell_scale_decision_landscape_family_{index}",
        path,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"could not load family definition: {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    definition = cast(_DevelopmentDefinitionModule, module).DEFINITION
    if type(definition) is not BandEquivalenceLocalityRequest:
        raise TypeError(f"DEFINITION is not BandEquivalenceLocalityRequest: {path}")
    return definition


def main() -> int:
    """Calculate all family landscapes and render separate and composite views."""
    calculator = ShellScaleDecisionLandscapeCalculator()
    requests = tuple(
        ShellScaleDecisionLandscapeRequest(
            locality_request=_load_definition(path, index),
            scale_sample_count=17,
        )
        for index, path in enumerate(FAMILY_DEFINITION_PATHS)
    )
    results = tuple(calculator.execute(request) for request in requests)
    environment = DecisionLandscapeEnvironment.capture()
    artifact_writer = ShellScaleDecisionLandscapeArtifactWriter()
    artifacts = tuple(
        artifact_writer.execute(request, result, OUTPUT_DIRECTORY, environment)
        for request, result in zip(requests, results, strict=True)
    )
    plots = ShellScaleDecisionLandscapePlotWriter().execute(
        ShellScaleDecisionLandscapePlotRequest(
            family_results=results,
            output_directory=OUTPUT_DIRECTORY,
        )
    )
    for result in results:
        for case in result.cases:
            print(
                "decision-landscape",
                f"case={case.name}",
                f"parent_scale={case.parent_scale:.12g}",
                f"gauge_amplitude={case.gauge_amplitude:.12g}",
                f"lambda_star={case.optimized_comparison_scale:.12g}",
                f"shells={case.shell_indices}",
                f"blocks={case.retained_block_counts}",
                f"calculated={case.calculated_vertex_count}",
                f"nondominated={case.pareto_efficient_vertex_count}",
            )
    for artifact in artifacts:
        print(
            "decision-landscape-artifact",
            artifact.decision_result_path,
            artifact.decision_result_sha256,
        )
    for path in plots.paths:
        print(f"output={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
