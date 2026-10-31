"""Tests for the cohesive embedded rank-two calculation record."""

from __future__ import annotations

import ast
import hashlib
import math
import runpy
import shutil
from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path

import pytest
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d import (
    CalculationWireEnum,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalyzer,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest,
    Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementThresholds,
    Periodic1DEmbeddedSubspaceRank2CalculationRecord,
    Periodic1DEmbeddedSubspaceRank2CalculationVerification,
    Periodic1DEmbeddedSubspaceRank2CalculationVerifier,
    Periodic1DEmbeddedSubspaceRank2CalculationVisualizationData,
    Periodic1DEmbeddedSubspaceRank2CalculationVisualizationPlot,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalyzer,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalyzer,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyRequest,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyVisualizationPlot,
    Periodic1DEmbeddedSubspaceRank2Request,
    Periodic1DEmbeddedSubspaceRank2TruncationAnalyzer,
    Periodic1DEmbeddedSubspaceRank2TruncationRequest,
)
from ksdft2effmass.serialization import TypedJsonValueCodec


def _script_directory() -> Path:
    repository = next(
        parent
        for parent in Path(__file__).resolve().parents
        if (parent / "calculations").is_dir()
    )
    return (
        repository
        / "calculations"
        / "periodic1d"
        / "rank2"
        / "band-equivalence-versus-hopping-locality"
    )


def _template() -> Periodic1DEmbeddedSubspaceRank2Request:
    return Periodic1DEmbeddedSubspaceRank2Request(
        reciprocal_mesh_size=8,
        amplitudes=(0.0, 0.2, math.pi / 4.0),
        parent_hopping_scale=1.0,
        minimum_external_gap=0.1,
        minimum_transport_singular_value=0.8,
        frame_absolute_tolerance=1.0e-10,
        transport_rank_relative_tolerance=1.0e-12,
        transport_validation_relative_tolerance=1.0e-10,
        harmonic_absolute_degeneracy_tolerance=1.0e-14,
        harmonic_relative_degeneracy_tolerance=1.0e-12,
    )


def _record() -> Periodic1DEmbeddedSubspaceRank2CalculationRecord:
    template = _template()
    transporter = ClosedLoopPolarFrameTransporter()
    parent_family = Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalyzer(
        request=Periodic1DEmbeddedSubspaceRank2ParentFamilyRequest(
            template_request=template,
            parent_hopping_scales=(0.0, 1.0),
        ),
        transporter=transporter,
    ).execute()
    momentum_refinement = Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalyzer(
        request=Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest(
            template_request=template,
            reciprocal_mesh_sizes=(8, 16),
            thresholds=Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds(
                maximum_parent_diagnostic_change=1.0,
                maximum_correlation_change=1.0,
                maximum_threshold_change=1.0,
                maximum_hopping_weight_change=1.0,
                maximum_hopping_power_change=1.0,
                maximum_angle_change=1.0,
                maximum_band_defect=1.0,
                maximum_reconstruction_defect=1.0,
                maximum_parseval_defect=1.0,
            ),
            required_stable_refinements=1,
        ),
        transporter=transporter,
    ).execute()
    adaptive_amplitude = Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalyzer(
        request=Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest(
            template_request=template,
            thresholds=Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementThresholds(
                maximum_correlation_defect=1.0,
                maximum_operator_threshold_defect=1.0,
                maximum_joint_threshold_defect=1.0,
                maximum_hopping_weight_defect=1.0,
                maximum_hopping_power_defect=1.0,
            ),
            maximum_refinement_levels=2,
            maximum_evaluated_amplitudes=20,
        ),
        transporter=transporter,
    ).execute()
    truncation = Periodic1DEmbeddedSubspaceRank2TruncationAnalyzer(
        request=Periodic1DEmbeddedSubspaceRank2TruncationRequest.every_integer_through(
            template_request=template,
            maximum_range=3,
            evaluation_mesh_size=17,
        ),
        transporter=transporter,
    ).execute()
    return Periodic1DEmbeddedSubspaceRank2CalculationRecord(
        parent_family=parent_family,
        momentum_refinement=momentum_refinement,
        adaptive_amplitude=adaptive_amplitude,
        truncation=truncation,
    )


class TestPeriodic1DEmbeddedSubspaceRank2CalculationRecord:
    """Establish canonical aggregate admission without rerunning producers."""

    def test_round_trip_preserves_canonical_typed_json(self) -> None:
        record = _record()
        payload = record.to_json()

        admitted = type(record).from_json(payload)
        admitted_from_mapping = type(record).from_dict(record.to_dict())

        assert admitted_from_mapping.to_json() == payload
        assert admitted.to_dict() == record.to_dict()
        assert admitted.to_json() == payload
        assert CalculationWireEnum.MOMENTUM_CONVERGED.value in payload.decode()
        assert CalculationWireEnum.AMPLITUDE_CONVERGED.value in payload.decode()
        assert CalculationWireEnum.TRUNCATION_COMPLETED.value in payload.decode()

    def test_rejects_unknown_or_cross_channel_wire_enums(self) -> None:
        record = _record()
        values = dict(record.to_dict())
        momentum_value = values["momentum_refinement"]
        assert isinstance(momentum_value, Mapping)
        momentum = dict(momentum_value)
        momentum["variant"] = CalculationWireEnum.TRUNCATION_COMPLETED.value
        values["momentum_refinement"] = momentum

        with pytest.raises(ValueError, match="momentum-refinement"):
            type(record).from_dict(values)

    def test_verifier_authenticates_bytes_and_all_independent_routes(self) -> None:
        subject = _record().to_json()

        verification = Periodic1DEmbeddedSubspaceRank2CalculationVerifier(
            subject
        ).result()

        assert verification.passed
        assert verification.subject_sha256 == hashlib.sha256(subject).hexdigest()
        assert tuple(verification.component_types) == (
            "parent_family",
            "momentum_refinement",
            "adaptive_amplitude",
            "truncation",
        )
        assert (
            type(verification).from_dict(verification.to_dict()).to_json()
            == verification.to_json()
        )
        assert (
            Periodic1DEmbeddedSubspaceRank2CalculationVerification.from_json(
                verification.to_json()
            ).to_json()
            == verification.to_json()
        )
        admitted = Periodic1DEmbeddedSubspaceRank2CalculationVerifier(
            subject
        ).admit_stored(verification)
        assert admitted.to_json() == subject
        visualization_data = (
            Periodic1DEmbeddedSubspaceRank2CalculationVisualizationData.from_record(
                admitted,
                source_sha256=verification.subject_sha256,
            )
        )
        assert hashlib.sha256(visualization_data.to_json()).hexdigest() == (
            verification.visualization_data_sha256
        )
        assert (
            type(visualization_data).from_json(visualization_data.to_json())
            == visualization_data
        )
        with pytest.raises(ValueError, match="different visualization data"):
            Periodic1DEmbeddedSubspaceRank2CalculationVerifier(subject).admit_stored(
                replace(verification, visualization_data_sha256="0" * 64)
            )
        with pytest.raises(ValueError, match="different subject bytes"):
            Periodic1DEmbeddedSubspaceRank2CalculationVerifier(subject).admit_stored(
                replace(verification, subject_sha256="0" * 64)
            )

    def test_verifier_rejects_noncanonical_subject_bytes(self) -> None:
        subject = _record().to_json()

        with pytest.raises(ValueError, match="canonical retained representation"):
            Periodic1DEmbeddedSubspaceRank2CalculationVerifier(subject + b"\n").result()

    def test_direct_scripts_use_stored_verification_and_refuse_overwrite(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        source_scripts = _script_directory()
        scripts = tmp_path / "band-equivalence-versus-hopping-locality"
        scripts.mkdir()
        for name in (
            "run_01_calculation.py",
            "run_02_verification.py",
            "run_03_render.py",
        ):
            source = (source_scripts / name).read_text(encoding="utf-8")
            tree = ast.parse(source)
            assert not any(
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                for node in ast.walk(tree)
            )
            assert not any(
                isinstance(node, ast.Attribute) and node.attr == "tolist"
                for node in ast.walk(tree)
            )
            assert "Workflow" not in source
            assert "argparse" not in source
            assert "import json" not in source
            (scripts / name).write_text(source, encoding="utf-8")

        calculation_path = scripts / "run_01_calculation.py"
        calculation_source = calculation_path.read_text(encoding="utf-8")
        replacements = {
            "DRAFT_TOLERANCE = 1.01e-8": "DRAFT_TOLERANCE = 0.1",
            "PARENT_FAMILY_MESH_SIZE = 256": "PARENT_FAMILY_MESH_SIZE = 8",
            "PARENT_FAMILY_AMPLITUDE_INTERVALS = 32": (
                "PARENT_FAMILY_AMPLITUDE_INTERVALS = 2"
            ),
            "PARENT_HOPPING_SCALES = (0.0, 0.25, 0.5, 0.75, 1.0)": (
                "PARENT_HOPPING_SCALES = (0.0, 1.0)"
            ),
            "MOMENTUM_MESH_SIZES = (32, 64, 128, 256, 512)": (
                "MOMENTUM_MESH_SIZES = (8, 16)"
            ),
            "MOMENTUM_AMPLITUDE_INTERVALS = 64": ("MOMENTUM_AMPLITUDE_INTERVALS = 2"),
            "MOMENTUM_REQUIRED_STABLE_REFINEMENTS = 2": (
                "MOMENTUM_REQUIRED_STABLE_REFINEMENTS = 1"
            ),
            "ADAPTIVE_MESH_SIZE = 128": "ADAPTIVE_MESH_SIZE = 8",
            "ADAPTIVE_INITIAL_AMPLITUDE_INTERVALS = 8": (
                "ADAPTIVE_INITIAL_AMPLITUDE_INTERVALS = 2"
            ),
            "ADAPTIVE_MAXIMUM_REFINEMENT_LEVELS = 4": (
                "ADAPTIVE_MAXIMUM_REFINEMENT_LEVELS = 1"
            ),
            "ADAPTIVE_MAXIMUM_EVALUATED_AMPLITUDES = 129": (
                "ADAPTIVE_MAXIMUM_EVALUATED_AMPLITUDES = 5"
            ),
            "TRUNCATION_MAXIMUM_RANGE = 16": "TRUNCATION_MAXIMUM_RANGE = 1",
            "TRUNCATION_EVALUATION_MESH_SIZE = 1025": (
                "TRUNCATION_EVALUATION_MESH_SIZE = 17"
            ),
        }
        for old, new in replacements.items():
            assert old in calculation_source
            calculation_source = calculation_source.replace(old, new)
        calculation_path.write_text(calculation_source, encoding="utf-8")
        render_path = scripts / "run_03_render.py"
        render_path.write_text(
            render_path.read_text(encoding="utf-8").replace("DPI = 180", "DPI = 72"),
            encoding="utf-8",
        )

        runpy.run_path(str(calculation_path))
        verification_path = scripts / "run_02_verification.py"
        runpy.run_path(str(verification_path))
        execution = scripts / "executions" / "direct-embedded-rank2-controlled-v2"
        result_bytes = (execution / "results" / "calculation.json").read_bytes()
        retained_verification_bytes = (
            execution / "verification" / "verification.json"
        ).read_bytes()
        assert (
            Periodic1DEmbeddedSubspaceRank2CalculationRecord.from_json(
                result_bytes
            ).to_json()
            == result_bytes
        )
        assert (
            Periodic1DEmbeddedSubspaceRank2CalculationVerification.from_json(
                retained_verification_bytes
            ).to_json()
            == retained_verification_bytes
        )

        tampered_scripts = tmp_path / "tampered"
        tampered_scripts.mkdir()
        for script in scripts.glob("run_0*.py"):
            shutil.copy2(script, tampered_scripts / script.name)
        shutil.copytree(scripts / "executions", tampered_scripts / "executions")
        tampered_result = (
            tampered_scripts
            / "executions"
            / "direct-embedded-rank2-controlled-v2"
            / "results"
            / "calculation.json"
        )
        tampered_result.write_bytes(tampered_result.read_bytes() + b"\n")

        def _forbidden_result(
            verifier: Periodic1DEmbeddedSubspaceRank2CalculationVerifier,
        ) -> Periodic1DEmbeddedSubspaceRank2CalculationVerification:
            raise AssertionError("rendering must not rerun independent verification")

        monkeypatch.setattr(
            Periodic1DEmbeddedSubspaceRank2CalculationVerifier,
            "result",
            _forbidden_result,
        )
        runpy.run_path(str(render_path))
        with pytest.raises(ValueError, match="different result bytes"):
            runpy.run_path(str(tampered_scripts / "run_03_render.py"))

        expected_filenames = {
            plot.value
            for plot in (
                *Periodic1DEmbeddedSubspaceRank2ParentFamilyVisualizationPlot,
                *Periodic1DEmbeddedSubspaceRank2CalculationVisualizationPlot,
            )
        }
        assert {
            path.name for path in (execution / "figures").glob("*.png")
        } == expected_filenames
        rendering_bytes = (execution / "figures" / "rendering.json").read_bytes()
        rendering = TypedJsonValueCodec().deserialize_bytes(rendering_bytes)
        assert isinstance(rendering, Mapping)
        figures = rendering["figures"]
        assert isinstance(figures, Mapping)
        assert set(figures) == expected_filenames
        assert not any(
            path.name.startswith(".") and path.name.endswith(".incomplete")
            for path in execution.parent.iterdir()
        )
        assert not any(
            path.name.startswith(".") and path.name.endswith(".incomplete")
            for path in execution.iterdir()
        )

        with pytest.raises(FileExistsError, match="overwrite"):
            runpy.run_path(str(calculation_path))
        with pytest.raises(FileExistsError, match="overwrite"):
            runpy.run_path(str(verification_path))
        with pytest.raises(FileExistsError, match="overwrite"):
            runpy.run_path(str(render_path))
