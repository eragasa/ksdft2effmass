"""Request values for rank-two hopping-locality analysis."""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.physkit.units import Unitless

from ksdft2effmass.periodic1d.hopping_locality.base import (
    Periodic1DHoppingLocalityAnalysisRequest,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.configuration import (
    Periodic1DCompositeBandAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.translations import (
    Periodic1DOrdinaryTranslationInventory,
)
from ksdft2effmass.solidstate.hopping_transforms import BlockHoppingModel1D


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRank2HoppingLocalityAnalysisRequest(
    Periodic1DHoppingLocalityAnalysisRequest
):
    """Bind one frozen rank-two channel to its unchanged ordinary hoppings."""

    configuration: Periodic1DCompositeBandAlignmentConfiguration
    channel: str
    ordinary_model: BlockHoppingModel1D

    def __post_init__(self) -> None:
        if (
            type(self.configuration)
            is not Periodic1DCompositeBandAlignmentConfiguration
        ):
            raise TypeError(
                "configuration must be Periodic1DCompositeBandAlignmentConfiguration"
            )
        if type(self.channel) is not str:
            raise TypeError("channel must be a built-in string")
        if self.channel not in self.configuration.HOPPING_LOCALITY_CHANNELS:
            raise ValueError("channel must belong to the frozen locality inventory")
        if type(self.ordinary_model) is not BlockHoppingModel1D:
            raise TypeError("ordinary_model must be an exact block-hopping model")
        model = self.ordinary_model
        inventory = Periodic1DOrdinaryTranslationInventory(model.representatives)
        half_size = self.configuration.construction_size // 2
        expected_representatives = tuple(range(-half_size + 1, half_size))
        if inventory.translations != expected_representatives:
            raise ValueError("ordinary model must use the frozen non-Nyquist inventory")
        if model.matrix_dimension != self.configuration.retained_rank:
            raise ValueError("ordinary model dimension must equal the retained rank")
        if model.maximum_range <= self.configuration.hopping_ranges[-1]:
            raise ValueError("ordinary support must exceed every diagnostic range")
        if (
            not isinstance(model.reciprocal_period.unit, Unitless)
            or model.reciprocal_period.magnitude != 1.0
        ):
            raise ValueError(
                "ordinary model must use the frozen unitless reciprocal period"
            )
        if any(not isinstance(block.unit, Unitless) for block in model.hopping_blocks):
            raise ValueError("ordinary hopping blocks must be unitless")

    @property
    def ordinary_translation_inventory(self) -> Periodic1DOrdinaryTranslationInventory:
        """Return the typed conjugate-closed ordinary translation inventory."""
        return Periodic1DOrdinaryTranslationInventory(
            self.ordinary_model.representatives
        )


__all__ = ["Periodic1DRank2HoppingLocalityAnalysisRequest"]
