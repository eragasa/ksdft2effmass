"""Plot cross-family development tolerance requirements without deciding acceptance."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Protocol, cast

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    BandEquivalenceLocalityRequest,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.analysis import (
    BandEquivalenceLocalityAnalyzer,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.plotting import (
    BandEquivalenceToleranceMapRequest,
    BandEquivalenceToleranceMapWriter,
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
    if type(definition) is not BandEquivalenceLocalityRequest:
        raise TypeError(f"DEFINITION is not a BandEquivalenceLocalityRequest: {path}")
    return definition


def main() -> int:
    """Calculate typed development diagnostics and render the shared protocol map."""
    definitions = tuple(
        _load_definition(path, index)
        for index, path in enumerate(FAMILY_DEFINITION_PATHS)
    )
    diagnostics = tuple(
        BandEquivalenceLocalityAnalyzer(request=definition).execute()
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
