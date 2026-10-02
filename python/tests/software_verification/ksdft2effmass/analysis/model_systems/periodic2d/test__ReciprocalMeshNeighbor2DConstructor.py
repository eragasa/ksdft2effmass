"""Software verification for ``ReciprocalMeshNeighbor2DConstructor``."""

import pytest

from ksdft2effmass.analysis.model_systems import (
    CenteredUniformReciprocalMesh2D,
    PositiveReciprocalDirection2D,
    ReciprocalMeshNeighbor2DConstructor,
    ReciprocalMeshNeighbor2DRequest,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestReciprocalMeshNeighbor2DConstructor:
    """Own ordinary-neighbor and independent boundary-wrap evidence."""

    def test_execute__ordinary_first_step__does_not_require_sewing(self) -> None:
        """An interior first-direction step advances without reciprocal translation."""
        mesh = CenteredUniformReciprocalMesh2D((4, 2), "mesh")
        request = ReciprocalMeshNeighbor2DRequest(
            mesh, (1, 0), PositiveReciprocalDirection2D.FIRST
        )

        result = ReciprocalMeshNeighbor2DConstructor().execute(request)

        assert result.neighbor_index == (2, 0)
        assert result.reciprocal_translation == (0, 0)
        assert not result.sewing_required

    def test_execute__second_boundary__wraps_only_second_direction(self) -> None:
        """A final second index wraps with translation ``(0, 1)``."""
        mesh = CenteredUniformReciprocalMesh2D((4, 2), "mesh")
        request = ReciprocalMeshNeighbor2DRequest(
            mesh, (2, 1), PositiveReciprocalDirection2D.SECOND
        )

        result = ReciprocalMeshNeighbor2DConstructor().execute(request)

        assert result.neighbor_index == (2, 0)
        assert result.reciprocal_translation == (0, 1)
        source = mesh.reduced_coordinate(request.point_index)
        neighbor = mesh.reduced_coordinate(result.neighbor_index)
        assert neighbor[0] + result.reciprocal_translation[0] == source[0]
        assert (
            neighbor[1] + result.reciprocal_translation[1]
            == source[1] + mesh.reduced_spacings[1]
        )
