r"""Software verification of ``PeriodicFourierPotential1D``.

Evidence profile: routine

Bounded artifact scope: extracted Appendix G periodic-1D public contract.

Facet and represented meaning

The public record is a finite real Fourier potential component. It is not a complete
scientific parent until a kinetic law and parent identities are composed separately.

Intrinsic and cross-object scope

The tests cover coefficient-unit canonicalization, analytic finite-series evaluation,
reciprocal-period conversion, and paired harmonic inventories.

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

        Requirement: Compatible harmonic units are canonicalized to the constant-term
        energy unit before evaluating the declared real Fourier series.

        Oracle: Direct analytic values for one cosine and one sine harmonic at three
        authored coordinates.

        Acceptance: Canonical coefficients and evaluated energies agree within the
        stated binary64 absolute tolerance.
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

        Requirement: A dimensionless period ``2*pi`` maps to reciprocal period one in
        the explicitly requested dimensionless reciprocal convention.

        Oracle: The analytic identity ``2*pi / (2*pi) = 1``.

        Acceptance: The returned built-in float equals one exactly for this input.
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

        Requirement: Every retained harmonic has paired cosine and sine coefficients,
        including an explicit zero where one channel is absent.

        Acceptance: Unequal inventory lengths raise ``ValueError`` rather than
        silently padding missing coefficients.
        """
        with pytest.raises(ValueError, match="equal length"):
            PeriodicFourierPotential1D(
                period=ScalarQuantity(1.0, Unitless()),
                constant_coefficient=ScalarQuantity(0.0, Unitless()),
                cosine_coefficients=VectorQuantity(np.asarray([1.0]), Unitless()),
                sine_coefficients=VectorQuantity(np.asarray([]), Unitless()),
            )
