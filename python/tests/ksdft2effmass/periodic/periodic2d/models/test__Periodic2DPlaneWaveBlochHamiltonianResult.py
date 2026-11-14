"""Software verification for ``Periodic2DPlaneWaveBlochHamiltonianResult``."""

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    ReciprocalLattice2D,
)
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
)

from ksdft2effmass.periodic.periodic2d.models import (
    Periodic2DPlaneWaveBlochHamiltonianModel,
    Periodic2DPlaneWaveBlochHamiltonianRequest,
    Periodic2DPlaneWaveBlochHamiltonianResult,
)
from ksdft2effmass.periodic.periodic2d.operators import Periodic2DBasisIdentity

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DPlaneWaveBlochHamiltonianResult:
    """Own result correlation, dimension, unit, and residual evidence."""

    @staticmethod
    def request() -> Periodic2DPlaneWaveBlochHamiltonianRequest:
        """Return one zero-potential one-state request for result tests."""
        direct = DirectLattice2D(
            np.array((2.0 * np.pi, 0.0)),
            np.array((0.0, 2.0 * np.pi)),
        )
        reciprocal = ReciprocalLattice2D.from_direct_lattice(direct)
        model = Periodic2DPlaneWaveBlochHamiltonianModel(
            direct,
            reciprocal,
            0,
            (),
            ScalarQuantity(1.0, Unitless()),
            "state",
            "basis",
            "zero",
        )
        return Periodic2DPlaneWaveBlochHamiltonianRequest(model, (0.0, 0.0), 1.0e-14)

    def test_basis_identity__forwards_exact_request_basis(self) -> None:
        """The represented matrix exposes its request-owned structured basis."""
        request = self.request()
        result = Periodic2DPlaneWaveBlochHamiltonianResult(
            request,
            0.0,
            ComplexMatrixQuantity(
                np.eye(1, dtype=np.complex128),
                Unitless(),
            ),
        )

        assert type(result.basis_identity) is Periodic2DBasisIdentity
        assert result.basis_identity == request.basis_identity

    def test_construction__incompatible_matrix_shape__raises_value_error(self) -> None:
        """A represented matrix must match the request's ordered basis dimension."""
        with pytest.raises(ValueError, match="shape"):
            Periodic2DPlaneWaveBlochHamiltonianResult(
                self.request(),
                0.0,
                ComplexMatrixQuantity(
                    np.eye(2, dtype=np.complex128),
                    Unitless(),
                ),
            )

    def test_construction__residual_above_tolerance__raises_value_error(self) -> None:
        """A result cannot retain a duality residual rejected by its request."""
        with pytest.raises(ValueError, match="exceeds"):
            Periodic2DPlaneWaveBlochHamiltonianResult(
                self.request(),
                2.0e-14,
                ComplexMatrixQuantity(
                    np.eye(1, dtype=np.complex128),
                    Unitless(),
                ),
            )
