"""Static contract tests for direct composite-alignment effect adapters."""

import ast
import runpy
import shutil
import subprocess
from collections.abc import Mapping
from pathlib import Path

import pytest
from projectkoios.physkit.units import PhysicalUnit

from ksdft2effmass.periodic1d.rank2.band_alignment.composite.result import (
    Periodic1DCompositeBandAlignmentCalculationResult,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic1DCompositeBandAlignmentDirectScripts:
    """Establish the closed direct calculate, verify, and render adapter set."""

    @staticmethod
    def scripts() -> tuple[Path, ...]:
        repository = Path(__file__).resolve().parents[7]
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

    @classmethod
    def copied_scripts(
        cls,
        tmp_path: Path,
    ) -> tuple[Path, Path, tuple[Path, ...]]:
        """Copy the closed adapters into one temporary repository."""
        repository = tmp_path / "repository"
        calculation = (
            repository
            / "calculations"
            / "periodic1d"
            / "rank2"
            / "composite-band-alignment-locality"
        )
        calculation.mkdir(parents=True)
        copied_scripts = tuple(calculation / path.name for path in cls.scripts())
        for source, destination in zip(cls.scripts(), copied_scripts, strict=True):
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
        return repository, calculation, copied_scripts

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
        calculation_source = sources[0]

        assert "Periodic1DAlignmentStudyFactory(" in calculation_source
        assert ").create()" in calculation_source
        assert "Periodic1DRank2AlignmentStudySpecification" in calculation_source
        assert "Periodic1DCompositeBandAlignmentAnalyzer" not in calculation_source
        assert all(
            'EXECUTION_ID = "direct-controlled-rank2-n64-v2"' in source
            for source in sources
        )
        assert all("RESULT_SCHEMA" in source for source in sources)
        assert all("CALCULATION_FAMILY" in source for source in sources)
        assert "Periodic1DCompositeBandAlignmentConfiguration.frozen()" in (
            calculation_source
        )
        assert all(
            "ksdft2effmass.periodic1d.controlled-four-state-parent.v1" not in source
            for source in sources
        )
        assert all(
            "Periodic1DCompositeBandAlignmentConfiguration" in source
            for source in sources
        )

    def test__technical_report__uses_publication_appropriate_capability_terms(
        self,
    ) -> None:
        report = (
            self.scripts()[0].parent / "technical-report" / "technical_report.tex"
        ).read_text(encoding="utf-8")

        assert "visualization projection" not in report
        assert "Authenticated" not in report
        assert "Finite-support error and complete hopping-block locality" in report
        assert "retained support" in report

    def test__scripts__execute_closed_lifecycle_in_temporary_repository(
        self, tmp_path: Path
    ) -> None:
        _, calculation, copied_scripts = self.copied_scripts(tmp_path)

        for script in copied_scripts:
            runpy.run_path(str(script))

        execution = calculation / "executions" / "direct-controlled-rank2-n64-v2"
        assert (execution / "execution.json").is_file()
        assert (execution / "results" / "result.json").is_file()
        assert (execution / "verification" / "verification.json").is_file()
        assert (execution / "figures" / "rendering.json").is_file()
        result_bytes = (execution / "results" / "result.json").read_bytes()
        result = Periodic1DCompositeBandAlignmentCalculationResult.from_json(
            result_bytes
        )
        assert result.to_json() == result_bytes
        assert result.result_schema == (
            "ksdft2effmass.periodic1d-rank2-composite-band-alignment-result.v2"
        )
        assert result.diagnostics.pointwise_procrustes.minimum_rank_margin > 0.0
        assert result.diagnostics.global_procrustes.minimum_rank_margin > 0.0
        codec = TypedJsonValueCodec()
        for document_path in (
            execution / "execution.json",
            execution / "verification" / "verification.json",
            execution / "figures" / "rendering.json",
        ):
            document = codec.deserialize_bytes(document_path.read_bytes())
            assert isinstance(document, Mapping)
            geometry = document["lattice_geometry"]
            assert isinstance(geometry, Mapping)
            assert geometry["lattice_period"] == 1.0
            assert geometry["lattice_unit"] == PhysicalUnit("bohr")
        assert {path.name for path in (execution / "figures").glob("*.png")} == {
            "rank2-composite-alignment.png",
            "rank2-composite-recovery-controls.png",
            "rank2-composite-hopping-diagnostics.png",
            "rank2-composite-locality.png",
            "rank2-composite-error-channels.png",
            "rank2-composite-error-trajectories.png",
        }

        for script in copied_scripts:
            with pytest.raises(FileExistsError):
                runpy.run_path(str(script))

    def test__scripts__reject_geometry_drift_between_lifecycle_stages(
        self,
        tmp_path: Path,
    ) -> None:
        _, calculation, scripts = self.copied_scripts(tmp_path)
        calculate, verify, render = scripts
        runpy.run_path(str(calculate))
        execution = calculation / "executions" / "direct-controlled-rank2-n64-v2"
        codec = TypedJsonValueCodec()

        execution_path = execution / "execution.json"
        execution_bytes = execution_path.read_bytes()
        execution_document = codec.deserialize_bytes(execution_bytes)
        assert isinstance(execution_document, Mapping)
        modified_execution = dict(execution_document)
        execution_geometry = execution_document["lattice_geometry"]
        assert isinstance(execution_geometry, Mapping)
        modified_execution["lattice_geometry"] = {
            **execution_geometry,
            "lattice_period": 2.0,
        }
        execution_path.write_bytes(codec.serialize_bytes(modified_execution))
        with pytest.raises(ValueError, match="lattice geometry"):
            runpy.run_path(str(verify))

        execution_path.write_bytes(execution_bytes)
        runpy.run_path(str(verify))
        verification_path = execution / "verification" / "verification.json"
        verification_document = codec.deserialize_bytes(verification_path.read_bytes())
        assert isinstance(verification_document, Mapping)
        modified_verification = dict(verification_document)
        verification_geometry = verification_document["lattice_geometry"]
        assert isinstance(verification_geometry, Mapping)
        modified_verification["lattice_geometry"] = {
            **verification_geometry,
            "lattice_period": 2.0,
        }
        verification_path.write_bytes(codec.serialize_bytes(modified_verification))
        with pytest.raises(ValueError, match="lattice geometry"):
            runpy.run_path(str(render))
