"""Encoded documents for the periodic-1D blind-alignment campaign."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BlindAlignmentEncodedDocuments:
    """Store exact input and retained-result bytes for blind alignment.

    Parameters
    ----------
    input_document
        Nonempty exact built-in :class:`bytes` for the version-one blind-alignment
        campaign input document.
    retained_result_document
        Nonempty exact built-in :class:`bytes` for the version-one retained campaign
        result document.

    Raises
    ------
    TypeError
        If either field is not exact built-in :class:`bytes`.
    ValueError
        If either exact byte representation is empty.

    Notes
    -----
    This frozen DataObject owns encoded documents only. It preserves caller-supplied
    byte objects without decoding, normalization, re-encoding, coercion, or copying.
    It is not a physical model, finite representation, retained space, represented
    operator, decoded campaign result, or scientific acceptance record.

    Repository location is deliberately absent. Absolute repository roots belong to
    calculation, retained-correlation, and verification requests that perform explicit
    authenticated source access. Content bytes or SHA-256 digests cannot supply a
    repository root, execution provenance, hidden alignment truth, scientific validity,
    uncertainty quantification, or acceptance.
    """

    input_document: bytes
    retained_result_document: bytes

    def __post_init__(self) -> None:
        """Validate the two exact nonempty encoded representations.

        Raises
        ------
        TypeError
            If either field is not exact built-in :class:`bytes`.
        ValueError
            If either exact byte representation is empty.
        """
        # Exact bytes prevent implicit JSON decoding or normalization at this storage
        # boundary; semantic validation belongs to explicit deserializers.
        if type(self.input_document) is not bytes:
            raise TypeError("input_document must be exact bytes")
        if not self.input_document:
            raise ValueError("input_document must be nonempty")
        if type(self.retained_result_document) is not bytes:
            raise TypeError("retained_result_document must be exact bytes")
        if not self.retained_result_document:
            raise ValueError("retained_result_document must be nonempty")
