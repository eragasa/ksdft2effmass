r"""Software evidence for the parent-qualified finite-difference fiber Result."""

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.analysis.model_systems import PeriodicFourierPotential1D
from ksdft2effmass.operators import (
    ComplexSparseMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.periodic import PeriodicOperatorReference
from ksdft2effmass.periodic1d import (
    Periodic1DFiberHamiltonianRequest,
    Periodic1DFourierHamiltonianToyModel,
    PeriodicFiniteDifferenceFiberHamiltonian1DResult,
    PeriodicUniformGrid1D,
)

pytestmark = pytest.mark.software_verification
SUT = PeriodicFiniteDifferenceFiberHamiltonian1DResult


class TestPeriodicFiniteDifferenceFiberHamiltonian1DResult:
    """Verify intrinsic sparse represented-fiber correlations only."""

    def test_constructor__representation__rejects_matrix_shape_not_matching_grid(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PERIODIC-ONE-D-002."""
        grid = PeriodicUniformGrid1D(
            ScalarQuantity(0.0, Unitless()), ScalarQuantity(1.0, Unitless()), 3
        )
        potential = PeriodicFourierPotential1D(
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(0.0, Unitless()),
            VectorQuantity(np.asarray([]), Unitless()),
            VectorQuantity(np.asarray([]), Unitless()),
        )
        parent = Periodic1DFourierHamiltonianToyModel(
            "synthetic-parent",
            "untruncated-space",
            "reduced-zone",
            potential,
            ScalarQuantity(1.0, Unitless()),
        )
        request = Periodic1DFiberHamiltonianRequest(
            "three-point-central-difference",
            parent,
            PeriodicOperatorReference(
                parent.model_id,
                "finite-difference-hamiltonian",
                "three-point-grid-space",
                1,
            ),
            0.0,
            "synthetic-result-fixture",
        )
        matrix = ComplexSparseMatrixQuantity.from_csr(
            sparse.eye(2, format="csr", dtype=np.complex128), Unitless()
        )

        with pytest.raises(ValueError, match="shape must match"):
            SUT(request, grid, 0.0, matrix)
