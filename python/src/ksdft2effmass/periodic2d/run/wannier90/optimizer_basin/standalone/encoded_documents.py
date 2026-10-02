"""Immutable encoded standalone optimizer-study documents."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerStandaloneEncodedDocuments:
    """Store exact proposal, gauge-design, and result bytes."""

    proposal_payload: bytes
    initial_gauges_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Require nonempty exact byte representations."""
        for name, payload in (
            ("proposal_payload", self.proposal_payload),
            ("initial_gauges_payload", self.initial_gauges_payload),
            ("result_payload", self.result_payload),
        ):
            if type(payload) is not bytes:
                raise TypeError(f"{name} must be exact bytes")
            if not payload:
                raise ValueError(f"{name} must be nonempty")
