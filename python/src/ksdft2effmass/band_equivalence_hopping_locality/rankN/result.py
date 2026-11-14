"""Dimension-neutral immutable value parents for periodic rank-N aggregates."""

from __future__ import annotations

import math
from dataclasses import dataclass


def _nonnegative_float(value: float, name: str) -> None:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class PeriodicRankNBandEquivalenceHoppingLocalityErrorChannels:
    """Retain dimension-neutral rank-normalized aggregate error channels."""

    maximum_matrix_frobenius: float
    root_mean_square_matrix_frobenius: float
    maximum_ordered_spectrum: float
    root_mean_square_ordered_spectrum: float

    def __post_init__(self) -> None:
        for name, value in (
            ("maximum_matrix_frobenius", self.maximum_matrix_frobenius),
            (
                "root_mean_square_matrix_frobenius",
                self.root_mean_square_matrix_frobenius,
            ),
            ("maximum_ordered_spectrum", self.maximum_ordered_spectrum),
            (
                "root_mean_square_ordered_spectrum",
                self.root_mean_square_ordered_spectrum,
            ),
        ):
            _nonnegative_float(value, name)


@dataclass(frozen=True, slots=True)
class PeriodicRankNBandEquivalenceHoppingLocalityLocalitySummary:
    """Retain dimension-neutral total, onsite, and non-onsite powers."""

    total_power: float
    onsite_power: float
    nononsite_power: float

    def __post_init__(self) -> None:
        for name, value in (
            ("total_power", self.total_power),
            ("onsite_power", self.onsite_power),
            ("nononsite_power", self.nononsite_power),
        ):
            _nonnegative_float(value, name)
        if abs(self.total_power - self.onsite_power - self.nononsite_power) > 1.0e-12:
            raise ValueError("locality powers must satisfy total = onsite + nononsite")


@dataclass(frozen=True, slots=True)
class PeriodicRankNSupportSelected:
    """Retain one minimum tolerance-satisfying metric shell."""

    ordinal_shell_index: int
    metric_shell_value: int
    satisfying_error: float
    preceding_error: float | None

    def __post_init__(self) -> None:
        for value, name in (
            (self.ordinal_shell_index, "ordinal_shell_index"),
            (self.metric_shell_value, "metric_shell_value"),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if value < 0:
                raise ValueError(f"{name} must be nonnegative")
        _nonnegative_float(self.satisfying_error, "satisfying_error")
        if self.preceding_error is not None:
            _nonnegative_float(self.preceding_error, "preceding_error")
        if (self.ordinal_shell_index == 0) is not (self.preceding_error is None):
            raise ValueError("preceding_error must be absent exactly at shell zero")


@dataclass(frozen=True, slots=True)
class PeriodicRankNSupportUnresolved:
    """Retain dimension-neutral unresolved support-selection evidence."""

    comparison_count: int
    minimum_observed_error: float
    largest_support_error: float

    def __post_init__(self) -> None:
        if type(self.comparison_count) is not int:
            raise TypeError("comparison_count must be a built-in integer")
        if self.comparison_count <= 0:
            raise ValueError("comparison_count must be positive")
        _nonnegative_float(self.minimum_observed_error, "minimum_observed_error")
        _nonnegative_float(self.largest_support_error, "largest_support_error")
        if self.minimum_observed_error > self.largest_support_error:
            raise ValueError(
                "minimum_observed_error cannot exceed largest_support_error"
            )


@dataclass(frozen=True, slots=True)
class PeriodicRankNFittedAlignmentEvidence:
    """Retain dimension-neutral invariant fitted-alignment evidence."""

    sample_count: int
    minimum_numerical_rank: int
    minimum_cross_singular_value: float
    maximum_optimal_residual_frobenius_norm: float
    maximum_applied_rank_cutoff: float

    def __post_init__(self) -> None:
        for value, name in (
            (self.sample_count, "sample_count"),
            (self.minimum_numerical_rank, "minimum_numerical_rank"),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        for name, float_value in (
            ("minimum_cross_singular_value", self.minimum_cross_singular_value),
            (
                "maximum_optimal_residual_frobenius_norm",
                self.maximum_optimal_residual_frobenius_norm,
            ),
            ("maximum_applied_rank_cutoff", self.maximum_applied_rank_cutoff),
        ):
            _nonnegative_float(float_value, name)


@dataclass(frozen=True, slots=True)
class PeriodicRankNPrescribedAlignmentEvidence:
    """Identify a prescribed identity or construction-oracle alignment."""

    identifier: str

    def __post_init__(self) -> None:
        if type(self.identifier) is not str or not self.identifier:
            raise TypeError("identifier must be a nonempty built-in string")
        if self.identifier not in ("identity", "known-inverse-oracle"):
            raise ValueError("identifier must be one prescribed alignment")


__all__ = [
    "PeriodicRankNBandEquivalenceHoppingLocalityErrorChannels",
    "PeriodicRankNBandEquivalenceHoppingLocalityLocalitySummary",
    "PeriodicRankNFittedAlignmentEvidence",
    "PeriodicRankNPrescribedAlignmentEvidence",
    "PeriodicRankNSupportSelected",
    "PeriodicRankNSupportUnresolved",
]
