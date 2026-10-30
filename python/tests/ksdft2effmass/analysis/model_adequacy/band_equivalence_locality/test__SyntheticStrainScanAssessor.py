"""Software verification for sampled synthetic-strain scan summaries."""

import math
from dataclasses import replace

import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    SyntheticStrainCalculator,
    SyntheticStrainPathEnum,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_response import (  # noqa: E501
    StrainResponseModelEnum,
    StrainWitnessControlEnum,
    calculate_strain_witness_scan,
    calculate_synthetic_strain_response,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_scan import (  # noqa: E501
    SyntheticStrainScanAssessor,
    SyntheticStrainScanRequest,
)

pytestmark = pytest.mark.unit


class TestSyntheticStrainScanAssessor:
    """Establish sampled envelope identities without scientific acceptance."""

    def test_request__canonical_typed_wire__round_trips(self) -> None:
        request = SyntheticStrainScanRequest(
            path=SyntheticStrainPathEnum.RHOMBIC_2D,
            strain_fractions=(0.0, 0.5, 1.0),
            geometry_construction_size=8,
            witness_construction_size=8,
            response_construction_size=8,
            response_evaluation_size=9,
            response_evaluation_shift=1.0 / 3.0,
            maximum_rotation_amplitude=math.pi / 4.0,
            radial_decay_beta=1.0,
            tail_tolerances=(1.0e-2, 1.0e-3),
            maximum_transition_refinement_depth=5,
        )

        wire = request.to_json()
        assert SyntheticStrainScanRequest.from_json(wire).to_json() == wire
        assert SyntheticStrainScanRequest.from_json(wire) == request

    def test_execute__common_scan_grid__summarizes_separate_envelopes(self) -> None:
        path = SyntheticStrainPathEnum.RHOMBIC_2D
        fractions = (0.0, 0.5, 1.0)
        tolerances = (1.0e-1, 1.0e-3)
        geometry = SyntheticStrainCalculator(
            path=path,
            construction_size=8,
            strain_fractions=fractions,
            maximum_rotation_amplitude=math.pi / 4.0,
            tail_tolerances=tolerances,
        ).execute()
        witnesses = tuple(
            calculate_strain_witness_scan(
                path,
                control,
                8,
                fractions,
                math.pi / 4.0,
            )
            for control in StrainWitnessControlEnum
        )
        frozen = calculate_synthetic_strain_response(
            path,
            StrainResponseModelEnum.M1_FROZEN,
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
            StrainResponseModelEnum.M2_RADIAL,
            8,
            9,
            1.0 / 3.0,
            fractions,
            math.pi / 4.0,
            1.0,
            tolerances,
        )

        result = SyntheticStrainScanAssessor(
            geometry_result=geometry,
            witness_results=witnesses,
            frozen_response=frozen,
            radial_response=radial,
        ).execute()

        wire = result.to_json()
        assert type(result).from_json(wire).to_json() == wire
        assert type(result).from_json(wire) == result
        assert result.base_sample_count == 3
        assert result.maximum_volume_defect < 5.0e-16
        assert result.maximum_direct_band_defect < 2.0e-15
        assert {item.control for item in result.witness_requirements} == set(
            StrainWitnessControlEnum
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
                StrainWitnessControlEnum.FROZEN_PARENT
            ].maximum_aligned_hamiltonian_defect
            < 2.0e-14
        )
        assert (
            response_by_control[
                StrainWitnessControlEnum.RADIAL_RESPONSE
            ].maximum_aligned_hamiltonian_defect
            > 1.0e-3
        )
        response_results = {
            StrainWitnessControlEnum.FROZEN_PARENT: frozen,
            StrainWitnessControlEnum.RADIAL_RESPONSE: radial,
        }
        qualification_by_control = {
            item.control: item for item in result.qualifications
        }
        approximation_by_control = {
            item.control: item for item in result.approximations
        }
        mechanism_by_control = {item.control: item for item in result.mechanisms}
        assert set(qualification_by_control) == set(StrainWitnessControlEnum) - {
            StrainWitnessControlEnum.GEOMETRY_ONLY
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
            SyntheticStrainScanAssessor(
                geometry_result=geometry,
                witness_results=mismatched,
                frozen_response=frozen,
                radial_response=radial,
            ).execute()
