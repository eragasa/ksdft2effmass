"""Run bounded 3-D M1/M2 synthetic Bain-response controls."""

from __future__ import annotations

import math
import sys
from pathlib import Path

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    strain_response_plotting,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    SyntheticStrainPath,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_response import (
    StrainResponseModel,
    calculate_synthetic_strain_response,
)

_WORKFLOW_ROOT = (
    Path(__file__).resolve().parents[3] / "band-equivalence-dimensional-comparison"
)
sys.path.insert(0, str(_WORKFLOW_ROOT))

from band_equivalence_workflow.strain_schemas import (
    SyntheticStrainSchema,
    SyntheticStrainSchemaKind,
)
from band_equivalence_workflow.strain_serialization import (
    SyntheticStrainResponseResultSerializer,
)

FRACTIONS = tuple(float(index) / 8.0 for index in range(9))
TOLERANCES = (1.0e-3, 1.0e-5)


def main() -> int:
    """Write replaceable M1/M2 JSON and publication-style development plots."""
    frozen = calculate_synthetic_strain_response(
        SyntheticStrainPath.BAIN_3D,
        StrainResponseModel.M1_FROZEN,
        8,
        17,
        1.0 / 3.0,
        FRACTIONS,
        math.pi / 4.0,
        0.0,
        TOLERANCES,
    )
    radial = calculate_synthetic_strain_response(
        SyntheticStrainPath.BAIN_3D,
        StrainResponseModel.M2_RADIAL,
        8,
        17,
        1.0 / 3.0,
        FRACTIONS,
        math.pi / 4.0,
        1.0,
        TOLERANCES,
    )
    output = Path(__file__).resolve().parent / "analysis" / "development" / "response"
    output.mkdir(parents=True, exist_ok=True)
    serializer = SyntheticStrainResponseResultSerializer()
    for name, result, kind in (
        ("M1", frozen, SyntheticStrainSchemaKind.M1_RESULT),
        ("M2", radial, SyntheticStrainSchemaKind.M2_RESULT),
    ):
        artifact = serializer.execute(result)
        schema = SyntheticStrainSchema(kind)
        schema.validate(artifact.canonical_bytes())
        artifact.write_to(output / f"{name.lower()}-result.json")
        schema.write_to(output)
    for path in strain_response_plotting.write_strain_response_plots(
        frozen, radial, output, "3-D Bain path"
    ):
        print(f"output={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
