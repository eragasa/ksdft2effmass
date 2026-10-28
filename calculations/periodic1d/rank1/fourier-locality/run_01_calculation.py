#!/usr/bin/env python3
"""Calculate one direct controlled rank-one Fourier-locality execution."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path

from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityAnalyzer,
    Periodic1DFourierLocalityCalculationResult,
    Periodic1DFourierLocalityConfiguration,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

EXECUTION_ID = "direct-controlled-four-state-n256"
CALCULATION_FAMILY = "periodic1d-rank1-fourier-locality"
configuration = Periodic1DFourierLocalityConfiguration(
    parent_identity=("ksdft2effmass.periodic1d.controlled-four-state-parent.v1"),
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
    construction_mesh_sizes=(32, 64, 128, 256),
    production_construction_size=256,
    evaluation_size=1025,
    evaluation_shift_numerator=1,
    evaluation_shift_denominator=257,
    maximum_ranges=tuple(range(16)),
    sampled_gap_threshold=0.25,
    energy_absolute_tolerance=1.0e-12,
    relative_tolerance=1.0e-12,
    squared_energy_absolute_tolerance=1.0e-12,
    dimensionless_absolute_tolerance=1.0e-12,
    refinement_tolerance=1.0e-10,
    application_threshold=1.0e-8,
)
script_path = Path(__file__).resolve()
execution_directory = script_path.parent / "executions" / EXECUTION_ID
temporary_directory = execution_directory.with_name(f".{EXECUTION_ID}.incomplete")
if execution_directory.exists() or temporary_directory.exists():
    raise FileExistsError("refusing to overwrite a Fourier-locality execution")
result = Periodic1DFourierLocalityAnalyzer().execute(configuration)
configuration_bytes = configuration.to_json()
result_bytes = result.to_json()
if (
    Periodic1DFourierLocalityConfiguration.from_json(configuration_bytes).to_json()
    != configuration_bytes
):
    raise ValueError("configuration failed canonical typed admission")
if (
    Periodic1DFourierLocalityCalculationResult.from_json(result_bytes).to_json()
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
            "claim_boundary": (
                "Finite sampled four-state parent, Fourier, fit, refinement, and gap "
                "diagnostics only; not continuum isolation, uncertainty "
                "quantification, "
                "material validation, publication acceptance, or sealed evidence."
            ),
            "sealed": False,
        }
    )
)
(temporary_directory / "UNSEALED.md").write_text(
    "# Unsealed Fourier-locality execution\n\n"
    "This is an illustrative finite numerical control, not sealed evidence.\n",
    encoding="utf-8",
)
temporary_directory.rename(execution_directory)
