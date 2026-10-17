"""Software verification for sampled synthetic-strain scan summaries."""

import math
from dataclasses import replace

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
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_scan import (  # noqa: E501
    SyntheticStrainScanAssessor,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestSyntheticStrainScanAssessor:
    """Establish sampled envelope identities without scientific acceptance."""

    def test_execute__common_scan_grid__summarizes_separate_envelopes(self) -> None:
        path = SyntheticStrainPath.RHOMBIC_2D
        fractions = (0.0, 0.5, 1.0)
        tolerances = (1.0e-1, 1.0e-3)
        geometry = SyntheticStrainCalculator().execute(
            path,
            8,
            fractions,
            math.pi / 4.0,
            tolerances,
        )
        witnesses = tuple(
            calculate_strain_witness_scan(
                path,
                control,
                8,
                fractions,
                math.pi / 4.0,
            )
            for control in StrainWitnessControl
        )
        frozen = calculate_synthetic_strain_response(
            path,
            StrainResponseModel.M1_FROZEN,
            8,
            9,
            1.0 / 3.0,
            fractions,
            math.pi / 4.0,
            0.0,
            tolerances,
        )
        radial = calculate_synthetic_strain_response(
            path,
            StrainResponseModel.M2_RADIAL,
            8,
            9,
            1.0 / 3.0,
            fractions,
            math.pi / 4.0,
            1.0,
            tolerances,
        )

        result = SyntheticStrainScanAssessor().execute(
            geometry,
            witnesses,
            frozen,
            radial,
        )

        assert result.base_sample_count == 3
        assert result.maximum_volume_defect < 5.0e-16
        assert result.maximum_direct_band_defect < 2.0e-15
        assert {item.control for item in result.witness_requirements} == set(
            StrainWitnessControl
        )
        for envelope in result.locality:
            tolerance_index = tolerances.index(envelope.tail_tolerance)
            assert envelope.maximum_physical_radius == max(
                point.first_passing_radius[tolerance_index]
                for point in geometry.points
                if point.first_passing_radius[tolerance_index] is not None
            )
            assert envelope.maximum_retained_blocks == max(
                point.first_passing_blocks[tolerance_index]
                for point in geometry.points
                if point.first_passing_blocks[tolerance_index] is not None
            )
        response_by_control = {item.control: item for item in result.responses}
        assert (
            response_by_control[
                StrainWitnessControl.FROZEN_PARENT
            ].maximum_aligned_hamiltonian_defect
            < 2.0e-14
        )
        assert (
            response_by_control[
                StrainWitnessControl.RADIAL_RESPONSE
            ].maximum_aligned_hamiltonian_defect
            > 1.0e-3
        )
        assert result.status == "sampled-development-summary-not-continuum-certificate"

        mismatched = (replace(witnesses[0], points=witnesses[0].points[:-1]),) + (
            witnesses[1:]
        )
        with pytest.raises(ValueError, match="one path and strain grid"):
            SyntheticStrainScanAssessor().execute(
                geometry,
                mismatched,
                frozen,
                radial,
            )
