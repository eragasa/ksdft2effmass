"""Run bounded 2-D M1/M2 synthetic strain-response controls."""

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
    """Write replaceable typed M1/M2 results and development plots."""
    frozen = calculate_synthetic_strain_response(
        SyntheticStrainPathEnum.RHOMBIC_2D,
        StrainResponseModelEnum.M1_FROZEN,
        16,
        33,
        1.0 / 3.0,
        FRACTIONS,
        math.pi / 4.0,
        0.0,
        TOLERANCES,
    )
    radial = calculate_synthetic_strain_response(
        SyntheticStrainPathEnum.RHOMBIC_2D,
        StrainResponseModelEnum.M2_RADIAL,
        16,
        33,
        1.0 / 3.0,
        FRACTIONS,
        math.pi / 4.0,
        1.0,
        TOLERANCES,
    )
    output = Path(__file__).resolve().parent / "analysis" / "response-development"
    output.mkdir(parents=True, exist_ok=True)
    typed_paths = (output / "m1-result.json", output / "m2-result.json")
    for path, result in zip(typed_paths, (frozen, radial), strict=True):
        path.write_bytes(result.to_json())
    for path in (
        *typed_paths,
        *strain_response_plotting.write_strain_response_plots(
            frozen, radial, output, "2-D rhombic path"
        ),
    ):
        print(f"output={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
