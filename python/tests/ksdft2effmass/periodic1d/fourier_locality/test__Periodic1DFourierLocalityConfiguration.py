"""Tests for the direct Fourier-locality configuration record."""

from dataclasses import replace

import pytest

from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityConfiguration,
)


def configuration() -> Periodic1DFourierLocalityConfiguration:
    """Return the selected compatible rank-one finite request."""
    return Periodic1DFourierLocalityConfiguration(
        parent_identity=("ksdft2effmass.periodic1d.controlled-four-state-parent.v1"),
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
        construction_mesh_sizes=(32, 64, 128, 256),
        production_construction_size=256,
        evaluation_size=1025,
        evaluation_shift_numerator=1,
        evaluation_shift_denominator=257,
        maximum_ranges=tuple(range(16)),
        sampled_gap_threshold=0.25,
        energy_absolute_tolerance=1.0e-12,
        relative_tolerance=1.0e-12,
        squared_energy_absolute_tolerance=1.0e-12,
        dimensionless_absolute_tolerance=1.0e-12,
        refinement_tolerance=1.0e-10,
        application_threshold=1.0e-8,
    )


class TestPeriodic1DFourierLocalityConfiguration:
    """Establish typed wire, rational parent, and mesh admission behavior."""

    def test__json__round_trips_canonical_bytes(self) -> None:
        subject = configuration()

        reconstructed = Periodic1DFourierLocalityConfiguration.from_json(
            subject.to_json()
        )

        assert reconstructed.to_json() == subject.to_json()
        assert reconstructed == subject

    def test__init__rejects_unbound_parent_identity(self) -> None:
        subject = configuration()

        with pytest.raises(ValueError, match="parent identity"):
            replace(subject, parent_identity="different-parent")

    def test__init__requires_adjacent_mesh_pair_for_refinement(self) -> None:
        subject = configuration()

        with pytest.raises(ValueError, match="strictly increasing"):
            replace(
                subject,
                construction_mesh_sizes=(256,),
                production_construction_size=256,
            )

    def test__init__rejects_nonsymmetric_onsite_parent(self) -> None:
        subject = configuration()
        nonsymmetric = (
            (-120, 7, 0, 0),
            (6, -35, 0, 0),
            (0, 0, 100, 4),
            (0, 0, 4, 175),
        )

        with pytest.raises(ValueError, match="exactly symmetric"):
            replace(subject, onsite_numerators=nonsymmetric)

    def test__init__rejects_boolean_parent_entries(self) -> None:
        subject = configuration()
        malformed = (
            (-120, 6, 0, 0),
            (6, -35, 0, 0),
            (0, 0, True, 4),
            (0, 0, 4, 175),
        )

        with pytest.raises(TypeError, match="four-by-four integer matrix"):
            replace(subject, onsite_numerators=malformed)

    def test__init__rejects_evaluation_points_on_construction_mesh(self) -> None:
        subject = configuration()

        with pytest.raises(ValueError, match="meshes must be disjoint"):
            replace(
                subject,
                evaluation_size=32,
                evaluation_shift_numerator=1,
                evaluation_shift_denominator=2,
            )

    def test__init__rejects_support_reaching_cyclic_nyquist_point(self) -> None:
        subject = configuration()

        with pytest.raises(ValueError, match="exclude every cyclic Nyquist"):
            replace(subject, maximum_ranges=tuple(range(17)))
