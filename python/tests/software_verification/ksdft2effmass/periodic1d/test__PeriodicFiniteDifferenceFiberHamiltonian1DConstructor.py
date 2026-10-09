r"""Software evidence for parent-qualified finite-difference fiber construction.

The synthetic matrix fixes the half-open grid order and directed Bloch seam.  It is
not evidence of mesh convergence or physical validation.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import PeriodicFourierPotential1D
from ksdft2effmass.operators import ScalarQuantity, Unitless, VectorQuantity
from ksdft2effmass.periodic import PeriodicOperatorReference
from ksdft2effmass.periodic1d import (
    Periodic1DFiberHamiltonianRequest,
    Periodic1DFourierHamiltonianToyModel,
    PeriodicFiniteDifferenceFiberHamiltonian1DConstructor,
    PeriodicUniformGrid1D,
)

pytestmark = pytest.mark.software_verification
SUT = PeriodicFiniteDifferenceFiberHamiltonian1DConstructor


class TestPeriodicFiniteDifferenceFiberHamiltonian1DConstructor:
    """Verify the sparse kinetic stencil and oriented Bloch seam."""

    def test_method__execute__constructs_twisted_sparse_fiber(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PERIODIC-ONE-D-001."""
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
        parent = Periodic1DFourierHamiltonianToyModel(
            "synthetic-parent",
            "untruncated-space",
            "reduced-zone",
            potential,
            ScalarQuantity(1.0, Unitless()),
        )
        request = Periodic1DFiberHamiltonianRequest(
            "four-point-central-difference",
            parent,
            PeriodicOperatorReference(
                parent.model_id,
                "finite-difference-hamiltonian",
                "four-point-grid-space",
                1,
            ),
            0.25,
            "synthetic-finite-difference-fixture",
        )

        result = SUT().execute(request, grid, 0.0)

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
        np.testing.assert_allclose(
            grid.coordinates.magnitude,
            np.asarray([0.0, 0.5 * np.pi, np.pi, 1.5 * np.pi]),
        )
        assert result.request is request
        assert result.represented_matrix.nonzero_count == 12
