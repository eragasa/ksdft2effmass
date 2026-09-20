r"""Software verification of ``PlaneWaveFiberHamiltonian1DConstructor``.

Evidence profile: routine

Bounded artifact scope: extracted Appendix G periodic-1D public contract.

Facet and represented meaning

The public class retains or transforms the explicitly represented periodic-1D values.

Intrinsic and cross-object scope

Construction invariants and the demonstrated public operation are included.

VVUQ and scientific exclusions

This is software verification, not a rerun or scientific validation of Appendix G.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import (
    PeriodicFourierPotential1D,
    PlaneWaveFiberHamiltonian1DConstructor,
)
from ksdft2effmass.operators import (
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import PlaneWaveBasis1D

pytestmark = pytest.mark.software_verification
SUT = PlaneWaveFiberHamiltonian1DConstructor


class TestPlaneWaveFiberHamiltonian1DConstructor:
    """Verify represented plane-wave Fourier fibers."""

    def test_method__execute__constructs_complex_hermitian_multiharmonic_fiber(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PERIODIC-ONE-D-008

        Requirement: The public contract enforces constructs complex hermitian
        multiharmonic fiber.

        Acceptance: The asserted values and failures match the declared contract.
        """
        potential = PeriodicFourierPotential1D(
            period=ScalarQuantity(2.0 * np.pi, Unitless()),
            constant_coefficient=ScalarQuantity(0.2, PhysicalUnit("electron_volt")),
            cosine_coefficients=VectorQuantity(
                np.asarray([0.8, -0.4]), PhysicalUnit("electron_volt")
            ),
            sine_coefficients=VectorQuantity(
                np.asarray([0.6, 0.2]), PhysicalUnit("electron_volt")
            ),
        )
        basis = PlaneWaveBasis1D(ScalarQuantity(1.0, Unitless()), 1)

        result = PlaneWaveFiberHamiltonian1DConstructor().execute(
            0.25,
            basis,
            potential,
            ScalarQuantity(2.0, PhysicalUnit("electron_volt")),
            1.0e-14,
        )

        expected = np.asarray(
            [
                [1.325, 0.4 + 0.3j, -0.2 + 0.1j],
                [0.4 - 0.3j, 0.325, 0.4 + 0.3j],
                [-0.2 - 0.1j, 0.4 - 0.3j, 3.325],
            ],
            dtype=np.complex128,
        )
        np.testing.assert_allclose(result.represented_matrix.magnitude, expected)
        np.testing.assert_array_equal(
            result.represented_matrix.magnitude,
            result.represented_matrix.magnitude.conj().T,
        )
        assert result.represented_matrix.unit == result.recoil_energy.unit

    def test_method__execute__rejects_period_and_reciprocal_vector_mismatch(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PERIODIC-ONE-D-009

        Requirement: The public contract enforces rejects period and reciprocal
        vector mismatch.

        Acceptance: The asserted values and failures match the declared contract.
        """
        potential = PeriodicFourierPotential1D(
            period=ScalarQuantity(2.0 * np.pi, Unitless()),
            constant_coefficient=ScalarQuantity(0.0, Unitless()),
            cosine_coefficients=VectorQuantity(np.asarray([]), Unitless()),
            sine_coefficients=VectorQuantity(np.asarray([]), Unitless()),
        )
        basis = PlaneWaveBasis1D(ScalarQuantity(2.0, Unitless()), 1)

        with pytest.raises(ValueError, match="incompatible with the period"):
            PlaneWaveFiberHamiltonian1DConstructor().execute(
                0.0,
                basis,
                potential,
                ScalarQuantity(1.0, Unitless()),
                1.0e-14,
            )
