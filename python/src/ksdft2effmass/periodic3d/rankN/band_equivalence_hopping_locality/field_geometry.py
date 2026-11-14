"""Parent-independent physical-metric geometry for represented-field analysis."""

from __future__ import annotations

from dataclasses import dataclass, field

from projectkoios.physkit.periodic.lattice import (
    DirectLattice3D,
    DirectLatticeMetric,
)

from ksdft2effmass.real_space_support_truncation import BasisResolvedMetricGeometry


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityFieldGeometry(
    BasisResolvedMetricGeometry
):
    """Bind the physical metric needed for three-dimensional shell analysis."""

    identifier: str
    direct_metric: DirectLatticeMetric
    shell_metric_scale: float
    basis_offsets: tuple[tuple[float, float, float], ...] = ()
    dimension: int = field(init=False, default=3, repr=False)

    def __post_init__(self) -> None:
        """Validate geometry identity, dimensional metric, scale, and offsets."""
        if type(self.identifier) is not str:
            raise TypeError("identifier must be a built-in string")
        if not self.identifier:
            raise ValueError("identifier must be nonempty")
        if type(self.direct_metric) is not DirectLatticeMetric:
            raise TypeError("direct_metric must be DirectLatticeMetric")
        if type(self.direct_metric.direct_lattice) is not DirectLattice3D:
            raise TypeError("direct_metric must use the exact PhysKit DirectLattice3D")
        self.validate_basis_resolved_metric_geometry()


__all__ = ["Periodic3DRankNBandEquivalenceHoppingLocalityFieldGeometry"]
