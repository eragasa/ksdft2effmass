"""Immutable retained-wire model for the isolated periodic-2D campaign."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DIsolatedBandCampaignModel:
    """Store exact version-one isolated campaign input and result payloads."""

    input_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Require nonempty exact byte representations."""
        if type(self.input_payload) is not bytes or not self.input_payload:
            raise ValueError("input_payload must be nonempty built-in bytes")
        if type(self.result_payload) is not bytes or not self.result_payload:
            raise ValueError("result_payload must be nonempty built-in bytes")
