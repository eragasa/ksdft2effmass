"""Software verification for ``ReciprocalMeshNeighbor2DRequest``."""

import pytest

from ksdft2effmass.analysis.model_systems import (
    CenteredUniformReciprocalMesh2D,
    PositiveReciprocalDirection2D,
    ReciprocalMeshNeighbor2DRequest,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestReciprocalMeshNeighbor2DRequest:
    """Own source-index and positive-direction request evidence."""

    def test_construction__valid_source__retains_exact_fields(self) -> None:
        """An in-range source index and enum direction are retained exactly."""
        mesh = CenteredUniformReciprocalMesh2D((4, 2), "mesh")
        request = ReciprocalMeshNeighbor2DRequest(
            mesh, (3, 1), PositiveReciprocalDirection2D.SECOND
        )

        assert request.mesh is mesh
        assert request.point_index == (3, 1)
        assert request.direction is PositiveReciprocalDirection2D.SECOND

    def test_construction__out_of_range_or_string_direction__raises(self) -> None:
        """Out-of-range indices and enum-like strings are rejected."""
        mesh = CenteredUniformReciprocalMesh2D((4, 2), "mesh")
        with pytest.raises(ValueError, match="inside"):
            ReciprocalMeshNeighbor2DRequest(
                mesh, (4, 0), PositiveReciprocalDirection2D.FIRST
            )
        with pytest.raises(TypeError, match="direction"):
            ReciprocalMeshNeighbor2DRequest(
                mesh,
                (0, 0),
                "plus_first_reciprocal_vector",  # type: ignore[arg-type]
            )
