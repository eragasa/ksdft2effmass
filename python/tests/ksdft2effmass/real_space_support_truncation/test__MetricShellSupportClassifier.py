"""Software contracts for typed metric-shell support classification."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    DirectLatticeMetric,
)
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)

from ksdft2effmass.real_space_support_truncation import (
    MetricGeometry,
    MetricShellSupportClassifier,
    MetricShellValueAnalyzer,
)

pytestmark = pytest.mark.software_verification


@dataclass(frozen=True, slots=True)
class _SquareMetricGeometry(MetricGeometry):
    dimension: int
    direct_metric: DirectLatticeMetric
    shell_metric_scale: float


def _square_geometry(*, scale: float = 1.0) -> _SquareMetricGeometry:
    return _SquareMetricGeometry(
        dimension=2,
        direct_metric=DirectLatticeMetric(
            DirectLattice2D(
                a1=np.asarray([1.0, 0.0], dtype=np.float64),
                a2=np.asarray([0.0, 1.0], dtype=np.float64),
            )
        ),
        shell_metric_scale=scale,
    )


def _square_support(maximum_component: int) -> tuple[LatticeDisplacement, ...]:
    return tuple(
        LatticeDisplacement(LatticeDimension.TWO, (first, second))
        for first in range(-maximum_component, maximum_component + 1)
        for second in range(-maximum_component, maximum_component + 1)
    )


class TestMetricShellSupportClassifier:
    """Keep ordinal support shells distinct from physical metric values."""

    def test_square_support__classifies_ordinal_and_metric_shells(self) -> None:
        result = MetricShellSupportClassifier().execute(
            _square_geometry(),
            _square_support(2),
        )

        assert tuple(sorted(set(result.metric_shell_values))) == (0, 1, 2, 4, 5, 8)
        assert tuple(sorted(set(result.support_inventory.ordinal_shell_indices))) == (
            0,
            1,
            2,
            3,
            4,
            5,
        )
        assert (
            result.metric_shell_value_for(
                LatticeDisplacement(LatticeDimension.TWO, (2, 1))
            )
            == 5
        )
        assert result.maximum_rounding_defect == 0.0

    def test_nonclosed_periodic_inventory__retains_metric_values_only(self) -> None:
        displacements = (
            LatticeDisplacement(LatticeDimension.TWO, (-2, 0)),
            LatticeDisplacement(LatticeDimension.TWO, (0, 0)),
            LatticeDisplacement(LatticeDimension.TWO, (1, 0)),
        )

        result = MetricShellValueAnalyzer().execute(
            _square_geometry(),
            displacements,
        )

        assert result.metric_shell_values == (4, 0, 1)
        with pytest.raises(ValueError, match="closed under displacement conjugation"):
            MetricShellSupportClassifier().execute(
                _square_geometry(),
                displacements,
            )

    def test_nonintegral_scaled_metric__is_rejected(self) -> None:
        with pytest.raises(ValueError, match="integer shell values"):
            MetricShellSupportClassifier().execute(
                _square_geometry(scale=0.5),
                _square_support(1),
            )

    @pytest.mark.parametrize("value", [True, 1, "1"])
    def test_rounding_tolerance__nonfloat__is_rejected(
        self,
        value: bool | int | str,
    ) -> None:
        with pytest.raises(TypeError, match="built-in float"):
            MetricShellSupportClassifier(
                rounding_absolute_tolerance=value  # type: ignore[arg-type]
            )
