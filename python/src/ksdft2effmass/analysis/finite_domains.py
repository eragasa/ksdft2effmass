"""Separate scalar-result contracts for finite-domain study channels.

These ResultObjects retain already-evaluated scalar diagnostics. They neither construct
operators nor execute a finite-domain campaign, and they intentionally provide no
pooled convergence status across measure, shape, orientation, and boundary phase.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from ksdft2effmass.operators import PhysicalUnit, Unitless
from ksdft2effmass.solid_state import (
    BoundaryTwistMesh,
    FiniteLatticeShape,
    LatticeDimension,
)

type FiniteDomainMetricUnit = PhysicalUnit | Unitless
"""Closed unit union for one scalar finite-domain diagnostic."""


@dataclass(frozen=True, slots=True)
class FiniteDomainScalarMetric:
    """Identify one scalar finite-domain diagnostic and its exact unit."""

    identifier: str
    unit: FiniteDomainMetricUnit

    def __post_init__(self) -> None:
        """Validate exact metric identity and supported unit."""
        if type(self.identifier) is not str:
            raise TypeError("identifier must be a string")
        if not self.identifier:
            raise ValueError("identifier must be nonempty")
        if not isinstance(self.unit, PhysicalUnit | Unitless):
            raise TypeError("unit must be PhysicalUnit or Unitless")


@dataclass(frozen=True, slots=True)
class FiniteDomainMeasureStudyResult:
    """Retain one scalar metric over an ordered increasing domain-measure sequence."""

    identifier: str
    metric: FiniteDomainScalarMetric
    shapes: tuple[FiniteLatticeShape, ...]
    values: tuple[float, ...]
    reference_shape: FiniteLatticeShape

    def __post_init__(self) -> None:
        """Validate one dimension, increasing measure, values, and final reference."""
        if type(self.identifier) is not str:
            raise TypeError("identifier must be a string")
        if not self.identifier:
            raise ValueError("identifier must be nonempty")
        if type(self.metric) is not FiniteDomainScalarMetric:
            raise TypeError("metric must be FiniteDomainScalarMetric")
        if type(self.shapes) is not tuple or any(
            type(shape) is not FiniteLatticeShape for shape in self.shapes
        ):
            raise TypeError("shapes must be a tuple of FiniteLatticeShape")
        if len(self.shapes) < 2:
            raise ValueError("measure study requires at least two shapes")
        dimension = self.shapes[0].dimension
        if any(shape.dimension is not dimension for shape in self.shapes):
            raise ValueError("measure-study shapes must share one dimension")
        measures = tuple(shape.cell_count for shape in self.shapes)
        if any(
            right <= left
            for left, right in zip(measures[:-1], measures[1:], strict=True)
        ):
            raise ValueError("measure-study cell counts must be strictly increasing")
        if type(self.values) is not tuple or any(
            type(value) is not float for value in self.values
        ):
            raise TypeError("values must be a tuple of built-in floats")
        if any(not math.isfinite(value) for value in self.values):
            raise ValueError("values must be finite")
        if len(self.values) != len(self.shapes):
            raise ValueError("values must align one-to-one with shapes")
        if type(self.reference_shape) is not FiniteLatticeShape:
            raise TypeError("reference_shape must be FiniteLatticeShape")
        if self.reference_shape != self.shapes[-1]:
            raise ValueError("reference_shape must be the final measure-study shape")

    @property
    def adjacent_changes(self) -> tuple[float, ...]:
        """Return ordered signed changes without assigning a convergence status."""
        return tuple(
            right - left
            for left, right in zip(self.values[:-1], self.values[1:], strict=True)
        )

    @property
    def final_change(self) -> float:
        """Return the final signed adjacent change."""
        return self.values[-1] - self.values[-2]


@dataclass(frozen=True, slots=True)
class FiniteDomainShapeStudyResult:
    """Retain one scalar metric over distinct geometries at fixed cell count."""

    identifier: str
    metric: FiniteDomainScalarMetric
    shapes: tuple[FiniteLatticeShape, ...]
    values: tuple[float, ...]
    reference_shape: FiniteLatticeShape

    def __post_init__(self) -> None:
        """Validate fixed measure, unique geometries, and explicit reference."""
        if type(self.identifier) is not str:
            raise TypeError("identifier must be a string")
        if not self.identifier:
            raise ValueError("identifier must be nonempty")
        if type(self.metric) is not FiniteDomainScalarMetric:
            raise TypeError("metric must be FiniteDomainScalarMetric")
        if type(self.shapes) is not tuple or any(
            type(shape) is not FiniteLatticeShape for shape in self.shapes
        ):
            raise TypeError("shapes must be a tuple of FiniteLatticeShape")
        if len(self.shapes) < 2:
            raise ValueError("shape study requires at least two geometries")
        dimension = self.shapes[0].dimension
        if dimension is LatticeDimension.ONE:
            raise ValueError(
                "nontrivial fixed-measure shape channel is inapplicable in 1D"
            )
        if len(set(self.shapes)) != len(self.shapes):
            raise ValueError("shape-study geometries must be unique")
        measure = self.shapes[0].cell_count
        if any(shape.dimension is not dimension for shape in self.shapes):
            raise ValueError("shape-study geometries must share one dimension")
        if any(shape.cell_count != measure for shape in self.shapes):
            raise ValueError("shape-study geometries must have one fixed cell count")
        if type(self.values) is not tuple or any(
            type(value) is not float for value in self.values
        ):
            raise TypeError("values must be a tuple of built-in floats")
        if any(not math.isfinite(value) for value in self.values):
            raise ValueError("values must be finite")
        if len(self.values) != len(self.shapes):
            raise ValueError("values must align one-to-one with shapes")
        if type(self.reference_shape) is not FiniteLatticeShape:
            raise TypeError("reference_shape must be FiniteLatticeShape")
        if self.reference_shape not in self.shapes:
            raise ValueError("reference_shape must occur in shape-study geometries")

    @property
    def contrasts(self) -> tuple[float, ...]:
        """Return signed contrasts relative to the declared reference geometry."""
        reference = self.values[self.shapes.index(self.reference_shape)]
        return tuple(value - reference for value in self.values)

    @property
    def spread(self) -> float:
        """Return maximum minus minimum without assigning convergence status."""
        return max(self.values) - min(self.values)


@dataclass(frozen=True, slots=True)
class FiniteDomainOrientationStudyResult:
    """Retain separate same-parent contrasts and transformed-parent residuals."""

    identifier: str
    metric: FiniteDomainScalarMetric
    shape_pairs: tuple[tuple[FiniteLatticeShape, FiniteLatticeShape], ...]
    same_parent_contrasts: tuple[float, ...]
    transformed_parent_covariance_residuals: tuple[float, ...]

    def __post_init__(self) -> None:
        """Validate paired equal-measure geometries and nonpooled outcomes."""
        if type(self.identifier) is not str:
            raise TypeError("identifier must be a string")
        if not self.identifier:
            raise ValueError("identifier must be nonempty")
        if type(self.metric) is not FiniteDomainScalarMetric:
            raise TypeError("metric must be FiniteDomainScalarMetric")
        if type(self.shape_pairs) is not tuple or not self.shape_pairs:
            raise TypeError("shape_pairs must be a nonempty tuple")
        normalized_pairs: list[tuple[FiniteLatticeShape, FiniteLatticeShape]] = []
        study_dimension: LatticeDimension | None = None
        for pair in self.shape_pairs:
            if type(pair) is not tuple or len(pair) != 2:
                raise TypeError("shape pairs must contain exactly two shapes")
            source, target = pair
            if (
                type(source) is not FiniteLatticeShape
                or type(target) is not FiniteLatticeShape
            ):
                raise TypeError("shape pairs must contain FiniteLatticeShape values")
            if source.dimension is not target.dimension:
                raise ValueError("orientation-pair dimensions must agree")
            if study_dimension is None:
                study_dimension = source.dimension
            elif source.dimension is not study_dimension:
                raise ValueError("orientation pairs must share one study dimension")
            if source.cell_count != target.cell_count:
                raise ValueError("orientation pairs must have equal cell count")
            if source == target:
                raise ValueError("orientation-pair geometries must be distinct")
            normalized_pairs.append((source, target))
        if len(set(normalized_pairs)) != len(normalized_pairs):
            raise ValueError("orientation shape pairs must be unique")
        if type(self.same_parent_contrasts) is not tuple or any(
            type(value) is not float for value in self.same_parent_contrasts
        ):
            raise TypeError("same_parent_contrasts must be a tuple of built-in floats")
        if any(not math.isfinite(value) for value in self.same_parent_contrasts):
            raise ValueError("same-parent contrasts must be finite")
        if type(self.transformed_parent_covariance_residuals) is not tuple or any(
            type(value) is not float
            for value in self.transformed_parent_covariance_residuals
        ):
            raise TypeError(
                "transformed_parent_covariance_residuals must be a tuple of floats"
            )
        if any(
            not math.isfinite(value)
            for value in self.transformed_parent_covariance_residuals
        ):
            raise ValueError("transformed-parent covariance residuals must be finite")
        if len(self.same_parent_contrasts) != len(self.shape_pairs) or len(
            self.transformed_parent_covariance_residuals
        ) != len(self.shape_pairs):
            raise ValueError(
                "orientation outcomes must align one-to-one with shape pairs"
            )
        if any(value < 0.0 for value in self.transformed_parent_covariance_residuals):
            raise ValueError(
                "transformed-parent covariance residuals must be nonnegative"
            )


@dataclass(frozen=True, slots=True)
class BoundaryPhaseStudyResult:
    """Retain one scalar metric and bound-state counts over one complete twist set."""

    identifier: str
    metric: FiniteDomainScalarMetric
    shape: FiniteLatticeShape
    mesh: BoundaryTwistMesh
    metric_values: tuple[float | None, ...]
    below_edge_state_counts: tuple[int, ...]

    def __post_init__(self) -> None:
        """Validate twist alignment, optional state metrics, counts, and unit."""
        if type(self.identifier) is not str:
            raise TypeError("identifier must be a string")
        if not self.identifier:
            raise ValueError("identifier must be nonempty")
        if type(self.metric) is not FiniteDomainScalarMetric:
            raise TypeError("metric must be FiniteDomainScalarMetric")
        if type(self.shape) is not FiniteLatticeShape:
            raise TypeError("shape must be FiniteLatticeShape")
        if type(self.mesh) is not BoundaryTwistMesh:
            raise TypeError("mesh must be BoundaryTwistMesh")
        if self.mesh.dimension is not self.shape.dimension:
            raise ValueError("twist mesh and finite shape must share one dimension")
        if type(self.metric_values) is not tuple:
            raise TypeError("metric_values must be a tuple")
        for value in self.metric_values:
            if value is not None and type(value) is not float:
                raise TypeError("metric values must be built-in floats or None")
            if value is not None and not math.isfinite(value):
                raise ValueError("available metric values must be finite")
        if type(self.below_edge_state_counts) is not tuple or any(
            type(count) is not int for count in self.below_edge_state_counts
        ):
            raise TypeError("below_edge_state_counts must be a tuple of built-in ints")
        if any(count < 0 for count in self.below_edge_state_counts):
            raise ValueError("below-edge state counts must be nonnegative")
        if (
            len(self.metric_values) != self.mesh.point_count
            or len(self.below_edge_state_counts) != self.mesh.point_count
        ):
            raise ValueError(
                "boundary-phase values and counts must align with the mesh"
            )
        if any(
            value is None and count != 0
            for value, count in zip(
                self.metric_values, self.below_edge_state_counts, strict=True
            )
        ):
            raise ValueError("unavailable state metrics require zero below-edge states")

    @property
    def no_bound_state_count(self) -> int:
        """Return the number of retained twists with no below-edge state."""
        return sum(count == 0 for count in self.below_edge_state_counts)

    @property
    def band_center(self) -> float | None:
        """Return the mean available metric value, or ``None`` when unavailable."""
        available = tuple(value for value in self.metric_values if value is not None)
        if not available:
            return None
        return math.fsum(available) / float(len(available))

    @property
    def band_width(self) -> float | None:
        """Return available maximum minus minimum, or ``None`` when unavailable."""
        available = tuple(value for value in self.metric_values if value is not None)
        if not available:
            return None
        return max(available) - min(available)
