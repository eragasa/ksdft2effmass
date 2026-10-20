r"""Software verification of ``QHO1DAnalytical``.

Evidence profile: routine

Bounded artifact scope: public exact-energy and number-state evaluation contract.

Facet and represented meaning

The class under test owns the declared public QHO1DAnalytical contract.

Intrinsic and cross-object scope

Intrinsic representation and directly documented compatibility behavior are included.

VVUQ and scientific exclusions

This verifies represented software behavior for dimensionless synthetic inputs. It does
not establish continuum convergence, scientific validation, uncertainty
quantification, or human acceptance.
"""

import numpy as np
import pytest
from ksdft2effmass import model_systems
from ksdft2effmass.model_systems.qho1d import (
    PhysicalUnit,
    QHO1DAnalytical,
    QHO1DNondimensionalizer,
    QHO1DParameters,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

pytestmark = pytest.mark.software_verification
SUT = QHO1DAnalytical


class TestQHO1DAnalytical:
    """Own software evidence for ``QHO1DAnalytical``."""

    @staticmethod
    def model() -> QHO1DAnalytical:
        """Return the dimensionless exact oscillator model."""
        return QHO1DAnalytical(
            QHO1DNondimensionalizer().execute(hbar=1.0, mass=1.0, omega=1.0)
        )

    def test_public_api__package__exports_supported_analytical_model(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-009

        Requirement: QHO1DAnalytical is available from the supported
        model-systems package.

        Acceptance: The package binding is the documented class object.
        """
        assert model_systems.QHO1DAnalytical is QHO1DAnalytical

    def test_method__number_state_wavefunctions__returns_unit_aware_exact_states(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-010

        Requirement: The analytical model returns ordered exact energies and sampled
        normalized Hermite states as immutable binary64 arrays.

        Acceptance: For the dimensionless model, the first three energies are
        ``(0.5, 1.5, 2.5)`` and the ground state at zero is ``pi**(-1/4)``; returned
        arrays reject mutation.
        """
        model = self.model()
        energies = model.number_state_energies(3)
        states = model.number_state_wavefunctions(
            VectorQuantity(np.array([0.0]), Unitless()), 1
        )

        np.testing.assert_array_equal(energies.magnitude, np.array([0.5, 1.5, 2.5]))
        np.testing.assert_allclose(states.magnitude, np.array([[np.pi ** (-0.25)]]))
        assert isinstance(energies.unit, Unitless)
        assert isinstance(states.unit, Unitless)
        assert not energies.magnitude.flags.writeable
        assert not states.magnitude.flags.writeable
        with pytest.raises(ValueError, match="read-only"):
            energies.magnitude[0] = 1.0

    def test_method__number_state_energies__retains_physical_energy_unit(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-015

        Requirement: The analytical model converts compatible physical parameter
        units to its canonical energy and wavefunction units.

        Acceptance: ``hbar=1 J*s``, ``m=1 kg``, and ``omega=1/s`` produce ground
        energy ``0.5 J`` and a coordinate-space wavefunction in ``m**-0.5``.
        """
        model = QHO1DAnalytical(
            QHO1DParameters(
                hbar=ScalarQuantity(1.0, PhysicalUnit("joule * second")),
                mass=ScalarQuantity(1.0, PhysicalUnit("kilogram")),
                omega=ScalarQuantity(1.0, PhysicalUnit("1 / second")),
            )
        )

        assert model.number_state_energies(1).unit == PhysicalUnit("joule")
        assert model.number_state_energies(1).magnitude[0] == 0.5
        assert model.number_state_wavefunctions(
            VectorQuantity(np.array([0.0]), Unitless()), 1
        ).unit == PhysicalUnit("meter ** -0.5")
