"""Transparent diagnostics for contrasting errors within an ordered spectrum."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SpectralDispersionContrast:
    r"""Compare declared low- and high-mode relative errors with explicit bounds.

    The diagnostic is observed when

    .. math::

       e_{\mathrm{low}} \leq \tau_{\mathrm{low}}
       \quad\text{and}\quad
       e_{\mathrm{high}} \geq \tau_{\mathrm{high}},

    where each quantity is a dimensionless relative error. The caller identifies the
    represented modes and owns both reference bounds. The class does not select modes,
    solve an eigenproblem, or assign verification or scientific-validity status.

    Parameters
    ----------
    low_mode_relative_error : float
        Finite nonnegative relative error for the caller-identified low mode.
    high_mode_relative_error : float
        Finite nonnegative relative error for the caller-identified high mode.
    low_mode_maximum_relative_error : float
        Finite nonnegative upper reference bound for the low-mode error.
    high_mode_minimum_relative_error : float
        Finite nonnegative lower reference bound for the high-mode error. It must
        exceed ``low_mode_maximum_relative_error`` so the two regimes are distinct.

    Notes
    -----
    A positive :attr:`error_difference` and :attr:`is_observed` are descriptive facts
    under the supplied bounds. They are not convergence proofs, error estimates for
    uncomputed modes, validation evidence, or acceptance decisions.
    """

    low_mode_relative_error: float
    high_mode_relative_error: float
    low_mode_maximum_relative_error: float
    high_mode_minimum_relative_error: float

    def __post_init__(self) -> None:
        """Reject wrong runtime types, non-finite values, and unordered bounds."""
        for name, value in (
            ("low_mode_relative_error", self.low_mode_relative_error),
            ("high_mode_relative_error", self.high_mode_relative_error),
            (
                "low_mode_maximum_relative_error",
                self.low_mode_maximum_relative_error,
            ),
            (
                "high_mode_minimum_relative_error",
                self.high_mode_minimum_relative_error,
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if (
            self.high_mode_minimum_relative_error
            <= self.low_mode_maximum_relative_error
        ):
            raise ValueError(
                "high_mode_minimum_relative_error must exceed "
                "low_mode_maximum_relative_error"
            )

    @property
    def low_mode_condition_satisfied(self) -> bool:
        """Return whether the low-mode error is at or below its supplied bound."""
        return self.low_mode_relative_error <= self.low_mode_maximum_relative_error

    @property
    def high_mode_condition_satisfied(self) -> bool:
        """Return whether the high-mode error is at or above its supplied bound."""
        return self.high_mode_relative_error >= self.high_mode_minimum_relative_error

    @property
    def is_observed(self) -> bool:
        """Return whether both caller-defined contrast conditions are satisfied."""
        return self.low_mode_condition_satisfied and self.high_mode_condition_satisfied

    @property
    def error_difference(self) -> float:
        """Return high-mode minus low-mode relative error."""
        return self.high_mode_relative_error - self.low_mode_relative_error
