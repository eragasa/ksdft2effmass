"""Periodic-2D rank-two retained lifecycle ownership contracts."""

from __future__ import annotations

from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.lifecycle import (
    Periodic2DRank2BandEquivalenceHoppingLocalityExecution,
    Periodic2DRank2BandEquivalenceHoppingLocalityExecutionVerification,
    Periodic2DRank2BandEquivalenceHoppingLocalityRendering,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.visualizations.data import (  # noqa: E501
    Periodic2DRank2BandEquivalenceHoppingLocalityVisualizationData,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.lifecycle import (
    Periodic3DRank2BandEquivalenceHoppingLocalityExecution,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic2DRank2LifecycleRecords:
    """Readmit historical bytes without changing their evidence status or encoding."""

    @staticmethod
    def _execution_root(repository_root: Path) -> Path:
        return (
            repository_root
            / "calculations"
            / "periodic2d"
            / "rank2"
            / "orthogonal"
            / "band-equivalence-locality"
            / "executions"
            / "direct-square-rank2-n16"
        )

    def test_retained_unsealed_records_round_trip_through_rank_first_owners(
        self, repository_root: Path
    ) -> None:
        root = self._execution_root(repository_root)
        execution_bytes = (root / "execution.json").read_bytes()
        verification_bytes = (root / "verification" / "verification.json").read_bytes()
        rendering_bytes = (root / "figures" / "rendering.json").read_bytes()

        execution = Periodic2DRank2BandEquivalenceHoppingLocalityExecution.from_json(
            execution_bytes
        )
        verification = Periodic2DRank2BandEquivalenceHoppingLocalityExecutionVerification.from_json(  # noqa: E501
            verification_bytes
        )
        rendering = Periodic2DRank2BandEquivalenceHoppingLocalityRendering.from_json(
            rendering_bytes
        )

        assert type(execution) is Periodic2DRank2BandEquivalenceHoppingLocalityExecution
        assert (
            type(verification)
            is Periodic2DRank2BandEquivalenceHoppingLocalityExecutionVerification
        )
        assert type(rendering) is Periodic2DRank2BandEquivalenceHoppingLocalityRendering
        assert (
            type(verification.visualization_data)
            is Periodic2DRank2BandEquivalenceHoppingLocalityVisualizationData
        )
        assert not execution.sealed
        assert execution.to_json() == execution_bytes
        assert verification.to_json() == verification_bytes
        assert rendering.to_json() == rendering_bytes
        with pytest.raises(ValueError, match="periodic-3D"):
            Periodic3DRank2BandEquivalenceHoppingLocalityExecution.from_json(
                execution_bytes
            )

    def test_current_scripts_and_historical_producers_keep_distinct_owners(
        self, repository_root: Path
    ) -> None:
        execution_root = self._execution_root(repository_root)
        calculation_root = execution_root.parents[1]
        for name in (
            "run_01_calculation.py",
            "run_02_verification.py",
            "run_03_render.py",
        ):
            current = (calculation_root / name).read_text(encoding="utf-8")
            historical = (execution_root / "producers" / name).read_text(
                encoding="utf-8"
            )
            assert (
                "periodic2d.rank2.band_equivalence_hopping_locality.lifecycle"
                in current
            )
            for forbidden_owner in (
                "analysis.model_adequacy.band_equivalence_locality.lifecycle",
                "analysis.model_adequacy.band_equivalence_hopping_locality.lifecycle",
                "ksdft2effmass.band_equivalence_hopping_locality.lifecycle",
            ):
                assert forbidden_owner not in current
            assert (
                "analysis.model_adequacy.band_equivalence_locality.lifecycle"
                in historical
            )
