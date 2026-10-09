"""Immutable encoded documents for the periodic-2D topological benchmark."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DTopologicalEncodedDocuments:
    """Retain exact encoded periodic-2D topological campaign documents.

    Parameters
    ----------
    input_payload
        Exact nonempty built-in bytes for the retained topological input document.
    result_payload
        Exact nonempty built-in bytes for the retained topological result document.

    Raises
    ------
    TypeError
        If either payload is not exact built-in :class:`bytes`.
    ValueError
        If either payload is empty.

    Notes
    -----
    The DataObject preserves byte identity without decoding, normalization, copying, or
    filesystem access. Encoded expected observations are retained campaign content, not
    qualified numerical oracles. The owner assigns no model, topology, provenance,
    convergence, validation, uncertainty, or acceptance meaning.
    """

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
