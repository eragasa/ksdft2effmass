"""Software verification of the direct Mathieu1D script lifecycle."""

from __future__ import annotations

import ast
import hashlib
import os
import shutil
import subprocess
import sys
from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path

import pytest
from projectkoios.physkit.units import ScalarQuantity, Unitless, VectorQuantity

from ksdft2effmass.model_systems.mathieu1d.configuration import (
    Mathieu1dConfiguration,
)
from ksdft2effmass.model_systems.mathieu1d.result import (
    Mathieu1dCalculationResult,
)
from ksdft2effmass.model_systems.mathieu1d.verification_values import (
    Mathieu1dVerification,
)
from ksdft2effmass.serialization import SerializableValue, TypedJsonValueCodec

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestMathieu1dDirectScripts:
    """Verify direct module-scope calculation, verification, and rendering."""

    def test_source__direct_scripts__remain_explicit_module_scope_adapters(
        self,
    ) -> None:
        """The three direct scripts contain no workflow-shaped execution API."""
        calculation = self._repository_root() / "calculations" / "mathieu1d"
        for name in self._script_names():
            source = (calculation / name).read_text(encoding="utf-8")
            tree = ast.parse(source)
            assert not any(
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                for node in ast.walk(tree)
            )
            assert "Workflow" not in source
            assert "main()" not in source
            assert "argparse" not in source
            assert "import json" not in source
            assert ".tolist(" not in source

    def test_modules__fresh_execution__publishes_authenticated_inventory(
        self,
        tmp_path: Path,
    ) -> None:
        """A fresh copied lifecycle publishes both verified native figures."""
        calculation = self._copy_calculation(tmp_path)
        environment = self._environment()
        for name in self._script_names():
            completed = self._run(calculation / name, environment)
            assert completed.returncode == 0, completed.stderr

        execution = calculation / "executions" / "direct-finite-reduction-n64"
        codec = TypedJsonValueCodec()
        execution_document = self._mapping(
            codec.deserialize_bytes((execution / "execution.json").read_bytes())
        )
        configuration_path = execution / "inputs" / "configuration.json"
        configuration_bytes = configuration_path.read_bytes()
        result_path = execution / "results" / "result.json"
        result_bytes = result_path.read_bytes()
        result_sha256 = hashlib.sha256(result_bytes).hexdigest()
        assert execution_document["configuration_schema"] == (
            "ksdft2effmass.mathieu1d-configuration.direct.v1"
        )
        assert (
            execution_document["configuration_sha256"]
            == hashlib.sha256(configuration_bytes).hexdigest()
        )
        assert execution_document["result_sha256"] == result_sha256
        configuration = Mathieu1dConfiguration.from_json(configuration_bytes)
        result = Mathieu1dCalculationResult.from_json(result_bytes)
        assert result.configuration.to_json() == configuration.to_json()
        assert result.calculation_family == execution_document["calculation_family"]
        assert result.execution_id == execution_document["execution_id"]
        assert result.evidence_status == execution_document["evidence_status"]
        assert result.claim_boundary == execution_document["claim_boundary"]
        verification_document = self._mapping(
            codec.deserialize_bytes(
                (execution / "verification" / "verification.json").read_bytes()
            )
        )
        verification_value = verification_document["verification"]
        assert isinstance(verification_value, Mapping)
        verification = Mathieu1dVerification.from_dict(verification_value)
        assert verification.passed
        assert verification.subject_sha256 == result_sha256
        assert len(verification.checks) == 873

        rendering = self._mapping(
            codec.deserialize_bytes(
                (execution / "figures" / "rendering.json").read_bytes()
            )
        )
        figures = rendering["figures"]
        report = rendering["technical_report"]
        assert isinstance(figures, Mapping)
        assert isinstance(report, Mapping)
        expected_figures = {
            "mathieu1d-finite-reduction.png",
            "mathieu1d-publication-summary.png",
        }
        assert set(figures) == expected_figures
        assert expected_figures < set(report)
        assert {"README.md", "technical-report.tex", "technical-report.pdf"} < set(
            report
        )
        for name in expected_figures:
            figure = execution / "figures" / name
            figure_record = figures[name]
            assert isinstance(figure_record, Mapping)
            assert (
                figure_record["sha256"]
                == hashlib.sha256(figure.read_bytes()).hexdigest()
            )
            assert figure.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
        assert not tuple(execution.glob(".*.incomplete"))

        for name in self._script_names():
            repeated = self._run(calculation / name, environment)
            assert repeated.returncode != 0

    def test_verification__mismatched_configuration__is_rejected(
        self,
        tmp_path: Path,
    ) -> None:
        """Verification rejects separately valid but inconsistent input bytes."""
        calculation = self._copy_calculation(tmp_path)
        environment = self._environment()
        calculated = self._run(calculation / "run_01_calculation.py", environment)
        assert calculated.returncode == 0, calculated.stderr

        execution = calculation / "executions" / "direct-finite-reduction-n64"
        configuration_path = execution / "inputs" / "configuration.json"
        configuration = Mathieu1dConfiguration.from_json(
            configuration_path.read_bytes()
        )
        altered_bytes = replace(
            configuration,
            imaginary_absolute_tolerance=2.0e-12,
        ).to_json()
        configuration_path.write_bytes(altered_bytes)
        codec = TypedJsonValueCodec()
        execution_path = execution / "execution.json"
        execution_document = dict(
            self._mapping(codec.deserialize_bytes(execution_path.read_bytes()))
        )
        execution_document["configuration_sha256"] = hashlib.sha256(
            altered_bytes
        ).hexdigest()
        execution_path.write_bytes(codec.serialize_bytes(execution_document))

        verified = self._run(calculation / "run_02_verification.py", environment)
        assert verified.returncode != 0
        assert "configuration and result configuration do not match" in verified.stderr
        assert not (execution / "verification").exists()
        assert not (execution / ".verification.incomplete").exists()

    def test_verification__modified_typed_result__publishes_no_figures(
        self,
        tmp_path: Path,
    ) -> None:
        """Independent verification failure prevents the rendering stage."""
        calculation = self._copy_calculation(tmp_path)
        environment = self._environment()
        calculated = self._run(calculation / "run_01_calculation.py", environment)
        assert calculated.returncode == 0, calculated.stderr

        execution = calculation / "executions" / "direct-finite-reduction-n64"
        result_path = execution / "results" / "result.json"
        result = Mathieu1dCalculationResult.from_json(result_path.read_bytes())
        first = result.ranges[0]
        altered = replace(
            result,
            ranges=(
                replace(
                    first,
                    bandwidth=ScalarQuantity(
                        first.bandwidth.magnitude + 1.0e-5,
                        Unitless(),
                    ),
                ),
                *result.ranges[1:],
            ),
        )
        altered_bytes = altered.to_json()
        result_path.write_bytes(altered_bytes)
        codec = TypedJsonValueCodec()
        execution_path = execution / "execution.json"
        execution_document = dict(
            self._mapping(codec.deserialize_bytes(execution_path.read_bytes()))
        )
        execution_document["result_sha256"] = hashlib.sha256(altered_bytes).hexdigest()
        execution_path.write_bytes(codec.serialize_bytes(execution_document))

        verified = self._run(calculation / "run_02_verification.py", environment)
        assert verified.returncode != 0
        assert "result.ranges[0].bandwidth" in verified.stderr
        assert (execution / "verification" / "verification.json").is_file()
        assert not (execution / "figures").exists()
        assert not (execution / "technical_report").exists()

    def test_rendering__modified_verification_or_projection__is_rejected(
        self,
        tmp_path: Path,
    ) -> None:
        """Rendering reconciles exact verification and projection records."""
        calculation = self._copy_calculation(tmp_path)
        environment = self._environment()
        for name in self._script_names()[:2]:
            completed = self._run(calculation / name, environment)
            assert completed.returncode == 0, completed.stderr

        execution = calculation / "executions" / "direct-finite-reduction-n64"
        verification_path = execution / "verification" / "verification.json"
        original_bytes = verification_path.read_bytes()
        codec = TypedJsonValueCodec()
        document = dict(self._mapping(codec.deserialize_bytes(original_bytes)))
        verification_value = document["verification"]
        assert isinstance(verification_value, Mapping)
        verification = dict(verification_value)
        components_value = verification["components"]
        assert isinstance(components_value, Mapping)
        components = dict(components_value)
        independent_value = components["independent_reconstruction"]
        assert isinstance(independent_value, Mapping)
        independent = dict(independent_value)
        observations_value = independent["observations"]
        assert isinstance(observations_value, Mapping)
        observations = dict(observations_value)
        del observations[next(iter(observations))]
        independent["observations"] = observations
        components["independent_reconstruction"] = independent
        verification["components"] = components
        document["verification"] = verification
        verification_path.write_bytes(codec.serialize_bytes(document))

        rendered = self._run(calculation / "run_03_render.py", environment)
        assert rendered.returncode != 0
        assert "stored verification differs" in rendered.stderr
        assert not (execution / "figures").exists()
        assert not (execution / "technical_report").exists()

        document = dict(self._mapping(codec.deserialize_bytes(original_bytes)))
        projection_value = document["visualization_data"]
        assert isinstance(projection_value, Mapping)
        projection = dict(projection_value)
        errors = projection["plane_wave_maximum_errors"]
        assert isinstance(errors, VectorQuantity)
        projection["plane_wave_maximum_errors"] = VectorQuantity(
            errors.magnitude + 1.0e-6,
            errors.unit,
        )
        document["visualization_data"] = projection
        verification_path.write_bytes(codec.serialize_bytes(document))

        rendered = self._run(calculation / "run_03_render.py", environment)
        assert rendered.returncode != 0
        assert "visualization projection differs" in rendered.stderr or (
            "digest" in rendered.stderr
        )
        assert not (execution / "figures").exists()
        assert not (execution / "technical_report").exists()

    def test_modules__incomplete_stage_paths__prevent_publication(
        self,
        tmp_path: Path,
    ) -> None:
        """Every incomplete-stage path blocks its corresponding final stage."""
        environment = self._environment()

        calculation = self._copy_calculation(tmp_path / "calculation")
        incomplete_execution = (
            calculation / "executions" / ".direct-finite-reduction-n64.incomplete"
        )
        incomplete_execution.mkdir()
        blocked = self._run(calculation / "run_01_calculation.py", environment)
        assert blocked.returncode != 0
        assert not (calculation / "executions" / "direct-finite-reduction-n64").exists()

        calculation = self._copy_calculation(tmp_path / "verification")
        completed = self._run(calculation / "run_01_calculation.py", environment)
        assert completed.returncode == 0, completed.stderr
        execution = calculation / "executions" / "direct-finite-reduction-n64"
        incomplete_verification = execution / ".verification.incomplete"
        incomplete_verification.mkdir()
        blocked = self._run(calculation / "run_02_verification.py", environment)
        assert blocked.returncode != 0
        assert not (execution / "verification").exists()

        calculation = self._copy_calculation(tmp_path / "rendering")
        for name in self._script_names()[:2]:
            completed = self._run(calculation / name, environment)
            assert completed.returncode == 0, completed.stderr
        execution = calculation / "executions" / "direct-finite-reduction-n64"
        incomplete_figures = execution / ".figures.incomplete"
        incomplete_figures.mkdir()
        blocked = self._run(calculation / "run_03_render.py", environment)
        assert blocked.returncode != 0
        assert not (execution / "figures").exists()
        incomplete_figures.rmdir()
        incomplete_report = execution / ".technical_report.incomplete"
        incomplete_report.mkdir()
        blocked = self._run(calculation / "run_03_render.py", environment)
        assert blocked.returncode != 0
        assert not (execution / "technical_report").exists()

    def test_retained_execution__publication_manifests_bind_authenticated_outputs(
        self,
    ) -> None:
        """Publication manifests bind only retained unsealed direct artifacts."""
        repository = self._repository_root()
        execution = (
            repository
            / "calculations"
            / "mathieu1d"
            / "executions"
            / "direct-finite-reduction-n64"
        )
        assert (execution / "UNSEALED.md").is_file()
        calculation = repository / "calculations" / "mathieu1d"
        assert not (calculation / "runs").exists()
        assert not (calculation / "input.json").exists()
        assert not (calculation / "schemas").exists()
        assert not (calculation / ".gitattributes").exists()
        codec = TypedJsonValueCodec()
        manifest_paths = (
            repository
            / "docs"
            / "publications"
            / "papers"
            / "Ragasa2026a"
            / "v1"
            / "experiment-references.json",
            repository
            / "docs"
            / "publications"
            / "papers"
            / "Ragasa2026a"
            / "v3"
            / "experiment-references.json",
            repository
            / "docs"
            / "publications"
            / "research-monograph"
            / "experiment-references.json",
        )
        for manifest_path in manifest_paths:
            manifest_bytes = manifest_path.read_bytes()
            manifest = self._mapping(codec.deserialize_bytes(manifest_bytes))
            assert codec.serialize_bytes(manifest) == manifest_bytes
            assert manifest["calculation_family"] == "mathieu1d-finite-reduction"
            assert manifest["execution_id"] == "direct-finite-reduction-n64"
            assert manifest["evidence_status"] == "illustrative numerical experiment"
            assert manifest["sealed"] is False
            assert "predecessor_provenance" not in manifest
            artifacts_value = manifest["artifacts"]
            assert isinstance(artifacts_value, Mapping)
            for artifact_value in artifacts_value.values():
                assert isinstance(artifact_value, Mapping)
                artifact_path_value = artifact_value["path"]
                artifact_sha256 = artifact_value["sha256"]
                assert type(artifact_path_value) is str
                assert type(artifact_sha256) is str
                assert "/runs/" not in artifact_path_value
                artifact_path = repository / artifact_path_value
                assert artifact_path.is_file()
                assert hashlib.sha256(artifact_path.read_bytes()).hexdigest() == (
                    artifact_sha256
                )

        report = repository / "calculations" / "mathieu1d" / "technical-report"
        for name in (
            "mathieu1d-finite-reduction.png",
            "mathieu1d-publication-summary.png",
            "technical-report.pdf",
        ):
            assert (report / name).read_bytes() == (
                execution / "technical_report" / name
            ).read_bytes()

    @classmethod
    def _copy_calculation(cls, tmp_path: Path) -> Path:
        source = cls._repository_root() / "calculations" / "mathieu1d"
        calculation = tmp_path / "calculations" / "mathieu1d"
        (calculation / "executions").mkdir(parents=True)
        for name in cls._script_names():
            shutil.copy2(source / name, calculation / name)
        shutil.copytree(source / "technical-report", calculation / "technical-report")
        return calculation

    @staticmethod
    def _environment() -> dict[str, str]:
        environment = dict(os.environ)
        environment["MPLBACKEND"] = "Agg"
        return environment

    @staticmethod
    def _run(
        path: Path, environment: Mapping[str, str]
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(path)],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )

    @staticmethod
    def _mapping(value: SerializableValue) -> Mapping[str, SerializableValue]:
        if not isinstance(value, Mapping):
            raise TypeError("decoded document must be a mapping")
        return value

    @staticmethod
    def _repository_root() -> Path:
        return Path(__file__).resolve().parents[5]

    @staticmethod
    def _script_names() -> tuple[str, ...]:
        return (
            "run_01_calculation.py",
            "run_02_verification.py",
            "run_03_render.py",
        )
