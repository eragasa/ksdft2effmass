"""Execution-free planning Workflow for the defect-2D finite-domain campaign."""

from __future__ import annotations

from dataclasses import dataclass

from .finite_domain_cases import (
    FiniteDomainEffectsCaseEnumerator,
    FiniteDomainEffectsCaseInventory,
    FiniteDomainEffectsStudyDefinition,
)
from .serialization import FiniteDomainEffectsCaseInventoryJsonSerializer


@dataclass(frozen=True, slots=True)
class FiniteDomainEffectsCampaignPlanResult:
    """Retain one enumerated campaign inventory and its canonical plan bytes."""

    inventory: FiniteDomainEffectsCaseInventory
    serialized_plan: bytes

    def __post_init__(self) -> None:
        """Require the bytes to reconstruct the exact retained inventory."""
        if type(self.inventory) is not FiniteDomainEffectsCaseInventory:
            raise TypeError("inventory must be FiniteDomainEffectsCaseInventory")
        if type(self.serialized_plan) is not bytes:
            raise TypeError("serialized_plan must be bytes")
        serializer = FiniteDomainEffectsCaseInventoryJsonSerializer()
        reconstructed = serializer.deserialize(self.serialized_plan)
        if reconstructed != self.inventory:
            raise ValueError("serialized plan must reconstruct the retained inventory")
        if serializer.serialize(reconstructed) != self.serialized_plan:
            raise ValueError("serialized plan must use the canonical representation")


class FiniteDomainEffectsCampaignPlanningWorkflow:
    """Compose definition validation, case enumeration, and plan serialization only."""

    __slots__ = ()

    def execute(
        self, definition: FiniteDomainEffectsStudyDefinition
    ) -> FiniteDomainEffectsCampaignPlanResult:
        """Return a canonical execution-free plan without constructing operators."""
        if type(definition) is not FiniteDomainEffectsStudyDefinition:
            raise TypeError("definition must be FiniteDomainEffectsStudyDefinition")
        inventory = FiniteDomainEffectsCaseEnumerator().execute(definition)
        serialized_plan = FiniteDomainEffectsCaseInventoryJsonSerializer().serialize(
            inventory
        )
        return FiniteDomainEffectsCampaignPlanResult(inventory, serialized_plan)
