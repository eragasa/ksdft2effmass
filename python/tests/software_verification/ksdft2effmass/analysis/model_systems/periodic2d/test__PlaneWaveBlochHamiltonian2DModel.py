"""Software verification for ``PlaneWaveBlochHamiltonian2DModel``."""

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    ReciprocalLattice2D,
)

from ksdft2effmass.analysis.model_systems import (
    PlaneWaveBlochHamiltonian2DModel,
    PlaneWaveFourierCoefficient2D,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPlaneWaveBlochHamiltonian2DModel:
    """Own basis-order, Fourier-symmetry, and represented-identity evidence."""

    @staticmethod
    def lattice_pair() -> tuple[DirectLattice2D, ReciprocalLattice2D]:
        """Return an exact square two-pi-dual lattice pair for test setup."""
        direct = DirectLattice2D(
            np.array((2.0 * np.pi, 0.0)),
            np.array((0.0, 2.0 * np.pi)),
        )
        return direct, ReciprocalLattice2D.from_direct_lattice(direct)

    def test_properties__square_cutoff__exposes_declared_basis_identity(self) -> None:
        """The model exposes its deterministic p-outer, q-inner basis inventory."""
        direct, reciprocal = self.lattice_pair()
        model = PlaneWaveBlochHamiltonian2DModel(
            direct,
            reciprocal,
            1,
            (
                PlaneWaveFourierCoefficient2D((-1, 0), 0.5 + 0.25j),
                PlaneWaveFourierCoefficient2D((1, 0), 0.5 - 0.25j),
            ),
            ScalarQuantity(2.0, Unitless()),
            "state",
            "basis",
            "zero",
        )

        assert model.basis_ordering == "p_outer_q_inner"
        assert model.spin_convention == "spinless_scalar"
        assert model.represented_dimension == 9
        assert model.reciprocal_indices[0] == (-1, -1)
        assert model.reciprocal_indices[-1] == (1, 1)
        assert model.coefficient((1, 0)) == 0.5 - 0.25j
        assert model.coefficient((0, 1)) == 0.0 + 0.0j

    def test_construction__missing_conjugate_partner__raises_value_error(self) -> None:
        """A Fourier inventory representing a non-real potential is rejected."""
        direct, reciprocal = self.lattice_pair()

        with pytest.raises(ValueError, match=r"V\[-m\]"):
            PlaneWaveBlochHamiltonian2DModel(
                direct,
                reciprocal,
                1,
                (PlaneWaveFourierCoefficient2D((1, 0), 0.5 + 0.25j),),
                ScalarQuantity(2.0, Unitless()),
                "state",
                "basis",
                "zero",
            )
