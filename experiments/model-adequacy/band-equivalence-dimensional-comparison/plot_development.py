"""Plot cross-family development tolerance requirements without deciding acceptance."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Protocol, cast

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    BandEquivalenceLocalityRequest,
)
from ksdft2effmass.application.band_equivalence_locality import (
    BandEquivalenceLocalityResultConstructor,
)
from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.plotting import (
    BandEquivalenceToleranceMapRequest,
    BandEquivalenceToleranceMapWriter,
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
    constructor = BandEquivalenceLocalityResultConstructor()
    diagnostics = tuple(
        constructor.execute(definition).diagnostics for definition in definitions
    )
    result = BandEquivalenceToleranceMapWriter().execute(
        BandEquivalenceToleranceMapRequest(
            family_results=diagnostics,
            output_directory=OUTPUT_DIRECTORY,
            title=(
                "Software-verified threshold requirements; "
                "scientific acceptance remains open"
            ),
        )
    )
    for path in result.paths:
        print(f"output={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
