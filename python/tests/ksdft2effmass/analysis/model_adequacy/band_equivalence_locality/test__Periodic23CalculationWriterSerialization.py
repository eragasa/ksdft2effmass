"""Canonical-byte contracts for migrated periodic-2D/3D calculation writers."""

from __future__ import annotations

import json
import runpy
import shutil
import sys
from collections.abc import Callable, Iterator
from dataclasses import replace
from pathlib import Path
from types import ModuleType
from typing import cast

import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    BandEquivalenceLocalityRequest,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.decision_landscape import (  # noqa: E501
    ShellScaleDecisionLandscapeRequest,
    ShellScaleDecisionLandscapeResult,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.records import (
    BandEquivalenceLocalityRefinementAssessmentRecord,
    BandEquivalenceLocalityVerificationDiagnostics,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.result import (
    BandEquivalenceLocalityCalculationResult,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    SyntheticStrainResult,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_response import (  # noqa: E501
    SyntheticStrainResponseResult,
    SyntheticStrainWitnessScanResult,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_scan import (  # noqa: E501
    SyntheticStrainScanRequest,
    SyntheticStrainScanSummary,
    SyntheticStrainTransitionRefinementResult,
)
from ksdft2effmass.serialization import BaseTypedRecord

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]

_LOCALITY_FAMILIES = (
    "periodic2d/rank2/orthogonal/band-equivalence-locality",
    "periodic2d/rank2/nonorthogonal/band-equivalence-locality",
    "periodic3d/rank2/orthogonal/band-equivalence-locality",
    "periodic3d/rank2/nonorthogonal/band-equivalence-locality",
)
_STRAIN_FAMILIES = (
    "periodic2d/rank2/strain-locality",
    "periodic3d/rank2/strain-locality",
)
_WRITER_PATHS = (
    *(
        f"{family}/{script}"
        for family in _LOCALITY_FAMILIES
        for script in (
            "run_development.py",
            "run_first_refinement.py",
            "run_second_refinement.py",
        )
    ),
    *(
        f"{family}/{script}"
        for family in _STRAIN_FAMILIES
        for script in (
            "run_development.py",
            "run_response_development.py",
            "run_scan_development.py",
        )
    ),
    "band-equivalence-dimensional-comparison/plot_shell_scale_decision_landscapes.py",
)


@pytest.fixture
def calculation_module_isolation() -> Iterator[None]:
    """Restore calculation-local module names after each script execution."""
    module_names = ("run_development", "run_first_refinement")
    previous: dict[str, ModuleType] = {}
    for module_name in module_names:
        module = sys.modules.pop(module_name, None)
        if module is not None:
            previous[module_name] = module
    try:
        yield
    finally:
        for module_name in module_names:
            sys.modules.pop(module_name, None)
        sys.modules.update(previous)


def _record_type(relative_path: str, path: Path) -> type[BaseTypedRecord]:
    name = path.name
    if name == "development-input.json":
        return BandEquivalenceLocalityRequest
    if name == "development-verification.json":
        return BandEquivalenceLocalityVerificationDiagnostics
    if name == "development-refinement-assessment.json":
        return BandEquivalenceLocalityRefinementAssessmentRecord
    if name.endswith("shell-scale-request.json"):
        return ShellScaleDecisionLandscapeRequest
    if name.endswith("shell-scale-result.json"):
        return ShellScaleDecisionLandscapeResult
    if name.endswith("strain-scan-request.json"):
        return SyntheticStrainScanRequest
    if name.endswith("geometry-source.json"):
        return SyntheticStrainResult
    if name.endswith("witness-source.json"):
        return SyntheticStrainWitnessScanResult
    if name.endswith(("response-source.json", "m1-result.json", "m2-result.json")):
        return SyntheticStrainResponseResult
    if name.endswith("strain-scan-summary.json"):
        return SyntheticStrainScanSummary
    if name.endswith("strain-transition-refinement.json"):
        return SyntheticStrainTransitionRefinementResult
    if name == "development-result.json" and "strain-locality" in relative_path:
        return SyntheticStrainResult
    if name == "development-result.json":
        return BandEquivalenceLocalityCalculationResult
    raise AssertionError(f"unclassified emitted JSON record: {path}")


class TestPeriodic23CalculationWriterSerialization:
    """Prevent bytes/text regressions in calculation-owned development writers."""

    @pytest.mark.parametrize("relative_path", _WRITER_PATHS)
    def test_writer_executes_and_emits_json_bytes(
        self,
        relative_path: str,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        calculation_module_isolation: None,
    ) -> None:
        repository = Path(__file__).resolve().parents[6]
        source_calculations = repository / "calculations"
        temporary_calculations = tmp_path / "calculations"
        source = source_calculations / relative_path
        destination = temporary_calculations / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

        if relative_path.endswith(
            ("run_first_refinement.py", "run_second_refinement.py")
        ):
            shutil.copy2(
                source.parent / "run_development.py",
                destination.parent,
            )
        if relative_path.endswith("run_second_refinement.py"):
            shutil.copy2(
                source.parent / "run_first_refinement.py",
                destination.parent,
            )
        if relative_path.startswith("band-equivalence-dimensional-comparison/"):
            for family in _LOCALITY_FAMILIES:
                dependency = source_calculations / family / "run_development.py"
                copied = temporary_calculations / family / "run_development.py"
                copied.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dependency, copied)

        monkeypatch.syspath_prepend(str(destination.parent))
        namespace = runpy.run_path(str(destination))
        main = cast(Callable[[], int], namespace["main"])
        script_globals = main.__globals__

        if relative_path.endswith(
            ("run_first_refinement.py", "run_second_refinement.py")
        ):
            nominal = cast(
                BandEquivalenceLocalityRequest,
                script_globals["DEFINITION"],
            )
            base_size = max(4, nominal.construction_size // 2)
            script_globals["REFINEMENT"] = replace(
                nominal,
                construction_size=base_size,
                evaluation_size=2 * base_size + 1,
            )
        if relative_path.endswith("run_second_refinement.py"):
            script_globals["DEFINITION"] = replace(
                nominal,
                construction_size=base_size,
                evaluation_size=2 * base_size + 1,
            )
            script_globals["FIRST_REFINEMENT"] = replace(
                nominal,
                construction_size=2 * base_size,
                evaluation_size=4 * base_size + 1,
            )
            script_globals["REFINEMENT"] = replace(
                nominal,
                construction_size=4 * base_size,
                evaluation_size=8 * base_size + 1,
            )
        if "strain-locality" in relative_path:
            script_globals["FRACTIONS"] = (0.0, 0.5, 1.0)
        if relative_path.startswith("band-equivalence-dimensional-comparison/"):
            original_loader = cast(
                Callable[[Path, int], BandEquivalenceLocalityRequest],
                script_globals["_load_definition"],
            )
            request_type = cast(
                type[ShellScaleDecisionLandscapeRequest],
                script_globals["ShellScaleDecisionLandscapeRequest"],
            )

            def reduced_loader(
                path: Path, index: int
            ) -> BandEquivalenceLocalityRequest:
                request = original_loader(path, index)
                construction_size = max(4, request.construction_size // 2)
                return replace(
                    request,
                    construction_size=construction_size,
                    evaluation_size=2 * construction_size + 1,
                )

            def reduced_request(
                *,
                locality_request: BandEquivalenceLocalityRequest,
                scale_sample_count: int,
            ) -> ShellScaleDecisionLandscapeRequest:
                del scale_sample_count
                return request_type(
                    locality_request=locality_request,
                    scale_sample_count=3,
                )

            script_globals["_load_definition"] = reduced_loader
            script_globals["ShellScaleDecisionLandscapeRequest"] = reduced_request

        assert main() == 0

        json_paths = tuple(destination.parent.rglob("*.json"))
        assert json_paths
        for path in json_paths:
            payload = path.read_bytes()
            assert payload
            assert isinstance(json.loads(payload), dict), path
            record = _record_type(relative_path, path).from_json(payload)
            assert record.to_json() == payload
