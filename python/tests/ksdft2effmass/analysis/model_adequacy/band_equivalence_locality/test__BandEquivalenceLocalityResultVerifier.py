"""Software contracts for BandEquivalenceLocalityResultVerifier."""

from __future__ import annotations

import ast
import hashlib
import inspect
import math
import runpy
import shutil
from dataclasses import replace
from pathlib import Path
from typing import Never

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import DirectLattice2D, DirectLatticeMetric
from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.analysis import (
    BandEquivalenceLocalityAnalyzer,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.calculation import (  # noqa: E501
    BandEquivalenceLocalityVerifier,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.definitions import (  # noqa: E501
    FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
    BandEquivalenceLocalityCase,
    BandEquivalenceLocalityFamilyEnum,
    BandEquivalenceLocalityRequest,
    GaugeNormalizationEnum,
    ParentEnum,
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
    BandEquivalenceLocalityAnalysisRecorder,
    BandEquivalenceLocalityCalculationResult,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.verification import (  # noqa: E501
    BandEquivalenceLocalityResultVerifier,
    BandEquivalenceLocalityVerificationThresholds,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestBandEquivalenceLocalityResultVerifier:
    """Establish exact-byte admission and its direct lifecycle integration."""

    def request(self) -> BandEquivalenceLocalityRequest:
        return BandEquivalenceLocalityRequest(
            family=BandEquivalenceLocalityFamilyEnum.SQUARE,
            synthetic_model=FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
            cases=(
                BandEquivalenceLocalityCase(
                    name="square-test-parent",
                    dimension=2,
                    parent_kind=ParentEnum.DIRECTED_AXIS,
                    gauge_normalization=GaugeNormalizationEnum.AXIS_MAXIMUM,
                    positive_bonds=((1, 0), (0, 1)),
                    direct_metric=DirectLatticeMetric(
                        DirectLattice2D(
                            a1=np.array((1.0, 0.0), dtype=np.float64),
                            a2=np.array((0.0, 1.0), dtype=np.float64),
                        )
                    ),
                    shell_metric_scale=1.0,
                ),
            ),
            construction_size=4,
            evaluation_size=5,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(0.0,),
            amplitudes=(0.0, math.pi / 8.0),
            band_tolerances=(1.0e-3,),
            shell_cap=4,
            amplitude_resolution_intervals=(1, 2),
        )

    def result(self) -> BandEquivalenceLocalityCalculationResult:
        request = self.request()
        analysis = BandEquivalenceLocalityAnalyzer(request=request).execute()
        return BandEquivalenceLocalityAnalysisRecorder(analysis).result()

    def scripts(self) -> tuple[Path, ...]:
        root = (
            Path(__file__).resolve().parents[6]
            / "calculations/periodic2d/rank2/orthogonal/band-equivalence-locality"
        )
        return tuple(
            root / name
            for name in (
                "run_01_calculation.py",
                "run_02_verification.py",
                "run_03_render.py",
            )
        )

    def test__request_admission__rejects_noncanonical_field_inventories(self) -> None:
        wire = self.request().to_json()

        extra = wire.removesuffix(b"}\n") + b',\n  "unexpected_field": 1\n}\n'
        with pytest.raises(ValueError, match="fields do not match"):
            BandEquivalenceLocalityRequest.from_json(extra)

        shell_cap_field = b'  "shell_cap": 4,\n'
        assert wire.count(shell_cap_field) == 1
        missing = wire.replace(shell_cap_field, b"")
        with pytest.raises(ValueError, match="fields do not match"):
            BandEquivalenceLocalityRequest.from_json(missing)

        case_suffix = b'        "shell_metric_scale": 1.0\n      }\n    ]\n  },'
        assert wire.count(case_suffix) == 1
        nested = wire.replace(
            case_suffix,
            b'        "shell_metric_scale": 1.0,\n'
            b'        "unexpected_nested_field": 1\n'
            b"      }\n    ]\n  },",
        )
        with pytest.raises(ValueError, match="case fields do not match"):
            BandEquivalenceLocalityRequest.from_json(nested)

        construction_size_field = b'  "construction_size": 4,\n'
        assert wire.count(construction_size_field) == 1
        malformed = wire.replace(
            construction_size_field,
            b'  "construction_size": "4",\n',
        )
        with pytest.raises(TypeError, match="construction_size"):
            BandEquivalenceLocalityRequest.from_json(malformed)

    def test__result_reconstruction__does_not_execute_scientific_producer(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        wire = self.result().to_json()

        def fail_if_executed(analyzer: BandEquivalenceLocalityAnalyzer) -> Never:
            raise AssertionError(analyzer)

        monkeypatch.setattr(
            BandEquivalenceLocalityAnalyzer, "execute", fail_if_executed
        )

        reconstructed = BandEquivalenceLocalityCalculationResult.from_json(wire)

        assert reconstructed.to_json() == wire

    def test__actions__bind_requests_and_collaborators_before_zero_argument_execution(
        self,
    ) -> None:
        analyzer_parameters = inspect.signature(
            BandEquivalenceLocalityAnalyzer.execute
        ).parameters
        diagnostic_verifier_parameters = inspect.signature(
            BandEquivalenceLocalityVerifier.execute
        ).parameters
        verifier_parameters = inspect.signature(
            BandEquivalenceLocalityResultVerifier.result
        ).parameters

        assert tuple(analyzer_parameters) == ("self",)
        assert tuple(diagnostic_verifier_parameters) == ("self",)
        assert tuple(verifier_parameters) == ("self",)
        request = self.request()
        analyzer = BandEquivalenceLocalityAnalyzer(request=request)
        assert analyzer.request is request

    def test__exact_byte_verifier__rejects_modified_result_and_projection(self) -> None:
        result = self.result()
        result_wire = result.to_json()
        request = self.request()
        thresholds = BandEquivalenceLocalityVerificationThresholds(
            stored_identity_maximum_defect=ScalarQuantity(5.0e-11, Unitless()),
            independent_parent_maximum_defect=ScalarQuantity(5.0e-14, Unitless()),
            independent_band_maximum_defect=ScalarQuantity(5.0e-14, Unitless()),
            independent_shell_power_maximum_defect=ScalarQuantity(
                5.0e-11,
                Unitless(),
            ),
        )
        verifier = BandEquivalenceLocalityResultVerifier(
            result_wire=result_wire,
            diagnostic_verifier=BandEquivalenceLocalityVerifier(
                request=request,
                result=result.diagnostics,
            ),
            shell_power_analyzer=(
                BandEquivalenceLocalityIndependentShellPowerAnalyzer(request=request)
            ),
            thresholds=thresholds,
        )
        verified = verifier.result()
        assert verified.verification.passed

        with pytest.raises(ValueError, match="verifier result does not match"):
            BandEquivalenceLocalityResultVerifier(
                result_wire=result_wire,
                diagnostic_verifier=BandEquivalenceLocalityVerifier(
                    request=request,
                    result=replace(result.diagnostics, status="mismatched"),
                ),
                shell_power_analyzer=(
                    BandEquivalenceLocalityIndependentShellPowerAnalyzer(
                        request=request
                    )
                ),
                thresholds=thresholds,
            )

        modified_result = (
            result_wire.removesuffix(b"}\n") + b',\n  "unexpected_field": 1\n}\n'
        )
        with pytest.raises(ValueError, match="fields do not match"):
            BandEquivalenceLocalityResultVerifier(
                result_wire=modified_result,
                diagnostic_verifier=BandEquivalenceLocalityVerifier(
                    request=request,
                    result=result.diagnostics,
                ),
                shell_power_analyzer=(
                    BandEquivalenceLocalityIndependentShellPowerAnalyzer(
                        request=request
                    )
                ),
                thresholds=thresholds,
            )

        modified_data = replace(
            verified.visualization_data,
            minimum_operator_thresholds=tuple(
                value + 1.0e-6
                for value in verified.visualization_data.minimum_operator_thresholds
            ),
        )
        with pytest.raises(ValueError, match="stored projection differs"):
            verifier.admit_stored(
                verification=verified.verification,
                visualization_data=modified_data,
            )

    @pytest.mark.parametrize(
        ("location", "field"),
        (
            ("point", "reference_nyquist_power"),
            ("point", "comparison_nyquist_power"),
            ("shell", "reference_shell_power"),
            ("shell", "comparison_shell_power"),
            ("shell", "reference_omitted_power"),
            ("shell", "comparison_omitted_power"),
            ("shell", "reference_total_omitted_power"),
            ("shell", "comparison_total_omitted_power"),
        ),
    )
    def test__independent_power_reference__rejects_canonical_stored_mutations(
        self,
        location: str,
        field: str,
    ) -> None:
        result = self.result()
        case = result.diagnostics.cases[0]
        point = case.points[0]
        if location == "point":
            value = getattr(point, field)
            assert type(value) is float
            mutated_point = replace(point, **{field: value + 0.125})
        else:
            shell = point.shell_diagnostics[0]
            value = getattr(shell, field)
            assert type(value) is float
            mutated_shell = replace(shell, **{field: value + 0.125})
            mutated_point = replace(
                point,
                shell_diagnostics=(
                    mutated_shell,
                    *point.shell_diagnostics[1:],
                ),
            )
        mutated_case = replace(
            case,
            points=(mutated_point, *case.points[1:]),
        )
        mutated_result = replace(
            result,
            diagnostics=replace(
                result.diagnostics,
                cases=(mutated_case, *result.diagnostics.cases[1:]),
            ),
        )
        mutated_wire = mutated_result.to_json()
        thresholds = BandEquivalenceLocalityVerificationThresholds(
            stored_identity_maximum_defect=ScalarQuantity(5.0e-11, Unitless()),
            independent_parent_maximum_defect=ScalarQuantity(5.0e-14, Unitless()),
            independent_band_maximum_defect=ScalarQuantity(5.0e-14, Unitless()),
            independent_shell_power_maximum_defect=ScalarQuantity(
                5.0e-11,
                Unitless(),
            ),
        )
        verification = (
            BandEquivalenceLocalityResultVerifier(
                result_wire=mutated_wire,
                diagnostic_verifier=BandEquivalenceLocalityVerifier(
                    request=result.request,
                    result=mutated_result.diagnostics,
                ),
                shell_power_analyzer=(
                    BandEquivalenceLocalityIndependentShellPowerAnalyzer(
                        request=result.request
                    )
                ),
                thresholds=thresholds,
            )
            .result()
            .verification
        )

        assert not verification.passed

    def test__direct_scripts__execute_closed_lifecycle(self, tmp_path: Path) -> None:
        source_root = self.scripts()[0].parent
        repository = Path(__file__).resolve().parents[6]
        relative_root = source_root.relative_to(repository)
        calculation = tmp_path / relative_root
        calculation.mkdir(parents=True)
        copied = tuple(calculation / path.name for path in self.scripts())
        for source, destination in zip(self.scripts(), copied, strict=True):
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

        for script in copied:
            runpy.run_path(str(script))

        execution = calculation / "executions" / "direct-square-rank2-n16"
        assert (execution / "execution.json").is_file()
        assert (execution / "inputs" / "configuration.json").is_file()
        assert (execution / "results" / "result.json").is_file()
        assert (execution / "verification" / "verification.json").is_file()
        assert {path.name for path in (execution / "figures").glob("*.png")} == {
            "band-equivalence-locality-requirements.png"
        }
        assert not tuple(execution.glob(".*.incomplete"))

    def test__retained_execution__authenticates_retained_producer_bytes(self) -> None:
        calculation = self.scripts()[0].parent
        execution_directory = calculation / "executions" / "direct-square-rank2-n16"
        producer_directory = execution_directory / "producers"
        producer_scripts = tuple(
            producer_directory / script.name for script in self.scripts()
        )
        execution_bytes = (execution_directory / "execution.json").read_bytes()
        verification_bytes = (
            execution_directory / "verification" / "verification.json"
        ).read_bytes()
        rendering_bytes = (
            execution_directory / "figures" / "rendering.json"
        ).read_bytes()
        execution = BandEquivalenceLocalityExecution.from_json(execution_bytes)
        verification = BandEquivalenceLocalityExecutionVerification.from_json(
            verification_bytes
        )
        rendering = BandEquivalenceLocalityRendering.from_json(rendering_bytes)
        configuration_bytes = (
            execution_directory / execution.configuration_path
        ).read_bytes()
        result_bytes = (execution_directory / execution.result_path).read_bytes()

        assert execution.to_json() == execution_bytes
        assert verification.to_json() == verification_bytes
        assert rendering.to_json() == rendering_bytes
        assert (
            BandEquivalenceLocalityRequest.from_json(configuration_bytes).to_json()
            == configuration_bytes
        )
        assert (
            BandEquivalenceLocalityCalculationResult.from_json(result_bytes).to_json()
            == result_bytes
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
            producer_scripts,
            (
                execution.script_sha256,
                verification.script_sha256,
                rendering.script_sha256,
            ),
            strict=True,
        ):
            assert hashlib.sha256(script.read_bytes()).hexdigest() == expected_sha256
        for filename, expected_sha256 in rendering.figures.items():
            figure_bytes = (execution_directory / "figures" / filename).read_bytes()
            assert hashlib.sha256(figure_bytes).hexdigest() == expected_sha256
