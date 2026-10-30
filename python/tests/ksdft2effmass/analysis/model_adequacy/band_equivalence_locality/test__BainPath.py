"""Software verification for the continuous unit-volume Bain path."""

import math

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import DirectLattice3D

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    BainPath,
)

pytestmark = pytest.mark.unit


class TestBainPath:
    """Establish the sampled volume invariant and path input boundary."""

    def test_result__201_point_scan__does_not_change_primitive_volume(self) -> None:
        points = tuple(
            BainPath(strain_fraction=float(index) / 200.0).result()
            for index in range(201)
        )
        volumes = np.asarray(
            tuple(point.primitive_volume for point in points),
            dtype=np.float64,
        )

        assert points[0].aspect_ratio == pytest.approx(math.sqrt(2.0))
        assert points[-1].aspect_ratio == pytest.approx(1.0)
        assert all(type(point.direct_lattice) is DirectLattice3D for point in points)
        assert all(not point.direct_lattice.A.flags.writeable for point in points)
        assert np.ptp(volumes) < 1.0e-15
        assert volumes == pytest.approx(np.ones(201), rel=0.0, abs=5.0e-16)
        assert all(
            np.linalg.det(point.direct_metric.metric_tensor)
            == pytest.approx(point.primitive_volume**2, rel=0.0, abs=3.0e-15)
            for point in points
        )

    @pytest.mark.parametrize("value", (True, -0.01, 1.01))
    def test_init__outside_float_interval__fails_closed(
        self, value: bool | float
    ) -> None:
        with pytest.raises(ValueError, match=r"built-in float in \[0, 1\]"):
            BainPath(strain_fraction=value)
