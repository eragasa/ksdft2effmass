"""Plot square-lattice development diagnostics from typed results."""

from dataclasses import replace
from pathlib import Path

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.analysis import (
    BandEquivalenceLocalityAnalyzer,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.plotting import (
    BandEquivalenceLocalityPlotRequest,
    BandEquivalenceLocalityPlotWriter,
)
from run_development import DEFINITION


def main() -> int:
    """Calculate typed diagnostics and write the development plot set."""
    requests = (
        DEFINITION,
        replace(DEFINITION, construction_size=32, evaluation_size=65),
        replace(DEFINITION, construction_size=64, evaluation_size=129),
    )
    diagnostics = tuple(
        BandEquivalenceLocalityAnalyzer(request=request).execute()
        for request in requests
    )
    figures = Path(__file__).resolve().parent / "analysis" / "development" / "figures"
    result = BandEquivalenceLocalityPlotWriter(
        request=BandEquivalenceLocalityPlotRequest(
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
