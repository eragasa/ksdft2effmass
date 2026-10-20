"""Software verification for :class:`TransformationIdentity`."""

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
    MomentumSampleRole,
)
from ksdft2effmass.operators.representations.identities import (
    BlochSpaceRole,
    RepresentationIdentity,
    RepresentationIdentityFactory,
)
from ksdft2effmass.operators.representations.spaces import (
    RepresentationSpaceIdentity,
)
from ksdft2effmass.operators.transformations.identities import (
    RepresentationTransformationKind,
    TransformationIdentity,
)

pytestmark = pytest.mark.software_verification


class TestTransformationIdentity:
    """Establish explicit edge kind, orientation, and endpoint binding."""

    @staticmethod
    def representation(identifier: str) -> RepresentationIdentity:
        """Return one rank-three retained Bloch identity."""
        space = RepresentationSpaceIdentity(
            identifier=f"{identifier}-space",
            state_space=StateSpace(
                f"{identifier}-state-space",
                "finite-fiber",
                3,
            ),
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
        domain = FiniteMomentumMeshDomain(
            identifier="construction-k-mesh",
            mesh=CenteredUniformMesh(1, 3, (0.0,)),
            coordinate_convention_id="centered-reduced-reciprocal.v1",
            sample_role=MomentumSampleRole.construction,
        )
        return RepresentationIdentityFactory().create_bloch(
            representation_id=identifier,
            domain=domain,
            space=space,
            role=BlochSpaceRole.retained,
            source_artifact_id="analytic-parent-law.v1",
        )

    def test_attributes__bind_explicit_kind_and_full_endpoint_identities(self) -> None:
        """Derivation history is an enum edge kind rather than a node-role variant."""
        source = self.representation("retained-reference")
        target = self.representation("attacked-representation")
        edge = TransformationIdentity(
            transformation_id="gauge-conjugation-r3",
            kind=RepresentationTransformationKind.gauge_conjugation,
            method_id="pointwise-conjugation.v1",
            orientation="gauge-dagger-source-gauge",
            source_identity=source,
            target_identity=target,
        )

        assert edge.kind is RepresentationTransformationKind.gauge_conjugation
        assert edge.source_identity is source
        assert edge.target_identity is target
        assert edge.method_id == "pointwise-conjugation.v1"
        assert edge.orientation == "gauge-dagger-source-gauge"

    def test_constructor__rejects_raw_kind_untyped_endpoint_and_empty_method(
        self,
    ) -> None:
        """Edges require the enum, full endpoints, and a named method."""
        source = self.representation("retained-reference")
        with pytest.raises(TypeError, match="kind"):
            TransformationIdentity(
                transformation_id="edge",
                kind=cast(
                    RepresentationTransformationKind,
                    "gauge_conjugation",
                ),
                method_id="method.v1",
                orientation="source-to-target",
                source_identity=source,
                target_identity=source,
            )
        with pytest.raises(TypeError, match="target_identity"):
            TransformationIdentity(
                transformation_id="edge",
                kind=RepresentationTransformationKind.alignment,
                method_id="method.v1",
                orientation="source-to-target",
                source_identity=source,
                target_identity=cast(RepresentationIdentity, "target"),
            )
        with pytest.raises(ValueError, match="method identity"):
            TransformationIdentity(
                transformation_id="edge",
                kind=RepresentationTransformationKind.alignment,
                method_id="",
                orientation="source-to-target",
                source_identity=source,
                target_identity=source,
            )
