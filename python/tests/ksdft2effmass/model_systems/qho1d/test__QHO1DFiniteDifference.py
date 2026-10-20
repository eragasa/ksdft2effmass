r"""Software verification of ``QHO1DFiniteDifference``.

Evidence profile: routine

Bounded artifact scope: public oscillator-specific finite-difference model contract.

Facet and represented meaning

The class under test applies harmonic-oscillator physics to a reusable
``DirichletInterval`` and generic represented operators.

Intrinsic and cross-object scope

Oscillator compatibility, symmetric-domain policy, physical scaling, and represented
Hamiltonian construction are included.

VVUQ and scientific exclusions

This verifies one finite represented matrix and admissibility rules. It does not
establish continuum convergence, scientific validation, uncertainty quantification,
or human acceptance.
"""

import numpy as np
import pytest
from ksdft2effmass import model_systems
from ksdft2effmass.model_systems import (
    DirichletBoundaryCondition,
    DirichletInterval,
    UniformCartesianGrid1D,
)
from ksdft2effmass.model_systems.qho1d import (
    PhysicalUnit,
    QHO1DAnalytical,
    QHO1DFiniteDifference,
    QHO1DNondimensionalizer,
    QHO1DParameters,
    ScalarQuantity,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = QHO1DFiniteDifference


class TestQHO1DFiniteDifference:
    """Own software evidence for ``QHO1DFiniteDifference``."""

    @staticmethod
    def analytical() -> QHO1DAnalytical:
        """Return the shared dimensionless analytical model."""
        return QHO1DAnalytical(
            QHO1DNondimensionalizer().execute(hbar=1.0, mass=1.0, omega=1.0)
        )

    def test_public_api__package__exports_supported_finite_difference_model(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-011

        Requirement: QHO1DFiniteDifference is publicly exported.

        Acceptance: The package binding is the documented class object.
        """
        assert model_systems.QHO1DFiniteDifference is (QHO1DFiniteDifference)

    def test_method__hamiltonian__applies_harmonic_physics_to_interval(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-012

        Requirement: The finite-difference oscillator composes one reusable interval
        with harmonic potential and kinetic-energy operators.

        Acceptance: ``b=1`` and ``h=0.5`` produce three interior points and the exact
        declared dimensionless matrix; nonhomogeneous boundary data are rejected.
        """
        interval = DirichletInterval(
            UniformCartesianGrid1D(
                ScalarQuantity(-1.0, Unitless()),
                ScalarQuantity(1.0, Unitless()),
                ScalarQuantity(0.5, Unitless()),
            ),
            DirichletBoundaryCondition(ScalarQuantity(0.0, Unitless())),
        )
        model = QHO1DFiniteDifference(self.analytical(), interval)

        assert model.interior_points == 3
        assert model.grid_spacing == ScalarQuantity(0.5, Unitless())
        np.testing.assert_array_equal(
            model.grid_coordinates().magnitude, [-0.5, 0.0, 0.5]
        )
        np.testing.assert_array_equal(
            model.hamiltonian().to_dense().magnitude,
            np.array([[4.125, -2.0, 0.0], [-2.0, 4.0, -2.0], [0.0, -2.0, 4.125]]),
        )
        assert isinstance(model.hamiltonian().unit, Unitless)
        assert not model.hamiltonian().data.flags.writeable
        with pytest.raises(ValueError, match="requires homogeneous"):
            QHO1DFiniteDifference(
                self.analytical(),
                DirichletInterval(
                    interval.grid,
                    DirichletBoundaryCondition(ScalarQuantity(1.0, Unitless())),
                ),
            )

    def test_property__grid_spacing__converts_physical_length_units(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-016

        Requirement: The physical model accepts compatible interval length units and
        canonicalizes represented coordinates and Hamiltonians to meters and joules.

        Acceptance: A one-meter half-width represented as 100 centimeters and a
        0.5-meter spacing produce canonical meter grid values and a joule matrix.
        """
        analytical = QHO1DAnalytical(
            QHO1DParameters(
                hbar=ScalarQuantity(1.0, PhysicalUnit("joule * second")),
                mass=ScalarQuantity(1.0, PhysicalUnit("kilogram")),
                omega=ScalarQuantity(1.0, PhysicalUnit("1 / second")),
            )
        )
        model = QHO1DFiniteDifference(
            analytical,
            DirichletInterval(
                UniformCartesianGrid1D(
                    ScalarQuantity(-100.0, PhysicalUnit("centimeter")),
                    ScalarQuantity(100.0, PhysicalUnit("centimeter")),
                    ScalarQuantity(50.0, PhysicalUnit("centimeter")),
                ),
                DirichletBoundaryCondition(
                    ScalarQuantity(0.0, PhysicalUnit("meter ** -0.5"))
                ),
            ),
        )

        assert model.grid_spacing == ScalarQuantity(0.5, PhysicalUnit("meter"))
        np.testing.assert_array_equal(
            model.grid_coordinates().magnitude, [-0.5, 0.0, 0.5]
        )
        assert model.hamiltonian().unit == PhysicalUnit("joule")
