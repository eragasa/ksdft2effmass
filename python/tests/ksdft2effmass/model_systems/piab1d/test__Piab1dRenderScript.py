"""Software verification of the successor PIAB1D rendering gate."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.model_systems.piab1d import (
    Piab1dCalculationResult,
    Piab1dVerification,
    Piab1dVisualizationPlotEnum,
)
from ksdft2effmass.serialization import SerializableValue, TypedJsonValueCodec
from ksdft2effmass.verification import VerificationObservation

pytestmark = pytest.mark.software_verification
SUT = "calculations/piab1d/run_03_render.py"


class TestPiab1dRenderScript:
    """Own rejection behavior before any PIAB1D figure is rendered."""

    @pytest.mark.parametrize(
        ("verification_passes", "valid_result_hash", "expected_error"),
        [
            (False, True, "passing verification record"),
            (True, False, "SHA-256"),
            (None, True, "verification fields"),
        ],
    )
    def test_module__untrusted_verification__rejects_before_rendering(
        self,
        tmp_path: Path,
        verification_passes: bool | None,
        valid_result_hash: bool,
        expected_error: str,
    ) -> None:
        repository_root = Path(__file__).resolve().parents[5]
        calculation = tmp_path / "calculations" / "piab1d"
        execution = calculation / "executions" / "direct-core-n8-m3"
        results = execution / "results"
        verification_directory = execution / "verification"
        figures = execution / "figures"
        results.mkdir(parents=True)
        verification_directory.mkdir()
        script = calculation / "run_03_render.py"
        shutil.copy2(repository_root / SUT, script)
        codec = TypedJsonValueCodec()
        result_path = results / "result.json"
        result_path.write_bytes(
            codec.serialize_bytes({"execution_id": "direct-core-n8-m3"})
        )
        result_sha256 = hashlib.sha256(result_path.read_bytes()).hexdigest()
        if verification_passes is None:
            verification: dict[str, SerializableValue] = {
                "unexpected": "malformed verification"
            }
        else:
            verification_value = Piab1dVerification(
                subject_sha256=result_sha256,
                visualization_data_sha256="0" * 64,
                components=tuple(
                    component_type(
                        {
                            f"declared_check_{index}": VerificationObservation(
                                value=ScalarQuantity(
                                    (
                                        2.0
                                        if index == 0 and not verification_passes
                                        else 0.0
                                    ),
                                    Unitless(),
                                ),
                                tolerance=ScalarQuantity(1.0, Unitless()),
                            )
                        }
                    )
                    for index, component_type in enumerate(
                        Piab1dVerification.component_types.values()
                    )
                ),
            )
            verification = dict(verification_value.to_dict())
        verification_document: dict[str, SerializableValue] = {
            "execution_id": "direct-core-n8-m3",
            "verification": verification,
            "result_sha256": result_sha256 if valid_result_hash else "0" * 64,
        }
        (verification_directory / "verification.json").write_bytes(
            codec.serialize_bytes(verification_document)
        )
        environment = dict(os.environ)
        environment["MPLBACKEND"] = "Agg"

        completed = subprocess.run(
            [sys.executable, str(script)],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )

        assert completed.returncode != 0
        assert expected_error in completed.stderr
        assert not figures.exists()
        assert not (execution / ".figures.incomplete").exists()

    def test_module__verified_result__atomically_writes_authenticated_inventory(
        self,
        tmp_path: Path,
    ) -> None:
        repository_root = Path(__file__).resolve().parents[5]
        calculation = tmp_path / "calculations" / "piab1d"
        (calculation / "executions").mkdir(parents=True)
        scripts = (
            "run_01_calculation.py",
            "run_02_verification.py",
            "run_03_render.py",
        )
        for name in scripts:
            shutil.copy2(
                repository_root / "calculations" / "piab1d" / name, calculation
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

        execution = calculation / "executions" / "direct-core-n8-m3"
        result_wire = (execution / "results" / "result.json").read_bytes()
        assert Piab1dCalculationResult.from_json(result_wire).to_json() == result_wire
        decoded_result = TypedJsonValueCodec().deserialize_bytes(result_wire)
        assert isinstance(decoded_result, dict)
        expected_section_fields = {
            "configuration": {
                "unit_system",
                "hbar",
                "length",
                "mass",
                "interior_points",
                "retained_dimension",
                "boundary_condition",
            },
            "eigenvectors": {"euclidean", "quadrature_normalized"},
            "quadrature": {
                "spacing",
                "interior_weights",
                "weighted_gram",
                "weighted_projector",
            },
            "retained_dimension_selection": {"beta", "selection"},
        }
        for section_name, expected_fields in expected_section_fields.items():
            section = decoded_result[section_name]
            assert isinstance(section, dict)
            assert set(section) == expected_fields
        figures = execution / "figures"
        rendering_value = TypedJsonValueCodec().deserialize_bytes(
            (figures / "rendering.json").read_bytes()
        )
        assert isinstance(rendering_value, dict)
        figure_records = rendering_value["figures"]
        assert isinstance(figure_records, dict)
        assert set(figure_records) == {
            "spectrum-and-states.png",
            "residual-matrices.png",
            "figure_01a_continuum_wavefunction_ladder.png",
            "figure_01b_discrete_wavefunction_ladder.png",
            "figure_02_retained_dimension_selection.png",
            "convergence-series.png",
            "convergence-mode-sweep.png",
            "higher-eigenpair-sweep.png",
            "higher-mode-convergence.png",
            "operator-residual-norms.png",
            "eigensolver-residual-norms.png",
            Piab1dVisualizationPlotEnum.finite_algebraic_diagnostics.value,
            Piab1dVisualizationPlotEnum.kinetic_potential_decomposition.value,
        }
        for filename, record_value in figure_records.items():
            assert isinstance(record_value, dict)
            assert record_value["media_type"] == "image/png"
            assert (
                record_value["sha256"]
                == hashlib.sha256((figures / filename).read_bytes()).hexdigest()
            )
        assert not (execution / ".figures.incomplete").exists()
