"""Rank-two hopping-locality values."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ksdft2effmass.periodic1d.hopping_locality.base import (
    Periodic1DHoppingLocality,
    Periodic1DHoppingLocalityAnalysis,
)
from ksdft2effmass.periodic1d.translations import (
    Periodic1DSymmetricTranslationRange,
)

from .request import Periodic1DRank2HoppingLocalityAnalysisRequest


@dataclass(frozen=True, slots=True)
class Periodic1DRank2HoppingPower(Periodic1DHoppingLocality):
    """Retain reference and comparison block power at one displacement."""

    displacement: int
    reference_normalized_squared_frobenius_norm: float
    comparison_normalized_squared_frobenius_norm: float

    def __post_init__(self) -> None:
        if type(self.displacement) is not int:
            raise TypeError("displacement must be a built-in int")
        _require_nonnegative_float(
            self.reference_normalized_squared_frobenius_norm,
            "reference_normalized_squared_frobenius_norm",
        )
        _require_nonnegative_float(
            self.comparison_normalized_squared_frobenius_norm,
            "comparison_normalized_squared_frobenius_norm",
        )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2HoppingTailResult(Periodic1DHoppingLocality):
    """Retain one channel's unchanged omitted-block norm at one range."""

    maximum_range: int
    ordinary_omitted_block_l2_norm: float

    def __post_init__(self) -> None:
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if self.maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        _require_nonnegative_float(
            self.ordinary_omitted_block_l2_norm,
            "ordinary_omitted_block_l2_norm",
        )

    @property
    def diagnostic_range(self) -> Periodic1DSymmetricTranslationRange:
        """Return the neutral symmetric range used by this tail diagnostic."""
        return Periodic1DSymmetricTranslationRange(self.maximum_range)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRank2HoppingLocalityAnalysis(Periodic1DHoppingLocalityAnalysis):
    """Retain unchanged hopping-tail diagnostics for one frozen channel."""

    request: Periodic1DRank2HoppingLocalityAnalysisRequest
    tails: tuple[Periodic1DRank2HoppingTailResult, ...]

    def __post_init__(self) -> None:
        if type(self.request) is not Periodic1DRank2HoppingLocalityAnalysisRequest:
            raise TypeError("request must be the exact hopping-locality request")
        if type(self.tails) is not tuple or not all(
            type(item) is Periodic1DRank2HoppingTailResult for item in self.tails
        ):
            raise TypeError("tails must contain exact hopping-tail results")
        if tuple(item.diagnostic_range for item in self.tails) != (
            self.request.configuration.hopping_diagnostic_range_inventory.ranges
        ):
            raise ValueError("tails must follow the frozen locality inventory")

    def tail_at_range(self, maximum_range: int) -> Periodic1DRank2HoppingTailResult:
        """Return the unique hopping-tail result for one configured range."""
        if type(maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        for result in self.tails:
            if result.maximum_range == maximum_range:
                return result
        raise ValueError("maximum_range is not in the frozen locality inventory")


def _require_nonnegative_float(value: float, name: str) -> None:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


__all__ = [
    "Periodic1DRank2HoppingLocalityAnalysis",
    "Periodic1DRank2HoppingPower",
    "Periodic1DRank2HoppingTailResult",
]
