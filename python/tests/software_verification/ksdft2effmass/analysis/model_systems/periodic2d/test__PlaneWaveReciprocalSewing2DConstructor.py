"""Software verification for ``PlaneWaveReciprocalSewing2DConstructor``."""

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    ReciprocalLattice2D,
)

from ksdft2effmass.analysis.model_systems import (
    PlaneWaveBlochHamiltonian2DModel,
    PlaneWaveReciprocalSewing2DConstructor,
    PlaneWaveReciprocalSewing2DRequest,
    PositiveReciprocalDirection2D,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPlaneWaveReciprocalSewing2DConstructor:
    """Own exact first- and second-direction coefficient-shift evidence."""

    @staticmethod
    def model() -> PlaneWaveBlochHamiltonian2DModel:
        """Return a cutoff-one square-lattice model for sewing tests."""
        direct = DirectLattice2D(
            np.array((2.0 * np.pi, 0.0)),
            np.array((0.0, 2.0 * np.pi)),
        )
        return PlaneWaveBlochHamiltonian2DModel(
            direct,
            ReciprocalLattice2D.from_direct_lattice(direct),
            1,
            (),
            ScalarQuantity(1.0, Unitless()),
            "state",
            "basis",
            "zero",
        )

    def test_execute__cutoff_one__matches_independent_kronecker_shifts(self) -> None:
        """The two maps shift only their declared reciprocal-index component."""
        model = self.model()
        constructor = PlaneWaveReciprocalSewing2DConstructor()
        first = constructor.execute(
            PlaneWaveReciprocalSewing2DRequest(
                model, PositiveReciprocalDirection2D.FIRST
            )
        )
        second = constructor.execute(
            PlaneWaveReciprocalSewing2DRequest(
                model, PositiveReciprocalDirection2D.SECOND
            )
        )
        one_dimensional_shift = np.zeros((3, 3), dtype=np.complex128)
        one_dimensional_shift[:-1, 1:] = np.eye(2, dtype=np.complex128)

        expected_first = np.kron(one_dimensional_shift, np.eye(3))
        expected_second = np.kron(np.eye(3), one_dimensional_shift)
        assert np.array_equal(first.coefficient_map.magnitude, expected_first)
        assert np.array_equal(second.coefficient_map.magnitude, expected_second)
        assert np.linalg.matrix_rank(first.coefficient_map.magnitude) == 6
        assert np.linalg.matrix_rank(second.coefficient_map.magnitude) == 6
        assert not np.array_equal(
            first.coefficient_map.magnitude.conj().T @ first.coefficient_map.magnitude,
            np.eye(9),
        )
