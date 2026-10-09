"""Exact encoded documents for retained censored optimizer regression."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerRegressionEncodedDocuments:
    """Own exact standalone-result, analyzer, and regression-result bytes.

    Parameters
    ----------
    standalone_result_payload
        Exact nonempty retained standalone-result bytes.
    analyzer_payload
        Exact nonempty retained analyzer-source bytes.
    regression_payload
        Exact nonempty retained convergence-regression bytes.

    Raises
    ------
    TypeError
        If a payload is not exact built-in :class:`bytes`.
    ValueError
        If a payload is empty.

    Notes
    -----
    This DataObject owns encoded content only. It assigns no provenance, statistical
    validity, optimizer convergence, causal interpretation, physical uncertainty,
    scientific validation, or acceptance.
    """

    standalone_result_payload: bytes
    analyzer_payload: bytes
    regression_payload: bytes

    def __post_init__(self) -> None:
        """Delegate exact nonempty byte checks."""
        self._check_args_payloads()

    def _check_args_payloads(self) -> None:
        """Require exact nonempty built-in bytes for every encoded document."""
        for name, payload in (
            ("standalone_result_payload", self.standalone_result_payload),
            ("analyzer_payload", self.analyzer_payload),
            ("regression_payload", self.regression_payload),
        ):
            if type(payload) is not bytes:
                raise TypeError(f"{name} must be exact bytes")
            if not payload:
                raise ValueError(f"{name} must be nonempty")
