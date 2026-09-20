r"""Software verification of ``PeriodicFiniteDifferenceFiberHamiltonian1DConstructor``.

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
    PeriodicFiniteDifferenceFiberHamiltonian1DConstructor,
    PeriodicFourierPotential1D,
    PeriodicUniformGrid1D,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless, VectorQuantity

pytestmark = pytest.mark.software_verification
SUT = PeriodicFiniteDifferenceFiberHamiltonian1DConstructor


class TestPeriodicFiniteDifferenceFiberHamiltonian1DConstructor:
    """Verify sparse twisted periodic finite-difference fibers."""

    def test_method__execute__constructs_twisted_sparse_fiber(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PERIODIC-ONE-D-001

        Requirement: The public contract enforces constructs conjugate bloch
        seam and scaled kinetic operator.

        Acceptance: The asserted values and failures match the declared contract.
        """
        grid = PeriodicUniformGrid1D(
            ScalarQuantity(0.0, Unitless()),
            ScalarQuantity(2.0 * np.pi, Unitless()),
            4,
        )
        potential = PeriodicFourierPotential1D(
            ScalarQuantity(2.0 * np.pi, Unitless()),
            ScalarQuantity(0.0, Unitless()),
            VectorQuantity(np.asarray([]), Unitless()),
            VectorQuantity(np.asarray([]), Unitless()),
        )

        result = PeriodicFiniteDifferenceFiberHamiltonian1DConstructor().execute(
            0.25, grid, potential, ScalarQuantity(1.0, Unitless()), 0.0
        )

        matrix = result.represented_matrix.to_csr().toarray()
        link = 4.0 / np.pi**2
        expected = np.asarray(
            [
                [2.0 * link, -link, 0.0, 1j * link],
                [-link, 2.0 * link, -link, 0.0],
                [0.0, -link, 2.0 * link, -link],
                [-1j * link, 0.0, -link, 2.0 * link],
            ],
            dtype=np.complex128,
        )
        np.testing.assert_allclose(matrix, expected, atol=1.0e-15)
        np.testing.assert_allclose(matrix, matrix.conj().T, atol=0.0)
        assert result.represented_matrix.nonzero_count == 12
