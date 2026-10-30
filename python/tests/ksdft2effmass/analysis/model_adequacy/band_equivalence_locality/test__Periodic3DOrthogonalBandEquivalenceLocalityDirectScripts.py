"""Direct-lifecycle contracts for orthogonal periodic-3D band locality."""

from __future__ import annotations

import ast
import hashlib
import runpy
import shutil
from dataclasses import replace
from pathlib import Path

import pytest
from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.calculation import (  # noqa: E501
    BandEquivalenceLocalityVerifier,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.definitions import (  # noqa: E501
    BandEquivalenceLocalityFamilyEnum,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.lifecycle import (  # noqa: E501
    BandEquivalenceLocalityExecution,
    BandEquivalenceLocalityExecutionVerification,
    BandEquivalenceLocalityRendering,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.reference import (  # noqa: E501
    BandEquivalenceLocalityIndependentShellPowerAnalyzer,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.result import (
    BandEquivalenceLocalityCalculationResult,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.verification import (  # noqa: E501
    BandEquivalenceLocalityResultVerifier,
    BandEquivalenceLocalityVerificationThresholds,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic3DOrthogonalBandEquivalenceLocalityDirectScripts:
    """Establish the bounded simple-cubic calculate/verify/render lifecycle."""

    def test_scripts_execute_closed_typed_lifecycle(self, tmp_path: Path) -> None:
        repository = Path(__file__).resolve().parents[6]
        source_root = (
            repository
            / "calculations"
            / "periodic3d"
            / "rank2"
            / "orthogonal"
            / "band-equivalence-locality"
        )
        calculation = (
            tmp_path
            / "calculations"
            / "periodic3d"
            / "rank2"
            / "orthogonal"
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
        for source, destination in zip(scripts, copied, strict=True):
            shutil.copy2(source, destination)
            source_text = source.read_text(encoding="utf-8")
            tree = ast.parse(source_text, filename=str(source))
            assert not any(
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                for node in ast.walk(tree)
            )
            assert "Workflow" not in source_text
            assert "import json" not in source_text
            assert "TypedJsonValueCodec" not in source_text
            assert "serialize_bytes" not in source_text
            assert "deserialize_bytes" not in source_text

        runpy.run_path(str(copied[0]))

        execution = calculation / "executions" / "direct-simple-cubic-rank2-n8"
        execution_path = execution / "execution.json"
        result_path = execution / "results" / "result.json"
        verification_path = execution / "verification" / "verification.json"
        result_bytes = result_path.read_bytes()
        result = BandEquivalenceLocalityCalculationResult.from_json(result_bytes)
        execution_bytes = execution_path.read_bytes()
        execution_record = BandEquivalenceLocalityExecution.from_json(execution_bytes)

        calculation_script_bytes = copied[0].read_bytes()
        copied[0].write_bytes(calculation_script_bytes + b"\n")
        with pytest.raises(ValueError, match="calculation script bytes"):
            runpy.run_path(str(copied[1]))
        assert not (execution / "verification").exists()
        assert not (execution / ".verification.incomplete").exists()
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
                execution_record,
                result_sha256=hashlib.sha256(mutated_bytes).hexdigest(),
            ).to_json()
        )
        with pytest.raises(ValueError, match="independent verification failed"):
            runpy.run_path(str(copied[1]))
        assert not (execution / "verification").exists()
        assert not (execution / ".verification.incomplete").exists()
        result_path.write_bytes(result_bytes)
        execution_path.write_bytes(execution_bytes)

        runpy.run_path(str(copied[1]))
        runpy.run_path(str(copied[2]))

        assert result.to_json() == result_bytes
        assert result.request.family is BandEquivalenceLocalityFamilyEnum.SIMPLE_CUBIC
        assert tuple(case.dimension for case in result.request.cases) == (3,)
        assert execution_record.to_json() == execution_bytes
        assert (execution / "inputs" / "configuration.json").is_file()
        assert verification_path.is_file()
        assert {path.name for path in (execution / "figures").glob("*.png")} == {
            "band-equivalence-locality-requirements.png"
        }
        assert not tuple(execution.glob(".*.incomplete"))

        verification_record = BandEquivalenceLocalityExecutionVerification.from_json(
            verification_path.read_bytes()
        )
        assert verification_record.verification.passed
        assert (
            verification_record.verification.subject_sha256
            == hashlib.sha256(result_bytes).hexdigest()
        )
        rendering_path = execution / "figures" / "rendering.json"
        rendering_bytes = rendering_path.read_bytes()
        assert (
            BandEquivalenceLocalityRendering.from_json(rendering_bytes).to_json()
            == rendering_bytes
        )

        shutil.rmtree(execution / "figures")
        verification_script_bytes = copied[1].read_bytes()
        copied[1].write_bytes(verification_script_bytes + b"\n")
        with pytest.raises(ValueError, match="verification script bytes"):
            runpy.run_path(str(copied[2]))
        assert not (execution / "figures").exists()
        assert not (execution / ".figures.incomplete").exists()
        copied[1].write_bytes(verification_script_bytes)
        runpy.run_path(str(copied[2]))

        thresholds = BandEquivalenceLocalityVerificationThresholds(
            stored_identity_maximum_defect=ScalarQuantity(5.0e-11, Unitless()),
            independent_parent_maximum_defect=ScalarQuantity(5.0e-14, Unitless()),
            independent_band_maximum_defect=ScalarQuantity(5.0e-14, Unitless()),
            independent_shell_power_maximum_defect=ScalarQuantity(
                5.0e-11,
                Unitless(),
            ),
        )
        mutated_verification = (
            BandEquivalenceLocalityResultVerifier(
                result_wire=mutated_bytes,
                diagnostic_verifier=BandEquivalenceLocalityVerifier(
                    request=result.request,
                    result=mutated_result.diagnostics,
                ),
                shell_power_analyzer=BandEquivalenceLocalityIndependentShellPowerAnalyzer(
                    request=result.request
                ),
                thresholds=thresholds,
            )
            .result()
            .verification
        )

        assert (
            mutated_verification.subject_sha256
            == hashlib.sha256(mutated_bytes).hexdigest()
        )
        assert not mutated_verification.passed
