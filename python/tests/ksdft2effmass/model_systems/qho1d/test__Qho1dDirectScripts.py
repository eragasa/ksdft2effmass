"""Software verification of the direct QHO1D calculation lifecycle."""

from __future__ import annotations

import ast
import hashlib
import os
import shutil
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

import pytest

from ksdft2effmass.model_systems.qho1d import Qho1dVerification
from ksdft2effmass.serialization import SerializableValue, TypedJsonValueCodec

pytestmark = pytest.mark.software_verification


class TestQho1dDirectScripts:
    """Verify fresh calculate, verify, and render composition."""

    def test_source__direct_scripts__remain_explicit_module_scope_adapters(
        self,
    ) -> None:
        """Direct adapters contain no workflow, main, parser, or custom JSON path."""
        repository_root = Path(__file__).resolve().parents[5]
        for path in sorted(
            (repository_root / "calculations" / "qho1d").glob("run_0*.py")
        ):
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
            assert not any(isinstance(node, ast.FunctionDef) for node in ast.walk(tree))
            assert "Workflow" not in source
            assert "argparse" not in source
            assert "import json" not in source
            assert ".tolist(" not in source

    def test_modules__fresh_execution__publish_authenticated_inventory(
        self,
        tmp_path: Path,
    ) -> None:
        """A fresh copied calculation runs without repository-local package paths."""
        repository_root = Path(__file__).resolve().parents[5]
        source_calculation = repository_root / "calculations" / "qho1d"
        calculation = tmp_path / "calculations" / "qho1d"
        (calculation / "executions").mkdir(parents=True)
        scripts = (
            "run_01_calculation.py",
            "run_02_verification.py",
            "run_03_render.py",
        )
        for name in scripts:
            shutil.copy2(source_calculation / name, calculation / name)
        shutil.copytree(
            source_calculation / "technical_report",
            calculation / "technical_report",
        )
        environment = dict(os.environ)
        environment["MPLBACKEND"] = "Agg"
        for name in scripts:
            completed = subprocess.run(
                [sys.executable, str(calculation / name)],
                check=False,
                capture_output=True,
                text=True,
                env=environment,
            )
            assert completed.returncode == 0, completed.stderr

        execution = calculation / "executions" / "direct-spatial-truncation-3x3x3"
        codec = TypedJsonValueCodec()
        execution_document = self._mapping(
            codec.deserialize_bytes((execution / "execution.json").read_bytes())
        )
        result_path = execution / "results" / "result.json"
        result_sha256 = hashlib.sha256(result_path.read_bytes()).hexdigest()
        assert execution_document["result_sha256"] == result_sha256
        verification_document = self._mapping(
            codec.deserialize_bytes(
                (execution / "verification" / "verification.json").read_bytes()
            )
        )
        verification_value = verification_document["verification"]
        assert isinstance(verification_value, Mapping)
        verification = Qho1dVerification.from_dict(verification_value)
        assert verification.passed
        assert len(verification.checks) == 468
        assert verification.subject_sha256 == result_sha256
        rendering = self._mapping(
            codec.deserialize_bytes(
                (execution / "figures" / "rendering.json").read_bytes()
            )
        )
        figures_value = rendering["figures"]
        report_value = rendering["technical_report"]
        assert isinstance(figures_value, Mapping)
        assert isinstance(report_value, Mapping)
        assert set(figures_value) == {
            "qho1d-eigenstates.png",
            "qho1d-eigenstate-distortion.png",
            "qho1d-diagnostics.png",
        }
        assert "technical_report.pdf" in report_value
        for filename, record_value in figures_value.items():
            assert isinstance(record_value, Mapping)
            path = execution / "figures" / filename
            assert (
                record_value["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
            )
        assert not tuple(execution.glob(".*.incomplete"))

    @staticmethod
    def _mapping(
        value: SerializableValue,
    ) -> Mapping[str, SerializableValue]:
        if not isinstance(value, Mapping):
            raise TypeError("decoded document must be a mapping")
        return value
