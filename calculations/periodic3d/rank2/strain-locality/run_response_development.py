"""Run bounded 3-D M1/M2 synthetic Bain-response controls."""

from __future__ import annotations

import math
from pathlib import Path

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    strain_response_plotting,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    SyntheticStrainPathEnum,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_response import (
    StrainResponseModelEnum,
    calculate_synthetic_strain_response,
)

FRACTIONS = tuple(float(index) / 8.0 for index in range(9))
TOLERANCES = (1.0e-3, 1.0e-5)


def main() -> int:
    """Write replaceable M1/M2 JSON and publication-style development plots."""
    frozen = calculate_synthetic_strain_response(
        SyntheticStrainPathEnum.BAIN_3D,
        StrainResponseModelEnum.M1_FROZEN,
        8,
        17,
        1.0 / 3.0,
        FRACTIONS,
        math.pi / 4.0,
        0.0,
        TOLERANCES,
    )
    radial = calculate_synthetic_strain_response(
        SyntheticStrainPathEnum.BAIN_3D,
        StrainResponseModelEnum.M2_RADIAL,
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
    for name, result in (("M1", frozen), ("M2", radial)):
        (output / f"{name.lower()}-result.json").write_bytes(result.to_json())
    for path in strain_response_plotting.write_strain_response_plots(
        frozen, radial, output, "3-D Bain path"
    ):
        print(f"output={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
