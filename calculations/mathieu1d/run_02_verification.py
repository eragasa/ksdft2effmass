#!/usr/bin/env python3
"""Independently verify one direct Mathieu1D finite-reduction execution."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from pathlib import Path

from ksdft2effmass.model_systems.mathieu1d import (
    Mathieu1dCalculationResult,
    Mathieu1dConfiguration,
    Mathieu1dVerifier,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

EXECUTION_ID = "direct-finite-reduction-n64"
CALCULATION_FAMILY = "mathieu1d-finite-reduction"
EVIDENCE_STATUS = "illustrative numerical experiment"
CLAIM_BOUNDARY = (
    "Independent software and finite numerical verification only; not continuum "
    "convergence, uncertainty quantification, material validation, publication "
    "acceptance, or evidence sealing."
)

script_path = Path(__file__).resolve()
execution_directory = script_path.parent / "executions" / EXECUTION_ID
execution_path = execution_directory / "execution.json"
configuration_path = execution_directory / "inputs" / "configuration.json"
result_path = execution_directory / "results" / "result.json"
verification_directory = execution_directory / "verification"
temporary_verification_directory = execution_directory / ".verification.incomplete"
if verification_directory.exists():
    raise FileExistsError(f"refusing to overwrite {verification_directory}")
if temporary_verification_directory.exists():
    raise FileExistsError(
        f"incomplete verification stage exists: {temporary_verification_directory}"
    )
if (
    not execution_path.is_file()
    or not configuration_path.is_file()
    or not result_path.is_file()
):
    raise FileNotFoundError(
        "the declared Mathieu1D calculation execution is incomplete"
    )

codec = TypedJsonValueCodec()
execution = codec.deserialize_bytes(execution_path.read_bytes())
if not isinstance(execution, Mapping):
    raise TypeError("execution document must decode to a mapping")
if execution.get("execution_id") != EXECUTION_ID:
    raise ValueError("execution identifier does not match the verification target")
if execution.get("calculation_family") != CALCULATION_FAMILY:
    raise ValueError("execution declares an unexpected calculation family")
if execution.get("outcome") != "completed":
    raise ValueError("verification requires a completed calculation execution")
if execution.get("evidence_status") != EVIDENCE_STATUS:
    raise ValueError("execution declares an unexpected evidence status")
if execution.get("configuration_path") != "inputs/configuration.json":
    raise ValueError("execution declares an unexpected configuration path")
if execution.get("configuration_schema") != (
    "ksdft2effmass.mathieu1d-configuration.direct.v1"
):
    raise ValueError("execution declares an unexpected configuration schema")
if execution.get("result_path") != "results/result.json":
    raise ValueError("execution declares an unexpected result path")
if execution.get("result_schema") != (
    "ksdft2effmass.mathieu1d-calculation-result.direct.v1"
):
    raise ValueError("execution declares an unexpected result schema")
if execution.get("plane_wave_route") != (
    "ksdft2effmass.model_systems.periodic_1d.PlaneWaveFiberHamiltonian1DConstructor"
):
    raise ValueError("execution declares an unexpected plane-wave route")
if execution.get("finite_difference_route") != (
    "ksdft2effmass.model_systems.periodic_1d."
    "PeriodicFiniteDifferenceFiberHamiltonian1DConstructor"
):
    raise ValueError("execution declares an unexpected finite-difference route")
if execution.get("hopping_transform_route") != (
    "ksdft2effmass.solidstate.ReciprocalOperatorFourierTransformer1D"
):
    raise ValueError("execution declares an unexpected hopping-transform route")
if execution.get("hopping_fit_route") != (
    "ksdft2effmass.analysis.hopping_fits.BlockHoppingLeastSquaresFitter1D"
):
    raise ValueError("execution declares an unexpected hopping-fit route")
configuration_bytes = configuration_path.read_bytes()
configuration_sha256 = hashlib.sha256(configuration_bytes).hexdigest()
if execution.get("configuration_sha256") != configuration_sha256:
    raise ValueError("configuration bytes do not match execution.json")
result_bytes = result_path.read_bytes()
result_sha256 = hashlib.sha256(result_bytes).hexdigest()
if execution.get("result_sha256") != result_sha256:
    raise ValueError("result bytes do not match execution.json")
configuration = Mathieu1dConfiguration.from_json(configuration_bytes)
result = Mathieu1dCalculationResult.from_json(result_bytes)
if configuration.to_json() != configuration_bytes:
    raise ValueError("configuration bytes are not canonical typed JSON")
if result.to_json() != result_bytes:
    raise ValueError("result bytes are not canonical typed JSON")
if result.configuration.to_json() != configuration_bytes:
    raise ValueError("configuration and result configuration do not match")
if result.calculation_family != CALCULATION_FAMILY:
    raise ValueError("result declares an unexpected calculation family")
if result.execution_id != EXECUTION_ID:
    raise ValueError("result declares an unexpected execution identifier")
if result.evidence_status != EVIDENCE_STATUS:
    raise ValueError("result declares an unexpected evidence status")
if result.claim_boundary != execution.get("claim_boundary"):
    raise ValueError("result and execution claim boundaries do not match")

verification_result = Mathieu1dVerifier(result_wire=result_bytes).result()
verification = verification_result.verification
verification_document = {
    "schema_version": 1,
    "schema": "ksdft2effmass.mathieu1d-verification.direct.v1",
    "calculation_family": CALCULATION_FAMILY,
    "execution_id": EXECUTION_ID,
    "evidence_status": EVIDENCE_STATUS,
    "verification_route": (
        "independent direct assembly of dense plane-wave fibers and sparse twisted "
        "finite-difference fibers, explicit finite Fourier sums, and NumPy weighted "
        "least squares without production analyzers or historical workflows"
    ),
    "verification": verification,
    "visualization_data": verification_result.visualization_data,
    "comparison_count": len(verification.checks),
    "claim_boundary": CLAIM_BOUNDARY,
    "result_sha256": result_sha256,
    "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
}
temporary_verification_directory.mkdir()
(temporary_verification_directory / "verification.json").write_bytes(
    codec.serialize_bytes(verification_document)
)
temporary_verification_directory.rename(verification_directory)
if not verification.passed:
    failed = [
        name
        for name, value in verification.checks.items()
        if value > verification.check_tolerances[name]
    ]
    raise ValueError("Mathieu1D verification failed: " + ", ".join(failed))
