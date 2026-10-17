"""Run the bounded graphene-inspired development replication."""

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
TRIANGULAR_METRIC = DirectLatticeMetric(
    DirectLattice2D(
        a1=np.array((1.0, 0.0), dtype=np.float64),
        a2=np.array((0.5, math.sqrt(3.0) / 2.0), dtype=np.float64),
    )
)
SQUARE_BONDS = ((1, 0), (0, 1))
TRIANGULAR_BONDS = ((1, 0), (0, 1), (1, -1))
MAXIMUM_AMPLITUDE = math.pi / (4.0 * math.sqrt(6.0))

DEFINITION = BandEquivalenceLocalityRequest(
    family=BandEquivalenceLocalityFamily.GRAPHENE_INSPIRED,
    cases=(
        BandEquivalenceLocalityCase(
            name="matched-square-bravais-control",
            dimension=2,
            parent_kind=ParentKind.HERMITIAN_BRAVAIS,
            gauge_normalization=GaugeNormalization.BOND_RMS,
            positive_bonds=SQUARE_BONDS,
            direct_metric=SQUARE_METRIC,
            shell_metric_scale=1.0,
        ),
        BandEquivalenceLocalityCase(
            name="triangular-bravais-control",
            dimension=2,
            parent_kind=ParentKind.HERMITIAN_BRAVAIS,
            gauge_normalization=GaugeNormalization.BOND_RMS,
            positive_bonds=TRIANGULAR_BONDS,
            direct_metric=TRIANGULAR_METRIC,
            shell_metric_scale=1.0,
        ),
        BandEquivalenceLocalityCase(
            name="graphene-inspired-honeycomb",
            dimension=2,
            parent_kind=ParentKind.BIPARTITE_INSPIRED,
            gauge_normalization=GaugeNormalization.BOND_RMS,
            positive_bonds=TRIANGULAR_BONDS,
            direct_metric=TRIANGULAR_METRIC,
            shell_metric_scale=1.0,
            basis_offsets=((0.0, 0.0), (1.0 / 3.0, 1.0 / 3.0)),
        ),
    ),
    construction_size=16,
    evaluation_size=33,
    evaluation_shift=1.0 / 3.0,
    parent_scales=(0.0, 1.0),
    amplitudes=(0.0, MAXIMUM_AMPLITUDE / 2.0, MAXIMUM_AMPLITUDE),
    band_tolerances=(1.0e-3, 1.0e-5),
    shell_cap=21,
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
