"""Immutable unit-free positive diagonal metric geometry.

Physical callers must nondimensionalize coordinates and metric entries before crossing
this boundary.  The object assigns no physical interpretation or acceptance policy.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass

from projectkoios.optimization._validation import finite_float, text


@dataclass(frozen=True, slots=True)
class PositiveDiagonalMetric:
    """Represent one named strictly positive diagonal metric."""

    coordinate_names: tuple[str, ...]
    diagonal: tuple[float, ...]

    def __post_init__(self) -> None:
        """Validate identity, dimension, and strict positivity."""
        if type(self.coordinate_names) is not tuple:
            raise TypeError("coordinate_names must be a tuple")
        if not self.coordinate_names:
            raise ValueError("coordinate_names must be nonempty")
        names = tuple(text(value, "coordinate name") for value in self.coordinate_names)
        if len(names) != len(set(names)):
            raise ValueError("coordinate names must be unique")
        if type(self.diagonal) is not tuple:
            raise TypeError("diagonal must be a tuple")
        values = tuple(finite_float(value, "metric entry") for value in self.diagonal)
        if len(values) != len(names):
            raise ValueError("metric dimension must match coordinate names")
        if any(value <= 0.0 for value in values):
            raise ValueError("metric entries must be strictly positive")
        object.__setattr__(self, "coordinate_names", names)
        object.__setattr__(self, "diagonal", values)

    @property
    def dimension(self) -> int:
        """Return the positive coordinate dimension."""
        return len(self.diagonal)

    def squared_distance(
        self,
        left: tuple[float, ...],
        right: tuple[float, ...],
        /,
    ) -> float:
        """Return ``(left-right)^T M (left-right)``."""
        left_values = self._coordinates(left, "left")
        right_values = self._coordinates(right, "right")
        contributions: list[float] = []
        for weight, first, second in zip(
            self.diagonal, left_values, right_values, strict=True
        ):
            difference = first - second
            if not math.isfinite(difference):
                raise ValueError("coordinate difference is nonfinite")
            contributions.append(
                _weighted_square(weight, difference, "metric contribution")
            )
        return _finite_sum(contributions, "squared distance")

    def distance(
        self,
        left: tuple[float, ...],
        right: tuple[float, ...],
        /,
    ) -> float:
        """Return the nonnegative metric distance."""
        return _norm(self._primal_components(left, right), "distance")

    def squared_dual_norm(self, covector: tuple[float, ...], /) -> float:
        """Return ``u^T M^{-1} u`` for one finite covector."""
        values = self._coordinates(covector, "covector")
        contributions = [
            _divided_square(value, weight, "dual-metric contribution")
            for weight, value in zip(self.diagonal, values, strict=True)
        ]
        return _finite_sum(contributions, "squared dual norm")

    def dual_norm(self, covector: tuple[float, ...], /) -> float:
        """Return the nonnegative dual norm ``sqrt(u^T M^{-1}u)``."""
        return _norm(self._dual_components(covector), "dual norm")

    def _primal_components(
        self,
        left: tuple[float, ...],
        right: tuple[float, ...],
    ) -> tuple[float, ...]:
        """Return ``sqrt(M) (left-right)`` without premature squaring."""
        left_values = self._coordinates(left, "left")
        right_values = self._coordinates(right, "right")
        components: list[float] = []
        for weight, first, second in zip(
            self.diagonal, left_values, right_values, strict=True
        ):
            difference = first - second
            if not math.isfinite(difference):
                raise ValueError("coordinate difference is nonfinite")
            components.append(
                _finite_product(
                    math.sqrt(weight),
                    difference,
                    "scaled coordinate difference",
                )
            )
        return tuple(components)

    def _dual_components(self, covector: tuple[float, ...]) -> tuple[float, ...]:
        """Return ``M^(-1/2) u`` without premature squaring."""
        values = self._coordinates(covector, "covector")
        components: list[float] = []
        for weight, value in zip(self.diagonal, values, strict=True):
            component = value / math.sqrt(weight)
            if not math.isfinite(component):
                raise ValueError("scaled dual component is nonfinite")
            components.append(component)
        return tuple(components)

    def _coordinates(self, value: tuple[float, ...], name: str) -> tuple[float, ...]:
        """Normalize one exact-dimensional coordinate tuple."""
        if type(value) is not tuple:
            raise TypeError(f"{name} must be a tuple")
        if len(value) != self.dimension:
            raise ValueError(f"{name} dimension must match the metric")
        return tuple(finite_float(item, f"{name} coordinate") for item in value)


def _norm(values: tuple[float, ...], name: str) -> float:
    result = math.hypot(*values)
    if not math.isfinite(result):
        raise ValueError(f"{name} is nonfinite")
    return result


def _weighted_square(weight: float, value: float, name: str) -> float:
    square = value * value
    if math.isfinite(square) and (
        abs(square) >= sys.float_info.min or (square == 0.0 and value == 0.0)
    ):
        result = weight * square
        if math.isfinite(result) and (
            abs(result) >= sys.float_info.min or (result == 0.0 and square == 0.0)
        ):
            return result
    scaled = _finite_product(math.sqrt(weight), value, name)
    return _finite_product(scaled, scaled, name)


def _divided_square(value: float, weight: float, name: str) -> float:
    square = value * value
    if math.isfinite(square) and (
        abs(square) >= sys.float_info.min or (square == 0.0 and value == 0.0)
    ):
        result = square / weight
        if math.isfinite(result) and (
            abs(result) >= sys.float_info.min or (result == 0.0 and square == 0.0)
        ):
            return result
    scaled = value / math.sqrt(weight)
    if not math.isfinite(scaled):
        raise ValueError(f"{name} is nonfinite")
    return _finite_product(scaled, scaled, name)


def _finite_product(first: float, second: float, name: str) -> float:
    result = first * second
    if not math.isfinite(result):
        raise ValueError(f"{name} is nonfinite")
    return result


def _finite_sum(values: list[float], name: str) -> float:
    try:
        result = math.fsum(values)
    except OverflowError as error:
        raise ValueError(f"{name} is nonfinite") from error
    if not math.isfinite(result):
        raise ValueError(f"{name} is nonfinite")
    return result


__all__ = ["PositiveDiagonalMetric"]
