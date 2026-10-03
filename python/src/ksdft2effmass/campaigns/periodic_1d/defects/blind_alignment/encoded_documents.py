"""Encoded documents for the periodic-1D blind-alignment campaign."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BlindAlignmentEncodedDocuments:
    """Store exact input and result document bytes for blind alignment.

    Parameters
    ----------
    input_document
        Exact immutable version-one input JSON bytes.
    retained_result_document
        Exact immutable version-one retained-result JSON bytes.

    Notes
    -----
    This DataObject owns encoded documents only. Repository resolution belongs to the
    campaign requests that perform authenticated filesystem access.
    """

    input_document: bytes
    retained_result_document: bytes

    def __post_init__(self) -> None:
        """Require nonempty exact byte representations."""
        if type(self.input_document) is not bytes:
            raise TypeError("input_document must be exact bytes")
        if not self.input_document:
            raise ValueError("input_document must be nonempty")
        if type(self.retained_result_document) is not bytes:
            raise TypeError("retained_result_document must be exact bytes")
        if not self.retained_result_document:
            raise ValueError("retained_result_document must be nonempty")
