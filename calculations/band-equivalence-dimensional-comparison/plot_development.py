"""Plot cross-family development tolerance requirements without deciding acceptance."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Protocol, cast

from ksdft2effmass.band_equivalence_hopping_locality.analysis import (
    Rank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.band_equivalence_hopping_locality.definitions import (
    BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.band_equivalence_hopping_locality.plotting import (
    BandEquivalenceToleranceMapRequest,
    BandEquivalenceToleranceMapWriter,
)


class _DevelopmentDefinitionModule(Protocol):
    """Expose the typed request owned by one family composition root."""

    DEFINITION: BandEquivalenceHoppingLocalityRequest


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


def _load_definition(path: Path, index: int) -> BandEquivalenceHoppingLocalityRequest:
    """Load one explicit family request without making experiment roots packages."""
    specification = importlib.util.spec_from_file_location(
        f"band_equivalence_tolerance_family_{index}",
        path,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"could not load family definition: {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    typed_module = cast(_DevelopmentDefinitionModule, module)
    definition = typed_module.DEFINITION
    if type(definition) is not BandEquivalenceHoppingLocalityRequest:
        raise TypeError(
            f"DEFINITION is not a BandEquivalenceHoppingLocalityRequest: {path}"
        )
    return definition


def main() -> int:
    """Calculate typed development diagnostics and render the shared protocol map."""
    definitions = tuple(
        _load_definition(path, index)
        for index, path in enumerate(FAMILY_DEFINITION_PATHS)
    )
    diagnostics = tuple(
        Rank2BandEquivalenceHoppingLocalityAnalyzer(request=definition).execute()
        for definition in definitions
    )
    result = BandEquivalenceToleranceMapWriter(
        request=BandEquivalenceToleranceMapRequest(
            family_results=diagnostics,
            output_directory=OUTPUT_DIRECTORY,
            title=(
                "Software-verified threshold requirements; "
                "scientific acceptance remains open"
            ),
        )
    ).execute()
    for path in result.paths:
        print(f"output={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
