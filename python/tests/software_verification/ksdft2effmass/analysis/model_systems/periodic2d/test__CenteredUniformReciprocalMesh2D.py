"""Verify removal of the retired analysis-owned reciprocal-mesh route."""

import pytest

import ksdft2effmass.analysis.model_systems as model_systems
import ksdft2effmass.analysis.model_systems.periodic2d as periodic2d
from ksdft2effmass.analysis.model_systems.periodic2d import reciprocal_mesh

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestCenteredUniformReciprocalMesh2DAnalysisRoute:
    """Keep the moved mesh out of its former analysis import routes."""

    def test_public_api__moved_mesh__has_no_compatibility_alias(self) -> None:
        """The old module and package routes do not re-export the moved DataObject."""
        name = "CenteredUniformReciprocalMesh2D"

        assert name not in model_systems.__all__
        assert not hasattr(model_systems, name)
        assert name not in periodic2d.__all__
        assert not hasattr(periodic2d, name)
        assert not hasattr(reciprocal_mesh, name)
