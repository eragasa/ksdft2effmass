"""Rank-one hopping-locality capability values."""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.physkit.periodic.lattice import DirectLattice1D
from projectkoios.physkit.units import ComplexVectorQuantity, ScalarQuantity

from ksdft2effmass.periodic1d.fourier_locality.result import (
    Periodic1DFourierLocalityCalculationResult,
    Periodic1DFourierLocalityMeshResult,
    Periodic1DFourierLocalityRangeResult,
)
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic1d.hopping_locality import Periodic1DHoppingLocality


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRank1HoppingTailResult(Periodic1DHoppingLocality):
    """Represent one scalar hopping tail without truncating the model."""

    lattice_geometry: Periodic1DLatticeGeometry
    source_calculation: Periodic1DFourierLocalityCalculationResult
    source_mesh: Periodic1DFourierLocalityMeshResult
    source_range: Periodic1DFourierLocalityRangeResult

    def __post_init__(self) -> None:
        """Bind the capability value to one exact source-mesh range member."""
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
        """Return the coefficient-tail boundary."""
        return self.source_range.maximum_range

    @property
    def complete_coefficients(self) -> ComplexVectorQuantity:
        """Return the unchanged complete scalar Fourier coefficients."""
        return self.source_mesh.complete_coefficients

    @property
    def omitted_coefficient_l2_norm(self) -> ScalarQuantity:
        """Return the stored coefficient-tail L2 norm."""
        return self.source_range.omitted_coefficient_l2_norm


__all__ = ["Periodic1DRank1HoppingTailResult"]
