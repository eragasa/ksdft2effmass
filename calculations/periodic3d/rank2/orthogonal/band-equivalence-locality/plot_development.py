"""Plot simple-cubic development diagnostics from typed results."""

from dataclasses import replace
from pathlib import Path

from run_development import DEFINITION

from ksdft2effmass.band_equivalence_hopping_locality.plotting import (
    BandEquivalenceHoppingLocalityPlotRequest,
    BandEquivalenceHoppingLocalityPlotWriter,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.analysis import (
    Periodic3DRank2BandEquivalenceHoppingLocalityAnalyzer,
)


def main() -> int:
    """Calculate typed diagnostics and write the development plot set."""
    requests = (
        DEFINITION,
        replace(DEFINITION, construction_size=16, evaluation_size=33),
        replace(DEFINITION, construction_size=32, evaluation_size=65),
    )
    diagnostics = tuple(
        Periodic3DRank2BandEquivalenceHoppingLocalityAnalyzer(request=request).execute()
        for request in requests
    )
    figures = Path(__file__).resolve().parent / "analysis" / "development" / "figures"
    result = BandEquivalenceHoppingLocalityPlotWriter(
        request=BandEquivalenceHoppingLocalityPlotRequest(
            mesh_results=diagnostics,
            output_directory=figures,
            title="Simple-cubic family",
        )
    ).execute()
    for path in result.paths:
        print(f"output={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
