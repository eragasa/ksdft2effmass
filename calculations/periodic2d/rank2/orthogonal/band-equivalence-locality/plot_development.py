"""Plot square-lattice development diagnostics from typed results."""

from dataclasses import replace
from pathlib import Path

from run_development import DEFINITION, ENDPOINT_SEWING

from ksdft2effmass.band_equivalence_hopping_locality.plotting import (
    BandEquivalenceHoppingLocalityPlotRequest,
    BandEquivalenceHoppingLocalityPlotWriter,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.analysis import (
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer,
)


def main() -> int:
    """Calculate typed diagnostics and write the development plot set."""
    requests = (
        DEFINITION,
        replace(DEFINITION, construction_size=32, evaluation_size=65),
        replace(DEFINITION, construction_size=64, evaluation_size=129),
    )
    diagnostics = tuple(
        Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer(
            request=request,
            endpoint_sewing=ENDPOINT_SEWING,
        ).execute()
        for request in requests
    )
    figures = Path(__file__).resolve().parent / "analysis" / "development" / "figures"
    result = BandEquivalenceHoppingLocalityPlotWriter(
        request=BandEquivalenceHoppingLocalityPlotRequest(
            mesh_results=diagnostics,
            output_directory=figures,
            title="Square-lattice family",
        )
    ).execute()
    for path in result.paths:
        print(f"output={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
