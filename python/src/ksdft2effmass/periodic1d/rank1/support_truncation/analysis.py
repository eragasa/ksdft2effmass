"""Rank-one support-truncation capability action."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

from ksdft2effmass.periodic1d.fourier_locality.result import (
    Periodic1DFourierLocalityCalculationResult,
    Periodic1DFourierLocalityMeshResult,
)
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic1d.support_truncation import (
    Periodic1DSupportTruncationAnalysis,
    Periodic1DSupportTruncationAnalysisRequest,
    Periodic1DSupportTruncationAnalyzer,
)

from .result import Periodic1DRank1SupportResult


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRank1SupportTruncationAnalysisRequest(
    Periodic1DSupportTruncationAnalysisRequest
):
    """Bind one stored scalar support-removal inventory."""

    lattice_geometry: Periodic1DLatticeGeometry
    source_calculation: Periodic1DFourierLocalityCalculationResult
    source_mesh: Periodic1DFourierLocalityMeshResult

    def __post_init__(self) -> None:
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
        if not any(
            mesh is self.source_mesh for mesh in self.source_calculation.meshes
        ):
            raise ValueError(
                "source_mesh must belong to source_calculation by identity"
            )


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRank1SupportTruncationAnalysis(
    Periodic1DSupportTruncationAnalysis
):
    """Retain transform-mediated support-removal capability values."""

    lattice_geometry: Periodic1DLatticeGeometry
    source_calculation: Periodic1DFourierLocalityCalculationResult
    source_mesh: Periodic1DFourierLocalityMeshResult
    supports: tuple[Periodic1DRank1SupportResult, ...]

    def __post_init__(self) -> None:
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
        if type(self.supports) is not tuple or any(
            type(item) is not Periodic1DRank1SupportResult for item in self.supports
        ):
            raise TypeError("supports must contain exact rank-one support results")
        if (
            tuple(item.source_range for item in self.supports)
            != self.source_mesh.ranges
        ):
            raise ValueError("supports must preserve the source range inventory")
        if any(item.source_mesh is not self.source_mesh for item in self.supports):
            raise ValueError("every support must retain the bound source mesh")
        if any(
            item.source_calculation is not self.source_calculation
            for item in self.supports
        ):
            raise ValueError("every support must retain the bound source calculation")
        if any(
            item.lattice_geometry != self.lattice_geometry for item in self.supports
        ):
            raise ValueError("every support must retain the bound lattice geometry")


@final
class Periodic1DRank1SupportTruncationAnalyzer(
    Periodic1DSupportTruncationAnalyzer[
        Periodic1DRank1SupportTruncationAnalysisRequest,
        Periodic1DRank1SupportTruncationAnalysis,
    ]
):
    """Construct support capability values from stored removal consequences."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic1DRank1SupportTruncationAnalysisRequest,
    ) -> None:
        if type(request) is not Periodic1DRank1SupportTruncationAnalysisRequest:
            raise TypeError(
                "request must be Periodic1DRank1SupportTruncationAnalysisRequest"
            )
        self._request = request

    @property
    def request(self) -> Periodic1DRank1SupportTruncationAnalysisRequest:
        """Return the exact capability request."""
        return self._request

    def execute(self) -> Periodic1DRank1SupportTruncationAnalysis:
        """Return one capability value for every stored support."""
        lattice_geometry = self._request.lattice_geometry
        source_calculation = self._request.source_calculation
        source_mesh = self._request.source_mesh
        return Periodic1DRank1SupportTruncationAnalysis(
            lattice_geometry=lattice_geometry,
            source_calculation=source_calculation,
            source_mesh=source_mesh,
            supports=tuple(
                Periodic1DRank1SupportResult(
                    lattice_geometry=lattice_geometry,
                    source_calculation=source_calculation,
                    source_mesh=source_mesh,
                    source_range=source_range,
                )
                for source_range in source_mesh.ranges
            ),
        )


__all__ = [
    "Periodic1DRank1SupportTruncationAnalysis",
    "Periodic1DRank1SupportTruncationAnalysisRequest",
    "Periodic1DRank1SupportTruncationAnalyzer",
]
