"""Software verification for higher-rank D1 definition attributes."""

from __future__ import annotations

import pytest

from ksdft2effmass.campaigns.periodic_reduction.higher_rank_d1 import (
    HigherRankD1CaseDefinition,
    HigherRankD1Definition,
)

pytestmark = pytest.mark.software_verification


class TestHigherRankD1Definition:
    """Establish the frozen case and sampling inventories."""

    def test_attributes__freeze_rank_depth_and_sampling_inventories(self) -> None:
        """The definition rejects alternate scientific controls."""
        definition = HigherRankD1Definition()

        assert tuple(case.case_id for case in definition.cases) == (
            "r03-L01",
            "r03-L02",
            "r03-L04",
            "r03-L08",
            "r04-L01",
            "r04-L02",
            "r04-L04",
            "r04-L08",
            "r08-L01",
            "r08-L02",
            "r08-L04",
            "r08-L08",
            "r16-L01",
            "r16-L02",
            "r16-L04",
            "r16-L08",
        )
        assert definition.construction_mesh_sizes == (513, 1025, 2049)
        assert definition.evaluation_mesh_size == 8191
        assert definition.supports == (0, 1, 2, 4, 8, 16, 32, 64, 128)

    def test_case_attributes__reject_boolean_and_unsupported_rank(self) -> None:
        """Rank validation rejects Boolean and out-of-protocol values."""
        with pytest.raises(TypeError, match="rank"):
            HigherRankD1CaseDefinition(True, 1)
        with pytest.raises(ValueError, match="rank"):
            HigherRankD1CaseDefinition(2, 1)
