"""Software verification for the research-results SQLite projection."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph.results_projection import (
    ResearchResultsProjectionRebuilder,
    ResearchResultsProjectionRequest,
)

pytestmark = [pytest.mark.software_verification, pytest.mark.integration]


class TestResearchResultsProjection:
    """Verify bounded projection, path, and atomic-rebuild behavior."""

    def _repository(self, root: Path) -> Path:
        calculation = root / "calculations" / "research-monograph" / "demo"
        calculation.mkdir(parents=True)
        (calculation / "README.md").write_text(
            "# Demonstration calculation\n\n"
            "## Status\n\n"
            "Calculated illustrative test fixture.\n",
            encoding="utf-8",
        )
        result_bytes = json.dumps(
            {
                "status": "calculated illustrative result",
                "energy": 1.25,
                "energy_unit": "eV",
                "samples": [0.0, 1.0, 2.0],
            },
            indent=2,
        ).encode()
        (calculation / "result.json").write_bytes(result_bytes)
        (calculation / "plot.png").write_bytes(b"synthetic image fixture")
        (calculation / "report.md").write_text("# Report\n", encoding="utf-8")
        result_sha256 = hashlib.sha256(result_bytes).hexdigest()
        (calculation / "SHA256SUMS").write_text(
            f"{result_sha256}  result.json\n{'0' * 64}  absent.json\n",
            encoding="utf-8",
        )
        return root

    def test_rebuild_projects_safe_results_and_manifest_observations(
        self, tmp_path: Path
    ) -> None:
        repository = self._repository(tmp_path / "repository")
        output = repository / "ui" / "analysis" / "build" / "results.sqlite"

        result = ResearchResultsProjectionRebuilder().execute(
            ResearchResultsProjectionRequest(
                repository_root=repository,
                output_path=output,
            )
        )

        assert result.output_path == output
        assert result.calculation_count == 1
        assert result.run_count == 1
        assert result.artifact_count == 5
        with sqlite3.connect(
            f"file:{output.as_posix()}?mode=ro&immutable=1", uri=True
        ) as connection:
            assert connection.execute("PRAGMA integrity_check").fetchone() == ("ok",)
            assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
            assert connection.execute("PRAGMA user_version").fetchone() == (1,)
            assert connection.execute(
                "SELECT calculation_id, root_path, title, artifact_count "
                "FROM calculations"
            ).fetchone() == (
                "demo",
                "calculations/research-monograph/demo",
                "Demonstration calculation",
                5,
            )
            assert connection.execute(
                "SELECT run_id, status_text, result_path FROM run_results"
            ).fetchone() == (
                "result:calculations/research-monograph/demo/result.json",
                "calculated illustrative result",
                "calculations/research-monograph/demo/result.json",
            )
            assert connection.execute(
                "SELECT path, media_type, artifact_kind FROM presentation_artifacts "
                "WHERE name = 'plot.png'"
            ).fetchone() == (
                "calculations/research-monograph/demo/plot.png",
                "image/png",
                "image",
            )
            assert connection.execute(
                "SELECT numeric_value, text_value, unit FROM scalar_observations "
                "WHERE name = 'energy'"
            ).fetchone() == (1.25, "1.25", "eV")
            assert connection.execute(
                "SELECT state, count(*) FROM manifest_observations "
                "GROUP BY state ORDER BY state"
            ).fetchall() == [("match", 1), ("missing", 1)]
            assert connection.execute(
                "SELECT count(*) FROM artifacts "
                "WHERE path LIKE '/%' OR path LIKE '../%' OR path LIKE '%/../%'"
            ).fetchone() == (0,)

    def test_rebuild_atomically_replaces_the_complete_projection(
        self, tmp_path: Path
    ) -> None:
        repository = self._repository(tmp_path / "repository")
        calculation = repository / "calculations" / "research-monograph" / "demo"
        output = repository / "ui" / "analysis" / "build" / "results.sqlite"
        rebuilder = ResearchResultsProjectionRebuilder()
        request = ResearchResultsProjectionRequest(
            repository_root=repository,
            output_path=output,
        )
        first_result = rebuilder.execute(request)
        original_identity = hashlib.sha256(output.read_bytes()).hexdigest()
        assert first_result.sha256 == original_identity
        (calculation / "notes.txt").write_text("new retained note\n", encoding="utf-8")

        replacement_result = rebuilder.execute(request)

        replacement_identity = hashlib.sha256(output.read_bytes()).hexdigest()
        assert replacement_result.sha256 == replacement_identity
        assert replacement_identity != original_identity
        with sqlite3.connect(
            f"file:{output.as_posix()}?mode=ro&immutable=1", uri=True
        ) as connection:
            assert connection.execute(
                "SELECT artifact_count FROM calculations WHERE calculation_id = 'demo'"
            ).fetchone() == (6,)
            assert connection.execute(
                "SELECT count(*) FROM artifacts WHERE name = 'notes.txt'"
            ).fetchone() == (1,)
        assert tuple(output.parent.glob(f".{output.name}.*.tmp")) == ()
