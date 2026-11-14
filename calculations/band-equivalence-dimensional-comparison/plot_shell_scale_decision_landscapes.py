"""Calculate and plot the eight sampled shell--scale decision landscapes."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
from typing import Protocol, cast

from ksdft2effmass.band_equivalence_hopping_locality.analysis import (
    Rank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.band_equivalence_hopping_locality.decision_landscape import (
    ShellScaleDecisionLandscapeCalculator,
    ShellScaleDecisionLandscapeRequest,
)
from ksdft2effmass.band_equivalence_hopping_locality.decision_landscape_plotting import (
    ShellScaleDecisionLandscapePlotRequest,
    ShellScaleDecisionLandscapePlotWriter,
)
from ksdft2effmass.band_equivalence_hopping_locality.definitions import (
    BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.sewing import (
    ReciprocalEndpointSewingInventory,
)


class _DevelopmentDefinitionModule(Protocol):
    """Expose the typed request owned by one family composition root."""

    DEFINITION: BandEquivalenceHoppingLocalityRequest
    ENDPOINT_SEWING: ReciprocalEndpointSewingInventory


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
    / "periodic2d_rank2_hexagonal"
    / "band_equivalence_hopping_locality"
    / "run_nominal_calculation.py",
    CALCULATIONS_DIRECTORY
    / "periodic3d_rank2_simple_cubic"
    / "band_equivalence_hopping_locality"
    / "run_nominal_calculation.py",
    CALCULATIONS_DIRECTORY
    / "periodic3d_rank2_fcc_diamond"
    / "band_equivalence_hopping_locality"
    / "run_nominal_calculation.py",
)
OUTPUT_DIRECTORY = CALCULATION_DIRECTORY / "analysis" / "development" / "generated"


def _load_composition(
    path: Path,
    index: int,
) -> tuple[BandEquivalenceHoppingLocalityRequest, ReciprocalEndpointSewingInventory]:
    """Load one explicit family request and reciprocal-axis sewing inventory."""
    specification = importlib.util.spec_from_file_location(
        f"shell_scale_decision_landscape_family_{index}",
        path,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"could not load family definition: {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    typed_module = cast(_DevelopmentDefinitionModule, module)
    definition = typed_module.DEFINITION
    endpoint_sewing = typed_module.ENDPOINT_SEWING
    if not isinstance(definition, BandEquivalenceHoppingLocalityRequest):
        raise TypeError(
            f"DEFINITION is not BandEquivalenceHoppingLocalityRequest: {path}"
        )
    if type(endpoint_sewing) is not ReciprocalEndpointSewingInventory:
        raise TypeError(f"ENDPOINT_SEWING has the wrong type: {path}")
    return definition, endpoint_sewing


def main() -> int:
    """Calculate all family landscapes and render separate and composite views."""
    compositions = tuple(
        _load_composition(path, index)
        for index, path in enumerate(FAMILY_DEFINITION_PATHS)
    )
    requests = tuple(
        ShellScaleDecisionLandscapeRequest(
            locality_request=definition,
            scale_sample_count=17,
        )
        for definition, _ in compositions
    )
    results = tuple(
        ShellScaleDecisionLandscapeCalculator(
            request=request,
            analyzer=Rank2BandEquivalenceHoppingLocalityAnalyzer(
                request=request.locality_request,
                endpoint_sewing=endpoint_sewing,
            ),
        ).execute()
        for request, (_, endpoint_sewing) in zip(
            requests,
            compositions,
            strict=True,
        )
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
            path.write_bytes(payload)
            artifacts.append((path, hashlib.sha256(payload).hexdigest()))
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
