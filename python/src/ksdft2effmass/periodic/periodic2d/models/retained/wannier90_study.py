"""Immutable retained portable Wannier90 study documents."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DWannier90StudyCampaignModel:
    """Store exact version-one study input and result bytes."""

    input_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        if not self.input_payload or not self.result_payload:
            raise ValueError("retained payloads must be nonempty")
