"""Shared immutable records for independent PIAB1D verification reports.

The records preserve numerical channel defects, collection-derived counts, source and
numerical separation, and the core discarded-sector condition. They contain no
campaign calculation behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import numpy as np

from .source import Piab1dSourceAuthenticationResult


@dataclass(frozen=True, slots=True)
class Piab1dVerificationCheck:
    """Retain one numerical channel defect and inclusive tolerance.

    Parameters
    ----------
    channel
        Member of the campaign's closed verification-channel enumeration.
    maximum_defect
        Finite nonnegative defect in the channel's documented convention.
    inclusive_tolerance
        Finite nonnegative inclusive threshold in the same convention.
    """

    channel: StrEnum
    maximum_defect: float
    inclusive_tolerance: float

    def __post_init__(self) -> None:
        """Reject fields outside their exact declared runtime domains."""
        if not isinstance(self.channel, StrEnum):
            raise TypeError("channel must be a StrEnum member")
        for name, value in (
            ("maximum_defect", self.maximum_defect),
            ("inclusive_tolerance", self.inclusive_tolerance),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")

    @property
    def passes(self) -> bool:
        """Return whether the defect satisfies its inclusive threshold."""
        return self.maximum_defect <= self.inclusive_tolerance


@dataclass(frozen=True, slots=True)
class Piab1dVerificationCount:
    """Retain one positive count derived from a decoded collection.

    Parameters
    ----------
    name
        Stable nonempty count identifier.
    value
        Positive collection-derived count.
    """

    name: str
    value: int

    def __post_init__(self) -> None:
        """Reject malformed count names and values."""
        if type(self.name) is not str or not self.name:
            raise TypeError("name must be a nonempty string")
        if type(self.value) is not int:
            raise TypeError("value must be a built-in int")
        if self.value <= 0:
            raise ValueError("value must be positive")


@dataclass(frozen=True, slots=True)
class Piab1dNumericalVerificationResult:
    """Retain a complete numerical reconstruction outcome.

    Parameters
    ----------
    checks
        Exactly one check for every member of ``expected_channels``.
    expected_channels
        Complete closed channel enumeration in deterministic order.
    counts
        Optional collection-derived counts.
    discarded_sector_is_resolved
        Core-only resolution state, or ``None`` for other campaigns.
    discarded_sector_expected
        Core-only truncation expectation, or ``None`` for other campaigns.
    """

    checks: tuple[Piab1dVerificationCheck, ...]
    expected_channels: tuple[StrEnum, ...]
    counts: tuple[Piab1dVerificationCount, ...] = ()
    discarded_sector_is_resolved: bool | None = None
    discarded_sector_expected: bool | None = None

    def __post_init__(self) -> None:
        """Validate complete channels, unique counts, and optional core state."""
        if type(self.checks) is not tuple or any(
            type(check) is not Piab1dVerificationCheck for check in self.checks
        ):
            raise TypeError("checks must contain verification checks")
        if type(self.expected_channels) is not tuple or not self.expected_channels:
            raise TypeError("expected_channels must be a nonempty tuple")
        channel_type = type(self.expected_channels[0])
        if not issubclass(channel_type, StrEnum) or any(
            type(channel) is not channel_type for channel in self.expected_channels
        ):
            raise TypeError("expected_channels must contain one exact StrEnum type")
        channels = tuple(check.channel for check in self.checks)
        if len(set(channels)) != len(channels):
            raise ValueError("verification channels must be unique")
        if channels != self.expected_channels:
            raise ValueError("verification channels must be complete and ordered")
        if type(self.counts) is not tuple or any(
            type(count) is not Piab1dVerificationCount for count in self.counts
        ):
            raise TypeError("counts must contain verification counts")
        names = tuple(count.name for count in self.counts)
        if len(set(names)) != len(names):
            raise ValueError("verification count names must be unique")
        for name, value in (
            ("discarded_sector_is_resolved", self.discarded_sector_is_resolved),
            ("discarded_sector_expected", self.discarded_sector_expected),
        ):
            if value is not None and type(value) is not bool:
                raise TypeError(f"{name} must be a built-in bool or None")
        if (self.discarded_sector_is_resolved is None) is not (
            self.discarded_sector_expected is None
        ):
            raise ValueError("discarded-sector states must both be present or absent")

    @property
    def discarded_sector_condition_satisfied(self) -> bool:
        """Return agreement of the optional resolved and expected core states."""
        return self.discarded_sector_is_resolved is self.discarded_sector_expected

    @property
    def passes(self) -> bool:
        """Return whether every channel and optional core condition passes."""
        return self.discarded_sector_condition_satisfied and all(
            check.passes for check in self.checks
        )

    @property
    def check_count(self) -> int:
        """Return the number of numerical channels."""
        return len(self.checks)

    def count(self, name: str) -> int:
        """Return one collection-derived count by its exact identifier.

        Parameters
        ----------
        name
            Exact count identifier.

        Returns
        -------
        int
            Positive decoded collection size.

        Raises
        ------
        TypeError
            If ``name`` is not a built-in string.
        KeyError
            If the report does not contain ``name``.
        """
        if type(name) is not str:
            raise TypeError("name must be a built-in string")
        for count in self.counts:
            if count.name == name:
                return count.value
        raise KeyError(name)


@dataclass(frozen=True, slots=True)
class Piab1dVerificationResult:
    """Retain separate source-authentication and numerical outcomes."""

    source_authentication: Piab1dSourceAuthenticationResult
    numerical_reconstruction: Piab1dNumericalVerificationResult

    def __post_init__(self) -> None:
        """Reject constituent values outside their exact AbstractResultObject types."""
        if type(self.source_authentication) is not Piab1dSourceAuthenticationResult:
            raise TypeError("source_authentication has the wrong type")
        if type(self.numerical_reconstruction) is not Piab1dNumericalVerificationResult:
            raise TypeError("numerical_reconstruction has the wrong type")

    @property
    def passes(self) -> bool:
        """Return true only when source and numerical outcomes both pass."""
        return (
            self.source_authentication.passes and self.numerical_reconstruction.passes
        )
