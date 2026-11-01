#!/usr/bin/env python3
"""Independently verify a retained complete five-scale aggregate."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from pathlib import Path

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.retention.complete_five_scale import (  # noqa: E501
    Periodic1DRank2CompleteFiveScaleCalculationRecord,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.retention.complete_five_scale_verification import (  # noqa: E501
    Periodic1DRank2CompleteFiveScaleVerifier,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

EXECUTION_ID = "direct-embedded-rank2-five-scale-complete-v1"
CALCULATION_FAMILY = "periodic1d-rank2-band-equivalence-hopping-locality"
CLAIM_BOUNDARY = (
    "Independent bounded finite-route software agreement only; not scientific "
    "validation, continuum convergence, evidence sealing, or publication acceptance."
)
SCRIPT_PATH = Path(__file__).resolve()
EXECUTION_DIRECTORY = SCRIPT_PATH.parent / "executions" / EXECUTION_ID
EXECUTION_PATH = EXECUTION_DIRECTORY / "execution.json"
RESULT_PATH = EXECUTION_DIRECTORY / "results" / "calculation.json"
VERIFICATION_DIRECTORY = EXECUTION_DIRECTORY / "verification"
TEMPORARY_DIRECTORY = EXECUTION_DIRECTORY / ".verification.incomplete"

if VERIFICATION_DIRECTORY.exists() or TEMPORARY_DIRECTORY.exists():
    raise FileExistsError("refusing to overwrite complete-five-scale verification")
if not EXECUTION_PATH.is_file() or not RESULT_PATH.is_file():
    raise FileNotFoundError("the declared complete-five-scale execution is incomplete")

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
if execution.get("result_path") != "results/calculation.json":
    raise ValueError("execution result path does not match")
source_worktree_clean = execution.get("source_worktree_clean")
if type(source_worktree_clean) is not bool:
    raise TypeError("source_worktree_clean must be a built-in bool")
if not source_worktree_clean:
    raise ValueError("calculation was not produced from a clean source worktree")
source_revision = execution.get("source_revision")
if type(source_revision) is not str:
    raise TypeError("execution source revision must be a built-in string")
if len(source_revision) not in (40, 64):
    raise ValueError("execution source revision is not a full Git identity")
if any(character not in "0123456789abcdef" for character in source_revision):
    raise ValueError("execution source revision is not lowercase hexadecimal")
sealed = execution.get("sealed")
if type(sealed) is not bool:
    raise TypeError("sealed must be a built-in bool")
if sealed:
    raise ValueError("complete-five-scale candidate must remain unsealed")

result_bytes = RESULT_PATH.read_bytes()
if execution.get("result_sha256") != hashlib.sha256(result_bytes).hexdigest():
    raise ValueError("calculation bytes do not match execution.json")
record = Periodic1DRank2CompleteFiveScaleCalculationRecord.from_json(result_bytes)
if record.to_json() != result_bytes:
    raise ValueError("calculation artifact is not canonical typed JSON")
verification = Periodic1DRank2CompleteFiveScaleVerifier(result_bytes).result()
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
    raise ValueError("complete-five-scale independent verification failed")
