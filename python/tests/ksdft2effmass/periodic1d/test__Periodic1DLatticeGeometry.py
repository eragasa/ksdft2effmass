"""Software contracts for PhysKit-backed periodic-1D lattice geometry."""

from __future__ import annotations

import math

import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice1D,
    ReciprocalLattice1D,
)
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)

from ksdft2effmass.periodic1d import (
    Periodic1DBandEquivalenceLocalityRequest,
    Periodic1DCompositeBandAlignmentConfiguration,
    Periodic1DHigherRankAlignmentConfiguration,
    Periodic1DLatticeGeometry,
    Periodic1DRank2Request,
    Periodic1DReducedCoordinateConvention,
)
from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityConfiguration,
)
from ksdft2effmass.real_space_support_truncation import SymmetricRangeSupport1D

pytestmark = pytest.mark.software_verification


class TestPeriodic1DLatticeGeometry:
    """Keep direct, reciprocal, and reduced-coordinate semantics explicit."""

    def test_lattice_geometry__direct_and_reciprocal_types__are_physkit_owned(
        self,
    ) -> None:
        """The immutable snapshot reconstructs the nominal PhysKit lattice types."""
        geometry = Periodic1DLatticeGeometry(lattice_period=2.0)

        assert type(geometry.direct_lattice) is DirectLattice1D
        assert type(geometry.reciprocal_lattice) is ReciprocalLattice1D
        assert geometry.direct_lattice.a1 == 2.0
        assert geometry.reciprocal_lattice.b1 == math.pi

    def test_lattice_geometry__support_indices__map_through_direct_lattice(
        self,
    ) -> None:
        """A symmetric support remains indexed while geometry supplies translations."""
        geometry = Periodic1DLatticeGeometry(lattice_period=2.0)
        support = SymmetricRangeSupport1D(maximum_range=2).support

        translations = tuple(
            geometry.direct_translation(displacement)
            for displacement in support.displacements
        )

        assert translations == (-4.0, -2.0, 0.0, 2.0, 4.0)
        with pytest.raises(ValueError, match="dimension one"):
            geometry.direct_translation(
                LatticeDisplacement(LatticeDimension.TWO, (0, 0))
            )

    def test_lattice_geometry__q_and_k_conversion__round_trips(self) -> None:
        """Reduced q remains dimensionless and physical k uses the reciprocal basis."""
        geometry = Periodic1DLatticeGeometry(lattice_period=2.0)

        wavenumber = geometry.bloch_wavenumber(0.25)

        assert wavenumber == math.pi / 4.0
        assert geometry.reduced_coordinate(wavenumber) == 0.25

    @pytest.mark.parametrize("value", [True, 1, "1"])
    def test_lattice_geometry__nonfloat_period__is_rejected(
        self, value: bool | int | str
    ) -> None:
        """Booleans, integers, and numeric strings do not enter the float contract."""
        with pytest.raises(TypeError, match="built-in float"):
            Periodic1DLatticeGeometry(lattice_period=value)  # type: ignore[arg-type]

    def test_reduced_coordinate_families__share_nominal_geometry_convention(
        self,
    ) -> None:
        """Maintained 1D reciprocal-mesh families no longer use structural typing."""
        for family_type in (
            Periodic1DBandEquivalenceLocalityRequest,
            Periodic1DRank2Request,
            Periodic1DFourierLocalityConfiguration,
            Periodic1DCompositeBandAlignmentConfiguration,
            Periodic1DHigherRankAlignmentConfiguration,
        ):
            assert issubclass(family_type, Periodic1DReducedCoordinateConvention)

    def test_reduced_coordinate_convention__uses_named_unit_period_normalization(
        self,
    ) -> None:
        """The common convention names a reduced unit, not a physical lattice claim."""

        class ExampleConvention(Periodic1DReducedCoordinateConvention):
            __slots__ = ()

        geometry = ExampleConvention().reduced_lattice_geometry

        assert geometry.lattice_period == 1.0
        assert geometry.reciprocal_lattice.b1 == 2.0 * math.pi
