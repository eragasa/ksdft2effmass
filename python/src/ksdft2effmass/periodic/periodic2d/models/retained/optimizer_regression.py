"""Immutable retained censored optimizer-regression documents."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerRegressionCampaignModel:
    """Store exact standalone result, analyzer, and regression bytes."""

    standalone_result_payload: bytes
    analyzer_payload: bytes
    regression_payload: bytes

    def __post_init__(self) -> None:
        if (
            not self.standalone_result_payload
            or not self.analyzer_payload
            or not self.regression_payload
        ):
            raise ValueError("retained payloads must be nonempty")
