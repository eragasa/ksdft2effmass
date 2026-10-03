"""Immutable encoded portable Wannier90 comparison document."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DWannier90BalancedEncodedDocuments:
    """Store exact version-one balanced Wannier90 result bytes."""

    result_payload: bytes

    def __post_init__(self) -> None:
        """Require a nonempty exact byte representation."""
        if type(self.result_payload) is not bytes:
            raise TypeError("result_payload must be exact bytes")
        if not self.result_payload:
            raise ValueError("result_payload must be nonempty")
