r"""Software evidence for parent-qualified plane-wave fiber construction.

The synthetic matrices exercise reciprocal-basis ordering and Fourier transfer.
They do not establish basis convergence, physical adequacy, or scientific validation.
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
from ksdft2effmass.periodic import PeriodicOperatorReference
from ksdft2effmass.periodic1d import (
    Periodic1DFiberHamiltonianRequest,
    Periodic1DFourierHamiltonianToyModel,
    PlaneWaveFiberHamiltonian1DConstructor,
)
from ksdft2effmass.solid_state import PlaneWaveBasis1D

pytestmark = pytest.mark.software_verification
SUT = PlaneWaveFiberHamiltonian1DConstructor


class TestPlaneWaveFiberHamiltonian1DConstructor:
    """Verify identity retention, reciprocal ordering, and finite numerics."""

    @staticmethod
    def _request(
        potential: PeriodicFourierPotential1D,
        recoil_energy: ScalarQuantity,
        reduced_momentum: float,
    ) -> Periodic1DFiberHamiltonianRequest:
        """Return an explicit synthetic parent-qualified request fixture."""
        parent = Periodic1DFourierHamiltonianToyModel(
            "synthetic-parent",
            "untruncated-bloch-space",
            "primitive-reduced-zone",
            potential,
            recoil_energy,
        )
        return Periodic1DFiberHamiltonianRequest(
            representation_id="plane-wave-cutoff-one",
            parent_model=parent,
            represented_operator=PeriodicOperatorReference(
                model_id=parent.model_id,
                operator_id="finite-plane-wave-hamiltonian",
                state_space_id="plane-wave-cutoff-one-space",
                spatial_dimension=1,
            ),
            reduced_momentum=reduced_momentum,
            provenance_id="synthetic-plane-wave-test-fixture",
        )

    def test_method__execute__constructs_complex_hermitian_multiharmonic_fiber(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PERIODIC-ONE-D-008."""
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
        request = self._request(
            potential, ScalarQuantity(2.0, PhysicalUnit("electron_volt")), 0.25
        )
        basis = PlaneWaveBasis1D(ScalarQuantity(1.0, Unitless()), 1)

        result = SUT().execute(request, basis, 1.0e-14)

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
        assert result.request is request
        assert result.basis.reciprocal_indices == (-1, 0, 1)
        assert result.represented_matrix.unit == request.parent_model.recoil_energy.unit

    def test_method__execute__rejects_period_and_reciprocal_vector_mismatch(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PERIODIC-ONE-D-009."""
        potential = PeriodicFourierPotential1D(
            period=ScalarQuantity(2.0 * np.pi, Unitless()),
            constant_coefficient=ScalarQuantity(0.0, Unitless()),
            cosine_coefficients=VectorQuantity(np.asarray([]), Unitless()),
            sine_coefficients=VectorQuantity(np.asarray([]), Unitless()),
        )
        request = self._request(potential, ScalarQuantity(1.0, Unitless()), 0.0)
        basis = PlaneWaveBasis1D(ScalarQuantity(2.0, Unitless()), 1)

        with pytest.raises(ValueError, match="incompatible with the period"):
            SUT().execute(request, basis, 1.0e-14)
