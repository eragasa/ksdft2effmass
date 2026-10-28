#!/usr/bin/env python3
"""Calculate one direct Mathieu1D finite-reduction execution."""

from __future__ import annotations

import hashlib
import inspect
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from ksdft2effmass.model_systems.mathieu1d import (
    Mathieu1dAnalyzer,
    Mathieu1dCalculationResult,
    Mathieu1dConfiguration,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

EXECUTION_ID = "direct-finite-reduction-n64"
CALCULATION_FAMILY = "mathieu1d-finite-reduction"
EVIDENCE_STATUS = "illustrative numerical experiment"
CLAIM_BOUNDARY = (
    "Calculated finite plane-wave, finite-difference, reciprocal-mesh, and "
    "finite-range values for Mathieu1D; not continuum convergence, uncertainty "
    "quantification, material validation, publication acceptance, or sealed evidence."
)
configuration = Mathieu1dConfiguration(
    period=float(2.0 * np.pi),
    reciprocal_vector=1.0,
    recoil_energy=1.0,
    constant_coefficient=0.0,
    cosine_amplitude=0.5,
    duality_absolute_tolerance=1.0e-14,
    plane_wave_cutoffs=(3, 5, 7, 9, 11),
    plane_wave_reference_cutoff=15,
    production_plane_wave_cutoff=11,
    finite_difference_points=(31, 63, 127, 255),
    parent_reduced_momenta=(-0.5, -0.25, 0.0, 0.25, 0.5),
    compared_band_count=3,
    selected_band_index=0,
    reciprocal_training_mesh_size=64,
    evaluation_reduced_momenta=tuple(
        float(-0.5 + (index + 1.0 / 65.0) / 257.0) for index in range(257)
    ),
    hopping_ranges=(0, 1, 2, 3, 4, 6, 8),
    fitting_weights=(1.0,) * 64,
    coordinate_absolute_tolerance=1.0e-14,
    reconstruction_absolute_tolerance=1.0e-12,
    hermiticity_absolute_tolerance=1.0e-12,
    parseval_absolute_tolerance=1.0e-12,
    imaginary_absolute_tolerance=1.0e-12,
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

git_head_process = subprocess.run(
    ("git", "-C", str(repository_root), "rev-parse", "HEAD"),
    check=False,
    capture_output=True,
    text=True,
)
git_status_process = subprocess.run(
    (
        "git",
        "-C",
        str(repository_root),
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    ),
    check=False,
    capture_output=True,
    text=True,
)
git_available = git_head_process.returncode == 0 and git_status_process.returncode == 0
if git_available:
    git_head = git_head_process.stdout.strip()
    git_status_bytes = git_status_process.stdout.encode("utf-8")
    git_worktree_state = "dirty" if git_status_bytes else "clean"
else:
    git_head = "unavailable-non-git-copy"
    git_status_bytes = b""
    git_worktree_state = "unavailable"

result = Mathieu1dAnalyzer().calculate(
    configuration,
    calculation_family=CALCULATION_FAMILY,
    execution_id=EXECUTION_ID,
    evidence_status=EVIDENCE_STATUS,
    claim_boundary=CLAIM_BOUNDARY,
)
configuration_bytes = configuration.to_json()
result_bytes = result.to_json()
if Mathieu1dConfiguration.from_json(configuration_bytes).to_json() != (
    configuration_bytes
):
    raise ValueError("configuration failed canonical typed round-trip admission")
if Mathieu1dCalculationResult.from_json(result_bytes).to_json() != result_bytes:
    raise ValueError("result failed canonical typed round-trip admission")
configuration_sha256 = hashlib.sha256(configuration_bytes).hexdigest()
result_sha256 = hashlib.sha256(result_bytes).hexdigest()
analyzer_source_path = Path(inspect.getfile(Mathieu1dAnalyzer)).resolve()
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
    "configuration_schema": "ksdft2effmass.mathieu1d-configuration.direct.v1",
    "result_path": "results/result.json",
    "result_sha256": result_sha256,
    "result_schema": "ksdft2effmass.mathieu1d-calculation-result.direct.v1",
    "plane_wave_route": (
        "ksdft2effmass.model_systems.periodic_1d.PlaneWaveFiberHamiltonian1DConstructor"
    ),
    "finite_difference_route": (
        "ksdft2effmass.model_systems.periodic_1d."
        "PeriodicFiniteDifferenceFiberHamiltonian1DConstructor"
    ),
    "hopping_transform_route": (
        "ksdft2effmass.solidstate.ReciprocalOperatorFourierTransformer1D"
    ),
    "hopping_fit_route": (
        "ksdft2effmass.analysis.hopping_fits.BlockHoppingLeastSquaresFitter1D"
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
    "repository": {
        "git_available": git_available,
        "git_head": git_head,
        "git_worktree_state": git_worktree_state,
        "git_status_sha256": hashlib.sha256(git_status_bytes).hexdigest(),
    },
    "claim_boundary": CLAIM_BOUNDARY,
    "sealed": False,
}
(temporary_directory / "execution.json").write_bytes(
    TypedJsonValueCodec().serialize_bytes(execution)
)
(temporary_directory / "UNSEALED.md").write_text(
    "# Unsealed Mathieu1D direct execution\n\n"
    "This retained execution is an illustrative local finite numerical calculation. "
    "It has independent software and numerical verification and authenticated "
    "rendering, but it is not a sealed evidence package, publication acceptance, "
    "continuum convergence, uncertainty quantification, or material validation.\n",
    encoding="utf-8",
)
temporary_directory.rename(execution_directory)
