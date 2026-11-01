"""Rank-two hopping-locality values."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ksdft2effmass.periodic1d.hopping_locality import Periodic1DHoppingLocality


@dataclass(frozen=True, slots=True)
class Periodic1DRank2HoppingPower(Periodic1DHoppingLocality):
    """Retain reference and comparison block power at one displacement."""

    displacement: int
    reference_normalized_squared_frobenius_norm: float
    comparison_normalized_squared_frobenius_norm: float

    def __post_init__(self) -> None:
        if type(self.displacement) is not int:
            raise TypeError("displacement must be a built-in int")
        self._require_nonnegative_float(
            self.reference_normalized_squared_frobenius_norm,
            "reference_normalized_squared_frobenius_norm",
        )
        self._require_nonnegative_float(
            self.comparison_normalized_squared_frobenius_norm,
            "comparison_normalized_squared_frobenius_norm",
        )

    @staticmethod
    def _require_nonnegative_float(value: float, name: str) -> None:
        if type(value) is not float:
            raise TypeError(f"{name} must be a built-in float")
        if not math.isfinite(value) or value < 0.0:
            raise ValueError(f"{name} must be finite and nonnegative")


__all__ = ["Periodic1DRank2HoppingPower"]
