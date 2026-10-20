"""Software verification for :class:`RepresentationIdentity`."""

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
    RepresentationIdentity,
)
from ksdft2effmass.operators.representations.spaces import (
    RepresentationSpaceIdentity,
)

pytestmark = pytest.mark.software_verification


class TestRepresentationIdentity:
    """Establish intrinsic node identity and carrier-role compatibility."""

    @staticmethod
    def space(identifier: str, dimension: int) -> RepresentationSpaceIdentity:
        """Return one synthetic represented-space identity."""
        return RepresentationSpaceIdentity(
            identifier=identifier,
            state_space=StateSpace(
                f"{identifier}-state-space",
                "finite-fiber",
                dimension,
            ),
            basis=Basis(
                f"{identifier}-basis",
                "reference-coordinates",
                tuple(f"b{index}" for index in range(dimension)),
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

    def test_attributes__derive_domain_rank_space_and_basis_identity(self) -> None:
        """Parallel domain-ID and rank inputs cannot disagree with composed owners."""
        identity = RepresentationIdentity(
            representation_id="retained-reference",
            domain=self.momentum_domain(),
            space=self.space("retained-reference-space", 3),
            role=BlochSpaceRole.retained,
            source_artifact_id="analytic-parent-law.v1",
        )

        assert identity.domain_id == "construction-k-mesh"
        assert identity.space_id == "retained-reference-space"
        assert identity.basis_id == "retained-reference-space-basis"
        assert identity.rank == 3
        assert identity.role is BlochSpaceRole.retained
        assert identity.source_artifact_id == "analytic-parent-law.v1"

    @pytest.mark.parametrize(
        ("domain", "role", "message"),
        [
            pytest.param(
                momentum_domain(),
                CellHoppingRepresentationRole.complete_declared_inventory,
                "momentum domain requires",
                id="cell_role_on_momentum_domain",
            ),
            pytest.param(
                translation_domain(),
                BlochSpaceRole.retained,
                "translation domain requires",
                id="bloch_role_on_translation_domain",
            ),
        ],
    )
    def test_domain_role__rejects_cross_family_choice(
        self,
        domain: FiniteMomentumMeshDomain | FiniteTranslationDomain,
        role: BlochSpaceRole | CellHoppingRepresentationRole,
        message: str,
    ) -> None:
        """Carrier-domain and role enum families cannot be mixed."""
        with pytest.raises(TypeError, match=message):
            RepresentationIdentity(
                representation_id="invalid-node",
                domain=domain,
                space=self.space("retained-space", 3),
                role=role,
                source_artifact_id="synthetic-source.v1",
            )

    def test_domain_and_role__reject_substitute_objects_and_raw_strings(self) -> None:
        """Nominal domain and enum boundaries reject structurally similar values."""
        space = self.space("retained-space", 3)
        with pytest.raises(TypeError, match="domain must be"):
            RepresentationIdentity(
                representation_id="invalid-node",
                domain=cast(
                    FiniteMomentumMeshDomain | FiniteTranslationDomain,
                    "construction-k-mesh",
                ),
                space=space,
                role=BlochSpaceRole.retained,
                source_artifact_id="synthetic-source.v1",
            )
        with pytest.raises(TypeError, match="requires a BlochSpaceRole"):
            RepresentationIdentity(
                representation_id="invalid-node",
                domain=self.momentum_domain(),
                space=space,
                role=cast(
                    BlochSpaceRole | CellHoppingRepresentationRole,
                    "retained",
                ),
                source_artifact_id="synthetic-source.v1",
            )
