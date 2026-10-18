"""Plot silicon-inspired development diagnostics from typed results."""

from dataclasses import replace
from pathlib import Path

from run_development import DEFINITION

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.constrained_bessel import (  # noqa: E501
    ConstrainedBesselGeometry,
)
from ksdft2effmass.application.band_equivalence_locality import (
    BandEquivalenceLocalityResultConstructor,
)
from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.plotting import (
    BandEquivalenceLocalityPlotRequest,
    BandEquivalenceLocalityPlotWriter,
)


def main() -> int:
    """Calculate typed diagnostics and write the development plot set."""
    requests = (
        DEFINITION,
        replace(DEFINITION, construction_size=16, evaluation_size=33),
        replace(DEFINITION, construction_size=32, evaluation_size=65),
    )
    constructor = BandEquivalenceLocalityResultConstructor()
    diagnostics = tuple(
        constructor.execute(request).diagnostics for request in requests
    )
    experiment = Path(__file__).resolve().parent
    result = BandEquivalenceLocalityPlotWriter().execute(
        BandEquivalenceLocalityPlotRequest(
            mesh_results=diagnostics,
            output_directory=experiment / "analysis",
            title="Silicon-inspired family",
            constrained_geometry=ConstrainedBesselGeometry.FCC,
            constrained_shell_cap=7,
            constrained_kernel_cap=9,
        )
    )
    for path in result.paths:
        print(f"output={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
