#!/usr/bin/env python3
"""Calculate one direct controlled rank-two composite-alignment execution."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path

from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)

from ksdft2effmass.periodic1d.rank2.band_alignment.composite import (
    Periodic1DCompositeBandAlignmentAnalyzer,
    Periodic1DCompositeBandAlignmentCalculationResult,
    Periodic1DCompositeBandAlignmentConfiguration,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

EXECUTION_ID = "direct-controlled-rank2-n64"
CALCULATION_FAMILY = "periodic1d-rank2-composite-band-alignment-locality"
configuration = Periodic1DCompositeBandAlignmentConfiguration(
    parent_identity="ksdft2effmass.periodic1d.controlled-four-state-parent.v1",
    onsite_numerators=(
        (-120, 6, 0, 0),
        (6, -35, 0, 0),
        (0, 0, 100, 4),
        (0, 0, 4, 175),
    ),
    positive_hopping_numerators=(
        (15, 0, 12, 0),
        (0, -10, 0, 10),
        (0, 0, 5, 0),
        (0, 0, 0, -4),
    ),
    coefficient_denominator=100,
    retained_rank=2,
    construction_size=64,
    evaluation_size=257,
    evaluation_shift_numerator=1,
    evaluation_shift_denominator=65,
    hopping_ranges=(0, 1, 2, 3, 4, 6, 8),
    attack_constant_angle=0.30,
    attack_sine_coefficients=(0.65, 0.30),
    sampled_gap_threshold=0.5,
    overlap_singular_value_threshold=0.8,
    procrustes_rank_absolute_tolerance=1.0e-14,
    procrustes_rank_relative_tolerance=1.0e-12,
    energy_absolute_tolerance=1.0e-11,
    dimensionless_absolute_tolerance=1.0e-12,
)
script_path = Path(__file__).resolve()
execution_directory = script_path.parent / "executions" / EXECUTION_ID
temporary_directory = execution_directory.with_name(f".{EXECUTION_ID}.incomplete")
if execution_directory.exists() or temporary_directory.exists():
    raise FileExistsError("refusing to overwrite a composite-alignment execution")
result = Periodic1DCompositeBandAlignmentAnalyzer(
    configuration,
    NumpyBatchedComplexUnitaryProcrustesSolver(),
).execute()
configuration_bytes = configuration.to_json()
result_bytes = result.to_json()
if (
    Periodic1DCompositeBandAlignmentConfiguration.from_json(
        configuration_bytes
    ).to_json()
    != configuration_bytes
):
    raise ValueError("configuration failed canonical typed admission")
if (
    Periodic1DCompositeBandAlignmentCalculationResult.from_json(result_bytes).to_json()
    != result_bytes
):
    raise ValueError("result failed canonical typed admission")
(temporary_directory / "inputs").mkdir(parents=True)
(temporary_directory / "results").mkdir()
(temporary_directory / "inputs" / "configuration.json").write_bytes(configuration_bytes)
(temporary_directory / "results" / "result.json").write_bytes(result_bytes)
(temporary_directory / "execution.json").write_bytes(
    TypedJsonValueCodec().serialize_bytes(
        {
            "schema_version": 1,
            "calculation_family": CALCULATION_FAMILY,
            "parent_identity": configuration.parent_identity,
            "execution_id": EXECUTION_ID,
            "created_utc": datetime.now(UTC).isoformat(),
            "outcome": "completed",
            "evidence_status": "illustrative finite numerical control",
            "configuration_path": "inputs/configuration.json",
            "configuration_sha256": hashlib.sha256(configuration_bytes).hexdigest(),
            "result_path": "results/result.json",
            "result_sha256": hashlib.sha256(result_bytes).hexdigest(),
            "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
            "software_versions": {
                "ksdft2effmass": version("ksdft2effmass"),
                "numpy": version("numpy"),
                "projectkoios-optimization": version("projectkoios-optimization"),
                "projectkoios-physkit": version("projectkoios-physkit"),
                "scipy": version("scipy"),
            },
            "claim_boundary": (
                "Finite sampled four-state parent, rank-two frame alignment, block "
                "Fourier transform, and truncation diagnostics only; not continuum "
                "isolation, uncertainty quantification, material validation, "
                "publication acceptance, or sealed evidence."
            ),
            "sealed": False,
        }
    )
)
(temporary_directory / "UNSEALED.md").write_text(
    "# Unsealed composite-band alignment execution\n\n"
    "This is an illustrative finite numerical control, not sealed evidence.\n",
    encoding="utf-8",
)
temporary_directory.rename(execution_directory)
