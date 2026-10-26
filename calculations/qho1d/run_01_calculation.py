#!/usr/bin/env python3
"""Calculate one direct QHO1D spatial-truncation execution."""

from __future__ import annotations

import hashlib
import inspect
import platform
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from ksdft2effmass.model_systems.qho1d import Qho1dAnalyzer, Qho1dConfiguration
from ksdft2effmass.serialization import TypedJsonValueCodec

# Authored scientific configuration. JSON is an output representation, not an input.
EXECUTION_ID = "direct-spatial-truncation-3x3x3-physkit-norms"
CALCULATION_FAMILY = "qho1d-spatial-truncation"
EVIDENCE_STATUS = "illustrative numerical experiment"
CLAIM_BOUNDARY = (
    "Calculated finite-dimensional spatial-truncation comparison; not continuum "
    "convergence evidence, physical uncertainty quantification, semiconductor "
    "validation, publication acceptance, or a sealed evidence package."
)
configuration = Qho1dConfiguration(
    hbar=1.0,
    mass=1.0,
    omega=1.0,
    box_half_widths=(4.0, 6.0, 8.0),
    grid_spacings=(0.2, 0.1, 0.05),
    retained_dimensions=(2, 4, 6),
    selected_box_half_width=8.0,
    selected_grid_spacing=0.05,
    selected_retained_dimension=6,
    displayed_states=4,
)

script_path = Path(__file__).resolve()
repository_root = script_path.parents[2]
calculation_directory = script_path.parent
execution_directory = calculation_directory / "executions" / EXECUTION_ID
temporary_directory = execution_directory.with_name(f".{EXECUTION_ID}.incomplete")
if execution_directory.exists():
    raise FileExistsError(f"refusing to overwrite {execution_directory}")
if temporary_directory.exists():
    raise FileExistsError(f"refusing to overwrite {temporary_directory}")

analyzer = Qho1dAnalyzer()
result = analyzer.execute(
    configuration,
    calculation_family=CALCULATION_FAMILY,
    execution_id=EXECUTION_ID,
    evidence_status=EVIDENCE_STATUS,
    claim_boundary=CLAIM_BOUNDARY,
)
configuration_bytes = configuration.to_json()
result_bytes = result.to_json()
configuration_sha256 = hashlib.sha256(configuration_bytes).hexdigest()
result_sha256 = hashlib.sha256(result_bytes).hexdigest()
analyzer_source_path = Path(inspect.getfile(Qho1dAnalyzer)).resolve()
try:
    analyzer_source_locator = analyzer_source_path.relative_to(
        repository_root
    ).as_posix()
except ValueError:
    analyzer_source_locator = analyzer_source_path.as_posix()

(temporary_directory / "inputs").mkdir(parents=True)
(temporary_directory / "results").mkdir()
(temporary_directory / "inputs" / "configuration.json").write_bytes(configuration_bytes)
(temporary_directory / "results" / "result.json").write_bytes(result_bytes)
codec = TypedJsonValueCodec()
execution = {
    "schema_version": 1,
    "calculation_family": CALCULATION_FAMILY,
    "execution_id": EXECUTION_ID,
    "execution_kind": "local deterministic Python calculation",
    "created_utc": datetime.now(UTC).isoformat(),
    "outcome": "completed",
    "evidence_status": EVIDENCE_STATUS,
    "configuration_path": "inputs/configuration.json",
    "configuration_sha256": configuration_sha256,
    "result_path": "results/result.json",
    "result_sha256": result_sha256,
    "result_schema": "ksdft2effmass.qho1d-calculation-result.sections.v1",
    "matrix_norm_route": (
        "projectkoios.physkit.linalg.matrix.norm.FrobeniusMatrixNorm"
    ),
    "script_path": script_path.relative_to(repository_root).as_posix(),
    "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
    "analyzer_source_path": analyzer_source_locator,
    "analyzer_source_sha256": hashlib.sha256(
        analyzer_source_path.read_bytes()
    ).hexdigest(),
    "runtime": {
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
    },
    "claim_boundary": CLAIM_BOUNDARY,
    "sealed": False,
}
(temporary_directory / "execution.json").write_bytes(codec.serialize_bytes(execution))
temporary_directory.rename(execution_directory)
