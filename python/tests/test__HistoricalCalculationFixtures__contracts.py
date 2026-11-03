"""Integrity checks for exact historical campaign JSON test fixtures."""

import hashlib
import json
from pathlib import Path

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestHistoricalCalculationFixtures:
    """Own the byte-identity boundary for removed-layout campaign fixtures."""

    @staticmethod
    def repository_root() -> Path:
        """Return the repository root containing the test resources."""
        return Path(__file__).resolve().parents[2]

    def test__HistoricalCalculationFixtures__artifact__manifest__binds_every_fixture_byte(  # noqa: E501
        self,
    ) -> None:
        """Every historical JSON fixture must match its declared digest and size."""
        root = self.repository_root()
        resource_root = root / "python/tests/resources/historical_calculations"
        manifest = json.loads((resource_root / "manifest.json").read_text())

        assert manifest["schema_version"] == 1
        artifacts = manifest["artifacts"]
        assert len(artifacts) == 32

        fixture_paths = tuple(item["fixture_path"] for item in artifacts)
        assert len(fixture_paths) == len(set(fixture_paths))
        expected_paths = {
            path.relative_to(root).as_posix()
            for path in resource_root.rglob("*")
            if path.is_file() and path.name not in {"README.md", "manifest.json"}
        }
        assert set(fixture_paths) == expected_paths

        for item in artifacts:
            fixture_path = root / item["fixture_path"]
            payload = fixture_path.read_bytes()
            assert len(payload) == item["size_bytes"]
            assert hashlib.sha256(payload).hexdigest() == item["sha256"]
            assert item["historical_path"].startswith(
                "calculations/research-monograph/periodic-"
            )
            assert item["source_revision"] == (
                "c5d34a93b4710a4a430738c404c775865d418d42"
            )
