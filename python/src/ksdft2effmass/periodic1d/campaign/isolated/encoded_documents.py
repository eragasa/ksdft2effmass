"""Exact encoded documents for the periodic-1D isolated-band campaign."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandEncodedDocuments:
    """Store exact version-one isolated campaign input and result bytes.

    Parameters
    ----------
    input_payload
        Nonempty immutable JSON bytes for the isolated campaign definition.
    result_payload
        Nonempty immutable JSON bytes for the retained isolated campaign result.

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
    source authentication, and scientific interpretation remain separate campaign
    operations. A payload or its digest identifies content only; neither establishes
    provenance, scientific validity, uncertainty quantification, or acceptance.
    """

    input_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Validate exact nonempty isolated-band payload representations."""
        self._check_args_payload("input_payload", self.input_payload)
        self._check_args_payload("result_payload", self.result_payload)

    def _check_args_payload(self, name: str, payload: bytes) -> None:
        """Require one nonempty exact built-in byte representation.

        Parameters
        ----------
        name
            Field name used in the fail-closed diagnostic.
        payload
            Candidate encoded document supplied by the constructor.

        Raises
        ------
        TypeError
            If ``payload`` is not exact built-in :class:`bytes`.
        ValueError
            If ``payload`` is empty.
        """
        if type(payload) is not bytes:
            raise TypeError(f"{name} must be built-in bytes")
        if not payload:
            raise ValueError(f"{name} must be nonempty")
