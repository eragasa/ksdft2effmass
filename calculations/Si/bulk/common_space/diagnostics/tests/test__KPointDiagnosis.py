"""Synthetic nominal producer-point records; no retained silicon calculation."""

from dataclasses import FrozenInstanceError, replace
from math import pi

import pytest
from common_space.diagnostics.diagnosis import KPointDiagnosis

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestKPointDiagnosis:
    """Keep per-point minimum-direction values typed, immutable, and explicit."""

    @staticmethod
    def _point(*, rank: int = 9) -> KPointDiagnosis:
        return KPointDiagnosis(
            ordered_index=12,
            fractional_coordinates=(0.0, 1 / 3, 0.0),
            resolved_rank=rank,
            maximum_singular_value=1.0,
            next_to_minimum_singular_value=1.0,
            minimum_singular_value=0.0 if rank < 10 else 1.0,
            condition_number=None if rank < 10 else 1.0,
            minimum_principal_cosine=0.0 if rank < 10 else 1.0,
            maximum_principal_angle_radians=pi / 2 if rank < 10 else 0.0,
            full_rank_gate_passed=rank == 10,
            minimum_direction_atomic_weights=tuple(
                0.25 if i in (0, 4, 5, 9) else 0.0 for i in range(10)
            )
            if rank < 10
            else (),
        )

    def test_group_weights__follow_atomic_s_p_and_radial_s_star_order(self) -> None:
        point = self._point()
        assert point.minimum_direction_group_weights == (0.5, 0.0, 0.5)
        assert point.to_json()["minimum_direction_atomic_weights"] == list(
            point.minimum_direction_atomic_weights
        )

    def test_full_rank__has_no_deficient_direction(self) -> None:
        point = self._point(rank=10)
        assert point.minimum_direction_atomic_weights == ()
        assert point.minimum_direction_group_weights == ()
        with pytest.raises(ValueError, match="ten minimum-direction"):
            replace(point, minimum_direction_atomic_weights=(1.0,) + (0.0,) * 9)

    @pytest.mark.parametrize(
        "value", (True, "0.25", float("inf"), float("nan"), -0.1, 1.1)
    )
    def test_invalid_weight__is_rejected_without_coercion(
        self, value: float | bool | str
    ) -> None:
        point = self._point()
        with pytest.raises(ValueError, match="finite probabilities"):
            replace(
                point,
                minimum_direction_atomic_weights=(
                    value,  # type: ignore[arg-type]  # Deliberately invalid scalar.
                    *point.minimum_direction_atomic_weights[1:],
                ),
            )

    def test_missing_deficient_direction__is_not_filled_from_gamma(self) -> None:
        with pytest.raises(ValueError, match="ten minimum-direction"):
            replace(self._point(), minimum_direction_atomic_weights=())

    def test_zero_direction__cannot_be_reported_as_an_svd_vector(self) -> None:
        with pytest.raises(ValueError, match="nonzero mass"):
            replace(self._point(), minimum_direction_atomic_weights=(0.0,) * 10)

    def test_mutable_fields__cannot_enter_immutable_result(self) -> None:
        point = self._point()
        with pytest.raises(ValueError, match="immutable tuple"):
            replace(
                point,
                minimum_direction_atomic_weights=list(  # type: ignore[arg-type]  # Deliberately mutable input.
                    point.minimum_direction_atomic_weights
                ),
            )
        with pytest.raises(ValueError, match="three finite"):
            replace(point, fractional_coordinates=[0.0, 0.0, 0.0])  # type: ignore[arg-type]  # Deliberately mutable input.
        with pytest.raises(FrozenInstanceError):
            point.minimum_direction_atomic_weights = ()  # type: ignore[misc]

    def test_full_rank_flag__must_match_resolved_rank(self) -> None:
        with pytest.raises(ValueError, match="flag differs"):
            replace(self._point(), full_rank_gate_passed=True)

    def test_wire_lists__are_detached_from_result(self) -> None:
        point = self._point()
        wire = point.to_json()
        weights = wire["minimum_direction_atomic_weights"]
        assert type(weights) is list
        weights[0] = 99.0
        assert point.minimum_direction_atomic_weights[0] == 0.25
        assert point.minimum_direction_group_weights == (0.5, 0.0, 0.5)
