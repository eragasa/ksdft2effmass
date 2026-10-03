"""Immutable encoded optimizer reanalysis documents."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerReanalysisEncodedDocuments:
    """Store exact source and reanalysis result bytes."""

    source_result_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Require nonempty exact byte representations."""
        if type(self.source_result_payload) is not bytes:
            raise TypeError("source_result_payload must be exact bytes")
        if not self.source_result_payload:
            raise ValueError("source_result_payload must be nonempty")
        if type(self.result_payload) is not bytes:
            raise TypeError("result_payload must be exact bytes")
        if not self.result_payload:
            raise ValueError("result_payload must be nonempty")
