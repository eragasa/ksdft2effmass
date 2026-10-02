"""Immutable retained standalone optimizer-study documents."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerStandaloneCampaignModel:
    """Store exact proposal, gauge-design, and result bytes."""

    proposal_payload: bytes
    initial_gauges_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        if (
            not self.proposal_payload
            or not self.initial_gauges_payload
            or not self.result_payload
        ):
            raise ValueError("retained payloads must be nonempty")
