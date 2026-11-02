"""Context-first ownership for periodic-2D hexagonal-metric calculation actions."""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic2DHexagonalMetricCalculationMigration:
    """Retire obsolete direct-lifecycle paths without losing migration boundaries."""

    def test_context_first_owner_replaces_obsolete_direct_lifecycle(
        self,
        repository_root: Path,
    ) -> None:
        calculations = repository_root / "calculations"
        legacy = (
            calculations
            / "periodic2d"
            / "rank2"
            / "nonorthogonal"
            / "band-equivalence-locality"
        )
        aggregate = (
            calculations
            / "periodic2d_rank2_hexagonal"
            / "band_equivalence_hopping_locality"
        )

        assert not legacy.exists()
        assert aggregate.is_dir()
        assert {
            path.name for path in aggregate.glob("*.py") if path.name.startswith("run_")
        } == {
            "run_nominal_calculation.py",
            "run_refinement_01.py",
            "run_refinement_02.py",
        }
        assert (aggregate / "render_nominal_analysis.py").is_file()
        assert not (aggregate / "executions").exists()
        for obsolete in (
            "run_01_calculation.py",
            "run_02_verification.py",
            "run_03_render.py",
        ):
            assert not (aggregate / obsolete).exists()

    def test_owner_and_forward_pointer_preserve_scientific_boundary(
        self,
        repository_root: Path,
    ) -> None:
        aggregate = (
            repository_root
            / "calculations"
            / "periodic2d_rank2_hexagonal"
            / "band_equivalence_hopping_locality"
        )
        owner = (aggregate / "README.md").read_text(encoding="utf-8")
        migration = (aggregate / "migration.md").read_text(encoding="utf-8")
        pointer = (
            repository_root
            / "experiments"
            / "model-adequacy"
            / "periodic2d_nonorthog"
            / "band-equivalence-versus-hopping-locality"
            / "README.md"
        ).read_text(encoding="utf-8")

        assert "run_nominal_calculation.py" in owner
        assert "calculates and independently verifies" in owner
        assert "No execution directory is retained" in owner
        assert "not a graphene material calculation" in owner
        assert "Retire duplicate scripts" in migration
        assert "calculation-writer runtime regression" in migration
        assert "Legacy forward pointer" in pointer
        assert "periodic2d_rank2_hexagonal" in pointer
        assert (
            "not the current\nprotocol, calculation, result, or report authority"
            in pointer
        )
