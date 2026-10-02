"""Immutable retained portable Wannier90 comparison document."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DWannier90BalancedCampaignModel:
    """Store exact version-one balanced Wannier90 result bytes."""

    result_payload: bytes

    def __post_init__(self) -> None:
        if not self.result_payload:
            raise ValueError("retained result payload must be nonempty")
