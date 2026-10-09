"""Exact encoded documents for the periodic-1D composite campaign."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeEncodedDocuments:
    """Store exact version-one composite campaign input and result bytes.

    Parameters
    ----------
    input_payload
        Nonempty immutable JSON bytes for the composite campaign definition.
    result_payload
        Nonempty immutable JSON bytes for the retained composite campaign result.

    Raises
    ------
    TypeError
        If either payload is not exact built-in :class:`bytes`.
    ValueError
        If either payload is empty.

    Notes
    -----
    This DataObject owns encoded documents only. It preserves caller-supplied byte
    objects without decoding, normalization, or copying. Correlation, verification,
    source authentication, scientific retention, and adoption remain separate campaign
    operations. In particular, the bytes do not define the composite retained band
    groups, their frames, or their represented operators. A payload or its digest
    identifies content only; neither establishes provenance, scientific validity,
    uncertainty quantification, or acceptance.
    """

    input_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Validate exact nonempty composite payload representations.

        Raises
        ------
        TypeError
            If either field is not exact built-in :class:`bytes`.
        ValueError
            If either exact byte representation is empty.
        """
        if type(self.input_payload) is not bytes:
            raise TypeError("input_payload must be built-in bytes")
        if not self.input_payload:
            raise ValueError("input_payload must be nonempty")
        if type(self.result_payload) is not bytes:
            raise TypeError("result_payload must be built-in bytes")
        if not self.result_payload:
            raise ValueError("result_payload must be nonempty")
