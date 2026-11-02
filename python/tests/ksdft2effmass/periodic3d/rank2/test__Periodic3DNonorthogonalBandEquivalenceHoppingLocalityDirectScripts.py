"""Context-first ownership for periodic-3D FCC/diamond calculation actions."""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic3DFCCDiamondCalculationMigration:
    """Retire the obsolete nonorthogonal lifecycle and retain donor provenance."""

    def test_context_first_owner_replaces_obsolete_direct_lifecycle(
        self,
        repository_root: Path,
    ) -> None:
        calculations = repository_root / "calculations"
        legacy = (
            calculations
            / "periodic3d"
            / "rank2"
            / "nonorthogonal"
            / "band-equivalence-locality"
        )
        aggregate = (
            calculations
            / "periodic3d_rank2_fcc_diamond"
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

    def test_migration_record_preserves_donor_and_nonmaterial_boundary(
        self,
        repository_root: Path,
    ) -> None:
        aggregate = (
            repository_root
            / "calculations"
            / "periodic3d_rank2_fcc_diamond"
            / "band_equivalence_hopping_locality"
        )
        owner = " ".join((aggregate / "README.md").read_text(encoding="utf-8").split())
        migration = (aggregate / "migration.md").read_text(encoding="utf-8")
        pointer = (
            repository_root
            / "experiments"
            / "model-adequacy"
            / "periodic3d_nonorthog"
            / "band-equivalence-versus-hopping-locality"
            / "README.md"
        ).read_text(encoding="utf-8")

        assert "run_nominal_calculation.py" in owner
        assert "calculates and independently verifies" in owner
        assert "No execution directory is retained" in owner
        assert "not a bulk-silicon calculation" in owner
        assert (
            "calculations/periodic3d/rank2/nonorthogonal/band-equivalence-locality/"
        ) in migration
        assert "The donor calculation path is retired" in migration
        assert "periodic3d_rank2_fcc_diamond" in pointer
        assert "legacy identity-preserving forward pointer" in pointer
