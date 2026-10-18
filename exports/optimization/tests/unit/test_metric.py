"""Software verification for positive diagonal metric geometry."""

from __future__ import annotations

import math

import pytest

from projectkoios.optimization.metric import PositiveDiagonalMetric


class TestPositiveDiagonalMetric:
    """Verify distance, dual geometry, validation, and overflow behavior."""

    def test_metric_evaluates_hand_derived_primal_and_dual_values(self) -> None:
        metric = PositiveDiagonalMetric(("x", "y"), (4.0, 9.0))

        assert metric.dimension == 2
        assert metric.squared_distance((1.0, 2.0), (4.0, 6.0)) == 180.0
        assert metric.distance((1.0, 2.0), (4.0, 6.0)) == pytest.approx(
            math.sqrt(180.0), rel=0.0, abs=2.0e-15
        )
        assert metric.squared_dual_norm((2.0, 3.0)) == 2.0
        assert metric.dual_norm((2.0, 3.0)) == pytest.approx(
            math.sqrt(2.0), rel=0.0, abs=2.0e-16
        )

    def test_metric_preserves_ordered_coordinate_identity(self) -> None:
        metric = PositiveDiagonalMetric(("orbit-000", "orbit-001"), (1.0, 2.0))

        assert metric.coordinate_names == ("orbit-000", "orbit-001")
        assert metric.diagonal == (1.0, 2.0)
        assert metric.distance((0.0, 0.0), (0.0, 0.0)) == 0.0
        assert metric.dual_norm((0.0, 0.0)) == 0.0

    def test_metric_rejects_duplicate_names_and_nonpositive_entries(self) -> None:
        with pytest.raises(ValueError):
            PositiveDiagonalMetric(("x", "x"), (1.0, 2.0))
        with pytest.raises(ValueError):
            PositiveDiagonalMetric(("x",), (0.0,))
        with pytest.raises(ValueError):
            PositiveDiagonalMetric(("x",), (-1.0,))

    def test_metric_rejects_boolean_and_dimension_mismatch(self) -> None:
        with pytest.raises(TypeError):
            PositiveDiagonalMetric(("x",), (True,))  # type: ignore[arg-type]
        metric = PositiveDiagonalMetric(("x",), (1.0,))
        with pytest.raises(ValueError):
            metric.distance((0.0,), (0.0, 1.0))
        with pytest.raises(TypeError):
            metric.dual_norm([1.0])  # type: ignore[arg-type]

    def test_metric_preserves_representable_compensated_scales(self) -> None:
        primal = PositiveDiagonalMetric(("x",), (1.0e300,))
        dual = PositiveDiagonalMetric(("x",), (1.0e-300,))
        large_dual = PositiveDiagonalMetric(("x",), (1.0e308,))

        assert primal.squared_distance((1.0e-200,), (0.0,)) == pytest.approx(
            1.0e-100,
            rel=5.0e-15,
            abs=0.0,
        )
        assert dual.squared_dual_norm((1.0e-200,)) == pytest.approx(
            1.0e-100,
            rel=5.0e-15,
            abs=0.0,
        )
        assert large_dual.squared_dual_norm((1.0e308,)) == pytest.approx(
            1.0e308,
            rel=5.0e-15,
            abs=0.0,
        )

    def test_metric_rescales_nonzero_subnormal_intermediate_squares(self) -> None:
        primal = PositiveDiagonalMetric(("x",), (1.0e300,))
        dual = PositiveDiagonalMetric(("x",), (1.0e-300,))

        assert primal.squared_distance((1.0e-161,), (0.0,)) == pytest.approx(
            1.0e-22,
            rel=5.0e-15,
            abs=0.0,
        )
        assert dual.squared_dual_norm((1.0e-161,)) == pytest.approx(
            1.0e-22,
            rel=5.0e-15,
            abs=0.0,
        )

    def test_metric_rejects_nonfinite_arithmetic(self) -> None:
        metric = PositiveDiagonalMetric(("x",), (1.0e308,))

        with pytest.raises(ValueError, match="nonfinite"):
            metric.squared_distance((1.0e308,), (0.0,))
