"""Software verification for :class:`RepresentationIdentityFactory`."""

from __future__ import annotations

from typing import cast

import pytest
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh

from ksdft2effmass.operators.records import (
    Basis,
    EnergyReference,
    Geometry,
    StateSpace,
)
from ksdft2effmass.operators.representations.domains import (
    FiniteMomentumMeshDomain,
    FiniteTranslationDomain,
    MomentumSampleRole,
)
from ksdft2effmass.operators.representations.identities import (
    BlochSpaceRole,
    CellHoppingRepresentationRole,
    RepresentationIdentityFactory,
)
from ksdft2effmass.operators.representations.spaces import (
    RepresentationSpaceIdentity,
)

pytestmark = pytest.mark.software_verification


class TestRepresentationIdentityFactory:
    """Establish operational construction of carrier-compatible identities."""

    @staticmethod
    def space() -> RepresentationSpaceIdentity:
        """Return one synthetic rank-three represented space."""
        return RepresentationSpaceIdentity(
            identifier="retained-space",
            state_space=StateSpace("retained-state-space", "finite-fiber", 3),
            basis=Basis(
                "retained-basis",
                "reference-coordinates",
                ("b0", "b1", "b2"),
                True,
            ),
            geometry=Geometry(
                system="synthetic-cell",
                cell=(
                    (1.0, 0.0, 0.0),
                    (0.0, 1.0, 0.0),
                    (0.0, 0.0, 1.0),
                ),
                boundary_conditions="periodic",
                coordinate_convention="row-direct-lattice-vectors",
                length_unit="angstrom",
            ),
            energy_reference=EnergyReference("analytic zero", "model-energy"),
            scalar_field_id="complex-numbers.v1",
            coordinate_convention_id="centered-reduced-reciprocal.v1",
        )

    @staticmethod
    def momentum_domain() -> FiniteMomentumMeshDomain:
        """Return one finite momentum domain."""
        return FiniteMomentumMeshDomain(
            identifier="construction-k-mesh",
            mesh=CenteredUniformMesh(1, 3, (0.0,)),
            coordinate_convention_id="centered-reduced-reciprocal.v1",
            sample_role=MomentumSampleRole.construction,
        )

    @staticmethod
    def translation_domain() -> FiniteTranslationDomain:
        """Return one finite translation domain."""
        return FiniteTranslationDomain(
            identifier="symmetric-r1",
            translations=((-1,), (0,), (1,)),
            coordinate_convention_id="integer-cell-translation.v1",
        )

    def test_create_bloch__derives_domain_and_rank_from_complete_objects(self) -> None:
        """Bloch construction exposes the enum choice and accepts no parallel rank."""
        identity = RepresentationIdentityFactory().create_bloch(
            representation_id="retained-reference",
            domain=self.momentum_domain(),
            space=self.space(),
            role=BlochSpaceRole.retained,
            source_artifact_id="analytic-parent-law.v1",
        )

        assert identity.domain_id == "construction-k-mesh"
        assert identity.rank == 3
        assert identity.role is BlochSpaceRole.retained

    def test_create_cell_hopping__uses_translation_role_enum(self) -> None:
        """Cell-hopping construction visibly selects its family-local enum."""
        identity = RepresentationIdentityFactory().create_cell_hopping(
            representation_id="complete-hopping",
            domain=self.translation_domain(),
            space=self.space(),
            role=CellHoppingRepresentationRole.complete_declared_inventory,
            source_artifact_id="finite-fourier-conversion.v1",
        )

        assert identity.domain_id == "symmetric-r1"
        assert (
            identity.role is CellHoppingRepresentationRole.complete_declared_inventory
        )

    def test_methods__reject_cross_family_domain_and_raw_role_string(self) -> None:
        """Factory methods preserve nominal carrier and enum boundaries at runtime."""
        factory = RepresentationIdentityFactory()
        with pytest.raises(TypeError, match="domain must be"):
            factory.create_bloch(
                representation_id="invalid-node",
                domain=cast(FiniteMomentumMeshDomain, self.translation_domain()),
                space=self.space(),
                role=BlochSpaceRole.retained,
                source_artifact_id="synthetic-source.v1",
            )
        with pytest.raises(TypeError, match="exact BlochSpaceRole"):
            factory.create_bloch(
                representation_id="invalid-node",
                domain=self.momentum_domain(),
                space=self.space(),
                role=cast(BlochSpaceRole, "retained"),
                source_artifact_id="synthetic-source.v1",
            )
