"""Tests for the direct rank-two composite-alignment analyzer and result."""

from dataclasses import replace

import pytest

from ksdft2effmass.periodic1d.rank2.band_alignment.composite.result import (
    Periodic1DCompositeBandAlignmentCalculationResult,
)
from ksdft2effmass.periodic1d.translations import (
    Periodic1DCyclicRepresentativeInventory,
    Periodic1DOrdinaryTranslationInventory,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic1DCompositeBandAlignmentAnalyzer:
    """Establish the complete aligned-frame, transform, and range inventory."""

    def test__execute__produces_the_frozen_complete_inventory(
        self,
        composite_result: Periodic1DCompositeBandAlignmentCalculationResult,
    ) -> None:
        assert composite_result.result_schema == (
            "ksdft2effmass.periodic1d-rank2-composite-band-alignment-result.v2"
        )
        assert composite_result.calculation_family == (
            "periodic1d-rank2-composite-band-alignment-locality"
        )
        assert composite_result.construction_parent_spectrum.magnitude.shape == (64, 4)
        assert composite_result.evaluation_parent_spectrum.magnitude.shape == (257, 4)
        assert len(composite_result.reference_frames) == 64
        assert len(composite_result.pointwise_rotations) == 64
        assert composite_result.diagnostics.pointwise_procrustes.selection_count == 64
        assert composite_result.diagnostics.global_procrustes.selection_count == 1
        assert tuple(item.channel for item in composite_result.transforms) == (
            "reference",
            "attacked",
            "pointwise",
        )
        assert tuple(item.maximum_range for item in composite_result.ranges) == (
            0,
            1,
            2,
            3,
            4,
            6,
            8,
        )

    def test__execute__retains_distinct_cyclic_and_ordinary_inventories(
        self,
        composite_result: Periodic1DCompositeBandAlignmentCalculationResult,
    ) -> None:
        transform = composite_result.transforms[0]

        assert type(transform.cyclic_representative_inventory) is (
            Periodic1DCyclicRepresentativeInventory
        )
        assert transform.cyclic_representative_inventory.representatives == tuple(
            range(-32, 32)
        )
        assert type(transform.ordinary_translation_inventory) is (
            Periodic1DOrdinaryTranslationInventory
        )
        assert transform.ordinary_translation_inventory.translations == tuple(
            range(-31, 32)
        )

    def test__execute__reproduces_named_finite_m2_channels(
        self,
        composite_result: Periodic1DCompositeBandAlignmentCalculationResult,
    ) -> None:
        diagnostics = composite_result.diagnostics
        range_four = composite_result.ranges[4]

        assert diagnostics.minimum_sampled_gap.magnitude == pytest.approx(
            1.0566461211497047,
            abs=2.0e-14,
        )
        assert diagnostics.attack_frame_maximum_frobenius_defect == pytest.approx(
            1.5056428951173264,
            abs=2.0e-14,
        )
        assert (
            diagnostics.attacked_operator_maximum_frobenius_defect.magnitude
            == pytest.approx(0.9972076810972811, abs=3.0e-14)
        )
        assert range_four.channels[
            0
        ].evaluation_total_spectral_maximum_error.magnitude == pytest.approx(
            2.486918337929467e-09, abs=2.0e-14
        )
        assert range_four.channels[
            1
        ].ordinary_omitted_block_l2_norm.magnitude == pytest.approx(
            0.008279656894486311, abs=2.0e-14
        )

    def test__execute__separates_conversion_interpolation_truncation_and_total(
        self,
        composite_result: Periodic1DCompositeBandAlignmentCalculationResult,
    ) -> None:
        attacked_transform = composite_result.transforms[1]
        attacked_range = composite_result.ranges[4].channels[1]

        assert attacked_transform.cyclic_conversion_representative == -32
        assert attacked_transform.ordinary_representatives == tuple(range(-31, 32))
        assert 0.0 <= attacked_transform.cyclic_conversion_power.magnitude < 1.0e-28
        assert (
            attacked_transform.evaluation_interpolation_spectral_maximum_error.magnitude
            == pytest.approx(1.9984014443252818e-15, abs=1.0e-15)
        )
        assert (
            attacked_range.evaluation_truncation_spectral_maximum_error.magnitude
            == pytest.approx(0.006429588433655875, abs=2.0e-14)
        )
        assert attacked_range.evaluation_total_spectral_maximum_error.magnitude == (
            pytest.approx(0.006429588433655653, abs=2.0e-14)
        )
        assert (
            attacked_range.evaluation_truncation_hamiltonian_maximum_error.magnitude
            == pytest.approx(0.009142140906351088, abs=2.0e-14)
        )
        assert attacked_range.evaluation_total_hamiltonian_maximum_error.magnitude == (
            pytest.approx(0.0091421409063511, abs=2.0e-14)
        )

    def test__json__round_trips_identical_canonical_bytes(
        self,
        composite_result: Periodic1DCompositeBandAlignmentCalculationResult,
    ) -> None:
        wire = composite_result.to_json()

        reconstructed = Periodic1DCompositeBandAlignmentCalculationResult.from_json(
            wire
        )

        assert reconstructed.to_json() == wire

    def test__init__rejects_obsolete_result_identity(
        self,
        composite_result: Periodic1DCompositeBandAlignmentCalculationResult,
    ) -> None:
        with pytest.raises(ValueError, match="rank-two v2 wire"):
            replace(
                composite_result,
                result_schema=(
                    "ksdft2effmass.periodic1d-rank2-composite-band-alignment-result.v1"
                ),
            )

    def test__init__rejects_reordered_transform_inventory(
        self,
        composite_result: Periodic1DCompositeBandAlignmentCalculationResult,
    ) -> None:
        with pytest.raises(ValueError, match="declared channel order"):
            replace(
                composite_result,
                transforms=tuple(reversed(composite_result.transforms)),
            )

    def test__init__rejects_range_inventory_not_correlated_with_configuration(
        self,
        composite_result: Periodic1DCompositeBandAlignmentCalculationResult,
    ) -> None:
        with pytest.raises(ValueError, match="configuration inventory"):
            replace(composite_result, ranges=composite_result.ranges[:-1])
