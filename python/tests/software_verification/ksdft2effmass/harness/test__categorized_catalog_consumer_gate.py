r"""Software verification of required categorized-catalog CLI inputs.

Evidence profile: routine

Bounded artifact scope: missing configured catalogs fail before publication.

Facet and represented meaning

All three configured directories are required. Consumers must not discover an
ambient flat catalog when the explicit categorized input is unavailable.

Intrinsic and cross-object scope

The artifact checks real command boundaries with maintained configuration fixtures
and framework-owned scratch; it does not call private consumer implementations.

VVUQ and scientific exclusions

Software verification only; no catalog cutover or scientific execution is exercised.
"""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.software_verification


class TestCategorizedCatalogConsumerGate:
    """Own fail-closed command behavior for missing configured input."""

    @pytest.mark.parametrize(
        "arguments",
        (
            pytest.param(("harness-projection", "sync"), id="projection_sync"),
            pytest.param(("harness-projection", "check"), id="projection_check"),
            pytest.param(("validate-harness",), id="repository_validation"),
        ),
    )
    def test_artifact__missing_catalogs__rejects_without_publication(
        self, tmp_path: Path, arguments: tuple[str, ...]
    ) -> None:
        """Evidence ID: software-verification.task-catalog.integration.missing-cli-input

        Requirement: Missing configured catalogs must not trigger flat-root fallback.

        Method: Invoke maintained commands on an isolated repository with exact
        configuration fixtures and a valid Task at the obsolete ambient location.

        Acceptance: Commands report the missing named root and create no control state.

        Limitations: This case checks absent inputs, not successful reconstruction.
        """
        fixture_root = Path(__file__).parent / "resources"
        repository = Path(__file__).resolve().parents[5]
        shutil.copytree(
            repository / "harness",
            tmp_path / "harness",
            ignore=shutil.ignore_patterns("state"),
        )
        shutil.copytree(repository / ".pi", tmp_path / ".pi")
        shutil.copytree(repository / ".agents", tmp_path / ".agents")
        shutil.copytree(repository / "python/tests", tmp_path / "python/tests")
        shutil.copyfile(
            repository / "python/pyproject.toml", tmp_path / "python/pyproject.toml"
        )
        (tmp_path / "harness/configuration.json").write_bytes(
            (fixture_root / "configuration-source-v2.json").read_bytes()
        )
        (tmp_path / ".pi/settings.json").write_bytes(b"{}")
        # A valid old-location record must not rescue missing configured roots.
        ambient = tmp_path / "harness/tasks"
        ambient.mkdir()
        shutil.copyfile(
            repository / "tasks/software/harness.task-status-details.json",
            ambient / "harness.task-status-details.json",
        )
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "ksdft2effmass.harness.cli",
                *arguments,
                "--repository-root",
                str(tmp_path),
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        assert result.returncode != 0
        assert "catalogs/questions" in result.stdout + result.stderr
        assert not (tmp_path / "harness/state").exists()
