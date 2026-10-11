"""Integration verification for weighted affine quadratic construction."""

from __future__ import annotations

import math
import random

import pytest

from projectkoios.optimization.affine import (
    WeightedAffineResidualDefinition,
    WeightedAffineResidualQuadraticConstructor,
    WeightedAffineResidualTerm,
)


class TestWeightedAffineResidualQuadraticConstructor:
    """Verify construction, backend agreement, and fail-closed boundaries."""

    @staticmethod
    def definition() -> WeightedAffineResidualDefinition:
        return WeightedAffineResidualDefinition(
            coordinate_names=("x", "y"),
            terms=(
                WeightedAffineResidualTerm((1.0, 0.0), 1.0, 2.0),
                WeightedAffineResidualTerm((0.0, 1.0), -2.0, 3.0),
                WeightedAffineResidualTerm((1.0, 1.0), -1.0, 0.5),
            ),
        )

    def test_execute_constructs_the_hand_derived_dense_quadratic(self) -> None:
        definition = self.definition()
        quadratic = WeightedAffineResidualQuadraticConstructor().execute(definition)

        assert quadratic.center == pytest.approx((1.0, -2.0), rel=0.0, abs=2.0e-15)
        assert quadratic.matrix == ((2.5, 0.5), (0.5, 3.5))
        assert quadratic.minimum_squared_loss == pytest.approx(
            0.0, rel=0.0, abs=2.0e-29
        )
        assert quadratic.squared_loss((3.0, -1.0)) == pytest.approx(
            15.5, rel=0.0, abs=4.0e-15
        )
        assert quadratic.squared_loss((3.0, -1.0)) == pytest.approx(
            definition.squared_loss((3.0, -1.0)), rel=0.0, abs=4.0e-15
        )

    def test_execute_constructs_the_same_sparse_function(self) -> None:
        definition = self.definition()
        quadratic = WeightedAffineResidualQuadraticConstructor().execute(
            definition, sparse=True
        )

        assert quadratic.sparse is True
        assert quadratic.squared_loss((3.0, -1.0)) == pytest.approx(
            definition.squared_loss((3.0, -1.0)), rel=0.0, abs=4.0e-15
        )
        assert quadratic.root_loss((3.0, -1.0)) == pytest.approx(
            math.sqrt(15.5), rel=0.0, abs=1.0e-15
        )

    def test_execute_preserves_a_nonzero_least_squares_minimum(self) -> None:
        definition = WeightedAffineResidualDefinition(
            coordinate_names=("x",),
            terms=(
                WeightedAffineResidualTerm((1.0,), 0.0, 1.0),
                WeightedAffineResidualTerm((1.0,), 2.0, 1.0),
            ),
        )

        quadratic = WeightedAffineResidualQuadraticConstructor().execute(definition)

        assert quadratic.center == (1.0,)
        assert quadratic.matrix == ((2.0,),)
        assert quadratic.minimum_squared_loss == 2.0
        assert quadratic.squared_loss((3.0,)) == definition.squared_loss((3.0,))

    def test_compensated_scales_do_not_underflow_before_weighting(self) -> None:
        definition = WeightedAffineResidualDefinition(
            coordinate_names=("x",),
            terms=(WeightedAffineResidualTerm((1.0e-200,), 2.0e-200, 1.0e300),),
        )

        quadratic = WeightedAffineResidualQuadraticConstructor().execute(definition)

        assert quadratic.center == pytest.approx((2.0,), rel=5.0e-15, abs=0.0)
        assert definition.squared_loss((3.0,)) == pytest.approx(
            1.0e-100,
            rel=5.0e-15,
            abs=0.0,
        )
        assert quadratic.matrix[0][0] == pytest.approx(
            1.0e-100,
            rel=5.0e-15,
            abs=0.0,
        )
        assert quadratic.squared_loss((3.0,)) == pytest.approx(
            definition.squared_loss((3.0,)),
            rel=5.0e-15,
            abs=0.0,
        )

    def test_subnormal_coefficient_product_uses_scaled_weighting(self) -> None:
        definition = WeightedAffineResidualDefinition(
            coordinate_names=("x", "y"),
            terms=(
                WeightedAffineResidualTerm(
                    (1.0e-200, 1.0e-123),
                    0.0,
                    1.0e300,
                ),
                WeightedAffineResidualTerm((1.0, 0.0), 0.0, 1.0),
            ),
        )

        quadratic = WeightedAffineResidualQuadraticConstructor().execute(definition)

        assert quadratic.matrix[0][1] == pytest.approx(
            1.0e-23,
            rel=5.0e-15,
            abs=0.0,
        )
        assert quadratic.matrix[1][0] == quadratic.matrix[0][1]

    def test_generated_full_rank_systems_match_direct_residual_evaluation(self) -> None:
        generator = random.Random(20261011)
        for dimension in range(1, 7):
            coordinate_names = tuple(f"x_{index}" for index in range(dimension))
            terms = [
                WeightedAffineResidualTerm(
                    tuple(1.0 if row == column else 0.0 for column in range(dimension)),
                    generator.uniform(-2.0, 2.0),
                    generator.uniform(0.25, 3.0),
                )
                for row in range(dimension)
            ]
            terms.extend(
                WeightedAffineResidualTerm(
                    tuple(generator.uniform(-2.0, 2.0) for _ in range(dimension)),
                    generator.uniform(-2.0, 2.0),
                    generator.uniform(0.25, 3.0),
                )
                for _ in range(3)
            )
            definition = WeightedAffineResidualDefinition(
                coordinate_names, tuple(terms)
            )
            loss = WeightedAffineResidualQuadraticConstructor().execute(definition)

            for _ in range(4):
                point = tuple(generator.uniform(-3.0, 3.0) for _ in range(dimension))
                assert loss.squared_loss(point) == pytest.approx(
                    definition.squared_loss(point),
                    rel=5.0e-13,
                    abs=5.0e-13,
                )

    def test_execute_rejects_a_rank_deficient_system_without_regularization(
        self,
    ) -> None:
        definition = WeightedAffineResidualDefinition(
            coordinate_names=("x", "y"),
            terms=(WeightedAffineResidualTerm((1.0, 1.0), 0.0, 1.0),),
        )

        with pytest.raises(ValueError):
            WeightedAffineResidualQuadraticConstructor().execute(definition)

    def test_definition_rejects_invalid_scalar_and_dimension_inputs(self) -> None:
        with pytest.raises(TypeError):
            WeightedAffineResidualTerm((True,), 0.0, 1.0)  # type: ignore[arg-type]
        with pytest.raises(ValueError):
            WeightedAffineResidualTerm((1.0,), 0.0, 0.0)
        with pytest.raises(ValueError):
            WeightedAffineResidualDefinition(
                coordinate_names=("x", "y"),
                terms=(WeightedAffineResidualTerm((1.0,), 0.0, 1.0),),
            )

    def test_direct_evaluation_rejects_overflow(self) -> None:
        definition = WeightedAffineResidualDefinition(
            coordinate_names=("x",),
            terms=(WeightedAffineResidualTerm((1.0,), 0.0, 1.0),),
        )

        with pytest.raises(ValueError, match="nonfinite"):
            definition.squared_loss((1.0e308,))
