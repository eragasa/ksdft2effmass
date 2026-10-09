r"""Exact encoded documents for the periodic-1D finite-rank-oracle campaign.

The module owns encoded transport state only. It does not decode the version-one wire,
resolve repository paths, authenticate the accepted parent or preceding campaign
results, execute the Bloch-resolvent or site-space routes, or qualify scientific
evidence.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FiniteRankOracleEncodedDocuments:
    r"""Store exact finite-rank-oracle input and retained-result bytes.

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
        If either value is not an exact built-in :class:`bytes` object. Bytearray,
        memory-view, text, and ``bytes`` subclasses are not coerced.
    ValueError
        If either exact byte representation is empty.

    Notes
    -----
    Construction preserves the supplied immutable byte objects. It performs no copy,
    decoding, normalization, source authentication, filesystem access, resolvent
    calculation, eigensolve, evidence qualification, or scientific interpretation.
    Repository location belongs to the operation that accesses authenticated
    sources, not to this DataObject.

    The encoded values do not themselves define a parent model, finite represented
    operator, defect operator, bound-state eigenspace, analytical oracle, numerical
    result, provenance record, uncertainty statement, or acceptance decision. Their
    names, lengths, JSON appearance, paths, and hashes must not be used to infer
    those meanings. A matching SHA-256 value establishes content identity only.
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
        # Exact representation is part of the retained wire boundary; do not coerce.
        if type(self.input_document) is not bytes:
            raise TypeError("input_document must be exact bytes")
        if not self.input_document:
            raise ValueError("input_document must be nonempty")
        if type(self.retained_result_document) is not bytes:
            raise TypeError("retained_result_document must be exact bytes")
        if not self.retained_result_document:
            raise ValueError("retained_result_document must be nonempty")
