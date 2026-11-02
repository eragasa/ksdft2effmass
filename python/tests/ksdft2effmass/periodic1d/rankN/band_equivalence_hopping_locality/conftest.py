"""Shared fixtures for higher-rank aggregate-study tests."""

import hashlib
import os
from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.rankN.band_alignment.configuration import (
    Periodic1DRankNAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.request import (
    Periodic1DRankNBandEquivalenceHoppingLocalityControls,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.request import (
    Periodic1DRankNBandEquivalenceHoppingLocalityRequest as StudyRequest,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.result import (
    Periodic1DRankNBandEquivalenceHoppingLocalityAnalysis as StudyAnalysis,
)


@pytest.fixture(scope="session")
def higher_rank_calculation_result(repository_root: Path) -> StudyAnalysis:
    """Read integrity-admitted cache bytes as test data, not scientific evidence."""
    environment_variable = "KSDFT2EFFMASS_PERIODIC1D_RANKN_DEVELOPMENT_CACHE_PATH"
    configured_path = os.environ.get(environment_variable)
    if configured_path is None:
        pytest.skip(
            f"set {environment_variable} to run external-cache software evidence"
        )
    result_path = Path(configured_path)
    result_bytes = result_path.read_bytes()
    assert len(result_bytes) == 4_895_370
    assert hashlib.sha256(result_bytes).hexdigest() == (
        "faf73ba869f60e4cb2f5573151de8679067445286685e94b5699aefa2cafa509"
    )
    return StudyAnalysis.from_json(result_bytes)


@pytest.fixture
def bounded_failure_study_request(
    monkeypatch: pytest.MonkeyPatch,
    higher_rank_calculation_result: StudyAnalysis,
) -> StudyRequest:
    """Return a synthetic reduced-resource request for typed failure-path tests."""
    support_radii = (0, 1, 2, 4, 8)
    monkeypatch.setattr(
        Periodic1DRankNAlignmentConfiguration,
        "EVALUATION_MESH_SIZE",
        129,
    )
    monkeypatch.setattr(
        Periodic1DRankNBandEquivalenceHoppingLocalityControls,
        "SUPPORT_RADII",
        support_radii,
    )
    monkeypatch.setattr(
        Periodic1DRankNBandEquivalenceHoppingLocalityControls,
        "MAXIMUM_RECORDED_BLOCK_RANGE",
        support_radii[-1],
    )
    admitted = higher_rank_calculation_result.request
    configuration = replace(admitted.configuration, evaluation_mesh_size=129)
    controls = replace(
        admitted.controls,
        support_radii=support_radii,
        maximum_recorded_block_range=support_radii[-1],
    )
    return replace(admitted, configuration=configuration, controls=controls)
