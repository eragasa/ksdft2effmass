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
from projectkoios.physkit.units import (
    ModelSystemUnitConverter,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_scale.request import (  # noqa: E501
    Periodic1DRank2Request,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.request import (
    Periodic1DBandEquivalenceLocalityRequest,
)
from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityConfiguration,
)
from ksdft2effmass.periodic1d.geometry import (
    Periodic1DLatticeGeometry,
    Periodic1DReducedCoordinateConvention,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.configuration import (
    Periodic1DCompositeBandAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.configuration import (
    Periodic1DRankNAlignmentConfiguration,
)
from ksdft2effmass.real_space_support_truncation import SymmetricRangeSupport1D

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DLatticeGeometry:
    """Keep direct, reciprocal, and reduced-coordinate semantics explicit."""

    def test_lattice_geometry__direct_and_reciprocal_types__are_physkit_owned(
        self,
    ) -> None:
        """The immutable snapshot reconstructs the nominal PhysKit lattice types."""
        geometry = Periodic1DLatticeGeometry(
            lattice_period=2.0,
            lattice_unit=PhysicalUnit("angstrom"),
        )

        assert geometry.lattice_unit == PhysicalUnit("angstrom")
        assert type(geometry.direct_lattice) is DirectLattice1D
        assert type(geometry.reciprocal_lattice) is ReciprocalLattice1D
        assert geometry.direct_lattice.a1 == 2.0
        assert geometry.reciprocal_lattice.b1 == math.pi

    def test_from_direct_lattice__snapshots_caller_selected_period(self) -> None:
        """The immutable geometry does not retain a mutable PhysKit object."""
        direct_lattice = DirectLattice1D(2.5)

        geometry = Periodic1DLatticeGeometry.from_direct_lattice(
            direct_lattice,
            PhysicalUnit("nanometer"),
        )
        direct_lattice.lattice_constant = 9.0

        assert geometry.lattice_period == 2.5
        assert geometry.lattice_unit == PhysicalUnit("nanometer")
        assert geometry.direct_lattice.lattice_constant == 2.5

    def test_lattice_geometry__rejects_unitless_length(self) -> None:
        """A lattice period remains unit-aware even when its magnitude is one."""
        with pytest.raises(TypeError, match="PhysicalUnit"):
            Periodic1DLatticeGeometry.from_direct_lattice(
                DirectLattice1D(1.0),
                Unitless(),  # type: ignore[arg-type]
            )

    def test_lattice_geometry__rejects_nonlength_physical_unit(self) -> None:
        """Physical lattice units must carry length dimensionality."""
        with pytest.raises(ValueError, match="length dimensionality"):
            Periodic1DLatticeGeometry(
                lattice_period=1.0,
                lattice_unit=PhysicalUnit("electron_volt"),
            )

    def test_lattice_geometry__support_indices__map_through_direct_lattice(
        self,
    ) -> None:
        """A symmetric support remains indexed while geometry supplies translations."""
        geometry = Periodic1DLatticeGeometry(
            lattice_period=2.0,
            lattice_unit=PhysicalUnit("bohr"),
        )
        support = SymmetricRangeSupport1D(maximum_range=2).support

        translations = tuple(
            geometry.direct_translation(displacement)
            for displacement in support.displacements
        )

        assert tuple(value.magnitude for value in translations) == (
            -4.0,
            -2.0,
            0.0,
            2.0,
            4.0,
        )
        assert all(value.unit == PhysicalUnit("bohr") for value in translations)
        with pytest.raises(ValueError, match="dimension one"):
            geometry.direct_translation(
                LatticeDisplacement(LatticeDimension.TWO, (0, 0))
            )

    def test_lattice_geometry__q_and_k_conversion__round_trips(self) -> None:
        """Reduced q remains dimensionless and physical k uses the reciprocal basis."""
        geometry = Periodic1DLatticeGeometry(
            lattice_period=2.0,
            lattice_unit=PhysicalUnit("meter"),
        )

        wavenumber = geometry.bloch_wavenumber(0.25)

        assert wavenumber.magnitude == math.pi / 4.0
        assert ModelSystemUnitConverter.compatible(
            wavenumber.unit,
            PhysicalUnit("1 / meter"),
        )
        assert geometry.reduced_coordinate(wavenumber) == 0.25
        assert geometry.reduced_coordinate(
            ScalarQuantity(math.pi / 400.0, PhysicalUnit("1 / centimeter"))
        ) == pytest.approx(0.25, rel=0.0, abs=1.0e-15)
        with pytest.raises(ValueError, match="inverse-length"):
            geometry.reduced_coordinate(
                ScalarQuantity(1.0, PhysicalUnit("electron_volt"))
            )

    @pytest.mark.parametrize("value", [True, 1, "1"])
    def test_lattice_geometry__nonfloat_period__is_rejected(
        self, value: bool | int | str
    ) -> None:
        """Booleans, integers, and numeric strings do not enter the float contract."""
        with pytest.raises(TypeError, match="built-in float"):
            Periodic1DLatticeGeometry(
                lattice_period=value,  # type: ignore[arg-type]
                lattice_unit=PhysicalUnit("bohr"),
            )

    @pytest.mark.parametrize(
        "value",
        [0.0, -1.0, float("inf"), float("-inf"), float("nan")],
    )
    def test_lattice_geometry__nonpositive_or_nonfinite_period__is_rejected(
        self,
        value: float,
    ) -> None:
        with pytest.raises(ValueError, match="finite and positive"):
            Periodic1DLatticeGeometry(
                lattice_period=value,
                lattice_unit=PhysicalUnit("bohr"),
            )

    @pytest.mark.parametrize("value", [True, 1, "1"])
    def test_bloch_wavenumber__rejects_nonfloat_coordinates(
        self,
        value: bool | int | str,
    ) -> None:
        geometry = Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr"))

        with pytest.raises(TypeError, match="built-in float"):
            geometry.bloch_wavenumber(value)  # type: ignore[arg-type]

    @pytest.mark.parametrize("value", [float("inf"), float("-inf"), float("nan")])
    def test_bloch_wavenumber__rejects_nonfinite_coordinates(
        self,
        value: float,
    ) -> None:
        geometry = Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr"))

        with pytest.raises(ValueError, match="must be finite"):
            geometry.bloch_wavenumber(value)

    def test_reduced_coordinate__rejects_untyped_or_unitless_wavenumber(self) -> None:
        geometry = Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr"))

        with pytest.raises(TypeError, match="must be ScalarQuantity"):
            geometry.reduced_coordinate(1.0)  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="must use PhysicalUnit"):
            geometry.reduced_coordinate(ScalarQuantity(1.0, Unitless()))

    def test_reduced_coordinate_families__share_nominal_geometry_convention(
        self,
    ) -> None:
        """Maintained 1D reciprocal-mesh families no longer use structural typing."""
        for family_type in (
            Periodic1DBandEquivalenceLocalityRequest,
            Periodic1DRank2Request,
            Periodic1DFourierLocalityConfiguration,
            Periodic1DCompositeBandAlignmentConfiguration,
            Periodic1DRankNAlignmentConfiguration,
        ):
            assert issubclass(family_type, Periodic1DReducedCoordinateConvention)

    def test_reduced_coordinate_convention__uses_unit_aware_atomic_length(
        self,
    ) -> None:
        """Magnitude one retains the explicit physical atomic-length unit."""

        class ExampleConvention(Periodic1DReducedCoordinateConvention):
            __slots__ = ()

        geometry = ExampleConvention().reduced_lattice_geometry

        assert geometry.lattice_period == 1.0
        assert geometry.lattice_unit == PhysicalUnit("bohr")
        assert geometry.reciprocal_lattice.b1 == 2.0 * math.pi
