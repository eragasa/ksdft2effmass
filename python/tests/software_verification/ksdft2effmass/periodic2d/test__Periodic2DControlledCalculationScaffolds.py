"""Software verification for the periodic-2D calculation scaffolds."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, dataclass

import pytest

from ksdft2effmass.periodic import (
    Periodic1DModel,
    Periodic2DModel,
    PeriodicModelRole,
)
from ksdft2effmass.periodic2d import (
    Periodic2DRepresentedParentCalculationScaffold,
    Periodic2DShellGaugeLocalityCalculationScaffold,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DControlledCalculationScaffolds:
    """Verify nominal parent inheritance and explicit M4-to-M5 composition."""

    @dataclass(frozen=True, slots=True)
    class Toy2D(Periodic2DModel):
        """Represent a synthetic nominal two-dimensional parent model."""

        @property
        def model_id(self) -> str:
            """Return the synthetic model identity."""
            return "test.periodic2d.parent"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the exact toy role."""
            return PeriodicModelRole.TOY

    @dataclass(frozen=True, slots=True)
    class Toy1D(Periodic1DModel):
        """Represent a wrong-dimensional synthetic parent model."""

        @property
        def model_id(self) -> str:
            """Return the synthetic model identity."""
            return "test.periodic1d.parent"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the exact toy role."""
            return PeriodicModelRole.TOY

    def test_construction__m4__requires_nominal_2d_parent(self) -> None:
        """M4 records its parent through the nominal 2D model branch."""
        parent = self.Toy2D()

        represented = Periodic2DRepresentedParentCalculationScaffold("m4-test", parent)

        assert represented.parent_model is parent
        assert isinstance(represented.parent_model, Periodic2DModel)

    def test_construction__m5__composes_m4_without_campaign_inheritance(self) -> None:
        """M5 retains its exact M4 baseline instead of subclassing M4."""
        baseline = Periodic2DRepresentedParentCalculationScaffold(
            "m4-test", self.Toy2D()
        )

        locality = Periodic2DShellGaugeLocalityCalculationScaffold("m5-test", baseline)

        assert locality.represented_parent_baseline is baseline
        assert locality.parent_model is baseline.parent_model
        assert not issubclass(
            Periodic2DShellGaugeLocalityCalculationScaffold,
            Periodic2DRepresentedParentCalculationScaffold,
        )

    def test_construction__wrong_dimension__raises_type_error(self) -> None:
        """Structural similarity cannot substitute for nominal 2D inheritance."""
        with pytest.raises(TypeError, match="inherit Periodic2DModel"):
            Periodic2DRepresentedParentCalculationScaffold(
                "m4-test",
                self.Toy1D(),  # type: ignore[arg-type]
            )

    def test_construction__wrong_baseline_type__raises_type_error(self) -> None:
        """M5 cannot silently accept an unrelated same-shaped input."""
        with pytest.raises(TypeError, match="represented_parent_baseline"):
            Periodic2DShellGaugeLocalityCalculationScaffold(
                "m5-test",
                self.Toy2D(),  # type: ignore[arg-type]
            )

    def test_mutation__frozen_scaffold__raises_frozen_instance_error(self) -> None:
        """Study dependency records are operationally immutable."""
        scaffold = Periodic2DRepresentedParentCalculationScaffold(
            "m4-test", self.Toy2D()
        )

        with pytest.raises(FrozenInstanceError):
            scaffold.definition_id = "changed"  # type: ignore[misc]
