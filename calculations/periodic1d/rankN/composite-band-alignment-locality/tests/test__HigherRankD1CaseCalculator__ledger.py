"""Software verification for the schema-free higher-rank D1 calculator ledger."""

from __future__ import annotations

import pytest
from workflow import (
    HigherRankD1CalculationResult,
    HigherRankD1CaseCalculator,
    HigherRankD1CaseDefinition,
    HigherRankD1ChannelMeshDiagnostics,
    HigherRankD1ScalarLedger,
)

pytestmark = pytest.mark.software_verification


class TestHigherRankD1CaseCalculator:
    """Establish complete qualified-case and sampled-Pareto coverage."""

    def test_execute__retains_all_meshes_channels_supports_and_pareto(
        self,
    ) -> None:
        """One bounded case covers all qualified schema-free ledger dimensions."""
        result = HigherRankD1CaseCalculator().execute(HigherRankD1CaseDefinition(3, 1))

        assert result.qualification == "qualified"
        partial = HigherRankD1CalculationResult.aggregate((result,))
        assert partial.overall_qualification == "incomplete-coverage"
        assert result.failed_gate_paths == ()
        assert tuple(mesh.mesh_size for mesh in result.meshes) == (513, 1025, 2049)
        assert len(result.refinement) > 1000
        for mesh in result.meshes:
            assert tuple(channel.channel for channel in mesh.channels) == (
                "A0",
                "A1",
                "A2",
                "A3",
            )
            for channel in mesh.channels:
                assert isinstance(channel, HigherRankD1ChannelMeshDiagnostics)
                assert type(channel.scalar_ledger) is HigherRankD1ScalarLedger
                assert channel.scalar_ledger.paths
                assert tuple(item.support for item in channel.supports) == (
                    0,
                    1,
                    2,
                    4,
                    8,
                    16,
                    32,
                    64,
                    128,
                )
        final_channels = tuple(
            channel
            for channel in result.meshes[-1].channels
            if isinstance(channel, HigherRankD1ChannelMeshDiagnostics)
        )
        assert len(final_channels) == 4
        for channel in final_channels:
            assert len(channel.pareto_points) == 9
            assert any(point.pareto_efficient for point in channel.pareto_points)
        assert final_channels[0].supports[2].tail.normalized_l2_norm >= 1.0e-6
        assert final_channels[3].supports[2].tail.normalized_l2_norm <= 1.0e-10
