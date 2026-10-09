"""Immutable encoded optimizer-basin reanalysis documents."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerReanalysisEncodedDocuments:
    """Retain exact source-result and offline-reanalysis result documents.

    Parameters
    ----------
    source_result_payload
        Exact nonempty built-in bytes for the row-052 optimizer-basin result consumed by
        the offline reanalysis.
    result_payload
        Exact nonempty built-in bytes for the retained offline reanalysis result.

    Raises
    ------
    TypeError
        If either payload is not exact built-in :class:`bytes`.
    ValueError
        If either payload is empty.

    Notes
    -----
    This frozen, slotted DataObject owns byte representation only. It performs no JSON
    decoding, normalization, copying, filesystem access, native-file authentication,
    spread reconstruction, trace classification, basin classification, convergence
    decision, uncertainty analysis, or scientific acceptance. Source/result correlation
    belongs to an explicit verifier Action.
    """

    source_result_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Validate exact nonempty wire representations."""
        self._check_args_payloads()

    def _check_args_payloads(self) -> None:
        """Require both payloads to be exact nonempty built-in bytes."""
        for name, payload in (
            ("source_result_payload", self.source_result_payload),
            ("result_payload", self.result_payload),
        ):
            if type(payload) is not bytes:
                raise TypeError(f"{name} must be exact bytes")
            if not payload:
                raise ValueError(f"{name} must be nonempty")
