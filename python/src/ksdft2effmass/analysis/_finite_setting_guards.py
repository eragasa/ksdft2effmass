"""Private finite-setting comparison and two-sided-guard analysis contracts.

These revisable records represent observed finite-setting evidence only.  They do not
select a production setting, bound an infinite-setting limit, classify calculator
warnings, authorize execution, or establish scientific validation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FiniteSettingCriteria:
    """Positive thresholds for five scalar finite-setting comparison channels."""

    energy: float
    pressure_and_max_stress_component: float
    fixed_point_band_and_gap: float

    def __post_init__(self) -> None:
        for value, name in (
            (self.energy, "energy"),
            (
                self.pressure_and_max_stress_component,
                "pressure_and_max_stress_component",
            ),
            (self.fixed_point_band_and_gap, "fixed_point_band_and_gap"),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")


@dataclass(frozen=True, slots=True)
class FiniteSettingPasses:
    """Pass/fail findings for all five finite-setting comparison channels."""

    energy: bool
    pressure: bool
    stress: bool
    fixed_point_band_at_printed_precision: bool
    fixed_point_gap_at_printed_precision: bool

    def __post_init__(self) -> None:
        if any(
            type(value) is not bool
            for value in (
                self.energy,
                self.pressure,
                self.stress,
                self.fixed_point_band_at_printed_precision,
                self.fixed_point_gap_at_printed_precision,
            )
        ):
            raise TypeError("finite-setting pass values must be built-in bool values")

    @property
    def all_pass(self) -> bool:
        """Return whether every represented comparison channel passes."""
        return all(
            (
                self.energy,
                self.pressure,
                self.stress,
                self.fixed_point_band_at_printed_precision,
                self.fixed_point_gap_at_printed_precision,
            )
        )


@dataclass(frozen=True, slots=True)
class FiniteSettingComparison:
    """One adjacent-setting comparison in explicitly declared channel units."""

    from_label: str
    to_label: str
    energy_change: float
    pressure_change: float
    maximum_stress_component_change: float
    maximum_fixed_point_band_change: float
    maximum_fixed_point_gap_change: float
    passes: FiniteSettingPasses

    def __post_init__(self) -> None:
        if type(self.from_label) is not str or type(self.to_label) is not str:
            raise TypeError("comparison labels must be built-in str values")
        if not self.from_label or not self.to_label:
            raise ValueError("comparison labels must not be empty")
        if self.from_label == self.to_label:
            raise ValueError("comparison endpoints must be distinct")
        for value, name in (
            (self.energy_change, "energy_change"),
            (self.pressure_change, "pressure_change"),
            (
                self.maximum_stress_component_change,
                "maximum_stress_component_change",
            ),
            (self.maximum_fixed_point_band_change, "maximum_fixed_point_band_change"),
            (self.maximum_fixed_point_gap_change, "maximum_fixed_point_gap_change"),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if type(self.passes) is not FiniteSettingPasses:
            raise TypeError("passes must be FiniteSettingPasses")


@dataclass(frozen=True, slots=True)
class FiniteSettingSeries:
    """One contiguous ordered adjacent-setting comparison series."""

    name: str
    comparisons: tuple[FiniteSettingComparison, ...]

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name:
            raise ValueError("series name must be a nonempty built-in str")
        if type(self.comparisons) is not tuple or any(
            type(value) is not FiniteSettingComparison for value in self.comparisons
        ):
            raise TypeError("comparisons must be a tuple of FiniteSettingComparison")
        if len(self.comparisons) < 2:
            raise ValueError("a guarded series requires at least two comparisons")
        if any(
            left.to_label != right.from_label
            for left, right in zip(
                self.comparisons[:-1], self.comparisons[1:], strict=True
            )
        ):
            raise ValueError("comparison series must form one contiguous chain")

    @property
    def candidate_labels(self) -> tuple[str, ...]:
        """Return ordered labels implied by the contiguous comparison chain."""
        return (self.comparisons[0].from_label,) + tuple(
            value.to_label for value in self.comparisons
        )


@dataclass(frozen=True, slots=True)
class FiniteSettingGuardAnalysis:
    """Validated series and every interior setting with two passing guards."""

    criteria: FiniteSettingCriteria
    series: FiniteSettingSeries
    guarded_labels: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.criteria) is not FiniteSettingCriteria:
            raise TypeError("criteria must be FiniteSettingCriteria")
        if type(self.series) is not FiniteSettingSeries:
            raise TypeError("series must be FiniteSettingSeries")
        if type(self.guarded_labels) is not tuple or any(
            type(value) is not str for value in self.guarded_labels
        ):
            raise TypeError("guarded_labels must be a tuple of built-in str values")
        candidates = self.series.candidate_labels[1:-1]
        if any(value not in candidates for value in self.guarded_labels):
            raise ValueError("guarded labels must be interior series candidates")


@dataclass(frozen=True, slots=True)
class FiniteSettingGuardAnalyzer:
    """Recompute retained flags and derive settings with lower and upper guards."""

    arithmetic_allowance: float = 1e-9

    def __post_init__(self) -> None:
        if type(self.arithmetic_allowance) is not float:
            raise TypeError("arithmetic_allowance must be a built-in float")
        if not math.isfinite(self.arithmetic_allowance):
            raise ValueError("arithmetic_allowance must be finite")
        if self.arithmetic_allowance < 0.0:
            raise ValueError("arithmetic_allowance must be nonnegative")

    def execute(
        self, criteria: FiniteSettingCriteria, series: FiniteSettingSeries
    ) -> FiniteSettingGuardAnalysis:
        """Validate exact pass flags and return two-sided guarded labels.

        ``arithmetic_allowance`` removes subtraction noise at a declared printed-value
        boundary; it does not enlarge the scientific criterion.
        """
        if type(criteria) is not FiniteSettingCriteria:
            raise TypeError("criteria must be FiniteSettingCriteria")
        if type(series) is not FiniteSettingSeries:
            raise TypeError("series must be FiniteSettingSeries")
        for comparison in series.comparisons:
            expected = self._expected_passes(criteria, comparison)
            if comparison.passes != expected:
                raise ValueError(
                    "retained criteria flags disagree with values for "
                    f"{comparison.from_label}->{comparison.to_label}"
                )
        guarded = tuple(
            series.comparisons[index].to_label
            for index in range(len(series.comparisons) - 1)
            if series.comparisons[index].passes.all_pass
            and series.comparisons[index + 1].passes.all_pass
        )
        return FiniteSettingGuardAnalysis(criteria, series, guarded)

    def _expected_passes(
        self, criteria: FiniteSettingCriteria, comparison: FiniteSettingComparison
    ) -> FiniteSettingPasses:
        """Apply the five declared threshold comparisons."""
        tolerance = criteria.fixed_point_band_and_gap
        return FiniteSettingPasses(
            energy=comparison.energy_change <= criteria.energy,
            pressure=(
                comparison.pressure_change <= criteria.pressure_and_max_stress_component
            ),
            stress=(
                comparison.maximum_stress_component_change
                <= criteria.pressure_and_max_stress_component
            ),
            fixed_point_band_at_printed_precision=(
                comparison.maximum_fixed_point_band_change <= tolerance
                or math.isclose(
                    comparison.maximum_fixed_point_band_change,
                    tolerance,
                    rel_tol=0.0,
                    abs_tol=self.arithmetic_allowance,
                )
            ),
            fixed_point_gap_at_printed_precision=(
                comparison.maximum_fixed_point_gap_change <= tolerance
                or math.isclose(
                    comparison.maximum_fixed_point_gap_change,
                    tolerance,
                    rel_tol=0.0,
                    abs_tol=self.arithmetic_allowance,
                )
            ),
        )
