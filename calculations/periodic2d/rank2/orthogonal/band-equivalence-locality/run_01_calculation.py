#!/usr/bin/env python3
"""Calculate one direct orthogonal periodic-2D rank-two locality execution."""

from __future__ import annotations

import hashlib
import math
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path

import numpy as np
from projectkoios.physkit.periodic.lattice import DirectLattice2D, DirectLatticeMetric

from ksdft2effmass.band_equivalence_hopping_locality.definitions import (
    FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
    BandEquivalenceHoppingLocalityCase,
    BandEquivalenceHoppingLocalityFamilyEnum,
    GaugeNormalizationEnum,
    ParentEnum,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.analysis import (
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.lifecycle import (
    Periodic2DRank2BandEquivalenceHoppingLocalityExecution,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.request import (
    Periodic2DRank2BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.result import (
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalysisRecorder,
    Periodic2DRank2BandEquivalenceHoppingLocalityCalculationResult,
)
from ksdft2effmass.sewing import (
    IdentityReciprocalSewing,
    ReciprocalEndpointSewingInventory,
)

EXECUTION_ID = "direct-square-rank2-n16"
CALCULATION_FAMILY = "periodic2d-rank2-orthogonal-band-equivalence-locality"
identity_reciprocal_sewing = IdentityReciprocalSewing(ambient_dimension=4)
endpoint_sewing = ReciprocalEndpointSewingInventory(
    positive_axis_maps=(
        identity_reciprocal_sewing.endpoint_map,
        identity_reciprocal_sewing.endpoint_map,
    )
)
configuration = Periodic2DRank2BandEquivalenceHoppingLocalityRequest(
    family=BandEquivalenceHoppingLocalityFamilyEnum.SQUARE,
    cases=(
        BandEquivalenceHoppingLocalityCase(
            name="square-directed-parent",
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
    synthetic_model=FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
    construction_size=16,
    evaluation_size=33,
    evaluation_shift=1.0 / 3.0,
    parent_scales=(0.0, 1.0),
    amplitudes=(0.0, math.pi / 8.0, math.pi / 4.0),
    band_tolerances=(1.0e-3, 1.0e-5),
    shell_cap=25,
)
script_path = Path(__file__).resolve()
execution_directory = script_path.parent / "executions" / EXECUTION_ID
temporary_directory = execution_directory.with_name(f".{EXECUTION_ID}.incomplete")
if execution_directory.exists() or temporary_directory.exists():
    raise FileExistsError("refusing to overwrite a periodic-2D locality execution")
analysis = Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer(
    request=configuration,
    endpoint_sewing=endpoint_sewing,
).execute()
result = Periodic2DRank2BandEquivalenceHoppingLocalityAnalysisRecorder(
    analysis
).result()
configuration_bytes = configuration.to_json()
result_bytes = result.to_json()
if Periodic2DRank2BandEquivalenceHoppingLocalityRequest.from_json(
    configuration_bytes
).to_json() != (configuration_bytes):
    raise ValueError("configuration failed canonical typed admission")
if Periodic2DRank2BandEquivalenceHoppingLocalityCalculationResult.from_json(
    result_bytes
).to_json() != (result_bytes):
    raise ValueError("result failed canonical typed admission")
(temporary_directory / "inputs").mkdir(parents=True)
(temporary_directory / "results").mkdir()
(temporary_directory / "inputs" / "configuration.json").write_bytes(configuration_bytes)
(temporary_directory / "results" / "result.json").write_bytes(result_bytes)
execution = Periodic2DRank2BandEquivalenceHoppingLocalityExecution(
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
        "Finite sampled synthetic square-lattice parent, rank-two gauge "
        "comparison, multidimensional Fourier interpolation, and complete "
        "metric-shell truncation diagnostics only; not continuum "
        "convergence, uncertainty quantification, material validation, "
        "publication acceptance, or sealed evidence."
    ),
    sealed=False,
)
(temporary_directory / "execution.json").write_bytes(execution.to_json())
(temporary_directory / "UNSEALED.md").write_text(
    "# Unsealed periodic-2D band-equivalence locality execution\n\n"
    "CALCULATED RESULT — UNSEALED. This is not sealed scientific evidence.\n",
    encoding="utf-8",
)
temporary_directory.rename(execution_directory)
