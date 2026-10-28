"""Tests for the direct Fourier-locality analyzer."""

from dataclasses import replace

import numpy as np
import pytest

from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityAnalyzer,
    Periodic1DFourierLocalityCalculationResult,
    Periodic1DFourierLocalityConfiguration,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic1DFourierLocalityAnalyzer:
    """Establish pure typed calculation on a reduced finite control."""

    @staticmethod
    def configuration() -> Periodic1DFourierLocalityConfiguration:
        return Periodic1DFourierLocalityConfiguration(
            parent_identity=(
                "ksdft2effmass.periodic1d.controlled-four-state-parent.v1"
            ),
            onsite_numerators=(
                (-120, 6, 0, 0),
                (6, -35, 0, 0),
                (0, 0, 100, 4),
                (0, 0, 4, 175),
            ),
            positive_hopping_numerators=(
                (15, 0, 12, 0),
                (0, -10, 0, 10),
                (0, 0, 5, 0),
                (0, 0, 0, -4),
            ),
            coefficient_denominator=100,
            construction_mesh_sizes=(4, 8),
            production_construction_size=8,
            evaluation_size=3,
            evaluation_shift_numerator=1,
            evaluation_shift_denominator=3,
            maximum_ranges=(0, 1),
            sampled_gap_threshold=0.25,
            energy_absolute_tolerance=1.0e-12,
            relative_tolerance=1.0e-12,
            squared_energy_absolute_tolerance=1.0e-12,
            dimensionless_absolute_tolerance=1.0e-12,
            refinement_tolerance=1.0e-10,
            application_threshold=1.0e-8,
        )

    def test__execute__returns_canonical_correlated_result(self) -> None:
        result = Periodic1DFourierLocalityAnalyzer().execute(self.configuration())

        reconstructed = Periodic1DFourierLocalityCalculationResult.from_json(
            result.to_json()
        )

        assert tuple(mesh.construction_size for mesh in result.meshes) == (4, 8)
        assert tuple(item.maximum_range for item in result.meshes[-1].ranges) == (
            0,
            1,
        )
        assert result.minimum_sampled_gap.magnitude > 0.0
        assert reconstructed.to_json() == result.to_json()

    def test__execute__admits_the_frozen_production_point_inventory(self) -> None:
        configuration = replace(
            self.configuration(),
            construction_mesh_sizes=(32, 64, 128, 256),
            production_construction_size=256,
            evaluation_size=1025,
            evaluation_shift_denominator=257,
            maximum_ranges=tuple(range(16)),
        )

        result = Periodic1DFourierLocalityAnalyzer().execute(configuration)

        assert np.array_equal(
            result.evaluation.reduced_momenta.magnitude,
            np.asarray(configuration.evaluation_reduced_momenta()),
        )
        assert result.meshes[-1].construction_size == 256
        assert result.refinement_channel_names == (
            configuration.refinement_channel_names()
        )

    def test__execute__rejects_wrong_configuration_type(self) -> None:
        with pytest.raises(TypeError, match="configuration"):
            Periodic1DFourierLocalityAnalyzer().execute(
                "wrong"  # type: ignore[arg-type]
            )
