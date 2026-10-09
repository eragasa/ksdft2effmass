"""Software verification for ``PlaneWaveBlochHamiltonian2DModel``.

The synthetic tests establish deterministic finite-basis ordering, represented-space
identity, spin convention, exact-zero handling for absent Fourier transfers, and the
coefficient-space reality condition. They do not establish continuum convergence,
material realism, scientific validation, or uncertainty quantification.
"""

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
from ksdft2effmass.periodic import PeriodicModel

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
        """The definition exposes its deterministic finite represented basis.

        The authored cutoff-one square inventory is the exact ordering oracle. The test
        also establishes that the historical ``Model`` suffix does not grant nominal
        scientific-model membership.
        """
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
        assert not isinstance(model, PeriodicModel)

    def test_construction__missing_conjugate_partner__raises_value_error(self) -> None:
        """A Fourier inventory violating the real-potential condition is rejected.

        The single complex positive transfer lacks its required negative-transfer
        conjugate. Rejection establishes exact inventory semantics, not a tolerance-
        based Hermiticity repair.
        """
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
