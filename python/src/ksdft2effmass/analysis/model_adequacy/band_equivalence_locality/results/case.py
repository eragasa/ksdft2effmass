"""Plain immutable scientific values for case analysis."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ksdft2effmass.numerical_consistency import NumericalConsistency

from ..geometry import BandEquivalenceLocalityMetricCovarianceDefectResult
from .point import BandEquivalenceLocalityPointAnalysis


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityFlatAmplitudeResolutionAnalysis(NumericalConsistency):
    """Represent analytic flat-parent midpoint interpolation defects."""

    amplitude_intervals: int
    amplitude_nodes: int
    maximum_operator_threshold_midpoint_interpolation_defect: float
    maximum_joint_threshold_midpoint_interpolation_defect: float
    passes_unit_scale_draft_tolerance: bool | None
    tolerance_inapplicable_reason: str

    def __post_init__(self) -> None:
        if type(self.amplitude_intervals) is not int or self.amplitude_intervals <= 0:
            raise TypeError("amplitude_intervals must be a positive built-in integer")
        if type(self.amplitude_nodes) is not int or self.amplitude_nodes <= 1:
            raise TypeError(
                "amplitude_nodes must be a built-in integer greater than one"
            )
        if self.amplitude_nodes != self.amplitude_intervals + 1:
            raise ValueError("amplitude_nodes must equal amplitude_intervals + 1")
        for name, value in (
            (
                "maximum_operator_threshold_midpoint_interpolation_defect",
                self.maximum_operator_threshold_midpoint_interpolation_defect,
            ),
            (
                "maximum_joint_threshold_midpoint_interpolation_defect",
                self.maximum_joint_threshold_midpoint_interpolation_defect,
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if self.passes_unit_scale_draft_tolerance is not None and (
            type(self.passes_unit_scale_draft_tolerance) is not bool
        ):
            raise TypeError("passes_unit_scale_draft_tolerance must be bool or None")
        if type(self.tolerance_inapplicable_reason) is not str:
            raise TypeError("tolerance_inapplicable_reason must be a string")


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityAmplitudeMidpointAnalysis(NumericalConsistency):
    """Represent direct midpoint-versus-linear-interpolation defects."""

    amplitude_nodes: int
    applicable: bool
    inapplicable_reason: str | None
    endpoint_minimum_threshold_over_sqrt_splitting: float | None
    maximum_correlation_midpoint_defect: float | None
    maximum_operator_threshold_midpoint_defect: float | None
    maximum_joint_threshold_midpoint_defect: float | None
    maximum_nonzero_hopping_weight_midpoint_defect: float | None
    maximum_hopping_block_power_midpoint_defect: float | None

    def __post_init__(self) -> None:
        if type(self.amplitude_nodes) is not int or self.amplitude_nodes <= 0:
            raise TypeError("amplitude_nodes must be a positive built-in integer")
        if type(self.applicable) is not bool:
            raise TypeError("applicable must be a built-in bool")
        if (
            self.inapplicable_reason is not None
            and type(self.inapplicable_reason) is not str
        ):
            raise TypeError("inapplicable_reason must be a string or None")
        optional_values = (
            (
                "endpoint_minimum_threshold_over_sqrt_splitting",
                self.endpoint_minimum_threshold_over_sqrt_splitting,
            ),
            (
                "maximum_correlation_midpoint_defect",
                self.maximum_correlation_midpoint_defect,
            ),
            (
                "maximum_operator_threshold_midpoint_defect",
                self.maximum_operator_threshold_midpoint_defect,
            ),
            (
                "maximum_joint_threshold_midpoint_defect",
                self.maximum_joint_threshold_midpoint_defect,
            ),
            (
                "maximum_nonzero_hopping_weight_midpoint_defect",
                self.maximum_nonzero_hopping_weight_midpoint_defect,
            ),
            (
                "maximum_hopping_block_power_midpoint_defect",
                self.maximum_hopping_block_power_midpoint_defect,
            ),
        )
        for name, value in optional_values:
            if value is not None:
                if type(value) is not float:
                    raise TypeError(f"{name} must be a built-in float or None")
                if not math.isfinite(value) or value < 0.0:
                    raise ValueError(f"{name} must be finite and nonnegative")
        if self.applicable:
            if self.amplitude_nodes != 3:
                raise ValueError("an applicable midpoint analysis requires three nodes")
            if self.inapplicable_reason is not None:
                raise ValueError("an applicable midpoint analysis cannot have a reason")
            if any(value is None for _, value in optional_values):
                raise ValueError(
                    "an applicable midpoint analysis requires all diagnostics"
                )
        elif self.inapplicable_reason is None:
            raise ValueError("an inapplicable midpoint analysis requires a reason")


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityCaseAnalysis:
    """Represent all points for one interpreted geometry and parent."""

    name: str
    metric_covariance: BandEquivalenceLocalityMetricCovarianceDefectResult
    construction_evaluation_minimum_separation: float
    amplitude_midpoint: BandEquivalenceLocalityAmplitudeMidpointAnalysis
    flat_amplitude_resolution: tuple[
        BandEquivalenceLocalityFlatAmplitudeResolutionAnalysis, ...
    ]
    points: tuple[BandEquivalenceLocalityPointAnalysis, ...]

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name:
            raise TypeError("name must be a nonempty string")
        if (
            type(self.metric_covariance)
            is not BandEquivalenceLocalityMetricCovarianceDefectResult
        ):
            raise TypeError("metric_covariance has the wrong scientific result type")
        separation = self.construction_evaluation_minimum_separation
        if type(separation) is not float:
            raise TypeError(
                "construction_evaluation_minimum_separation must be a built-in float"
            )
        if not math.isfinite(separation) or separation < 0.0:
            raise ValueError(
                "construction_evaluation_minimum_separation must be finite and "
                "nonnegative"
            )
        if (
            type(self.amplitude_midpoint)
            is not BandEquivalenceLocalityAmplitudeMidpointAnalysis
        ):
            raise TypeError("amplitude_midpoint has the wrong scientific result type")
        if type(self.flat_amplitude_resolution) is not tuple or not all(
            type(item) is BandEquivalenceLocalityFlatAmplitudeResolutionAnalysis
            for item in self.flat_amplitude_resolution
        ):
            raise TypeError("flat_amplitude_resolution must contain typed results")
        if (
            type(self.points) is not tuple
            or not self.points
            or not all(
                type(point) is BandEquivalenceLocalityPointAnalysis
                for point in self.points
            )
        ):
            raise TypeError("points must be a nonempty tuple of typed point results")

    @property
    def metric_covariance_defect(self) -> float:
        """Project the typed covariance result into the historical scalar channel."""
        return self.metric_covariance.maximum_absolute_defect
