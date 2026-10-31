"""Numerical-consistency analysis for reduced periodic tensor grids."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from .base import NumericalConsistency

type FloatArray = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class PeriodicTensorGridSeparationAnalyzer(NumericalConsistency):
    """Measure minimum torus separation between two Cartesian-product grids."""

    def execute(self, construction: FloatArray, evaluation: FloatArray) -> float:
        """Return the Euclidean combination of per-axis minimum torus distances."""
        self._validate_grid("construction", construction)
        self._validate_grid("evaluation", evaluation)
        dimension = construction.shape[-1]
        if evaluation.shape[-1] != dimension:
            raise ValueError("construction and evaluation dimensions must agree")

        squared = 0.0
        for axis in range(dimension):
            construction_index: list[int | slice] = [0] * dimension
            evaluation_index: list[int | slice] = [0] * dimension
            construction_index[axis] = slice(None)
            evaluation_index[axis] = slice(None)
            first = construction[tuple(construction_index)][..., axis]
            second = evaluation[tuple(evaluation_index)][..., axis]
            delta = second[:, None] - first[None, :]
            delta -= np.rint(delta)
            squared += float(np.min(np.abs(delta))) ** 2
        return math.sqrt(squared)

    @staticmethod
    def _validate_grid(name: str, values: FloatArray) -> None:
        if type(values) is not np.ndarray:
            raise TypeError(f"{name} must be an exact numpy.ndarray")
        if values.dtype != np.dtype(np.float64):
            raise TypeError(f"{name} must have dtype float64")
        if values.ndim < 2:
            raise ValueError(f"{name} must have tensor axes and a coordinate axis")
        dimension = values.shape[-1]
        if dimension not in (1, 2, 3) or values.ndim != dimension + 1:
            raise ValueError(
                f"{name} must have shape (axis_size, ..., axis_size, dimension)"
            )
        if any(size < 1 for size in values.shape[:-1]):
            raise ValueError(f"{name} tensor axes must be nonempty")
        if not bool(np.all(np.isfinite(values))):
            raise ValueError(f"{name} coordinates must be finite")


__all__ = ["PeriodicTensorGridSeparationAnalyzer"]
