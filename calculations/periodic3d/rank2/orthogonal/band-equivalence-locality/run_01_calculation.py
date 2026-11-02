#!/usr/bin/env python3
"""Calculate one direct orthogonal periodic-3D rank-two locality execution."""

from __future__ import annotations

import hashlib
import math
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path

from projectkoios.physkit.periodic.lattice import BravaisLattice, DirectLatticeMetric

from ksdft2effmass.band_equivalence_hopping_locality.definitions import (
    FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
    BandEquivalenceHoppingLocalityCase,
    BandEquivalenceHoppingLocalityFamilyEnum,
    GaugeNormalizationEnum,
    ParentEnum,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.analysis import (
    Periodic3DRank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.lifecycle import (
    Periodic3DRank2BandEquivalenceHoppingLocalityExecution,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.request import (
    Periodic3DRank2BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.result import (
    Periodic3DRank2BandEquivalenceHoppingLocalityAnalysisRecorder,
    Periodic3DRank2BandEquivalenceHoppingLocalityCalculationResult,
)

EXECUTION_ID = "direct-simple-cubic-rank2-n8"
CALCULATION_FAMILY = "periodic3d-rank2-orthogonal-band-equivalence-locality"
configuration = Periodic3DRank2BandEquivalenceHoppingLocalityRequest(
    family=BandEquivalenceHoppingLocalityFamilyEnum.SIMPLE_CUBIC,
    cases=(
        BandEquivalenceHoppingLocalityCase(
            name="simple-cubic-directed-parent",
            dimension=3,
            parent_kind=ParentEnum.DIRECTED_AXIS,
            gauge_normalization=GaugeNormalizationEnum.AXIS_MAXIMUM,
            positive_bonds=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            direct_metric=DirectLatticeMetric(
                BravaisLattice.cubic_primitive().direct_lattice
            ),
            shell_metric_scale=1.0,
        ),
    ),
    synthetic_model=FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
    construction_size=8,
    evaluation_size=17,
    evaluation_shift=1.0 / 3.0,
    parent_scales=(0.0, 1.0),
    amplitudes=(0.0, math.pi / 8.0, math.pi / 4.0),
    band_tolerances=(1.0e-3, 1.0e-5),
    shell_cap=9,
)
script_path = Path(__file__).resolve()
execution_directory = script_path.parent / "executions" / EXECUTION_ID
temporary_directory = execution_directory.with_name(f".{EXECUTION_ID}.incomplete")
if execution_directory.exists() or temporary_directory.exists():
    raise FileExistsError("refusing to overwrite a periodic-3D locality execution")
analysis = Periodic3DRank2BandEquivalenceHoppingLocalityAnalyzer(
    request=configuration
).execute()
result = Periodic3DRank2BandEquivalenceHoppingLocalityAnalysisRecorder(analysis).result()
configuration_bytes = configuration.to_json()
result_bytes = result.to_json()
if Periodic3DRank2BandEquivalenceHoppingLocalityRequest.from_json(
    configuration_bytes
).to_json() != (configuration_bytes):
    raise ValueError("configuration failed canonical typed admission")
if Periodic3DRank2BandEquivalenceHoppingLocalityCalculationResult.from_json(
    result_bytes
).to_json() != (result_bytes):
    raise ValueError("result failed canonical typed admission")
(temporary_directory / "inputs").mkdir(parents=True)
(temporary_directory / "results").mkdir()
(temporary_directory / "inputs" / "configuration.json").write_bytes(configuration_bytes)
(temporary_directory / "results" / "result.json").write_bytes(result_bytes)
execution = Periodic3DRank2BandEquivalenceHoppingLocalityExecution(
    schema_version=1,
    calculation_family=CALCULATION_FAMILY,
    study_family=configuration.family.to_wire(),
    execution_id=EXECUTION_ID,
    created_utc=datetime.now(UTC).isoformat(),
    outcome="completed",
    evidence_status="calculated result — unsealed",
    configuration_path="inputs/configuration.json",
    configuration_sha256=hashlib.sha256(configuration_bytes).hexdigest(),
    result_path="results/result.json",
    result_sha256=hashlib.sha256(result_bytes).hexdigest(),
    script_sha256=hashlib.sha256(script_path.read_bytes()).hexdigest(),
    software_versions={
        "ksdft2effmass": version("ksdft2effmass"),
        "numpy": version("numpy"),
        "projectkoios-optimization": version("projectkoios-optimization"),
        "projectkoios-physkit": version("projectkoios-physkit"),
        "scipy": version("scipy"),
    },
    claim_boundary=(
        "Finite sampled synthetic simple-cubic parent, rank-two gauge "
        "comparison, multidimensional Fourier interpolation, and complete "
        "metric-shell truncation diagnostics only; not continuum "
        "convergence, uncertainty quantification, material validation, "
        "publication acceptance, or sealed evidence."
    ),
    sealed=False,
)
(temporary_directory / "execution.json").write_bytes(execution.to_json())
(temporary_directory / "UNSEALED.md").write_text(
    "# Unsealed periodic-3D band-equivalence locality execution\n\n"
    "CALCULATED RESULT — UNSEALED. This is not sealed scientific evidence.\n",
    encoding="utf-8",
)
temporary_directory.rename(execution_directory)
