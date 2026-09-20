r"""Software verification of ``PlaneWaveFiberHamiltonian1DResult``.

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
    PlaneWaveFiberHamiltonian1DResult,
)
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import PlaneWaveBasis1D

pytestmark = pytest.mark.software_verification
SUT = PlaneWaveFiberHamiltonian1DResult


class TestPlaneWaveFiberHamiltonian1DResult:
    """Verify correlations retained by a represented plane-wave fiber."""

    def test_constructor__representation__rejects_matrix_shape_not_matching_basis(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PERIODIC-ONE-D-010

        Requirement: The public contract enforces rejects matrix shape not
        matching basis.

        Acceptance: The asserted values and failures match the declared contract.
        """
        basis = PlaneWaveBasis1D(ScalarQuantity(1.0, Unitless()), 1)
        potential = PeriodicFourierPotential1D(
            period=ScalarQuantity(2.0 * np.pi, Unitless()),
            constant_coefficient=ScalarQuantity(0.0, Unitless()),
            cosine_coefficients=VectorQuantity(np.asarray([]), Unitless()),
            sine_coefficients=VectorQuantity(np.asarray([]), Unitless()),
        )

        with pytest.raises(ValueError, match="shape must match"):
            PlaneWaveFiberHamiltonian1DResult(
                0.0,
                basis,
                potential,
                ScalarQuantity(1.0, Unitless()),
                0.0,
                ComplexMatrixQuantity(np.eye(2), Unitless()),
            )
