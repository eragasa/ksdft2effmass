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
            available_radii = tuple(
                radius
                for point in geometry.points
                if (radius := point.first_passing_radius[tolerance_index]) is not None
            )
            available_block_counts = tuple(
                count
                for point in geometry.points
                if (count := point.first_passing_blocks[tolerance_index]) is not None
            )
            assert envelope.maximum_physical_radius == max(available_radii)
            assert envelope.maximum_retained_blocks == max(available_block_counts)
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
        response_results = {
            StrainWitnessControl.FROZEN_PARENT: frozen,
            StrainWitnessControl.RADIAL_RESPONSE: radial,
        }
        qualification_by_control = {
            item.control: item for item in result.qualifications
        }
        approximation_by_control = {
            item.control: item for item in result.approximations
        }
        mechanism_by_control = {item.control: item for item in result.mechanisms}
        assert set(qualification_by_control) == set(StrainWitnessControl) - {
            StrainWitnessControl.GEOMETRY_ONLY
        }
        assert set(approximation_by_control) == set(qualification_by_control)
        assert set(mechanism_by_control) == set(qualification_by_control)
        for control, response_result in response_results.items():
            qualification = qualification_by_control[control]
            assert qualification.external_isolation_gap.value == min(
                point.minimum_sampled_external_isolation_gap
                for point in response_result.points
            )
            assert qualification.seed_overlap.value == min(
                point.minimum_seed_overlap for point in response_result.points
            )
            assert qualification.frame_overlap_singular_value.value == min(
                point.minimum_frame_overlap_singular_value
                for point in response_result.points
            )
            assert qualification.pointwise_frame_alignment_residual.value == max(
                point.maximum_pointwise_frame_alignment_residual
                for point in response_result.points
            )
            approximation = approximation_by_control[control]
            assert approximation.interpolation.sample_count == len(fractions)
            assert approximation.interpolation.maximum_hamiltonian.value == max(
                point.interpolation.maximum_hamiltonian
                for point in response_result.points
            )
            assert approximation.delta_interpolation.maximum_band.value == max(
                point.delta_interpolation.maximum_band
                for point in response_result.points
            )
            assert len(approximation.cutoffs) == len(tolerances)
            for tolerance_index, cutoff in enumerate(approximation.cutoffs):
                assert cutoff.tail_tolerance == tolerances[tolerance_index]
                assert cutoff.omitted_power.value == max(
                    point.cutoffs[tolerance_index].omitted_power
                    for point in response_result.points
                )
                assert cutoff.delta_omitted_power.value == max(
                    point.cutoffs[tolerance_index].delta_omitted_power
                    for point in response_result.points
                )
            mechanism = mechanism_by_control[control]
            assert mechanism.hopping_response_minimum.value == min(
                point.minimum_hopping_response for point in response_result.points
            )
            assert mechanism.hopping_response_maximum.value == max(
                point.maximum_hopping_response for point in response_result.points
            )
            assert mechanism.traceless_component_maximum.value == max(
                point.maximum_traceless_strain_component
                for point in response_result.points
            )
            assert mechanism.delta_offsite_power_maximum.value == max(
                point.delta_offsite_power for point in response_result.points
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
