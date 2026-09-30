# ruff: noqa: E501
"""Software-verification evidence for strict route-reconciliation input decoding."""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.route_reconciliation.workflow import (
    RouteReconciliationCampaignInputDeserializer,
)

pytestmark = pytest.mark.unit
SUT = RouteReconciliationCampaignInputDeserializer


class TestRouteReconciliationCampaignInputDeserializer:
    """Own closed version-one input-decoding evidence."""

    @staticmethod
    def retained_input() -> bytes:
        """Return the exact retained route-reconciliation input document."""
        root = Path(__file__).resolve().parents[8]
        return (
            root
            / "calculations/research-monograph/impurity-defect-1d-independent-route/input.json"
        ).read_bytes()

    def test_method__execute__decodes_retained_contract(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-026.

        Requirement: The closed decoder must accept the retained version-one contract.

        Method: Decode the exact retained bytes.

        Oracle: Frozen experiment identity, seven unique controls, and route dimensions.

        Acceptance: Identity, control count, cell count, and common hopping ranges agree.

        Interpretation: A pass establishes software-contract decoding only.

        Limitations: Decoding does not authenticate sources or calculate route results.
        """
        result = SUT().execute(self.retained_input())

        assert result.experiment_id.endswith("independent-route-v1")
        assert len(result.control_ids) == 7
        assert result.route.cell_count == 16
        assert result.route.real_space_range == result.route.bloch_range == 4

    @pytest.mark.parametrize(
        ("payload", "message"),
        [
            (
                b'{"schema_version": 1, "schema_version": 1}',
                "duplicate JSON key",
            ),
            (b'{"schema_version": NaN}', "non-finite JSON constant"),
            (b'{"schema_version": 1, "unexpected": true}', "input fields"),
        ],
        ids=("duplicate-key", "nonfinite-constant", "unexpected-field"),
    )
    def test_method__execute__rejects_noncanonical_json(
        self, payload: bytes, message: str
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-027.

        Requirement: Duplicate keys, non-finite constants, and open root fields must be
        rejected independently of interpreter optimization.

        Method: Decode one malformed document per explicit semantic case.

        Oracle: The strict version-one wire contract.

        Acceptance: Each case raises ``ValueError`` with its contract category.

        Interpretation: A pass establishes fail-closed input parsing.

        Limitations: Nested field-shape checks are exercised by retained composition.
        """
        with pytest.raises(ValueError, match=message):
            SUT().execute(payload)
