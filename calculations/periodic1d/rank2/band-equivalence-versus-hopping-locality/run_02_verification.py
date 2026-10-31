#!/usr/bin/env python3
"""Independently verify one retained embedded rank-two calculation aggregate."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from pathlib import Path

from ksdft2effmass.periodic1d import (
    Periodic1DEmbeddedSubspaceRank2CalculationRecord,
    Periodic1DEmbeddedSubspaceRank2CalculationVerifier,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

EXECUTION_ID = "direct-embedded-rank2-controlled-v2"
CALCULATION_FAMILY = "periodic1d-rank2-band-equivalence-hopping-locality"
CLAIM_BOUNDARY = (
    "Independent bounded finite-route software agreement only; not scientific "
    "validation, evidence sealing, or publication acceptance."
)
SCRIPT_PATH = Path(__file__).resolve()
EXECUTION_DIRECTORY = SCRIPT_PATH.parent / "executions" / EXECUTION_ID
EXECUTION_PATH = EXECUTION_DIRECTORY / "execution.json"
RESULT_PATH = EXECUTION_DIRECTORY / "results" / "calculation.json"
VERIFICATION_DIRECTORY = EXECUTION_DIRECTORY / "verification"
TEMPORARY_DIRECTORY = EXECUTION_DIRECTORY / ".verification.incomplete"

if VERIFICATION_DIRECTORY.exists() or TEMPORARY_DIRECTORY.exists():
    raise FileExistsError("refusing to overwrite band-locality verification")
if not EXECUTION_PATH.is_file() or not RESULT_PATH.is_file():
    raise FileNotFoundError("the declared band-locality execution is incomplete")

codec = TypedJsonValueCodec()
execution_bytes = EXECUTION_PATH.read_bytes()
execution = codec.deserialize_bytes(execution_bytes)
if not isinstance(execution, Mapping):
    raise TypeError("execution document must decode to a mapping")
if codec.serialize_bytes(execution) != execution_bytes:
    raise ValueError("execution document is not canonical typed JSON")
if execution.get("execution_id") != EXECUTION_ID:
    raise ValueError("execution identifier does not match")
if execution.get("calculation_family") != CALCULATION_FAMILY:
    raise ValueError("calculation family does not match")

result_bytes = RESULT_PATH.read_bytes()
if execution.get("result_sha256") != hashlib.sha256(result_bytes).hexdigest():
    raise ValueError("calculation bytes do not match execution.json")
record = Periodic1DEmbeddedSubspaceRank2CalculationRecord.from_json(result_bytes)
if record.to_json() != result_bytes:
    raise ValueError("calculation artifact is not canonical typed JSON")
verification = Periodic1DEmbeddedSubspaceRank2CalculationVerifier(
    result_bytes
).result()
verification_bytes = verification.to_json()
if type(verification).from_json(verification_bytes).to_json() != verification_bytes:
    raise ValueError("verification failed canonical typed admission")

TEMPORARY_DIRECTORY.mkdir()
(TEMPORARY_DIRECTORY / "verification.json").write_bytes(verification_bytes)
(TEMPORARY_DIRECTORY / "manifest.json").write_bytes(
    codec.serialize_bytes(
        {
            "schema_version": 1,
            "calculation_family": CALCULATION_FAMILY,
            "execution_id": EXECUTION_ID,
            "result_sha256": hashlib.sha256(result_bytes).hexdigest(),
            "verification_sha256": hashlib.sha256(verification_bytes).hexdigest(),
            "script_sha256": hashlib.sha256(SCRIPT_PATH.read_bytes()).hexdigest(),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
)
TEMPORARY_DIRECTORY.rename(VERIFICATION_DIRECTORY)
if not verification.passed:
    raise ValueError("band-locality independent verification failed")
