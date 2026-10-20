"""Software verification for :class:`FiniteMomentumMeshDomain`."""

from __future__ import annotations

from typing import cast

import pytest
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh

from ksdft2effmass.operators.representations.domains import (
    FiniteDomainABC,
    FiniteMomentumMeshDomain,
    MomentumSampleRole,
)

pytestmark = pytest.mark.software_verification


class TestFiniteMomentumMeshDomain:
    """Establish explicit centered-mesh composition and exact types."""

    def test_construction__derives_geometry_from_owner_mesh(self) -> None:
        """Cardinality and dimension are derived from one owner mesh."""
        mesh = CenteredUniformMesh(2, 3, (0.0, 0.5))
        domain = FiniteMomentumMeshDomain(
            identifier="construction-k-mesh",
            mesh=mesh,
            coordinate_convention_id="centered-reduced-reciprocal.v1",
            sample_role=MomentumSampleRole.construction,
        )

        assert isinstance(domain, FiniteDomainABC)
        assert domain.identity == "construction-k-mesh"
        assert domain.mesh is mesh
        assert domain.cardinality == 9
        assert domain.dimension == 2
        assert domain.sample_role is MomentumSampleRole.construction
        assert not hasattr(domain, "coordinates")

    def test_construction__rejects_untyped_role_mesh_and_identifiers(self) -> None:
        """Raw strings, numeric identifiers, and substitute meshes fail closed."""
        mesh = CenteredUniformMesh(1, 3, (0.0,))
        with pytest.raises(TypeError, match="sample_role"):
            FiniteMomentumMeshDomain(
                "mesh",
                mesh,
                "centered-reduced-reciprocal.v1",
                cast(MomentumSampleRole, "construction"),
            )
        with pytest.raises(TypeError, match="mesh"):
            FiniteMomentumMeshDomain(
                "mesh",
                cast(CenteredUniformMesh, "three points"),
                "centered-reduced-reciprocal.v1",
                MomentumSampleRole.general,
            )
        with pytest.raises(TypeError, match="identifier"):
            FiniteMomentumMeshDomain(
                cast(str, 3),
                mesh,
                "centered-reduced-reciprocal.v1",
                MomentumSampleRole.general,
            )
