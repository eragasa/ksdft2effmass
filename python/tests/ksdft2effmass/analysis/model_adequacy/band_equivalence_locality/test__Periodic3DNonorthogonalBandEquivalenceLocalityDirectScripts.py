"""Direct-lifecycle contracts for nonorthogonal periodic-3D band locality."""

from __future__ import annotations

import ast
import hashlib
import math
import runpy
import shutil
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.definitions import (  # noqa: E501
    BandEquivalenceLocalityFamilyEnum,
    GaugeNormalizationEnum,
    ParentEnum,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.lifecycle import (  # noqa: E501
    BandEquivalenceLocalityExecution,
    BandEquivalenceLocalityExecutionVerification,
    BandEquivalenceLocalityRendering,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.result import (
    BandEquivalenceLocalityCalculationResult,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic3DNonorthogonalBandEquivalenceLocalityDirectScripts:
    """Establish the bounded FCC/diamond-basis direct lifecycle."""

    def test_scripts_execute_closed_typed_lifecycle(self, tmp_path: Path) -> None:
        repository = Path(__file__).resolve().parents[6]
        source_root = (
            repository
            / "calculations"
            / "periodic3d"
            / "rank2"
            / "nonorthogonal"
            / "band-equivalence-locality"
        )
        assert not (source_root / "executions").exists()
        calculation = (
            tmp_path
            / "calculations"
            / "periodic3d"
            / "rank2"
            / "nonorthogonal"
            / "band-equivalence-locality"
        )
        calculation.mkdir(parents=True)
        scripts = tuple(
            source_root / name
            for name in (
                "run_01_calculation.py",
                "run_02_verification.py",
                "run_03_render.py",
            )
        )
        copied = tuple(calculation / script.name for script in scripts)
        terminal_verbs = {
            "analyze",
            "assess",
            "evaluate",
            "execute",
            "result",
            "transform",
            "visualize",
            "write",
        }
        for source, destination in zip(scripts, copied, strict=True):
            shutil.copy2(source, destination)
            source_text = source.read_text(encoding="utf-8")
            tree = ast.parse(source_text, filename=str(source))
            assert not any(
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                for node in ast.walk(tree)
            )
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr in terminal_verbs
                    and isinstance(node.func.value, ast.Call)
                ):
                    assert node.func.value.args or node.func.value.keywords
            assert "Workflow" not in source_text
            assert "import json" not in source_text
            assert "TypedJsonValueCodec" not in source_text
            assert "serialize_bytes" not in source_text
            assert "deserialize_bytes" not in source_text
            assert "run_development" not in source_text

        runpy.run_path(str(copied[0]))

        execution_directory = calculation / "executions" / "direct-fcc-diamond-rank2-n8"
        execution_path = execution_directory / "execution.json"
        configuration_path = execution_directory / "inputs" / "configuration.json"
        result_path = execution_directory / "results" / "result.json"
        verification_path = execution_directory / "verification" / "verification.json"
        execution_bytes = execution_path.read_bytes()
        configuration_bytes = configuration_path.read_bytes()
        result_bytes = result_path.read_bytes()
        execution = BandEquivalenceLocalityExecution.from_json(execution_bytes)
        result = BandEquivalenceLocalityCalculationResult.from_json(result_bytes)

        calculation_script_bytes = copied[0].read_bytes()
        copied[0].write_bytes(calculation_script_bytes + b"\n")
        with pytest.raises(ValueError, match="calculation script bytes"):
            runpy.run_path(str(copied[1]))
        assert not (execution_directory / "verification").exists()
        assert not (execution_directory / ".verification.incomplete").exists()
        copied[0].write_bytes(calculation_script_bytes)

        first_case = result.diagnostics.cases[0]
        first_point = first_case.points[0]
        first_shell = first_point.shell_diagnostics[0]
        mutated_shell = replace(
            first_shell,
            reference_shell_power=first_shell.reference_shell_power + 0.125,
        )
        mutated_point = replace(
            first_point,
            shell_diagnostics=(
                mutated_shell,
                *first_point.shell_diagnostics[1:],
            ),
        )
        mutated_case = replace(
            first_case,
            points=(mutated_point, *first_case.points[1:]),
        )
        mutated_result = replace(
            result,
            diagnostics=replace(
                result.diagnostics,
                cases=(mutated_case, *result.diagnostics.cases[1:]),
            ),
        )
        mutated_bytes = mutated_result.to_json()
        result_path.write_bytes(mutated_bytes)
        execution_path.write_bytes(
            replace(
                execution,
                result_sha256=hashlib.sha256(mutated_bytes).hexdigest(),
            ).to_json()
        )
        with pytest.raises(ValueError, match="independent verification failed"):
            runpy.run_path(str(copied[1]))
        assert not (execution_directory / "verification").exists()
        assert not (execution_directory / ".verification.incomplete").exists()
        result_path.write_bytes(result_bytes)
        execution_path.write_bytes(execution_bytes)

        runpy.run_path(str(copied[1]))
        runpy.run_path(str(copied[2]))

        verification_bytes = verification_path.read_bytes()
        rendering_path = execution_directory / "figures" / "rendering.json"
        rendering_bytes = rendering_path.read_bytes()
        verification = BandEquivalenceLocalityExecutionVerification.from_json(
            verification_bytes
        )
        rendering = BandEquivalenceLocalityRendering.from_json(rendering_bytes)
        assert execution.to_json() == execution_bytes
        assert result.request.to_json() == configuration_bytes
        assert result.to_json() == result_bytes
        assert verification.to_json() == verification_bytes
        assert rendering.to_json() == rendering_bytes
        assert (
            result.request.family is BandEquivalenceLocalityFamilyEnum.SILICON_INSPIRED
        )
        assert tuple(case.name for case in result.request.cases) == (
            "matched-simple-cubic-bravais-control",
            "fcc-bravais-control",
            "silicon-inspired-diamond",
        )
        assert tuple(case.parent_kind for case in result.request.cases) == (
            ParentEnum.HERMITIAN_BRAVAIS,
            ParentEnum.HERMITIAN_BRAVAIS,
            ParentEnum.BIPARTITE_INSPIRED,
        )
        assert all(
            case.gauge_normalization is GaugeNormalizationEnum.BOND_RMS
            for case in result.request.cases
        )
        assert tuple(case.positive_bonds for case in result.request.cases) == (
            ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            (
                (1, 0, 0),
                (0, 1, 0),
                (0, 0, 1),
                (-1, 1, 0),
                (-1, 0, 1),
                (0, -1, 1),
            ),
            (
                (1, 0, 0),
                (0, 1, 0),
                (0, 0, 1),
                (-1, 1, 0),
                (-1, 0, 1),
                (0, -1, 1),
            ),
        )
        np.testing.assert_allclose(
            result.request.cases[0].direct_metric.primitive_basis,
            math.sqrt(0.5) * np.eye(3, dtype=np.float64),
            rtol=0.0,
            atol=1.0e-15,
        )
        fcc_basis = np.array(
            (
                (-0.5, 0.0, -0.5),
                (0.0, 0.5, 0.5),
                (0.5, 0.5, 0.0),
            ),
            dtype=np.float64,
        )
        np.testing.assert_allclose(
            result.request.cases[1].direct_metric.primitive_basis,
            fcc_basis,
            rtol=0.0,
            atol=0.0,
        )
        np.testing.assert_allclose(
            result.request.cases[2].direct_metric.primitive_basis,
            fcc_basis,
            rtol=0.0,
            atol=0.0,
        )
        assert tuple(case.shell_metric_scale for case in result.request.cases) == (
            2.0,
            2.0,
            2.0,
        )
        assert result.request.cases[2].basis_offsets == (
            (0.0, 0.0, 0.0),
            (0.25, 0.25, 0.25),
        )
        assert result.request.construction_size == 8
        assert result.request.evaluation_size == 17
        assert result.request.shell_cap == 7
        maximum_amplitude = math.pi / (4.0 * math.sqrt(12.0))
        assert result.request.amplitudes == pytest.approx(
            (0.0, maximum_amplitude / 2.0, maximum_amplitude)
        )
        assert (
            execution.configuration_sha256
            == hashlib.sha256(configuration_bytes).hexdigest()
        )
        assert execution.result_sha256 == hashlib.sha256(result_bytes).hexdigest()
        assert verification.result_sha256 == execution.result_sha256
        assert verification.verification.passed
        assert (
            rendering.verification_sha256
            == hashlib.sha256(verification_bytes).hexdigest()
        )
        for script, expected_sha256 in zip(
            copied,
            (
                execution.script_sha256,
                verification.script_sha256,
                rendering.script_sha256,
            ),
            strict=True,
        ):
            assert hashlib.sha256(script.read_bytes()).hexdigest() == expected_sha256
        assert {
            path.name for path in (execution_directory / "figures").glob("*.png")
        } == {"band-equivalence-locality-requirements.png"}
        assert not tuple(execution_directory.glob(".*.incomplete"))

        shutil.rmtree(execution_directory / "figures")
        verification_script_bytes = copied[1].read_bytes()
        copied[1].write_bytes(verification_script_bytes + b"\n")
        with pytest.raises(ValueError, match="verification script bytes"):
            runpy.run_path(str(copied[2]))
        assert not (execution_directory / "figures").exists()
        assert not (execution_directory / ".figures.incomplete").exists()
        copied[1].write_bytes(verification_script_bytes)
        runpy.run_path(str(copied[2]))
