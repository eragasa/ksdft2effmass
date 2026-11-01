"""Tests for immutable rank-N block-refinement records."""

import numpy as np
import pytest

from ksdft2effmass.periodic1d.rankN.band_alignment.refinement_result import (
    Periodic1DRankNBlockRefinementResult,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.definition import (
    Periodic1DRankNGaugeAlignment,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNBlockRefinementResult:
    """Establish immutable array-backed serialization behavior."""

    def test__round_trip__does_not_generate_numpy_equality(self) -> None:
        coarse = np.asarray([1.0, 2.0], dtype=np.float64)
        zeros = np.zeros(2, dtype=np.float64)
        tolerances = 1.0e-10 + 1.0e-6 * coarse
        result = Periodic1DRankNBlockRefinementResult(
            gauge_alignment=Periodic1DRankNGaugeAlignment.IDENTITY,
            coarse_mesh_size=513,
            fine_mesh_size=1025,
            translations=np.asarray([0, 1], dtype=np.int64),
            coarse_normalized_block_norms=coarse,
            fine_normalized_block_norms=coarse,
            absolute_changes=zeros,
            relative_changes=zeros,
            applied_tolerances=tolerances,
            signed_margins=tolerances,
            all_pass=True,
        )

        reconstructed = Periodic1DRankNBlockRefinementResult.from_json(result.to_json())

        assert reconstructed is not result
        assert (reconstructed == result) is False
        assert reconstructed.to_json() == result.to_json()
