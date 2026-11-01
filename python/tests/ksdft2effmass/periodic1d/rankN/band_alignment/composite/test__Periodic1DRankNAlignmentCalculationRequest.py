"""Tests for higher-rank calculation controls and request bytes."""

from dataclasses import replace

import pytest

from ksdft2effmass.periodic1d.rankN.band_alignment.calculation import (
    Periodic1DRankNAlignmentCalculationControls,
    Periodic1DRankNAlignmentCalculationRequest,
)

CalculationRequest = Periodic1DRankNAlignmentCalculationRequest

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNAlignmentCalculationRequest:
    """Establish immutable controls, complete identity binding, and canonical bytes."""

    def test__calculation_request__round_trips_canonical_bytes(
        self,
        higher_rank_calculation_request: CalculationRequest,
    ) -> None:
        wire = higher_rank_calculation_request.to_json()

        reconstructed = Periodic1DRankNAlignmentCalculationRequest.from_json(wire)

        assert reconstructed == higher_rank_calculation_request
        assert reconstructed.to_json() == wire
        assert reconstructed.case_identity == "r03-L01"
        assert reconstructed.controls.support_radii == (0, 1, 2, 4, 8, 16, 32, 64, 128)
        diagnostics = reconstructed.controls.hopping_diagnostic_range_inventory
        supports = reconstructed.controls.support_range_inventory
        assert diagnostics.maximum_ranges == reconstructed.controls.support_radii
        assert supports.maximum_ranges == diagnostics.maximum_ranges
        assert supports.ranges == diagnostics.ranges
        assert reconstructed.transport_request(1025).construction_mesh_size == 1025

    def test__calculation_controls__reject_tampered_support_or_tolerance(self) -> None:
        controls = Periodic1DRankNAlignmentCalculationControls.frozen()

        with pytest.raises(ValueError, match="support_radii"):
            replace(controls, support_radii=(0, 1, 2))
        with pytest.raises(ValueError, match="frozen protocol"):
            replace(controls, final_interpolation_operator_tolerance=2.0e-9)

    def test__calculation_request__rejects_missing_physical_identity(
        self,
        higher_rank_calculation_request: CalculationRequest,
    ) -> None:
        with pytest.raises(ValueError, match="energy_reference_identifier"):
            replace(higher_rank_calculation_request, energy_reference_identifier="")
