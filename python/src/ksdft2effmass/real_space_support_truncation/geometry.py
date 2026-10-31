"""Nominal metric geometry admitted by real-space support analysis."""

from __future__ import annotations

import math
from abc import ABC

from projectkoios.physkit.periodic.lattice import DirectLatticeMetric


class MetricGeometry(ABC):  # noqa: B024 - intentionally nominal geometry owner
    """Nominal contract for KSD-owned metric-shell classification.

    PhysKit owns the direct-lattice metric. KSD owns the dimension-to-metric
    correlation and the scale used to identify complete metric shells. Concrete
    calculation families retain their own serialization and evidence identities.
    """

    __slots__ = ()

    dimension: int
    direct_metric: DirectLatticeMetric
    shell_metric_scale: float

    def validate_metric_geometry(self) -> None:
        """Validate the shared dimension, direct metric, and shell scale."""
        if type(self.dimension) is not int or self.dimension not in (2, 3):
            raise ValueError("dimension must be the built-in integer 2 or 3")
        if type(self.direct_metric) is not DirectLatticeMetric:
            raise TypeError("direct_metric must be DirectLatticeMetric")
        if self.direct_metric.dimension != self.dimension:
            raise ValueError("direct metric dimension must match the geometry")
        if type(self.shell_metric_scale) is not float:
            raise TypeError("shell_metric_scale must be a built-in float")
        if not math.isfinite(self.shell_metric_scale):
            raise ValueError("shell_metric_scale must be finite")
        if self.shell_metric_scale <= 0.0:
            raise ValueError("shell_metric_scale must be positive")


class BasisResolvedMetricGeometry(MetricGeometry):  # noqa: B024 - intentionally nominal geometry owner
    """Metric geometry with explicit basis offsets for distance diagnostics."""

    __slots__ = ()

    basis_offsets: tuple[tuple[float, ...], ...]

    def validate_basis_resolved_metric_geometry(self) -> None:
        """Validate metric geometry and its aligned finite basis offsets."""
        self.validate_metric_geometry()
        if type(self.basis_offsets) is not tuple:
            raise TypeError("basis_offsets must be a tuple")
        if any(
            type(offset) is not tuple
            or len(offset) != self.dimension
            or any(
                type(component) is not float or not math.isfinite(component)
                for component in offset
            )
            for offset in self.basis_offsets
        ):
            raise TypeError(
                "basis_offsets must contain finite built-in float tuples matching "
                "dimension"
            )


__all__ = ["BasisResolvedMetricGeometry", "MetricGeometry"]
