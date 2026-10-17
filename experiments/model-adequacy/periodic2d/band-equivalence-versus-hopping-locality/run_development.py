"""Run the bounded square-lattice development replication."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    DirectLatticeMetric,
)

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    BandEquivalenceLocalityCase,
    BandEquivalenceLocalityFamily,
    BandEquivalenceLocalityRequest,
    GaugeNormalization,
    ParentKind,
)
from ksdft2effmass.application.band_equivalence_locality import (
    BandEquivalenceLocalityResult,
    BandEquivalenceLocalityResultConstructor,
    BandEquivalenceLocalityResultVerifier,
    BandEquivalenceLocalityVerificationRequest,
    BandEquivalenceLocalityVerificationResult,
)

SQUARE_METRIC = DirectLatticeMetric(
    DirectLattice2D(
        a1=np.array((1.0, 0.0), dtype=np.float64),
        a2=np.array((0.0, 1.0), dtype=np.float64),
    )
)

DEFINITION = BandEquivalenceLocalityRequest(
    family=BandEquivalenceLocalityFamily.SQUARE,
    cases=(
        BandEquivalenceLocalityCase(
            name="square-directed-parent",
            dimension=2,
            parent_kind=ParentKind.DIRECTED_AXIS,
            gauge_normalization=GaugeNormalization.AXIS_MAXIMUM,
            positive_bonds=((1, 0), (0, 1)),
            direct_metric=SQUARE_METRIC,
            shell_metric_scale=1.0,
        ),
    ),
    construction_size=16,
    evaluation_size=33,
    evaluation_shift=1.0 / 3.0,
    parent_scales=(0.0, 1.0),
    amplitudes=(0.0, math.pi / 8.0, math.pi / 4.0),
    band_tolerances=(1.0e-3, 1.0e-5),
    shell_cap=25,
)


def construct_artifacts(
    request: BandEquivalenceLocalityRequest,
) -> tuple[
    BandEquivalenceLocalityResult,
    BandEquivalenceLocalityVerificationResult,
]:
    """Construct one canonical result and its independent verification artifact."""
    result = BandEquivalenceLocalityResultConstructor().execute(request)
    verification = BandEquivalenceLocalityResultVerifier().execute(
        BandEquivalenceLocalityVerificationRequest(request, result)
    )
    return result, verification


def write_artifacts(
    output: Path,
    result: BandEquivalenceLocalityResult,
    verification: BandEquivalenceLocalityVerificationResult,
) -> None:
    """Write the three canonical replaceable development documents."""
    output.mkdir(parents=True, exist_ok=True)
    result.request_document.write_to(output / "development-input.json")
    result.document.write_to(output / "development-result.json")
    verification.document.write_to(output / "development-verification.json")


def main() -> None:
    """Calculate, independently verify, and write replaceable development records."""
    result, verification = construct_artifacts(DEFINITION)
    output = Path(__file__).resolve().parent / "analysis" / "development"
    write_artifacts(output, result, verification)
    print(
        f"{DEFINITION.family.value}: "
        f"verification passes={verification.diagnostics.passes}"
    )


if __name__ == "__main__":
    main()
