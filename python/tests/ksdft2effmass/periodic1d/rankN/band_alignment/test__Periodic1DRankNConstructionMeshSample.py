"""Tests for immutable rank-N analytic construction-mesh samples."""

import numpy as np
import pytest

from ksdft2effmass.periodic1d.rankN.band_alignment.configuration import (
    Periodic1DRankNAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.mesh_sample import (
    Periodic1DRankNConstructionMeshSample,
)
from periodic1d_rankn_analytic_case_support import (
    SyntheticPeriodic1DRankNAnalyticCaseConstructor,
)
from periodic1d_rankn_analytic_oracle import analytic_fourier_givens_transformation
from periodic1d_rankn_control_basis_support import synthetic_basis_identity

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNConstructionMeshSample:
    """Establish one immutable and internally consistent model sample."""

    def test__sample__binds_coordinates_and_frames_to_one_mesh(
        self,
        higher_rank_configuration: Periodic1DRankNAlignmentConfiguration,
    ) -> None:
        model = SyntheticPeriodic1DRankNAnalyticCaseConstructor(
            retained_rank=3,
            circuit_depth=1,
            basis_identity=synthetic_basis_identity(3),
            gauge_transformation=analytic_fourier_givens_transformation(
                retained_rank=3,
                circuit_depth=1,
            ),
        ).execute()

        sample = Periodic1DRankNConstructionMeshSample(
            model.parent_model,
            model.gauge_transformation,
            higher_rank_configuration,
            513,
        )

        assert sample.parent_model is model.parent_model
        assert sample.gauge_transformation is model.gauge_transformation
        assert sample.construction_mesh_size == 513
        assert sample.mesh.size == 513
        assert sample.mesh.offsets == (0.0,)
        assert sample.coordinates.shape == (513,)
        assert sample.reference_frames.shape == (513, 6, 3)
        assert sample.gauge_transformed_frames.shape == (513, 6, 3)
        assert np.array_equal(
            sample.reference_frames,
            model.reference_frames(sample.coordinates),
        )
        assert not sample.coordinates.flags.writeable
        assert not sample.reference_frames.flags.writeable
        assert not sample.gauge_transformed_frames.flags.writeable

    def test__sample__rejects_mesh_outside_configuration(
        self,
        higher_rank_configuration: Periodic1DRankNAlignmentConfiguration,
    ) -> None:
        model = SyntheticPeriodic1DRankNAnalyticCaseConstructor(
            retained_rank=3,
            circuit_depth=1,
            basis_identity=synthetic_basis_identity(3),
            gauge_transformation=analytic_fourier_givens_transformation(
                retained_rank=3,
                circuit_depth=1,
            ),
        ).execute()

        with pytest.raises(ValueError, match="configuration inventory"):
            Periodic1DRankNConstructionMeshSample(
                model.parent_model,
                model.gauge_transformation,
                higher_rank_configuration,
                511,
            )
