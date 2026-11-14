"""Immutable retained optimizer reanalysis documents."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerReanalysisCampaignModel:
    """Store exact source and reanalysis result bytes."""

    source_result_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        if not self.source_result_payload or not self.result_payload:
            raise ValueError("retained payloads must be nonempty")
