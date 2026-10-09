r"""Exact encoded documents for periodic-1D route reconciliation.

The module owns encoded transport state only. It does not decode the version-one wire,
resolve repository paths, authenticate matched-extraction or periodic-parent sources,
construct either represented route, reconcile route compatibility, or verify retained
numerical observations.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RouteReconciliationEncodedDocuments:
    r"""Store exact route-reconciliation input and retained-result bytes.

    Parameters
    ----------
    input_document
        Exact nonempty built-in :class:`bytes` containing the encoded campaign
        input.
    retained_result_document
        Exact nonempty built-in :class:`bytes` containing the encoded retained
        result.

    Raises
    ------
    TypeError
        If either value is not exact built-in :class:`bytes`. Text, bytearray,
        memory-view, and ``bytes`` subclasses are not coerced.
    ValueError
        If either exact byte representation is empty.

    Notes
    -----
    Construction preserves the supplied immutable byte objects. It performs no copy,
    decoding, normalization, source authentication, filesystem access, route
    construction, reconciliation, verification, or scientific interpretation.
    Repository location belongs to the exact operation request that authenticates
    repository-relative sources, not to this DataObject.

    The encoded values do not themselves define a parent model, represented
    operator, defect operator, common state space, alignment map, reconciliation,
    numerical result, provenance record, uncertainty statement, or acceptance
    decision. Their names, lengths, JSON appearance, paths, and hashes must not be
    used to infer those meanings. A matching SHA-256 value establishes content
    identity only.
    """

    input_document: bytes
    retained_result_document: bytes

    def __post_init__(self) -> None:
        """Require nonempty exact byte representations.

        Raises
        ------
        TypeError
            If either field is not exact built-in :class:`bytes`.
        ValueError
            If either exact byte representation is empty.
        """
        if type(self.input_document) is not bytes:
            raise TypeError("input_document must be exact bytes")
        if not self.input_document:
            raise ValueError("input_document must be nonempty")
        if type(self.retained_result_document) is not bytes:
            raise TypeError("retained_result_document must be exact bytes")
        if not self.retained_result_document:
            raise ValueError("retained_result_document must be nonempty")
