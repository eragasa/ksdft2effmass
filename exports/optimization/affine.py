"""Immutable unit-free weighted affine residuals and quadratic construction.

This module is a target-relative candidate for ``projectkoios-optimization``.  It owns
only generic unit-free mathematics.  Scientific callers remain responsible for units,
normalization, sample meaning, and acceptance policy.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass

from projectkoios.optimization._validation import finite_float, text
from projectkoios.optimization.adapters import PositiveDefiniteQuadraticLoss


@dataclass(frozen=True, slots=True)
class WeightedAffineResidualTerm:
    """One positive-weight residual ``coefficients @ x - target``."""

    coefficients: tuple[float, ...]
    target: float
    weight: float

    def __post_init__(self) -> None:
        """Normalize finite values and require a nonempty positive-weight term."""
        if type(self.coefficients) is not tuple:
            raise TypeError("coefficients must be a tuple")
        if not self.coefficients:
            raise ValueError("coefficients must be nonempty")
        coefficients = tuple(
            finite_float(value, "coefficient") for value in self.coefficients
        )
        target = finite_float(self.target, "target")
        weight = finite_float(self.weight, "weight")
        if weight <= 0.0:
            raise ValueError("weight must be positive")
        object.__setattr__(self, "coefficients", coefficients)
        object.__setattr__(self, "target", target)
        object.__setattr__(self, "weight", weight)


@dataclass(frozen=True, slots=True)
class WeightedAffineResidualDefinition:
    """Define an ordered finite unit-free weighted affine residual system.

    Weights are used exactly as supplied.  A caller that requires mean-square or other
    normalization must incorporate that normalization before construction.
    """

    coordinate_names: tuple[str, ...]
    terms: tuple[WeightedAffineResidualTerm, ...]

    def __post_init__(self) -> None:
        """Validate coordinate identity, term ownership, and common dimension."""
        if type(self.coordinate_names) is not tuple:
            raise TypeError("coordinate_names must be a tuple")
        if not self.coordinate_names:
            raise ValueError("coordinate_names must be nonempty")
        names = tuple(text(value, "coordinate name") for value in self.coordinate_names)
        if len(names) != len(set(names)):
            raise ValueError("coordinate names must be unique")
        if type(self.terms) is not tuple or any(
            type(term) is not WeightedAffineResidualTerm for term in self.terms
        ):
            raise TypeError("terms must be a tuple of WeightedAffineResidualTerm")
        if not self.terms:
            raise ValueError("terms must be nonempty")
        if any(len(term.coefficients) != len(names) for term in self.terms):
            raise ValueError("every residual term must match the coordinate dimension")
        object.__setattr__(self, "coordinate_names", names)

    @property
    def dimension(self) -> int:
        """Return the positive coordinate dimension."""
        return len(self.coordinate_names)

    def squared_loss(self, coordinates: tuple[float, ...], /) -> float:
        """Evaluate the weighted residual sum directly and fail on overflow."""
        if type(coordinates) is not tuple:
            raise TypeError("coordinates must be a tuple")
        if len(coordinates) != self.dimension:
            raise ValueError("coordinate dimension must match the residual definition")
        values = tuple(finite_float(value, "coordinate") for value in coordinates)
        contributions: list[float] = []
        for term in self.terms:
            products = tuple(
                _finite_product(coefficient, value, "affine product")
                for coefficient, value in zip(term.coefficients, values, strict=True)
            )
            residual = _finite_sum(products, "affine value") - term.target
            if not math.isfinite(residual):
                raise ValueError("affine residual is nonfinite")
            contributions.append(
                _weighted_product(
                    term.weight,
                    residual,
                    residual,
                    "weighted squared residual",
                )
            )
        return _finite_sum(contributions, "weighted squared loss")


class WeightedAffineResidualQuadraticConstructor:
    """Construct the strictly positive-definite completed-square representation."""

    __slots__ = ()

    def execute(
        self,
        definition: WeightedAffineResidualDefinition,
        *,
        sparse: bool = False,
    ) -> PositiveDefiniteQuadraticLoss:
        """Return a dense or sparse quadratic for one full-column-rank definition.

        The action forms the normal matrix with deterministic scalar summation, solves
        only for the represented center, and evaluates the minimum from the original
        residual definition.  Rank-deficient or numerically non-positive-definite
        systems fail rather than being regularized.
        """
        if type(definition) is not WeightedAffineResidualDefinition:
            raise TypeError("definition must be WeightedAffineResidualDefinition")
        if type(sparse) is not bool:
            raise TypeError("sparse must be a built-in bool")

        dimension = definition.dimension
        rows = [[0.0 for _ in range(dimension)] for _ in range(dimension)]
        for first in range(dimension):
            for second in range(first, dimension):
                products = tuple(
                    _weighted_product(
                        term.weight,
                        term.coefficients[first],
                        term.coefficients[second],
                        "weighted normal-matrix product",
                    )
                    for term in definition.terms
                )
                value = _finite_sum(products, "normal matrix entry")
                rows[first][second] = value
                rows[second][first] = value
        matrix = tuple(tuple(row) for row in rows)

        right_hand_side = tuple(
            _finite_sum(
                tuple(
                    _weighted_product(
                        term.weight,
                        term.coefficients[index],
                        term.target,
                        "weighted normal-equation product",
                    )
                    for term in definition.terms
                ),
                "normal-equation right-hand side entry",
            )
            for index in range(dimension)
        )
        if not all(math.isfinite(value) for value in right_hand_side):
            raise ValueError("normal-equation right-hand side is nonfinite")

        # NumPy is an explicit optional dependency, imported only by this action.
        import numpy as np

        try:
            center_values = np.linalg.solve(
                np.asarray(matrix, dtype=np.float64),
                np.asarray(right_hand_side, dtype=np.float64),
            )
        except np.linalg.LinAlgError as error:
            raise ValueError(
                "affine residual system must have full represented column rank"
            ) from error
        center = tuple(float(value) for value in center_values)
        if not all(math.isfinite(value) for value in center):
            raise ValueError("quadratic center is nonfinite")
        minimum_squared_loss = definition.squared_loss(center)
        return PositiveDefiniteQuadraticLoss(
            center,
            matrix,
            minimum_squared_loss,
            sparse=sparse,
        )


def _weighted_product(
    weight: float,
    first: float,
    second: float,
    name: str,
) -> float:
    product = first * second
    if math.isfinite(product) and (
        abs(product) >= sys.float_info.min
        or (product == 0.0 and (first == 0.0 or second == 0.0))
    ):
        result = weight * product
        if math.isfinite(result) and (
            abs(result) >= sys.float_info.min or (result == 0.0 and product == 0.0)
        ):
            return result
    scale = math.sqrt(weight)
    scaled_first = _finite_product(scale, first, name)
    scaled_second = _finite_product(scale, second, name)
    return _finite_product(scaled_first, scaled_second, name)


def _finite_product(first: float, second: float, name: str) -> float:
    """Return one binary64 product and reject overflow."""
    result = first * second
    if not math.isfinite(result):
        raise ValueError(f"{name} is nonfinite")
    return result


def _finite_sum(values: tuple[float, ...] | list[float], name: str) -> float:
    """Return one checked high-quality floating sum."""
    try:
        result = math.fsum(values)
    except OverflowError as error:
        raise ValueError(f"{name} is nonfinite") from error
    if not math.isfinite(result):
        raise ValueError(f"{name} is nonfinite")
    return result


__all__ = [
    "WeightedAffineResidualDefinition",
    "WeightedAffineResidualQuadraticConstructor",
    "WeightedAffineResidualTerm",
]
