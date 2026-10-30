"""Run the bounded simple-cubic development replication."""

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
    DirectLatticeMetric,
)

SIMPLE_CUBIC_METRIC = DirectLatticeMetric(
    BravaisLattice.cubic_primitive().direct_lattice
)

DEFINITION = BandEquivalenceLocalityRequest(
    family=BandEquivalenceLocalityFamilyEnum.SIMPLE_CUBIC,
    synthetic_model=FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
    cases=(
        BandEquivalenceLocalityCase(
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
    request: BandEquivalenceLocalityRequest,
) -> tuple[
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
    return result, verification


def write_artifacts(
    output: Path,
    result: BandEquivalenceLocalityCalculationResult,
    verification: BandEquivalenceLocalityVerificationDiagnostics,
) -> None:
    """Write canonical typed development records."""
    output.mkdir(parents=True, exist_ok=True)
    (output / "development-input.json").write_text(
        result.request.to_json(), encoding="utf-8"
    )
    (output / "development-result.json").write_text(result.to_json(), encoding="utf-8")
    (output / "development-verification.json").write_text(
        verification.to_json(), encoding="utf-8"
    )


def main() -> int:
    """Calculate, verify, and write replaceable development records."""
    result, verification = construct_artifacts(DEFINITION)
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
