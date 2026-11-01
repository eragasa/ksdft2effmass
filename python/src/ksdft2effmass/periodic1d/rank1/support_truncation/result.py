"""Rank-one support-truncation capability values."""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.physkit.periodic.lattice import DirectLattice1D
from projectkoios.physkit.units import (
    ComplexVectorQuantity,
    ScalarQuantity,
    VectorQuantity,
)

from ksdft2effmass.periodic1d.fourier_locality.result import (
    Periodic1DFourierLocalityCalculationResult,
    Periodic1DFourierLocalityMeshResult,
    Periodic1DFourierLocalityRangeResult,
)
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic1d.support_truncation import Periodic1DSupportTruncation


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRank1SupportResult(Periodic1DSupportTruncation):
    """Represent consequences of one scalar support removal."""

    lattice_geometry: Periodic1DLatticeGeometry
    source_calculation: Periodic1DFourierLocalityCalculationResult
    source_mesh: Periodic1DFourierLocalityMeshResult
    source_range: Periodic1DFourierLocalityRangeResult

    def __post_init__(self) -> None:
        """Bind support consequences to one exact source-mesh range member."""
        if type(self.lattice_geometry) is not Periodic1DLatticeGeometry:
            raise TypeError("lattice_geometry must be Periodic1DLatticeGeometry")
        if type(self.source_calculation) is not (
            Periodic1DFourierLocalityCalculationResult
        ):
            raise TypeError(
                "source_calculation must be the exact Fourier-locality result"
            )
        if type(self.source_mesh) is not Periodic1DFourierLocalityMeshResult:
            raise TypeError(
                "source_mesh must be the exact Fourier-locality mesh result"
            )
        if not any(mesh is self.source_mesh for mesh in self.source_calculation.meshes):
            raise ValueError(
                "source_mesh must belong to source_calculation by identity"
            )
        if type(self.source_range) is not Periodic1DFourierLocalityRangeResult:
            raise TypeError(
                "source_range must be the exact Fourier-locality range result"
            )
        if not any(item is self.source_range for item in self.source_mesh.ranges):
            raise ValueError("source_range must belong to source_mesh by identity")

    @property
    def direct_lattice(self) -> DirectLattice1D:
        """Return the explicit caller-selected PhysKit direct lattice."""
        return self.lattice_geometry.direct_lattice

    @property
    def maximum_range(self) -> int:
        """Return the retained symmetric support radius."""
        return self.source_range.maximum_range

    @property
    def retained_coefficients(self) -> ComplexVectorQuantity:
        """Return the transform-mediated coefficients retained on this support."""
        return self.source_range.mediated_coefficients

    @property
    def construction_candidate(self) -> VectorQuantity:
        """Return the support-truncated construction samples."""
        return self.source_range.mediated_construction_candidate

    @property
    def evaluation_candidate(self) -> VectorQuantity:
        """Return the support-truncated disjoint evaluation samples."""
        return self.source_range.mediated_evaluation_candidate

    @property
    def truncation_maximum_error(self) -> ScalarQuantity:
        """Return the complete-to-truncated maximum error."""
        return self.source_range.truncation_maximum_error

    @property
    def truncation_rms_error(self) -> ScalarQuantity:
        """Return the complete-to-truncated RMS error."""
        return self.source_range.truncation_rms_error

    @property
    def total_maximum_error(self) -> ScalarQuantity:
        """Return the direct-to-truncated maximum error."""
        return self.source_range.mediated_total_maximum_error

    @property
    def total_rms_error(self) -> ScalarQuantity:
        """Return the direct-to-truncated RMS error."""
        return self.source_range.mediated_total_rms_error


__all__ = ["Periodic1DRank1SupportResult"]
