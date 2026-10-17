"""Run the bounded silicon-inspired development replication."""

from __future__ import annotations

import math
from pathlib import Path

from projectkoios.physkit.periodic.lattice import (
    BravaisLattice,
    DirectLattice3D,
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

SIMPLE_CUBIC_METRIC = DirectLatticeMetric(
    DirectLattice3D.from_lattice_parameters(
        a=math.sqrt(0.5),
        b=math.sqrt(0.5),
        c=math.sqrt(0.5),
        alpha_degrees=90.0,
        beta_degrees=90.0,
        gamma_degrees=90.0,
    )
)
FCC_METRIC = DirectLatticeMetric(BravaisLattice.cubic_face_centered().direct_lattice)
SIMPLE_CUBIC_BONDS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
FCC_BONDS = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (-1, 1, 0),
    (-1, 0, 1),
    (0, -1, 1),
)
MAXIMUM_AMPLITUDE = math.pi / (4.0 * math.sqrt(12.0))

DEFINITION = BandEquivalenceLocalityRequest(
    family=BandEquivalenceLocalityFamily.SILICON_INSPIRED,
    cases=(
        BandEquivalenceLocalityCase(
            name="matched-simple-cubic-bravais-control",
            dimension=3,
            parent_kind=ParentKind.HERMITIAN_BRAVAIS,
            gauge_normalization=GaugeNormalization.BOND_RMS,
            positive_bonds=SIMPLE_CUBIC_BONDS,
            direct_metric=SIMPLE_CUBIC_METRIC,
            shell_metric_scale=2.0,
        ),
        BandEquivalenceLocalityCase(
            name="fcc-bravais-control",
            dimension=3,
            parent_kind=ParentKind.HERMITIAN_BRAVAIS,
            gauge_normalization=GaugeNormalization.BOND_RMS,
            positive_bonds=FCC_BONDS,
            direct_metric=FCC_METRIC,
            shell_metric_scale=2.0,
        ),
        BandEquivalenceLocalityCase(
            name="silicon-inspired-diamond",
            dimension=3,
            parent_kind=ParentKind.BIPARTITE_INSPIRED,
            gauge_normalization=GaugeNormalization.BOND_RMS,
            positive_bonds=FCC_BONDS,
            direct_metric=FCC_METRIC,
            shell_metric_scale=2.0,
            basis_offsets=(
                (0.0, 0.0, 0.0),
                (1.0 / 4.0, 1.0 / 4.0, 1.0 / 4.0),
            ),
        ),
    ),
    construction_size=8,
    evaluation_size=17,
    evaluation_shift=1.0 / 3.0,
    parent_scales=(0.0, 1.0),
    amplitudes=(0.0, MAXIMUM_AMPLITUDE / 2.0, MAXIMUM_AMPLITUDE),
    band_tolerances=(1.0e-3, 1.0e-5),
    shell_cap=7,
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
