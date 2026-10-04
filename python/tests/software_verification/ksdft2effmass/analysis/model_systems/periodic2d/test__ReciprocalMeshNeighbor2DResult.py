"""Software verification for ``ReciprocalMeshNeighbor2DResult``."""

import pytest

from ksdft2effmass.analysis.model_systems import (
    PositiveReciprocalDirection2D,
    ReciprocalMeshNeighbor2DRequest,
    ReciprocalMeshNeighbor2DResult,
)
from ksdft2effmass.solid_state import CenteredUniformReciprocalMesh2D

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestReciprocalMeshNeighbor2DResult:
    """Own result correlation and reciprocal-translation evidence."""

    @staticmethod
    def request() -> ReciprocalMeshNeighbor2DRequest:
        """Return a boundary-crossing request for result tests."""
        return ReciprocalMeshNeighbor2DRequest(
            CenteredUniformReciprocalMesh2D((4, 2), "mesh"),
            (3, 1),
            PositiveReciprocalDirection2D.FIRST,
        )

    def test_construction__valid_wrap__reports_required_sewing(self) -> None:
        """The positive-first boundary wraps to index zero with translation one."""
        result = ReciprocalMeshNeighbor2DResult(self.request(), (0, 1), (1, 0))

        assert result.sewing_required

    def test_construction__forged_translation__raises_value_error(self) -> None:
        """A wrapped neighbor cannot omit its reciprocal translation."""
        with pytest.raises(ValueError, match="translation"):
            ReciprocalMeshNeighbor2DResult(self.request(), (0, 1), (0, 0))
