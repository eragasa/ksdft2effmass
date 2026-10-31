"""Software contracts for periodic tensor-grid separation analysis."""

from __future__ import annotations

import math

import numpy as np
import pytest

from ksdft2effmass.numerical_consistency import (
    NumericalConsistency,
    PeriodicTensorGridSeparationAnalyzer,
)

pytestmark = pytest.mark.software_verification


class TestPeriodicTensorGridSeparationAnalyzer:
    """Keep periodic sampling separation distinct from physical model errors."""

    def test_shifted_two_dimensional_grids__combine_axis_separations(self) -> None:
        construction_axis = np.asarray([0.0, 0.5], dtype=np.float64)
        evaluation_axis = np.asarray([0.25, 0.75], dtype=np.float64)
        construction = np.stack(
            np.meshgrid(construction_axis, construction_axis, indexing="ij"),
            axis=-1,
        )
        evaluation = np.stack(
            np.meshgrid(evaluation_axis, evaluation_axis, indexing="ij"),
            axis=-1,
        )
        analyzer = PeriodicTensorGridSeparationAnalyzer()

        result = analyzer.execute(construction, evaluation)

        assert isinstance(analyzer, NumericalConsistency)
        assert result == pytest.approx(math.sqrt(2.0) * 0.25, abs=1.0e-15)

    def test_periodic_wrap__uses_shortest_torus_distance(self) -> None:
        result = PeriodicTensorGridSeparationAnalyzer().execute(
            np.asarray([[0.9]], dtype=np.float64),
            np.asarray([[0.1]], dtype=np.float64),
        )

        assert result == pytest.approx(0.2, abs=1.0e-15)

    def test_non_float64_grid__is_rejected(self) -> None:
        with pytest.raises(TypeError, match="dtype float64"):
            PeriodicTensorGridSeparationAnalyzer().execute(
                np.asarray([[0]], dtype=np.int64),
                np.asarray([[0.1]], dtype=np.float64),
            )
