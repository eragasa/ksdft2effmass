"""Immutable encoded documents for the composite periodic-2D campaign."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DCompositeEncodedDocuments:
    """Retain exact encoded periodic-2D composite campaign documents.

    Parameters
    ----------
    input_payload
        Exact nonempty built-in bytes for the retained composite input document.
    result_payload
        Exact nonempty built-in bytes for the retained composite result document.

    Raises
    ------
    TypeError
        If either payload is not exact built-in :class:`bytes`.
    ValueError
        If either payload is empty.

    Notes
    -----
    The DataObject preserves byte identity without decoding, normalization, copying, or
    filesystem access. It assigns no schema, scientific model, retained band group,
    frame, operator, provenance, convergence, validation, uncertainty, or acceptance
    meaning.
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
