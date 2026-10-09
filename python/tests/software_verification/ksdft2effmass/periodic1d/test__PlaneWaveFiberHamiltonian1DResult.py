r"""Software evidence for the parent-qualified plane-wave fiber Result."""

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import PeriodicFourierPotential1D
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.periodic import PeriodicOperatorReference
from ksdft2effmass.periodic1d import (
    Periodic1DFiberHamiltonianRequest,
    Periodic1DFourierHamiltonianToyModel,
    PlaneWaveFiberHamiltonian1DResult,
)
from ksdft2effmass.solid_state import PlaneWaveBasis1D

pytestmark = pytest.mark.software_verification
SUT = PlaneWaveFiberHamiltonian1DResult


class TestPlaneWaveFiberHamiltonian1DResult:
    """Verify intrinsic represented-fiber correlations only."""

    def test_constructor__representation__rejects_matrix_shape_not_matching_basis(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PERIODIC-ONE-D-010."""
        potential = PeriodicFourierPotential1D(
            period=ScalarQuantity(2.0 * np.pi, Unitless()),
            constant_coefficient=ScalarQuantity(0.0, Unitless()),
            cosine_coefficients=VectorQuantity(np.asarray([]), Unitless()),
            sine_coefficients=VectorQuantity(np.asarray([]), Unitless()),
        )
        parent = Periodic1DFourierHamiltonianToyModel(
            "synthetic-parent",
            "untruncated-space",
            "reduced-zone",
            potential,
            ScalarQuantity(1.0, Unitless()),
        )
        request = Periodic1DFiberHamiltonianRequest(
            "plane-wave-cutoff-one",
            parent,
            PeriodicOperatorReference(
                parent.model_id,
                "finite-plane-wave-hamiltonian",
                "finite-plane-wave-space",
                1,
            ),
            0.0,
            "synthetic-result-fixture",
        )
        basis = PlaneWaveBasis1D(ScalarQuantity(1.0, Unitless()), 1)

        with pytest.raises(ValueError, match="shape must match"):
            SUT(
                request,
                basis,
                0.0,
                ComplexMatrixQuantity(np.eye(2), Unitless()),
            )
