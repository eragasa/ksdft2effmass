"""Immutable encoded censored optimizer-regression documents."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerRegressionEncodedDocuments:
    """Store exact standalone result, analyzer, and regression bytes."""

    standalone_result_payload: bytes
    analyzer_payload: bytes
    regression_payload: bytes

    def __post_init__(self) -> None:
        """Require nonempty exact byte representations."""
        for name, payload in (
            ("standalone_result_payload", self.standalone_result_payload),
            ("analyzer_payload", self.analyzer_payload),
            ("regression_payload", self.regression_payload),
        ):
            if type(payload) is not bytes:
                raise TypeError(f"{name} must be exact bytes")
            if not payload:
                raise ValueError(f"{name} must be nonempty")
