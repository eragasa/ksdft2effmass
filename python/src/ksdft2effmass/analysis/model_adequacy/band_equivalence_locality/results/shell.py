"""Plain immutable scientific values for shell analysis."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .channels import BandEquivalenceLocalityErrorChannels


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityShellAnalysis:
    """Represent all diagnostics at one complete metric-shell cutoff."""

    shell_index: int
    retained_blocks: int
    reference_truncation: BandEquivalenceLocalityErrorChannels
    comparison_truncation: BandEquivalenceLocalityErrorChannels
    reference_total: BandEquivalenceLocalityErrorChannels
    comparison_total: BandEquivalenceLocalityErrorChannels
    reference_shell_power: float
    comparison_shell_power: float
    reference_omitted_power: float
    comparison_omitted_power: float
    reference_total_omitted_power: float
    comparison_total_omitted_power: float
    reference_truncation_parseval_defect: float
    comparison_truncation_parseval_defect: float

    def __post_init__(self) -> None:
        if type(self.shell_index) is not int or self.shell_index < 0:
            raise TypeError("shell_index must be a nonnegative built-in integer")
        if type(self.retained_blocks) is not int or self.retained_blocks <= 0:
            raise TypeError("retained_blocks must be a positive built-in integer")
        for name, channel in (
            ("reference_truncation", self.reference_truncation),
            ("comparison_truncation", self.comparison_truncation),
            ("reference_total", self.reference_total),
            ("comparison_total", self.comparison_total),
        ):
            if type(channel) is not BandEquivalenceLocalityErrorChannels:
                raise TypeError(f"{name} must be BandEquivalenceLocalityErrorChannels")
        for name, power in (
            ("reference_shell_power", self.reference_shell_power),
            ("comparison_shell_power", self.comparison_shell_power),
            ("reference_omitted_power", self.reference_omitted_power),
            ("comparison_omitted_power", self.comparison_omitted_power),
            ("reference_total_omitted_power", self.reference_total_omitted_power),
            ("comparison_total_omitted_power", self.comparison_total_omitted_power),
            (
                "reference_truncation_parseval_defect",
                self.reference_truncation_parseval_defect,
            ),
            (
                "comparison_truncation_parseval_defect",
                self.comparison_truncation_parseval_defect,
            ),
        ):
            if type(power) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(power) or power < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityFirstPassingDecision:
    """Name one first-passing complete shell or an unresolved sampled decision."""

    tolerance: float
    reference_band_shell: int | None
    comparison_band_shell: int | None
    reference_hamiltonian_shell: int | None
    comparison_hamiltonian_shell: int | None
    reference_band_passing_error: float | None
    reference_band_preceding_error: float | None
    comparison_band_passing_error: float | None
    comparison_band_preceding_error: float | None
    reference_hamiltonian_passing_error: float | None
    reference_hamiltonian_preceding_error: float | None
    comparison_hamiltonian_passing_error: float | None
    comparison_hamiltonian_preceding_error: float | None

    def __post_init__(self) -> None:
        if type(self.tolerance) is not float:
            raise TypeError("tolerance must be a built-in float")
        if not math.isfinite(self.tolerance) or self.tolerance < 0.0:
            raise ValueError("tolerance must be finite and nonnegative")
        for name, shell in (
            ("reference_band_shell", self.reference_band_shell),
            ("comparison_band_shell", self.comparison_band_shell),
            ("reference_hamiltonian_shell", self.reference_hamiltonian_shell),
            ("comparison_hamiltonian_shell", self.comparison_hamiltonian_shell),
        ):
            if shell is not None and (type(shell) is not int or shell < 0):
                raise TypeError(f"{name} must be a nonnegative integer or None")
        for name, error in (
            ("reference_band_passing_error", self.reference_band_passing_error),
            ("reference_band_preceding_error", self.reference_band_preceding_error),
            ("comparison_band_passing_error", self.comparison_band_passing_error),
            (
                "comparison_band_preceding_error",
                self.comparison_band_preceding_error,
            ),
            (
                "reference_hamiltonian_passing_error",
                self.reference_hamiltonian_passing_error,
            ),
            (
                "reference_hamiltonian_preceding_error",
                self.reference_hamiltonian_preceding_error,
            ),
            (
                "comparison_hamiltonian_passing_error",
                self.comparison_hamiltonian_passing_error,
            ),
            (
                "comparison_hamiltonian_preceding_error",
                self.comparison_hamiltonian_preceding_error,
            ),
        ):
            if error is not None:
                if type(error) is not float:
                    raise TypeError(f"{name} must be a built-in float or None")
                if not math.isfinite(error) or error < 0.0:
                    raise ValueError(f"{name} must be finite and nonnegative")
