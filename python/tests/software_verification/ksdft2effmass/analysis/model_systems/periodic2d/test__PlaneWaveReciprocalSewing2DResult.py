"""Software verification for ``PlaneWaveReciprocalSewing2DResult``."""

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    ReciprocalLattice2D,
)

from ksdft2effmass.analysis.model_systems import (
    PlaneWaveBlochHamiltonian2DModel,
    PlaneWaveReciprocalSewing2DRequest,
    PlaneWaveReciprocalSewing2DResult,
    PositiveReciprocalDirection2D,
)
from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPlaneWaveReciprocalSewing2DResult:
    """Own coefficient-map shape, unit, and exact-shift invariant evidence."""

    @staticmethod
    def request() -> PlaneWaveReciprocalSewing2DRequest:
        """Return a cutoff-zero request whose finite sewing map is exact zero."""
        direct = DirectLattice2D(
            np.array((2.0 * np.pi, 0.0)),
            np.array((0.0, 2.0 * np.pi)),
        )
        model = PlaneWaveBlochHamiltonian2DModel(
            direct,
            ReciprocalLattice2D.from_direct_lattice(direct),
            0,
            (),
            ScalarQuantity(1.0, Unitless()),
            "state",
            "basis",
            "zero",
        )
        return PlaneWaveReciprocalSewing2DRequest(
            model, PositiveReciprocalDirection2D.FIRST
        )

    def test_construction__cutoff_zero_zero_map__is_valid(self) -> None:
        """A one-mode basis loses its only coefficient under a positive shift."""
        result = PlaneWaveReciprocalSewing2DResult(
            self.request(),
            ComplexMatrixQuantity(np.zeros((1, 1), dtype=np.complex128), Unitless()),
        )

        assert np.array_equal(result.coefficient_map.magnitude, np.zeros((1, 1)))
        assert not result.coefficient_map.magnitude.flags.writeable

    def test_construction__wrapped_permutation__raises_value_error(self) -> None:
        """Finite plane-wave sewing must truncate rather than wrap coefficients."""
        with pytest.raises(ValueError, match="declared reciprocal shift"):
            PlaneWaveReciprocalSewing2DResult(
                self.request(),
                ComplexMatrixQuantity(np.ones((1, 1), dtype=np.complex128), Unitless()),
            )
