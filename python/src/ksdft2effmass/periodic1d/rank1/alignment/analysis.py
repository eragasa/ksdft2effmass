"""Rank-one scalar alignment-applicability action."""

from __future__ import annotations

from typing import final

from projectkoios.physkit.periodic.lattice import DirectLattice1D

from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityConfiguration,
)
from ksdft2effmass.periodic1d.gauge_alignment import Periodic1DGaugeAlignment
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry

from .definition import Periodic1DRank1AlignmentApplicability
from .result import Periodic1DRank1AlignmentApplicabilityResult


@final
class Periodic1DRank1AlignmentApplicabilityAnalyzer(Periodic1DGaugeAlignment):
    """Return the exact operator-trivial alignment disposition for one scalar family."""

    __slots__ = ("_lattice_geometry", "_request")

    def __init__(
        self,
        *,
        request: Periodic1DFourierLocalityConfiguration,
        lattice_geometry: Periodic1DLatticeGeometry,
    ) -> None:
        """Bind the scalar configuration and explicit lattice geometry."""
        if type(request) is not Periodic1DFourierLocalityConfiguration:
            raise TypeError("request must be Periodic1DFourierLocalityConfiguration")
        if type(lattice_geometry) is not Periodic1DLatticeGeometry:
            raise TypeError("lattice_geometry must be Periodic1DLatticeGeometry")
        self._request = request
        self._lattice_geometry = lattice_geometry

    @property
    def lattice_geometry(self) -> Periodic1DLatticeGeometry:
        """Return the explicit caller-selected lattice geometry."""
        return self._lattice_geometry

    @property
    def direct_lattice(self) -> DirectLattice1D:
        """Return the caller-selected PhysKit direct lattice."""
        return self._lattice_geometry.direct_lattice

    @property
    def request(self) -> Periodic1DFourierLocalityConfiguration:
        """Return the exact scalar-family request bound to this action."""
        return self._request

    def execute(self) -> Periodic1DRank1AlignmentApplicabilityResult:
        """Return one applicability result and no duplicate alignment calculation."""
        return Periodic1DRank1AlignmentApplicabilityResult(
            configuration=self._request,
            lattice_geometry=self._lattice_geometry,
            gauge_group_identity=(
                Periodic1DRank1AlignmentApplicabilityResult.GAUGE_GROUP_IDENTITY
            ),
            applicability=(Periodic1DRank1AlignmentApplicability.OPERATOR_TRIVIAL),
            inapplicable_alignment_controls=(
                Periodic1DRank1AlignmentApplicabilityResult.INAPPLICABLE_ALIGNMENT_CONTROLS
            ),
        )


__all__ = ["Periodic1DRank1AlignmentApplicabilityAnalyzer"]
