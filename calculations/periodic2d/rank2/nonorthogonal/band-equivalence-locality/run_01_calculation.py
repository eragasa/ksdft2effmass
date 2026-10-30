#!/usr/bin/env python3
"""Calculate one direct nonorthogonal periodic-2D rank-two locality execution."""

from __future__ import annotations

import hashlib
import math
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path

import numpy as np
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.analysis import (
    BandEquivalenceLocalityAnalyzer,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.definitions import (
    FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
    BandEquivalenceLocalityCase,
    BandEquivalenceLocalityFamilyEnum,
    BandEquivalenceLocalityRequest,
    GaugeNormalizationEnum,
    ParentEnum,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.lifecycle import (
    BandEquivalenceLocalityExecution,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.result import (
    BandEquivalenceLocalityAnalysisRecorder,
    BandEquivalenceLocalityCalculationResult,
)
from projectkoios.physkit.periodic.lattice import DirectLattice2D, DirectLatticeMetric

EXECUTION_ID = "direct-triangular-honeycomb-rank2-n16"
CALCULATION_FAMILY = "periodic2d-rank2-nonorthogonal-band-equivalence-locality"
SQUARE_METRIC = DirectLatticeMetric(
    DirectLattice2D(
        a1=np.array((1.0, 0.0), dtype=np.float64),
        a2=np.array((0.0, 1.0), dtype=np.float64),
    )
)
TRIANGULAR_METRIC = DirectLatticeMetric(
    DirectLattice2D(
        a1=np.array((1.0, 0.0), dtype=np.float64),
        a2=np.array((0.5, math.sqrt(3.0) / 2.0), dtype=np.float64),
    )
)
SQUARE_BONDS = ((1, 0), (0, 1))
TRIANGULAR_BONDS = ((1, 0), (0, 1), (1, -1))
MAXIMUM_AMPLITUDE = math.pi / (4.0 * math.sqrt(6.0))
configuration = BandEquivalenceLocalityRequest(
    family=BandEquivalenceLocalityFamilyEnum.GRAPHENE_INSPIRED,
    cases=(
        BandEquivalenceLocalityCase(
            name="matched-square-bravais-control",
            dimension=2,
            parent_kind=ParentEnum.HERMITIAN_BRAVAIS,
            gauge_normalization=GaugeNormalizationEnum.BOND_RMS,
            positive_bonds=SQUARE_BONDS,
            direct_metric=SQUARE_METRIC,
            shell_metric_scale=1.0,
        ),
        BandEquivalenceLocalityCase(
            name="triangular-bravais-control",
            dimension=2,
            parent_kind=ParentEnum.HERMITIAN_BRAVAIS,
            gauge_normalization=GaugeNormalizationEnum.BOND_RMS,
            positive_bonds=TRIANGULAR_BONDS,
            direct_metric=TRIANGULAR_METRIC,
            shell_metric_scale=1.0,
        ),
        BandEquivalenceLocalityCase(
            name="graphene-inspired-honeycomb",
            dimension=2,
            parent_kind=ParentEnum.BIPARTITE_INSPIRED,
            gauge_normalization=GaugeNormalizationEnum.BOND_RMS,
            positive_bonds=TRIANGULAR_BONDS,
            direct_metric=TRIANGULAR_METRIC,
            shell_metric_scale=1.0,
            basis_offsets=((0.0, 0.0), (1.0 / 3.0, 1.0 / 3.0)),
        ),
    ),
    synthetic_model=FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
    construction_size=16,
    evaluation_size=33,
    evaluation_shift=1.0 / 3.0,
    parent_scales=(0.0, 1.0),
    amplitudes=(0.0, MAXIMUM_AMPLITUDE / 2.0, MAXIMUM_AMPLITUDE),
    band_tolerances=(1.0e-3, 1.0e-5),
    shell_cap=21,
)
script_path = Path(__file__).resolve()
execution_directory = script_path.parent / "executions" / EXECUTION_ID
temporary_directory = execution_directory.with_name(f".{EXECUTION_ID}.incomplete")
if execution_directory.exists() or temporary_directory.exists():
    raise FileExistsError(
        "refusing to overwrite a nonorthogonal periodic-2D locality execution"
    )
analysis = BandEquivalenceLocalityAnalyzer(request=configuration).execute()
result = BandEquivalenceLocalityAnalysisRecorder(analysis).result()
configuration_bytes = configuration.to_json()
result_bytes = result.to_json()
if BandEquivalenceLocalityRequest.from_json(configuration_bytes).to_json() != (
    configuration_bytes
):
    raise ValueError("configuration failed canonical typed admission")
if BandEquivalenceLocalityCalculationResult.from_json(result_bytes).to_json() != (
    result_bytes
):
    raise ValueError("result failed canonical typed admission")
(temporary_directory / "inputs").mkdir(parents=True)
(temporary_directory / "results").mkdir()
(temporary_directory / "inputs" / "configuration.json").write_bytes(configuration_bytes)
(temporary_directory / "results" / "result.json").write_bytes(result_bytes)
execution = BandEquivalenceLocalityExecution(
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
        "Finite sampled synthetic matched-square, triangular-Bravais, and "
        "honeycomb-basis controls, rank-two gauge comparison, multidimensional "
        "Fourier interpolation, and complete metric-shell truncation diagnostics "
        "only; not graphene, continuum convergence, uncertainty quantification, "
        "material validation, publication acceptance, or sealed evidence."
    ),
    sealed=False,
)
(temporary_directory / "execution.json").write_bytes(execution.to_json())
(temporary_directory / "UNSEALED.md").write_text(
    "# Unsealed nonorthogonal periodic-2D band-equivalence locality execution\n\n"
    "CALCULATED RESULT — UNSEALED. This is not graphene or sealed scientific "
    "evidence.\n",
    encoding="utf-8",
)
temporary_directory.rename(execution_directory)
