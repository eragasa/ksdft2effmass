"""Run bounded 3-D M1/M2 synthetic Bain-response controls."""

from __future__ import annotations

import math
from pathlib import Path

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (  # noqa: E501
    strain_response_plotting,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (  # noqa: E501
    SyntheticStrainPath,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_response import (  # noqa: E501
    StrainResponseModel,
    calculate_synthetic_strain_response,
)
from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.strain_schemas import (  # noqa: E501
    SyntheticStrainSchema,
    SyntheticStrainSchemaKind,
)
from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.strain_serialization import (  # noqa: E501
    SyntheticStrainResponseResultSerializer,
)

FRACTIONS = tuple(float(index) / 8.0 for index in range(9))
TOLERANCES = (1.0e-3, 1.0e-5)


def main() -> None:
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
    output = Path(__file__).resolve().parent / "analysis" / "response-development"
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
        print(path)


if __name__ == "__main__":
    main()
