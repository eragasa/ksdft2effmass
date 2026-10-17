"""Software verification for sampled synthetic-strain scan rendering."""

import math
from pathlib import Path

import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    SyntheticStrainCalculator,
    SyntheticStrainPath,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_response import (  # noqa: E501
    StrainResponseModel,
    StrainWitnessControl,
    calculate_strain_witness_scan,
    calculate_synthetic_strain_response,
)
from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.strain_scan_plotting import (  # noqa: E501
    SyntheticStrainScanPlotRequest,
    SyntheticStrainScanPlotWriter,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestSyntheticStrainScanPlotWriter:
    """Establish typed input checks and the two declared renderings."""

    def test_execute__complete_typed_scan__writes_pdf_and_png(
        self, tmp_path: Path
    ) -> None:
        fractions = (0.0, 0.5, 1.0)
        path = SyntheticStrainPath.RHOMBIC_2D
        witnesses = tuple(
            calculate_strain_witness_scan(
                path,
                control,
                4,
                fractions,
                math.pi / 8.0,
            )
            for control in StrainWitnessControl
        )
        geometry = SyntheticStrainCalculator().execute(
            path,
            4,
            fractions,
            math.pi / 8.0,
            (1.0e-3,),
        )
        frozen = calculate_synthetic_strain_response(
            path,
            StrainResponseModel.M1_FROZEN,
            4,
            5,
            1.0 / 3.0,
            fractions,
            math.pi / 8.0,
            0.0,
            (1.0e-3,),
        )
        radial = calculate_synthetic_strain_response(
            path,
            StrainResponseModel.M2_RADIAL,
            4,
            5,
            1.0 / 3.0,
            fractions,
            math.pi / 8.0,
            1.0,
            (1.0e-3,),
        )

        result = SyntheticStrainScanPlotWriter().execute(
            SyntheticStrainScanPlotRequest(
                witness_results=witnesses,
                geometry_result=geometry,
                frozen_response=frozen,
                radial_response=radial,
                output_directory=tmp_path,
                title="Synthetic strain scan",
            )
        )

        assert result.paths == (
            tmp_path / "strain-witness-locality-scan.pdf",
            tmp_path / "strain-witness-locality-scan.png",
        )
        assert all(
            output.is_file() and output.stat().st_size > 0 for output in result.paths
        )
