"""Typed classification of PhysKit lattice displacements into metric shells."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)

from .base import RealSpaceSupportTruncation
from .geometry import MetricGeometry
from .support import MetricShellSupportInventory


@dataclass(frozen=True, slots=True)
class MetricShellValueAnalysis:
    """Preserve scaled integer metric values and their rounding defect."""

    metric_shell_values: tuple[int, ...]
    maximum_rounding_defect: float
    rounding_absolute_tolerance: float

    def __post_init__(self) -> None:
        if type(self.metric_shell_values) is not tuple or not self.metric_shell_values:
            raise TypeError("metric_shell_values must be a nonempty tuple")
        if any(type(value) is not int for value in self.metric_shell_values):
            raise TypeError("metric_shell_values must contain built-in integers")
        if any(value < 0 for value in self.metric_shell_values):
            raise ValueError("metric_shell_values must be nonnegative")
        if type(self.maximum_rounding_defect) is not float:
            raise TypeError("maximum_rounding_defect must be a built-in float")
        if (
            not math.isfinite(self.maximum_rounding_defect)
            or self.maximum_rounding_defect < 0.0
        ):
            raise ValueError("maximum_rounding_defect must be finite and nonnegative")
        if type(self.rounding_absolute_tolerance) is not float:
            raise TypeError("rounding_absolute_tolerance must be a built-in float")
        if (
            not math.isfinite(self.rounding_absolute_tolerance)
            or self.rounding_absolute_tolerance <= 0.0
        ):
            raise ValueError("rounding_absolute_tolerance must be finite and positive")
        if self.maximum_rounding_defect > self.rounding_absolute_tolerance:
            raise ValueError("maximum_rounding_defect exceeds its tolerance")


@dataclass(frozen=True, slots=True)
class MetricShellValueAnalyzer(RealSpaceSupportTruncation):
    """Calculate scaled integer metric values for any finite displacement sequence."""

    rounding_absolute_tolerance: float = 1.0e-12

    def __post_init__(self) -> None:
        if type(self.rounding_absolute_tolerance) is not float:
            raise TypeError("rounding_absolute_tolerance must be a built-in float")
        if (
            not math.isfinite(self.rounding_absolute_tolerance)
            or self.rounding_absolute_tolerance <= 0.0
        ):
            raise ValueError("rounding_absolute_tolerance must be finite and positive")

    def execute(
        self,
        geometry: MetricGeometry,
        displacements: tuple[LatticeDisplacement, ...],
    ) -> MetricShellValueAnalysis:
        """Return metric values aligned with the supplied displacement order."""
        if not isinstance(geometry, MetricGeometry):
            raise TypeError("geometry must inherit MetricGeometry")
        geometry.validate_metric_geometry()
        if type(displacements) is not tuple or not displacements:
            raise TypeError("displacements must be a nonempty tuple")
        if any(type(value) is not LatticeDisplacement for value in displacements):
            raise TypeError(
                "displacements must contain exact LatticeDisplacement values"
            )
        expected_dimension = (
            LatticeDimension.TWO if geometry.dimension == 2 else LatticeDimension.THREE
        )
        if any(value.dimension is not expected_dimension for value in displacements):
            raise ValueError("displacement dimension must match the metric geometry")
        components = np.asarray(
            tuple(value.components for value in displacements),
            dtype=np.float64,
        )
        metric = geometry.direct_metric.metric_tensor
        scaled_values = geometry.shell_metric_scale * np.einsum(
            "ri,ij,rj->r",
            components,
            metric,
            components,
        )
        rounded_values = np.rint(scaled_values)
        maximum_defect = float(np.max(np.abs(scaled_values - rounded_values)))
        if maximum_defect > self.rounding_absolute_tolerance:
            raise ValueError(
                "scaled physical metric does not give integer shell values"
            )
        return MetricShellValueAnalysis(
            metric_shell_values=tuple(int(value) for value in rounded_values),
            maximum_rounding_defect=maximum_defect,
            rounding_absolute_tolerance=self.rounding_absolute_tolerance,
        )


@dataclass(frozen=True, slots=True)
class MetricShellClassification:
    """Bind ordinal support shells to their scaled integer metric values.

    ``support_inventory.ordinal_shell_indices`` are contiguous ordinal shell indices.
    The
    value analysis preserves the physical scaled-metric labels used by existing
    dimensional calculations, which need not be contiguous.
    """

    support_inventory: MetricShellSupportInventory
    value_analysis: MetricShellValueAnalysis

    def __post_init__(self) -> None:
        if type(self.support_inventory) is not MetricShellSupportInventory:
            raise TypeError("support_inventory must be MetricShellSupportInventory")
        if type(self.value_analysis) is not MetricShellValueAnalysis:
            raise TypeError("value_analysis must be MetricShellValueAnalysis")
        metric_values = self.value_analysis.metric_shell_values
        if len(metric_values) != len(self.support_inventory.displacements):
            raise ValueError(
                "metric_shell_values must align with the support inventory"
            )
        zero_position = next(
            index
            for index, displacement in enumerate(self.support_inventory.displacements)
            if displacement.is_zero
        )
        if metric_values[zero_position] != 0:
            raise ValueError("the zero displacement must have metric shell value zero")
        ordinal_to_metric: dict[int, int] = {}
        for ordinal, metric_value in zip(
            self.support_inventory.ordinal_shell_indices,
            metric_values,
            strict=True,
        ):
            previous = ordinal_to_metric.setdefault(ordinal, metric_value)
            if previous != metric_value:
                raise ValueError("one ordinal shell must have one metric value")
        if tuple(
            ordinal_to_metric[index] for index in sorted(ordinal_to_metric)
        ) != tuple(sorted(set(metric_values))):
            raise ValueError("ordinal shell order must follow metric-value order")

    @property
    def metric_shell_values(self) -> tuple[int, ...]:
        """Return scaled metric values aligned with the support inventory."""
        return self.value_analysis.metric_shell_values

    @property
    def maximum_rounding_defect(self) -> float:
        """Return the maximum scaled-metric integer-rounding defect."""
        return self.value_analysis.maximum_rounding_defect

    @property
    def rounding_absolute_tolerance(self) -> float:
        """Return the tolerance used only for metric-value integer qualification."""
        return self.value_analysis.rounding_absolute_tolerance

    def metric_shell_value_for(self, displacement: LatticeDisplacement) -> int:
        """Return the scaled integer metric value for one admitted displacement."""
        if type(displacement) is not LatticeDisplacement:
            raise TypeError("displacement must be an exact LatticeDisplacement")
        try:
            position = self.support_inventory.displacements.index(displacement)
        except ValueError as error:
            raise ValueError(
                "displacement is outside the admitted inventory"
            ) from error
        return self.metric_shell_values[position]


@dataclass(frozen=True, slots=True)
class MetricShellSupportClassifier(RealSpaceSupportTruncation):
    """Classify one conjugate-closed support using a nominal metric geometry."""

    rounding_absolute_tolerance: float = 1.0e-12

    def __post_init__(self) -> None:
        MetricShellValueAnalyzer(self.rounding_absolute_tolerance)

    def execute(
        self,
        geometry: MetricGeometry,
        displacements: tuple[LatticeDisplacement, ...],
    ) -> MetricShellClassification:
        """Return canonical ordinal shells and aligned scaled metric values."""
        value_analysis = MetricShellValueAnalyzer(
            self.rounding_absolute_tolerance
        ).execute(geometry, displacements)
        metric_values = value_analysis.metric_shell_values
        distinct_metric_values = tuple(sorted(set(metric_values)))
        ordinal_by_metric = {
            metric_value: ordinal
            for ordinal, metric_value in enumerate(distinct_metric_values)
        }
        support_inventory = MetricShellSupportInventory(
            displacements=displacements,
            ordinal_shell_indices=tuple(
                ordinal_by_metric[value] for value in metric_values
            ),
        )
        return MetricShellClassification(
            support_inventory=support_inventory,
            value_analysis=value_analysis,
        )


__all__ = [
    "MetricShellClassification",
    "MetricShellSupportClassifier",
    "MetricShellValueAnalysis",
    "MetricShellValueAnalyzer",
]
