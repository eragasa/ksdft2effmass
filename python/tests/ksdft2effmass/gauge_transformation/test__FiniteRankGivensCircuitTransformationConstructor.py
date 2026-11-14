"""Contracts for generic sampled finite-rank Givens transformations."""

import numpy as np
import pytest

from ksdft2effmass.gauge_transformation import (
    FiniteRankAlternatingNearestNeighborGivensCircuitConstructor,
    FiniteRankGivensCircuit,
    FiniteRankGivensCircuitTransformationConstructor,
    FiniteRankGivensLayer,
    FiniteRankGivensRotation,
)


class TestFiniteRankGivensCircuitTransformationConstructor:
    """Establish ordered circuit construction and explicit right actions."""

    def test__alternating_constructor__supports_rank_two_and_omits_empty_layers(
        self,
    ) -> None:
        circuit = FiniteRankAlternatingNearestNeighborGivensCircuitConstructor(
            represented_rank=2,
            layer_count=4,
        ).execute()

        assert circuit.layers == (
            FiniteRankGivensLayer(rotations=(FiniteRankGivensRotation(0, 1),)),
            FiniteRankGivensLayer(rotations=(FiniteRankGivensRotation(0, 1),)),
        )
        assert circuit.rotation_count == 2

    def test__execute__constructs_the_declared_ordered_layers(self) -> None:
        circuit = FiniteRankGivensCircuit(
            represented_rank=3,
            layers=(
                FiniteRankGivensLayer(rotations=(FiniteRankGivensRotation(0, 1),)),
                FiniteRankGivensLayer(rotations=(FiniteRankGivensRotation(1, 2),)),
            ),
        )
        angles = np.asarray(((0.2, -0.3), (0.0, 0.4)), dtype=np.float64)

        transformation = FiniteRankGivensCircuitTransformationConstructor(
            circuit=circuit,
            angle_samples=angles,
        ).execute()

        expected = np.empty((2, 3, 3), dtype=np.complex128)
        for sample_index, (first_angle, second_angle) in enumerate(angles):
            first = np.asarray(
                (
                    (np.cos(first_angle), -np.sin(first_angle), 0.0),
                    (np.sin(first_angle), np.cos(first_angle), 0.0),
                    (0.0, 0.0, 1.0),
                ),
                dtype=np.complex128,
            )
            second = np.asarray(
                (
                    (1.0, 0.0, 0.0),
                    (0.0, np.cos(second_angle), -np.sin(second_angle)),
                    (0.0, np.sin(second_angle), np.cos(second_angle)),
                ),
                dtype=np.complex128,
            )
            expected[sample_index] = first @ second
        assert np.allclose(transformation.unitaries, expected, atol=1.0e-15)

    def test__transformation__applies_right_actions_to_frames_and_operators(
        self,
    ) -> None:
        circuit = FiniteRankGivensCircuit(
            represented_rank=2,
            layers=(
                FiniteRankGivensLayer(rotations=(FiniteRankGivensRotation(0, 1),)),
            ),
        )
        transformation = FiniteRankGivensCircuitTransformationConstructor(
            circuit=circuit,
            angle_samples=np.asarray(((0.25,), (-0.4,)), dtype=np.float64),
        ).execute()
        frames = np.broadcast_to(
            np.eye(2, dtype=np.complex128),
            (2, 2, 2),
        ).copy()
        operators = np.asarray(
            (
                ((1.0, 0.0), (0.0, 2.0)),
                ((-1.0, 0.0), (0.0, 3.0)),
            ),
            dtype=np.complex128,
        )

        transformed_frames = transformation.transform_frames(frames)
        transformed_operators = transformation.transform_operators(operators)

        assert np.allclose(
            transformed_frames,
            transformation.unitaries,
            atol=1.0e-15,
        )
        assert np.allclose(
            transformed_operators,
            transformation.inverse_right_actions @ operators @ transformation.unitaries,
            atol=1.0e-15,
        )

    def test__layer__rejects_overlapping_rotations(self) -> None:
        with pytest.raises(ValueError, match="pairwise disjoint"):
            FiniteRankGivensLayer(
                rotations=(
                    FiniteRankGivensRotation(0, 1),
                    FiniteRankGivensRotation(1, 2),
                )
            )

    def test__constructor__rejects_missing_angle_columns(self) -> None:
        circuit = FiniteRankGivensCircuit(
            represented_rank=3,
            layers=(
                FiniteRankGivensLayer(rotations=(FiniteRankGivensRotation(0, 1),)),
                FiniteRankGivensLayer(rotations=(FiniteRankGivensRotation(1, 2),)),
            ),
        )
        with pytest.raises(ValueError, match="columns"):
            FiniteRankGivensCircuitTransformationConstructor(
                circuit=circuit,
                angle_samples=np.zeros((3, 1), dtype=np.float64),
            )
