"""Run the bounded silicon-inspired development replication."""

from __future__ import annotations

import math
from pathlib import Path

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    BandEquivalenceLocalityCase,
    BandEquivalenceLocalityFamilyEnum,
    BandEquivalenceLocalityRequest,
    GaugeNormalizationEnum,
    ParentEnum,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.analysis import (
    BandEquivalenceLocalityAnalysis,
    BandEquivalenceLocalityAnalyzer,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.calculation import (
    BandEquivalenceLocalityVerifier,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.definitions import (
    FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.records import (
    BandEquivalenceLocalityVerificationDiagnostics,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.result import (
    BandEquivalenceLocalityAnalysisRecorder,
    BandEquivalenceLocalityCalculationResult,
)
from projectkoios.physkit.periodic.lattice import (
    BravaisLattice,
    DirectLattice3D,
    DirectLatticeMetric,
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
    family=BandEquivalenceLocalityFamilyEnum.SILICON_INSPIRED,
    synthetic_model=FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
    cases=(
        BandEquivalenceLocalityCase(
            name="matched-simple-cubic-bravais-control",
            dimension=3,
            parent_kind=ParentEnum.HERMITIAN_BRAVAIS,
            gauge_normalization=GaugeNormalizationEnum.BOND_RMS,
            positive_bonds=SIMPLE_CUBIC_BONDS,
            direct_metric=SIMPLE_CUBIC_METRIC,
            shell_metric_scale=2.0,
        ),
        BandEquivalenceLocalityCase(
            name="fcc-bravais-control",
            dimension=3,
            parent_kind=ParentEnum.HERMITIAN_BRAVAIS,
            gauge_normalization=GaugeNormalizationEnum.BOND_RMS,
            positive_bonds=FCC_BONDS,
            direct_metric=FCC_METRIC,
            shell_metric_scale=2.0,
        ),
        BandEquivalenceLocalityCase(
            name="silicon-inspired-diamond",
            dimension=3,
            parent_kind=ParentEnum.BIPARTITE_INSPIRED,
            gauge_normalization=GaugeNormalizationEnum.BOND_RMS,
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
    BandEquivalenceLocalityAnalysis,
    BandEquivalenceLocalityCalculationResult,
    BandEquivalenceLocalityVerificationDiagnostics,
]:
    """Calculate and independently verify one typed result."""
    analysis = BandEquivalenceLocalityAnalyzer(request=request).execute()
    result = BandEquivalenceLocalityAnalysisRecorder(analysis).result()
    verification = BandEquivalenceLocalityVerifier(
        request=request,
        result=result.diagnostics,
    ).execute()
    return analysis, result, verification


def write_artifacts(
    output: Path,
    result: BandEquivalenceLocalityCalculationResult,
    verification: BandEquivalenceLocalityVerificationDiagnostics,
) -> None:
    """Write canonical typed development records."""
    output.mkdir(parents=True, exist_ok=True)
    (output / "development-input.json").write_bytes(result.request.to_json())
    (output / "development-result.json").write_bytes(result.to_json())
    (output / "development-verification.json").write_bytes(verification.to_json())


def main() -> int:
    """Calculate, verify, and write replaceable development records."""
    _, result, verification = construct_artifacts(DEFINITION)
    if not verification.passes:
        raise RuntimeError("independent development verification failed")
    output = (
        Path(__file__).resolve().parent
        / "simulations"
        / "development"
        / "results"
        / "development"
    )
    write_artifacts(output, result, verification)
    print(
        f"family={DEFINITION.family.to_wire()} lifecycle=development "
        f"verification=pass output={output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
