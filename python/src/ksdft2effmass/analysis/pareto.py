"""Exact sampled Pareto classification for prespecified finite objective sets."""

from __future__ import annotations

import math


def _objective_rows(
    objectives: tuple[tuple[float, ...], ...],
) -> tuple[tuple[float, ...], ...]:
    """Validate one nonempty finite rectangular objective inventory."""
    if type(objectives) is not tuple or not objectives:
        raise TypeError("objectives must be a nonempty tuple")
    dimension: int | None = None
    for point in objectives:
        if type(point) is not tuple or not point:
            raise TypeError("every objective point must be a nonempty tuple")
        if dimension is None:
            dimension = len(point)
        elif len(point) != dimension:
            raise ValueError("objective points must have one common dimension")
        for value in point:
            if type(value) is not float:
                raise TypeError("objective values must be built-in floats")
            if not math.isfinite(value):
                raise ValueError("objective values must be finite")
    return objectives


def _dominates(candidate: tuple[float, ...], point: tuple[float, ...]) -> bool:
    """Return exact weak-all and strict-any minimization dominance."""
    return all(
        left <= right for left, right in zip(candidate, point, strict=True)
    ) and any(left < right for left, right in zip(candidate, point, strict=True))


class SampledParetoClassifier:
    """Classify a finite prespecified minimization set without tolerance or fitting."""

    __slots__ = ()

    def execute(
        self,
        objectives: tuple[tuple[float, ...], ...],
    ) -> tuple[bool, ...]:
        """Return one nondominance flag per objective point in supplied order."""
        objectives = _objective_rows(objectives)
        return tuple(
            not any(
                other_index != point_index and _dominates(other, point)
                for other_index, other in enumerate(objectives)
            )
            for point_index, point in enumerate(objectives)
        )


__all__ = ["SampledParetoClassifier"]
