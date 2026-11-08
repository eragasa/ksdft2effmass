"""Run the bounded simple-cubic nominal calculation."""

from __future__ import annotations

import math
from pathlib import Path

from ksdft2effmass.band_equivalence_hopping_locality.calculation import (
    BandEquivalenceHoppingLocalityVerifier,
)
from ksdft2effmass.band_equivalence_hopping_locality.definitions import (
    FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
    BandEquivalenceHoppingLocalityCase,
    BandEquivalenceHoppingLocalityFamilyEnum,
    GaugeNormalizationEnum,
    ParentEnum,
)
from ksdft2effmass.band_equivalence_hopping_locality.records import (
    BandEquivalenceHoppingLocalityVerificationDiagnostics,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.analysis import (
    Periodic3DRank2BandEquivalenceHoppingLocalityAnalysis,
    Periodic3DRank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.request import (
    Periodic3DRank2BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.result import (
    Periodic3DRank2BandEquivalenceHoppingLocalityAnalysisRecorder,
    Periodic3DRank2BandEquivalenceHoppingLocalityCalculationResult,
)
from ksdft2effmass.sewing import (
    IdentityReciprocalSewing,
    ReciprocalEndpointSewingInventory,
)
from projectkoios.physkit.periodic.lattice import (
    BravaisLattice,
    DirectLatticeMetric,
)

IDENTITY_RECIPROCAL_SEWING = IdentityReciprocalSewing(ambient_dimension=4)
ENDPOINT_SEWING = ReciprocalEndpointSewingInventory(
    positive_axis_maps=(
        IDENTITY_RECIPROCAL_SEWING.endpoint_map,
        IDENTITY_RECIPROCAL_SEWING.endpoint_map,
        IDENTITY_RECIPROCAL_SEWING.endpoint_map,
    )
)
SIMPLE_CUBIC_METRIC = DirectLatticeMetric(
    BravaisLattice.cubic_primitive().direct_lattice
)

DEFINITION = Periodic3DRank2BandEquivalenceHoppingLocalityRequest(
    family=BandEquivalenceHoppingLocalityFamilyEnum.SIMPLE_CUBIC,
    synthetic_model=FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
    cases=(
        BandEquivalenceHoppingLocalityCase(
            name="simple-cubic-directed-parent",
            dimension=3,
            parent_kind=ParentEnum.DIRECTED_AXIS,
            gauge_normalization=GaugeNormalizationEnum.AXIS_MAXIMUM,
            positive_bonds=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            direct_metric=SIMPLE_CUBIC_METRIC,
            shell_metric_scale=1.0,
        ),
    ),
    construction_size=8,
    evaluation_size=17,
    evaluation_shift=1.0 / 3.0,
    parent_scales=(0.0, 1.0),
    amplitudes=(0.0, math.pi / 8.0, math.pi / 4.0),
    band_tolerances=(1.0e-3, 1.0e-5),
    shell_cap=9,
)


def construct_artifacts(
    request: Periodic3DRank2BandEquivalenceHoppingLocalityRequest,
) -> tuple[
    Periodic3DRank2BandEquivalenceHoppingLocalityAnalysis,
    Periodic3DRank2BandEquivalenceHoppingLocalityCalculationResult,
    BandEquivalenceHoppingLocalityVerificationDiagnostics,
]:
    """Calculate and independently verify one typed result."""
    analysis = Periodic3DRank2BandEquivalenceHoppingLocalityAnalyzer(
        request=request,
        endpoint_sewing=ENDPOINT_SEWING,
    ).execute()
    result = Periodic3DRank2BandEquivalenceHoppingLocalityAnalysisRecorder(
        analysis
    ).result()
    verification = BandEquivalenceHoppingLocalityVerifier(
        request=request,
        result=result.diagnostics,
    ).execute()
    return analysis, result, verification


def write_artifacts(
    output: Path,
    result: Periodic3DRank2BandEquivalenceHoppingLocalityCalculationResult,
    verification: BandEquivalenceHoppingLocalityVerificationDiagnostics,
) -> None:
    """Write canonical typed development records."""
    output.mkdir(parents=True, exist_ok=True)
    (output / "development-input.json").write_bytes(result.request.to_json())
    (output / "development-result.json").write_bytes(result.to_json())
    (output / "development-verification.json").write_bytes(verification.to_json())


def main() -> int:
    """Calculate, verify, and write replaceable nominal records."""
    _, result, verification = construct_artifacts(DEFINITION)
    if not verification.passes:
        raise RuntimeError("independent development verification failed")
    output = (
        Path(__file__).resolve().parent
        / "simulations"
        / "replaceable"
        / "results"
        / "nominal"
    )
    write_artifacts(output, result, verification)
    print(
        f"family={DEFINITION.family.to_wire()} lifecycle=development "
        f"verification=pass output={output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
