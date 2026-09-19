r"""Software verification of ``HarmonicOscillatorLadderOperators``.

Evidence profile: routine

Bounded artifact scope: public harmonic energy scaling of a retained ladder basis.

Facet and represented meaning

The class under test owns the declared public HarmonicOscillatorLadderOperators
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

from ksdft2effmass.analysis import model_systems
from ksdft2effmass.analysis.model_systems.harmonic_oscillator import (
    HarmonicOscillatorAnalytical,
    HarmonicOscillatorLadderOperators,
    HarmonicOscillatorNondimensionalizer,
    HarmonicOscillatorParameters,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.operators import LadderOperator1D

pytestmark = pytest.mark.software_verification
SUT = HarmonicOscillatorLadderOperators


class TestHarmonicOscillatorLadderOperators:
    """Own software evidence for ``HarmonicOscillatorLadderOperators``."""

    @staticmethod
    def model() -> HarmonicOscillatorLadderOperators:
        """Return a three-state dimensionless retained ladder model."""
        analytical = HarmonicOscillatorAnalytical(
            HarmonicOscillatorNondimensionalizer().execute(
                hbar=1.0, mass=1.0, omega=1.0
            )
        )
        return HarmonicOscillatorLadderOperators(analytical, LadderOperator1D(3))

    def test_public_api__package__exports_supported_ladder_model(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-013

        Requirement: HarmonicOscillatorLadderOperators is publicly exported.

        Acceptance: The package binding is the documented class object.
        """
        assert model_systems.HarmonicOscillatorLadderOperators is (
            HarmonicOscillatorLadderOperators
        )

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
        analytical = HarmonicOscillatorAnalytical(
            HarmonicOscillatorParameters(
                hbar=ScalarQuantity(2.0, PhysicalUnit("joule * second")),
                mass=ScalarQuantity(1.0, PhysicalUnit("kilogram")),
                omega=ScalarQuantity(3.0, PhysicalUnit("1 / second")),
            )
        )
        model = HarmonicOscillatorLadderOperators(analytical, LadderOperator1D(2))

        np.testing.assert_array_equal(
            model.hamiltonian().to_dense().magnitude, np.diag([3.0, 9.0])
        )
        assert model.hamiltonian().unit == PhysicalUnit("joule")
        assert isinstance(model.annihilation().unit, Unitless)
        assert isinstance(model.number().unit, Unitless)
