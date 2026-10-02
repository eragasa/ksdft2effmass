"""Immutable encoded documents for periodic one-dimensional campaigns."""

from dataclasses import dataclass

from .result_documents import Periodic1DRetainedResultKind


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandEncodedDocuments:
    """Store exact version-one isolated campaign input and result bytes.

    Parameters
    ----------
    input_payload
        Nonempty immutable JSON bytes for the isolated campaign definition.
    result_payload
        Nonempty immutable JSON bytes for the retained isolated campaign result.

    Notes
    -----
    This DataObject owns encoded documents only. Correlation and verification remain
    separate campaign operations.
    """

    input_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Require nonempty exact byte representations."""
        if type(self.input_payload) is not bytes:
            raise TypeError("input_payload must be built-in bytes")
        if not self.input_payload:
            raise ValueError("input_payload must be nonempty")
        if type(self.result_payload) is not bytes:
            raise TypeError("result_payload must be built-in bytes")
        if not self.result_payload:
            raise ValueError("result_payload must be nonempty")


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeEncodedDocuments:
    """Store exact version-one composite campaign input and result bytes.

    Parameters
    ----------
    input_payload
        Nonempty immutable JSON bytes for the composite campaign definition.
    result_payload
        Nonempty immutable JSON bytes for the retained composite campaign result.

    Notes
    -----
    This DataObject owns encoded documents only. Correlation and verification remain
    separate campaign operations.
    """

    input_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Require nonempty exact byte representations."""
        if type(self.input_payload) is not bytes:
            raise TypeError("input_payload must be built-in bytes")
        if not self.input_payload:
            raise ValueError("input_payload must be nonempty")
        if type(self.result_payload) is not bytes:
            raise TypeError("result_payload must be built-in bytes")
        if not self.result_payload:
            raise ValueError("result_payload must be nonempty")


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeEncodedDocuments:
    """Store exact input and result bytes for the reduction challenge campaign.

    Parameters
    ----------
    input_payload
        Nonempty immutable JSON bytes for the reduction challenge definition.
    result_payload
        Nonempty immutable JSON bytes for the retained reduction challenge result.

    Notes
    -----
    This DataObject owns encoded documents only. Correlation and verification remain
    separate campaign operations.
    """

    input_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Require nonempty exact byte representations."""
        if type(self.input_payload) is not bytes:
            raise TypeError("input_payload must be built-in bytes")
        if not self.input_payload:
            raise ValueError("input_payload must be nonempty")
        if type(self.result_payload) is not bytes:
            raise TypeError("result_payload must be built-in bytes")
        if not self.result_payload:
            raise ValueError("result_payload must be nonempty")


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90EncodedDocuments:
    """Store exact composite input and Wannier90 result document bytes.

    Parameters
    ----------
    composite_input_payload
        Nonempty immutable version-one composite campaign input bytes.
    result_payload
        Nonempty immutable Wannier90 result bytes.
    result_kind
        Exact supported result-document variant represented by ``result_payload``.

    Notes
    -----
    This DataObject owns encoded documents and their variant identity only. Native
    artifact groups remain separate integration inputs.
    """

    composite_input_payload: bytes
    result_payload: bytes
    result_kind: Periodic1DRetainedResultKind

    def __post_init__(self) -> None:
        """Require exact nonempty bytes and a supported Wannier90 result kind."""
        if type(self.composite_input_payload) is not bytes:
            raise TypeError("composite_input_payload must be built-in bytes")
        if not self.composite_input_payload:
            raise ValueError("composite_input_payload must be nonempty")
        if type(self.result_payload) is not bytes:
            raise TypeError("result_payload must be built-in bytes")
        if not self.result_payload:
            raise ValueError("result_payload must be nonempty")
        if type(self.result_kind) is not Periodic1DRetainedResultKind:
            raise TypeError("result_kind must be Periodic1DRetainedResultKind")
        if self.result_kind not in {
            Periodic1DRetainedResultKind.WANNIER90,
            Periodic1DRetainedResultKind.WANNIER90_PRECONDITIONED,
        }:
            raise ValueError("result_kind must identify a supported Wannier90 result")
