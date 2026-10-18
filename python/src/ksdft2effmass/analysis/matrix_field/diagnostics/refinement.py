"""Typed absolute-relative scalar refinement diagnostics."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ._validation import nonnegative_float


@dataclass(frozen=True, slots=True)
class ScalarRefinementDiagnostics:
    """Retain one nonnegative scalar comparison under an absolute-relative rule."""

    coarse_mesh_size: int
    fine_mesh_size: int
    coarse_value: float
    fine_value: float
    absolute_change: float
    denominator_floor: float
    relative_change: float
    absolute_tolerance: float
    relative_tolerance: float
    applied_tolerance: float
    signed_margin: float
    passes: bool

    def __post_init__(self) -> None:
        """Validate mesh order, finite values, and every derived comparison field."""
        if (
            type(self.coarse_mesh_size) is not int
            or type(self.fine_mesh_size) is not int
        ):
            raise TypeError("mesh sizes must be built-in integers")
        if self.coarse_mesh_size <= 0 or self.fine_mesh_size <= self.coarse_mesh_size:
            raise ValueError("mesh sizes must be positive and increasing")
        for name, value in (
            ("coarse_value", self.coarse_value),
            ("fine_value", self.fine_value),
            ("absolute_change", self.absolute_change),
            ("denominator_floor", self.denominator_floor),
            ("relative_change", self.relative_change),
            ("absolute_tolerance", self.absolute_tolerance),
            ("relative_tolerance", self.relative_tolerance),
            ("applied_tolerance", self.applied_tolerance),
        ):
            nonnegative_float(name, value)
        if type(self.signed_margin) is not float:
            raise TypeError("signed_margin must be a built-in float")
        if not math.isfinite(self.signed_margin):
            raise ValueError("signed_margin must be finite")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        expected_change = abs(self.fine_value - self.coarse_value)
        scale = max(
            abs(self.coarse_value),
            abs(self.fine_value),
            self.denominator_floor,
        )
        expected_relative = 0.0 if scale == 0.0 else expected_change / scale
        expected_tolerance = self.absolute_tolerance + self.relative_tolerance * max(
            abs(self.coarse_value),
            abs(self.fine_value),
        )
        expected_margin = expected_tolerance - expected_change
        if self.absolute_change != expected_change:
            raise ValueError("absolute_change is inconsistent")
        if self.relative_change != expected_relative:
            raise ValueError("relative_change is inconsistent")
        if self.applied_tolerance != expected_tolerance:
            raise ValueError("applied_tolerance is inconsistent")
        if self.signed_margin != expected_margin:
            raise ValueError("signed_margin is inconsistent")
        if self.passes is not (expected_change <= expected_tolerance):
            raise ValueError("passes is inconsistent")


class ScalarRefinementAnalyzer:
    """Apply one inclusive absolute-relative stability rule without interpretation."""

    __slots__ = ()

    def execute(
        self,
        coarse_mesh_size: int,
        fine_mesh_size: int,
        coarse_value: float,
        fine_value: float,
        denominator_floor: float,
        absolute_tolerance: float,
        relative_tolerance: float,
    ) -> ScalarRefinementDiagnostics:
        """Return values, changes, threshold, signed margin, and pass state."""
        if type(coarse_mesh_size) is not int or type(fine_mesh_size) is not int:
            raise TypeError("mesh sizes must be built-in integers")
        if coarse_mesh_size <= 0 or fine_mesh_size <= coarse_mesh_size:
            raise ValueError("mesh sizes must be positive and increasing")
        coarse_value = nonnegative_float("coarse_value", coarse_value)
        fine_value = nonnegative_float("fine_value", fine_value)
        denominator_floor = nonnegative_float("denominator_floor", denominator_floor)
        absolute_tolerance = nonnegative_float("absolute_tolerance", absolute_tolerance)
        relative_tolerance = nonnegative_float("relative_tolerance", relative_tolerance)
        change = abs(fine_value - coarse_value)
        scale = max(abs(coarse_value), abs(fine_value), denominator_floor)
        relative_change = 0.0 if scale == 0.0 else change / scale
        applied = absolute_tolerance + relative_tolerance * max(
            abs(coarse_value),
            abs(fine_value),
        )
        return ScalarRefinementDiagnostics(
            coarse_mesh_size=coarse_mesh_size,
            fine_mesh_size=fine_mesh_size,
            coarse_value=coarse_value,
            fine_value=fine_value,
            absolute_change=change,
            denominator_floor=denominator_floor,
            relative_change=relative_change,
            absolute_tolerance=absolute_tolerance,
            relative_tolerance=relative_tolerance,
            applied_tolerance=applied,
            signed_margin=applied - change,
            passes=change <= applied,
        )


__all__ = ["ScalarRefinementAnalyzer", "ScalarRefinementDiagnostics"]
