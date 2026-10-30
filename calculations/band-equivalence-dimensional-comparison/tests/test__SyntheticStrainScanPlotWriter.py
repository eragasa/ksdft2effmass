"""Software verification for sampled synthetic-strain scan rendering."""

import math
from pathlib import Path

import pytest
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    SyntheticStrainCalculator,
    SyntheticStrainPathEnum,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_response import (
    StrainResponseModelEnum,
    StrainWitnessControlEnum,
    calculate_strain_witness_scan,
    calculate_synthetic_strain_response,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_scan_plotting import (
    SyntheticStrainScanPlotRequest,
    SyntheticStrainScanPlotWriter,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestSyntheticStrainScanPlotWriter:
    """Establish typed input checks and the declared renderings."""

    def test_execute__complete_typed_scan__writes_pdf_and_png(
        self, tmp_path: Path
    ) -> None:
        fractions = (0.0, 0.5, 1.0)
        path = SyntheticStrainPathEnum.RHOMBIC_2D
        witnesses = tuple(
            calculate_strain_witness_scan(
                path,
                control,
                4,
                fractions,
                math.pi / 8.0,
            )
            for control in StrainWitnessControlEnum
        )
        geometry = SyntheticStrainCalculator(
            path=path,
            construction_size=4,
            strain_fractions=fractions,
            maximum_rotation_amplitude=math.pi / 8.0,
            tail_tolerances=(1.0e-3,),
        ).execute()
        frozen = calculate_synthetic_strain_response(
            path,
            StrainResponseModelEnum.M1_FROZEN,
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
            StrainResponseModelEnum.M2_RADIAL,
            4,
            5,
            1.0 / 3.0,
            fractions,
            math.pi / 8.0,
            1.0,
            (1.0e-3,),
        )

        result = SyntheticStrainScanPlotWriter(
            request=SyntheticStrainScanPlotRequest(
                witness_results=witnesses,
                geometry_result=geometry,
                frozen_response=frozen,
                radial_response=radial,
                output_directory=tmp_path,
                title="Synthetic strain scan",
            )
        ).execute()

        assert result.paths == (
            tmp_path / "strain-witness-locality-scan.pdf",
            tmp_path / "strain-witness-locality-scan.png",
            tmp_path / "strain-qualification-response-scan.pdf",
            tmp_path / "strain-qualification-response-scan.png",
        )
        assert all(
            output.is_file() and output.stat().st_size > 0 for output in result.paths
        )
