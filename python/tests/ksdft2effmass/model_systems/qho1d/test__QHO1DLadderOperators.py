r"""Software verification of ``QHO1DLadderOperators``.

Evidence profile: routine

Bounded artifact scope: public harmonic energy scaling of a retained ladder basis.

Facet and represented meaning

The class under test owns the declared public QHO1DLadderOperators
contract.

Intrinsic and cross-object scope

Generic ladder-basis correlation, analytical scaling, units, and immutability are
included.

VVUQ and scientific exclusions

This verifies finite represented operators. It does not identify a finite commutator
with the infinite-dimensional canonical algebra and establishes no scientific
validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest
from ksdft2effmass import model_systems
from ksdft2effmass.model_systems.qho1d import (
    PhysicalUnit,
    QHO1DAnalytical,
    QHO1DLadderOperators,
    QHO1DNondimensionalizer,
    QHO1DParameters,
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.operators import LadderOperator1D

pytestmark = pytest.mark.software_verification
SUT = QHO1DLadderOperators


class TestQHO1DLadderOperators:
    """Own software evidence for ``QHO1DLadderOperators``."""

    @staticmethod
    def model() -> QHO1DLadderOperators:
        """Return a three-state dimensionless retained ladder model."""
        analytical = QHO1DAnalytical(
            QHO1DNondimensionalizer().execute(hbar=1.0, mass=1.0, omega=1.0)
        )
        return QHO1DLadderOperators(analytical, LadderOperator1D(3))

    def test_public_api__package__exports_supported_ladder_model(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-013

        Requirement: QHO1DLadderOperators is publicly exported.

        Acceptance: The package binding is the documented class object.
        """
        assert model_systems.QHO1DLadderOperators is (QHO1DLadderOperators)

    def test_method__hamiltonian__exposes_retained_ladder_contract(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-014

        Requirement: The oscillator-specific model composes a generic retained
        ladder basis and applies the analytical oscillator energy scale.

        Acceptance: In the dimensionless three-state basis, ``H`` is exactly
        ``diag(0.5,1.5,2.5)``, retains Unitless, and is immutable.
        """
        model = self.model()

        np.testing.assert_array_equal(
            model.hamiltonian().to_dense().magnitude, np.diag([0.5, 1.5, 2.5])
        )
        assert isinstance(model.hamiltonian().unit, Unitless)
        assert not model.hamiltonian().data.flags.writeable

    def test_method__hamiltonian__retains_physical_energy_unit(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-017

        Requirement: The retained ladder Hamiltonian carries the physical energy unit
        derived from compatible action and inverse-time parameters.

        Acceptance: ``hbar=2 J*s`` and ``omega=3/s`` produce diagonal energies
        ``(3, 9) J`` while ladder and number operators remain Unitless.
        """
        analytical = QHO1DAnalytical(
            QHO1DParameters(
                hbar=ScalarQuantity(2.0, PhysicalUnit("joule * second")),
                mass=ScalarQuantity(1.0, PhysicalUnit("kilogram")),
                omega=ScalarQuantity(3.0, PhysicalUnit("1 / second")),
            )
        )
        model = QHO1DLadderOperators(analytical, LadderOperator1D(2))

        np.testing.assert_array_equal(
            model.hamiltonian().to_dense().magnitude, np.diag([3.0, 9.0])
        )
        assert model.hamiltonian().unit == PhysicalUnit("joule")
        assert isinstance(model.annihilation().unit, Unitless)
        assert isinstance(model.number().unit, Unitless)
