"""Immutable encoded documents for the periodic-2D topological benchmark."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DTopologicalEncodedDocuments:
    """Store exact version-one topological input and result bytes."""

    input_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Require nonempty exact byte representations."""
        if type(self.input_payload) is not bytes:
            raise TypeError("input_payload must be exact bytes")
        if not self.input_payload:
            raise ValueError("input_payload must be nonempty")
        if type(self.result_payload) is not bytes:
            raise TypeError("result_payload must be exact bytes")
        if not self.result_payload:
            raise ValueError("result_payload must be nonempty")
