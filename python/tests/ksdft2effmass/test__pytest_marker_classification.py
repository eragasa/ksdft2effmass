"""Software verification of explicit pytest marker classification."""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPytestMarkerClassification:
    """Keep cost, boundary, and evidence markers explicit in test modules."""

    @staticmethod
    def repository_root() -> Path:
        """Return the repository root that owns the test trees."""
        return Path(__file__).resolve().parents[3]

    def test_expensive_modules__also_declare_integration(self) -> None:
        """Every explicitly expensive module declares its crossed boundary."""
        root = self.repository_root()
        candidates = tuple((root / "python/tests").rglob("*.py")) + tuple(
            (root / "calculations").rglob("*.py")
        )
        missing = tuple(
            path.relative_to(root).as_posix()
            for path in candidates
            if "pytest.mark.expensive" in path.read_text(encoding="utf-8")
            and "pytest.mark.integration" not in path.read_text(encoding="utf-8")
        )
        assert missing == ()

    def test_reclassified_groups__own_markers_without_collection_hooks(self) -> None:
        """Previously blanket-marked groups classify each module directly."""
        root = self.repository_root()
        groups = (
            root / "python/tests/ksdft2effmass/model_systems/piab1d/study",
            root
            / "python/tests/numerical_verification/ksdft2effmass/campaigns/periodic_1d",
            root
            / "python/tests/software_verification/ksdft2effmass/campaigns/periodic_1d",
            root
            / "python/tests/software_verification/ksdft2effmass/research_monograph"
            / "impurity_defect_2d",
        )
        failures: list[str] = []
        for group in groups:
            if (group / "conftest.py").exists():
                failures.append((group / "conftest.py").relative_to(root).as_posix())
            for path in group.glob("test__*.py"):
                source = path.read_text(encoding="utf-8")
                if "pytestmark" not in source or not (
                    "pytest.mark.unit" in source or "pytest.mark.integration" in source
                ):
                    failures.append(path.relative_to(root).as_posix())
        assert tuple(sorted(failures)) == ()

    def test_integration_modules__also_declare_evidence_class(self) -> None:
        """Boundary classification never replaces the tested evidence claim."""
        root = self.repository_root()
        evidence_markers = (
            "pytest.mark.software_verification",
            "pytest.mark.numerical_verification",
            "pytest.mark.scientific_validation",
            "pytest.mark.uncertainty_quantification",
        )
        candidates = tuple((root / "python/tests").rglob("*.py")) + tuple(
            (root / "calculations").rglob("*.py")
        )
        missing = tuple(
            path.relative_to(root).as_posix()
            for path in candidates
            if "pytest.mark.integration" in path.read_text(encoding="utf-8")
            and not any(
                marker in path.read_text(encoding="utf-8")
                for marker in evidence_markers
            )
        )
        assert missing == ()
