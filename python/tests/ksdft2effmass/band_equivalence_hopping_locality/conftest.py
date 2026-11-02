"""Shared execution assertion for calculation-writer serialization tests."""

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

from ksdft2effmass.band_equivalence_hopping_locality.decision_landscape import (
    ShellScaleDecisionLandscapeRequest,
    ShellScaleDecisionLandscapeResult,
)
from ksdft2effmass.band_equivalence_hopping_locality.definitions import (
    BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.band_equivalence_hopping_locality.records import (
    BandEquivalenceHoppingLocalityRefinementAssessmentRecord,
    BandEquivalenceHoppingLocalityVerificationDiagnostics,
)
from ksdft2effmass.band_equivalence_hopping_locality.strain import (
    SyntheticStrainResult,
)
from ksdft2effmass.band_equivalence_hopping_locality.strain_response import (
    SyntheticStrainResponseResult,
    SyntheticStrainWitnessScanResult,
)
from ksdft2effmass.band_equivalence_hopping_locality.strain_scan import (
    SyntheticStrainScanRequest,
    SyntheticStrainScanSummary,
    SyntheticStrainTransitionRefinementResult,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.request import (
    Periodic2DRank2BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.result import (
    Periodic2DRank2BandEquivalenceHoppingLocalityCalculationResult,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.request import (
    Periodic3DRank2BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.result import (
    Periodic3DRank2BandEquivalenceHoppingLocalityCalculationResult,
)
from ksdft2effmass.serialization import BaseTypedRecord

_LOCALITY_DEFINITION_SCRIPTS = (
    "periodic2d/rank2/orthogonal/band-equivalence-locality/run_development.py",
    (
        "periodic2d_rank2_hexagonal/band_equivalence_hopping_locality/"
        "run_nominal_calculation.py"
    ),
    "periodic3d/rank2/orthogonal/band-equivalence-locality/run_development.py",
    "periodic3d/rank2/nonorthogonal/band-equivalence-locality/run_development.py",
)
_LEGACY_REFINEMENT_SCRIPTS = (
    "run_first_refinement.py",
    "run_second_refinement.py",
)
_CONTEXT_REFINEMENT_SCRIPTS = (
    "run_refinement_01.py",
    "run_refinement_02.py",
)

CalculationWriterSerializationAssertion = Callable[
    [str, Path, pytest.MonkeyPatch, Path], None
]


@pytest.fixture
def calculation_module_isolation() -> Iterator[None]:
    """Restore calculation-local module names after each script execution."""
    module_names = (
        "run_development",
        "run_first_refinement",
        "run_nominal_calculation",
        "run_refinement_01",
    )
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


def _is_periodic2d(relative_path: str) -> bool:
    return relative_path.startswith(("periodic2d/", "periodic2d_"))


def _is_strain_context(relative_path: str) -> bool:
    return "strain-locality" in relative_path or relative_path.startswith(
        "periodic2d_rank2_rhombic_path/"
    )


def _locality_record_type(
    relative_path: str,
    *,
    result: bool,
) -> type[BaseTypedRecord]:
    if _is_periodic2d(relative_path):
        if result:
            return Periodic2DRank2BandEquivalenceHoppingLocalityCalculationResult
        return Periodic2DRank2BandEquivalenceHoppingLocalityRequest
    if relative_path.startswith(("periodic3d/", "periodic3d_")):
        if result:
            return Periodic3DRank2BandEquivalenceHoppingLocalityCalculationResult
        return Periodic3DRank2BandEquivalenceHoppingLocalityRequest
    raise AssertionError(f"unclassified locality calculation: {relative_path}")


def _record_type(relative_path: str, path: Path) -> type[BaseTypedRecord]:
    name = path.name
    if name == "development-input.json":
        return _locality_record_type(relative_path, result=False)
    if name == "development-verification.json":
        return BandEquivalenceHoppingLocalityVerificationDiagnostics
    if name == "development-refinement-assessment.json":
        return BandEquivalenceHoppingLocalityRefinementAssessmentRecord
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
    if name == "development-result.json" and _is_strain_context(relative_path):
        return SyntheticStrainResult
    if name == "development-result.json":
        return _locality_record_type(relative_path, result=True)
    raise AssertionError(f"unclassified emitted JSON record: {path}")


@pytest.fixture
def assert_calculation_writer_serialization(
    calculation_module_isolation: None,
) -> CalculationWriterSerializationAssertion:
    """Return an assertion that executes one writer in isolated scratch space."""
    del calculation_module_isolation

    def assert_writer(
        relative_path: str,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        repository_root: Path,
    ) -> None:
        source_calculations = repository_root / "calculations"
        temporary_calculations = tmp_path / "calculations"
        source = source_calculations / relative_path
        destination = temporary_calculations / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

        script_name = source.name
        if script_name in _LEGACY_REFINEMENT_SCRIPTS:
            shutil.copy2(source.parent / "run_development.py", destination.parent)
        if script_name == "run_second_refinement.py":
            shutil.copy2(source.parent / "run_first_refinement.py", destination.parent)
        if script_name in _CONTEXT_REFINEMENT_SCRIPTS:
            shutil.copy2(
                source.parent / "run_nominal_calculation.py",
                destination.parent,
            )
        if script_name == "run_refinement_02.py":
            shutil.copy2(source.parent / "run_refinement_01.py", destination.parent)
        if relative_path.startswith("band-equivalence-dimensional-comparison/"):
            for definition_script in _LOCALITY_DEFINITION_SCRIPTS:
                dependency = source_calculations / definition_script
                copied = temporary_calculations / definition_script
                copied.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dependency, copied)

        monkeypatch.syspath_prepend(str(destination.parent))
        namespace = runpy.run_path(str(destination))
        main = cast(Callable[[], int], namespace["main"])
        script_globals = main.__globals__

        if not _is_strain_context(relative_path) and not relative_path.startswith(
            "band-equivalence-dimensional-comparison/"
        ):
            nominal = cast(
                BandEquivalenceHoppingLocalityRequest,
                script_globals["DEFINITION"],
            )
            bounded_definition = replace(
                nominal,
                construction_size=4,
                evaluation_size=9,
            )
            script_globals["DEFINITION"] = bounded_definition
            for module_name in ("run_development", "run_nominal_calculation"):
                definition_module = sys.modules.get(module_name)
                if definition_module is not None:
                    definition_module.__dict__["DEFINITION"] = bounded_definition
            if script_name in (
                *_LEGACY_REFINEMENT_SCRIPTS,
                *_CONTEXT_REFINEMENT_SCRIPTS,
            ):
                script_globals["REFINEMENT"] = replace(
                    nominal,
                    construction_size=8,
                    evaluation_size=17,
                )
            if script_name in ("run_second_refinement.py", "run_refinement_02.py"):
                script_globals["FIRST_REFINEMENT"] = replace(
                    nominal,
                    construction_size=8,
                    evaluation_size=17,
                )
                script_globals["REFINEMENT"] = replace(
                    nominal,
                    construction_size=16,
                    evaluation_size=33,
                )
        if _is_strain_context(relative_path):
            script_globals["FRACTIONS"] = (0.0, 0.5, 1.0)
            if "MAXIMUM_TRANSITION_REFINEMENT_DEPTH" in script_globals:
                script_globals["MAXIMUM_TRANSITION_REFINEMENT_DEPTH"] = 1
        if relative_path.startswith("band-equivalence-dimensional-comparison/"):
            original_loader = cast(
                Callable[[Path, int], BandEquivalenceHoppingLocalityRequest],
                script_globals["_load_definition"],
            )
            request_type = cast(
                type[ShellScaleDecisionLandscapeRequest],
                script_globals["ShellScaleDecisionLandscapeRequest"],
            )

            def reduced_loader(
                path: Path, index: int
            ) -> BandEquivalenceHoppingLocalityRequest:
                request = original_loader(path, index)
                construction_size = max(4, request.construction_size // 2)
                return replace(
                    request,
                    construction_size=construction_size,
                    evaluation_size=2 * construction_size + 1,
                )

            def reduced_request(
                *,
                locality_request: BandEquivalenceHoppingLocalityRequest,
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

    return assert_writer
