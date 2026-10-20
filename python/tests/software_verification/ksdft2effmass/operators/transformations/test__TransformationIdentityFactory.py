"""Software verification for :class:`TransformationIdentityFactory`."""

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
    RepresentationIdentityFactory,
)
from ksdft2effmass.operators.representations.spaces import (
    RepresentationSpaceIdentity,
)
from ksdft2effmass.operators.transformations.identities import (
    RepresentationTransformationKind,
    TransformationIdentityFactory,
)

pytestmark = pytest.mark.software_verification


class TestTransformationIdentityFactory:
    """Establish operational construction of carrier-compatible graph edges."""

    @staticmethod
    def space(identifier: str) -> RepresentationSpaceIdentity:
        """Return one synthetic rank-three represented space."""
        return RepresentationSpaceIdentity(
            identifier=identifier,
            state_space=StateSpace(f"{identifier}-state", "finite-fiber", 3),
            basis=Basis(
                f"{identifier}-basis",
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

    @classmethod
    def identities(cls) -> dict[str, RepresentationIdentity]:
        """Return nodes spanning every Phase 1 role transition."""
        identity_factory = RepresentationIdentityFactory()
        momentum_domain = FiniteMomentumMeshDomain(
            identifier="construction-k-mesh",
            mesh=CenteredUniformMesh(1, 3, (0.0,)),
            coordinate_convention_id="centered-reduced-reciprocal.v1",
            sample_role=MomentumSampleRole.construction,
        )
        complete_domain = FiniteTranslationDomain(
            identifier="complete-translations",
            translations=((-1,), (0,), (1,)),
            coordinate_convention_id="integer-cell-translation.v1",
        )
        support_domain = FiniteTranslationDomain(
            identifier="onsite-support",
            translations=((0,),),
            coordinate_convention_id="integer-cell-translation.v1",
        )
        ambient_space = cls.space("ambient-space")
        retained_space = cls.space("retained-space")
        return {
            "ambient": identity_factory.create_bloch(
                representation_id="ambient",
                domain=momentum_domain,
                space=ambient_space,
                role=BlochSpaceRole.ambient,
                source_artifact_id="ambient-law.v1",
            ),
            "retained": identity_factory.create_bloch(
                representation_id="retained",
                domain=momentum_domain,
                space=retained_space,
                role=BlochSpaceRole.retained,
                source_artifact_id="retained-law.v1",
            ),
            "retained-derived": identity_factory.create_bloch(
                representation_id="retained-derived",
                domain=momentum_domain,
                space=retained_space,
                role=BlochSpaceRole.retained,
                source_artifact_id="derived-law.v1",
            ),
            "complete": identity_factory.create_cell_hopping(
                representation_id="complete",
                domain=complete_domain,
                space=retained_space,
                role=CellHoppingRepresentationRole.complete_declared_inventory,
                source_artifact_id="fourier-conversion.v1",
            ),
            "truncated": identity_factory.create_cell_hopping(
                representation_id="truncated",
                domain=support_domain,
                space=retained_space,
                role=CellHoppingRepresentationRole.support_truncated,
                source_artifact_id="support-truncation.v1",
            ),
        }

    @pytest.mark.parametrize(
        ("kind", "source_key", "target_key"),
        [
            pytest.param(
                RepresentationTransformationKind.frame_compression,
                "ambient",
                "retained",
                id="frame_compression",
            ),
            pytest.param(
                RepresentationTransformationKind.gauge_conjugation,
                "retained",
                "retained-derived",
                id="gauge_conjugation",
            ),
            pytest.param(
                RepresentationTransformationKind.alignment,
                "retained-derived",
                "retained",
                id="alignment",
            ),
            pytest.param(
                RepresentationTransformationKind.finite_fourier_conversion,
                "retained",
                "complete",
                id="finite_fourier_conversion",
            ),
            pytest.param(
                RepresentationTransformationKind.support_truncation,
                "complete",
                "truncated",
                id="support_truncation",
            ),
            pytest.param(
                RepresentationTransformationKind.fourier_reconstruction,
                "truncated",
                "retained-derived",
                id="fourier_reconstruction",
            ),
        ],
    )
    def test_create__accepts_each_declared_role_transition(
        self,
        kind: RepresentationTransformationKind,
        source_key: str,
        target_key: str,
    ) -> None:
        """Each transformation enum member selects one compatible edge family."""
        identities = self.identities()
        edge = TransformationIdentityFactory().create(
            transformation_id=f"{kind.name}-edge",
            kind=kind,
            method_id="synthetic-method.v1",
            orientation="source-to-target",
            source_identity=identities[source_key],
            target_identity=identities[target_key],
        )

        assert edge.kind is kind
        assert edge.source_identity is identities[source_key]
        assert edge.target_identity is identities[target_key]

    def test_create__rejects_incompatible_roles_and_raw_kind_string(self) -> None:
        """The factory fails closed before constructing a mistyped graph edge."""
        identities = self.identities()
        factory = TransformationIdentityFactory()
        with pytest.raises(ValueError, match="incompatible"):
            factory.create(
                transformation_id="invalid-fourier-edge",
                kind=RepresentationTransformationKind.finite_fourier_conversion,
                method_id="synthetic-method.v1",
                orientation="source-to-target",
                source_identity=identities["ambient"],
                target_identity=identities["truncated"],
            )
        with pytest.raises(TypeError, match="kind"):
            factory.create(
                transformation_id="raw-string-kind",
                kind=cast(
                    RepresentationTransformationKind,
                    "finite_fourier_conversion",
                ),
                method_id="synthetic-method.v1",
                orientation="source-to-target",
                source_identity=identities["retained"],
                target_identity=identities["complete"],
            )
