"""Software verification for ``Periodic2DPlaneWaveBlochHamiltonianModel``."""

import importlib.util

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    ReciprocalLattice2D,
)
from projectkoios.physkit.units import (
    ScalarQuantity,
    Unitless,
)

from ksdft2effmass.periodic.operators.basis import (
    PeriodicBasisFamily,
    PlaneWaveBasisCoordinate,
)
from ksdft2effmass.periodic.periodic2d.models import (
    Periodic2DPlaneWaveBlochHamiltonianModel,
    Periodic2DPlaneWaveFourierCoefficient,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DPlaneWaveBlochHamiltonianModel:
    """Own basis-order, Fourier-symmetry, and represented-identity evidence."""

    def test_ownership__periodic_models_replace_model_systems_without_alias(
        self,
    ) -> None:
        assert (
            importlib.util.find_spec("ksdft2effmass.model_systems.periodic2d") is None
        )
        assert (
            importlib.util.find_spec("ksdft2effmass.periodic.periodic2d.models")
            is not None
        )

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
        model = Periodic2DPlaneWaveBlochHamiltonianModel(
            direct,
            reciprocal,
            1,
            (
                Periodic2DPlaneWaveFourierCoefficient((-1, 0), 0.5 + 0.25j),
                Periodic2DPlaneWaveFourierCoefficient((1, 0), 0.5 - 0.25j),
            ),
            ScalarQuantity(2.0, Unitless()),
            "state",
            "basis",
            "zero",
        )

        assert model.basis_ordering == "p_outer_q_inner"
        assert model.spin_convention == "spinless_scalar"
        assert model.basis_identity.display_identifier == "basis"
        assert model.basis_identity.family is PeriodicBasisFamily.PLANE_WAVE
        assert model.basis_identity.coordinates[0] == PlaneWaveBasisCoordinate((-1, -1))
        assert model.basis_identity.coordinates[-1] == PlaneWaveBasisCoordinate((1, 1))
        assert model.represented_dimension == 9
        assert model.reciprocal_indices[0] == (-1, -1)
        assert model.reciprocal_indices[-1] == (1, 1)
        assert model.coefficient((1, 0)) == 0.5 - 0.25j
        assert model.coefficient((0, 1)) == 0.0 + 0.0j

    def test_construction__missing_conjugate_partner__raises_value_error(self) -> None:
        """A Fourier inventory representing a non-real potential is rejected."""
        direct, reciprocal = self.lattice_pair()

        with pytest.raises(ValueError, match=r"V\[-m\]"):
            Periodic2DPlaneWaveBlochHamiltonianModel(
                direct,
                reciprocal,
                1,
                (Periodic2DPlaneWaveFourierCoefficient((1, 0), 0.5 + 0.25j),),
                ScalarQuantity(2.0, Unitless()),
                "state",
                "basis",
                "zero",
            )
