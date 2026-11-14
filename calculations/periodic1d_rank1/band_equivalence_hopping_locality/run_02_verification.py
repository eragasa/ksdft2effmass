#!/usr/bin/env python3
"""Independently verify one direct rank-one Fourier-locality execution."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from pathlib import Path

from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityCalculationResult,
    Periodic1DFourierLocalityConfiguration,
    Periodic1DFourierLocalityVerifier,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

EXECUTION_ID = "direct-controlled-four-state-n256"
CALCULATION_FAMILY = "periodic1d-rank1-fourier-locality"
script_path = Path(__file__).resolve()
execution_directory = script_path.parent / "executions" / EXECUTION_ID
execution_path = execution_directory / "execution.json"
configuration_path = execution_directory / "inputs" / "configuration.json"
result_path = execution_directory / "results" / "result.json"
verification_directory = execution_directory / "verification"
temporary_directory = execution_directory / ".verification.incomplete"
if verification_directory.exists() or temporary_directory.exists():
    raise FileExistsError("refusing to overwrite Fourier-locality verification")
if not all(
    path.is_file() for path in (execution_path, configuration_path, result_path)
):
    raise FileNotFoundError("the declared Fourier-locality execution is incomplete")
codec = TypedJsonValueCodec()
execution = codec.deserialize_bytes(execution_path.read_bytes())
if not isinstance(execution, Mapping):
    raise TypeError("execution document must decode to a mapping")
if execution.get("execution_id") != EXECUTION_ID:
    raise ValueError("execution identifier does not match")
if execution.get("calculation_family") != CALCULATION_FAMILY:
    raise ValueError("calculation family does not match")
if execution.get("parent_identity") != (
    "ksdft2effmass.periodic1d.controlled-four-state-parent.v1"
):
    raise ValueError("parent identity does not match")
configuration_bytes = configuration_path.read_bytes()
result_bytes = result_path.read_bytes()
if (
    execution.get("configuration_sha256")
    != hashlib.sha256(configuration_bytes).hexdigest()
):
    raise ValueError("configuration bytes do not match execution.json")
if execution.get("result_sha256") != hashlib.sha256(result_bytes).hexdigest():
    raise ValueError("result bytes do not match execution.json")
configuration = Periodic1DFourierLocalityConfiguration.from_json(configuration_bytes)
result = Periodic1DFourierLocalityCalculationResult.from_json(result_bytes)
if configuration.to_json() != configuration_bytes or result.to_json() != result_bytes:
    raise ValueError("calculation artifacts are not canonical typed JSON")
if result.configuration.to_json() != configuration_bytes:
    raise ValueError("configuration and result configuration differ")
if result.configuration.parent_identity != execution.get("parent_identity"):
    raise ValueError("result and execution parent identities differ")
verified = Periodic1DFourierLocalityVerifier(result_wire=result_bytes).result()
temporary_directory.mkdir()
(temporary_directory / "verification.json").write_bytes(
    codec.serialize_bytes(
        {
            "schema_version": 1,
            "schema": (
                "ksdft2effmass.periodic1d-fourier-locality-verification.direct.v1"
            ),
            "calculation_family": CALCULATION_FAMILY,
            "parent_identity": result.configuration.parent_identity,
            "execution_id": EXECUTION_ID,
            "verification": verified.verification,
            "visualization_data": verified.visualization_data,
            "comparison_count": len(verified.verification.checks),
            "result_sha256": hashlib.sha256(result_bytes).hexdigest(),
            "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
            "claim_boundary": (
                "Independent finite numerical verification only; not continuum "
                "isolation, uncertainty quantification, material validation, "
                "publication acceptance, or evidence sealing."
            ),
        }
    )
)
temporary_directory.rename(verification_directory)
if not verified.verification.passed:
    raise ValueError("Fourier-locality independent verification failed")
