"""Tests for immutable rank-N analytic construction-mesh samples."""

import numpy as np
import pytest

from ksdft2effmass.periodic1d.rankN.band_alignment.configuration import (
    Periodic1DRankNAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.mesh_sample import (
    Periodic1DRankNAnalyticMeshSample,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.model import (
    Periodic1DRankNAnalyticCaseConstructor,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNAnalyticMeshSample:
    """Establish one immutable and internally consistent model sample."""

    def test__sample__binds_coordinates_and_frames_to_one_mesh(
        self,
        higher_rank_configuration: Periodic1DRankNAlignmentConfiguration,
    ) -> None:
        model = Periodic1DRankNAnalyticCaseConstructor(
            retained_rank=3,
            circuit_depth=1,
        ).execute()

        sample = Periodic1DRankNAnalyticMeshSample(
            model,
            higher_rank_configuration,
            513,
        )

        assert sample.model is model
        assert sample.construction_mesh_size == 513
        assert sample.mesh.size == 513
        assert sample.mesh.offsets == (0.0,)
        assert sample.coordinates.shape == (513,)
        assert sample.reference_frames.shape == (513, 6, 3)
        assert sample.attacked_frames.shape == (513, 6, 3)
        assert np.array_equal(
            sample.reference_frames,
            model.reference_frames(sample.coordinates),
        )
        assert not sample.coordinates.flags.writeable
        assert not sample.reference_frames.flags.writeable
        assert not sample.attacked_frames.flags.writeable

    def test__sample__rejects_mesh_outside_configuration(
        self,
        higher_rank_configuration: Periodic1DRankNAlignmentConfiguration,
    ) -> None:
        model = Periodic1DRankNAnalyticCaseConstructor(
            retained_rank=3,
            circuit_depth=1,
        ).execute()

        with pytest.raises(ValueError, match="configuration inventory"):
            Periodic1DRankNAnalyticMeshSample(
                model,
                higher_rank_configuration,
                511,
            )
