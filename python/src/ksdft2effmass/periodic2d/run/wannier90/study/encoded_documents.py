"""Immutable encoded portable Wannier90 study documents."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DWannier90StudyEncodedDocuments:
    """Retain exact encoded periodic-2D Wannier90 study documents.

    Parameters
    ----------
    input_payload
        Exact nonempty built-in bytes for the retained study input document.
    result_payload
        Exact nonempty built-in bytes for the retained study result document.

    Raises
    ------
    TypeError
        If either payload is not exact built-in :class:`bytes`.
    ValueError
        If either payload is empty.

    Notes
    -----
    The DataObject preserves byte identity without decoding, normalization, copying, or
    filesystem access. It does not interpret sensitivity axes, authenticate case
    completion or native files, prove numerical convergence, validate localization or
    embedding choices, quantify uncertainty, or record acceptance. Encoded observations
    remain retained campaign content until explicit scientific owners adopt them.
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
