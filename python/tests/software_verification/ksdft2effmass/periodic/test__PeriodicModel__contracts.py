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
    class Control1D(Periodic1DModel):
        """Represent a synthetic one-dimensional control model."""

        @property
        def model_id(self) -> str:
            """Return the test-owned model identity."""
            return "test.control.1d"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the control-model role."""
            return PeriodicModelRole.CONTROL_MODEL

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
    class Control3DDefect(Periodic3DDefectModel):
        """Represent a synthetic three-dimensional control defect model."""

        @property
        def model_id(self) -> str:
            """Return the test-owned model identity."""
            return "test.control.defect.3d"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the control-model role."""
            return PeriodicModelRole.CONTROL_MODEL

        @property
        def parent_model_id(self) -> str:
            """Return the test-owned pristine parent identity."""
            return "test.control.parent.3d"

    def test__PeriodicModel__model_role__includes_parameterized_reduced_models(
        self,
    ) -> None:
        """The reduced role remains distinct from control and material references."""
        assert (
            PeriodicModelRole.CONTROL_MODEL.value,
            PeriodicModelRole.REDUCED_MODEL.value,
            PeriodicModelRole.MATERIAL_REFERENCE.value,
        ) == ("control_model", "reduced_model", "material_reference")

    def test__PeriodicModel__inheritance__dimensions__uses_nominal_branches(
        self,
    ) -> None:
        """Dimension-specific models retain explicit nominal membership."""
        one_dimensional = self.Control1D()
        two_dimensional = self.Reference2D()
        three_dimensional = self.Control3DDefect()

        assert isinstance(one_dimensional, PeriodicModel)
        assert isinstance(one_dimensional, Periodic1DModel)
        assert not isinstance(one_dimensional, Periodic2DModel)
        assert isinstance(two_dimensional, Periodic2DModel)
        assert not isinstance(two_dimensional, Periodic3DModel)
        assert isinstance(three_dimensional, Periodic3DModel)
        assert isinstance(three_dimensional, Periodic3DDefectModel)

    def test__PeriodicModel__property__spatial_dimension__returns_exact_built_in_identity(  # noqa: E501
        self,
    ) -> None:
        """Each nominal dimension branch returns its exact built-in integer."""
        dimensions = (
            self.Control1D().spatial_dimension,
            self.Reference2D().spatial_dimension,
            self.Control3DDefect().spatial_dimension,
        )

        assert dimensions == (1, 2, 3)
        assert tuple(type(value) for value in dimensions) == (int, int, int)

    def test__PeriodicModel__inheritance__defect_models__remain_dimension_specific(
        self,
    ) -> None:
        """Every defect base is also a member of its exact dimension branch."""
        assert issubclass(Periodic1DDefectModel, Periodic1DModel)
        assert issubclass(Periodic2DDefectModel, Periodic2DModel)
        assert issubclass(Periodic3DDefectModel, Periodic3DModel)
        assert not issubclass(Periodic1DDefectModel, Periodic2DModel)
        assert self.Control3DDefect().parent_model_id == "test.control.parent.3d"

    def test__PeriodicModel__constructor__abstract_contract__requires_identity_and_role(
        self,
    ) -> None:
        """A dimension-only subclass cannot instantiate without identity and role."""

        class IncompleteModel(Periodic1DModel):
            """Deliberately omit required model identity properties."""

        with pytest.raises(TypeError, match="abstract"):
            IncompleteModel()  # type: ignore[abstract]

    def test__PeriodicModel__class_definition__dimension_override__is_rejected(
        self,
    ) -> None:
        """A subclass cannot replace its nominal branch's exact dimension."""
        with pytest.raises(TypeError, match="cannot override spatial_dimension"):

            class InvalidDimensionModel(Periodic1DModel):
                """Deliberately attempt to replace the fixed dimension."""

                @property
                def model_id(self) -> str:
                    return "test.invalid.dimension"

                @property
                def model_role(self) -> PeriodicModelRole:
                    return PeriodicModelRole.CONTROL_MODEL

                @property  # type: ignore[misc]
                def spatial_dimension(self) -> int:  # type: ignore[override]
                    return 2
