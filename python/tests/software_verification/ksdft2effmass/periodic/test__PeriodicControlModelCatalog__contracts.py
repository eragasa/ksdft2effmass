"""Software verification for explicit immutable periodic control-model catalogs."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, dataclass

import pytest

from ksdft2effmass.periodic import (
    Periodic1DModel,
    Periodic2DModel,
    Periodic3DModel,
    PeriodicControlModelCatalog,
    PeriodicModel,
    PeriodicModelRole,
)

pytestmark = pytest.mark.software_verification


class TestPeriodicControlModelCatalog:
    """Verify explicit registration, order, and nominal membership constraints."""

    @dataclass(frozen=True, slots=True)
    class Control1D(Periodic1DModel):
        """Represent a synthetic registered one-dimensional control model."""

        identity: str

        @property
        def model_id(self) -> str:
            """Return the caller-provided test identity."""
            return self.identity

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the control-model role."""
            return PeriodicModelRole.CONTROL_MODEL

    @dataclass(frozen=True, slots=True)
    class Control2D(Periodic2DModel):
        """Represent a synthetic registered two-dimensional control model."""

        @property
        def model_id(self) -> str:
            """Return the test-owned identity."""
            return "test.control.2d"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the control-model role."""
            return PeriodicModelRole.CONTROL_MODEL

    @dataclass(frozen=True, slots=True)
    class Control3D(Periodic3DModel):
        """Represent a synthetic registered three-dimensional control model."""

        @property
        def model_id(self) -> str:
            """Return the test-owned identity."""
            return "test.control.3d"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the control-model role."""
            return PeriodicModelRole.CONTROL_MODEL

    @dataclass(frozen=True, slots=True)
    class MaterialReference2D(Periodic2DModel):
        """Represent a synthetic material-reference model."""

        @property
        def model_id(self) -> str:
            """Return the test-owned identity."""
            return "test.reference.2d"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the material-reference role."""
            return PeriodicModelRole.MATERIAL_REFERENCE

    @dataclass(frozen=True, slots=True)
    class WrongRole1D(Periodic1DModel):
        """Represent a model whose role has the wrong runtime type."""

        @property
        def model_id(self) -> str:
            """Return the test-owned identity."""
            return "test.wrong-role"

        @property
        def model_role(self) -> str:  # type: ignore[override]
            """Return an invalid string in place of the closed role enum."""
            return "control_model"

    @dataclass(frozen=True, slots=True)
    class WrongIdentity1D(Periodic1DModel):
        """Represent a model whose identity has the wrong runtime type."""

        @property
        def model_id(self) -> int:  # type: ignore[override]
            """Return an invalid integer identity."""
            return 1

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the control-model role."""
            return PeriodicModelRole.CONTROL_MODEL

    @dataclass(frozen=True, slots=True)
    class BooleanDimensionControl(PeriodicModel):
        """Represent a root-only model with an invalid boolean dimension."""

        @property
        def model_id(self) -> str:
            """Return the test-owned identity."""
            return "test.boolean-dimension"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the control-model role."""
            return PeriodicModelRole.CONTROL_MODEL

        @property
        def spatial_dimension(self) -> bool:  # type: ignore[override]
            """Return an invalid boolean dimension."""
            return True

    @dataclass(frozen=True, slots=True)
    class RootOnlyControl(PeriodicModel):
        """Represent a model lacking nominal dimension-branch membership."""

        @property
        def model_id(self) -> str:
            """Return the test-owned identity."""
            return "test.root-only"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the control-model role."""
            return PeriodicModelRole.CONTROL_MODEL

        @property
        def spatial_dimension(self) -> int:  # type: ignore[override]
            """Return a valid value without valid nominal membership."""
            return 1

    def test__PeriodicControlModelCatalog__constructor__models__preserves_explicit_deterministic_order(  # noqa: E501
        self,
    ) -> None:
        """Catalog order is exactly the caller's immutable registration order."""
        catalog = PeriodicControlModelCatalog(
            models=(
                self.Control2D(),
                self.Control1D("test.control.1d"),
                self.Control3D(),
            )
        )

        assert catalog.model_ids == (
            "test.control.2d",
            "test.control.1d",
            "test.control.3d",
        )
        assert catalog.spatial_dimensions == (2, 1, 3)
        assert tuple(type(value) for value in catalog.spatial_dimensions) == (
            int,
            int,
            int,
        )

    def test__PeriodicControlModelCatalog__constructor__models__requires_an_exact_nonempty_tuple(  # noqa: E501
        self,
    ) -> None:
        """Mutable and empty model inventories are rejected."""
        with pytest.raises(TypeError, match="exact tuple"):
            PeriodicControlModelCatalog(
                models=[self.Control2D()]  # type: ignore[arg-type]
            )
        with pytest.raises(ValueError, match="nonempty"):
            PeriodicControlModelCatalog(models=())

    def test__PeriodicControlModelCatalog__constructor__models__requires_periodic_model_members(  # noqa: E501
        self,
    ) -> None:
        """Catalog registration rejects values outside the nominal model root."""
        with pytest.raises(TypeError, match="PeriodicModel"):
            PeriodicControlModelCatalog(
                models=("not a model",)  # type: ignore[arg-type]
            )

    def test__PeriodicControlModelCatalog__constructor__models__requires_control_role(
        self,
    ) -> None:
        """Material-reference models cannot enter the control-model catalog."""
        with pytest.raises(ValueError, match="CONTROL_MODEL role"):
            PeriodicControlModelCatalog(models=(self.MaterialReference2D(),))

    def test__PeriodicControlModelCatalog__constructor__model_role__requires_exact_enum_type(  # noqa: E501
        self,
    ) -> None:
        """A coercible role string cannot substitute for the closed role enum."""
        with pytest.raises(TypeError, match="PeriodicModelRole"):
            PeriodicControlModelCatalog(models=(self.WrongRole1D(),))

    def test__PeriodicControlModelCatalog__constructor__model_id__requires_exact_string_type(  # noqa: E501
        self,
    ) -> None:
        """A numeric identity cannot substitute for an exact string."""
        with pytest.raises(TypeError, match="exact str"):
            PeriodicControlModelCatalog(models=(self.WrongIdentity1D(),))

    def test__PeriodicControlModelCatalog__constructor__spatial_dimension__rejects_boolean(  # noqa: E501
        self,
    ) -> None:
        """A boolean cannot substitute for an exact built-in dimension integer."""
        with pytest.raises(TypeError, match="exact int"):
            PeriodicControlModelCatalog(models=(self.BooleanDimensionControl(),))

    def test__PeriodicControlModelCatalog__constructor__models__requires_unique_nonempty_identity(  # noqa: E501
        self,
    ) -> None:
        """Every explicit registration has a nonempty unique identity."""
        with pytest.raises(ValueError, match="nonempty"):
            PeriodicControlModelCatalog(models=(self.Control1D(""),))
        with pytest.raises(ValueError, match="unique"):
            PeriodicControlModelCatalog(
                models=(
                    self.Control1D("duplicate"),
                    self.Control1D("duplicate"),
                )
            )

    def test__PeriodicControlModelCatalog__constructor__models__requires_nominal_dimension_membership(  # noqa: E501
        self,
    ) -> None:
        """A reported dimension cannot substitute for nominal branch membership."""
        with pytest.raises(ValueError, match="nominal dimension membership"):
            PeriodicControlModelCatalog(models=(self.RootOnlyControl(),))

    def test__PeriodicControlModelCatalog__instance__catalog__is_immutable(
        self,
    ) -> None:
        """Registered model order cannot be replaced after construction."""
        catalog = PeriodicControlModelCatalog(models=(self.Control2D(),))

        with pytest.raises(FrozenInstanceError):
            catalog.models = (self.Control3D(),)  # type: ignore[misc]
