"""Software contracts for PhysKit-backed periodic-2D lattice geometry."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    DirectLattice3D,
    DirectLatticeMetric,
    ReciprocalLattice2D,
)
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)
from projectkoios.physkit.units import PhysicalUnit, Unitless, VectorQuantity

from ksdft2effmass.periodic2d.geometry import Periodic2DLatticeGeometry

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DLatticeGeometry:
    """Keep direct, reciprocal, and reduced-coordinate semantics explicit."""

    @staticmethod
    def _direct_lattice() -> DirectLattice2D:
        return DirectLattice2D(
            a1=np.array((2.0, 0.0), dtype=np.float64),
            a2=np.array((0.5, 3.0), dtype=np.float64),
        )

    @classmethod
    def _geometry(cls) -> Periodic2DLatticeGeometry:
        return Periodic2DLatticeGeometry.from_direct_lattice(
            cls._direct_lattice(),
            PhysicalUnit("angstrom"),
        )

    def test__direct_and_reciprocal_types__are_physkit_owned(self) -> None:
        geometry = self._geometry()

        assert type(geometry.direct_lattice) is DirectLattice2D
        assert type(geometry.reciprocal_lattice) is ReciprocalLattice2D
        assert type(geometry.direct_metric) is DirectLatticeMetric
        np.testing.assert_array_equal(
            geometry.direct_lattice.A,
            self._direct_lattice().A,
        )
        np.testing.assert_allclose(
            geometry.direct_lattice.A.T @ geometry.reciprocal_lattice.primitive_basis,
            2.0 * np.pi * np.eye(2),
            rtol=0.0,
            atol=1.0e-14,
        )

    def test__from_direct_lattice__snapshots_primitive_vectors(self) -> None:
        direct_lattice = self._direct_lattice()
        geometry = Periodic2DLatticeGeometry.from_direct_lattice(
            direct_lattice,
            PhysicalUnit("bohr"),
        )

        replacement = direct_lattice.A.copy()
        replacement[0, 0] = 9.0

        assert geometry.primitive_basis_rows == ((2.0, 0.5), (0.0, 3.0))
        assert geometry.direct_lattice.A[0, 0] == 2.0

    def test__support_indices__map_through_direct_lattice(self) -> None:
        geometry = self._geometry()
        displacement = LatticeDisplacement(LatticeDimension.TWO, (1, -2))

        translation = geometry.direct_translation(displacement)

        np.testing.assert_array_equal(translation.magnitude, np.array((1.0, -6.0)))
        assert translation.unit == PhysicalUnit("angstrom")
        with pytest.raises(ValueError, match="dimension two"):
            geometry.direct_translation(
                LatticeDisplacement(LatticeDimension.THREE, (0, 0, 0))
            )

    def test__reduced_and_physical_wavevectors__round_trip(self) -> None:
        geometry = self._geometry()
        reduced = (0.25, -0.125)

        wavevector = geometry.bloch_wavevector(reduced)

        assert wavevector.magnitude.shape == (2,)
        assert geometry.reduced_coordinates(wavevector) == pytest.approx(
            reduced,
            rel=0.0,
            abs=1.0e-15,
        )
        centimeter_wavevector = VectorQuantity(
            wavevector.magnitude * 1.0e8,
            PhysicalUnit("1 / centimeter"),
        )
        assert geometry.reduced_coordinates(centimeter_wavevector) == pytest.approx(
            reduced,
            rel=0.0,
            abs=1.0e-15,
        )

    def test__rejects_wrong_lattice_type_units_and_scalar_contracts(self) -> None:
        with pytest.raises(TypeError, match="DirectLattice2D"):
            Periodic2DLatticeGeometry.from_direct_lattice(
                DirectLattice3D(  # type: ignore[arg-type]
                    a1=np.array((1.0, 0.0, 0.0)),
                    a2=np.array((0.0, 1.0, 0.0)),
                    a3=np.array((0.0, 0.0, 1.0)),
                ),
                PhysicalUnit("bohr"),
            )
        with pytest.raises(TypeError, match="PhysicalUnit"):
            Periodic2DLatticeGeometry.from_direct_lattice(
                self._direct_lattice(),
                Unitless(),  # type: ignore[arg-type]
            )
        with pytest.raises(ValueError, match="length dimensionality"):
            Periodic2DLatticeGeometry(
                primitive_basis_rows=((1.0, 0.0), (0.0, 1.0)),
                lattice_unit=PhysicalUnit("electron_volt"),
            )
        with pytest.raises(TypeError, match="built-in floats"):
            Periodic2DLatticeGeometry(
                primitive_basis_rows=((1.0, 0.0), (0.0, True)),
                lattice_unit=PhysicalUnit("bohr"),
            )
        with pytest.raises(TypeError, match="built-in floats"):
            self._geometry().bloch_wavevector((0.0, 1))
        with pytest.raises(TypeError, match="must use PhysicalUnit"):
            self._geometry().reduced_coordinates(
                VectorQuantity(np.array((0.0, 0.0)), Unitless())
            )
