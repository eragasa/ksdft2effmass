"""Immutable encoded standalone optimizer-study documents."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerStandaloneEncodedDocuments:
    """Store exact proposal, deterministic-start, and result wire bytes.

    Parameters
    ----------
    proposal_payload
        Exact retained standalone-study proposal bytes.
    initial_gauges_payload
        Exact retained deterministic initial-gauge design bytes.
    result_payload
        Exact retained standalone-result bytes.

    Raises
    ------
    TypeError
        If any payload is not exact built-in :class:`bytes`.
    ValueError
        If any payload is empty.

    Notes
    -----
    This DataObject owns wire representations only. It assigns no repository location,
    native-file presence, execution provenance, gauge validity, optimizer convergence,
    basin meaning, scientific validation, uncertainty, or acceptance.
    """

    proposal_payload: bytes
    initial_gauges_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Delegate exact representation and nonempty-wire validation."""
        self._check_args_payload_representations()
        self._check_args_payload_content()

    def _check_args_payload_representations(self) -> None:
        """Require exact built-in byte-wire representations."""
        for name, payload in self._named_payloads():
            if type(payload) is not bytes:
                raise TypeError(f"{name} must be exact bytes")

    def _check_args_payload_content(self) -> None:
        """Require every owned wire to contain at least one byte."""
        for name, payload in self._named_payloads():
            if not payload:
                raise ValueError(f"{name} must be nonempty")

    def _named_payloads(self) -> tuple[tuple[str, bytes], ...]:
        """Return field names paired with exact owned byte wires."""
        return (
            ("proposal_payload", self.proposal_payload),
            ("initial_gauges_payload", self.initial_gauges_payload),
            ("result_payload", self.result_payload),
        )
