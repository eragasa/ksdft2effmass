"""Software verification for ``Periodic2DIsolatedBandCampaignDefinition``."""

from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.campaign.nbands_1 import (
    Periodic2DIsolatedBandCampaignDefinition,
    Periodic2DIsolatedBandCampaignJsonSerializer,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DIsolatedBandCampaignDefinition:
    """Own exact-type, invariant, and immutability evidence for the definition."""

    @staticmethod
    def definition() -> Periodic2DIsolatedBandCampaignDefinition:
        """Decode the retained version-one definition through its public boundary."""
        root = Path(__file__).resolve().parents[7]
        payload = root.joinpath(
            "calculations/research-monograph/periodic-2d/input.json"
        ).read_bytes()
        return Periodic2DIsolatedBandCampaignJsonSerializer().deserialize(payload)

    def test_construction__retained_controls__are_exact_and_immutable(self) -> None:
        """The record retains dimensionless controls without mutable containers."""
        definition = self.definition()

        assert definition.plane_wave_cutoffs == (1, 2, 3, 4)
        assert definition.parent_sample_momenta[2] == (0.25, -0.25)
        assert definition.shell_squared_radii[-1] == 98
        with pytest.raises(FrozenInstanceError):
            definition.experiment_id = "changed"  # type: ignore[misc]

    def test_construction__integer_for_real_control__raises_type_error(self) -> None:
        """A built-in integer is not coerced into a documented float control."""
        definition = self.definition()

        with pytest.raises(TypeError, match="lattice_period must be a built-in float"):
            replace(definition, lattice_period=6)

    def test_construction__aliased_momentum_component__raises_type_error(self) -> None:
        """Momentum components require exact built-in floats before calculation."""
        definition = self.definition()

        with pytest.raises(TypeError, match="components must be built-in floats"):
            replace(
                definition,
                parent_sample_momenta=((0.0, 0.0), (1, 0.0)),
            )
