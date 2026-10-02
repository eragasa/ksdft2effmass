"""Numerical verification for ``PlaneWaveBlochHamiltonian2DConstructor``."""

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    ReciprocalLattice2D,
)

from ksdft2effmass.analysis.model_systems import (
    PlaneWaveBlochHamiltonian2DConstructor,
    PlaneWaveBlochHamiltonian2DModel,
    PlaneWaveBlochHamiltonian2DRequest,
    PlaneWaveFourierCoefficient2D,
)
from ksdft2effmass.operators import PhysicalUnit, ScalarQuantity

pytestmark = [pytest.mark.unit, pytest.mark.numerical_verification]


class TestPlaneWaveBlochHamiltonian2DConstructor:
    """Own analytical matrix and direct--reciprocal duality evidence."""

    @staticmethod
    def rectangular_model() -> PlaneWaveBlochHamiltonian2DModel:
        """Return a rectangular model with analytically known reciprocal scaling."""
        direct = DirectLattice2D(
            np.array((2.0 * np.pi, 0.0)),
            np.array((0.0, np.pi)),
        )
        reciprocal = ReciprocalLattice2D.from_direct_lattice(direct)
        return PlaneWaveBlochHamiltonian2DModel(
            direct,
            reciprocal,
            0,
            (PlaneWaveFourierCoefficient2D((0, 0), 1.2 + 0.0j),),
            ScalarQuantity(3.0, PhysicalUnit("electron_volt")),
            "rectangular-spinless-state",
            "single-reciprocal-mode",
            "constant-potential-zero",
        )

    def test_execute__rectangular_lattice__matches_analytical_kinetic_energy(
        self,
    ) -> None:
        r"""The diagonal equals ``3*(0.25**2 + (2*(-0.2))**2) + 1.2`` eV."""
        request = PlaneWaveBlochHamiltonian2DRequest(
            self.rectangular_model(), (0.25, -0.2), 1.0e-14
        )

        result = PlaneWaveBlochHamiltonian2DConstructor().execute(request)

        expected = 3.0 * (0.25**2 + (-0.4) ** 2) + 1.2
        assert result.represented_matrix.unit == PhysicalUnit("electron_volt")
        assert result.represented_matrix.magnitude.shape == (1, 1)
        assert np.isclose(
            result.represented_matrix.magnitude[0, 0],
            expected,
            rtol=0.0,
            atol=4.0e-16,
        )
        assert result.maximum_duality_residual <= 1.0e-14
        assert not result.represented_matrix.magnitude.flags.writeable

    def test_execute__skew_lattice__uses_primitive_vectors_as_columns(self) -> None:
        """A skew cell maps reduced momentum by ``B @ kappa``, not its transpose."""
        direct = DirectLattice2D(
            np.array((2.0 * np.pi, 0.0)),
            np.array((np.pi, 2.0 * np.pi)),
        )
        model = PlaneWaveBlochHamiltonian2DModel(
            direct,
            ReciprocalLattice2D.from_direct_lattice(direct),
            0,
            (),
            ScalarQuantity(2.0, PhysicalUnit("electron_volt")),
            "skew-spinless-state",
            "single-reciprocal-mode",
            "kinetic-zero",
        )

        result = PlaneWaveBlochHamiltonian2DConstructor().execute(
            PlaneWaveBlochHamiltonian2DRequest(model, (0.2, -0.1), 1.0e-14)
        )

        # A = [[2*pi, pi], [0, 2*pi]] gives B = [[1, 0], [-1/2, 1]].
        # Therefore B @ (0.2, -0.1) = (0.2, -0.2) and 2*|B*kappa|^2 = 0.16.
        assert np.isclose(
            result.represented_matrix.magnitude[0, 0],
            0.16,
            rtol=0.0,
            atol=2.0e-16,
        )

    def test_execute__complex_fourier_pair__uses_row_minus_column_transfer(
        self,
    ) -> None:
        """Off-diagonal entries follow ``V[n_prime - n]`` and are Hermitian."""
        source = self.rectangular_model()
        model = PlaneWaveBlochHamiltonian2DModel(
            source.direct_lattice,
            source.reciprocal_lattice,
            1,
            (
                PlaneWaveFourierCoefficient2D((-1, 0), 0.5 + 0.25j),
                PlaneWaveFourierCoefficient2D((1, 0), 0.5 - 0.25j),
            ),
            source.kinetic_scale,
            source.state_space_identifier,
            source.basis_identifier,
            source.energy_reference,
        )

        result = PlaneWaveBlochHamiltonian2DConstructor().execute(
            PlaneWaveBlochHamiltonian2DRequest(model, (0.0, 0.0), 1.0e-14)
        )

        matrix = result.represented_matrix.magnitude
        assert matrix[4, 1] == 0.5 - 0.25j
        assert matrix[1, 4] == 0.5 + 0.25j
        assert np.array_equal(matrix, matrix.conj().T)

    def test_execute__incompatible_lattice_pair__raises_value_error(self) -> None:
        """An independently valid but nondual reciprocal basis is rejected."""
        source = self.rectangular_model()
        incompatible = ReciprocalLattice2D(
            np.array((1.1, 0.0)),
            np.array((0.0, 2.0)),
        )
        model = PlaneWaveBlochHamiltonian2DModel(
            source.direct_lattice,
            incompatible,
            source.reciprocal_cutoff,
            source.fourier_coefficients,
            source.kinetic_scale,
            source.state_space_identifier,
            source.basis_identifier,
            source.energy_reference,
        )
        request = PlaneWaveBlochHamiltonian2DRequest(model, (0.0, 0.0), 1.0e-14)

        with pytest.raises(ValueError, match="duality tolerance"):
            PlaneWaveBlochHamiltonian2DConstructor().execute(request)
