"""Correlate retained and maintained topological campaign documents."""

import hashlib
import json
from dataclasses import dataclass
from typing import cast

from ...model.retained.topological import Periodic2DTopologicalCampaignModel
from .calculate import (
    Periodic2DTopologicalCalculationRequest,
    Periodic2DTopologicalCalculationWorkflow,
    Periodic2DTopologicalProvenance,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


@dataclass(frozen=True, slots=True)
class Periodic2DTopologicalCampaignCorrelationRequest:
    """Request deterministic retained-document correlation."""

    model: Periodic2DTopologicalCampaignModel


@dataclass(frozen=True, slots=True)
class Periodic2DTopologicalCampaignCorrelationResult:
    """Report semantic and exact-byte document identities."""

    semantic_identity: bool
    canonical_byte_identity: bool
    calculated_sha256: str
    retained_sha256: str

    @property
    def passes(self) -> bool:
        """Return whether both identity channels pass."""
        return self.semantic_identity and self.canonical_byte_identity


class Periodic2DTopologicalCampaignCorrelator:
    """Regenerate a retained result under its recorded provenance."""

    __slots__ = ()
    workflow = Periodic2DTopologicalCalculationWorkflow()

    def execute(
        self, request: Periodic2DTopologicalCampaignCorrelationRequest
    ) -> Periodic2DTopologicalCampaignCorrelationResult:
        """Return semantic and byte identities for one campaign."""
        retained = self._mapping(
            cast(JsonValue, json.loads(request.model.result_payload))
        )
        provenance = self._mapping(retained["provenance"])
        calculated = self.workflow.execute(
            Periodic2DTopologicalCalculationRequest(
                request.model.input_payload,
                Periodic2DTopologicalProvenance(
                    self._string(retained["generated_at_utc"]),
                    self._string(provenance["input_sha256"]),
                    self._string(provenance["runner_sha256"]),
                    self._string(provenance["python_version"]),
                    self._string(provenance["numpy_version"]),
                ),
            )
        ).document
        calculated_value = cast(JsonValue, json.loads(calculated))
        retained_value = cast(JsonValue, json.loads(request.model.result_payload))
        return Periodic2DTopologicalCampaignCorrelationResult(
            calculated_value == retained_value,
            calculated == request.model.result_payload,
            hashlib.sha256(calculated).hexdigest(),
            hashlib.sha256(request.model.result_payload).hexdigest(),
        )

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected mapping")
        return value

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected string")
        return value
