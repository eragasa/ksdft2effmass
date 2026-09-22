r"""Software verification of ``PeriodicFiniteDifferenceFiberHamiltonian1DResult``.

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
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.analysis.model_systems import (
    PeriodicFiniteDifferenceFiberHamiltonian1DResult,
    PeriodicFourierPotential1D,
    PeriodicUniformGrid1D,
)
from ksdft2effmass.operators import (
    ComplexSparseMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

pytestmark = pytest.mark.software_verification
SUT = PeriodicFiniteDifferenceFiberHamiltonian1DResult


class TestPeriodicFiniteDifferenceFiberHamiltonian1DResult:
    """Verify represented periodic finite-difference fiber correlations."""

    def test_constructor__representation__rejects_matrix_shape_not_matching_grid(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PERIODIC-ONE-D-002

        Requirement: The public contract enforces rejects matrix shape not
        matching grid.

        Acceptance: The asserted values and failures match the declared contract.
        """
        grid = PeriodicUniformGrid1D(
            ScalarQuantity(0.0, Unitless()), ScalarQuantity(1.0, Unitless()), 3
        )
        potential = PeriodicFourierPotential1D(
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(0.0, Unitless()),
            VectorQuantity(np.asarray([]), Unitless()),
            VectorQuantity(np.asarray([]), Unitless()),
        )
        matrix = ComplexSparseMatrixQuantity.from_csr(
            sparse.eye(2, format="csr", dtype=np.complex128), Unitless()
        )

        with pytest.raises(ValueError, match="shape must match"):
            PeriodicFiniteDifferenceFiberHamiltonian1DResult(
                0.0,
                grid,
                potential,
                ScalarQuantity(1.0, Unitless()),
                0.0,
                matrix,
            )
