"""Immutable encoded portable Wannier90 comparison document."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DWannier90BalancedEncodedDocuments:
    """Retain an exact encoded balanced Wannier90 result document.

    Parameters
    ----------
    result_payload
        Exact nonempty built-in bytes for the retained balanced-comparison result.

    Raises
    ------
    TypeError
        If ``result_payload`` is not exact built-in :class:`bytes`.
    ValueError
        If ``result_payload`` is empty.

    Notes
    -----
    The DataObject preserves byte identity without decoding, normalization, copying, or
    filesystem access. It owns no input document and does not imply that native
    Wannier90 files exist. Encoded observations do not establish execution provenance,
    localization convergence, decoded correctness, scientific validation, uncertainty,
    or acceptance.
    """

    result_payload: bytes

    def __post_init__(self) -> None:
        """Require a nonempty exact byte representation."""
        if type(self.result_payload) is not bytes:
            raise TypeError("result_payload must be exact bytes")
        if not self.result_payload:
            raise ValueError("result_payload must be nonempty")
