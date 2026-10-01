"""Correlate retained and maintained topological phase-sweep campaign documents."""

import hashlib
import json
from dataclasses import dataclass
from typing import cast

from ...model.retained.topological_phase_sweep import (
    Periodic2DTopologicalPhaseSweepCampaignModel,
)
from .calculate import (
    Periodic2DTopologicalPhaseSweepCalculationRequest,
    Periodic2DTopologicalPhaseSweepCalculationWorkflow,
    Periodic2DTopologicalPhaseSweepProvenance,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


@dataclass(frozen=True, slots=True)
class Periodic2DTopologicalPhaseSweepCampaignCorrelationRequest:
    """Request deterministic retained-document correlation."""

    model: Periodic2DTopologicalPhaseSweepCampaignModel


@dataclass(frozen=True, slots=True)
class Periodic2DTopologicalPhaseSweepCampaignCorrelationResult:
    """Report semantic and exact-byte document identities."""

    semantic_identity: bool
    canonical_byte_identity: bool
    calculated_sha256: str
    retained_sha256: str

    @property
    def passes(self) -> bool:
        """Return whether both identity channels pass."""
        return self.semantic_identity and self.canonical_byte_identity


class Periodic2DTopologicalPhaseSweepCampaignCorrelator:
    """Regenerate a retained result under its recorded provenance."""

    __slots__ = ()
    workflow = Periodic2DTopologicalPhaseSweepCalculationWorkflow()

    def execute(
        self, request: Periodic2DTopologicalPhaseSweepCampaignCorrelationRequest
    ) -> Periodic2DTopologicalPhaseSweepCampaignCorrelationResult:
        """Return semantic and byte identities for one campaign."""
        retained = self._mapping(
            cast(JsonValue, json.loads(request.model.result_payload))
        )
        provenance = self._mapping(retained["provenance"])
        calculated = self.workflow.execute(
            Periodic2DTopologicalPhaseSweepCalculationRequest(
                request.model.input_payload,
                Periodic2DTopologicalPhaseSweepProvenance(
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
        return Periodic2DTopologicalPhaseSweepCampaignCorrelationResult(
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
