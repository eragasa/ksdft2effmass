"""Immutable encoded optimizer-basin study documents."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerBasinEncodedDocuments:
    """Retain exact encoded periodic-2D optimizer-basin study documents.

    Parameters
    ----------
    input_payload
        Exact nonempty built-in bytes for the retained optimizer-basin study input.
    result_payload
        Exact nonempty built-in bytes for the retained optimizer-basin study result.

    Raises
    ------
    TypeError
        If either payload is not exact built-in :class:`bytes`.
    ValueError
        If either payload is empty.

    Notes
    -----
    The DataObject preserves byte identity without decoding, normalization, copying, or
    filesystem access. It does not interpret initial gauges or observed basins,
    authenticate execution or native files, prove convergence or a global optimum,
    validate optimizer behavior, quantify uncertainty, or record acceptance. The
    retained negative convergence disposition remains encoded content until an explicit
    verifier adopts it.
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
