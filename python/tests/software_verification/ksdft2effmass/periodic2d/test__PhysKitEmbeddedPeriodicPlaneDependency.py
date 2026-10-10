r"""Software verification of the pinned PhysKit embedded-plane dependency.

This test establishes only that the resolved dependency exposes the accepted public
geometry, serialization, and scalar-Laplacian composition route. It does not validate a
material model, kinetic-energy scaling, a slab geometry, or a ksdft2effmass campaign.
"""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.physkit.periodic.finite_difference.grid import (
    PeriodicFiniteDifferenceGrid,
)
from projectkoios.physkit.periodic.finite_difference.laplacian import (
    BlochPeriodicLaplacianConstructionRequest,
    BlochPeriodicLaplacianConstructor,
)
from projectkoios.physkit.periodic.lattice.boundary_phases import BoundaryTwistLift
from projectkoios.physkit.periodic.lattice.embedding import (
    EmbeddedDirectLattice2D,
    EmbeddedDirectLattice2DAdaptationRequest,
    EmbeddedDirectLattice2DAdapter,
)
from projectkoios.physkit.periodic.lattice.embedding.serialization import (
    EmbeddedDirectLattice2DJsonCodec,
)
from projectkoios.physkit.periodic.lattice.finite_domain import (
    FinitePeriodicDomain,
    LatticeDimension,
)
from projectkoios.physkit.units import MatrixQuantity, PhysicalUnit

pytestmark = pytest.mark.software_verification


class TestPhysKitEmbeddedPeriodicPlaneDependency:
    """Own the consuming-project smoke evidence for the pinned PhysKit API."""

    def test_public_api__routes_embedded_basis_to_intrinsic_laplacian(self) -> None:
        """The strict codec and explicit adapter compose with the 2D Laplacian."""
        basis = np.array(
            (
                (1.0, 0.25),
                (0.0, 1.2),
                (0.5, -0.1),
            ),
            dtype=np.float64,
        )
        length_unit = PhysicalUnit("angstrom")
        embedded = EmbeddedDirectLattice2D(
            ambient_basis=MatrixQuantity(basis, length_unit)
        )

        codec = EmbeddedDirectLattice2DJsonCodec()
        wire = codec.dumps(embedded)
        restored = codec.loads(wire)
        np.testing.assert_array_equal(restored.ambient_basis.magnitude, basis)
        assert restored.basis_unit == length_unit
        assert "induced_metric" not in wire
        assert "dual_reciprocal_basis" not in wire

        adaptation = EmbeddedDirectLattice2DAdapter().action(
            request=EmbeddedDirectLattice2DAdaptationRequest(embedded_lattice=restored)
        )
        np.testing.assert_allclose(
            adaptation.induced_metric.magnitude,
            basis.T @ basis,
            rtol=0.0,
            atol=32.0 * np.finfo(np.float64).eps,
        )
        np.testing.assert_allclose(
            basis.T @ adaptation.dual_reciprocal_basis.magnitude,
            2.0 * np.pi * np.identity(2),
            rtol=0.0,
            atol=128.0 * np.finfo(np.float64).eps,
        )

        grid = PeriodicFiniteDifferenceGrid(
            metric=adaptation.intrinsic_metric,
            domain=FinitePeriodicDomain(LatticeDimension.TWO, (4, 5)),
            direct_basis_unit=length_unit,
        )
        result = BlochPeriodicLaplacianConstructor().action(
            request=BlochPeriodicLaplacianConstructionRequest(
                grid=grid,
                twist=BoundaryTwistLift(
                    LatticeDimension.TWO,
                    (0.125, -0.25),
                ),
            )
        )
        matrix = result.represented_laplacian.to_csr()
        residual = matrix - matrix.conjugate().T

        assert matrix.shape == (20, 20)
        assert residual.nnz == 0
        assert result.represented_laplacian.unit == PhysicalUnit("1 / (angstrom) ** 2")
