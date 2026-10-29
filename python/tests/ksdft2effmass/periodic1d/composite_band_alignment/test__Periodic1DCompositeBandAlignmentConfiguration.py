"""Tests for the direct rank-two composite-alignment configuration."""

from dataclasses import replace

import pytest

from ksdft2effmass.periodic1d.composite_band_alignment import (
    Periodic1DCompositeBandAlignmentConfiguration,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DCompositeBandAlignmentConfiguration:
    """Establish frozen-parent, mesh, rank-policy, and typed-wire admission."""

    def test__json__round_trips_canonical_bytes(
        self,
        composite_configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> None:
        wire = composite_configuration.to_json()

        reconstructed = Periodic1DCompositeBandAlignmentConfiguration.from_json(wire)

        assert reconstructed == composite_configuration
        assert reconstructed.to_json() == wire

    def test__init__rejects_unbound_parent_identity(
        self,
        composite_configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> None:
        with pytest.raises(ValueError, match="parent identity"):
            replace(composite_configuration, parent_identity="different-parent")

    def test__init__rejects_nonfrozen_construction_mesh(
        self,
        composite_configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> None:
        with pytest.raises(ValueError, match="construction_size"):
            replace(composite_configuration, construction_size=128)

    def test__init__rejects_evaluation_point_intersection(
        self,
        composite_configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> None:
        with pytest.raises(ValueError, match="evaluation_size"):
            replace(
                composite_configuration,
                evaluation_size=64,
                evaluation_shift_numerator=0,
                evaluation_shift_denominator=65,
            )

    def test__init__rejects_boolean_parent_entries(
        self,
        composite_configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> None:
        malformed = (
            (-120, 6, 0, 0),
            (6, -35, 0, 0),
            (0, 0, True, 4),
            (0, 0, 4, 175),
        )

        with pytest.raises(TypeError, match="integer tuple"):
            replace(composite_configuration, onsite_numerators=malformed)

    def test__init__rejects_changed_rank_cutoff_policy(
        self,
        composite_configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> None:
        with pytest.raises(ValueError, match="absolute rank cutoff"):
            replace(
                composite_configuration,
                procrustes_rank_absolute_tolerance=1.0e-13,
            )

    def test__derived_coordinates__are_exactly_disjoint(
        self,
        composite_configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> None:
        construction = set(composite_configuration.construction_reduced_momenta())
        evaluation = set(composite_configuration.evaluation_reduced_momenta())

        assert len(construction) == 64
        assert len(evaluation) == 257
        assert construction.isdisjoint(evaluation)
