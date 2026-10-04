"""Software verification for ``CenteredUniformReciprocalMesh2D``."""

import pytest

from ksdft2effmass.solid_state import CenteredUniformReciprocalMesh2D

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]
SUT = CenteredUniformReciprocalMesh2D


class TestCenteredUniformReciprocalMesh2D:
    """Own reciprocal-mesh ordering, coordinate, and input-boundary evidence."""

    def test_properties__rectangular_mesh__uses_centered_half_open_order(self) -> None:
        """Coordinates are first-outer and second-inner on the half-open cell."""
        mesh = CenteredUniformReciprocalMesh2D((4, 2), "four-by-two")

        assert mesh.point_count == 8
        assert mesh.reduced_spacings == (0.25, 0.5)
        assert mesh.point_ordering == "first_outer_second_inner"
        assert mesh.point_indices == (
            (0, 0),
            (0, 1),
            (1, 0),
            (1, 1),
            (2, 0),
            (2, 1),
            (3, 0),
            (3, 1),
        )
        assert mesh.reduced_coordinates[0] == (-0.5, -0.5)
        assert mesh.reduced_coordinates[-1] == (0.25, 0.0)

    def test_properties__odd_counts__remain_valid_half_open_meshes(self) -> None:
        """Odd counts are valid without sampling reduced-coordinate zero."""
        mesh = CenteredUniformReciprocalMesh2D((3, 5), "three-by-five")

        assert mesh.point_count == 15
        assert (0.0, 0.0) not in mesh.reduced_coordinates
        assert mesh.reduced_coordinates[-1] == (-0.5 + 2.0 / 3.0, -0.5 + 4.0 / 5.0)

    def test_construction__wrong_or_trivial_counts__raises(self) -> None:
        """Booleans and counts below two are rejected rather than coerced."""
        with pytest.raises(TypeError, match="built-in integers"):
            CenteredUniformReciprocalMesh2D((True, 2), "mesh")
        with pytest.raises(ValueError, match="at least two"):
            CenteredUniformReciprocalMesh2D((1, 2), "mesh")
