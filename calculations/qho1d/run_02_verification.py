#!/usr/bin/env python3
"""Independently verify one direct QHO1D execution."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from pathlib import Path

from ksdft2effmass.model_systems.qho1d import Qho1dVerifier
from ksdft2effmass.serialization import (
    TypedJsonMappingDeserializer,
    TypedJsonValueCodec,
)

EXECUTION_ID = "direct-spatial-truncation-3x3x3-sections"
CALCULATION_FAMILY = "qho1d-spatial-truncation"

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
if not execution_path.is_file() or not result_path.is_file():
    raise FileNotFoundError("the declared QHO1D calculation execution is incomplete")

codec = TypedJsonValueCodec()
execution = codec.deserialize_bytes(execution_path.read_bytes())
if not isinstance(execution, Mapping):
    raise TypeError("execution document must decode to a mapping")
if execution.get("execution_id") != EXECUTION_ID:
    raise ValueError("execution identity does not match the verification target")
if execution.get("calculation_family") != CALCULATION_FAMILY:
    raise ValueError("execution declares an unexpected calculation family")
if execution.get("outcome") != "completed":
    raise ValueError("verification requires a completed calculation execution")
if execution.get("result_path") != "results/result.json":
    raise ValueError("execution declares an unexpected result path")
if execution.get("result_schema") != (
    "ksdft2effmass.qho1d-calculation-result.sections.v1"
):
    raise ValueError("execution declares an unexpected result schema")
if execution.get("configuration_path") != "inputs/configuration.json":
    raise ValueError("execution declares an unexpected configuration path")
configuration_sha256 = hashlib.sha256(configuration_path.read_bytes()).hexdigest()
if execution.get("configuration_sha256") != configuration_sha256:
    raise ValueError("configuration bytes do not match execution.json")
result_bytes = result_path.read_bytes()
result_sha256 = hashlib.sha256(result_bytes).hexdigest()
if execution.get("result_sha256") != result_sha256:
    raise ValueError("result bytes do not match execution.json")
result = TypedJsonMappingDeserializer().deserialize(result_bytes)
verification_result = Qho1dVerifier(
    result=result,
    subject_sha256=result_sha256,
).result()
verification = verification_result.verification
verification_document = {
    "schema_version": 1,
    "schema": "ksdft2effmass.qho1d-verification.semantic-sections.v1",
    "calculation_family": CALCULATION_FAMILY,
    "execution_id": EXECUTION_ID,
    "verification_route": (
        "independent SciPy Hermite evaluation and direct NumPy construction of "
        "the centered-difference Dirichlet Hamiltonian"
    ),
    "verification": verification,
    "visualization_data": verification_result.visualization_data,
    "comparison_count": len(verification.checks),
    "claim_boundary": (
        "Software and finite-dimensional numerical verification only; not "
        "continuum convergence, physical validation, or publication acceptance."
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
    raise ValueError("QHO1D verification failed: " + ", ".join(failed))
