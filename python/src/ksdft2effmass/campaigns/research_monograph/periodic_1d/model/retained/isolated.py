"""Immutable retained-wire model for the isolated periodic-1D campaign."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandCampaignModel:
    """Store exact version-one isolated campaign input and result payloads.

    Parameters
    ----------
    input_payload
        Nonempty immutable JSON bytes for the isolated campaign definition.
    result_payload
        Nonempty immutable JSON bytes for the retained isolated campaign result.

    Notes
    -----
    This DataObjectModel owns encoded state only. Correlation and verification policy
    belong to separate Actionizers.
    """

    input_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Require nonempty exact byte representations."""
        if type(self.input_payload) is not bytes or not self.input_payload:
            raise ValueError("input_payload must be nonempty built-in bytes")
        if type(self.result_payload) is not bytes or not self.result_payload:
            raise ValueError("result_payload must be nonempty built-in bytes")
