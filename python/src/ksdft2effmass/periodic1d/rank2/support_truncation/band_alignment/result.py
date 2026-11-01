"""Support-truncation results for the rank-two band-alignment study."""

from __future__ import annotations

import math
from dataclasses import dataclass

from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.periodic1d.support_truncation.base import (
    Periodic1DSupportTruncation,
    Periodic1DSupportTruncationAnalysis,
)
from ksdft2effmass.periodic1d.translations import (
    Periodic1DSymmetricTranslationRange,
)
from ksdft2effmass.real_space_support_truncation.support import (
    SymmetricRangeSupport1D,
)

from .request import Periodic1DRank2SupportTruncationAnalysisRequest


@dataclass(frozen=True, slots=True)
class Periodic1DRank2SupportResult(Periodic1DSupportTruncation):
    """Retain one channel's consequences of one symmetric support removal."""

    maximum_range: int
    construction_total_spectral_maximum_error: ScalarQuantity
    evaluation_truncation_hamiltonian_maximum_error: ScalarQuantity
    evaluation_total_hamiltonian_maximum_error: ScalarQuantity
    evaluation_truncation_spectral_maximum_error: ScalarQuantity
    evaluation_total_spectral_maximum_error: ScalarQuantity

    def __post_init__(self) -> None:
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if self.maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        for value, name in (
            (
                self.construction_total_spectral_maximum_error,
                "construction_total_spectral_maximum_error",
            ),
            (
                self.evaluation_truncation_hamiltonian_maximum_error,
                "evaluation_truncation_hamiltonian_maximum_error",
            ),
            (
                self.evaluation_total_hamiltonian_maximum_error,
                "evaluation_total_hamiltonian_maximum_error",
            ),
            (
                self.evaluation_truncation_spectral_maximum_error,
                "evaluation_truncation_spectral_maximum_error",
            ),
            (
                self.evaluation_total_spectral_maximum_error,
                "evaluation_total_spectral_maximum_error",
            ),
        ):
            _require_nonnegative_unitless(value, name)

    @property
    def retained_range(self) -> Periodic1DSymmetricTranslationRange:
        """Return the neutral range underlying this retained-support policy."""
        return Periodic1DSymmetricTranslationRange(self.maximum_range)

    @property
    def support_policy(self) -> SymmetricRangeSupport1D:
        """Return the typed symmetric retained-support policy."""
        return SymmetricRangeSupport1D(self.maximum_range)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRank2SupportTruncationAnalysis(Periodic1DSupportTruncationAnalysis):
    """Retain support-removal consequences for one frozen rank-two channel."""

    request: Periodic1DRank2SupportTruncationAnalysisRequest
    supports: tuple[Periodic1DRank2SupportResult, ...]

    def __post_init__(self) -> None:
        if type(self.request) is not Periodic1DRank2SupportTruncationAnalysisRequest:
            raise TypeError("request must be the exact support-truncation request")
        if type(self.supports) is not tuple or not all(
            type(item) is Periodic1DRank2SupportResult for item in self.supports
        ):
            raise TypeError("supports must contain exact support results")
        if tuple(item.retained_range for item in self.supports) != (
            self.request.configuration.support_range_inventory.ranges
        ):
            raise ValueError("supports must follow the frozen support inventory")

    def support_at_range(self, maximum_range: int) -> Periodic1DRank2SupportResult:
        """Return the unique support result for one configured range."""
        if type(maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        for result in self.supports:
            if result.maximum_range == maximum_range:
                return result
        raise ValueError("maximum_range is not in the frozen support inventory")


def _require_nonnegative_unitless(value: ScalarQuantity, name: str) -> None:
    if type(value) is not ScalarQuantity:
        raise TypeError(f"{name} must be ScalarQuantity")
    if not isinstance(value.unit, Unitless):
        raise ValueError(f"{name} must be unitless")
    if type(value.magnitude) is not float:
        raise TypeError(f"{name} magnitude must be a built-in float")
    if not math.isfinite(value.magnitude) or value.magnitude < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


__all__ = [
    "Periodic1DRank2SupportResult",
    "Periodic1DRank2SupportTruncationAnalysis",
]
