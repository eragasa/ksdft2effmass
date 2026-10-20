"""Software verification for represented-space identity composition."""

from __future__ import annotations

from typing import cast

import pytest

from ksdft2effmass.operators.records import (
    Basis,
    EnergyReference,
    Geometry,
    StateSpace,
)
from ksdft2effmass.operators.representations.spaces import (
    RepresentationSpaceIdentity,
)

pytestmark = pytest.mark.software_verification


class _StringSubclass(str):
    """Synthetic non-exact string used at strict nominal boundaries."""


class TestRepresentationSpaceIdentity:
    """Establish reuse of operator metadata and dimension consistency."""

    @staticmethod
    def geometry() -> Geometry:
        """Return one synthetic finite periodic cell metadata object."""
        return Geometry(
            system="synthetic-cell",
            cell=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
            boundary_conditions="periodic",
            coordinate_convention="row-direct-lattice-vectors",
            length_unit="angstrom",
        )

    @staticmethod
    def make_space(*, basis_size: int = 3) -> RepresentationSpaceIdentity:
        """Return one rank-three represented-space identity fixture."""
        return RepresentationSpaceIdentity(
            identifier="retained-space-r3",
            state_space=StateSpace("retained-r3", "retained-fiber", 3),
            basis=Basis(
                "reference-frame-r3",
                "frame-coordinates",
                tuple(f"b{index}" for index in range(basis_size)),
                True,
            ),
            geometry=TestRepresentationSpaceIdentity.geometry(),
            energy_reference=EnergyReference("analytic zero", "model-energy"),
            scalar_field_id="complex-numbers.v1",
            coordinate_convention_id="centered-reduced-reciprocal.v1",
        )

    def test_space__composes_existing_metadata_without_duplication(self) -> None:
        """The space exposes one dimension from existing StateSpace metadata."""
        space = self.make_space()

        assert type(space.state_space) is StateSpace
        assert type(space.basis) is Basis
        assert type(space.geometry) is Geometry
        assert type(space.energy_reference) is EnergyReference
        assert space.dimension == 3
        assert space.basis.ordering == ("b0", "b1", "b2")

    def test_space__rejects_basis_state_space_dimension_mismatch(self) -> None:
        """A basis with a different cardinality cannot identify the same space."""
        with pytest.raises(ValueError, match="basis ordering length"):
            self.make_space(basis_size=2)

    def test_space__rejects_substitute_metadata_and_nonexact_strings(self) -> None:
        """Phase 1 accepts only the existing nominal metadata leaves."""
        valid = self.make_space()
        with pytest.raises(TypeError, match="state_space"):
            RepresentationSpaceIdentity(
                "space",
                cast(StateSpace, "rank three"),
                valid.basis,
                valid.geometry,
                valid.energy_reference,
                "complex-numbers.v1",
                "centered-reduced-reciprocal.v1",
            )
        with pytest.raises(TypeError, match="scalar field"):
            RepresentationSpaceIdentity(
                "space",
                valid.state_space,
                valid.basis,
                valid.geometry,
                valid.energy_reference,
                cast(str, 128),
                "centered-reduced-reciprocal.v1",
            )
        with pytest.raises(TypeError, match="space identity"):
            RepresentationSpaceIdentity(
                _StringSubclass("space"),
                valid.state_space,
                valid.basis,
                valid.geometry,
                valid.energy_reference,
                "complex-numbers.v1",
                "centered-reduced-reciprocal.v1",
            )
