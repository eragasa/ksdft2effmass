"""Static contract tests for direct composite-alignment effect adapters."""

import ast
import runpy
import shutil
import subprocess
from pathlib import Path

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic1DCompositeBandAlignmentDirectScripts:
    """Establish the closed direct calculate, verify, and render adapter set."""

    @staticmethod
    def scripts() -> tuple[Path, ...]:
        repository = Path(__file__).resolve().parents[5]
        calculation = (
            repository
            / "calculations"
            / "periodic1d"
            / "rank2"
            / "composite-band-alignment-locality"
        )
        return (
            calculation / "run_01_calculation.py",
            calculation / "run_02_verification.py",
            calculation / "run_03_render.py",
        )

    def test__scripts__are_direct_effect_adapters(self) -> None:
        scripts = self.scripts()

        assert all(path.is_file() for path in scripts)
        assert all(path.stat().st_mode & 0o111 for path in scripts)
        for path in scripts:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            imported_modules = {
                alias.name
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            }
            imported_from = {
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module is not None
            }
            functions = {
                node.name
                for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef)
            }
            assert "argparse" not in imported_modules | imported_from
            assert "json" not in imported_modules | imported_from
            assert "main" not in functions
            assert "Workflow" not in source
            assert "workflow/" not in source
            compile(source, str(path), "exec")

    def test__scripts__declare_the_same_closed_execution(self) -> None:
        sources = [path.read_text(encoding="utf-8") for path in self.scripts()]

        assert all(
            'EXECUTION_ID = "direct-controlled-rank2-n64"' in source
            for source in sources
        )
        assert all(
            "periodic1d-rank2-composite-band-alignment-locality" in source
            for source in sources
        )
        assert all(
            "ksdft2effmass.periodic1d.controlled-four-state-parent.v1" in source
            for source in sources
        )

    def test__scripts__execute_closed_lifecycle_in_temporary_repository(
        self, tmp_path: Path
    ) -> None:
        repository = tmp_path / "repository"
        calculation = (
            repository
            / "calculations"
            / "periodic1d"
            / "rank2"
            / "composite-band-alignment-locality"
        )
        calculation.mkdir(parents=True)
        copied_scripts = tuple(calculation / path.name for path in self.scripts())
        for source, destination in zip(self.scripts(), copied_scripts, strict=True):
            shutil.copy2(source, destination)
        (repository / "README.md").write_text("temporary test repository\n")
        subprocess.run(["git", "init", "--quiet"], cwd=repository, check=True)
        subprocess.run(["git", "add", "README.md"], cwd=repository, check=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Test",
                "-c",
                "user.email=test@example.invalid",
                "commit",
                "--quiet",
                "-m",
                "temporary lifecycle root",
            ],
            cwd=repository,
            check=True,
        )

        for script in copied_scripts:
            runpy.run_path(str(script))

        execution = calculation / "executions" / "direct-controlled-rank2-n64"
        assert (execution / "execution.json").is_file()
        assert (execution / "results" / "result.json").is_file()
        assert (execution / "verification" / "verification.json").is_file()
        assert (execution / "figures" / "rendering.json").is_file()
        assert {path.name for path in (execution / "figures").glob("*.png")} == {
            "rank2-composite-alignment.png",
            "rank2-composite-locality.png",
            "rank2-composite-error-channels.png",
        }

        for script in copied_scripts:
            with pytest.raises(FileExistsError):
                runpy.run_path(str(script))
