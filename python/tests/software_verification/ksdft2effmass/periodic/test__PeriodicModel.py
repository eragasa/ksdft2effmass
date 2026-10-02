"""Software verification for the nominal periodic scientific-model hierarchy."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from ksdft2effmass.periodic import (
    Periodic1DDefectModel,
    Periodic1DModel,
    Periodic2DDefectModel,
    Periodic2DModel,
    Periodic3DDefectModel,
    Periodic3DModel,
    PeriodicModel,
    PeriodicModelRole,
)

pytestmark = pytest.mark.software_verification


class TestPeriodicModel:
    """Verify nominal hierarchy, exact dimensions, roles, and parent identities."""

    @dataclass(frozen=True, slots=True)
    class Toy1D(Periodic1DModel):
        """Represent a synthetic one-dimensional toy model."""

        @property
        def model_id(self) -> str:
            """Return the test-owned model identity."""
            return "test.toy.1d"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the toy role."""
            return PeriodicModelRole.TOY

    @dataclass(frozen=True, slots=True)
    class Reference2D(Periodic2DModel):
        """Represent a synthetic two-dimensional material-reference model."""

        @property
        def model_id(self) -> str:
            """Return the test-owned model identity."""
            return "test.reference.2d"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the material-reference role."""
            return PeriodicModelRole.MATERIAL_REFERENCE

    @dataclass(frozen=True, slots=True)
    class Toy3DDefect(Periodic3DDefectModel):
        """Represent a synthetic three-dimensional toy defect model."""

        @property
        def model_id(self) -> str:
            """Return the test-owned model identity."""
            return "test.toy.defect.3d"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the toy role."""
            return PeriodicModelRole.TOY

        @property
        def parent_model_id(self) -> str:
            """Return the test-owned pristine parent identity."""
            return "test.toy.parent.3d"

    def test_inheritance__dimensions__uses_nominal_branches(self) -> None:
        """Dimension-specific models retain explicit nominal membership."""
        one_dimensional = self.Toy1D()
        two_dimensional = self.Reference2D()
        three_dimensional = self.Toy3DDefect()

        assert isinstance(one_dimensional, PeriodicModel)
        assert isinstance(one_dimensional, Periodic1DModel)
        assert not isinstance(one_dimensional, Periodic2DModel)
        assert isinstance(two_dimensional, Periodic2DModel)
        assert not isinstance(two_dimensional, Periodic3DModel)
        assert isinstance(three_dimensional, Periodic3DModel)
        assert isinstance(three_dimensional, Periodic3DDefectModel)

    def test_property__spatial_dimension__returns_exact_built_in_identity(self) -> None:
        """Each nominal dimension branch returns its exact built-in integer."""
        dimensions = (
            self.Toy1D().spatial_dimension,
            self.Reference2D().spatial_dimension,
            self.Toy3DDefect().spatial_dimension,
        )

        assert dimensions == (1, 2, 3)
        assert tuple(type(value) for value in dimensions) == (int, int, int)

    def test_inheritance__defect_models__remain_dimension_specific(self) -> None:
        """Every defect base is also a member of its exact dimension branch."""
        assert issubclass(Periodic1DDefectModel, Periodic1DModel)
        assert issubclass(Periodic2DDefectModel, Periodic2DModel)
        assert issubclass(Periodic3DDefectModel, Periodic3DModel)
        assert not issubclass(Periodic1DDefectModel, Periodic2DModel)
        assert self.Toy3DDefect().parent_model_id == "test.toy.parent.3d"

    def test_constructor__abstract_contract__requires_identity_and_role(self) -> None:
        """A dimension-only subclass cannot instantiate without identity and role."""

        class IncompleteModel(Periodic1DModel):
            """Deliberately omit required model identity properties."""

        with pytest.raises(TypeError, match="abstract"):
            IncompleteModel()  # type: ignore[abstract]

    def test_class_definition__dimension_override__is_rejected(self) -> None:
        """A subclass cannot replace its nominal branch's exact dimension."""
        with pytest.raises(TypeError, match="cannot override spatial_dimension"):

            class InvalidDimensionModel(Periodic1DModel):
                """Deliberately attempt to replace the fixed dimension."""

                @property
                def model_id(self) -> str:
                    return "test.invalid.dimension"

                @property
                def model_role(self) -> PeriodicModelRole:
                    return PeriodicModelRole.TOY

                @property  # type: ignore[misc]
                def spatial_dimension(self) -> int:  # type: ignore[override]
                    return 2
