"""Plot silicon-inspired development diagnostics from typed results."""

from dataclasses import replace
from pathlib import Path

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.analysis import (
    BandEquivalenceLocalityAnalyzer,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.constrained_bessel import (
    ConstrainedBesselGeometryEnum,
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
        replace(DEFINITION, construction_size=16, evaluation_size=33),
        replace(DEFINITION, construction_size=32, evaluation_size=65),
    )
    diagnostics = tuple(
        BandEquivalenceLocalityAnalyzer(request=request).execute()
        for request in requests
    )
    experiment = Path(__file__).resolve().parent
    result = BandEquivalenceLocalityPlotWriter(
        request=BandEquivalenceLocalityPlotRequest(
            mesh_results=diagnostics,
            output_directory=experiment / "analysis",
            title="Silicon-inspired family",
            constrained_geometry=ConstrainedBesselGeometryEnum.FCC,
            constrained_shell_cap=7,
            constrained_kernel_cap=9,
        )
    ).execute()
    for path in result.paths:
        print(f"output={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
