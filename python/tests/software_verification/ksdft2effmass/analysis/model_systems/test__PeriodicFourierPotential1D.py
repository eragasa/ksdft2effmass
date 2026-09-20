r"""Software verification of ``PeriodicFourierPotential1D``.

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

from ksdft2effmass.analysis.model_systems import PeriodicFourierPotential1D
from ksdft2effmass.operators import (
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

pytestmark = pytest.mark.software_verification
SUT = PeriodicFourierPotential1D


class TestPeriodicFourierPotential1D:
    """Verify finite real Fourier potential records and evaluation."""

    def test_constructor__fourier_series__normalizes_and_evaluates(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PERIODIC-ONE-D-003

        Requirement: The public contract enforces normalizes coefficients and
        evaluates harmonics.

        Acceptance: The asserted values and failures match the declared contract.
        """
        potential = PeriodicFourierPotential1D(
            period=ScalarQuantity(2.0, PhysicalUnit("nanometer")),
            constant_coefficient=ScalarQuantity(1.0, PhysicalUnit("electron_volt")),
            cosine_coefficients=VectorQuantity(
                np.asarray([500.0], dtype=np.float64),
                PhysicalUnit("millielectron_volt"),
            ),
            sine_coefficients=VectorQuantity(
                np.asarray([250.0], dtype=np.float64),
                PhysicalUnit("millielectron_volt"),
            ),
        )

        assert potential.harmonic_count == 1
        np.testing.assert_allclose(potential.cosine_coefficients.magnitude, [0.5])
        np.testing.assert_allclose(potential.sine_coefficients.magnitude, [0.25])
        values = potential.evaluate(
            VectorQuantity(
                np.asarray([0.0, 0.5, 1.0], dtype=np.float64),
                PhysicalUnit("nanometer"),
            )
        )
        np.testing.assert_allclose(values.magnitude, [1.5, 1.25, 0.5], atol=1.0e-15)
        assert values.unit == potential.constant_coefficient.unit

    def test_constructor__fourier_series__computes_reciprocal_period_in_requested_unit(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PERIODIC-ONE-D-004

        Requirement: The public contract enforces computes reciprocal period in
        requested unit.

        Acceptance: The asserted values and failures match the declared contract.
        """
        potential = PeriodicFourierPotential1D(
            period=ScalarQuantity(2.0 * np.pi, Unitless()),
            constant_coefficient=ScalarQuantity(0.0, Unitless()),
            cosine_coefficients=VectorQuantity(np.asarray([]), Unitless()),
            sine_coefficients=VectorQuantity(np.asarray([]), Unitless()),
        )

        assert potential.reciprocal_period_in(ScalarQuantity(1.0, Unitless())) == 1.0

    def test_constructor__fourier_series__rejects_unequal_inventories(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PERIODIC-ONE-D-005

        Requirement: The public contract enforces rejects unequal harmonic
        inventories.

        Acceptance: The asserted values and failures match the declared contract.
        """
        with pytest.raises(ValueError, match="equal length"):
            PeriodicFourierPotential1D(
                period=ScalarQuantity(1.0, Unitless()),
                constant_coefficient=ScalarQuantity(0.0, Unitless()),
                cosine_coefficients=VectorQuantity(np.asarray([1.0]), Unitless()),
                sine_coefficients=VectorQuantity(np.asarray([]), Unitless()),
            )
