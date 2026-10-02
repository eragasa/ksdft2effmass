"""Software verification for explicit immutable periodic toy-model catalogs."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, dataclass

import pytest

from ksdft2effmass.periodic import (
    Periodic1DModel,
    Periodic2DModel,
    Periodic3DModel,
    PeriodicModel,
    PeriodicModelRole,
    PeriodicToyModelCatalog,
)

pytestmark = pytest.mark.software_verification


class TestPeriodicToyModelCatalog:
    """Verify explicit registration, order, and nominal membership constraints."""

    @dataclass(frozen=True, slots=True)
    class Toy1D(Periodic1DModel):
        """Represent a synthetic registered one-dimensional toy model."""

        identity: str

        @property
        def model_id(self) -> str:
            """Return the caller-provided test identity."""
            return self.identity

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the toy role."""
            return PeriodicModelRole.TOY

    @dataclass(frozen=True, slots=True)
    class Toy2D(Periodic2DModel):
        """Represent a synthetic registered two-dimensional toy model."""

        @property
        def model_id(self) -> str:
            """Return the test-owned identity."""
            return "test.toy.2d"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the toy role."""
            return PeriodicModelRole.TOY

    @dataclass(frozen=True, slots=True)
    class Toy3D(Periodic3DModel):
        """Represent a synthetic registered three-dimensional toy model."""

        @property
        def model_id(self) -> str:
            """Return the test-owned identity."""
            return "test.toy.3d"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the toy role."""
            return PeriodicModelRole.TOY

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
            return "toy"

    @dataclass(frozen=True, slots=True)
    class WrongIdentity1D(Periodic1DModel):
        """Represent a model whose identity has the wrong runtime type."""

        @property
        def model_id(self) -> int:  # type: ignore[override]
            """Return an invalid integer identity."""
            return 1

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the toy role."""
            return PeriodicModelRole.TOY

    @dataclass(frozen=True, slots=True)
    class BooleanDimensionToy(PeriodicModel):
        """Represent a root-only model with an invalid boolean dimension."""

        @property
        def model_id(self) -> str:
            """Return the test-owned identity."""
            return "test.boolean-dimension"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the toy role."""
            return PeriodicModelRole.TOY

        @property
        def spatial_dimension(self) -> bool:  # type: ignore[override]
            """Return an invalid boolean dimension."""
            return True

    @dataclass(frozen=True, slots=True)
    class RootOnlyToy(PeriodicModel):
        """Represent a model lacking nominal dimension-branch membership."""

        @property
        def model_id(self) -> str:
            """Return the test-owned identity."""
            return "test.root-only"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the toy role."""
            return PeriodicModelRole.TOY

        @property
        def spatial_dimension(self) -> int:  # type: ignore[override]
            """Return a valid value without valid nominal membership."""
            return 1

    def test_constructor__models__preserves_explicit_deterministic_order(self) -> None:
        """Catalog order is exactly the caller's immutable registration order."""
        catalog = PeriodicToyModelCatalog(
            models=(self.Toy2D(), self.Toy1D("test.toy.1d"), self.Toy3D())
        )

        assert catalog.model_ids == (
            "test.toy.2d",
            "test.toy.1d",
            "test.toy.3d",
        )
        assert catalog.spatial_dimensions == (2, 1, 3)
        assert tuple(type(value) for value in catalog.spatial_dimensions) == (
            int,
            int,
            int,
        )

    def test_constructor__models__requires_an_exact_nonempty_tuple(self) -> None:
        """Mutable and empty model inventories are rejected."""
        with pytest.raises(TypeError, match="exact tuple"):
            PeriodicToyModelCatalog(models=[self.Toy2D()])  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="nonempty"):
            PeriodicToyModelCatalog(models=())

    def test_constructor__models__requires_periodic_model_members(self) -> None:
        """Catalog registration rejects values outside the nominal model root."""
        with pytest.raises(TypeError, match="PeriodicModel"):
            PeriodicToyModelCatalog(models=("not a model",))  # type: ignore[arg-type]

    def test_constructor__models__requires_toy_role(self) -> None:
        """Material-reference models cannot enter the toy-model catalog."""
        with pytest.raises(ValueError, match="TOY role"):
            PeriodicToyModelCatalog(models=(self.MaterialReference2D(),))

    def test_constructor__model_role__requires_exact_enum_type(self) -> None:
        """A coercible role string cannot substitute for the closed role enum."""
        with pytest.raises(TypeError, match="PeriodicModelRole"):
            PeriodicToyModelCatalog(models=(self.WrongRole1D(),))

    def test_constructor__model_id__requires_exact_string_type(self) -> None:
        """A numeric identity cannot substitute for an exact string."""
        with pytest.raises(TypeError, match="exact str"):
            PeriodicToyModelCatalog(models=(self.WrongIdentity1D(),))

    def test_constructor__spatial_dimension__rejects_boolean(self) -> None:
        """A boolean cannot substitute for an exact built-in dimension integer."""
        with pytest.raises(TypeError, match="exact int"):
            PeriodicToyModelCatalog(models=(self.BooleanDimensionToy(),))

    def test_constructor__models__requires_unique_nonempty_identity(self) -> None:
        """Every explicit registration has a nonempty unique identity."""
        with pytest.raises(ValueError, match="nonempty"):
            PeriodicToyModelCatalog(models=(self.Toy1D(""),))
        with pytest.raises(ValueError, match="unique"):
            PeriodicToyModelCatalog(
                models=(self.Toy1D("duplicate"), self.Toy1D("duplicate"))
            )

    def test_constructor__models__requires_nominal_dimension_membership(self) -> None:
        """A reported dimension cannot substitute for nominal branch membership."""
        with pytest.raises(ValueError, match="nominal dimension membership"):
            PeriodicToyModelCatalog(models=(self.RootOnlyToy(),))

    def test_instance__catalog__is_immutable(self) -> None:
        """Registered model order cannot be replaced after construction."""
        catalog = PeriodicToyModelCatalog(models=(self.Toy2D(),))

        with pytest.raises(FrozenInstanceError):
            catalog.models = (self.Toy3D(),)  # type: ignore[misc]
