"""Calculate and plot the eight sampled shell--scale decision landscapes."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
from typing import Protocol, cast

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    BandEquivalenceLocalityRequest,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.analysis import (
    BandEquivalenceLocalityAnalyzer,
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


COMPARISON_DIRECTORY = Path(__file__).resolve().parent
MODEL_ADEQUACY_DIRECTORY = COMPARISON_DIRECTORY.parent
FAMILY_DEFINITION_PATHS = (
    MODEL_ADEQUACY_DIRECTORY
    / "periodic2d"
    / "band-equivalence-versus-hopping-locality"
    / "run_development.py",
    MODEL_ADEQUACY_DIRECTORY
    / "periodic2d_nonorthog"
    / "band-equivalence-versus-hopping-locality"
    / "run_development.py",
    MODEL_ADEQUACY_DIRECTORY
    / "periodic3d"
    / "band-equivalence-versus-hopping-locality"
    / "run_development.py",
    MODEL_ADEQUACY_DIRECTORY
    / "periodic3d_nonorthog"
    / "band-equivalence-versus-hopping-locality"
    / "run_development.py",
)
OUTPUT_DIRECTORY = COMPARISON_DIRECTORY / "analysis" / "development"


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
    requests = tuple(
        ShellScaleDecisionLandscapeRequest(
            locality_request=_load_definition(path, index),
            scale_sample_count=17,
        )
        for index, path in enumerate(FAMILY_DEFINITION_PATHS)
    )
    results = tuple(
        ShellScaleDecisionLandscapeCalculator(
            request=request,
            analyzer=BandEquivalenceLocalityAnalyzer(request=request.locality_request),
        ).execute()
        for request in requests
    )
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    artifacts: list[tuple[Path, str]] = []
    for request, result in zip(requests, results, strict=True):
        slug = result.family.to_wire().replace("_", "-")
        for path, record in (
            (OUTPUT_DIRECTORY / f"{slug}-shell-scale-request.json", request),
            (OUTPUT_DIRECTORY / f"{slug}-shell-scale-result.json", result),
        ):
            payload = record.to_json()
            path.write_text(payload, encoding="utf-8")
            artifacts.append(
                (path, hashlib.sha256(payload.encode("utf-8")).hexdigest())
            )
    plots = ShellScaleDecisionLandscapePlotWriter(
        request=ShellScaleDecisionLandscapePlotRequest(
            family_results=results,
            output_directory=OUTPUT_DIRECTORY,
        )
    ).execute()
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
    for path, digest in artifacts:
        print("decision-landscape-artifact", path, digest)
    for path in plots.paths:
        print(f"output={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
