"""Exact immutable wires for the periodic-1D reduction challenge."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeEncodedDocuments:
    """Store exact input and result bytes for the reduction challenge campaign.

    Parameters
    ----------
    input_payload
        Nonempty immutable JSON bytes for the reduction challenge definition.
    result_payload
        Nonempty immutable JSON bytes for the retained reduction challenge result.

    Raises
    ------
    TypeError
        If either payload is not exact built-in :class:`bytes`.
    ValueError
        If either payload is empty.

    Notes
    -----
    This DataObject owns encoded documents only. ``ReductionChallenge`` names the
    campaign's adversarial tests of potential, discretization, band-isolation, gauge,
    hopping-range, and fitting-route assumptions; it does not denote mechanical stress.
    The record preserves the historical version-one ``stress`` filenames, experiment
    identity, and wire bytes without decoding, normalization, or copying. Correlation,
    verification, source authentication, and scientific interpretation remain separate
    operations. A payload or its digest identifies content only; neither establishes
    provenance, scientific validity, uncertainty quantification, or acceptance.
    """

    input_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Validate exact nonempty reduction-challenge payload representations.

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
