#!/usr/bin/env python3
"""Calculate one direct nonorthogonal periodic-3D rank-two locality execution."""

from __future__ import annotations

import hashlib
import math
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path

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
from projectkoios.physkit.periodic.lattice import (
    BravaisLattice,
    DirectLattice3D,
    DirectLatticeMetric,
)

EXECUTION_ID = "direct-fcc-diamond-rank2-n8"
CALCULATION_FAMILY = "periodic3d-rank2-nonorthogonal-band-equivalence-locality"
SIMPLE_CUBIC_METRIC = DirectLatticeMetric(
    DirectLattice3D.from_lattice_parameters(
        a=math.sqrt(0.5),
        b=math.sqrt(0.5),
        c=math.sqrt(0.5),
        alpha_degrees=90.0,
        beta_degrees=90.0,
        gamma_degrees=90.0,
    )
)
FCC_METRIC = DirectLatticeMetric(BravaisLattice.cubic_face_centered().direct_lattice)
SIMPLE_CUBIC_BONDS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
FCC_BONDS = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (-1, 1, 0),
    (-1, 0, 1),
    (0, -1, 1),
)
MAXIMUM_AMPLITUDE = math.pi / (4.0 * math.sqrt(12.0))
configuration = BandEquivalenceLocalityRequest(
    family=BandEquivalenceLocalityFamilyEnum.SILICON_INSPIRED,
    synthetic_model=FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
    cases=(
        BandEquivalenceLocalityCase(
            name="matched-simple-cubic-bravais-control",
            dimension=3,
            parent_kind=ParentEnum.HERMITIAN_BRAVAIS,
            gauge_normalization=GaugeNormalizationEnum.BOND_RMS,
            positive_bonds=SIMPLE_CUBIC_BONDS,
            direct_metric=SIMPLE_CUBIC_METRIC,
            shell_metric_scale=2.0,
        ),
        BandEquivalenceLocalityCase(
            name="fcc-bravais-control",
            dimension=3,
            parent_kind=ParentEnum.HERMITIAN_BRAVAIS,
            gauge_normalization=GaugeNormalizationEnum.BOND_RMS,
            positive_bonds=FCC_BONDS,
            direct_metric=FCC_METRIC,
            shell_metric_scale=2.0,
        ),
        BandEquivalenceLocalityCase(
            name="silicon-inspired-diamond",
            dimension=3,
            parent_kind=ParentEnum.BIPARTITE_INSPIRED,
            gauge_normalization=GaugeNormalizationEnum.BOND_RMS,
            positive_bonds=FCC_BONDS,
            direct_metric=FCC_METRIC,
            shell_metric_scale=2.0,
            basis_offsets=(
                (0.0, 0.0, 0.0),
                (1.0 / 4.0, 1.0 / 4.0, 1.0 / 4.0),
            ),
        ),
    ),
    construction_size=8,
    evaluation_size=17,
    evaluation_shift=1.0 / 3.0,
    parent_scales=(0.0, 1.0),
    amplitudes=(0.0, MAXIMUM_AMPLITUDE / 2.0, MAXIMUM_AMPLITUDE),
    band_tolerances=(1.0e-3, 1.0e-5),
    shell_cap=7,
)
script_path = Path(__file__).resolve()
execution_directory = script_path.parent / "executions" / EXECUTION_ID
temporary_directory = execution_directory.with_name(f".{EXECUTION_ID}.incomplete")
if execution_directory.exists() or temporary_directory.exists():
    raise FileExistsError("refusing to overwrite a periodic-3D nonorthogonal execution")
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
        "Finite sampled synthetic matched-simple-cubic, FCC-Bravais, and "
        "diamond-basis rank-two gauge comparisons with multidimensional "
        "Fourier interpolation and complete metric-shell truncation "
        "diagnostics only; not a silicon calculation, continuum convergence, "
        "uncertainty quantification, material validation, publication "
        "acceptance, or sealed evidence."
    ),
    sealed=False,
)
(temporary_directory / "execution.json").write_bytes(execution.to_json())
(temporary_directory / "UNSEALED.md").write_text(
    "# Unsealed periodic-3D nonorthogonal band-equivalence locality execution\n\n"
    "CALCULATED RESULT — UNSEALED. This synthetic calculation is not silicon "
    "validation or sealed scientific evidence.\n",
    encoding="utf-8",
)
temporary_directory.rename(execution_directory)
