"""Immutable retained-wire model for the composite periodic-2D campaign."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DCompositeCampaignModel:
    """Store exact version-one composite input and result payloads."""

    input_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Require nonempty exact byte representations."""
        if type(self.input_payload) is not bytes or not self.input_payload:
            raise ValueError("input_payload must be nonempty exact bytes")
        if type(self.result_payload) is not bytes or not self.result_payload:
            raise ValueError("result_payload must be nonempty exact bytes")
