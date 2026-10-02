"""Immutable retained topological phase-sweep documents."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DTopologicalPhaseSweepCampaignModel:
    """Store exact version-one phase-sweep input and result bytes."""

    input_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        if not self.input_payload or not self.result_payload:
            raise ValueError("retained payloads must be nonempty")
