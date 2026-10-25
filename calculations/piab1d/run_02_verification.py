#!/usr/bin/env python3
"""Independently verify one direct PIAB1D execution."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from pathlib import Path

from ksdft2effmass.model_systems.piab1d import Piab1dVerifier
from ksdft2effmass.serialization import SerializableValue, TypedJsonValueCodec

EXECUTION_ID = "direct-core-n8-m3"

script_path = Path(__file__).resolve()
execution_directory = script_path.parent / "executions" / EXECUTION_ID
execution_path = execution_directory / "execution.json"
result_path = execution_directory / "results" / "result.json"
verification_directory = execution_directory / "verification"
temporary_verification_directory = execution_directory / ".verification.incomplete"
verification_path = verification_directory / "verification.json"
if verification_directory.exists():
    raise FileExistsError(f"refusing to overwrite {verification_directory}")
if temporary_verification_directory.exists():
    raise FileExistsError(
        f"incomplete verification stage exists: {temporary_verification_directory}"
    )
if not execution_path.is_file() or not result_path.is_file():
    raise FileNotFoundError("the declared calculation execution is incomplete")

codec = TypedJsonValueCodec()
execution = codec.deserialize_bytes(execution_path.read_bytes())
result = codec.deserialize_bytes(result_path.read_bytes())
if not isinstance(execution, Mapping) or not isinstance(result, Mapping):
    raise TypeError("execution and result documents must decode to mappings")
if execution.get("execution_id") != EXECUTION_ID:
    raise ValueError("execution identity does not match the verification target")
if execution.get("outcome") != "completed":
    raise ValueError("verification requires a completed calculation execution")
if execution.get("result_path") != "results/result.json":
    raise ValueError("execution declares an unexpected result path")
if result.get("execution_id") != EXECUTION_ID:
    raise ValueError("result identity does not match the verification target")
if result.get("calculation_family") != "piab1d-spectral-reduction":
    raise ValueError("result declares an unexpected calculation family")
result_sha256 = hashlib.sha256(result_path.read_bytes()).hexdigest()
if execution.get("result_sha256") != result_sha256:
    raise ValueError("result bytes do not match execution.json")

verification_result = Piab1dVerifier(
    result=result,
    subject_sha256=result_sha256,
).result()
verification = verification_result.verification
verification_document: dict[str, SerializableValue] = {
    "schema_version": 1,
    "calculation_family": "piab1d-spectral-reduction",
    "execution_id": EXECUTION_ID,
    "verification_route": (
        "independent NumPy construction from the declared centered-difference "
        "Dirichlet formulas"
    ),
    "verification": verification,
    "visualization_data": verification_result.visualization_data,
    "claim_boundary": (
        "Software and finite-dimensional numerical verification only; not physical "
        "validation or publication acceptance."
    ),
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
    raise ValueError("PIAB1D verification failed: " + ", ".join(failed))
