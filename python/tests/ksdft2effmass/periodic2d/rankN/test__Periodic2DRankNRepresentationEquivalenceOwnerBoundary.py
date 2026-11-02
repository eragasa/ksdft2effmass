"""Periodic-2D rank-N ownership contracts for ``RepresentationEquivalence``."""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic2DRankNRepresentationEquivalenceOwnerBoundary:
    """Keep the prospective root explicit without overstating a lifecycle."""

    @staticmethod
    def _root(repository_root: Path) -> Path:
        return (
            repository_root
            / "calculations"
            / "periodic2d"
            / "rankN"
            / "composite-band-alignment-locality"
        )

    def test_declares_common_scientific_base_ownership(
        self, repository_root: Path
    ) -> None:
        readme = (self._root(repository_root) / "README.md").read_text(encoding="utf-8")

        for base_name in (
            "SubspaceReduction",
            "RepresentationEquivalence",
            "RealSpaceSupportTruncation",
            "NumericalConsistency",
        ):
            assert f"`{base_name}`" in readme

    def test_does_not_claim_unselected_direct_entrypoints(
        self, repository_root: Path
    ) -> None:
        root = self._root(repository_root)

        assert not (root / "run_01_calculation.py").exists()
        assert not (root / "run_02_verification.py").exists()
        assert not (root / "run_03_render.py").exists()
